# This file will create the SymTree from the tokens
from tree import *
from node import *
import os
from lexer import tokens

# Pointer for tokens
p = 0

# Numbers to keep unique names


# Scope number
scope = 0

# Control Parents
scopeParent = ""


def createSymbolTree():
    global SymTree

    runCreateSymTree = False

    # Make sure there are no errors in parse and lex before creating tree
    if os.stat('errors.txt').st_size == 0:
        runCreateSymTree = True

    SymTree = Tree()

    # If there are no errors continue to SymTree creation
    if runCreateSymTree:
        # Start creating the SymTree
        runSymTree()

        # Displays the SymTree after completion
        SymTree.display('SymTree')


# Match tokens and prints out if there's a match
def match(currTok, projectedTok):
    if (currTok is projectedTok or currTok == projectedTok):
        #print("Matched --> " + currTok)
        return True
    return False


# Function to begin recursively creating SymTree
def runSymTree():
    global SymTree
    global scopeParent
    global p

    # Create SymTree node
    SymTree.add_node('SymTree')

    scopeParent = 'SymTree'

    # Logic for block
    if match(tokens[p].character, '{'):
        createBlock()
        # createStatementList()
        if match(tokens[p].character, '$'):
            print('SymTree Creation --> SymTree Complete\n')

#--------
def createBlock():
    global SymTree
    global scope
    global p

    if match(tokens[p].character, '{'):
        print('Symbol Tree --> Token >> ' + str(tokens[p].character))
        scope = scope + 1
        SymTree.add_node("Scope" + str(scope), scopeParent)
        p = p + 1
        createBlock()
    elif match(tokens[p].kind, 'type') and match(tokens[p + 1].kind, 'char'):
        print('Symbol Tree --> Found varDecl, ' + str(tokens[p].character))
        SymTree.add_node(tokens[p].character + ',' + tokens[p+1].character + ',' + str(scope), "Scope" + str(scope))
        p = p + 1
        createBlock()
    elif match(tokens[p].character, '}'):
        scope = scope - 1
        p = p + 1
    elif match(tokens[p].character, '$'):
        print('Symbol Tree --> End Symbol Tree creation')
    else:
        print('Symbol Tree --> Token >> ' + str(tokens[p].character))
        p = p + 1
        createBlock()

createSymbolTree()