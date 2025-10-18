from .tokenizer import Token

def convert_to_il(ast: Token) -> list[str]:
    return _convert_longer(ast) if ast.args is not None else _convert_token(ast)


def _convert_token(token: Token) -> list[str]:
    if token.token_type == "integer":
        return [f"LOAD_IMMEDIATE INT {token.value}"]
    elif token.token_type == "string":
        return [f"LOAD_IMMEDIATE STRING {token.value}"]
    raise ValueError(f"Could not convert: {token}. Invalid type: {token.token_type}")

def _convert_longer(token: Token) -> list[str]:  # TODO: better naming :smiling_face_with_tear:
    if token.token_type == "function_call":
        output: list[str] = []

        for arg in token.args: # pyright: ignore[reportArgumentType, reportOptionalIterable]
            output.extend(convert_to_il(arg))

        if token.value == "print":
            output = output[::-1]  # Reverse to print it out more easily
            output.append("LOAD_IMMEDIATE STRING \n")
            output.append("STDOUT_ALL")
        elif token.value == "put":
            output = output[::-1]  # Reverse to print it out more easily
            output.append("STDOUT_ALL")
        else:
            raise ValueError(f"Unknown opcode {token.value}")

        return output
    raise ValueError(f"Could not convert: {token}")

def optimize_il(il: list[str]) -> list[str]:
    return il
