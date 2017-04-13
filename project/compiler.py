# This file runs the compiler

from lexer import runLexer
import parser
from createAST import createAST

tokens = runLexer()
#runParse(tokens)
print("\nAST Creation\n")
createAST(tokens)