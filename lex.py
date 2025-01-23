import enum
import sys

#Note to self: init stands for initialization & is a constructor (therefore is used in OOP to create & initialze an object, ie. instance of a class)
#Note to self: "self" is always a parameter of the __init__ function which is a reference to the new object being created
#Note to self: you must store objects in fields (ie. setter methods)
#Note to self: pass is used in python when you want a function to execue without an error (if it's empty)
#Note to self: enum in Python stands for "enumeration" which is a set of symolic names bound to unique values. Used when you wish to define constants with meaningful names.
#You can access enums [TokenType.EOF] by either name [TokenType.EOF.name] or value [TokenType.EOF.value]
#Note to self: if you import sys, you're importing the sys module which provides access to system specific parameters and functions that interact with python's runtime environment

class Lexer:
    
    """This class is where all the methods of the Lexer will be implemented."""
    
    #Lexer keeps track of the current position in the input string & the character at that position. These are initialized in the following constructor:
    def __init__ (self, source): 
        self.source = source + '\n' #this adds the source code to the lexer as a string, and a newline character is appended in order to simpify lexing/parsing the last token/statement
        self.curChar = "" #current character in the string 
        self.curPos = -1 #current position in the string 
        self.nextChar() #VERY IMPORTANT note to self: the _init_ method is called automatically when the class of the object is created, therefore it will also call on the nextChar() method
        
    #Processing the next character
    def nextChar (self):
        self.curPos += 1 #increments the lexer's current position
        if self.curPos >= len (self.source):
            self.curChar = '\0' #EOF (reach end of the file)
        else:
            self.curChar = self.source [self.curPos]
    
    #Return the lookahead character 
    def peek (self):
        if self.curPos + 1 >= len (self.source): 
            return '\0'
        return self.source [self.curPos + 1]
            
    #If an invalid token is found, then print an error message and exit 
    def abort (self, message):
        sys.exit ("Lexing error. "+message) #Note to self: As a part of the sys module, you can terminate a program using sys.exit([status])
    
    #Skip whitespaces except newlines, which will be used to indicate the end of a sentence 
    def skipWhitespace (self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()
    
    #Skip comments in the code 
    #Whenever a lexer sees a comment, it should ignore all the text after it until a newline (will be discarded)
    #it's important that the newline at the end of the comment isn't thrown away since it its own token and may still be needed 
    def skipComment (self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()
    
    # Return the next token
    def getToken(self):
        
        #skip everytime you encounter a whitespace
        self.skipWhitespace()
        
        #skip everytime you encounter a comment 
        self.skipComment()
        
        token = None #Note to self: none is used to define a null value in Python
        
        #checking the first character of the token to see if we can decide what it is 
        #if it is a multiple character operator (eg. !=), number, identifier or keyword then we will process the rest
        if self.curChar == '+': #plus token
            token = Token (self.curChar, TokenType.PLUS)
        elif self.curChar == '-': #minus token
            token = Token (self.curChar, TokenType.MINUS)
        elif self.curChar == '*': #asterisk token
            token = Token (self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/': #slash token
            token = Token (self.curChar, TokenType.SLASH)
        
        #lexing operators made up of 2 characters (== & >= & <= & !=)
        elif self.curChar == '=':
            #check whether the token is = or == 
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token (lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token (self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            #check whether this token is > or >= 
            if self.peek() == '=':
                lastChar = self.curChar 
                self.nextChar()
                token = Token (lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token (self.curChar, TokenType.GT)
        elif self.curChar == '<':
            #check whether this token is < or <= 
            if self.peek() == '=':
                lastChar = self.curChar 
                self.nextChar()
                token = Token (lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token (self.curChar, TokenType.LT)
        elif self.curChar == '!':
            #check whether this oken is ! or !=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token (lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        
        #supports printing a string - which starts with a double quotation mark up until the 2nd double quotation mark
        elif self.curChar == '\"':
            
            #get all the characters between the quotation marks
            self.nextChar()
            startPos = self.curPos
            
            while self.curChar != '\"':
                #No special characters are allowed in the string, including no escape characters, newlines, tabs or %
                #we're using C's printf on this sting
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort ("Illegal character in the string")
                self.nextChar()
            tokText = self.source [startPos:self.curPos] #this slices the source string from the beginning of the " to the end of " (start and end of string)"
            token = Token (tokText, TokenType.STRING)
        
        #In the Teeny Tiny Language, it supports a number as one or more digits (from 0-9) that is followed by an optional decimal point that must be followed by atleast 1 digit
        #peek function will help look ahead one character 
        
        elif self.curChar.isdigit(): #Note to self: isdigit() is a string method used to check whether all characters in a string are digits (0-9). Returns True if they're numeric digits, and False otherwise
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':
                self.nextChar() 
    
                #ensure that you have atleast one digit after the decimal to be valid
                if not self.peek().isdigit():
                    #you get an error if it's not a digit 
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()
            tokText = self.source [startPos:self.curPos + 1] #Note to self: remember string slicing goes up to the value before itself
            token = Token (tokText, TokenType.NUMBER)   
        
        #Handling keywords & identifiers. An identifier is anything that begins with an alphabetical character followed by zero or more alphanumeric characters
        elif self.curChar.isalpha(): #Note to self: isalpha() is a method used in Python that checks whether the characters in a string are alphabetic (ie. letters a to z). Returns True if so, otherwise False
            startPos = self.curPos
            while self.peek().isalnum(): #Note to self: isalnum() is a method used in Python that checks whether the characters in a string are alphanumeric
                self.nextChar()    
            
            #check to see whether the token is in the list of keywords
            tokText = self.source [startPos : self.curPos + 1] #getting the substring of text
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None: #This means it's an identifier
                token = Token (tokText, TokenType.IDENT)  
            else:
                token = Token (tokText, keyword)
                                                            
        elif self.curChar == '\n': #newline token
            token = Token (self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token ("", TokenType.EOF)
        else:
            #unknown token!
            self.abort ("Unknown token: " + self.curChar)
        self.nextChar()
        return token

class Token:
    """This is a token class that keeps track of what type of token it is & the exact text from the code"""
    
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText #the token's actual text. Used for identifiers, strings & numbers 
        self.kind = tokenKind #the "type" of token that this will be identified as
        
    @staticmethod #method that belongs to a class rather than an instance of a class (doesn't take self as a parameter) 
    #it's used when the method logic is related to the class but does not need access to the instance or class attributes
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            #relies on all enumvalues being 1xx
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None

#TokenType is our enum for all types of tokens
#Note to self: we've imported the entire enum module, hence need to use "enum.Enum" in order to access the Enum class
class TokenType(enum.Enum):
        EOF = -1
        NEWLINE = 0
        NUMBER = 1
        IDENT = 2
        STRING = 3 
        #Keywords
        LABEL = 101
        GOTO = 102
        PRINT = 103
        INPUT = 104
        LET = 105
        IF = 106
        THEN = 107
        ENDIF = 108
        WHILE = 109
        REPEAT = 110
        ENDWHILE = 111
        #Operators 
        EQ = 201
        PLUS = 202
        MINUS = 203
        ASTERISK = 204
        SLASH = 205
        EQEQ = 206
        NOTEQ = 207
        LT = 208
        LTEQ = 209
        GT = 210
        GTEQ = 211
        
        
        
        
    
    

    