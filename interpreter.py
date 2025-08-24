from typing import Any, Callable
from tokenizer import Token
from internal_types import InternalType, StringType, OutputTokenType, IntegerType, FloatType
from memory_manager import MemoryManager

def evaluate_tokens(mm: MemoryManager, tokens):
    if type(tokens) != list:
        return evaluate_internal_type(tokens)
    
    if len(tokens) == 0:
        return None
    if tokens[0].type == "identifier":
        # FIXME it's not only for function calls you dumbass. Variables is also marked as identifier! 
        # But... variables aren't in the lang yet, so... don't worry about it YET
        
        # Handle function call #? Generalize for classes/other stuff if I add it later
        # Format is: [identifier, [arg1, arg2]]
        obj = indetidentifiers.get(tokens[0].value)
        if obj is None:
            raise ValueError(f"Unknown identifier: {tokens[0].value}")
        return obj(mm, [evaluate_tokens(mm, arg) for arg in tokens[1]])

def evaluate_internal_type(token: Token) -> InternalType:
    if token.type == "string":
        return StringType(token.value)
    if token.type == "integer":
        return IntegerType(token.value)
    if token.type == "float":
        return FloatType(token.value)
    raise ValueError(f"Invalid internal type: {token.type} with value: {token.value}")

# === Indetidentifiers ===

def print_(mm: MemoryManager, data: list[InternalType | None]):
    output = ""

    string_types = [str(x.value) for x in data if x != None and type(x) in [IntegerType, StringType, FloatType]]

    output_token_types: list[OutputTokenType] = list(filter(lambda x: type(x) == OutputTokenType, data))  # type: ignore

    # If any other types aren't that, raise an error
    if len(string_types) + len(output_token_types)!= len(data):
        raise ValueError("Invalid arguments passed")
    
    # Firstly handle output tokens because logically they would (and was) called first
    for output_token_type in output_token_types:
        output += output_token_type.value


    ## And then handle string types
    # Convert all args into a single string
    concated = " ".join([g for g in string_types]) + "\n"

    for char in concated:
        value = ord(char)
        index = mm.get_index(value)
        if index == -1:
            index = mm.get_ununsed(1)
            output += mm.go(index)
            output += mm.set(value)
        output += mm.go(index) + "."

    return OutputTokenType(output)

indetidentifiers: dict[str, Callable[[MemoryManager, list[InternalType | None]], Any]] = {
    "print": print_
}
