# This file will create the AST from the tokens
from tree import *
import re
import os

# from lexer import tokens

# Pointer for tokens
p = 0

# Pointer for scope
scope = -1

# Numbers to keep unique names
blockNum = -1
stmtNum = -1
printNum = -1
parenNum = -1
assignNum = -1
varDeclNum = -1
typeNum = -1
exprNum = -1
whileNum = -1
boolNum = -1
ifStmtNum = -1
digitNum = -1
charNum = -1
valNum = -1
stringNum = -1
opNum = -1
plusNum = -1

tempAddDigit = ''

# Program number
progNum = 0

# Control Parents
blockParent = "Program" + str(progNum)
exprParent = ""
boolParent = ""

# Tree var
ast = Tree()


def createAST(tokens):
    global ast
    global blockNum
    global stmtNum
    global printNum
    global parenNum
    global assignNum
    global varDeclNum
    global typeNum
    global exprNum
    global whileNum
    global boolNum
    global ifStmtNum
    global digitNum

    global charNum
    global valNum
    global stringNum
    global opNum

    # Reset Values
    blockNum = -1
    stmtNum = -1
    printNum = -1
    parenNum = -1
    assignNum = -1
    varDeclNum = -1
    typeNum = -1
    exprNum = -1
    whileNum = -1
    boolNum = -1
    ifStmtNum = -1
    digitNum = -1
    charNum = -1
    valNum = -1
    stringNum = -1
    opNum = -1

    # Reset Parents
    blockParent = "Program" + str(progNum)
    exprParent = ""
    boolParent = ""

    # Make sure there are no errors in parse and lex before creating tree
    if os.stat('errors.txt').st_size == 0:
        runCreateAST = True

    # If there are no errors continue to AST creation
    if runCreateAST:
        # Start creating the AST
        startCreateAST(tokens)


# Match tokens and prints out if there's a match
def match(currTok, projectedTok):
    if (currTok is projectedTok or currTok == projectedTok):
        print("AST Creation --> Matched --> " + currTok)
        return True
    return False


# Function to begin recursively creating AST
def startCreateAST(tokens):
    global ast
    global p
    # global scope
    global blockNum
    global progNum

    print('\nProgram', progNum, '\n')

    # Create  + str(progNum) node
    ast.add_node('Program' + str(progNum))

    # Logic for block
    if match(tokens[p].character, '{'):
        createBlock(tokens)
        if match(tokens[p].character, '$'):
            ast.add_node(tokens[p].character, 'Program' + str(progNum))
            print('AST Creation --> AST Complete')
            print('\nAST ' + str(progNum) + ' Below\n')
            ast.display("Program" + str(progNum))
            # -- I am not sure why this breaks block -- for now can not create AST for multiple programs, only the first one
            try:
                if (tokens[p + 1].character == '{'):
                    progNum = progNum + 1
                    # print('here')
                    p = p + 1
                    # print(tokens[p].character)
                    startCreateAST(tokens)
            except IndexError:
                pass


def createBlock(tokens):
    global ast
    global scope
    global blockNum
    global p

    # Increment scope when creating a block
    scope = scope + 1

    blockNum = blockNum + 1

    # Add a block to the Tree
    print('AST Creation --> in block')
    ast.add_node('Block' + str(blockNum), blockParent)
    p = p + 1

    createStatementList(tokens)

    if tokens[p].character == '}':
        print('end brace')
        scope = scope - 1

        blockNum = blockNum - 1
    # Add 1 to get past end bracket
    p = p + 1




def createStatementList(tokens):
    global ast
    global p

    firstSet = ('keyword', 'char', 'type', 'while', 'if', '{')

    print('AST Creation --> in StatementList')
    print('AST Creation --> Token --> ' + tokens[p].character)

    if (tokens[p].character in firstSet or tokens[p].kind in firstSet):
        createStatement(tokens)


