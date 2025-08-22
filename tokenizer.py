from typing import Literal
import re


TokenType = Literal["string", "identifier", "unknown"]
class Token:
    type: TokenType
    value: str

    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:
        return super().__repr__().replace(">", f" ({self.type=}; {self.value=})>")
    
    def __str__(self) -> str:
        return repr(self)

object_call_regex = re.compile(r"^\s*([\w\d_]+)\s*\(\s*(.*)\s*\)\s*$")
string_regex = re.compile(r'^"(.*)"$')

def tokenize(code: str):
    if (out := object_call_regex.match(code)) is not None:
        tokens: list = [Token(type="identifier", value=out.group(1))] 
        args = out.group(2).split(",")
        if args[0] == "":
            tokens.append([])
        else:
            tokens.append([tokenize(arg.strip()) for arg in args])
        return tokens
    if (out := string_regex.match(code)) is not None:
        return Token(type="string", value=out.group(1))
    print(f"[WARNING] [Tokenizer] Unexpected token: {code}")
    return Token(type="unknown", value=code)
