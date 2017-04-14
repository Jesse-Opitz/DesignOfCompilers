# This file runs the compiler

from lexer import runLexer
#from parser import runParses
from createAST import createAST
from createSymTable import createSymbolTree

tokens = runLexer()
#runParse(tokens)
#print("\nAST Creation\n")
#createAST(tokens)
print("\nSymbol Tree Creation\n")
createSymbolTree(tokens)