def createStatement(tokens):
    global ast
    global blockParent
    global p

    print('AST Creation --> in Statement')
    print('AST Creation --> Token --> ' + tokens[p].character)
    # Go to print stmnt
    if match(tokens[p].character, 'print'):
        # print('if print')
        createPrintStmt(tokens)

    # Go to assign stmnt
    elif match(tokens[p].kind, 'char') and match(tokens[p + 1].kind, 'assign'):
        # print('if assign')
        createAssignmentStmt(tokens)

    # Go to varDecl stmnt
    elif match(tokens[p].kind, 'type') and match(tokens[p + 1].kind, 'char'):
        # print('if vardecl')
        createVarDeclStmt(tokens)

    # Go to while stmnt
    elif match(tokens[p].character, 'while'):
        # print('if while')
        createWhileStmnt(tokens)

    # Go to if stmnt
    elif match(tokens[p].character, 'if'):
        # print('if if')
        createIfStmnt(tokens)

    # Go to block
    elif match(tokens[p].character, '{'):
        # print('if block')
        blockParent = "Block" + str(blockNum)
        createBlock(tokens)

    createStatementList(tokens)


# -------
# Adds print to the AST as Print<uniqueID>
# Changes parent of Expr to Print<uniqueID>
# Adds Expr as child to print
# -------
def createPrintStmt(tokens):
    global ast
    global printNum
    global exprParent
    global p

    print('AST Creation --> in print')
    print('AST Creation --> Token --> ' + tokens[p].character)

    printNum = printNum + 1
    ast.add_node('Print' + str(printNum), 'Block' + str(blockNum))

    # Have to skip over open paren
    p = p + 2

    print('AST Creation --> Token --> ' + tokens[p].character)

    # Changes parent of the expr to print
    exprParent = 'Print' + str(printNum)

    createExpr(tokens)

    # Have to skip over closing paren
    p = p + 1


# -------
# When adding char to tree, it is added as <char>,<lineNum>,<uniqueID>
# When adding value to tree, it is added as <value>,<lineNum>,<uniqueID>
# -------
def createAssignmentStmt(tokens):
    global ast
    global assignNum
    global charNum
    global valNum
    global exprParent
    global boolParent
    global p

    print('AST Creation --> in assign')

    assignNum = assignNum + 1
    ast.add_node('Assign' + str(assignNum), 'Block' + str(blockNum))
    print('AST Creation --> Token --> ' + tokens[p].character)
    charNum = charNum + 1
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(charNum), 'Assign' + str(assignNum))

    p = p + 2

    exprParent = 'Assign' + str(assignNum)

    print('AST Creation --> Token --> ' + tokens[p].character)

    # If value is a string
    if tokens[p].character == '"':
        createStringExpr(tokens)
    # If value is a digit
    elif tokens[p].kind == 'digit':
        valNum = valNum + 1
        parseDigit(tokens)
        p = p + 1
    elif tokens[p].kind == 'boolval':
        boolParent = exprParent
        createBoolExpr(tokens)
    elif tokens[p].character == '(':
        boolParent = exprParent
        createBoolExpr(tokens)

    print('AST Creation --> Token --> ' + tokens[p].character)
    # createStatementList()


# ------
# When adding varDecl to the tree, it is added as varDecl,<uniqueID>
# When adding variable type to the tree, it is added as <type>,<lineNum>,<uniqueID>
# When adding char to tree, it is added as <char>,<lineNum>,<uniqueID>
# ------
def createVarDeclStmt(tokens):
    global ast
    global typeNum
    global varDeclNum
    global charNum
    global p

    print('AST Creation --> in VarDecl')

    varDeclNum = varDeclNum + 1
    ast.add_node('varDecl' + ',' + str(varDeclNum), 'Block' + str(blockNum))
    print('AST Creation --> Token --> ' + tokens[p].character)
    typeNum = typeNum + 1
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(typeNum),
                 'varDecl' + ',' + str(varDeclNum))

    p = p + 1

    print('AST Creation --> Token --> ' + tokens[p].character)
    charNum = charNum + 1
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(charNum),
                 'varDecl' + ',' + str(varDeclNum))

    p = p + 1

    # createStatementList()


