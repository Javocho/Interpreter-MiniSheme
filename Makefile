ANTLR=antlr-4.13.2-complete.jar
NAME=scheme.g4

all: schemeLexer.py schemeParser.py schemeVisitor.py

schemeLexer.py schemeParser.py schemeVisitor.py: $(NAME)
	antlr4 -Dlanguage=Python3 -visitor -no-listener $(NAME)

clean:
	rm -rf schemeLexer.py schemeLexer.tokens schemeParser.py scheme.tokens schemeLexer.interp schemeLexer.interp __pycache__ scheme.interp schemeVisitor.py
