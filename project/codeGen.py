import re

code = ['00'] * 256

# Pointer for code list
p = 0

# Pointer for dynamic variables
dp = 254

# Temp Variable number
tempVarNum = 0
tempAddNum = 0
tempStringNum = 0

# Scope - used to keep track of scope
scope = -1

# Table for variables stored as:
# <type>:<id>@<scope>,T<tempVarNum>XX
varList = []

# Table for strings stored as:
# <type>:<id>@<scope>,T<tempStringNum>XX
stringList = []
stringStartList = []

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
    for node in ast.traverse('Program0'):
        #print(node)
        print('Code Gen --> Pointer --> ' + node + ' in scope ' + str(scope))
        if re.search('Block[0-9]', node):
            scope = scope + 1
            print('Code Gen --> Found a new scope')
        # ******Multi-line comment code goes here, when I adjust AST******* IDK WHAT THIS MEANS??????
        elif re.search('varDecl,[0-9]', node):
            print('Code Gen --> Found VarDecl!')
            #This is a way to get children --REMEMBER THIS
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

    #print(varList)

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
    global dp
    global varLocList
    staticVarNum = p
    i = 0
    t = 0
    p = p + 1

    varLocList = []

    while i < len(varList):
        # <type>:<id>@<scope>,T<tempVarNum>XX
        checkString = varList[i].split(':')
        '''if checkString[0] == 'string':
            #print('string')
            #print(str(stringStartList))
            varLocList.append((varList[i].split(',')[1].split(' ')[0] + ',' + stringStartList[t]).upper())
        else:'''
        temp = varList[i].split(',')
        temp = temp[1]
        temp = temp.split(' ')
        tempHex = str(hex(p))
        tempHex = tempHex.split('x')
        tempHex = tempHex[1].upper()
        varLocList.append(str(temp[0]) + ',' + tempHex)
        p = p + 1
        i = i + 1
    #print('Var List: ' + str(varLocList))

def replaceTempLocVars():
    #global p
    global varLocList
    global strLocList
    i = 0
    while i < len(code):
        if re.match('T[0-9]', code[i]):
            for x in varLocList:
                if re.match(code[i], x):
                    temp = x.split(',')
                    #print(temp[1])
                    if len(temp[1]) == 1:
                        temp[1] = '0' + temp[1]
                    code[i] = temp[1]
                    print('HERE: ' + code[i+1])
                    if code[i+1] == 'XX':
                        code[i+1] = '00'
        i = i + 1


# Generates Op codes for Variable Declaration Statements
def generateVarDecl(node, prev):
    global code
    global p
    global tempVarNum
    global scope
    global inVarDecl
    global tempStringNum
    global stringList

    if re.search('[a-z][a-z]+,[0-9]', node):
        print('Code Gen --> Found variable type --> ' + node)
    if re.match('[a-z],[0-9],[0-9]', node):
        print('Code Gen --> Generating code for VarDecl --> ' + node)
        # --Generating op codes for Var Decl

        # Stores the actual variable
        currVarList = node.split(',')
        currVar = currVarList[0]

        # Stores the variable type
        currVarTypeList = prev.split(',')
        varType = currVarTypeList[0]

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
    global dp
    global inAssign
    global stringList
    generateAddRan = False
    addValues = []

    print('Code Gen --> Generating code for assign statement...')
    if re.search('[+]', ast.__getitem__(node).children[0]) or re.search('[+]', ast.__getitem__(node).children[1]):
        print('Dont load acc, need to add first')
        generateAddRan = True
    else:
        print('here' + ast.__getitem__(node).children[0] + ast.__getitem__(node).children[1])
        # Load the accumulator
        code[p] = 'A9'
        p = p + 1

    print('Code Gen --> Looking at children... --> ' + str(ast.__getitem__(node).children))

    varNameList = ast.__getitem__(node).children[0].split(',')
    varName = varNameList[0]

    varValueList = ast.__getitem__(node).children[1].split(',')
    varValue = varValueList[0]

    notInt = True
    notString = True
    notBool = True

    # Value loaded to accumulator
    if re.match('[0-9]', varValue):
        code[p] = '0' + str(varValue)
        notInt = False
        notString = True
        notBool = True
        print('Code Gen --> Generated "0' + str(varValue) + '" for int')
    elif re.match('true', varValue):
        code[p] = '01'
        notInt = True
        notString = True
        notBool = False
        print('Code Gen --> Generated "01" for true boolean')
    elif re.match('false', varValue):
        code[p] = '00'
        notInt = True
        notString = True
        notBool = False
        print('Code Gen --> Generated "00" for true boolean')
    elif re.match('[a-z]+[/]?', varValue):
        # --------***********NEED TO MAKE STRINGS WORK***********-------
        print('Code Gen --> Generating code for string...')
        tempCharList = list(varValue)

        i = 0
        #spaceSlash = ''
        #stringStartList.append(hex(dp).split('x')[1])
        print('Temp char list' + str(tempCharList))
        while i < len(tempCharList):
            #print('i: ' + str(i))
            temp = hex(ord(tempCharList[i]))
            temp = temp.split('x')
            temp = temp[1]
            code[dp] = temp
            dp = dp - 1
            i = i + 1
        #stringStartList.append(hex(dp+1).split('x')[1])
        code[p] = hex(dp+1).split('x')[1].upper()
        dp = dp - 1
        #print(stringStartList)

        notInt = True
        notString = False
        notBool = True
    elif re.match('[+]', varValue):
        print('Code Gen --> Hold up, there is an addition in here...')
        generateAddition(node, ast)
    else:
        print(varValue)
        # THIS CASE SHOULDN'T HAPPEN
        notInt = True
        notString = True
        notBool = True
        exit('WTF did you do?!?!?!? You broke everything...')

    if not generateAddRan:
        #print('here')
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
    print('Code Gen --> Generating code for printing this list of children ' + str(ast.__getitem__(node).children))
    if len(ast.__getitem__(node).children) == 1:
        #print('1 child')
        # Load Y register from memory
        code[p] = 'AC'
        p = p + 1

        temp = ast.__getitem__(node).children[0].split(',')
        checkString = ''
        for x in varList:
            # Choose constant from memory
            # Stored as <type>:<id>@<scope>,T<tempLocID>XX
            if re.search(temp[0] + '[@]' + str(scope),x):
                print(x)
                t = x.split(',')
                #print(str(t) + 'here')
                checkString = t[0].split(':')[0]
                t = t[1]
                t = t.split(' ')
                t = t[0]
                #print(code[p])
                code[p] = t
                #print(code[p])
                p = p + 1
                #print(t)


        if checkString == 'string':
            print('here' + str(p))
            # Load X register with 01
           # p = p + 1
            p = p + 1
            code[p] = 'A2'
            p = p + 1
            # Load Y register as constant
            code[p - 4] = 'AC'
            code[p - 2] = '00'

            code[p] = '02'
            p = p + 1

        else:
            code[p] = '00'
            p = p + 1

            # Load X register with 01
            code[p] = 'A2'
            p = p + 1

            code[p] = '01'
            p = p + 1

        #print(code[p])
        code[p] = 'FF'
        #print(code[p])
        p = p + 1
        inPrint = False