# ------
def createWhileStmnt(tokens):
    global ast
    global whileNum
    global p
    global blockParent
    global boolParent

    print('AST Creation --> in while')
    print('AST Creation --> Token --> ' + tokens[p].character)
    whileNum = whileNum + 1
    ast.add_node(tokens[p].character + str(whileNum), 'Block' + str(blockNum))

    blockParent = tokens[p].character + str(whileNum)
    boolParent = tokens[p].character + str(whileNum)

    p = p + 1
    print('AST Creation --> Token --> ' + tokens[p].character)
    createBoolExpr(tokens)

    createBlock(tokens)


# ------
# Adds if statement tree under block
# ------
def createIfStmnt(tokens):
    global ast
    global ifStmtNum
    global opNum
    global boolParent
    global blockParent
    global p

    print('AST Creation --> in if')
    print('AST Creation --> Token --> ' + tokens[p].character)

    # Add if statement
    ifStmtNum = ifStmtNum + 1
    #print(ifStmtNum)
    ast.add_node('if,' + str(tokens[p].lineNum) + ',' + str(ifStmtNum), 'Block' + str(blockNum))
    boolParent = 'if,' + str(tokens[p].lineNum) + ',' + str(ifStmtNum)
    blockParent = 'if,' + str(tokens[p].lineNum) + ',' + str(ifStmtNum)

    p = p + 1
    print('AST Creation --> Token --> ' + tokens[p].character)

    createBoolExpr(tokens)

    print('AST Creation --> Token --> ' + tokens[p].character)

    createBlock(tokens)
    #blockNum = blockNum - 1


# ------
# Figures out which expression it should go to
# ------
def createExpr(tokens):
    global ast
    global boolParent
    print('AST Creation --> in Expr')
    print('AST Creation --> Token --> ' + tokens[p].character)

    # exprFirstSet = ('digit', 'char', '"', '(', 'boolval')

    if (tokens[p].kind == 'digit'):
        createIntExpr(tokens)
    elif (tokens[p].kind == 'char'):
        createId(tokens)
    elif (tokens[p].character == '"'):
        createStringExpr(tokens)
    elif (tokens[p].character == '(' or tokens[p].kind == 'boolval'):
        boolParent = exprParent
        createBoolExpr(tokens)


# ------
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
# ------
def createIntExpr(tokens):
    global ast
    global p
    global digitNum
    global idParent

    print('AST Creation --> in intExpr')
    print('AST Creation --> Token --> ' + tokens[p].character)

    if (tokens[p].kind == 'digit' and tokens[p + 1].kind == 'operator'):
        # Add the digit to tree under exprParent
        ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(digitNum), exprParent)

        p = p + 1

        # Add operator to tree under exprParent
        # -- SINCE WE ONLY HAVE + OPERATOR ONLY HAS TO BE ADD
        ast.add_node('Add ,' + str(tokens[p].lineNum) + ',' + str(digitNum), exprParent)

        p = p + 1

        # Must go back to Expr
        createExpr(tokens)

    elif (tokens[p].kind == 'digit'):
        digitNum = digitNum + 1
        ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(digitNum), exprParent)
        p = p + 1


# ------
# Adds the char ID under exprParent
# ------
def createId(tokens):
    global ast
    global p
    global charNum

    print('AST Creation --> in id')
    print('AST Creation --> Token --> ' + tokens[p].character)

    charNum = charNum + 1
    # Add id under it's parent
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(charNum), exprParent)

    p = p + 1


# ------
# Adds the string expression under exprParent
# ------
def createStringExpr(tokens):
    global ast
    global p
    global stringNum

    print('AST Creation --> in string expr')
    print('AST Creation --> Token --> ' + tokens[p].character)

    # Skip open quote
    p = p + 1

    stringList = []

    # String goes to exprParent
    while (tokens[p].character != '"'):
        print('AST Creation --> Token --> ' + tokens[p].character)
        stringNum = stringNum + 1
        stringList.append(tokens[p].character)
        p = p + 1

    stringCombine = ''
    for x in stringList:
        stringCombine = stringCombine + x

    print('AST Creation --> Token --> ' + stringCombine)
    ast.add_node(stringCombine + ',' + str(tokens[p].lineNum) + ',' + str(stringNum), exprParent)

    # Skip end quote
    p = p + 1

    print('AST Creation --> Token --> ' + tokens[p].character)


