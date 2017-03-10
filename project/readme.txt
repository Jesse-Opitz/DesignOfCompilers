This program uses Python 3.0 or above. **Version 2.7 will return errors for some features.

lexer.py is the python 3.X file containing the code for Project One, creating the lexer of the compiler.  The compiler will run all the way through and list any errors that occured at the end of execution.  Inta is an issue because it is not the correct grammar and my compiler will be similar to Jave because I have not used much of any other object-oriented languages.

In order to run the python file use one of these options:

One, any OS with python installed
1. Double click the python file to run in command prompt
*It will stay open until you press enter after the lexer is done

Two, any OS
1. Right click the file lexer.py
2. Click Edit with IDLE
3. Press f5 to run in IDLE

Three, Mac or Linux
1. Open terminal
2. Switch to the directory where lexer.py is located
3. Type python lexer.py

After running the program you will be able to type in the name of a text file with code that you wish to execute the lexer upon. NOTE: The code file MUST be inside the same directory as the python file, otherwise you must enter a full path to that file.

When the lexer is complete, the tokens will be printed to screen and saved in the tokens.txt file.

There is a sample file codeHere.txt that I used while testing the compiler.

Parser Instructions:

The parser uses a special library called treelib that must be installed via pip.  Pip is downloaded by default with python.  The website for the programs documentation is 
https://github.com/caesar0301/treelib/blob/master/README.md.

To install treelib type into a terminal: 

sudo pip install treelib

IF pip does not run, you must go to the python folder where pip is located, open a terminal window there and then try the command.

Due to parser limitations and time restraints, the parser can only parse 1 program at a time, no matter how many programs are in the text file.

***Not yet implemented:

python parser.py testCode.txt
 - The code will prompt for which text file you wish to run and as long as that text file is in the same file as the lexer, it should run.  However it does not take in standard input
   from the command line yet.  It will be fixed in future versions, I just do not have the time to do it for this project.