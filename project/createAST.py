# This file will create the AST from the tokens
from tree import *
import os
from lexer import tokens

# Pointer for tokens
p = 0

# Pointer for scope
#scope = -1

# Numbers to keep names different
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

# Control Parents
blockParent = "Root"

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
    if(currTok is projectedTok):
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
    if match(tokens[p].character, '{'):
        p = p + 1
        createBlock()
        if match(tokens[p].character, '}'):
            #scope = scope - 1
            if match(tokens[p].character,'$'):
                ast.add_node(tokens[p].character, 'Root')
            else:
                blockNum = blockNum - 1
                createStatementList()
        else:
            createStatementList()

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

    createStatementList()


def createStatementList():
    firstSet = ('print', 'char', 'type', 'while', 'if', '{')
    print("In StatementList")
    if(tokens[p].character in firstSet or tokens[p].kind in firstSet):
        createStatement()


def createStatement():
    global blockParent
    global p

    print("In Statement")

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

#-------
def createPrintStmt():
    global printNum

    printNum = printNum + 1
    ast.add_node('Print' + str(printNum),'Block' + str(blockNum))

#-------
# When adding char to tree, it is added as <char>,<lineNum>,<uniqueID>
# When adding value to tree, it is added as <value>,<lineNum>,<uniqueID>
#-------
def createAssignmentStmt():
    global assignNum
    global charNum
    global valNum
    global p

    assignNum = assignNum + 1
    ast.add_node('Assign' + str(assignNum),'Block' + str(blockNum))

    charNum = charNum + 1
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum)  + ',' + str(charNum) ,'Assign' + str(assignNum))

    p = p + 2

    valNum = valNum + 1
    ast.add_node(str(tokens[p].character) + ',' + str(tokens[p].lineNum)  + ',' + str(valNum), 'Assign' + str(assignNum))

    p = p + 1

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

    varDeclNum = varDeclNum + 1
    ast.add_node('varDecl' + ',' + str(varDeclNum), 'Block' + str(blockNum))

    typeNum = typeNum + 1
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(typeNum), 'varDecl' + ',' + str(varDeclNum))

    p = p + 1

    charNum = charNum + 1
    ast.add_node(tokens[p].character + ',' + str(tokens[p].lineNum) + ',' + str(charNum), 'varDecl' + ',' + str(varDeclNum))

    p = p + 1

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


main()