import re

code = ['00'] * 256

# Pointer for code list
p = 0

# Temp Variable number
tempVarNum = 0

# Scope - used to keep track of scope
scope = -1

# Table for variables stored as:
# <type>:<id>@<scope>,T<tempVarNum>XX
varList = []

inVarDecl = False
inAssign = False
inPrint = False

# Creates 6502alan Machine Language Instructions from a depth-first in-order traversal of an AST
def runCodeGenerator(ast, symTable):
    global code
    global p
    global tempVarNum
    global scope
    global varList
    global inVarDecl
    global inAssign
    global inPrint

    print("Let's gen code hoe!!!!")

    prev = ''
    '''
            if re.search('{', node):
                scope = scope + 1
                print('Code Gen --> Found new scope')

            elif re.search('}', node):
                scope = scope - 1
                print('Code Gen --> Found end of scope')
    '''
    for node in ast.traverse('Program0'):

        print('Code Gen --> Pointer --> ' + node + ' in scope ' + str(scope))
        if re.search('Block[0-9]', node):
            scope = scope + 1
            print('Code Gen --> Found a new scope')
        # ******Multi-line comment code goes here, when I adjust AST*******

        elif re.search('varDecl,[0-9]', node):
            print('Code Gen --> Found VarDecl!')
            #This is a way to get children
            #print(ast.__getitem__(node).children[1])
            inVarDecl = True
        elif re.search('Assign[0-9]', node):
            print('Code Gen --> Found Assign!')
            inAssign = True
        elif re.search('Print[0-9]', node):
            print('Code Gen --> Found Print!')
            inPrint = True

        if inVarDecl:
            generateVarDecl(node, prev)
        elif inAssign:
            generateAssign(node, prev, ast)
        elif inPrint:
            generatePrint(node, prev, ast)


        #print('Present: ' + node)
        #print('Previous: ' + prev)
        prev = node

    getTempLocVars()

    replaceTempLocVars()

    x = 0
    for i in range(0,8):
        #if x != 0:
        #    print(x, end='')
        print('')
        for j in range(0,32):
            print(code[x], end=" ")
            try:
                x = x + 1
            except IndexError:
                pass

    #print(x, end='')

# Gets all Temp locations used for variables, replaces them with actual locations
def getTempLocVars():
    global p
    global locList
    staticVarNum = p
    i = 0
    p = p + 1

    locList = []

    while i < len(varList):
        # <type>:<id>@<scope>,T<tempVarNum>XX
        checkString = varList[i].split(':')
        if checkString[0] != 'string':
            temp = varList[i].split(',')
            temp = temp[1]
            temp = temp.split(' ')
            tempHex = str(hex(p))
            tempHex = tempHex.split('x')
            tempHex = tempHex[1].upper()
            locList.append(str(temp[0]) + ',' + tempHex)
            p = p + 1
        i = i + 1
    print(locList)

def replaceTempLocVars():
    #global p
    global locList
    i = 0
    while i < len(code):
        if re.match('T[0-9]', code[i]):
            for x in locList:
                if re.match(code[i], x):
                    temp = x.split(',')
                    #print(temp[1])
                    if len(temp[1]) == 1:
                        temp[1] = '0' + temp[1]
                    code[i] = temp[1]
                    code[i+1] = '00'
        i = i + 1

# Generates Op codes for Variable Declaration Statements
def generateVarDecl(node, prev):
    global code
    global p
    global tempVarNum
    global scope
    global inVarDecl

    if re.search('[a-z][a-z]+,[0-9]', node):
        print('Code Gen --> Found variable type --> ' + node)
    if re.match('[a-z],[0-9],[0-9]', node):
        print('Code Gen --> Generating code for VarDecl --> ' + node)
        # --Generating op codes for Var Decl
        # Clear the accumulator
        code[p] = 'A9'
        p = p + 1
        code[p] = '00'
        p = p + 1

        # Store variable value in a temp location
        code[p] = '8D'
        p = p + 1
        code[p] = 'T' + str(tempVarNum)
        p = p + 1
        code[p] = 'XX'
        p = p + 1

        # Stores the actual variable
        currVarList = node.split(',')
        currVar = currVarList[0]

        # Stores the variable type
        currVarTypeList = prev.split(',')
        varType = currVarTypeList[0]

        # Stores the variable name customized for var table
        # Stored as <type>:<id>@<scope>,T<tempLocID>XX
        varName = str(varType) + ':' + str(currVar) + '@' + str(scope) + ',' + 'T' + str(tempVarNum) + ' XX'


        # Add variable's temporary variable to table
        varList.append(varName)
        print('Code Gen --> Variable added to variable table: ' + str(varList))

        tempVarNum = tempVarNum + 1

        inVarDecl = False

