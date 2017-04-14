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

comparisonFirstSet = ['digit', '"', '(', 'boolval', 'char']

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
    if (currTok == projectedTok):
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
# 1) Variable aren't redeclared in same scope,
# 2) the variable is assigned to the correct type,
# 4) Warn if declared but never initalized
# 5) Warn if initialized but never used
# 6) check parent scope if variable isn't initialized in current scope,
# 7) Check comparisons
#--------
def createSymTree(tokens):
    global SymTree
    global scope
    global p

    # Block statements
    if match(tokens[p].character, '{'):
        print('Symbol Tree --> New Scope Token --> ' + str(tokens[p].character))
        scope = scope + 1
        SymTree.add_node("Scope" + str(scope), scopeParent)
        p = p + 1
        createSymTree(tokens)
    # VarDecl Statements
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
    # Assign Statements
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
            elif(re.search(stringTypePattern, node))and re.search(r'[,]' + str(scope), node):
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
    # Bool Expr statements
    elif (tokens[p].character in comparisonFirstSet or tokens[p].kind in comparisonFirstSet) and (tokens[p+1].kind == 'compare' or tokens[p+2].kind == 'compare'):
        print('Symbol Tree --> Bool Expr --> ' + tokens[p].character)

        p = p + 1

        # If comparison starts with a digit
        if match(tokens[p].kind, 'digit'):
            print('Symbol Tree --> Compare Ints/digits --> ' + tokens[p].character)
            p = p + 1
            print('SymbolTree --> Compare Ints/digits --> ' + str(tokens[p].character))
            p = p + 1
            if match(tokens[p].kind, 'digit'):
                print('SymbolTree --> Compare Ints/digits --> ' + str(tokens[p].character))
                print('SymbolTree --> Types Match!')
            elif match(tokens[p].kind, 'char'):
                print('SymbolTree --> Compare Ints/digits --> ' + str(tokens[p].character))
                print('Symbol Tree --> Checking variable type...')
                inSameScope = False
                for node in SymTree.traverse('SymTree' + str(progNum)):
                    if tokens[p].character + ',' + str(scope) in node:
                        inSameScope = True
                for node in SymTree.traverse('SymTree' + str(progNum)):
                    #print(node)
                    #print(tokens[p].character + ',' + str(scope))

                    # IF id is in same scope and is correct kind
                    if match('int,' + tokens[p].character + ',' + str(scope), node):
                        print('Symbol Tree --> Types match! Found ' + node + '!')
                        # skip over id and )
                        p = p + 2
                        break
                    # IF id is NOT in same scope, but is in a parent scope and correct kind
                    elif re.search('[,][' + tokens[p].character + '][,]', node) and not inSameScope:
                        if re.search('[i][n][t][,]', node):
                            print('Symbol Tree --> Types match! Found ' + node + '!')
                            # skip over id and )
                            p = p + 2
                            break
                        else:
                            print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                                  tokens[p].character + '" can not compare to an int! "' + tokens[
                                      p].character + '" is a ' + node)
                            errorFile = open('errors.txt', 'w')
                            errorFile.write('Error while type checking')
                            exit()
                    #el:
                    #    print('Variable has never been declared')
                    #    exit()

                    '''print('int,' + tokens[p].character + ',' + str(scope))
                    if match(',][' + tokens[p].character + '][,][' + str(scope) + ']', node):
                        if match('int,' + tokens[p].character + ',' + str(scope),node):
                            print('Symbol Tree --> Types match!')
                            p = p + 2
                            print('Symbol Tree --> Token --> ' + tokens[p].character)
                        else:
                            print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' + tokens[p].character + '" can not compare to an int! "' + tokens[p].character + '" is a ' + node)
                            errorFile = open('errors.txt', 'w')
                            errorFile.write('Error while scope checking')
                            exit()
                    elif re.search('[,]' + tokens[p].character + '[,]', node) and not re.search('[,]' + tokens[p].character + '[,]' + str(scope), node):
                        if(re.search('int', node)):
                            print('Symbol Tree --> Types match!')
                            p = p + 2
                            print('Symbol Tree --> Token --> ' + tokens[p].character)
                        else:
                            print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                                  tokens[p].character + '" can not compare to an int! "' + tokens[
                                      p].character + '" is a ' + node)
                            errorFile = open('errors.txt', 'w')
                            errorFile.write('Error while scope checking')
                            exit()'''

        createSymTree(tokens)

    # End block
    elif match(tokens[p].character, '}'):
        print('Symbol Tree --> End Scope Token --> ' + str(tokens[p].character))
        scope = scope - 1
        p = p + 1
        createSymTree(tokens)
    # End program
    elif match(tokens[p].character, '$'):
        print('Symbol Tree --> End Symbol Token --> ' + str(tokens[p].character))
    else:
        print('Symbol Tree --> Ignored Token --> ' + str(tokens[p].character))
        p = p + 1
        createSymTree(tokens)

#createSymbolTree(tokens)
