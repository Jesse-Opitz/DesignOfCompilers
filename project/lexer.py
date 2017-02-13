#Compiler using if statements as opposed to DFA
import re

def main():
    
    file = input('Which file would you like to compile?');
    #file = 'codeHere.txt'
    #Fix checkChars
    errors = []
    e = 0
    if checkChars(open(file, 'r'), errors):
        wordList = createList(file)
        #print(str(brokenText))
        writeTokens(wordList, errors)
    #print('Errors: ' + str(errors))
    while e < len(errors):
        print(errors[e])
        e = e + 1

    input('Press enter to end')


    
# Creates a list of every character in a file
def createList(file):
    inFile = open(file, 'r')
    #chars = [re.findall(r'[a-z][a-z]+|[a-z]|[0-9]|[=][=]|[(){}=]|[!][=]|["][a-z]+["]|[\n]|[\t]|[+]|[$]',line) 
    #        for line in open(file)]
    pattern = re.compile(r'[a-z][a-z]+|[a-z]|[0-9]|[=][=]|[(){}=]|[!][=]|["]|[ ]|[\n]|[\t]|[+]|[$]')
    chars = []
    for line in inFile:
        chars.append(pattern.findall(line))

    #print(chars)
    inFile.close()
    return chars

def checkChars(file, errors):
    validChar = 'abcdefghijklmnopqrstuvwxyz0123456789$""(){}!= \n\t+'
    lineNum = 1
    #Would add position, but I am not sure how to implement it in writeTokens
    #position = 1
    for line in file:
        for c in line:
            if c is '\n':
                lineNum = lineNum + 1
            if c not in validChar:
                errorLine = 'Error: Unexpected character ' + str(c) + ' at line' + str(lineNum)
                errors.append(errorLine)
                #print('Error: Unexpected character', c, 'at line', str(lineNum)
                #return False
            #position = position + 1
    return True


# '/n' is new line
# '/t' is tab
# Goes through a list for specific grammer
# Line numbers start at 0 because we are programmers
def writeTokens(wordList, errors):
    resultFile = open('tokens.txt', 'w')
    tokens = []
    lineNum = 1
    quoteCount = 0
    
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
    quotePattern = r'["]'
    nonTokenBlankSpacePattern = r'[\n]|[\t]|[ ]'
    invalStrBlanks = r'[\n]|[\t]'
    
    line = 0
    word = 0
    while line < len(wordList):
        print(line, wordList[line])
        #print(wordList[line], line)
        #print(len(wordList[line]))
        beforeQuote = True
        for word in range(0, len(wordList[line]), 1):
            uncheckedWord = wordList[line][word]
            #print(uncheckedWord)
            if re.match(keyWordPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                if uncheckedWord in keywords:
                    newTok = token('keyword', uncheckedWord, line)
                    tokens.append(newTok)
                else:
                    print('Error: unexpected syntax "', uncheckedWord, '" on line', line)
                    errorLine = 'Error: Unexpected syntax ' + str(uncheckedWord) + ' at line' + str(lineNum)
                    errors.append(errorLine)
            elif re.match(charPattern, uncheckedWord, 0)  and quoteCount % 2 == 0:
                newTok = token('char', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(numPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('digit', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(comparePattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('compare', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(assignPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('assign', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(bracketPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('bracket', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(parenPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('paren', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(operatorPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('operator', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(quotePattern, uncheckedWord, 0):
                quoteCount = quoteCount + 1
                newTok = token('quote', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(eopPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('endProgram', uncheckedWord, line)
                tokens.append(newTok)
            elif re.match(nonTokenBlankSpacePattern, uncheckedWord, 0):
                continue
            elif quoteCount % 2 == 1:
                #print(uncheckedWord)
                for c in uncheckedWord:
                    if c is '"':
                        beforeQuote = False
                    elif c is not '"':
                        if re.match(r'[a-z]', c, 0):
                            print('Here1 ' + str(line))
                            newTok = token('char', c, line)
                            print('Here2 ' + str(line))
                            tokens.append(newTok)
                        elif c is ' ':
                            newTok = token('char', '\s', line)
                            tokens.append(newTok)
                        else:
                            errorLine = 'Error: Unexpected syntax ' + str(uncheckedWord) + ' at line ' + str(lineNum)
                            errors.append(errorLine)
                    print(errorLine)
                else:
                    if quoteCount % 2 == 0:
                        print('Error: unexpected syntax', uncheckedWord, 'on line ', line)
        line = line + 1
            
        

    for a in range(0,len(tokens),1):
        print('Lexer -->', 'Line: ' + str(tokens[a].lineNum) + ' ' + tokens[a].kind + ' ' + str(tokens[a].character))
        resultFile.write(str(tokens[a].lineNum) + ' ' + tokens[a].kind + ' ' + str(tokens[a].character) + '\n')

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
