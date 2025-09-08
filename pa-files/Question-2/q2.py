#!/bin/python3

import sys

##################### BOILERPLATE BEGINS ############################

# Token types enumeration
##################### YOU CAN CHANGE THE ENUMERATION IF YOU WANT #######################
class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"

# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}


# helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False

    return True


# Tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char=='_')

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(source_code[position]):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                # check if it is a valid identifier
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit():
            lexeme = char
            position += 1

            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # checking if it is a float, or a full-stop
                if next_char == '.':
                    if (position + 1 < len(source_code)):
                        next_next_char = source_code[position+1]
                        if next_next_char.isdigit():
                            is_float = True

                # checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(source_code[position]):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits")

                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme))

    return tokens

########################## BOILERPLATE ENDS ###########################


class Parser:
    """
    Performs syntactical analysis using a recursive descent parser based on the grammar.
    """

    ARITH_OPS = {"+", "-", "*", "/", "^"}
    COMP_OPS = {"<", ">", "="}

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        """Main entry point for parsing. Parses statements until the end of input."""
        if not self.tokens:
            return
        while self.pos < len(self.tokens):
            self.parse_statement()

    # --- Helper Functions ---

    def peek(self):
        """Return the token at the current position without consuming it."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None, expected_value=None):
        """Consume the current token, optionally verifying its type and value."""
        if self.pos >= len(self.tokens):
            raise SyntaxError(
                f"Unexpected end of input. Expected: {expected_value or expected_type or 'token'}"
            )
        token = self.tokens[self.pos]
        tok_type, tok_val = token
        if expected_type and tok_type != expected_type:
            raise SyntaxError(
                f"Unexpected token type: found {tok_type}, expected {expected_type}"
            )
        if expected_value and tok_val != expected_value:
            raise SyntaxError(
                f"Unexpected token value: found '{tok_val}', expected '{expected_value}'"
            )
        self.pos += 1
        return token

    # --- Parsing Functions (one for each grammar rule) ---

    def parse_atom(self):
        """atom ::= INTEGER | FLOAT | IDENTIFIER | KEYWORD(not if/else)"""
        tok = self.peek()
        if not tok:
            raise SyntaxError("Unexpected end of input, expected an atom.")
        ttype, tval = tok
        if ttype in (TokenType.INTEGER, TokenType.FLOAT, TokenType.IDENTIFIER):
            self.consume()
        elif ttype == TokenType.KEYWORD and tval not in ("if", "else"):
            self.consume()
        else:
            raise SyntaxError(
                f"Expected an atom (number, identifier, or 'print'), but found '{tval}'"
            )

    def parse_factor(self):
        """factor ::= "-" factor | "(" cond ")" | atom"""
        tok = self.peek()
        if not tok:
            raise SyntaxError("Unexpected end of input, expected a factor.")
        ttype, tval = tok
        if ttype == TokenType.SYMBOL and tval == "-":
            self.consume(TokenType.SYMBOL, "-")
            self.parse_factor()
        elif ttype == TokenType.SYMBOL and tval == "(":
            self.consume(TokenType.SYMBOL, "(")
            self.parse_cond()
            self.consume(TokenType.SYMBOL, ")")
        else:
            self.parse_atom()

    def parse_expr(self):
        """expr ::= factor (arith_op factor)*"""
        self.parse_factor()
        while True:
            tok = self.peek()
            if tok and tok[0] == TokenType.SYMBOL and tok[1] in self.ARITH_OPS:
                self.consume()
                self.parse_factor()
            else:
                break

    def parse_cond(self):
        """cond ::= expr (comp_op expr)?"""
        tok = self.peek()
        if not tok or (tok[0] == TokenType.KEYWORD and tok[1] in ("else", "print")):
            self.parse_atom()
            return
        self.parse_expr()
        tok = self.peek()
        if tok and tok[0] == TokenType.SYMBOL and tok[1] in self.COMP_OPS:
            self.consume()
            self.parse_expr()

    def parse_atomic_statement(self):
        """atomic_statement ::= "print" expr | atom"""
        tok = self.peek()
        if not tok:
            raise SyntaxError("Unexpected end of input, expected a statement.")
        if tok[0] == TokenType.KEYWORD and tok[1] == "print":
            self.consume(TokenType.KEYWORD, "print")
            next_tok = self.peek()
            if next_tok and not (
                next_tok[0] == TokenType.KEYWORD and next_tok[1] == "else"
            ):
                self.parse_expr()
        else:
            self.parse_atom()

    def parse_if_statement(self):
        """if_statement ::= "if" cond ("then")? statement ("else" statement)? ("endif")?"""
        self.consume(TokenType.KEYWORD, "if")
        self.parse_cond()
        tok = self.peek()
        if tok and tok[0] == TokenType.IDENTIFIER and tok[1] == "then":
            self.consume(TokenType.IDENTIFIER, "then")
        self.parse_statement()
        tok = self.peek()
        if tok and tok[0] == TokenType.KEYWORD and tok[1] == "else":
            self.consume(TokenType.KEYWORD, "else")
            self.parse_statement()

        tok = self.peek()
        if tok and tok[0] == TokenType.IDENTIFIER and tok[1] == "endif":
            self.consume(TokenType.IDENTIFIER, "endif")

    def parse_statement(self):
        """statement ::= if_statement | atomic_statement"""
        tok = self.peek()
        if not tok:
            raise SyntaxError("Unexpected end of input, expected a statement.")

        if tok[0] == TokenType.KEYWORD and tok[1] == "if":
            self.parse_if_statement()
        else:
            self.parse_atomic_statement()


def checkGrammar(tokens):
    """
    Initializes the Parser and runs the syntactical analysis.
    """
    parser = Parser(tokens)
    parser.parse()


def main():
    line = input()
    line = line.strip()
    if not line:
        return
    try:
        tokens = tokenize(line)
        checkGrammar(tokens)
        print("No Error")
    except ValueError:
        print("Lexical Error")
    except SyntaxError:
        print("Syntax Error")


if __name__ == "__main__":
    main()
