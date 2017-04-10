# This file will create the AST from the tokens
from tree import *
import os
from lexer import tokens
from lexer import token


runCreateAST = False

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

# Control Parents
blockParent = "Root"

def main():
    global ast

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
        print('AST Creation Matched --> ', tokens[p].character, tokens[p].kind)
        return True
    return False

# Function to begin recursively creating AST
def createAST():
    global ast
    global p
    global scope

    # Create root node
    ast.add_node('Root')
    if match(tokens[p].character, '{'):
        p = p + 1
        createBlock()
        if match(tokens[p].character, '}'):
            #scope = scope - 1
            if match(tokens[p].character,'$'):
                ast.add_node(tokens[p].character, 'Root')

def createBlock():
    #global scope
    global blockNum

    # Increment scope when creating a block
    #scope = scope + 1

    blockNum = blockNum + 1

    # Add a block to the Tree
    ast.add_node('Block' + str(blockNum), blockParent)

    createStatementList()


def createStatementList():
    global p
    global blockParent

    if match(tokens[p].character, 'print'):
        createPrintStmt()
    elif match(tokens[p].kind, 'char'):
        createAssignmentStmt()
    elif match(tokens[p].kind, 'type'):
        createVarDeclStmt()
    elif match(tokens[p].character, 'while'):
        createWhileStmnt()
    elif match(tokens[p].character, 'if'):
        createIfStmnt()
    elif match(tokens[p].character, '{'):
        blockParent = "Block" + str(blockNum)
        createBlock()

#-------
def createPrintStmt():
    global printNum

    printNum = printNum + 1
    ast.add_node('Print' + str(printNum),'Block' + str(blockNum))

#-------
def createAssignmentStmt():
    global assignNum

    assignNum = assignNum + 1
    ast.add_node('Assign' + str(assignNum),'Block' + str(blockNum))

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