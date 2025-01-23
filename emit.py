#Enitter object will keep track of the generated code & outputs it

#'code' is the string containing the C code that is emitted 
#'header' contains things that will be prepended to the code
#'fullPath' is the path to write the file containing the C code


class Emitter:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.header = ""
        self.code = ""
    
    #adds a fragment of C code 
    def emit (self, code):
        self.code += code
    
    #adds a fragment that ends a line
    def emitLine (self, code):
        self.code += code + '\n'
    
    #adds a line of C code to the top of the C code file (ie. library header, main function, variable declarations)
    def headerLine (self, code):
        self.header += code + '\n'
    
    #writes the C code to a file
    def writeFile (self):
        with open (self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code)