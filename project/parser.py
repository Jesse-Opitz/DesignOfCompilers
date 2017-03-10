# This will be the Parser for Design of Compilers
import os
from lexer import token
from lexer import tokens
import treelib

# P for pointer, global variable
p = 0
a = 0
def main():
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
    # Parse for Block
    if(parseBlock(token)):
        if (match(token[p].kind, 'endProgram')):
            print("Parse Complete!")
        else:
           print("Error on line " + str(token.lineNum) + ". Expecting '$', got " + token[p].character + ".")

# Block Parse: { StatementList }
def parseBlock(token):
    global p
    
    print('parse block', token[p].kind, token[p].character)
    parseBlockFirstSet = ['{']
    if token[p].character in parseBlockFirstSet:
        if(match(token[p].character, '{')):
            p = p + 1
            if(parseStatementList(token)):
                if(match(token[p].character, '}')):
                    p = p + 1
                    return True
                else:

                       print("Error on line " + str(token[p].lineNum) + ". Expecting '}', got " + token[p].character + ".")
            else:
                print('parseStatementList false')
        else:
           print("Error on line " + str(token[p].lineNum) + ". Expecting '{', got '" + token[p].character + "'.")
    
    return False

# StatementList Parse: Statement StatementList OR Epsilon/Lambda
def parseStatementList(token):
    print('parse SL', token[p].kind, token[p].character)
    StatementListFirstSet = ['keyword','char','type', 'digit', '"', '(', '==', '!=']
    if token[p].kind in StatementListFirstSet:
        if(parseStatement(token)):
            if(parseStatementList(token)):
                return True
            else:
                print('False Statement List')
                return False
        else:
            print('False Statement')
            return False
    else:
        return True
        
    
    #if(parseStatement(token)):
    #    parseStatementList(token)
    #else:
        # Epsilon/Lambda, could be nothing
    #    return True

# Statement Parse: PrintStatement OR AssignemntStatement OR VarDecl OR WhileStatement OR IfStatement OR Block
def parseStatement(token):
    print('parse S', token[p].kind, token[p].character)
    
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

    return False

# PrintStatement Parse: print ( Expr )
def parsePrintStatement(token):
    global p
    
    print('parse PS', token[p].kind, token[p].character)
    
    if(match(token[p].character, 'print')):
        p = p + 1
        if(match(token[p].character, '(')):
            p = p + 1
            if(parseExpr(token)):
                if(match(token[p].character, ')')):
                    p = p + 1
                    return True
                else:
                    print("Error on line " + str(token[p].lineNum) + ". Expecting ')', got " + token[p].character + ".")
        else:
           print("Error on line " + str(token[p].lineNum) + ". Expecting '(', got " + token[p].character + ".")
    #else:
       #print("Error on line " + str(token[p].lineNum) + ". Expecting 'print', got " + token[p].character + ".")

    return False

# AssignmentStatement Parse: Id = Expr
def parseAssignmentStatement(token):
    global a
    global p
    
    print('parse AS', token[p].kind, token[p].character)
    
    if(parseId(token)):
        if(match(token[p].character, '=')):
            p = p + 1
            if(parseExpr(token)):
                return True
                #print("Error on line " + str(token[p].lineNum) + ". Expecting '=', got " + token[p].character + ".")
        #else:
            #p = p - 1

    return False

#VarDecl Parse: type Id
def parseVarDecl(token):
    global p
    print('parse VD', token[p].kind, token[p].character)
    if(match(token[p].kind, 'type')):
        p = p + 1
        if(parseId(token)):
            return True
    #else:
        #print("Error on line " + str(token[p].lineNum) + ". Expecting 'int', 'string' or 'boolean', got " + token[p].character + ".")

    return False

# WhileStatement Parse: while BooleanExpr Block
def parseWhileStatement(token):
    global p
    print('parse WS', token[p].kind, token[p].character)
    if(match(token[p].character, 'while')):
        p = p + 1
        if(parseBooleanExpr(token)):
            if(parseBlock(token)):
                return True
    #else:
        #print("Error on line " + str(token[p].lineNum) + ". Expecting 'while', got " + token[p].character + ".")

    return False

