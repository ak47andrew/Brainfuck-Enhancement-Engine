from bee.tokenizer import Token

def convert_to_il(ast: Token | list) -> list[str]: # type: ignore
    return _convert_token(ast) if isinstance(ast, Token) else _convert_longer(ast)


def _convert_token(token: Token) -> list[str]:
    if token.token_type == "integer":
        if token.value < 0 or token.value > 255:
            raise ValueError(f"Token value {token.value} is out of range")
        return [f"LOAD_IMMEDIATE {token.value}"]
    elif token.token_type == "string":
        # if len(token.value) > 3:  # "a"
        #     raise ValueError(f"Token value {token.value} is too long. Only chars are supported for now")
        # return [f"LOAD_IMMEDIATE {token.value}"]  # type: ignore
        # FIXME !!! THIS IS HACKY APPROACH BECAUSE WE'RE CURRENTLY ONLY PRINTING AND PUTTING STRING! FIX THIS ASAP IN THE NEXT RELEASE!
        output: list[str] = []
        for char in token.value[1:-1]:
            output.extend((f'LOAD_IMMEDIATE \"{char}\"', "PUT"))
        return output[:-1] if output else ["LOAD_IMMEDIATE \"\0\""]
    raise ValueError(f"Could not convert: {token}. Invalid type: {token.token_type}")

def _convert_longer(tokens: list[Token | list]) -> list[str]:  # type: ignore # TODO: better naming :smiling_face_with_tear:
    if not tokens:
        return []
    if not isinstance(tokens[0], Token):
        raise ValueError(f"Something went horribly wrong. First value in line isn't token, but rather \"{type(tokens[0]).__name__}\"") # pyright: ignore[reportUnknownArgumentType]

    if tokens[0].token_type == "identifier":
        # It's a function call
        # TODO: make it more extendable
        output: list[str] = []

        for arg in tokens[1]: # type: ignore
            output.extend(_convert_token(arg)) # type: ignore

        if tokens[0].value == "print":
            output.append("PRINT")
        elif tokens[0].value == "put":
            output.append("PUT")
        else:
            raise ValueError(f"Unknown opcode {tokens[0].value}")

        return output
    raise ValueError(f"Could not convert: {tokens}")

def optimize_il(il: list[str]) -> list[str]:
    return il
