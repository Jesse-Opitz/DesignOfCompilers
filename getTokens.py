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
        for c in line:
            chars.append(c)
    return chars

# '/n' is new line
# '/t' is tab
def writeTokens(fileList):
    resultFile = open('tokens.txt', 'w')
    tokens = []
    lineNum = 1
    for c in fileList:
        #print(lineNum, c)
        if re.match(r'[0-9]', c, 0):
            num = token('integer', c, lineNum)
            #print('int', c)
            tokens.append(num)
        elif re.match(r'[a-zA-Z]', c, 0):
            alpha = token('alphabetic', c, lineNum)
            #print('alpha', c)
            tokens.append(alpha)
        elif c is '\n':
            lineNum = lineNum + 1
    for a in range(0,len(tokens),1):
        print(resultFile.write(tokens[a].kind + ' ' + tokens[a].character + ' ' + str(tokens[a].lineNum) + '\n'))
    
    resultFile.close()

class token:
    def __init__(self, kind, character, lineNum):
        self.kind = kind
        self.character = character
        self.lineNum = lineNum
        #self.position = position

main()