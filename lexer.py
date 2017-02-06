#Compiler using if statements as opposed to DFA
import re

def main():
    #file = input('Which file would you like to compile?');
    file = 'codeHere.txt'
    brokenText = createList(file)
    #print(str(brokenText))
    writeTokens(brokenText)
    
# Creates a list of every character in a file
def createList(file):
    inFile = open(file, 'r')
    #chars = [re.findall(r'[a-z][a-z]+|[a-z]|[0-9]|[=][=]|[(){}=]|[!][=]|["][a-z]+["]|[\n]|[\t]|[+]|[$]',line) 
    #        for line in open(file)]
    pattern = re.compile(r'[a-z][a-z]+|[a-z]|[0-9]|[=][=]|[(){}=]|[!][=]|["][a-z]+["]|[\n]|[\t]|[+]|[$]')
    chars = []
    for line in inFile:
        chars.append(pattern.findall(line))
        
    return chars



# '/n' is new line
# '/t' is tab
# Goes through a list for specific grammer
# Line numbers start at 0 because we are programmers
def writeTokens(charList):
    resultFile = open('tokens.txt', 'w')
    tokens = []
    lineNum = 1
    seperators = [' ', '\n', '\t', '=', '==']
    specialStatements = ['if', 'while', 'print', 'int', 'string', 'boolean', 'false', 'true']
    line = 0
    word = 0
    while line < len(charList)-1:
        print(charList[line])
        line = line + 1
        #while word < len(charList[0:]) - 1 :
            #word = word + 1
            #print(charList[line][word])

    #for a in range(0,len(tokens),1):
        #print(tokens[a].kind + ' ' + tokens[a].character + ' ' + str(tokens[a].lineNum) + '')
        #resultFile.write(tokens[a].kind + ' ' + tokens[a].character + ' ' + str(tokens[a].lineNum) + '\n')
    
    resultFile.close()

# Tokens are the objects the lexor produces for the parser to read
class token:
    def __init__(self, kind, character, lineNum):
        self.kind = kind
        self.character = character
        self.lineNum = lineNum
        #self.position = position

main()
