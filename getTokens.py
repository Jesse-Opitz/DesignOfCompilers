import re

def main():
    #file = input('Which file would you like to compile?');
    file = 'codeHere.txt'
    brokenText = createList(file)
    writeTokens(brokenText)
    

def createList(fileName):
    inFile = open(fileName, 'rU')
    chars = []
    for line in inFile:
        #chars.append(line)
        for c in line:
            chars.append(c)
    return chars

# '/n' is new line
# '/t' is tab
def writeTokens(fileList):
    resultFile = open('tokens.txt', 'w')
    tokens = []
    lineNum = 1
    tempChar = []
    for c in fileList:
        #print(lineNum, c)
        if not (re.match('[0-9a-zA-Z]', c, 0)):
            if len(tempChar) > 1:
                tempWord = ''.join(tempChar)
                keyWord = token('keyWord', tempWord, lineNum)
                tokens.append(keyWord)
                tempChar = []
        
        if re.match('[0-9]', c, 0):
            num = token('integer', c, lineNum)
            #print('int', c)
            tokens.append(num)
            if len(tempChar) > 0:
                tempChar.append(str(c))
        elif re.match('[a-zA-Z]', c, 0):
            alpha = token('alphabetic', c, lineNum)
            #print('alpha', c)
            tokens.append(alpha)
            tempChar.append(c)
# key words aren't recognized b/c file is being read line by line
# can't read multiple letters at once
        #elif re.match(r'/([a-zA-Z])*/g', c, 0):
        #    keyWord = token('keyWord', c, lineNum)
        #    tokens.append(keyWord)
        elif c is '{':#re.match(r'/[{]/g', c, 0):  
            opBracket = token('opBracket', c, lineNum)
            tokens.append(opBracket)
        elif c is '}':#re.match(r'/[}]/g', c, 0):
            clBracket = token('clBracket', c, lineNum)
            tokens.append(clBracket)
        elif c is '(':
            opParen = token('opParen', c, lineNum)
            tokens.append(opParen)
        elif c is ')':
            clParen = token('clParen', c, lineNum)
            tokens.append(clParen)
        elif c is ' ':
            space = token('whiteSpace', 't_space', lineNum)
            tokens.append(space)
        elif c is '\n':
            lineNum = lineNum + 1
        elif c is '$':
            end = token('program', c, lineNum)
            tokens.append(end)

    for a in range(0,len(tokens),1):
        print(tokens[a].kind + ' ' + tokens[a].character + ' ' + str(tokens[a].lineNum) + '')
        resultFile.write(tokens[a].kind + ' ' + tokens[a].character + ' ' + str(tokens[a].lineNum) + '\n')
    
    resultFile.close()

class token:
    def __init__(self, kind, character, lineNum):
        self.kind = kind
        self.character = character
        self.lineNum = lineNum
        #self.position = position

main()
