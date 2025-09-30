from typing import Literal

from bee.tokenizer import Token

IL = Literal[
    "LOAD_IMMEDIATE",
    "PRINT"
]

def convert_to_il(ast: Token | list) -> list[IL]:
    if isinstance(ast, Token):
        # It's a single value
        return _convert_token(ast)
    # It's something more complex like function call, if statement or something else
    return _convert_longer(ast)


def _convert_token(token: Token) -> list[IL]:
    if token.token_type == "integer":
        if token.value < 0 or token.value > 255:
            raise ValueError(f"Token value {token.value} is out of range")
        return [f"LOAD_IMMEDIATE {token.value}"]  # type: ignore
    raise ValueError(f"Could not convert: {token}. Invalid type: {token.token_type}")

def _convert_longer(tokens: list[Token | list]) -> list[IL]:  # TODO: better naming :smiling_face_with_tear:
    if not tokens:
        return []
    if not isinstance(tokens[0], Token):
        raise ValueError(f"Something went horribly wrong. First value in line isn't token, but rather \"{type(tokens[0]).__name__}\"")

    if tokens[0].token_type == "identifier":
        # It's a function call
        # TODO: make it more extendable
        if tokens[0].value == "print":
            output = []

            for arg in tokens[1]:
                output.extend(_convert_token(arg))

            output.append("PRINT")
            return output
    raise ValueError(f"Could not convert: {tokens}")

def optimize_il(il: list[IL]) -> list[IL]:
    return il