# IfStatement Parse: if BooleanExpr Block
def parseIfStatement(token):
    global p
    print('parse IS', token[p].kind, token[p].character)
    if(match(token[p].character, 'if')):
        p = p + 1
        if(parseBooleanExpr(token)):
            if(parseBlock(token)):
                return True
    #else:
        #print("Error on line " + str(token[p].lineNum) + ". Expecting 'if', got " + token[p].character + ".")

    return False

# Expr Parse: IntExpr OR StringExpr OR BooleanExpr OR Id
def parseExpr(token):
    print('parse E', token[p].kind, token[p].character)
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
    global a
    global p
    
    print('parse IE', token[p].kind, token[p].character)
    
    # Triggers
    digitBool = False
    
    if(match(token[p].kind, 'digit')):
        digitBool = True
        p = p + 1
        # Checks for intop Expr, if they are there, return True
        if(parseIntOp(token)):
            if(parseExpr(token)):
                return True
    #else:
        #print("Error on line " + str(token[p].lineNum) + ". Expecting a digit 0-9, got " + token[p].character + ".")

    # Since intop Expr is not there, we only need to check the digit
    if(digitBool):
        return True

    return False

# StringExpr Parse: " CharList "
def parseStringExpr(token):
    global p
    print('parse SE', token[p].kind, token[p].character)
    if(match(token[p].character, '"')):
        p = p + 1
        if(parseCharList(token)):
            if(match(token[p].character, '"')):
                p = p + 1
                return True
            else:
                print("Error on line " + str(token[p].lineNum) + '. Expecting \'"\', got ' + token[p].character + ".")
    #else:
        #print("Error on line " + str(token[p].lineNum) + '. Expecting \'"\', got ' + token[p].character + ".")

    return False

# BooleanExpr Parse: ( Expr boolop Expr )
def parseBooleanExpr(token):
    global p
    print('parse BE', token[p].kind, token[p].character)
    if(match(token[p].character, '(')):
        p = p + 1
        if(parseExpr(token)):
            if(match(token[p].kind, 'compare')):
                p = p + 1
                if(parseExpr(token)):
                    if(match(token[p].character, ')')):
                        p = p + 1
                        return True
                    else:
                        print("Error on line " + str(token[p].lineNum) + ". Expecting ')', got " + token[p].character + ".")
            else:
                print("Error on line " + str(token[p].lineNum) + ". Expecting '==' or '!=', got " + token[p].character + ".")
    #else:
        #print("Error on line " + str(token[p].lineNum) + ". Expecting '(', got " + token[p].character + ".")

    return False

# Id Parse: char
# Did not return parseChar(token) because I only want to return True or False, not a possible error message
def parseId(token):
    print('parse ID', token[p].kind, token[p].character)
    if(parseChar(token)):
        return True
    
    return False

# CharList Parse: char CharList OR space CharList OR Epsilon/Lambda
# I will not need to verify 'space CharList' b/c spaces inside strings are recognized as char's in my lexer
def parseCharList(token):
    global p
    print('parse CL', token[p].kind, token[p].character)
    if(match(token[p].kind, 'char')):
        p = p + 1
        if(parseCharList(token)):
            return True
    else:
        # Epsilon/Lambda
        return True
# Char Parse: a-z
def parseChar(token):
    global p
    print('parse C', token[p].kind, token[p].character)
    if(match(token[p].kind, 'char')):
        p = p + 1
        return True

    return False

# IntOp Parse: +
# This is here in case the language needs more operators
def parseIntOp(token):
    global p
    print('parse IO', token[p].kind, token[p].character)
    if(match(token[p].kind, 'operator')):
        p = p + 1
        return True
    #else: # Will need to add operators to error message if more operators are added
        #print("Error on line " + str(token[p].lineNum) + ". Expecting '+', got " + token[p].character + ".")

    return False

main()
