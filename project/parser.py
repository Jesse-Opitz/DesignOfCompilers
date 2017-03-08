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
    if(runParse):
        # P for pointer
        p = 0
        while p < len(tokens):
            parseStart(tokens[p].kind)
            p = p + 1
    # Do not parse, error in lexer
    else:
        print("Error in lexer, can not run parse.")

def match(tokenChar, expectedChar):
    if tokenChar is expectedChar:
        return True
    
    return False

def parseStart(token):
    parseBlock(token)
    match("$", "$")

#def parseBlock(tokenVal):
    


main()
