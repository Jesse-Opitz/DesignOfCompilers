# This will be the Parser for Design of Compilers
import os
import sys
from lexer import token
from lexer import tokens
# Code in tree is NOT mine
# The website it is from is: http://www.quesucede.com/page/show/id/python-3-tree-implementation#tree-class
# tree code created by Brett Krokamp and has not been altered by me
from tree import Tree

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
idNum = 0
quoteNum = 0
charListNum = 0
boolOpNum = 0
boolValNum = 0
charNum = 0
keywordNum = 0

brackCount = 0

blockParent = ''
exprParent = ''
idParent = ''
charParent = ''
boolExprParent = ''

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

    input("Press any key to end program")

def match(token, expected):
    if token == expected:
        print('matched', token, 'p is ', p, str(tokens[p].kind), str(tokens[p].character))
        return True

    return False

# Begin parse: Block $
def parseStart(token):
    global cst
    global blockParent
    #cst.create_node("Start", "start") # root node
    cst.add_node("Start") # root node
    blockParent = 'Start'
    # Parse for Block
    if(parseBlock(token)):
        if (match(token[p].kind, 'endProgram')):
            #cst.create_node("EOP", "EOP", parent="block1")
            #cst.create_node("$", "endProgram", parent="EOP")
            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "Start")
            print("Parse Complete!")
            #cst.show()
            cst.display("Start")
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
        cst.add_node("Block" + str(blockNum), blockParent)
        #if(blockNum > 1):
            #cst.create_node("Block", "block" + str(blockNum), parent='statement' + str(stmtNum))
        #else:
            #cst.create_node("Block", "block" + str(blockNum), parent='start')
        if(match(token[p].character, '{')):
            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "Block" + str(blockNum))
            
            brackNum = brackNum + 1 
            #cst.create_node("Bracket", "bracket" + str(brackNum), parent="block" + str(blockNum))
            #cst.create_node("{", "opBracket" + str(brackNum), parent="bracket" + str(brackNum), data=[token[p].character,token[p].lineNum])
            #brackCount = brackCount + 1
            p = p + 1
            if(parseStatementList(token)):
                if(match(token[p].character, '}')):
                    
                    #cst.add_node(str(token[p].lineNum) + token[p].character, "Block")
                    #brackNum = brackNum + 1
                    if(brackCount % 2 == 0):
                        cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "Block" + str(blockNum))
                    else:
                        cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "Block" + str(blockNum - 1))
                    #    cst.create_node("Bracket", "bracket" + str(brackNum), parent="block" + str(blockNum - 1))
                    #brackCount = brackCount + 1
                    #cst.create_node("}", "clBracket" + str(brackNum), parent="bracket" + str(brackNum), data=[token[p].character,token[p].lineNum])
                    #brackNum = brackNum + 1
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
    global stmtListNum
    
    print('parse SL', token[p].kind, token[p].character)
    
    statementListFirstSet = ['keyword','char','type', 'digit', '"', '(', '==', '!=', '{']
    if token[p].kind in statementListFirstSet or token[p].character in statementListFirstSet:
        stmtListNum = stmtListNum + 1
        cst.add_node("StatementList" + str(stmtListNum), "Block" + str(blockNum))
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
    global stmtListNum
    global blockParent
    
    print('parse S', token[p].kind, token[p].character)
    statementListFirstSet = ['keyword','char','type', 'quote', '{']
    if token[p].kind in statementListFirstSet or token[p].character in statementListFirstSet:
        #cst.create_node("Statement", "statement" + str(stmtNum), parent='block' + str(blockNum))
        stmtNum = stmtNum + 1
        cst.add_node("Statement" + str(stmtNum), "StatementList" + str(stmtListNum))
        if(parsePrintStatement(token)):
            stmtListNum = stmtListNum + 1
            return True
        if(parseAssignmentStatement(token)):
            stmtListNum = stmtListNum + 1
            return True
        if(parseVarDecl(token)):
            stmtListNum = stmtListNum + 1
            return True
        if(parseWhileStatement(token)):
            stmtListNum = stmtListNum + 1
            return True
        if(parseIfStatement(token)):
            stmtListNum = stmtListNum + 1
            return True
        if(parseBlock(token)):
            print('HERE --------------', blockParent)
            blockParent = "StatementList" + str(stmtListNum)
            print('HERE2 --------------', blockParent)
            stmtListNum = stmtListNum + 1
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
    global exprParent
    
    print('parse PS', token[p].kind, token[p].character)
    
    printStatementFirstSet = ['print']
    if token[p].character in printStatementFirstSet:
        cst.add_node("PrintStmt" + str(printStmtNum), "Statement" + str(stmtNum))
        #printStmtNum = printStmtNum + 1
        #cst.create_node("printStatement", "printStatement" + str(printStmtNum), parent='statement' + str(stmtNum))
        if(match(token[p].character, 'print')):
            #keywordNum = keywordNum + 1
            #cst.create_node("print", "keyword" + str(keywordNum), parent='printStatement' + str(printStmtNum))
            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "PrintStmt" + str(printStmtNum))
            p = p + 1
            if(match(token[p].character, '(')):
                cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "PrintStmt" + str(printStmtNum))
                p = p + 1
                exprParent = "PrintStmt" + str(printStmtNum)
                if(parseExpr(token)):
                    if(match(token[p].character, ')')):
                        cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "PrintStmt" + str(printStmtNum))
                        printStmtNum = printStmtNum + 1
                        #keywordNum = keywordNum + 1
                        #printNum = printNum + 1
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
    global assignNum
    global p
    global exprParent
    global idParent
    
    print('parse AS', token[p].kind, token[p].character)
    printStatementFirstSet = ['char']
    if token[p].kind in printStatementFirstSet:
        idParent = "AssignmentStmt" + str(assignNum)
        assignNum = assignNum + 1
        cst.add_node("AssignmentStmt" + str(assignNum), "PrintStmt" + str(printStmtNum))
        if(parseId(token)):
            if(match(token[p].character, '=')):
                cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "PrintStmt" + str(printStmtNum))
                p = p + 1
                exprParent = "AssignmentStmt" + str(assignNum)
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
    global varDeclNum
    global idParent
    
    print('parse VD', token[p].kind, token[p].character)
    varDeclFirstSet = ['type']
    if token[p].kind in varDeclFirstSet:
        idParent = "VarDecl" + str(varDeclNum)
        cst.add_node("VarDecl" + str(varDeclNum), "Statement" + str(stmtNum))
        if(match(token[p].kind, 'type')):
            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "VarDecl" + str(varDeclNum))
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
    global whileNum
    global boolExprParent
    
    print('parse WS', token[p].kind, token[p].character)
    
    whileStatementFirstSet = ['while']
    if token[p].character in whileStatementFirstSet:
        whileNum = whileNum + 1
        cst.add_node("WhileStmt" + str(whileNum), "Statement" + str(stmtNum))
        if(match(token[p].character, 'while')):
            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "WhileStmt" + str(whileNum))
            p = p + 1
            boolExprParent = "WhileStmt" + str(whileNum)
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
    global ifStmtNum
    global boolExprParent
    
    print('parse IS', token[p].kind, token[p].character)
    ifStatementFirstSet = ['if']
    if token[p].character in ifStatementFirstSet:
        ifStmtNum = ifStmtNum + 1
        cst.add_node("ifStmt" + str(ifStmtNum), "Statement" + str(stmtNum))
        if(match(token[p].character, 'if')):
            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "ifStmt" + str(ifStmtNum))
            p = p + 1
            boolExprParent = "ifStmt" + str(ifStmtNum)
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
    global idParent
    global exprNum
    print('parse E', token[p].kind, token[p].character)
    exprFirstSet = ['digit', 'quote', '(', 'boolval', 'char']
    if(token[p].character in exprFirstSet or token[p].kind in exprFirstSet):
        exprNum = exprNum + 1
        idParent = "Expr" + str(exprNum)
        boolExprParent = "Expr" + str(exprNum)
        cst.add_node("Expr" + str(exprNum), exprParent)
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
    global intExprNum
    
    # Triggers
    digitBool = False

    print('parse IE', token[p].kind, token[p].character)
    
    intExprFirstSet = ['digit']
    if(token[p].kind in intExprFirstSet):
        cst.add_node("IntExpr" + str(intExprNum),"Expr" + str(exprNum))
        if(match(token[p].kind, 'digit')):
            cst.add_node(str(token[p].lineNum)+ ',' + token[p].character, "IntExpr" + str(intExprNum))
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
        cst.add_node("stringExpr" + str(strExprNum), "Expr" + str(exprNum))
        if(match(token[p].character, '"')):
            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "stringExpr" + str(strExprNum))
            p = p + 1
            if(parseCharList(token)):
                if(match(token[p].character, '"')):
                    cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "stringExpr" + str(strExprNum))
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
    global boolExprNum
    global exprNum
    global exprParent
    
    print('parse BE', token[p].kind, token[p].character)

    boolExprFirstSet = ['(', 'true', 'false']
    if(token[p].character in boolExprFirstSet):
        boolExprNum = boolExprNum + 1
        cst.add_node("boolExpr" + str(boolExprNum), boolExprParent)
        if(match(token[p].character, '(')):
            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "boolExpr" + str(boolExprNum))
            p = p + 1
            exprParent = "boolExpr" + str(boolExprNum)
            if(parseExpr(token)):
                if(match(token[p].kind, 'compare')):
                    cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "boolExpr" + str(boolExprNum))
                    p = p + 1
                    if(parseExpr(token)):
                        if(match(token[p].character, ')')):
                            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "boolExpr" + str(boolExprNum))
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
    global idNum
    global charParent
    
    print('parse ID', token[p].kind, token[p].character)
    
    idFirstSet = ['char']
    if(token[p].kind in idFirstSet):
        idNum = idNum + 1
        charParent = "Id" + str(idNum)
        cst.add_node("Id" + str(idNum), idParent)
        if(parseChar(token)):
            return True
    
    return False

# CharList Parse: char CharList OR space CharList OR Epsilon/Lambda
# I will not need to verify 'space CharList' b/c spaces inside strings are recognized as char's in my lexer
def parseCharList(token):
    global cst
    global p
    global charListNum
    
    print('parse CL', token[p].kind, token[p].character)

    charListFirstSet = ['char']
    if(token[p].kind in charListFirstSet):
        charListNum = charListNum + 1
        cst.add_node("CharList" + str(charListNum), "StringExpr" + str(strExprNum))
        charParent = "CharList" + str(charListNum

                                      )
        if(match(token[p].kind, 'char')):
            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, "CharList" + str(charListNum))
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
        cst.add_node('char' + str(charNum), charParent)
        if(match(token[p].kind, 'char')):
            cst.add_node(str(token[p].lineNum) + ',' + token[p].character, 'char' + str(charNum))
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
        cst.add_node(str(token[p].lineNum) + ',' + token[p].character, 'intExpr' + str(intExprNum))
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
