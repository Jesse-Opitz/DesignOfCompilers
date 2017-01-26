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
    #print(fileList[0:])
    for c in fileList:

        # Increments line number everytime a \n or new line character is entered
        if c is "\n":
            lineNum = lineNum + 1
        
        if re.match(r'[0-9]', c, 0):
            num = token('integer', lineNum)
            print('int', c, lineNum)
            tokens.append(num)
        elif re.match(r'[a-zA-Z]', c, 0):
            alpha = token('alphabetic', lineNum)
            print('alpha', c, lineNum)
            tokens.append(alpha)
    #for a in range(0,len(tokens),1):
    #    print(tokens[0].kind)
    
        
        
    #print(tokens)
    #resultFile.write(tokens)
    resultFile.close()

class token:
    def __init__(self, kind, lineNum):
        self.kind = kind
        self.lineNum = lineNum
        #self.position = position

main()
