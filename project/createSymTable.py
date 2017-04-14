# This file will create the SymTree from the tokens
from tree import *
import re
from node import *
import os
#from lexer import tokens

# Pointer for tokens
p = 0

# Scope number
scope = 0

# Control Parents
scopeParent = ""

progNum = 0

def createSymbolTree(tokens):
    global SymTree

    runCreateSymTree = False

    # Make sure there are no errors in parse and lex before creating tree
    if os.stat('errors.txt').st_size == 0:
        runCreateSymTree = True

    SymTree = Tree()

    # If there are no errors continue to SymTree creation
    if runCreateSymTree:
        # Start creating the SymTree
        runSymTree(tokens)

        # Displays the SymTree after completion
        i = 0
        while(i <= progNum):
            SymTree.display('SymTree' + str(i))
            i = i + 1


# Match tokens and prints out if there's a match
def match(currTok, projectedTok):
    if (currTok is projectedTok or currTok == projectedTok):
        #print("Matched --> " + currTok)
        return True
    return False


# Function to begin recursively creating SymTree
def runSymTree(tokens):
    global SymTree
    global scopeParent
    global p
    global progNum

    # Create SymTree node
    SymTree.add_node('SymTree' + str(progNum))

    scopeParent = 'SymTree' + str(progNum)

    # Logic for block
    if match(tokens[p].character, '{'):
        createBlock(tokens)
        if match(tokens[p].character, '$'):
            print('Symbol Tree --> Symbol Tree Complete\n')
            #try:
            #    if tokens[p + 1].character == '{':
            #        p = p + 1
            #        progNum = progNum + 1
            #        runSymTree(tokens)
            #except IndexError:
            #    pass

#--------
def createBlock(tokens):
    global SymTree
    global scope
    global p

    if match(tokens[p].character, '{'):
        print('Symbol Tree --> New Scope Token >> ' + str(tokens[p].character))
        scope = scope + 1
        SymTree.add_node("Scope" + str(scope), scopeParent)
        p = p + 1
        createBlock(tokens)
    elif match(tokens[p].kind, 'type') and match(tokens[p + 1].kind, 'char'):
        print('Symbol Tree --> Found varDecl -->' + str(tokens[p].character) + ',' + str(tokens[p+1].character))

        for node in SymTree.traverse('SymTree' + str(progNum)):
            charPattern = r'[,][' + tokens[p+1].character + '][,]'
            scopePattern = r'[,]' + str(scope)
            #print('Node: ' + node + ' Pattern: ' + pattern)
            if (re.search(charPattern, node, 0) and re.search(scopePattern, node, 0)):
                print('Scope Error: Variable "', tokens[p+1].character, '" is initialized a second time in the same scope, scope', str(scope), 'on line', tokens[p].lineNum, ':', tokens[p].character, tokens[p+1].character)
                exit()

        SymTree.add_node(tokens[p].character + ',' + tokens[p+1].character + ',' + str(scope), "Scope" + str(scope))
        p = p + 1
        createBlock(tokens)
    elif match(tokens[p].character, '}'):
        print('Symbol Tree --> End Scope Token --> ' + str(tokens[p].character))
        scope = scope - 1
        p = p + 1
        createBlock(tokens)
    elif match(tokens[p].character, '$'):
        print('Symbol Tree --> End Symbol Tree creation')
    else:
        print('Symbol Tree --> Ignored Token --> ' + str(tokens[p].character))
        p = p + 1
        createBlock(tokens)

#createSymbolTree(tokens)
