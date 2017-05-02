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

# Creates 6502alan Machine Language Instructions from a depth-first in-order traversal of an AST
def runCodeGenerator(ast, symTable):
    global code
    global p
    global tempVarNum
    global scope
    global varList
    global inVarDecl
    global inAssign

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

        if inVarDecl:
            generateVarDecl(node, prev)
        elif inAssign:
            generateAssign(node, prev, ast)


        #print('Present: ' + node)
        #print('Previous: ' + prev)
        prev = node

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
        varName = str(varType) + ':' + str(currVar) + '@' + str(scope) + ',' + 'T' + str(tempVarNum) + ' XX'


        # Add variable's temporary variable to table
        varList.append(varName)
        print('Code Gen --> Variable added to variable table: ' + str(varList))

        tempVarNum = tempVarNum + 1

        inVarDecl = False

def generateAssign(node, prev, ast):
    # ***********Currently only works for INTS**************
    global code
    global p
    global inAssign

    print('Code Gen --> Generating code for assign statement...')
    # Load the accumulator
    code[p] = 'A9'
    p = p + 1

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
        code[p] = '0T'
        notInt = True
        notString = True
        notBool = False
    elif re.match('false', varValue):
        code[p] = '0F'
        notInt = True
        notString = True
        notBool = False

    elif re.match('[a-z]', varValue):
        # --------***********NEED TO MAKE STRINGS WORK***********-------
        code[p] = '0S'
        notInt = True
        notString = False
        notBool = True
    else:
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