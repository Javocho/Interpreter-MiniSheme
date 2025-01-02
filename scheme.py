from antlr4 import InputStream, CommonTokenStream
from schemeLexer import schemeLexer
from schemeParser import schemeParser
from schemeVisitor import schemeVisitor
import sys
import re

SCANNING = False
LITERAL_MODE = False
# ENV[0] actua com a entorn global; push_env/pop_env per a let, lambda, etc.
ENV = [{}]
FUNCS = {}

def current_env():
    return ENV[-1]

def push_env(binds):
    """Copia l'entorn actual i afegeix binds."""
    new_e = current_env().copy()
    new_e.update(binds)
    ENV.append(new_e)

def pop_env():
    ENV.pop()

def check_syntax(txt):
    idx = txt.find('missing')
    if idx != -1:
        raise Exception(f"Error de sintaxi: {txt[idx:-1]}")

def raise_div0():
    raise Exception("Error: Divisió per zero.")

def define_var(var, val):
    """
    Defineix una variable global. Llença una excepció si ja està declarada.
    """
    if var in ENV[0]:
        raise Exception(f"ERROR: La variable '{var}' ja ha estat declarada")
    ENV[0][var] = val

def define_func(children):
    """
    (define (nom param1 param2 ...) body...)
    Es guarda a FUNCS com ([params], [body]).
    """
    sig = [x.getText() for x in children[1].instr()]
    name = sig[0]
    params = sig[1:]
    FUNCS[name] = (params, children[2:])

def eval_let(children, vis):
    """
    (let ((v1 e1) (v2 e2) ...) body...)
    Crea un entorn local amb v1=e1, v2=e2..., executa body i el destrueix.
    """
    binds_node = children[1]
    local_binds = {}
    for b in binds_node.instr():
        pair = list(b.instr())
        var_name = pair[0].getText()
        val = vis.visit(pair[1])
        local_binds[var_name] = val
    push_env(local_binds)
    result = None
    for instr in children[2:]:
        result = vis.visit(instr)
    pop_env()
    return result

def eval_cond(children, vis):
    """
    (cond ((cond1 res1) (cond2 res2) ...) )
    Executa la primera branca que el cond sigui True.
    """
    for part in children[1:]:
        sub = list(part.instr())
        if vis.visit(sub[0]):
            return vis.visit(sub[1])
    return None

def eval_if(children, vis):
    """
    (if cond expr-true expr-false)
    """
    if len(children) < 4:
        raise Exception("if requereix 3 arguments.")
    cond = vis.visit(children[1])
    return vis.visit(children[2]) if cond else vis.visit(children[3])

def call_user_func(children, visitor, fname):
    """
    Crida una funció definida per l'usuari (fname).
    FUNCS[fname] = ([params], [body]).
    """
    params, body = FUNCS[fname]
    args_visited = []
    # Avaluar cada argument
    for ch in children[1:]:
        val = visitor.visit(ch)
        if isinstance(val, str) and val in FUNCS:
            args_visited.append((val, "func"))
        else:
            args_visited.append((val, "param"))

    if len(args_visited) != len(params):
        raise Exception(f"La funció '{fname}' rep {len(params)} arg(s), "
                        f"però es van donar {len(args_visited)}.")

    # Crear entorn local: param->value
    local_env = {}
    for i, (v, kind) in enumerate(args_visited):
        if kind == "func":
            FUNCS[params[i]] = FUNCS[v]
        else:
            local_env[params[i]] = v

    push_env(local_env)
    result = None
    for instr in body:
        result = visitor.visit(instr)
    pop_env()
    return result

def scheme_str(val):
    """Converteix 'val' en una cadena amb format Scheme, 
       sense cometes inicials (') y amb parèntesi para listas."""
    if isinstance(val, bool):
        return "#t" if val else "#f"
    if isinstance(val, list):
        return "(" + " ".join(scheme_str(x) for x in val) + ")"
    return str(val)

def display(val):
    """Imprimeix el valor si SCANNING està actiu."""
    if not SCANNING:
        return
    print(scheme_str(val), end='')

def read_fn(_children, _visitor):
    r = input().strip()
    # Acceptar opcionalment un signe '-' seguit de dígits
    if re.match(r'^-?\d+$', r):
        return int(r)
    elif r.startswith("'(") and r.endswith(")"):
        contenido = r[2:-1].split()
        return [int(x) if x.isdigit() else x for x in contenido]
    return r

