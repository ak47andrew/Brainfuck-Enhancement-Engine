from typing import Any, Literal
import re

TokenType = Literal["integer", "string", "identifier"]
# TODO: maybe add a whole bunch of custom exceptions?


# TODO: I'm actually dumb :3 Extend this class to get rid of `type: ignore` everywhere and make it more... one-way or smth like that
class Token:
    token_type: TokenType
    value: Any

    def __init__(self, token_type: TokenType, value: Any):
        self.token_type = token_type
        self.value = value

    def __repr__(self) -> str:
        return f"Token(token_type={self.token_type!r}, value={self.value!r})"

    def __str__(self) -> str:
        return repr(self)


object_call_regex = re.compile(r"^\s*([\w_]+)\s*\(\s*(.*)\s*\)\s*$")
integer_regex = re.compile(r"^(\d+)$")
string_regex = re.compile(r"^(\".*\")$")
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


def tokenize(code: str):
    if (out := integer_regex.match(code)) is not None:
        return Token(token_type="integer", value=int(out.group(1)))
    if (out := string_regex.match(code)) is not None:
        return Token(token_type="string", value=out.group(1))
    if (out := object_call_regex.match(code)) is not None:
        tokens = [Token(token_type="identifier", value=out.group(1))]
        args_str = out.group(2).strip()

        if args_str == "":
            tokens.append([]) # type: ignore
        else:
            args = split_args_respecting_quotes(args_str)
            tokens.append([tokenize(arg) for arg in args if arg != ""]) # type: ignore

        return tokens
    # if (out := variable_regex.match(code)) is not None:
    #     return [Token(token_type="variable_declaration", value=out.group(1).strip()), tokenize(out.group(2))]
    # return Token(token_type="identifier", value=code)
    raise ValueError(f"Could not tokenize: {code}")