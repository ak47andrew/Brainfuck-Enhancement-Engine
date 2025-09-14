from typing import Any, Callable
from tokenizer import Token
from internal_types import InternalType, StringType, OutputTokenType, IntegerType, FloatType, BooleanType
from memory_manager import MemoryManager

def evaluate_tokens(mm: MemoryManager, tokens):
    if type(tokens) != list:
        return evaluate_internal_type(mm, tokens)
    
    if len(tokens) == 0:
        return None
    if tokens[0].type == "identifier":
        # Handle function call # TODO: Generalize for classes/other stuff if I add it later
        # Format is: [identifier, [arg1, arg2]]
        obj = identifiers.get(tokens[0].value)
        if obj is None:
            raise ValueError(f"Unknown identifier: {tokens[0].value}")
        return obj(mm, [evaluate_tokens(mm, arg) for arg in tokens[1]])
    if tokens[0].type == "variable_declaration":
        # Okay, I moved variable declaration here instead of cramping it into identifier
        # Format is: [variable_name, value]
        return store_variable(mm, tokens[0].value, tokens[1])
    return None

def evaluate_internal_type(mm: MemoryManager, token: Token) -> InternalType:
    if token.type == "string":
        return StringType(token.value)
    if token.type == "integer":
        return IntegerType(token.value)
    if token.type == "float":
        return FloatType(token.value)
    if token.type == "boolean":
        return BooleanType(token.value)
    if token.type == "identifier":
        return load_variable(mm, token.value)
    raise ValueError(f"Invalid internal type: {token.type} with value: {token.value}")

def store_variable(mm: MemoryManager, name: str, value: Token) -> OutputTokenType:
    """Returns brainfuck code to store that variable in memory"""
    internal_type = evaluate_internal_type(mm, value)
    memory_layout = internal_type.get_memory_layout()
    memory_address = mm.get_unused(len(memory_layout))

    bf_code = ""
    bf_code += mm.go(memory_address)
    bf_code += mm.set(memory_layout)

    variables[name] = (memory_address, type(internal_type))

    return OutputTokenType(bf_code)

def load_variable(mm: MemoryManager, name: str) -> InternalType:
    initial_pointer = mm.pointer

    if name not in variables:
        raise ValueError(f"Variable {name} is not defined")

    memory_address, internal_type = variables[name]

    mm.pointer = memory_address
    obj = internal_type.get_value(mm)

    mm.pointer = initial_pointer
    return obj

# === Identifiers ===

def print_(mm: MemoryManager, data: list[InternalType | None]):
    output = ""

    string_types = [str(x) for x in data if x is not None and type(x) in [IntegerType, StringType, FloatType, BooleanType]]

    output_token_types: list[OutputTokenType] = list(filter(lambda x: type(x) == OutputTokenType, data))  # type: ignore

    # If any other types aren't that, raise an error
    if len(string_types) + len(output_token_types)!= len(data):
        raise ValueError("Invalid arguments passed")
    
    # Firstly handle output tokens because logically they would (and was) called first
    for output_token_type in output_token_types:
        output += output_token_type.value


    ## And then handle string types
    # Convert all args into a single string
    concatenated = " ".join([g for g in string_types]) + "\n"

    for char in concatenated:
        value = ord(char)
        index = mm.get_index(value)
        if index == -1:
            index = mm.get_unused(1)
            output += mm.go(index)
            output += mm.set([value])
        output += mm.go(index) + "."

    return OutputTokenType(output)

identifiers: dict[str, Callable[[MemoryManager, list[InternalType | None]], Any]] = {
    "print": print_
}

variables: dict[str, tuple[int, type[InternalType]]] = dict()  # Name of the variable and index in memory
