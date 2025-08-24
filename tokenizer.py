from typing import Any, Literal
import re


TokenType = Literal["string", "integer", "float", "boolean", "identifier"]
class Token:
    type: TokenType
    value: Any

    def __init__(self, type: TokenType, value: Any):
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:
        return super().__repr__().replace(">", f" ({self.type=}; {self.value=})>")
    
    def __str__(self) -> str:
        return repr(self)

object_call_regex = re.compile(r"^\s*([\w\d_]+)\s*\(\s*(.*)\s*\)\s*$")
string_regex = re.compile(r'^"(.*)"$')
integer_regex = re.compile(r"^((?:\d)+)$")
float_regex = re.compile(r"^((?:\d)+\.(?:\d)+)$")
variable_regex = re.compile(r"^var\s+(.+)\s*=\s*(.+)$")
bool_regex = re.compile(r"^(true|false)$")

def split_args_respecting_quotes(s: str) -> list[str]:
    """Split arguments by commas, but respect commas inside quotes"""
    parts = []
    current = []
    in_string = False
    escaped = False

    for char in s:
        if escaped:
            current.append(char)
            escaped = False
        elif char == '\\':
            escaped = True
        elif char == '"':
            in_string = not in_string
            current.append(char)
        elif char == ',' and not in_string:
            parts.append(''.join(current).strip())
            current = []
        else:
            current.append(char)

    if current:
        parts.append(''.join(current).strip())

    return parts

def tokenize(code: str):
    if (out := string_regex.match(code)) is not None:
        return Token(type="string", value=out.group(1))
    if (out := integer_regex.match(code)) is not None:
        return Token(type="integer", value=int(out.group(1)))
    if (out := float_regex.match(code)) is not None:
        return Token(type="float", value=float(out.group(1)))
    if (out := bool_regex.match(code)) is not None:
        return Token(type="boolean", value=out.group(1) == "true")
    if (out := object_call_regex.match(code)) is not None:
        tokens: list = [Token(type="identifier", value=out.group(1))] 
        args_str = out.group(2).strip()

        if args_str == "":
            tokens.append([])
        else:
            args = split_args_respecting_quotes(args_str)
            tokens.append([tokenize(arg) for arg in args if arg != ""])

        return tokens
    return Token(type="identifier", value=code)
