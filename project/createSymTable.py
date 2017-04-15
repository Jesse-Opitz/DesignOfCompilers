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
        global listOfDeclaredVars

        listOfDeclaredVars.append(tokens[p+1].character + ',' + str(scope))

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

        listOfAssignedVars.append(tokens[p].character + ',' + str(scope))
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
            elif(re.search(r'[,][' + tokens[p].character + '][,]' , node)):
                print('Symbol Tree --> Found assign --> ', tokens[p].character)
                if re.search('[b][o][o][l][e][a][n][,]', node):
                    varType = 'boolean'
                elif re.search('[s][t][r][i][n][g][,]', node):
                    varType = 'string'
                elif re.search('[i][n][t][,]', node):
                    varType = 'int'
                print('Symbol Tree --> Variable type found! Type for "' + tokens[p].character + '" is ' + varType + '.')
                #p = p + 1
                #print('Symbol Tree --> Found assign --> ', tokens[p].character)




        if match(tokens[p+2].character, '"') and varType == 'string':
            print('Symbol Tree --> Found assign --> ', tokens[p].character)
            i = p + 3
            while not match(tokens[i].character, '"'):
                print('Symbol Tree --> Assigned String:', tokens[i].character)
                i = i + 1
            p = i
            print('Symbol Tree --> Assignment correct type!')
        elif match(tokens[p+2].kind, 'digit') and varType == 'int':
            print('Symbol Tree --> Found assign between ', tokens[p].character, ',', tokens[p+2].character)
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
                        if re.search('[i][n][t][,]', node):
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
                        if re.search('[s][t][r][i][n][g][,]', node):
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
                        if re.search('[b][o][o][l][e][a][n][,]', node):
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
        # Comparing id to id/Expr
        elif (match(tokens[p].kind, 'char')):
            # print('here')
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
                    print('A fucking bool Expr')
                elif match(tokens[p].character, '"'):
                    print('Great a string')

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
