# This file runs the compiler

from lexer import tokens
#from parser import runParses
from createAST import createAST
from createSymTable import createSymbolTree

# ---Lexer runs when tokens are imported---

# ---Start Parse---
# runParse currently does not work, not sure why?!?!?
#runParse(tokens)

# ---Start Semantic Analysis---

#print("\nAST Creation\n")
#createAST(tokens)

print("\nSymbol Tree and Table Creation\n")
createSymbolTree(tokens)


# ---Code Gen---