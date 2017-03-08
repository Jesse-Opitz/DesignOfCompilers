# This will be the Parser for Design of Compilers
import os
from lexer import token
from lexer import tokens

print(tokens[1].kind)

def main():
    runParse = False
    
    if(os.stat("errors.txt").st_size == 0):
        runParse = True

    if(runParse):
        a = 0
        while a < len(tokens):
            print(tokens[a].kind)
            a = a + 1
        
    else:
        print("Error in lexer, can not run parse.")

def match(tokenChar, expectedChar):
    if tokenChar is expectedChar:
        return True
    
    return False

def parseStart(tokenVal):
    parseBlock(tokenVal)
    match("$", "$")

#def parseBlock(tokenVal):
    


main()
