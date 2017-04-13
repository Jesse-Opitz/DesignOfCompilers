# This file will create the AST from the tokens
from tree import *
import os
from lexer import tokens

# Pointer for tokens
p = 0

# Pointer for scope
#scope = -1

# Numbers to keep unique names
blockNum = -1
brackNum = -1
stmtListNum = -1
stmtNum = -1
printStmtNum = -1
printNum = -1
parenNum = -1
assignNum = -1
varDeclNum = -1
typeNum = -1
exprNum = -1
whileNum = -1
boolExprNum = -1
ifStmtNum = -1
intExprNum = -1
digitNum = -1
intopNum = -1
charNum = -1
valNum = -1
stringExprNum = -1

# Control Parents
blockParent = "Root"
exprParent = ""

def main():
    global ast

    runCreateAST = False

    # Make sure there are no errors in parse and lex before creating tree
    if os.stat('errors.txt').st_size == 0:
        runCreateAST = True

    ast = Tree()

    # If there are no errors continue to AST creation
    if runCreateAST:
        # Start creating the AST
        createAST()

        # Displays the AST after completion
        ast.display('Root')

# Match tokens and prints out if there's a match
def match(currTok, projectedTok):
    if(currTok is projectedTok or currTok == projectedTok):
        print("Matched --> " + currTok)
        return True
    return False

# Function to begin recursively creating AST
def createAST():
    global ast
    global p
    #global scope
    global blockNum

    # Create root node
    ast.add_node('Root')

    # Logic for block
    if match(tokens[p].character, '{'):
        createBlock()
        #createStatementList()
        if match(tokens[p].character,'$'):
            ast.add_node(tokens[p].character, 'Root')
            print('AST Creation --> AST Complete\n')


def createBlock():
    #global scope
    global blockNum
    global p

    # Increment scope when creating a block
    #scope = scope + 1

    blockNum = blockNum + 1

    # Add a block to the Tree
    print('Added block')
    ast.add_node('Block' + str(blockNum), blockParent)
    p = p + 1

    createStatementList()

    # Add 1 to get past end bracket
    p = p + 1

    blockNum = blockNum - 1

def createStatementList():
    global p

    firstSet = ('keyword', 'char', 'type', 'while', 'if', '{')

    print("In StatementList")
    print('tokens --> ' + tokens[p].character)

    if(tokens[p].character in firstSet or tokens[p].kind in firstSet):
        createStatement()

def createStatement():
    global blockParent
    global p

    print("In Statement")
    print('tokens --> ' + tokens[p].character)
    # Go to print stmnt
    if match(tokens[p].character, 'print'):
        print('if print')
        createPrintStmt()

    # Go to assign stmnt
    elif match(tokens[p].kind, 'char') and match(tokens[p + 1].kind, 'assign'):
        print('if assign')
        createAssignmentStmt()

    # Go to varDecl stmnt
    elif match(tokens[p].kind, 'type') and match(tokens[p + 1].kind, 'char'):
        print('if vardecl')
        createVarDeclStmt()

    # Go to while stmnt
    elif match(tokens[p].character, 'while'):
        print('if while')
        createWhileStmnt()

    # Go to if stmnt
    elif match(tokens[p].character, 'if'):
        print('if if')
        createIfStmnt()

    # Go to block
    elif match(tokens[p].character, '{'):
        print('if block')
        blockParent = "Block" + str(blockNum)
        createBlock()

    createStatementList()

#-------
# Adds print to the AST as Print<uniqueID>
# Changes parent of Expr to Print<uniqueID>
# Adds Expr as child to print
#-------
def createPrintStmt():
    global printNum
    global exprParent
    global p

    print("in print")
    print('tokens --> ' + tokens[p].character)

    printNum = printNum + 1
    ast.add_node('Print' + str(printNum),'Block' + str(blockNum))

    # Have to skip over open paren
    p = p + 2

    print('tokens --> ' + tokens[p].character)

    # Changes parent of the expr to print
    exprParent = 'Print' + str(printNum)

    createExpr()

    # Have to skip over closing paren
    p = p + 1

