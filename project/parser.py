# This will be the Parser for Design of Compilers
import os
from lexer import token
from lexer import tokens

def main():
    runParse = False

    # Checks if errors file is empty
    # If errors file is empty, lexer had no errors
    if(os.stat("errors.txt").st_size == 0):
        runParse = True

    # Parse if there are no errors in the lexer
    # P for pointer
    p = 0
    if(runParse):
        while p < len(tokens):
            parseStart(tokens[p], p)
            
    # Do not parse, error in lexer
    else:
        print("Error in lexer, can not run parse.")

def match(token, expected, p):
    if token == expected:
        print('matched', token)
        p = p + 1
        return True
    
    return False
# Begin parse: Block $
def parseStart(token, p):
    
    # Parse for Block
    if(parseBlock(token, p)):
        if (match(token.kind, 'endProgram', p)):
            print("Parse Successful!")
        else:
           print("Error on line " + str(token.lineNum) + ". Expecting '$', got " + token.character + ".")

# Block Parse: { StatementList }
def parseBlock(token, p):

    if(match(token.character, '{', p)):
        if(parseStatementList(token, p)):
            if(match(token.character, '}', p)):
                return True
            else:
                   print("Error on line " + str(token.lineNum) + ". Expecting '}', got " + token.character + ".")
    else:
       print("Error on line " + str(token.lineNum) + ". Expecting '{', got '" + token.character + "'.")

    return False

# StatementList Parse: Statement StatementList OR Epsilon/Lambda
def parseStatementList(token, p):
    if(parseStatement(token, p)):
        parseStatementList(token,p)
    else:
        # Epsilon/Lambda, could be nothing
        return True

# Statement Parse: PrintStatement OR AssignemntStatement OR VarDecl OR WhileStatement OR IfStatement OR Block
def parseStatement(token, p):
    if(parsePrintStatement(token, p)):
        return True
    elif(parseAssignmentStatement(token, p)):
        return True
    elif(parseVarDecl(token, p)):
        return True
    elif(parseWhileStatement(token, p)):
        return True
    elif(parseIfStatement(token, p)):
        return True
    elif(parseBlock(token, p)):
        return True

    return False

# PrintStatement Parse: print ( Expr )
def parsePrintStatement(token, p):
    if(match(token.character, 'print', p)):
        if(match(token.character, '(', p)):
            if(parseExpr(token, p)):
                    if(match(token.character, ')', p)):
                        return True
                    else:
                        print("Error on line " + str(token.lineNum) + ". Expecting ')', got " + token.character + ".")
        else:
           print("Error on line " + str(token.lineNum) + ". Expecting '(', got " + token.character + ".")
    else:
       print("Error on line " + str(token.lineNum) + ". Expecting 'print', got " + token.character + ".")

    return False

# AssignmentStatement Parse: Id = Expr
def parseAssignmentStatement(token, p):
    if(parseId(token, p)):
        if(match(token.character, '=', p)):
            if(parseExpr(token,p)):
                return True
        else:
            print("Error on line " + str(token.lineNum) + ". Expecting '=', got " + token.character + ".")

    return False

#VarDecl Parse: type Id
def parseVarDecl(token, p):
    if(match(token.kind, 'type', p)):
        if(parseId(token, p)):
            return True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting 'int', 'string' or 'boolean', got " + token.character + ".")

    return False

# WhileStatement Parse: while BooleanExpr Block
def parseWhileStatement(token, p):
    if(match(token.character, 'while', p)):
        if(parseBooleanExpr(token, p)):
            if(parseBlock(token, p)):
                return True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting 'while', got " + token.character + ".")

    return False

# IfStatement Parse: if BooleanExpr Block
def parseIfStatement(token, p):
    if(match(token.character, 'if')):
        if(parseBooleanExpr(token, p)):
            if(parseBlock(token, p)):
                return True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting 'if', got " + token.character + ".")

    return False

# Expr Parse: IntExpr OR StringExpr OR BooleanExpr OR Id
def parseExpr(token, p):
    if(parseIntExpr(token, p)):
        return True
    elif(parseStringExpr(token, p)):
        return True
    elif(parseBooleanExpr(token, p)):
        return True
    elif(parseId(token, p)):
        return True

    return False

# IntExpr Parse: digit intop Expr OR digit
def parseIntExpr(token, p):
    # Triggers
    digitBool = False
    
    if(match(token.kind, 'digit', p)):
        digitBool = True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting a digit 0-9, got " + token.character + ".")

    # Checks for intop Expr, if they are there, return True
    if(parseIntOp(token, p)):
        if(parseExpr(token, p)):
            return True

    # Since intop Expr is not there, we only need to check the digit
    if(digitBool):
        return True

    return False

# StringExpr Parse: " CharList "
def parseStringExpr(token, p):
    # Triggers
    opQuote = False
    charList = False
    clQuote = False

    if(match(token.character, '"', p)):
        if(parseCharList(token, p)):
            if(match(token.character, '"', p)):
                return True
            else:
                print("Error on line " + str(token.lineNum) + '. Expecting \'"\', got ' + token.character + ".")
    else:
        print("Error on line " + str(token.lineNum) + '. Expecting \'"\', got ' + token.character + ".")

    return False

# BooleanExpr Parse: ( Expr boolop Expr )
def parseBooleanExpr(token, p):
    if(match(token.character, '(', p)):
        if(parseExpr(token, p)):
            if(match(token.kind, 'compare', p)):
                if(parseExpr(token, p)):
                    if(match(token.character, ')', p)):
                        return True
                    else:
                        print("Error on line " + str(token.lineNum) + ". Expecting ')', got " + token.character + ".")
            else:
                print("Error on line " + str(token.lineNum) + ". Expecting '==' or '!=', got " + token.character + ".")
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting '(', got " + token.character + ".")

    return False

# Id Parse: char
# Did not return parseChar(token, p) because I only want to return True or False, not a possible error message
def parseId(token, p):
    if(parseChar(token, p)):
        return True
    
    return False

# CharList Parse: char CharList OR space CharList OR Epsilon/Lambda
# I will not need to verify 'space CharList' b/c spaces inside strings are recognized as char's in my lexer
def parseCharList(token, p):
    if(match(token.kind, 'char', p)):
        if(parse(charList(token, p))):
                 return True
    else:
        # Epsilon/Lambda
        return True

# IntOp Parse: +
# This is here in case the language needs more operators
def parseIntOp(token, p):
    if(match(token.kind, 'operator', p)):
        return True
    else: # Will need to add operators to error message if more operators are added
        print("Error on line " + str(token.lineNum) + ". Expecting '+', got " + token.character + ".")

    return False

main()
