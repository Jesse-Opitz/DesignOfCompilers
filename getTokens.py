import re

def main():
    #file = input('Which file would you like to compile?');
    file = 'codeHere.txt'
    inFile = open(file, 'rU')
    tokens = []
    lineNum = 0
    for line in inFile:
        #print(line)
        tokens.append(writeTokens(line, lineNum))
        

    resultFile = open('tokens.txt', 'w')
    for a in range(0,len(tokens),1):
        print(tokens[a].kind + ' ' + str(tokens[a].character) + ' ' + str(tokens[a].lineNum))
        
    #resultFile.write(tokens[a].kind + ' ' + tokens[a].character + ' ' + str(tokens[a].lineNum) + '\n')
    resultFile.close()

#def createList(fileName):
#    inFile = open(fileName, 'rU')
#    chars = []
#    for line in inFile:
#        for c in line:
#            chars.append(c)
#    return chars

# '/n' is new line
# '/t' is tab
def writeTokens(line, lineNum):
    if re.match(r'[0-9]', line, 0):
        num = token(1, 'integer', lineNum)
        #print('int', c, lineNum)
        return num
    elif re.match(r'[a-zA-Z]', line, 0):
        alpha = token(2, 'alphabetical', lineNum)
        #print('alpha', c, lineNum)
        #tokens.append(alpha)
        return alpha
        
    #print(tokens)
    #resultFile.write(tokens)
    

class token:
    def __init__(self, character, kind, lineNum):
        self.character = character
        self.kind = kind
        self.lineNum = lineNum
        #self.position = position

main()
