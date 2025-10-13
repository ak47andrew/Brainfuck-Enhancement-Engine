from bee.tokenizer import Token

def convert_to_il(ast: Token) -> list[str]:
    return _convert_longer(ast) if ast.args is not None else _convert_token(ast)


def _convert_token(token: Token) -> list[str]:
    if token.token_type == "integer":
        if token.value < 0 or token.value > 255:
            raise ValueError(f"Token value {token.value} is out of range")
        return [f"LOAD_IMMEDIATE {token.value}"]
    elif token.token_type == "string":
        # FIXME !!! THIS IS HACKY APPROACH BECAUSE WE'RE CURRENTLY ONLY PRINTING AND PUTTING STRING! FIX THIS ASAP IN THE NEXT RELEASE!
        output: list[str] = []
        for char in token.value[1:-1]:
            output.extend((f'LOAD_IMMEDIATE \"{char}\"', "PUT"))
        return output[:-1] if output else ["LOAD_IMMEDIATE \"\0\""]
    raise ValueError(f"Could not convert: {token}. Invalid type: {token.token_type}")

def _convert_longer(token: Token) -> list[str]:  # type: ignore # TODO: better naming :smiling_face_with_tear:
    if token.token_type == "function_call":
        # TODO: make it more extendable
        output: list[str] = []

        for ind, arg in enumerate(token.args): # pyright: ignore[reportArgumentType, reportOptionalIterable]
            output.extend(_convert_token(arg))
            if ind != len(token.args) - 1 and output[-1].startswith("LOAD_IMMEDIATE \""): # pyright: ignore[reportArgumentType]
                output.extend(("PUT", "LOAD_IMMEDIATE \" \"", "PUT"))  # FIXME: more of a hacky approach :3
                # Fuck... I'm going to hate myself tomorrow morning 0_0

        if token.value == "print":
            output.append("PRINT")
        elif token.value == "put":
            output.append("PUT")
        else:
            raise ValueError(f"Unknown opcode {token.value}")

        return output
    raise ValueError(f"Could not convert: {token}")

def optimize_il(il: list[str]) -> list[str]:
    return il
