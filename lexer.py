#Compiler using if statements as opposed to DFA
import re

def main():
    
    #file = input('Which file would you like to compile?');
    file = 'codeHere.txt'
    #Fix checkChars
    if checkChars(open(file, 'r')):
        wordList = createList(file)
        #print(str(brokenText))
        writeTokens(wordList)


    
# Creates a list of every character in a file
def createList(file):
    inFile = open(file, 'r')
    #chars = [re.findall(r'[a-z][a-z]+|[a-z]|[0-9]|[=][=]|[(){}=]|[!][=]|["][a-z]+["]|[\n]|[\t]|[+]|[$]',line) 
    #        for line in open(file)]
    pattern = re.compile(r'[a-z][a-z]+|[a-z]|[0-9]|[=][=]|[(){}=]|[!][=]|["][a-z]+["]|[\n]|[\t]|[+]|[$]')
    chars = []
    for line in inFile:
        chars.append(pattern.findall(line))
    inFile.close()
    return chars

def checkChars(file):
    validChar = 'abcdefghijklmnopqrstuvwxyz0123456789$""(){}!= \n\t+'
    lineNum = 1
    position = 1
    for line in file:
        for c in line:
            if c is '\n':
                lineNum = lineNum + 1
            if c not in validChar:
                print('Error: Unexpected character', c, 'at line', str(lineNum), 'position', str(position))
                #return False
            position = position + 1
    return True


# '/n' is new line
# '/t' is tab
# Goes through a list for specific grammer
# Line numbers start at 0 because we are programmers
def writeTokens(wordList):
    resultFile = open('tokens.txt', 'w')
    tokens = []
    lineNum = 1
    
    # Patterns
    keywords = ['if', 'while', 'print', 'int', 'string', 'boolean', 'false', 'true']
    charPattern = r'[a-z]'
    numPattern = r'[0-9]'
    keyWordPattern = r'[a-z][a-z]+'
    assignPattern = r'[=]'
    comparePattern = r'[!][=]|[=][=]'
    bracketPattern = r'[{]|[}]'
    parenPattern = r'[(]|[)]'
    operatorPattern = r'[+]'
    eopPattern = r'[$]'
    blankSpacePattern = r'[ ]|[\n]|[\t]'
    
    line = 0
    word = 0
    while line < len(wordList):
        #print(wordList[line], line)
        #print(len(wordList[line]))
        for word in range(0, len(wordList[line]), 1):                
            uncheckedWord = wordList[line][word]
            #print(uncheckedWord)
            if uncheckedWord in keywords:
                newTok = token('keyword', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(charPattern, uncheckedWord, 0):
                newTok = token('char', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(numPattern, uncheckedWord, 0):
                newTok = token('digit', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(comparePattern, uncheckedWord, 0):
                newTok = token('compare', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(assignPattern, uncheckedWord, 0):
                newTok = token('assign', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(bracketPattern, uncheckedWord, 0):
                newTok = token('bracket', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(parenPattern, uncheckedWord, 0):
                newTok = token('paren', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(operatorPattern, uncheckedWord, 0):
                newTok = token('operator', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(eopPattern, uncheckedWord, 0):
                newTok = token('endProgram', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(blankSpacePattern, uncheckedWord, 0):
                newTok = token('blankSpaces', '\space', line)
                tokens.append(newTok)
            else:
                print('Error: unexpected syntax', uncheckedWord, 'on line', line)
        line = line + 1
            
        

    for a in range(0,len(tokens),1):
        print('Lexer -->', 'Line:', str(tokens[a].lineNum), tokens[a].kind + ' ' + tokens[a].character + ' ')
        resultFile.write(str(tokens[a].lineNum) + ' ' + tokens[a].kind + ' ' + tokens[a].character + '\n')

    print('Lexer --> Complete')
    resultFile.close()

# Tokens are the objects the lexor produces for the parser to read
class token:
    def __init__(self, kind, character, lineNum):
        self.kind = kind
        self.character = character
        self.lineNum = lineNum
        #self.position = position

main()
