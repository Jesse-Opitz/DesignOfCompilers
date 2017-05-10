# This file will create the AST from the tokens
from tree import *
import re
import os

# from lexer import tokens

# Pointer for tokens
p = 0

# Pointer for scope
scope = -1

blockNum = -1
opNum = -1
compNum = -1
varDeclNum = -1
assignNum = -1
printNum = -1
whileNum = -1
ifNum = -1

# Tree var
ast = Tree()

def createAST(tokens):
  print('AST Creation --> Create AST')
  runCreateAST = False
  # Make sure there are no errors in parse and lex before creating tree
  if os.stat('errors.txt').st_size == 0:
      runCreateAST = True

  # If there are no errors continue to AST creation
  if runCreateAST:
      # Start creating the AST
      startCreateAST(tokens)
      ast.display('Program')


# Match tokens and prints out if there's a match
def match(currTok, projectedTok):
    if (currTok is projectedTok or currTok == projectedTok):
        print("AST Creation --> Matched --> " + currTok)
        return True
    return False

# Function to begin recursively creating AST
def startCreateAST(tokens):
    print('AST Creation --> Start Create AST')
    global p
    ast.add_node('Program')
    if tokens[p].character == '{':
        createBlock(tokens, 'Program')
        if match(tokens[p].character, '$'):
            print('AST Creation --> Complete')

def createBlock(tokens, parent):
    print('AST Creation --> Create Block')
    global p
    global scope
    global blockNum

    if match(tokens[p].character, '{'):
        blockNum = blockNum + 1
        p = p + 1
        scope = scope + 1
        # Stores block as Block@<scope>
        print('AST Creation --> Add "' + tokens[p].character + '" to AST')
        ast.add_node('Block@' + str(scope) + '|ui ' + str(blockNum), parent)

        createStatementList(tokens, 'Block@' + str(scope) + '|ui ' + str(blockNum))
        #print(tokens[p].character)
        if match(tokens[p].character, '}'):
            p = p + 1
            scope = scope - 1

    return

def createStatementList(tokens, parent):
    print('AST Creation --> Create Statement List')
    statementListFirstSet = ['print', 'char', 'type', 'while', 'if', '{']
    if tokens[p].character in statementListFirstSet or tokens[p].kind in statementListFirstSet:
        createStatement(tokens, parent)
        createStatementList(tokens, parent)
    else:
        return



def createStatement(tokens, parent):
    print('AST Creation --> Create Statement')
    statementFirstSet = ['print', 'char', 'type', 'while', 'if', '{']
    if match(tokens[p].character, 'print'):
        createPrintStmt(tokens, parent)
    elif match(tokens[p].kind, 'char'):
        createAssign(tokens, parent)
    elif match(tokens[p].kind, 'type'):
        createVarDeclStmt(tokens, parent)
    elif match(tokens[p].character, 'while'):
        createWhileStmt(tokens, parent)
    elif match(tokens[p].character, 'if'):
        createIfStmnt(tokens, parent)
    elif match(tokens[p].character, '{'):
        createBlock(tokens, parent)

    return

def createPrintStmt(tokens, parent):
    print('AST Creation --> Create Print Statement')
    global p
    global printNum
    printNum = printNum + 1
    if tokens[p].character == 'print':
        print('AST Creation --> Add "' + tokens[p].character + '" to AST')
        ast.add_node('Print@' + str(scope) + '|' + str(printNum), parent)
        parent = 'Print@' + str(scope) + '|' + str(printNum)
        p = p + 2

        createExpr(tokens, parent)
        p = p + 1

    return

def createAssign(tokens, parent):
    global p
    global assignNum
    assignNum = assignNum + 1
    ast.add_node('Assign@' + str(scope) + '|' + str(assignNum), parent)
    parent = 'Assign@' + str(scope) + '|' + str(assignNum)
    if tokens[p].kind == 'char':
        createId(tokens, parent)

        # Skip the =
        p = p + 1

        createExpr(tokens, parent)


def createVarDeclStmt(tokens, parent):
    global p
    global varDeclNum

    if tokens[p].kind == 'type':
        if tokens[p+1].kind == 'char':
            varDeclNum = varDeclNum + 1
            ast.add_node("VarDecl@" + str(scope) + '|' + str(varDeclNum), parent)
            parent = "VarDecl@" + str(scope) + '|' + str(varDeclNum)
            ast.add_node(tokens[p].character, parent)
            p = p + 1
            ast.add_node(tokens[p].character + '@' + str(scope), parent)
            p = p + 1


