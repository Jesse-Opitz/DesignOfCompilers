#Compiler using if statements as opposed to DFA
import re

tokens = []

def runLexer(codeFile='codeHere.txt'):
    
    #file = input('Which file would you like to compile?');
    #file = 'codeHere.txt'
    #Fix checkChars
    errors = []
    e = 0
    if checkChars(open(codeFile, 'r'), errors):
        wordList = createList(codeFile)
        #print(str(brokenText))
        writeTokens(wordList, errors)
    #print('Errors: ' + str(errors))
    errorFile = open('errors.txt', 'w')
    while e < len(errors):
        print(errors[e])
        errorFile.write(str(errors[e]) + '\n')
        e = e + 1
    errorFile.close()

    return tokens
    #input('Press enter to end lexer and continue to the parser.')

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
    lineNum = 1
    quoteCount = 0
    
    # Patterns
    keywords = ['if', 'while', 'print']
    types = ['int', 'string', 'boolean']
    boolval = ['false', 'true']
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
        #print(line, wordList[line])
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
                elif uncheckedWord in types:
                    newTok = token('type', uncheckedWord, line)
                    tokens.append(newTok)
                elif uncheckedWord in boolval:
                    newTok = token('boolval', uncheckedWord, line)
                    tokens.append(newTok)
                else:
                    #print('Error: unexpected syntax "', uncheckedWord, '" on line', line)
                    errorLine = 'Error: Unexpected syntax ' + str(uncheckedWord) + ' at line ' + str(line)
                    errors.append(errorLine)
            elif re.match(charPattern, uncheckedWord, 0)  and quoteCount % 2 == 0:
                newTok = token('char', uncheckedWord, line + 1)
                tokens.append(newTok)
            elif re.match(numPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('digit', uncheckedWord, line + 1)
                tokens.append(newTok)
            elif re.match(comparePattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('compare', uncheckedWord, line + 1)
                tokens.append(newTok)
            elif re.match(assignPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('assign', uncheckedWord, line + 1)
                tokens.append(newTok)
            elif re.match(bracketPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('bracket', uncheckedWord, line + 1)
                tokens.append(newTok)
            elif re.match(parenPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('paren', uncheckedWord, line + 1)
                tokens.append(newTok)
            elif re.match(operatorPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('operator', uncheckedWord, line + 1)
                tokens.append(newTok)
            elif re.match(quotePattern, uncheckedWord, 0):
                quoteCount = quoteCount + 1
                newTok = token('quote', uncheckedWord, line + 1)
                tokens.append(newTok)
            elif re.match(eopPattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                newTok = token('endProgram', uncheckedWord, (line + 1))
                tokens.append(newTok)
            elif re.match(nonTokenBlankSpacePattern, uncheckedWord, 0) and quoteCount % 2 == 0:
                continue
            elif quoteCount % 2 == 1:
                #print(uncheckedWord)
                #print('first c is ' + c)
                #print(uncheckedWord)
                if uncheckedWord is '"':
                    beforeQuote = False
                    #print('qc is ' + c)
                elif uncheckedWord is not '"':
                    #print('c is ' + c)
                    if re.match(r'[a-z]+', uncheckedWord, 0):
                        #print('Here1 ' + str(line))     # This line shows correct line num
                        newTok = token('char', uncheckedWord, str(line + 1)) # This line shows as 1
                        #print('Here2 ' + str(line))    # This line shows correct line num
                        tokens.append(newTok)
                    elif re.match(r'[ ]', uncheckedWord, 0):
                        #print('space')
                        newTok = token('char', '\s', line + 1)
                        tokens.append(newTok)
                    elif re.match(r'[\n]', uncheckedWord, 0):
                        errorLine = 'Error: Unexpected \\n in a string, at line ' + str(line + 1)
                        errors.append(errorLine)
                    elif re.match(r'[\t]', uncheckedWord, 0):
                        errorLine = 'Error: Unexpected tab in a string, at line ' + str(line + 1)
                        errors.append(errorLine)
                    else:
                        #print('Else Here' + str(line))
                        errorLine = 'Error: Unexpected syntax in a string, ' + str(uncheckedWord) + ' at line ' + str(line + 1)
                        errors.append(errorLine)
                        #print(errorLine)
            else:
                if quoteCount % 2 == 0:
                    print('Error: unexpected syntax', uncheckedWord, 'on line ', str(line + 1))
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

runLexer()
