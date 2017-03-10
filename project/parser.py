# This will be the Parser for Design of Compilers
import os
from lexer import token
from lexer import tokens
from treelib import Node, Tree
import sys

# P for pointer, global variable
p = 0
blockNum = 0
brackNum = 0
stmtListNum = 0
stmtNum = 0
printStmtNum = 0
printNum = 0
parenNum = 0
assignNum = 0
varDeclNum = 0
typeNum = 0
exprNum = 0
whileNum = 0
boolExprNum = 0
ifstmtNum = 0
intExprNum = 0
digitNum = 0
intopNum = 0
strExprNum = 0
boolExprNum = 0
idNum = 0
quoteNum = 0
charListNum = 0
boolOpNum = 0
boolValNum = 0
charNum = 0
keywordNum = 0

brackCount = 0

blockParent = 'start'

cst = Tree()


def main():
    global cst
    runParse = False

    # Checks if errors file is empty
    # If errors file is empty, lexer had no errors
    if(os.stat("errors.txt").st_size == 0):
        runParse = True

    # Parse if there are no errors in the lexer
    if(runParse):
        parseStart(tokens)
    # Do not parse, error in lexer
    else:
        print("Error in lexer, can not run parse.")

def match(token, expected):
    if token == expected:
        print('matched', token, 'p is ', p, str(tokens[p].kind), str(tokens[p].character))
        return True

    return False

# Begin parse: Block $
def parseStart(token):
    global cst
    cst.create_node("Start", "start") # root node
    # Parse for Block
    if(parseBlock(token)):
        if (match(token[p].kind, 'endProgram')):
            cst.create_node("EOP", "EOP", parent="block1")
            cst.create_node("$", "endProgram", parent="EOP")
            print("Parse Complete!")
            cst.show()
        else:
            print("Error on line " + str(token.lineNum) + ". Expecting '$', got " + token[p].character + ".")
            endParse()
# Block Parse: { StatementList }
def parseBlock(token):
    global p
    global cst
    global brackNum
    global blockNum
    global blockParent
    global brackCount
    
    print('parse block', token[p].kind, token[p].character)
    parseBlockFirstSet = ['{']
    if token[p].character in parseBlockFirstSet:
        blockNum = blockNum + 1
        if(blockNum > 1):
            cst.create_node("Block", "block" + str(blockNum), parent='statement' + str(stmtNum))
        else:
            cst.create_node("Block", "block" + str(blockNum), parent='start')
        if(match(token[p].character, '{')):
            brackNum = brackNum + 1
            cst.create_node("Bracket", "bracket" + str(brackNum), parent="block" + str(blockNum))
            cst.create_node("{", "opBracket" + str(brackNum), parent="bracket" + str(brackNum), data=[token[p].character,token[p].lineNum])
            brackCount = brackCount + 1
            p = p + 1
            if(parseStatementList(token)):
                if(match(token[p].character, '}')):
                    brackNum = brackNum + 1
                    if(brackCount % 2 == 1):
                        cst.create_node("Bracket", "bracket" + str(brackNum), parent="block" + str(blockNum))
                    else:
                        cst.create_node("Bracket", "bracket" + str(brackNum), parent="block" + str(blockNum - 1))
                    brackCount = brackCount + 1
                    cst.create_node("}", "clBracket" + str(brackNum), parent="bracket" + str(brackNum), data=[token[p].character,token[p].lineNum])
                    brackNum = brackNum + 1
                    p = p + 1
                    return True
                else:
                    print("Error on line " + str(token[p].lineNum) + ". Expecting '}', got " + token[p].character + ".")
                    endParse()
            else:
                print('parseStatementList false')
                endParse()
        else:
            print("Error on line " + str(token[p].lineNum) + ". Expecting '{', got '" + token[p].character + "'.")
            endParse()
    return False

# StatementList Parse: Statement StatementList OR Epsilon/Lambda
def parseStatementList(token):
    global cst
    
    print('parse SL', token[p].kind, token[p].character)
    
    statementListFirstSet = ['keyword','char','type', 'digit', '"', '(', '==', '!=', '{']
    if token[p].kind in statementListFirstSet or token[p].character in statementListFirstSet:
        if(parseStatement(token)):
            if(parseStatementList(token)):
                return True
            else:
                print('Error on line', str(token[p].lineNum), '. Unexpected token:', str(token[p].character))
                endParse()
                return False
        else:
            print('Error on line', str(token[p].lineNum), '. Unexpected token:', str(token[p].character))
            endParse()
            return False
    else:
        return True

