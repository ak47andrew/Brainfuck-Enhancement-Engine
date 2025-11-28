from .tokenizer import Token

def convert_to_il(ast: Token) -> list[str]:
    return _convert_longer(ast) if ast.args is not None else _convert_token(ast)


def _convert_token(token: Token) -> list[str]:
    if token.token_type == "integer":
        if token.value < 0 or token.value > 255:
            raise ValueError(f"Token value {token.value} is out of range")
        return [f"LOAD_IMMEDIATE {token.value}"]
    elif token.token_type == "string":
        output: list[str] = []
        for char in token.value[1:-1]:
            output.append(f'LOAD_IMMEDIATE \"{char}\"')
        return output
    raise ValueError(f"Could not convert: {token}. Invalid type: {token.token_type}")

def _convert_longer(token: Token) -> list[str]:  # type: ignore # TODO: better naming :smiling_face_with_tear:
    if token.token_type == "function_call":
        # TODO: make it more extendable
        output: list[str] = []

        for arg in token.args: # pyright: ignore[reportArgumentType, reportOptionalIterable]
            output.extend(_convert_token(arg))
            # if ind != len(token.args) - 1 and output[-1].startswith("LOAD_IMMEDIATE \""): # pyright: ignore[reportArgumentType]
            #     output.extend(("PRINT_SINGLE", "LOAD_IMMEDIATE \" \"", "PRINT_SINGLE"))  # FIXME: more of a hacky approach :3
                # Fuck... I'm going to hate myself tomorrow morning 0_0
                # FIXME: just kill past me off of this earth. He messed up the responsobility. Real solution: just load arguments on top of the stack 
                # and let the command handle what to do between them. For example if we would had an addition function, we don't want printing and loading the space.
                # FIXME: Later. Uhhh.... How can we do it once again...? 

        if token.value == "print":
            output.append("LOAD_IMMEDIATE \"\n\"")
            output.reverse()  # FIXME (?) Is it a good idea to do it here?
            output.append("PRINT_ALL")
        elif token.value == "put":
            output.reverse()  # FIXME (?) Is it a good idea to do it here?
            output.append("PRINT_ALL")
        else:
            raise ValueError(f"Unknown opcode {token.value}")

        return output
    raise ValueError(f"Could not convert: {token}")

def optimize_il(il: list[str]) -> list[str]:
    # LOAD_IMMEDIATE ([^\n]+)\n(PUT|PRINT)
    return il
