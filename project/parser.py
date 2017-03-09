# This will be the Parser for Design of Compilers
import os
from lexer import token
from lexer import tokens
# P for pointer, global variable
p = 0

def main():
    global p
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
    global p
    if token is expected:
        print('matched', token, 'p is ', p)
        if p < len(tokens):
            p = p + 1
        return True

    return False
# Begin parse: Block $
def parseStart(token):
    # Parse for Block
    if(parseBlock(token)):
        if (match(token[p].kind, 'endProgram')):
            print("Parse Complete!")
        else:
           print("Error on line " + str(token.lineNum) + ". Expecting '$', got " + token.character + ".")

# Block Parse: { StatementList }
def parseBlock(token):
    print('parse block')
    if(match(token[p].character, '{')):
        if(parseStatementList(token)):
            if(match(token[p].character, '}')):
                return True
            else:
                   print("Error on line " + str(token[p].lineNum) + ". Expecting '}', got " + token[p].character + ".")
    #else:
       #print("Error on line " + str(token[p].lineNum) + ". Expecting '{', got '" + token[p].character + "'.")

    return False

# StatementList Parse: Statement StatementList OR Epsilon/Lambda
def parseStatementList(token):
    print('parse SL')
    if(parseStatement(token)):
        parseStatementList(token)
    else:
        # Epsilon/Lambda, could be nothing
        return True

# Statement Parse: PrintStatement OR AssignemntStatement OR VarDecl OR WhileStatement OR IfStatement OR Block
def parseStatement(token):
    print('parse S')
    if(parsePrintStatement(token)):
        return True
    elif(parseAssignmentStatement(token)):
        return True
    elif(parseVarDecl(token)):
        return True
    elif(parseWhileStatement(token)):
        return True
    elif(parseIfStatement(token)):
        return True
    elif(parseBlock(token)):
        return True

    return False

# PrintStatement Parse: print ( Expr )
def parsePrintStatement(token):
    print('parse PS')
    if(match(token[p].character, 'print')):
        if(match(token[p].character, '(')):
            if(parseExpr(token)):
                    if(match(token[p].character, ')')):
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
    print('parse AS')
    if(parseId(token)):
        if(match(token[p].character, '=')):
            if(parseExpr(token)):
                return True
        else:
            print("Error on line " + str(token[p].lineNum) + ". Expecting '=', got " + token[p].character + ".")

    return False

#VarDecl Parse: type Id
def parseVarDecl(token):
    print('parse VD')
    if(match(token[p].kind, 'type')):
        if(parseId(token)):
            return True
    #else:
        #print("Error on line " + str(token[p].lineNum) + ". Expecting 'int', 'string' or 'boolean', got " + token[p].character + ".")

    return False

# WhileStatement Parse: while BooleanExpr Block
def parseWhileStatement(token):
    print('parse WS')
    if(match(token[p].character, 'while')):
        if(parseBooleanExpr(token)):
            if(parseBlock(token)):
                return True
    #else:
        #print("Error on line " + str(token[p].lineNum) + ". Expecting 'while', got " + token[p].character + ".")

    return False

# IfStatement Parse: if BooleanExpr Block
def parseIfStatement(token):
    print('parse IS')
    if(match(token[p].character, 'if')):
        if(parseBooleanExpr(token)):
            if(parseBlock(token)):
                return True
    #else:
        #print("Error on line " + str(token[p].lineNum) + ". Expecting 'if', got " + token[p].character + ".")

    return False

# Expr Parse: IntExpr OR StringExpr OR BooleanExpr OR Id
def parseExpr(token):
    print('parse E')
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
    print('parse IE')
    # Triggers
    digitBool = False
    
    if(match(token[p].kind, 'digit')):
        digitBool = True
    #else:
        #print("Error on line " + str(token[p].lineNum) + ". Expecting a digit 0-9, got " + token[p].character + ".")

    # Checks for intop Expr, if they are there, return True
    if(parseIntOp(token)):
        if(parseExpr(token)):
            return True

    # Since intop Expr is not there, we only need to check the digit
    if(digitBool):
        return True

    return False

# StringExpr Parse: " CharList "
def parseStringExpr(token):
    print('parse SE')
    if(match(token[p].character, '"')):
        if(parseCharList(token)):
            if(match(token[p].character, '"')):
                return True
            else:
                print("Error on line " + str(token[p].lineNum) + '. Expecting \'"\', got ' + token[p].character + ".")
    #else:
        #print("Error on line " + str(token[p].lineNum) + '. Expecting \'"\', got ' + token[p].character + ".")

    return False

# BooleanExpr Parse: ( Expr boolop Expr )
def parseBooleanExpr(token):
    print('parse BE')
    if(match(token[p].character, '(')):
        if(parseExpr(token)):
            if(match(token[p].kind, 'compare')):
                if(parseExpr(token)):
                    if(match(token[p].character, ')')):
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
    print('parse ID')
    if(parseChar(token)):
        return True
    
    return False

# CharList Parse: char CharList OR space CharList OR Epsilon/Lambda
# I will not need to verify 'space CharList' b/c spaces inside strings are recognized as char's in my lexer
def parseCharList(token):
    print('parse CL')
    if(match(token[p].kind, 'char')):
        if(parse(charList(token))):
                 return True
    else:
        # Epsilon/Lambda
        return True
# Char Parse: a-z
def parseChar(token):
    print('parse C')
    if(match(token[p].kind, 'char')):
        return True

    return False

# IntOp Parse: +
# This is here in case the language needs more operators
def parseIntOp(token):
    print('parse IO')
    if(match(token[p].kind, 'operator')):
        return True
    else: # Will need to add operators to error message if more operators are added
        print("Error on line " + str(token[p].lineNum) + ". Expecting '+', got " + token[p].character + ".")

    return False

main()