# Statement Parse: PrintStatement OR AssignemntStatement OR VarDecl OR WhileStatement OR IfStatement OR Block
def parseStatement(token):
    global cst
    global stmtNum
    global blockParent
    
    stmtNum = stmtNum + 1
    print('parse S', token[p].kind, token[p].character)
    statementListFirstSet = ['keyword','char','type', 'quote', '{']
    if token[p].kind in statementListFirstSet or token[p].character in statementListFirstSet:
        cst.create_node("Statement", "statement" + str(stmtNum), parent='block' + str(blockNum))
        if(parsePrintStatement(token)):
            return True
        if(parseAssignmentStatement(token)):
            return True
        if(parseVarDecl(token)):
            return True
        if(parseWhileStatement(token)):
            return True
        if(parseIfStatement(token)):
            return True
        if(parseBlock(token)):
            return True
    else:
        print('Error on line', str(token[p].lineNum), ': Expecting a keyword, char, type, quote or start brace, got:', token[p].character)
        endParse()
    return False

# PrintStatement Parse: print ( Expr )
def parsePrintStatement(token):
    global cst
    global p
    global printStmtNum
    global keywordNum
    global printNum
    
    print('parse PS', token[p].kind, token[p].character)
    
    printStatementFirstSet = ['print']
    if token[p].character in printStatementFirstSet:
        printStmtNum = printStmtNum + 1
        cst.create_node("printStatement", "printStatement" + str(printStmtNum), parent='statement' + str(stmtNum))
        if(match(token[p].character, 'print')):
            keywordNum = keywordNum + 1
            cst.create_node("print", "keyword" + str(keywordNum), parent='printStatement' + str(printStmtNum))
            p = p + 1
            if(match(token[p].character, '(')):
                p = p + 1
                if(parseExpr(token)):
                    if(match(token[p].character, ')')):
                        keywordNum = keywordNum + 1
                        printNum = printNum + 1
                        p = p + 1
                        return True
                    else:
                        print("Error on line " + str(token[p].lineNum) + ". Expecting ')', got " + token[p].character + ".")
                        endParse()
            else:
                print("Error on line " + str(token[p].lineNum) + ". Expecting '(', got " + token[p].character + ".")
                endParse()
    return False

# AssignmentStatement Parse: Id = Expr
def parseAssignmentStatement(token):
    global cst
    global p
    
    print('parse AS', token[p].kind, token[p].character)
    printStatementFirstSet = ['char']
    if token[p].kind in printStatementFirstSet:
        if(parseId(token)):
            if(match(token[p].character, '=')):
                p = p + 1
                if(parseExpr(token)):
                    return True                    
            elif(token[p].character is not '=' or token[p].character is not '+'):
                print("Error on line " + str(token[p].lineNum) + ". Expecting '=' or '+' or there needs to be a variable type ['string', 'int', 'boolean'] before, got " + token[p].character + ".")
                endParse()
    return False

#VarDecl Parse: type Id
def parseVarDecl(token):
    global cst
    global p
    print('parse VD', token[p].kind, token[p].character)
    varDeclFirstSet = ['type']
    if token[p].kind in varDeclFirstSet:
        if(match(token[p].kind, 'type')):
            p = p + 1
            if(parseId(token)):
                return True
        else:
            print("Error on line " + str(token[p].lineNum) + ". Expecting 'int', 'string' or 'boolean', got " + token[p].character + ".")
            endParse()
    return False

# WhileStatement Parse: while BooleanExpr Block
def parseWhileStatement(token):
    global cst
    global p
    global blockNum
    print('parse WS', token[p].kind, token[p].character)
    whileStatementFirstSet = ['while']
    if token[p].character in whileStatementFirstSet:
        if(match(token[p].character, 'while')):
            p = p + 1
            if(parseBooleanExpr(token)):
                if(parseBlock(token)):
                    return True
        else:
            print("Error on line " + str(token[p].lineNum) + ". Expecting 'while', got " + token[p].character + ".")
            endParse()
    return False

# IfStatement Parse: if BooleanExpr Block
def parseIfStatement(token):
    global cst
    global p
    print('parse IS', token[p].kind, token[p].character)
    ifStatementFirstSet = ['if']
    if token[p].character in ifStatementFirstSet:
        if(match(token[p].character, 'if')):
            p = p + 1
            if(parseBooleanExpr(token)):
                if(parseBlock(token)):
                    return True
        else:
            print("Error on line " + str(token[p].lineNum) + ". Expecting 'if', got " + token[p].character + ".")
            endParse()
    return False