def createWhileStmt(tokens, parent):
    global p
    global whileNum
    whileNum = whileNum + 1
    print('AST Creation --> Create While Statement')
    #print(tokens[p].character)
    ast.add_node('while' + '@' + str(scope) + '|' + str(whileNum), parent)
    parent = 'while' + '@' + str(scope) + '|' + str(whileNum)
    p = p + 1
    createBoolExpr(tokens, parent)
    print(tokens[p].character)
    createBlock(tokens, parent)

    return


def createIfStmnt(tokens, parent):
    global p
    global ifNum

    #print(tokens[p].character)
    ifNum = ifNum + 1
    ast.add_node('if@' + str(scope) + '|' + str(ifNum), parent)
    parent = 'if@' + str(scope) + '|' + str(ifNum)
    p = p + 1

    createBoolExpr(tokens, parent)

    createBlock(tokens, parent)

    return

def createExpr(tokens, parent):
    print('AST Creation --> Create Expression')
    #exprFirstSet = ['digit', '"', '(', 'boolval', 'char']
    if match(tokens[p].kind, 'digit'):
        createIntExpr(tokens, parent)
    elif match(tokens[p].character, '"'):
        createStringExpr(tokens, parent)
    elif match(tokens[p].character, '(') or match(tokens[p].kind, 'boolval'):
        createBoolExpr(tokens, parent)
    elif match(tokens[p].kind, 'char'):
        createId(tokens, parent)

    return

def createIntExpr(tokens, parent):
    print('AST Creation --> Create Int Expression')
    global p
    global opNum

    if tokens[p].kind == 'digit':
        if tokens[p+1].kind == 'operator':
            opNum = opNum + 1
            createOperator('+|' + str(opNum), parent)
            parent = '+|' + str(opNum)
            print(parent)
            createDigit(tokens, parent)
            print("0: " + tokens[p - 2].character)
            print("1: " + tokens[p - 1].character)
            print("2: " + tokens[p].character)
            print("3: " + tokens[p + 1].character)
            print("4: " + tokens[p + 2].character)
            p = p + 1
            createDigit(tokens, parent)

            if tokens[p].kind == 'operator':
                #createOperator('+,' + str(opNum), parent)
                print('here' + tokens[p].character)
                opNum = opNum + 1
                ast.add_node('+|' + str(opNum), parent)
                parent = '+|' + str(opNum)
                p = p + 1
                print(tokens[p].character)
                createExpr(tokens, parent)
            createDigit(tokens, parent)

    return

def createStringExpr(tokens, parent):
    global p

    print('AST Creation --> Create String Expression')

    if tokens[p].character == '"':
        quoteCount = 1
        p = p + 1
        fullString = ''
        while tokens[p].character != '"':
            fullString = fullString + tokens[p].character
            p = p + 1

        ast.add_node(fullString, parent)

        # Skip end quote
        p = p + 1


def createBoolExpr(tokens, parent):
    global p
    global compNum
    print('AST Creation --> Create Bool Expression')
    if tokens[p].kind == 'boolval':
        print('AST Creation --> Add "' + tokens[p].character + '" to AST')
        ast.add_node(tokens[p].character, parent)
        p = p + 1
    elif tokens[p].character == '(':
        p = p + 1

        compNum = compNum + 1
        prevParent = parent
        ast.add_node('Comp' + str(compNum), parent)
        parent = 'Comp' + str(compNum)

        if tokens[p].character == '(':
            print('Boolean Hell is almost as bad as Daniel Craig at playing James Bond, please calm down.')

            exit()
        #print(tokens[p].character)
        createExpr(tokens, parent)

        #print('here')
        #print(tokens[p].character)
        tempNode = Node(tokens[p].character)
        #print(tempNode)
        #print('Comp' + str(compNum))

        ast.changeID('Comp' + str(compNum), tokens[p].character + '|' + str(compNum), prevParent)

        parent = tokens[p].character + '|' + str(compNum)

        p = p + 1
        createExpr(tokens, parent)

        if tokens[p].character == ')':
            p = p + 1


    return


def createDigit(tokens, parent):
    global p
    print('AST Creation --> Create Digit')
    print('AST Creation --> Add "' + tokens[p].character + '" to AST')
    ast.add_node(tokens[p].character, parent)
    p = p + 1

def createId(tokens, parent):
    global p
    print('AST Creation --> Create ID')
    print('AST Creation --> Add "' + tokens[p].character + '" to AST')
    ast.add_node(tokens[p].character + '@' + str(scope), parent)
    p = p + 1


def createOperator(tokens, parent):
    print('AST Creation --> Create Operator')
    ast.add_node(tokens, parent)