# Diccionari de "funcions" builtin (macros/primitives amb lambdas).
FUNCS = {
    'define':  lambda c, v: (define_func(c) if c[1].getChildCount() > 1
                             else define_var(c[1].getText(), v.visit(c[2]))),
    'let':     lambda c, v: eval_let(c, v),
    'cond':    lambda c, v: eval_cond(c, v),
    'if':      lambda c, v: eval_if(c, v),
    'display': lambda c, v: display(v.visit(c[1])),
    'read':    read_fn
}

BUILTINS = {
    '+': lambda *xs: sum(xs),
    '-': lambda *xs: xs[0] - sum(xs[1:]) if len(xs) > 1 else -xs[0],
    '*': lambda x, y: x*y,
    '/': lambda x, y: x//y if y != 0 else raise_div0(),
    'mod': lambda x, y: x % y,
    '^': lambda x, y: x ** y,
    'car': lambda l: l[0] if isinstance(l, list) and l else None,
    'cdr': lambda l: l[1:] if isinstance(l, list) and len(l) > 1 else [],
    'cons': lambda x, l: [x] + l if isinstance(l, list) else None,
    'null?': lambda l: isinstance(l, list) and len(l) == 0,
    '<': lambda a, b: a < b,  '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,  '>=': lambda a, b: a >= b,
    '<>': lambda a, b: a != b, '=': lambda a, b: a == b,
    'and': lambda *xs: all(xs),
    'or': lambda *xs: any(xs),
    'not': lambda x: not x,
    'newline': lambda: print() if SCANNING else None
}

class Visitor(schemeVisitor):
    def visitRoot(self, ctx):
        global SCANNING
        check_syntax(ctx.getText())
        # Activem SCANNING per imprimir en qualsevol moment
        SCANNING = True
        # 1) Recorrem totes les instruccions arrel
        for i in ctx.instr():
            self.visit(i)
        # 2) Si existeix main, el cridem al final
        if "main" in FUNCS:
            call_user_func(["main"], self, "main")

    def visitNested(self, ctx):
        global LITERAL_MODE
        if LITERAL_MODE:
            return self.parseData(ctx)
        c = list(ctx.instr())
        if not c:
            return None
        fn = c[0].getText()
        if fn in BUILTINS:
            args = [self.visit(x) for x in c[1:]]
            return BUILTINS[fn](*args)
        if fn in FUNCS:
            entry = FUNCS[fn]
            if callable(entry) and not isinstance(entry, tuple):
                return entry(c, self)
            return call_user_func(c, self, fn)
        raise Exception(f"Error: Funció '{fn}' no definida.")

    def visitSymbol(self, ctx):
        t = ctx.getText()
        if t in current_env():
            return current_env()[t]
        if t in ['#t', '#f']:
            return (t == '#t')
        return t

    def visitString(self, ctx):
        return ctx.getText()[1:-1]

    def visitNumber(self, ctx):
        return int(ctx.getText())

    def visitQuoted(self, ctx):
        global LITERAL_MODE
        txt = ctx.getText()
        if len(txt) > 1 and txt[1] != '(':
            raise Exception("S'esperava llista després de '")
        old = LITERAL_MODE
        LITERAL_MODE = True
        data = self.parseData(ctx.instr())
        LITERAL_MODE = old
        return data

    def parseData(self, node):
        typ = node.__class__.__name__
        if typ == "NestedContext":
            subs = node.instr()
            if not subs: return []
            return [self.parseData(s) for s in subs]
        elif typ == "QuotedContext":
            return [self.parseData(node.instr())]
        elif typ == "SymbolContext":
            txt = node.getText()
            if txt == '#t': return True
            if txt == '#f': return False
            return txt
        elif typ == "StringContext":
            return node.getText()[1:-1]
        elif typ == "NumberContext":
            return int(node.getText())
        return node.getText()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Ús: python3 scheme.py <arxiu.scm>")
        sys.exit()
    fname = sys.argv[1]
    try:
        code = open(fname).read()
    except:
        raise Exception(f"No existeix el fitxer '{fname}'")
    lexer = schemeLexer(InputStream(code))
    parser = schemeParser(CommonTokenStream(lexer))
    tree = parser.root()
    if parser.getNumberOfSyntaxErrors() == 0:
        Visitor().visit(tree)
    else:
        print("Hi ha errors de sintaxi.")