def generateAddition(node, ast):
    global p
    global tempVarNum
    global tempAddNum

    numbersToAdd = []
    print('Addition' + str(ast.__getitem__(ast.__getitem__(node).children[1]).children))
    #print(ast.__getitem__(ast.__getitem__(node).children[1]).children[1])
    i = 0
    isAPlusNested = False
    while i < len(ast.__getitem__(ast.__getitem__(node).children[1]).children):
        #print('count: ' + str(i))
        temp = ast.__getitem__(ast.__getitem__(node).children[1]).children[i].split(',')
        temp = temp[0]
        #print(temp)
        if temp != '+':
            numbersToAdd.append(temp)
        else:
            # *************** NESTED PLUS NEEDS WORK ****************
            #print('Nested +, didn"t get here yet')
            isAPlusNested = True
        i = i + 1
    if not isAPlusNested:
        #print(numbersToAdd)
        code[p] = 'A9'
        p = p + 1
        code[p] = '0' + numbersToAdd[0]
        p = p + 1

        # Store variable value in a temp location
        code[p] = '8D'
        p = p + 1
        code[p] = 'T' + str(tempVarNum)
        p = p + 1
        code[p] = 'XX'
        p = p + 1

        # Stores the variable name customized for var table
        # Stored as <type>:<id>@<scope>,T<tempLocID>XX
        varName = 'TempPlace:' + 'Temp' + str(tempAddNum) + '@' + str(scope) + ',' + 'T' + str(tempVarNum) + ' XX'
        tempAddNum = tempAddNum + 1

        # Add variable's temporary variable to table
        varList.append(varName)
        print('Code Gen --> Variable added to variable table: ' + str(varList))

        code[p] = '6D'
        p = p + 1

        code[p] = 'T' + str(tempVarNum)
        p = p + 1

        code[p] = 'XX'
        p = p + 1

        tempVarNum = tempVarNum + 1

        code[p] = '8D'
        p = p + 1

        print(str(ast.__getitem__(node).children))
        temp = ast.__getitem__(node).children[0]
        temp = temp.split(',')
        for x in varList:
            if re.search(temp[0] + '@' + str(scope), x):
                temp = x.split(',')
                temp = temp[1]
                temp = temp.split(' ')
                temp = temp[0]
        code[p] = temp
        p = p + 1

        code[p] = 'XX'
        p = p + 1

        #print(numbersToAdd)


'''        # Load accumulator with constant
        code[p] = 'A9'
        p = p + 1

        temp = hex(int(numbersToAdd[0]))
        temp = temp.split('x')
        print('Temp ' + temp[1])
        code[p] = '0' + str(temp[1])
        p = p + 1
        print('here')
'''



'''
    if re.search('[0-9],', ast.__getitem__(ast.__getitem__(node).children[1]).children[0]):
        print('its int')
        temp = ast.__getitem__(ast.__getitem__(node).children[1]).children[0].split(',')
        temp = temp[0]
        print(temp)
        numbersToAdd.append(temp)
    else:
        print('Nested +')

    if re.search('[0-9],', ast.__getitem__(ast.__getitem__(node).children[1]).children[1]):
        print('its int')
        temp = ast.__getitem__(ast.__getitem__(node).children[1]).children[1].split(',')
        temp = temp[0]
        print(temp)
        numbersToAdd.append(temp)
    else:
        print('Nested +')'''



