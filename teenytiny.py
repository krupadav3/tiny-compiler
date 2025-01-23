#Note to self: In order to work with files in Python, you must open them first & "with" allows you to read a file without explicitly closing it 
#"with" has 2 built-in methods already (__enter()__ & __exit()__)
#to use the open function, you must delcare a variable for it first, and the open() function can take up to 3 parameters: filename, mode, encoding



from lex import * #the * instructs Python to implement all public names (functions, classes, variables, etc.) from the lex module into the curernt namespace
from emit import *
from parse import * 
import sys


def main ():
    print ("Teeny Tiny Compiler")
    
    if len(sys.argv) != 2: #Note to self: sys.argv is a list of command-line arguments as strings. You run the program via the command line
        sys.exit ("Error: Compiler needs some source as argument")
    with open (sys.argv[1], 'r') as inputFile:
        source = inputFile.read()
    
    #Initialize the lexer, emitter and parser 
    lexer = Lexer(source)
    emitter = Emitter ("out.c")
    parser = Parser (lexer, emitter)
    
    
    parser.program() #Start the parser
    emitter.writeFile() #Write the output to file
    
    print ("Compiling completed.")

main()