# Generates Op Codes for Assign statement
def generateAssign(node, prev, ast):
    # ***********Currently only works for INTS and BOOLS**************
    global code
    global p
    global inAssign

    addValues = []

    print('Code Gen --> Generating code for assign statement...')
    # Load the accumulator
    code[p] = 'A9'
    p = p + 1
    print('Code Gen --> Looking at children... --> ' + str(ast.__getitem__(node).children))
    varNameList = ast.__getitem__(node).children[0].split(',')
    varName = varNameList[0]

    varValueList = ast.__getitem__(node).children[1].split(',')
    varValue = varValueList[0]

    # Value loaded to accumulator
    if re.match('[0-9]', varValue):
        code[p] = '0' + str(varValue)
        notInt = False
        notString = True
        notBool = True
    elif re.match('true', varValue):
        code[p] = '01'
        notInt = True
        notString = True
        notBool = False
    elif re.match('false', varValue):
        code[p] = '00'
        notInt = True
        notString = True
        notBool = False

    elif re.match('[a-z]', varValue):
        # --------***********NEED TO MAKE STRINGS WORK***********-------
        code[p] = '0S'
        notInt = True
        notString = False
        notBool = True
    elif re.match('[+]', varValue):
        print('Code Gen --> Hold up, there is an addition in here...')
    else:
        print(varValue)
        # THIS CASE SHOULDN'T HAPPEN
        notInt = True
        notString = True
        notBool = True
        exit('WTF did you do?!?!?!? You broke everything...')

    p = p + 1

    code[p] = '8D'
    p = p + 1

    foundInScope = False

    #print(varValue)

    # Add's location of variable to code table if it is in same scope
    for i in range(0, len(varList)):
        if re.search(varName + '@' + str(scope), varList[i]):
            #print(varList[i])
            temp = varList[i].split(',')
            temp = temp[1]
            temp = temp.split(' ')
            tempLoc = temp[0]
            tempXX = temp[1]

            # Adds location of variable to the code table as T<tempVarLoc> XX
            code[p] = tempLoc
            p = p + 1
            code[p] = tempXX
            p = p + 1

            foundInScope = True
    # NOT TESTED, but should work
    # If the variable is not in the same scope, this will find it's state
    if not foundInScope:
        for i in range(0, len(varList)):
            tempScope = scope
            while tempScope > 0:
                if re.search(varName + '@' + str(tempScope), varList[i]):
                    temp = varList[i].split(',')
                    temp = temp[1]
                    temp = temp.split(' ')
                    tempLoc = temp[0]
                    tempXX = temp[1]

                    # Adds location of variable to the code table as T<tempVarLoc> XX
                    code[p] = tempLoc
                    p = p + 1
                    code[p] = tempXX
                    p = p + 1
                    break

                tempScope = tempScope - 1

    inAssign = False

def generatePrint(node, prev, ast):
    #***** CAN PRINT INTS/BOOLS *******
    global inPrint
    global p
    inPrint = False
    print(str(ast.__getitem__(node).children))
    if len(ast.__getitem__(node).children) == 1:
        print('1 child')
        # Load Y register with constant
        code[p] = 'AC'
        p = p + 1


        temp = ast.__getitem__(node).children[0].split(',')
        for x in varList:
            # Choose constant from memory
            # Stored as <type>:<id>@<scope>,T<tempLocID>XX
            if re.search(temp[0] + '[@]' + str(scope),x):
                t = x.split(',')
                t = t[1]
                t = t.split(' ')
                t = t[0]
                #print(code[p])
                code[p] = t
                #print(code[p])
                p = p + 1
                #print(t)
        code[p] = '00'
        p = p + 1

        # Load X register with 01
        code[p] = 'A2'
        p = p + 1

        code[p] = '01'
        p = p + 1

        #print(code[p])
        code[p] = 'FF'
        print(code[p])
        p = p + 1
        inPrint = False