# Expr Parse: IntExpr OR StringExpr OR BooleanExpr OR Id
def parseExpr(token):
    global cst
    print('parse E', token[p].kind, token[p].character)
    exprFirstSet = ['digit', 'quote', '(', 'boolval', 'char']
    if(token[p].character in exprFirstSet or token[p].kind in exprFirstSet):
        if(parseIntExpr(token)):
            return True
        elif(parseStringExpr(token)):
            return True
        elif(parseBooleanExpr(token)):
            return True
        elif(parseId(token)):
            return True

    return False

# IntExpr Parse: digit intop Expr OR digit
def parseIntExpr(token):
    global cst
    global p
    
    # Triggers
    digitBool = False

    print('parse IE', token[p].kind, token[p].character)
    
    intExprFirstSet = ['digit']
    if(token[p].kind in intExprFirstSet):
        if(match(token[p].kind, 'digit')):
            digitBool = True
            p = p + 1
            # Checks for intop Expr, if they are there, return True
            if(parseIntOp(token)):
                if(parseExpr(token)):
                    return True
        else:
            print("Error on line " + str(token[p].lineNum) + ". Expecting a digit 0-9, got " + token[p].character + ".")
            endParse()

    # Since intop Expr is not there, we only need to check the digit
    if(digitBool):
        return True

    return False

# StringExpr Parse: " CharList "
def parseStringExpr(token):
    global cst
    global p

    print('parse SE', token[p].kind, token[p].character)

    strExprFirstSet = ['"']
    if(token[p].character in strExprFirstSet):
        if(match(token[p].character, '"')):
            p = p + 1
            if(parseCharList(token)):
                if(match(token[p].character, '"')):
                    p = p + 1
                    return True
                else:
                    print("Error on line " + str(token[p].lineNum) + '. Expecting \'"\', got ' + token[p].character + ".")
        else:
            print("Error on line " + str(token[p].lineNum) + '. Expecting \'"\', got ' + token[p].character + ".")

    return False

# BooleanExpr Parse: ( Expr boolop Expr )
def parseBooleanExpr(token):
    global cst
    global p
    
    print('parse BE', token[p].kind, token[p].character)

    boolExprFirstSet = ['(', 'true', 'false']
    if(token[p].character in boolExprFirstSet):
        if(match(token[p].character, '(')):
            p = p + 1
            print('in paren')
            if(parseExpr(token)):
                print('no comp')
                if(match(token[p].kind, 'compare')):
                    print('compare')
                    p = p + 1
                    if(parseExpr(token)):
                        if(match(token[p].character, ')')):
                            p = p + 1
                            return True
                        else:
                            print("Error on line " + str(token[p].lineNum) + ". Expecting ')', got " + token[p].character + ".")
                            endParse()
                else:
                    print("Error on line " + str(token[p].lineNum) + ". Expecting '==' or '!=', got " + token[p].character + ".")
                    endParse()
        elif(match(token[p].kind, 'boolval')):
            p = p + 1
            return True
        else:
            print("Error on line " + str(token[p].lineNum) + ". Expecting '(' or boolval, got " + token[p].character + ".")
            endParse()
    return False

# Id Parse: char
# Did not return parseChar(token) because I only want to return True or False, not a possible error message
def parseId(token):
    global cst
    
    print('parse ID', token[p].kind, token[p].character)
    
    idFirstSet = ['char']
    if(token[p].kind in idFirstSet):
        if(parseChar(token)):
            return True
    
    return False

# CharList Parse: char CharList OR space CharList OR Epsilon/Lambda
# I will not need to verify 'space CharList' b/c spaces inside strings are recognized as char's in my lexer
def parseCharList(token):
    global cst
    global p
    
    print('parse CL', token[p].kind, token[p].character)

    charListFirstSet = ['char']
    if(token[p].kind in charListFirstSet):
        if(match(token[p].kind, 'char')):
            p = p + 1
            if(parseCharList(token)):
                return True
    else:
        # Epsilon/Lambda
        return True

# Char Parse: a-z
def parseChar(token):
    global cst
    global p
    
    print('parse C', token[p].kind, token[p].character)
    
    charFirstSet = ['char']
    if(token[p].kind in charFirstSet):
        if(match(token[p].kind, 'char')):
            p = p + 1
            return True

    return False

# IntOp Parse: +
# This is here in case the language needs more operators
def parseIntOp(token):
    global cst
    global p
    
    print('parse IO', token[p].kind, token[p].character)
    
    if(match(token[p].kind, 'operator')):
        p = p + 1
        return True
    elif(token[p].kind is 'assign'):
        return True
    #else: # Will need to add operators to error message if more operators are added
        #print("Error on line " + str(token[p].lineNum) + ". Expecting '=' or '+', got " + token[p].character + ".")

    return False

def endParse():
    print('Parse Failed')
    sys.exit('Parse Failed')

main()
