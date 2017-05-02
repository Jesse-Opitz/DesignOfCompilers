import re

# Creates 6502alan Machine Language Instructions from a depth-first in-order traversal of an AST
def runCodeGenerator(ast, symTable):
    print("Let's gen code hoe!!!!")

    prev = ''

    code = ['00'] * 256

    # Pointer for code list
    p = 0

    # Temp Variable number
    tempVarNum = 0

    # Scope - used to keep track of scope
    scope = 0

    inVarDecl = False

    varList = []

    for node in ast.traverse('Program0'):
        #inVarDecl = True

        print('Code Gen --> Pointer --> ' + node)
        if re.search('varDecl,[0-9]', node):
            print('Code Gen --> Found VarDecl!')
            #This is a way to get children
            #print(ast.__getitem__(node).children[1])
            inVarDecl = True

        #print('inVD ' + str(inVarDecl))

        if inVarDecl:
            #print('here ' + node)
            if re.search('int,[0-9]', node):
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
                varName = str(varType) + ':' + str(currVar) + '@' + str(scope) + ',' + 'T' + str(tempVarNum) + 'XX'

                # Add variable's temporary variable to table
                varList.append(varName)
                print('Code Gen --> Variable added to variable table: ' + str(varList))

                tempVarNum = tempVarNum + 1

                inVarDecl = False

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