# ------
# Adds a bool expression that is either just <boolval> or (<expr><boolop><expr>)
# ------
def createBoolExpr(tokens):
    global ast
    global p
    global boolNum
    global opNum
    global exprParent

    print('AST Creation --> in bool expr')
    print('AST Creation --> Token --> ' + tokens[p].character)
    if match(tokens[p].kind, 'boolval'):
        boolNum = boolNum + 1
        ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(boolNum), boolParent)
        p = p + 1
    elif match(tokens[p].character, '('):
        # Skip (
        p = p + 1

        # Add isEq or isNotEq
        # isEq is ==
        # isNotEq is !=
        print('AST Creation --> Token --> ' + tokens[p].character)
        opNum = opNum + 1
        if match(tokens[p + 1].character, '=='):
            ast.add_node('isEq,' + str(tokens[p + 1].lineNum) + ',' + str(opNum), boolParent)
            exprParent = 'isEq,' + str(tokens[p + 1].lineNum) + ',' + str(opNum)
            # First Expr
            createExpr(tokens)
            p = p + 1
        elif match(tokens[p + 3].character, '=='):
            ast.add_node('isEq,' + str(tokens[p + 3].lineNum) + ',' + str(opNum), boolParent)
            exprParent = 'isEq,' + str(tokens[p + 3].lineNum) + ',' + str(opNum)
            # First Expr
            createExpr(tokens)
            p = p + 3
        elif match(tokens[p + 1].character, '!='):
            ast.add_node('isNotEq,' + str(tokens[p + 1].lineNum) + ',' + str(opNum), boolParent)
            exprParent = 'isNotEq,' + str(tokens[p + 1].lineNum) + ',' + str(opNum)
            # First Expr
            createExpr(tokens)
            p = p + 1
        elif match(tokens[p + 3].character, '!='):
            ast.add_node('isNotEq,' + str(tokens[p + 3].lineNum) + ',' + str(opNum), boolParent)
            exprParent = 'isNotEq,' + str(tokens[p + 3].lineNum) + ',' + str(opNum)
            # First Expr
            createExpr(tokens)
            p = p + 3

        print('AST Creation --> Token --> ' + tokens[p].character)
        # Add Expr
        createExpr(tokens)

        # Skip )
        p = p + 1


def parseDigit(tokens):
    global p
    global tempAddDigit
    # print(tokens[p].character)
    print(tokens[p + 1].character)
    if tokens[p + 1].character == '+':
        parsePlus(tokens)
    elif tokens[p + 1].character != '+':
        # print('no')
        # print('here')
        # print(tokens[p-1].character)
        print(tokens[p].character)
        # print(tokens[p + 1].character)
        ast.add_node(str(tokens[p].character) + ',' + str(tokens[p].lineNum) + ',' + str(valNum),
                     'Assign' + str(assignNum))


def parsePlus(tokens):
    global p
    global plusNum
    global exprParent
    # print('plus here')

    if tokens[p + 1].character == '+':
        plusNum = plusNum + 1
        if plusNum > 0:
            plusParent = str(tokens[p + 1].character + ',' + str(tokens[p + 1].lineNum)) + ',' + str(plusNum - 1)
            print('hi')
        else:
            plusParent = exprParent
        print(tokens[p + 1].character, plusParent)
        ast.add_node(str(tokens[p + 1].character + ',' + str(tokens[p + 1].lineNum)) + ',' + str(plusNum), plusParent)
        ast.add_node(str(tokens[p].character + ',' + str(tokens[p].lineNum)),
                     str(tokens[p + 1].character + ',' + str(tokens[p + 1].lineNum)) + ',' + str(plusNum))
        p = p + 2
        ast.add_node(str(tokens[p].character + ',' + str(tokens[p].lineNum)),
                     str(tokens[p - 1].character + ',' + str(tokens[p - 1].lineNum)) + ',' + str(plusNum))
        parsePlus(tokens)

        # ast.display("Program0")
        # createAST(tokens)