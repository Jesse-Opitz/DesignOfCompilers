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

displayTree = False

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
        createSymTree(tokens)
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
# This function is god
# This function creates a symbol tree, while scope and type checking
# using tree traversals and regEx and of course dank memes
#--------
def createSymTree(tokens):
    global SymTree
    global scope
    global p

    if match(tokens[p].character, '{'):
        print('Symbol Tree --> New Scope Token >> ' + str(tokens[p].character))
        scope = scope + 1
        SymTree.add_node("Scope" + str(scope), scopeParent)
        p = p + 1
        createSymTree(tokens)
    elif match(tokens[p].kind, 'type') and match(tokens[p + 1].kind, 'char'):
        print('Symbol Tree --> Found varDecl -->' + str(tokens[p].character) + ',' + str(tokens[p+1].character))

        for node in SymTree.traverse('SymTree' + str(progNum)):
            charPattern = r'[,][' + tokens[p+1].character + '][,]'
            scopePattern = r'[,]' + str(scope)
            #print('Node: ' + node + ' Pattern: ' + pattern)
            if (re.search(charPattern, node, 0) and re.search(scopePattern, node, 0)):
                print('Scope Error: Variable "', tokens[p+1].character, '" is initialized a second time in the same scope, scope', str(scope), 'on line', tokens[p].lineNum, ':', tokens[p].character, tokens[p+1].character)
                errorFile = open('errors.txt', 'w')
                errorFile.write('Error while scope checking')
                exit()
        SymTree.add_node(tokens[p].character + ',' + tokens[p+1].character + ',' + str(scope), "Scope" + str(scope))
        p = p + 1
        createSymTree(tokens)
    elif match(tokens[p].kind, 'char') and match(tokens[p+1].kind, 'assign'):
        boolTypePattern = r'[n][,]' + tokens[p].character + '[,]'
        stringTypePattern = r'[g][,]' + tokens[p].character + '[,]'
        intTypePattern = r'[t][,]' + tokens[p].character + '[,]'
        for node in SymTree.traverse('SymTree' + str(progNum)):
            if(re.search(boolTypePattern, node))and re.search(r'[,]' + str(scope), node):
                if tokens[p+2].kind != 'boolval':
                    if tokens[p+2].character == '"':
                        print('Type Error: Variable "' + tokens[
                            p].character + '" is originally defined as a boolean in scope ' + str(
                            scope) + ', but is assigned a string on line ' + str(
                            tokens[p].lineNum))
                    if tokens[p+2].kind == 'digit':
                        print('Type Error: Variable "' + tokens[
                            p].character + '" is originally defined as a boolean in scope ' + str(
                            scope) + ', but is assigned a digit on line ' + str(
                            tokens[p].lineNum))
                    errorFile = open('errors.txt', 'w')
                    errorFile.write('Error while type checking')
                    exit()
            if(re.search(stringTypePattern, node))and re.search(r'[,]' + str(scope), node):
                if tokens[p+2].character != '"':
                    if tokens[p+2].kind == 'digit':
                        print('Type Error: Variable "' + tokens[p].character + '" is originally defined as a string in scope ' + str(scope) + ', but is assigned a int on line ' + str(tokens[p].lineNum))
                    elif tokens[p+2].kind == 'boolval':
                        print('Type Error: Variable "' + tokens[
                            p].character + '" is originally defined as a string in scope ' + str(scope) + ', but is assigned a boolval on line ' + str(
                            tokens[p].lineNum))
                    errorFile = open('errors.txt', 'w')
                    errorFile.write('Error while type checking')
                    exit()
            elif(re.search(intTypePattern, node))and re.search(r'[,]' + str(scope), node):
                if tokens[p+2].kind != 'digit':
                    if tokens[p+2].character == '"':
                        print('Type Error: Variable "' + tokens[p].character + '" is originally defined as an int in scope ' + str(scope) + ', but is assigned a string on line ' + str(tokens[p].lineNum))
                    elif tokens[p+2].kind == 'boolval':
                        print('Type Error: Variable "' + tokens[
                            p].character + '" is originally defined as an int in scope ' + str(scope) + ', but is assigned a boolval on line ' + str(
                            tokens[p].lineNum))
                    errorFile = open('errors.txt', 'w')
                    errorFile.write('Error while type checking')
                    exit()
        if match(tokens[p+2].character, '"'):
            print('Symbol Tree --> Found assign --> ', tokens[p].character)
            i = p + 3
            while not match(tokens[i].character, '"'):
                print('Symbol Tree --> assigned string:', tokens[i].character)
                i = i + 1
            p = i

        else:
            print('Symbol Tree --> Found assign --> ', tokens[p].character, tokens[p+2].character)
        p = p + 1
        createSymTree(tokens)
    elif match(tokens[p].character, '}'):
        print('Symbol Tree --> End Scope Token --> ' + str(tokens[p].character))
        scope = scope - 1
        p = p + 1
        createSymTree(tokens)
    elif match(tokens[p].character, '$'):
        print('Symbol Tree --> End Symbol Tree creation')
    else:
        print('Symbol Tree --> Ignored Token --> ' + str(tokens[p].character))
        p = p + 1
        createSymTree(tokens)

#createSymbolTree(tokens)
