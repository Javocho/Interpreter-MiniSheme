grammar scheme;

root: instr* EOF;

instr
    : '(' instr* ')'      # nested
    | QUOTE instr         # quoted
    | ID_OR_SYMBOL        # symbol
    | STRING              # string
    | NUM                 # number
    ;

QUOTE: '\''; 
ID_OR_SYMBOL: [a-zA-Z][a-zA-Z0-9_?-]* | [+\-*/<>='#]+ | '#t' | '#f';
NUM: '-'?[0-9]+; 
STRING: '"' (~["\r\n])* '"'; 
COMMENT: ';' ~[\r\n]* -> skip; 
WS: [ \t\r\n]+ -> skip; 

//agraiment a en Jordi Petit (sino aixo tindria if, let, display i tomaquet)


