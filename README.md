# Mini Scheme - Pràctica LP (2024-2025 Q1)

Aquest projecte implementa un intèrpret per una versió simplificada de Scheme, un llenguatge funcional derivat de Lisp. Aquesta pràctica ha estat inspirada pel professor Jordi Petit, amb qui vam dissenyar les bases de la gramàtica a classe. Tot i que inicialment pensàvem en termes de funcions natives com `let`, `display` i `if`, ens vam adonar que aquestes no difereixen molt d’altres funcions definides, com el clàssic `mcd`. Aquest enfocament ens ha ajudat a entendre millor la simplicitat i la potència de Scheme.

## Característiques del projecte

Aquest intèrpret implementa una sèrie de característiques de Scheme, incloent:

- Operacions bàsiques com suma, resta, multiplicació, i divisó.
- Comparacions com `>`, `<`, `>=`, `<=`, `=`, `<>`.
- Definició de constants i funcions globals.
- Suport per estructures com cond, if i let.
- Manipulació de llistes: `car`, `cdr`, `cons`, `null?`.
- Suport per booleans amb `#t` i `#f`.
- Funcions d’ordre superior com `map` i `filter`.
- Entrada i sortida mitjançant `read`, `display` i `newline`.

El projecte també inclou un control bàsic d’errors per gestionar situacions com la divisó per zero o l’ús d’arguments invàlids. Tot i això, hi ha limitacions en casos com l’execució de recursions molt profundes (errors de pila).

## Particularitats del llenguatge Scheme

### Simplicitat i estructures bàsiques

Scheme es distingeix per la seva simplicitat, utilitzant expressions prefixades en lloc de notacions infixades. Per exemple:

```scheme
(+ 1 2 3) ; Resultat: 6
```

Les estructures bàsiques són composades per funcions i arguments, on la notació prefixeda facilita la manipulació recursiva i funcional.

### Manipulació de llistes

Les llistes són fonamentals en Scheme. En aquest projecte, es mostren en la forma `(1 2 3)` sense l'apòstrof inicial. Aquesta decisó simplifica les sortides i les fa més comprensibles.

Exemples d'operacions amb llistes:

- `car`: Retorna el primer element.
- `cdr`: Retorna la cua.
- `cons`: Afegir un element al principi.

### Entrada i sortida

El projecte utilitza `read` per capturar dades de l’entrada estàndard i `display` per mostrar resultats a la sortida estàndard. A més, `newline` afegeix salts de línia.

Un exemple senzill:

```scheme
(define (main)
  (display "Introdueix un nombre: ")
  (let ((x (read)))
    (display "Has introduït: ")
    (display x)
    (newline)))
```

## Jocs de proves

Els jocs de proves estan organitzats a la carpeta `tests_scm`. Cada joc de prova inclou:

- Un programa Scheme a `inputs`.
- Una sortida esperada a `outputs`.
- Si el programa utilitza `read`, també hi ha un fitxer `.in` per redirigir l'entrada.

Podeu executar-los amb:

```bash
python3 scheme.py inputs/entradaX.scm < inputs/entradaX.in
```

L’arxiu `explicacioJP` descriu detalladament cada joc de prova. 

Els jocs de proves cobreixen molts casos comuns, incloent llistes buides, valors negatius, i condicions complexes. Tot i això, el projecte pot trobar limitacions amb programes molt grans o complexos.

## Limitacions conegudes

1. **Profunditat de pila**: Els programes amb recursions molt profundes poden superar el límit de la pila de Python i generar un `RecursionError`.
2. **Gestió d’errors limitada**: Tot i que s’ha implementat un control bàsic, algunes situacions poden no estar cobertes.

## Instal·lació i execució

1. **Compilació de la gramàtica:**

   ```bash
   make
   ```

2. **Execució de l’intèrpret:**

   ```bash
   python3 scheme.py programa.scm
   ```

   Per redirigir entrada i sortida:

   ```bash
   python3 scheme.py programa.scm < entrada.txt > sortida.txt
   ```

3. **Estructura del projecte:**

   - `scheme.g4`: Gramàtica ANTLR.
   - `scheme.py`: Intèrpret principal.
   - `tests_scm`: Jocs de proves amb inputs, outputs, i arxius `.in`.

## Conclusió

Aquest projecte representa un intèrpret funcional per Mini Scheme, amb una implementació robusta i diversos jocs de proves per validar-ne el comportament. Tot i les limitacions, cobreix els casos més comuns i ofereix una base per futurs desenvolupaments i ampliacions.