#-------
# When adding char to tree, it is added as <char>,<lineNum>,<uniqueID>
# When adding value to tree, it is added as <value>,<lineNum>,<uniqueID>
#-------
def createAssignmentStmt():
    global assignNum
    global charNum
    global valNum
    global exprParent
    global p

    print('in assign')

    assignNum = assignNum + 1
    ast.add_node('Assign' + str(assignNum),'Block' + str(blockNum))
    print('tokens --> ' + tokens[p].character)
    charNum = charNum + 1
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum)  + ',' + str(charNum) ,'Assign' + str(assignNum))

    p = p + 2

    exprParent = 'Assign' + str(assignNum)

    # If value is a string
    if tokens[p].character == '"':
        createStringExpr()
    # If value is a digit
    elif tokens[p].kind == 'digit':
        print('tokens --> ' + tokens[p].character)
        valNum = valNum + 1
        ast.add_node(str(tokens[p].character) + ',' + str(tokens[p].lineNum)  + ',' + str(valNum), 'Assign' + str(assignNum))
        p = p + 1

    print('tokens --> ' + tokens[p].character)
    #createStatementList()

#------
# When adding varDecl to the tree, it is added as varDecl,<uniqueID>
# When adding variable type to the tree, it is added as <type>,<lineNum>,<uniqueID>
# When adding char to tree, it is added as <char>,<lineNum>,<uniqueID>
#------
def createVarDeclStmt():
    global typeNum
    global varDeclNum
    global charNum
    global p

    print('in VarDecl')

    varDeclNum = varDeclNum + 1
    ast.add_node('varDecl' + ',' + str(varDeclNum), 'Block' + str(blockNum))
    print('tokens --> ' + tokens[p].character)
    typeNum = typeNum + 1
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(typeNum), 'varDecl' + ',' + str(varDeclNum))

    p = p + 1

    print('tokens --> ' + tokens[p].character)
    charNum = charNum + 1
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(charNum), 'varDecl' + ',' + str(varDeclNum))

    p = p + 1

    #createStatementList()

#------
def createWhileStmnt():
    global whileNum

    whileNum = whileNum + 1
    ast.add_node(tokens[p].character + str(whileNum), 'Block' + str(blockNum))



#------
def createIfStmnt():
    global ifStmtNum

    ifStmtNum = ifStmtNum + 1
    ast.add_node(tokens[p].character + str(ifStmtNum), 'Block' + str(blockNum))

#------
# Figures out which expression it should go to
#------
def createExpr():

    print('in Expr')
    print('tokens --> ' + tokens[p].character)

    #exprFirstSet = ('digit', 'char', '"', '(', 'boolval')

    if(tokens[p].kind == 'digit'):
        createIntExpr()
    elif(tokens[p].kind == 'char'):
        createId()
    elif(tokens[p].character == '"'):
        createStringExpr()
    elif(tokens[p].character == '(' or tokens[p].kind == 'boolval'):
        createBoolExpr()

#------
# The only <operator> possible is +, in the AST it is changed to 'Add' to follow the principle that
# a language should not be shown in the AST.
#
# Adds a <digit> <operator> <Expr> under exprParent
# OR
# Adds <digit> under exprParent
#
# Digit is added as <digit>,<lineNum>,<uniqueID>
# Operator is added as Add,<lineNum>,<uniqueID>
# Expr is added using createExpr function
#------
def createIntExpr():
    global p
    global digitNum
    global idParent

    print('in intExpr')
    print('tokens --> ' + tokens[p].character)

    if(tokens[p].kind == 'digit' and tokens[p + 1].kind == 'operator'):
        # Add the digit to tree under exprParent
        ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(digitNum), exprParent)

        p = p + 1

        # Add operator to tree under exprParent
        # -- SINCE WE ONLY HAVE + OPERATOR ONLY HAS TO BE ADD
        ast.add_node('Add ,' + str(tokens[p].lineNum) + ',' + str(digitNum), exprParent)

        p = p + 1

        # Must go back to Expr
        createExpr()

    elif(tokens[p].kind == 'digit'):
        digitNum = digitNum + 1
        ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(digitNum), exprParent)
        p = p + 1

#------
# Adds the char ID under exprParent
#------
def createId():
    global p
    global charNum

    print('in id')
    print('tokens --> ' + tokens[p].character)

    charNum = charNum + 1
    # Add id under it's parent
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(charNum), exprParent)

    p = p + 1

#------
# Adds the string expression under exprParent
#------
def createStringExpr():
    global p
    global stringExprNum

    print('in string expr')
    print('tokens --> ' + tokens[p].character)

    # Skip open quote
    p = p + 1

    print('tokens --> ' + tokens[p].character)
    # String goes to parent
    stringExprNum = stringExprNum + 1
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(charNum), exprParent)

    # Skip end quote
    p = p + 2

    print('tokens --> ' + tokens[p].character)

#------
def createBoolExpr():
    print('in bool expr')
    print('tokens --> ' + tokens[p].character)


main()