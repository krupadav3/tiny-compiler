# "Teeny Tiny" Compiler

Welcome to Teeny Tiny Compiler! A minimalistic yet powerful compiler project designed to display the fundamentals of compilers & inspire exploration into the world of programming language design.
This project takes inspiration from Austin Henley's [Teeny Tiny Compiler] (https://austinhenley.com/blog/teenytinycompiler1.html), involving a lot of learning, and is tailored to reflect my own passion for language processing. 

# Project Structure
- **Lexical Analysis (Lexer)**: Breaks the input source code into tokens (keywords, identifiers, operators) 
- **Parser (Tokenizer)**: Constructs an Abstract Syntax Tree (AST) that represents the structure of the of the code, from the lexer. The parser verifies whether the sequences of tokens conform to the syntax rules.
- **Emitter**: Converts the AST into C code

![](https://austinhenley.com/blog/images/compilersteps.png)

# Why Build a Compiler?
This project was built to:
 - Gain a deeper understanding of how programming languages work under the hood (when I click "compile & run", what actually happens?!) 
 - Explore the Fundamental concepts of compilers including lexical anlaysis, parsing, and code generation
 - Provides a starting point for others interested in compilers and language design

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/krupadav3/tiny-compiler.git
   ```

2. Navigate to the project directory:
   ```bash
   cd teeny-tiny-compiler
   ```
3. Build the project using the provided Bash script:
   ```bash
   bash build.sh hello.teeny
   ```
4. Run the compiled executable:
   ```bash
   ./hello
   ```
---


## Roadmap
- [ ] Add support for FOR loops, Arrays, Record Types (eg. integer, strings)
- [ ] Add an AST representation
- [ ] Instead of "Teeny Tiny", create my own Programming Language 
- [ ] Instead of C, compile it to Assembly Code

## Acknowledgements
- Inspired by Austin Henley's [Teeny Tiny Compiler] (https://austinhenley.com/blog/teenytinycompiler1.html)
- Thanks to the open-source community for compiler resources and discussions
