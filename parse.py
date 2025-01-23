import sys 
from lex import*

#Parser object keeps track of current token & checks if the code matches the grammar 

class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter 
        
        #Note to self: the set() function in Python is used to create a set (an unordered collection of unique, hashable elements)
        self.symbols = set() #This is all the variables that have been declared so far
        self.labelsDeclared = set() #This is all the labels declared so far
        self.labelsGotoed = set() #This is all labels goto'ed so far
        
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken() #nextToken() is called twice so that it initializes current & peak
    
    #Returns true if the current token matches 
    def checkToken (self, kind):
        return kind == self.curToken.kind #Note to self: this operation is an equality comparision which evaluates to a boolean (True if 2 values are equal, False if not)
    
    #Returns true if the next token matches 
    def checkPeek (self, kind):
        return kind == self.peekToken.kind 
    
    #Trying to match current token. If not, error. Advances to the next token
    def match (self, kind):
        if not self.checkToken(kind):
            self.abort ("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()
    
    #Advances the curernt token
    def nextToken (self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken() #you don't need to parse through the EOF because the lexer handles that already
    
    def abort (self, message):
        sys.exit ("Error! " + message)
        
    #Parsing Statements (Going through the grammar & implementing a function for each rule) - this line checks whether the program is made up of 0 or more statements
    # program ::= {statement}
    def program (self):
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")
        
        #Some newlines are required in the grammar, hence we need to skip over the excess 
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
        
        #Parse through all the statements in the program
        while not self.checkToken(TokenType.EOF):
            self.statement()
        
        #at the end of the C code
        self.emitter.emitLine ("return 0;")
        self.emitter.emitLine ("}")
        
        #Check that each label referenced in a GOTO is declared
        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort ("Attempting to GOTO to undeclared variable: " + label)
    
    #Next rule in grammar is "statement" which allows for 7 different types of rules. 
    def statement(self):
        #Check the first token to see what kind of token it is
        
        #'PRINT' (expression | string)
        if self.checkToken(TokenType.PRINT):
            self.nextToken()
            
            if self.checkToken(TokenType.STRING):
                #simple string, so just print it
                self.emitter.emitLine ("printf (\"" + self.curToken.text + "\\n\");")
                self.nextToken()
                
            else:
                #expect an expression, therefore print the result as a float
                self.emitter.emit ("printf (\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine ("));")
        
        # "IF" comparision "THEN" {statement} 
        elif self.checkToken (TokenType.IF):
            self.nextToken()
            self.emitter.emit ("if(")
            self.comparision() #another grammar rule - comparision 
            
            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emitLine ("){")
            
            #Zero or more statements in the body 
            while not self.checkToken(TokenType.ENDIF):
                self.statement()
                
            self.match(TokenType.ENDIF)
            self.emitter.emitLine ("}")
        
        #"WHILE" comparision "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken (TokenType.WHILE):
            self.nextToken()
            self.emitter.emit("while(")
            self.comparision()
            
            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emitLine ("){")
            
            #Zero or more statements in the loop body
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
            
            self.match(TokenType.ENDWHILE)
            self.emitter.emitLine ("}")
        
        # "LABEL" ident 
        elif self.checkToken(TokenType.LABEL):
            self.nextToken()
            
            #Ensure that the label doesn't already exist
            if self.curToken.text in self.labelsDeclared:
                self.abort ("Label aready exists: " + self.curToken.text)
            self.labelsDeclared.add(self.curToken.text)

            self.emitter.emitLine (self.curToken.text + ":")
            self.match(TokenType.IDENT)
        
        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            self.nextToken()
            self.labelsGotoed.add(self.curToken.text) #Note to self: the .add() method is used in Python to add a single element to a set & if the element already exists, will ignore duplicates
            self.emitter.emitLine ("goto " + self.curToken.text + ";")
            self.match(TokenType.IDENT)
        
        # "LET" ident "=" expression 
        elif self.checkToken (TokenType.LET):
            self.nextToken()
            
            #Check if the symbols exist in the symbol table, and if not - then make sure to declare it
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine ("float " + self.curToken.text + ";")
            
            self.emitter.emit(self.curToken.text + " = ")
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            
            self.expression()
            self.emitter.emitLine(";")
        
        
        #Note: There's a limitation to the "Teeny Tiny" language. You can't tell if the user input was the value 0 or an invalid input
        # "INPUT" ident =
        elif self.checkToken (TokenType.INPUT):
            self.nextToken()
            
            #if the variable doesn't already exist, declare it 
            if self.curToken.text not in self.symbols:
                self.symbols.add (self.curToken.text) 
                self.emitter.headerLine ("float " + self.curToken.text + ";")
                
            #Emit scanf but also validate the input. If it's invalid, then set the variable to 0 and clear the input
            self.emitter.emitLine ("if(0 == scanf(\"%" + "f\", &" + self.curToken.text + ")) {")
            self.emitter.emitLine (self.curToken.text + " = 0;")
            self.emitter.emit ("scanf(\"%")
            self.emitter.emitLine ("*s\");")
            self.emitter.emitLine ("}")
            self.match(TokenType.IDENT)
                        
        #otherwise, it's not a valid statement so you want to print an error
        else:
            self.abort("Invalid statement at " + self.curToken.text + " ("+ self.curToken.kind.name + ")")
        #newline
        self.nl()
    
    #comparision ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparision (self):
        self.expression()
        
        #You must have atleast 1 comparision operator and another expression
        if self.isComparisionOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()
        
        #else:
        #    self.abort ("Expected comparision operator at: " + self.curToken.text)
            
        #You can have 0 or more comparision operator & expressions
        while self.isComparisionOperator():
            self.emitter.emit (self.curToken.text)
            self.nextToken()
            self.expression()
        
    #Checks whether its a comparision operator or not (returns True if it is & the type of comparision operator) 
    def isComparisionOperator(self):
        return self.checkToken (TokenType.GT) or self.checkToken (TokenType.GTEQ) or self.checkToken (TokenType.LT) or self.checkToken (TokenType.LTEQ) or self.checkToken (TokenType.EQEQ) or self.checkToken (TokenType.NOTEQ)
    
    # expression ::= term {( "-" | "+" ) term}
    def expression (self):
        self.term()
        #You can have 0 or more (+/-) expressions
        while self.checkToken (TokenType.PLUS) or self.checkToken (TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.term()
    
    # term ::= unary {( "/" | "*" ) unary}
    def term (self):
        self.unary()
        #can have 0 or more *// and expressions
        while self.checkToken (TokenType.ASTERISK) or self.checkToken (TokenType.SLASH):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()   
    
    #unary ::= ["+" | "-"] primary
    def unary (self):        
        #optional unary +/-
        if self.checkToken (TokenType.PLUS) or self.checkToken (TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        self.primary()
    
    #primary ::= number | ident
    def primary (self):
        
        if self.checkToken (TokenType.NUMBER):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        elif self.checkToken (TokenType.IDENT):
        
            #Ensure the variable already exists
            if self.curToken.text not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.curToken.text)
            
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        else:
            #error
            self.abort ("Unexpected token at " + self.curToken.text)
        
    #Implementing the nl function that can handle newlines (called at the end of the statement function) - it expects 1 newline character but allows for more 
    # nl ::= '\n'+
    def nl (self):
        #requiring atleast 1 type of newline
        self.match(TokenType.NEWLINE)
        #allows for extra newlines too 
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
        
    
            