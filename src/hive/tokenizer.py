from typing import Any, Literal, Optional, Self
import re

TokenType = Literal["integer", "string", "identifier", "function_call"]
# TODO: maybe add a whole bunch of custom exceptions?


class Token:
    token_type: TokenType
    value: Any
    args: Optional[list[Self]]

    def __init__(self, token_type: TokenType, value: Any, args: Optional[list[Self]] = None):
        self.token_type = token_type
        self.value = value
        self.args = args

    def __repr__(self) -> str:
        return f"Token(token_type={self.token_type!r}, value={self.value!r}, args={self.args!r})"

    def __str__(self) -> str:
        return repr(self)


object_call_regex = re.compile(r"^\s*([\w_]+)\s*\(\s*(.*)\s*\)\s*$")
integer_regex = re.compile(r"^(\d+)$")
string_regex = re.compile(r"^(\".*\")$")  # TODO: fix newlines
variable_regex = re.compile(r"^var\s+(.+)\s*=\s*(.+)$")


def split_args_respecting_quotes(s: str) -> list[str]:
    """Split arguments by commas, but respect commas inside quotes"""
    parts: list[str] = []
    current: list[str] = []
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


def tokenize(code: str) -> Token:

    if (out := integer_regex.match(code)) is not None:
        return Token(token_type="integer", value=int(out.group(1)))
    if (out := string_regex.match(code)) is not None:
        return Token(token_type="string", value=out.group(1).replace("\\n", "\n"))
    if (out := object_call_regex.match(code)) is not None:
        args_str = out.group(2).strip()

        if args_str == "":
            args = []
        else:
            args_splitted = split_args_respecting_quotes(args_str)
            args = [tokenize(arg) for arg in args_splitted if arg != ""]

        return Token(token_type="function_call", value=out.group(1), args=args)
    # if (out := variable_regex.match(code)) is not None:
    #     return [Token(token_type="variable_declaration", value=out.group(1).strip()), tokenize(out.group(2))]
    # return Token(token_type="identifier", value=code)
    raise ValueError(f"Could not tokenize: {code}")