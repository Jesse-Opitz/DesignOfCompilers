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
    # Triggers
    pBlock = False
    ep = False
    
    # Parse for Block
    if(parseBlock(token, p)):
       pBlock = True

    # Parse for end of program
    if (match(token.kind, 'endProgram', p)):
       ep = True
    else:
       print("Error on line " + str(token.lineNum) + ". Expecting '$', got " + token.character + ".")

    # Both block and end of program are correct, parse is successful
    if(pBlock and ep):
        print("Parse successful")
    else:
        print("Parse failed")

# Block Parse: { StatementList }
def parseBlock(token, p):
    # Triggers
    opBrack = False
    sL = False
    clBrack = False
    
    if(match(token.character, '{', p)):
        opBrack = True
    else:
       print("Error on line " + str(token.lineNum) + ". Expecting '{', got '" + token.character + "'.")

    if(parseStatementList(token, p)):
        sL = True

    if(match(token.character, '}', p)):
        clBrack = True
    else:
       print("Error on line " + str(token.lineNum) + ". Expecting '}', got " + token.character + ".")

    if(opBrack and sL and clBrack):
        return True

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
    #elif(parseVarDecl(token, p)):
    #    return True
    #elif(parseWhileStatement(token, p)):
    #    return True
    #elif(parseIfStatement(token, p)):
    #    return True
    #elif(parseBlock(token, p)):
    #    return True

    return False

# PrintStatement Parse: print ( Expr )
def parsePrintStatement(token, p):
    #Triggers
    prnt = False
    opParen = False
    expr = False
    clParen = False
 
    if(match(token.character, 'print', p)):
        p = True
    else:
       print("Error on line " + str(token.lineNum) + ". Expecting 'print', got " + token.character + ".")

    if(match(token.character, '(', p)):
        opParen = True
    else:
       print("Error on line " + str(token.lineNum) + ". Expecting '(', got " + token.character + ".")

    if(parseExpr(token, p)):
        expr = True

    if(match(token.character, ')', p)):
        clParen = True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting ')', got " + token.character + ".")

    if(prnt and opParen and expr and clParen):
        return True

    return False

# AssignmentStatement Parse: Id = Expr
def parseAssignmentStatement(token, p):
    # Triggers
    idBool = False
    assign = False
    expr = False

    if(parseId(token, p)):
        idBool = True

    if(match(token.kind, 'assign', p)):
        assign = True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting '=', got " + token.character + ".")

    if(parseExpr(token,p)):
        expr = True

    if(idBool and assign and expr):
        return True

    return False

#VarDecl Parse: type Id
def parseVarDecl(token, p):
    # Triggers
    typeBool = False
    idBool = False

    if(match(token.kind, 'type', p)):
        typeBool = True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting 'int', 'string' or 'boolean', got " + token.character + ".")

    if(parseId(token, p)):
        idBool = True

    if(typeBool and idBool):
        return True

    return False

# WhileStatement Parse: while BooleanExpr Block
def parseWhileStatement(token, p):
        # Triggers
    whileBool = False
    booleanExpr = False
    block = False

    if(match(token.character, 'while', p)):
        whileBool = True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting 'while', got " + token.character + ".")

    if(parseBooleanExpr(token, p)):
        booleanExpr = True

    if(parseBlock(token, p)):
        block = True

    if( whileBool and booleanExpr and block):
        return True

    return False

# IfStatement Parse: if BooleanExpr Block
def parseIfStatement(token, p):
    # Triggers
    ifBool = False
    booleanExpr = False
    block = False

    if(match(token.character, 'if')):
        ifBool = True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting 'if', got " + token.character + ".")

    if(parseBooleanExpr(token, p)):
        booleanExpr = True

    if(parseBlock(token, p)):
        block = True

    if(ifBool and booleanExpr and block):
        return True

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
        opQuote = True
    else:
        print("Error on line " + str(token.lineNum) + '. Expecting \'"\', got ' + token.character + ".")

    if(parseCharList(token, p)):
        charList = True

    if(match(token.character, '"', p)):
        clQuote = True
    else:
        print("Error on line " + str(token.lineNum) + '. Expecting \'"\', got ' + token.character + ".")

    if(opQuote and charList and clQuote):
        return True

    return False

# BooleanExpr Parse: ( Expr boolop Expr )
def parseBooleanExpr(token, p):
    # Triggers
    opParen = False
    expr1 = False
    boolop = False
    expr2 = False
    clParen = False
    
    if(match(token.character, '(', p)):
        opParen = True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting '(', got " + token.character + ".")

    if(parseExpr(token, p)):
        expr1 = True

    if(match(token.kind, 'compare', p)):
        boolop = True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting '==' or '!=', got " + token.character + ".")

    if(parseExpr(token, p)):
        expr2 = True

    if(match(token.character, ')', p)):
        clParen = True
    else:
        print("Error on line " + str(token.lineNum) + ". Expecting ')', got " + token.character + ".")

    if(opParen and expr1 and boolop and expr2 and clParen):
        return True

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
