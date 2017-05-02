# This file will create the SymTree from the tokens
from tree import *
import re
#from node import *
import os
#from lexer import tokens

# Pointer for tokens
p = 0

# Scope number
scope = 0

# Control Parents
scopeParent = ""

progNum = 0

listOfAssignedVars = []
listOfDeclaredVars = []

displayTree = False

comparisonFirstSet = ['digit', '"', '(', 'boolval', 'char']

SymTree = Tree()

def createSymbolTree(tokens):
    global SymTree
    global p
    global scope
    global scopeParent
    global progNum
    global listOfAssignedVars
    global listOfDeclaredVars
    global runCreateSymTree

    # Pointer for tokens
    p = 0

    # Scope number
    scope = 0

    # Control Parents
    scopeParent = ""

    listOfAssignedVars = []
    listOfDeclaredVars = []

    runCreateSymTree = False

    # Make sure there are no errors in parse and lex before creating tree
    if os.stat('errors.txt').st_size == 0:
        runCreateSymTree = True


    # If there are no errors continue to SymTree creation
    if runCreateSymTree:
        # Start creating the SymTree
        runSymTree(tokens)

        # Displays the SymTree after completion
        i = 0
        while(i <= progNum):
            print('\n')
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
            print('Symbol Tree --> Symbol Tree Complete')

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
    global progNum

    # Block statements
    if match(tokens[p].character, '{'):
        print('Symbol Tree --> New Scope Token --> ' + str(tokens[p].character))
        scope = scope + 1
        SymTree.add_node("Scope" + str(scope), scopeParent)
        p = p + 1
        createSymTree(tokens)
    # VarDecl Statements
    elif match(tokens[p].kind, 'type') and match(tokens[p + 1].kind, 'char'):
        global listOfDeclaredVars

        listOfDeclaredVars.append(tokens[p+1].character)

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
        global listOfAssignedVars
        if tokens[p].character not in listOfDeclaredVars:
            print(listOfDeclaredVars)
            print('Undeclared variable: "' + tokens[p].character + '" on line ' + str(tokens[p].lineNum) + ' is not declared.')
            errorFile = open('errors.txt', 'w')
            errorFile.write('Error while type checking')
            exit()

        listOfAssignedVars.append(tokens[p].character)
        varType = ''
        boolTypePattern = r'[n][,]' + tokens[p].character + '[,]'
        stringTypePattern = r'[g][,]' + tokens[p].character + '[,]'
        intTypePattern = r'[t][,]' + tokens[p].character + '[,]'
        inSameScope = False
        for node in SymTree.traverse('SymTree' + str(progNum)):
            if(re.search(r'[,][' + tokens[p].character + '][,][' + str(scope) + ']' , node)):
                inSameScope = True
                #print('insamescope')
        for node in SymTree.traverse('SymTree' + str(progNum)):
            # Check symbol tree for boolean declaration in same scope
            if(re.search(boolTypePattern, node))and re.search(r'[,]' + str(scope), node):
                varType = 'boolean'
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
            # Check symbol tree for string declaration in same scope
            elif(re.search(stringTypePattern, node))and re.search(r'[,]' + str(scope), node):
                varType = 'string'
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
            # Check symbol tree for int declaration in same scope
            elif(re.search(intTypePattern, node))and re.search(r'[,]' + str(scope), node):
                varType = 'int'
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
                else:
                    print('Symbol Tree --> Variable types match!')
                    break
            elif(re.search(r'[,][' + tokens[p].character + '][,]' , node) and not inSameScope):

                print('Symbol Tree --> Found assign --> ', tokens[p].character)
                #print(node)
                #print('[0-' + str(scope) + ']')
                if re.search('[b][o][o][l][e][a][n][,][a-z][,][0-' + str(scope) + ']', node):
                    varType = 'boolean'
                elif re.search('[s][t][r][i][n][g][,][a-z][,][0-' + str(scope) + ']', node):
                    varType = 'string'
                elif re.search('[i][n][t][,][a-z][,][0-' + str(scope) + ']', node):
                    varType = 'int'
                else:
                    print('Type Error: Variable ' + tokens[p].character + ' is not initialized in scope ' + str(scope) + '!')
                    errorFile = open('errors.txt', 'w')
                    errorFile.write('Error while type checking')
                    exit()

                print('Symbol Tree --> Variable type found! Type for "' + tokens[p].character + '" is ' + varType + '.')


        #print('here', varType, tokens[p + 2].kind)
        if match(tokens[p+2].character, '"') and varType == 'string':
            print('Symbol Tree --> Found assign --> ', tokens[p].character)
            i = p + 3
            while not match(tokens[i].character, '"'):
                print('Symbol Tree --> Assigned String:', tokens[i].character)
                i = i + 1
            p = i
            print('Symbol Tree --> Assignment correct type!')
            p = p + 1

        elif match(tokens[p+2].kind, 'digit') and varType == 'int':
            print('Symbol Tree --> Found assign between ', tokens[p].character, ',', tokens[p+2].character)
            if tokens[p+3].character == '+':
                if tokens[p+4].kind == 'digit':
                    print('Symbol Tree --> Assigned correct type!')
                elif tokens[p+4].character == '"':
                    print('Type Error: Error on line ' + str(tokens[p+4].lineNum) + '. Can not assign a string to an int!')
                    errorFile = open('errors.txt', 'w')
                    errorFile.write('Error while type checking')
                    exit()
            else:
                print('Symbol Tree --> Assigned correct type!')
                p = p + 2

        elif match(tokens[p+2].kind, 'boolval') and varType == 'boolean':
            print('Symbol Tree --> Found assign between ', tokens[p].character, ',', tokens[p + 2].character)
            print('Symbol Tree --> Assign correct type!')
            p = p + 2

        else:
            print('Symbol Tree --> Found assign --> ', tokens[p].character, str(tokens[p+2].character))
            print('Type Error: Assigned incorrect type on line ' + str(tokens[p].lineNum) + '! Variable ' + tokens[p].character + ' is an ' + varType + '!')
            errorFile = open('errors.txt', 'w')
            errorFile.write('Error while type checking')
            exit()
        p = p + 1


        createSymTree(tokens)
    # Bool Expr statements
    elif match(tokens[p].character, '(') and (match(tokens[p-1].character, 'if') or match(tokens[p-1].character, 'while')):
        print('Symbol Tree --> Found Bool Expr --> ' + tokens[p].character)
        p = p + 1
        #print(tokens[p].character)
        # If comparison starts with a digit
        if match(tokens[p].kind, 'digit'):
            print('Symbol Tree --> Compare Ints/digits --> ' + tokens[p].character)
            p = p + 1
            print('Symbol Tree --> Compare Ints/digits --> ' + str(tokens[p].character))
            p = p + 1
            if match(tokens[p].kind, 'digit'):
                print('Symbol Tree --> Compare Ints/digits --> ' + str(tokens[p].character))
                print('Symbol Tree --> Types Match!')
            elif match(tokens[p].kind, 'char'):
                print('Symbol Tree --> Compare Ints/digits --> ' + str(tokens[p].character))
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
                        if re.search('[i][n][t][,][a-z][,][0-' + str(scope) + ']', node):
                            print('Symbol Tree --> Types match!')
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
                    elif re.search('[,][' + tokens[p].character + '][,][' + str(scope) + ']', node):
                        print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                              tokens[p].character + '" can not compare to an int! "' + tokens[
                                  p].character + '" is a ' + node)
                        errorFile = open('errors.txt', 'w')
                        errorFile.write('Error while type checking')
                        exit()
            else:
                print('Type Error: Type mismatch on line: ' + str(
                    tokens[p].lineNum) + '. Can not compare int to a ' + tokens[p].kind)
                errorFile = open('errors.txt', 'w')
                errorFile.write('Error while type checking')
                exit()

        # If comparison is starting with a string
        elif match(tokens[p].character , '"'):
            #print('here')
            print('Symbol Tree --> Compare Strings --> ' + tokens[p].character)
            # Skip start "
            p = p + 1
            print('Symbol Tree --> Compare Strings --> ' + str(tokens[p].character))
            while(tokens[p].character != '"'):
                p = p + 1

            print('Symbol Tree --> Compare Strings --> ' + str(tokens[p].character))
            # Skip end "
            p = p + 1
            print('Symbol Tree --> Compare Strings --> ' + str(tokens[p].character))

            # Skip the compare operator
            p = p + 1
            #print('Token:' + tokens[p].character)
            if(match(tokens[p].character, '"')):
                print('Symbol Tree --> Compare Strings --> ' + str(tokens[p].character))
                # Skip start "
                p = p + 1
                stringList = []
                while (tokens[p].character != '"'):
                    print('Symbol Tree --> Compare Strings --> ' + tokens[p].character)
                    stringList.append(tokens[p].character)
                    p = p + 1


                print('Symbol Tree --> Compare Strings --> ' + str(tokens[p].character))

                # Skip end "
                p = p + 1

                print('Symbol Tree --> Compare Strings --> ' + str(tokens[p].character))
                print('Symbol Tree --> Types match!')
                # Skip end )
                p = p + 1
            elif(match(tokens[p].kind, 'char')):
                print('Symbol Tree --> Compare Strings --> ' + str(tokens[p].character))
                print('Symbol Tree --> Checking variable type...')
                inSameScope = False
                for node in SymTree.traverse('SymTree' + str(progNum)):
                    if tokens[p].character + ',' + str(scope) in node:
                        inSameScope = True
                for node in SymTree.traverse('SymTree' + str(progNum)):
                    #print(node)
                    #print(tokens[p].character + ',' + str(scope))

                    # IF id is in same scope and is correct kind
                    if match('string,' + tokens[p].character + ',' + str(scope), node):
                        print('Symbol Tree --> Types match! Found ' + node + '!')
                        # skip over id and )
                        p = p + 2
                        break
                    # IF id is NOT in same scope, but is in a parent scope and correct kind
                    elif re.search('[,][' + tokens[p].character + '][,]', node) and not inSameScope:
                        if re.search('[s][t][r][i][n][g][,][a-z][,][0-' + str(scope) + ']'
                                , node):
                            print('Symbol Tree --> Types match!')
                            # skip over id and )
                            p = p + 2
                            break
                        else:
                            print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                                  tokens[p].character + '" can not compare to an string! "' + tokens[
                                      p].character + '" is a ' + node)
                            errorFile = open('errors.txt', 'w')
                            errorFile.write('Error while type checking')
                            exit()
                    elif re.search('[,][' + tokens[p].character + '][,][' + str(scope) + ']', node):
                        print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                              tokens[p].character + '" can not compare to a string! "' + tokens[
                                  p].character + '" is a ' + node)
                        errorFile = open('errors.txt', 'w')
                        errorFile.write('Error while type checking')
                        exit()
            else:
                print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + '. Can not compare string to a/an ' + tokens[p].kind)
                errorFile = open('errors.txt', 'w')
                errorFile.write('Error while type checking')
                exit()

        # Comparing boolval to Expr
        elif(match(tokens[p].kind, 'boolval')):
            #print('here')
            print('Symbol Tree --> Compare Booleans --> ' + tokens[p].character)

            # Skip boolval
            p = p + 1
            print('Symbol Tree --> Compare Booleans --> ' + str(tokens[p].character))

            # Skip the compare operator
            p = p + 1
            #print('Token:' + tokens[p].character)
            if(match(tokens[p].kind, 'boolval')):
                print('Symbol Tree --> Compare Booleans --> ' + str(tokens[p].character))

                p = p + 1

                print('Symbol Tree --> Compare Booleans --> ' + str(tokens[p].character))
                print('Symbol Tree --> Types match!')
                # Skip end )
                p = p + 1
            elif(match(tokens[p].kind, 'char')):
                print('Symbol Tree --> Compare Booleans --> ' + str(tokens[p].character))
                print('Symbol Tree --> Checking variable type...')
                inSameScope = False
                for node in SymTree.traverse('SymTree' + str(progNum)):
                    #print(node)
                    if tokens[p].character + ',' + str(scope) in node:
                        inSameScope = True
                for node in SymTree.traverse('SymTree' + str(progNum)):
                    #print(node)
                    #print(tokens[p].character + ',' + str(scope))

                    # IF id is in same scope and is correct kind
                    if match('boolean,' + tokens[p].character + ',' + str(scope), node):
                        print('Symbol Tree --> Types match! Found ' + node + '!')
                        # skip over id and )
                        p = p + 2
                        break
                    # IF id is NOT in same scope, but is in a parent scope and correct kind
                    elif re.search('[,][' + tokens[p].character + '][,]', node) and not inSameScope:
                        if re.search('[b][o][o][l][e][a][n][,][a-z][,][0-' + str(scope) + ']', node):
                            print('Symbol Tree --> Types match!')
                            # skip over id and )
                            p = p + 2
                            break
                        else:
                            print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                                  tokens[p].character + '" can not compare to a boolean! "' + tokens[
                                      p].character + '" is a ' + node)
                            errorFile = open('errors.txt', 'w')
                            errorFile.write('Error while type checking')
                            exit()
                    elif re.search('[,][' + tokens[p].character + '][,][' + str(scope) + ']', node):
                        print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                              tokens[p].character + '" can not compare to a boolean! "' + tokens[
                                  p].character + '" is a ' + node)
                        errorFile = open('errors.txt', 'w')
                        errorFile.write('Error while type checking')
                        exit()
            else:
                print('Type Error: Type mismatch on line: ' + str(
                    tokens[p].lineNum) + '. Can not compare boolean to a/an ' + tokens[p].kind)
                errorFile = open('errors.txt', 'w')
                errorFile.write('Error while type checking')
                exit()



        # Comparing id to id/Expr
        elif (match(tokens[p].kind, 'char')):
            #print('here')
            firstVarType = ''
            print('Symbol Tree --> Compare Variables --> ' + tokens[p].character)
            print('Symbol Tree --> Checking variable type...')
            # Getting first variable type
            inSameScope = False
            for node in SymTree.traverse('SymTree' + str(progNum)):
                # print(node)
                if tokens[p].character + ',' + str(scope) in node:
                    inSameScope = True
                    if re.search('[b][o][o][l][e][a][n][,]', node):
                        firstVarType = 'boolean'
                    elif re.search('[s][t][r][i][n][g][,]', node):
                        firstVarType = 'string'
                    elif re.search('[i][n][t][,]', node):
                        firstVarType = 'int'
                    print('Symbol Tree --> Variable type found! Type for "' + tokens[p].character + '" is ' + firstVarType + '.')
                    # Skip id and compare operator
                    p = p + 1

                    print('Symbol Tree --> Compare Variables --> ' + tokens[p].character)
                    p = p + 1

                    break

            # IF the first variable is in the same scope
            if inSameScope:
                print('Symbol Tree --> Compare Variables --> ' + tokens[p].character)

                if match(tokens[p].kind, 'char'):
                    inSameScope2 = False
                    secondVarType = ''
                    for node in SymTree.traverse('SymTree' + str(progNum)):
                        #print(node)
                        if tokens[p].character + ',' + str(scope) in node:
                            inSameScope2 = True
                            if re.search('[b][o][o][l][e][a][n][,]', node):
                                secondVarType = 'boolean'
                            elif re.search('[s][t][r][i][n][g][,]', node):
                                secondVarType = 'string'
                            elif re.search('[i][n][t][,]', node):
                                secondVarType = 'int'
                            print('Symbol Tree --> Variable type found! Type for "' + tokens[p].character + '" is ' + secondVarType + '.')
                            break
                    if inSameScope2:
                        if firstVarType == secondVarType:
                            print('Symbol Tree --> Types match!')
                            p = p + 2
                        else:
                            print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                                  tokens[p].character + '" can not compare to a ' + firstVarType + '! "' + tokens[
                                      p].character + '" is a ' + secondVarType)
                            errorFile = open('errors.txt', 'w')
                            errorFile.write('Error while type checking')
                            exit()
                    else:
                        for node in SymTree.traverse('SymTree' + str(progNum)):
                            #print(node)
                            tempBreak = False
                            tempScope = scope - 1
                            while tempScope > 0:
                                #print('[,][' + tokens[p].character + '][,][' + str(tempScope) + ']', node)
                                if re.search('[,][' + tokens[p].character + '][,][' + str(tempScope) + ']',node):
                                    if re.search('[b][o][o][l][e][a][n][,]', node):
                                        secondVarType = 'boolean'
                                    elif re.search('[s][t][r][i][n][g][,]', node):
                                        secondVarType = 'string'
                                    elif re.search('[i][n][t][,]', node):
                                        secondVarType = 'int'
                                    print('Symbol Tree -->2nd Variable type found! Type for "' + tokens[
                                        p].character + '" is ' + secondVarType + '.')
                                    tempBreak = True
                                    break
                                tempScope = tempScope - 1
                            if tempBreak:
                                break

                        if firstVarType == secondVarType:
                            print('Symbol Tree --> Types match!')
                            p = p + 2
                        else:
                            print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                                  tokens[p].character + '" can not compare to a ' + firstVarType + '! "' + tokens[
                                      p].character + '" is a ' + secondVarType)
                            errorFile = open('errors.txt', 'w')
                            errorFile.write('Error while type checking')
                            exit()


                elif match(tokens[p].kind, 'boolval') or match(tokens[p].character, '('):
                    secondVarType = 'boolean'
                    if firstVarType == 'boolean':
                        print('Symbol Tree --> Types match!')
                        p = p + 2
                    else:
                        print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                              tokens[p].character + '" can not compare to a ' + firstVarType + '! "' + tokens[
                                  p].character + '" is a ' + secondVarType)
                        errorFile = open('errors.txt', 'w')
                        errorFile.write('Error while type checking')
                        exit()

                elif match(tokens[p].character, '"'):
                    secondVarType = 'string'
                    if firstVarType == 'string':

                        # Skip first "
                        p = p + 1
                        while tokens[p].character != '"':
                            print('Symbol Tree --> Full String --> ' +str(tokens[p].character))
                            p = p + 1
                        print('Symbol Tree --> Compare Variables --> "')
                        # Skip end " and )
                        p = p + 2
                        print('Symbol Tree --> Types match!')
                    else:
                        print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                              tokens[p].character + '" can not compare to a ' + firstVarType + '! "' + tokens[
                                  p].character + '" is a ' + secondVarType)
                        errorFile = open('errors.txt', 'w')
                        errorFile.write('Error while type checking')
                        exit()

                elif match(tokens[p].kind, 'digit'):
                    secondVarType = 'int'
                    if firstVarType == 'int':
                        print('Symbol Tree --> Types match!')
                        p = p + 2
                    else:
                        print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', variable "' +
                              tokens[p].character + '" can not compare to an ' + firstVarType + '! "' + tokens[
                                  p].character + '" is an ' + secondVarType)
                        errorFile = open('errors.txt', 'w')
                        errorFile.write('Error while type checking')
                        exit()

            else:
                print('Symbol Tree --> Compare Variables --> ' + tokens[p].character)
                firstVarType = ''
                for node in SymTree.traverse('SymTree' + str(progNum)):
                    # print(node)
                    tempBreak = False
                    tempScope = scope - 1
                    while tempScope > 0:
                        # print('[,][' + tokens[p].character + '][,][' + str(tempScope) + ']', node)
                        if re.search('[,][' + tokens[p].character + '][,][' + str(tempScope) + ']', node):
                            if re.search('[b][o][o][l][e][a][n][,]', node):
                                firstVarType = 'boolean'
                            elif re.search('[s][t][r][i][n][g][,]', node):
                                firstVarType = 'string'
                            elif re.search('[i][n][t][,]', node):
                                firstVarType = 'int'
                            print('Symbol Tree --> Variable type found! Type for "' + tokens[
                                p].character + '" is ' + firstVarType + '.')
                            tempBreak = True
                            break
                        tempScope = tempScope - 1
                    if tempBreak:
                        break

                # Skip first id
                p = p + 1
                print('Symbol Tree --> Compare Variables --> ' + tokens[p].character)

                # Skip compare operator
                p = p + 1
                print('Symbol Tree --> Compare Variables --> ' + tokens[p].character)

                secondVarType = ''
                fullString = ''

                if match(tokens[p].kind, 'char'):
                    inSameScope2 = False
                    secondVarType = ''
                    for node in SymTree.traverse('SymTree' + str(progNum)):
                        #print(node)
                        if tokens[p].character + ',' + str(scope) in node:
                            inSameScope2 = True
                            if re.search('[b][o][o][l][e][a][n][,]', node):
                                secondVarType = 'boolean'
                            elif re.search('[s][t][r][i][n][g][,]', node):
                                secondVarType = 'string'
                            elif re.search('[i][n][t][,]', node):
                                secondVarType = 'int'
                            print('Symbol Tree --> Variable type found! Type for "' + tokens[p].character + '" is ' + secondVarType + '.')
                            break

                    else:
                        for node in SymTree.traverse('SymTree' + str(progNum)):
                            #print(node)
                            tempBreak = False
                            tempScope = scope - 1
                            while tempScope > 0:
                                #print('[,][' + tokens[p].character + '][,][' + str(tempScope) + ']', node)
                                if re.search('[,][' + tokens[p].character + '][,][' + str(tempScope) + ']',node):
                                    if re.search('[b][o][o][l][e][a][n][,]', node):
                                        secondVarType = 'boolean'
                                    elif re.search('[s][t][r][i][n][g][,]', node):
                                        secondVarType = 'string'
                                    elif re.search('[i][n][t][,]', node):
                                        secondVarType = 'int'
                                    print('Symbol Tree -->2nd Variable type found! Type for "' + tokens[
                                        p].character + '" is ' + secondVarType + '.')
                                    tempBreak = True
                                    break
                                tempScope = tempScope - 1
                            if tempBreak:
                                break
                # ID compared to string
                elif(match(tokens[p].character, '"')):
                    secondVarType = 'string'
                    p = p + 1
                    #print(tokens[p].character)
                    while tokens[p].character != '"':
                        fullString = fullString + tokens[p].character
                        p = p + 1
                # ID compared to boolean value
                elif(match(tokens[p].kind, 'boolval')):
                    secondVarType = 'boolean'
                elif(match(tokens[p].kind, 'digit')):
                    secondVarType = 'int'

                if firstVarType == secondVarType:
                    print('Symbol Tree --> Types match!')
                    p = p + 2
                else:
                    if fullString == '':
                        print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ',' + secondVarType + ' can not compare to a ' + firstVarType + '! "' + tokens[
                                  p].character + '" is a ' + secondVarType)
                    else:
                        print('Type Error: Type mismatch on line: ' + str(tokens[p].lineNum) + ', a string can not compare to a ' + firstVarType + '! "' + fullString + '" is a ' + secondVarType)
                    errorFile = open('errors.txt', 'w')
                    errorFile.write('Error while type checking')
                    exit()
        createSymTree(tokens)

    elif tokens[p].character == 'print':
        print('Symbol Tree --> Found Print statement')
        # Skip print
        p = p + 1
        print('Symbol Tree --> Print statement --> ' + tokens[p].character)
        # Skip (
        p = p + 1
        if tokens[p].kind == 'char':
            print('Symbol Tree --> Print statement Variable --> ' + tokens[p].character)
            isFound = False
            for node in SymTree.traverse('SymTree' + str(progNum)):
                if re.search('[,][' + tokens[p].character + '][,][0-' + str(scope-1) + ']', node):
                    isFound = True
            if isFound:
                print('Symbol Tree --> Print statement variable --> Variable exists!')
            else:
                print('Error: Variable "' + tokens[p].character + '" on line ' + str(tokens[p].lineNum) + ' not found!')
                errorFile = open('errors.txt', 'w')
                errorFile.write('Error while type checking')
                exit()


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
        try:
            #print(tokens[p+1].character == '{')
            if tokens[p+1].character == '{':
                progNum = progNum + 1
                p = p + 1
                runSymTree(tokens)
        except IndexError:
            pass

    else:
        print('Symbol Tree --> Ignored Token --> ' + str(tokens[p].character))
        p = p + 1
        createSymTree(tokens)


def printWarnings():
    for var in listOfDeclaredVars:
        if var not in listOfAssignedVars:
            print('Warning: Variable "' + var + '" declared, but not assigned!')

#createSymbolTree(tokens)
