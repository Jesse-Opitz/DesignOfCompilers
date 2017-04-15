# This file runs the compiler

from lexer import tokens
#from parser import runParse
from createAST import createAST
from createSymTable import createSymbolTree
import os

# Must have end all function of course
# ---End all function---
def endAll():
    input('Press enter to exit')
    exit()

# ---Lexer runs when tokens are imported---

# ---Start Parse---
# runParse currently does not import or execute using exec() command, not sure why?!?!?
#runParse(tokens)
#exec('parser.py')

# For some reason, parser.py refuses to be imported. Input command to execute parser.py below
#os.system('python parser.py')

# ---Start Semantic Analysis---
#if(os.stat("errors.txt").st_size == 0):
#    print("\nAST Creation\n")
#    createAST(tokens)

if(os.stat("errors.txt").st_size == 0):
    print("\nSymbol Tree and Table Creation\n")
    createSymbolTree(tokens)


# ---Code Gen---

#endAll()


