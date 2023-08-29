from typing import List, Dict

# Represents tokens that our language understands in parsing.
class TokenType:
    # Literal Types
    Number = "Number"
    Identifier = "Identifier"
    # Keywords
    Let = "Let"
    Const = "Const"
    Fn = "Fn"  # fn

    # Grouping & Operators
    BinaryOperator = "BinaryOperator"
    Equals = "Equals"
    Comma = "Comma"
    Dot = "Dot"
    Colon = "Colon"
    Semicolon = "Semicolon"
    OpenParen = "OpenParen"  # (
    CloseParen = "CloseParen"  # )
    OpenBrace = "OpenBrace"  # {
    CloseBrace = "CloseBrace"  # }
    OpenBracket = "OpenBracket"  # [
    CloseBracket = "CloseBracket"  # ]
    EOF = "EOF"  # Signified the end of file

# Constant lookup for keywords and known identifiers + symbols.
KEYWORDS: Dict[str, TokenType] = {
    "let": TokenType.Let,
    "const": TokenType.Const,
    "fn": TokenType.Fn,
}

# Represents a single token from the source code.
class Token:
    def __init__(self, value: str, type: TokenType):
        self.value = value  # contains the raw value as seen inside the source code.
        self.type = type  # tagged structure.

# Returns a token of a given type and value
def token(value="", type: TokenType = TokenType.EOF) -> Token:
    return Token(value, type)

# Returns whether the character passed in alphabetic -> [a-zA-Z]
def isalpha(src: str) -> bool:
    return src.isalpha()

# Returns true if the character is whitespace like -> [\s, \t, \n]
def isskippable(str: str) -> bool:
    return str in [" ", "\n", "\t", "\r"]

# Return whether the character is a valid integer -> [0-9]
def isint(str: str) -> bool:
    return str.isdigit()

# Given a string representing source code: Produce tokens and handles
# possible unidentified characters.
# - Returns an array of tokens.
# - Does not modify the incoming string.
def tokenize(sourceCode: str) -> List[Token]:
    tokens = []
    src = list(sourceCode)

    # Produce tokens until the EOF is reached.
    while src:
        # BEGIN PARSING ONE CHARACTER TOKENS
        if src[0] == "(":
            tokens.append(token(src.pop(0), TokenType.OpenParen))
        elif src[0] == ")":
            tokens.append(token(src.pop(0), TokenType.CloseParen))
        elif src[0] == "{":
            tokens.append(token(src.pop(0), TokenType.OpenBrace))
        elif src[0] == "}":
            tokens.append(token(src.pop(0), TokenType.CloseBrace))
        elif src[0] == "[":
            tokens.append(token(src.pop(0), TokenType.OpenBracket))
        elif src[0] == "]":
            tokens.append(token(src.pop(0), TokenType.CloseBracket))
        # HANDLE BINARY OPERATORS
        elif src[0] in "+-*/%":
            tokens.append(token(src.pop(0), TokenType.BinaryOperator))
        # Handle Conditional & Assignment Tokens
        elif src[0] == "=":
            tokens.append(token(src.pop(0), TokenType.Equals))
        elif src[0] == ";":
            tokens.append(token(src.pop(0), TokenType.Semicolon))
        elif src[0] == ":":
            tokens.append(token(src.pop(0), TokenType.Colon))
        elif src[0] == ",":
            tokens.append(token(src.pop(0), TokenType.Comma))
        elif src[0] == ".":
            tokens.append(token(src.pop(0), TokenType.Dot))
        # HANDLE MULTICHARACTER KEYWORDS, TOKENS, IDENTIFIERS, ETC...
        else:
            # Handle numeric literals -> Integers
            if isint(src[0]):
                num = ""
                while src and isint(src[0]):
                    num += src.pop(0)

                # append new numeric token.
                tokens.append(token(num, TokenType.Number))
            # Handle Identifier & Keyword Tokens.
            elif isalpha(src[0]):
                ident = ""
                while src and isalpha(src[0]):
                    ident += src.pop(0)

                # CHECK FOR RESERVED KEYWORDS
                reserved = KEYWORDS.get(ident)
                # If value is not None, then the identifier is
                # recognized keyword.
                if reserved is not None:
                    tokens.append(token(ident, reserved))
                else:
                    # Unrecognized name must mean a user-defined symbol.
                    tokens.append(token(ident, TokenType.Identifier))
            elif isskippable(src[0]):
                # Skip uneeded chars.
                src.pop(0)
            # Handle unrecognized characters.
            # TODO: Implement better errors and error recovery.
            else:
                print("Unrecognized character found in source:", ord(src[0]), src[0])
                exit(1)

    tokens.append(token(type=TokenType.EOF, value="EndOfFile"))
    return tokens
