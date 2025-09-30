from bee.memory_manager import MemoryManager, VALUE_TYPES
from bee.intermidiate_language import IL


def translate(mm: MemoryManager, il: IL) -> str:
    output = ""

    if il == "PRINT":
        # Step 0: Set output type depending on the type of the variable at the top of the stack
        output += ">!>>>[-]"
        if mm.get_top_stack() == "int":
            output += "+"

        # Step 1: Take top of the stack and move to cell 1 using >!
        output += ">!<[<]>[->!>+<<[<]>]"

        # Step 2: Print
        output += "."

        # Step 3: output newline
        output += "\n>!>>>[-]<<[-]++++++++++.[-]"

        # Step 3: Repeat until there's still characters
        # TODO: It still only support chars, so we don't need that, but add this for strings and some other stuff later
    elif il == "PUT":
        # TODO: maybe spilt into lower-level opcodes? PUT and PRINT is pretty similar
        # Step 0: Set output type depending on the type of the variable at the top of the stack
        output += ">!>>>[-]"
        if mm.get_top_stack() == "int":
            output += "+"

        # Step 1: Take top of the stack and move to cell 1 using >!
        output += ">!<[<]>[->!>+<<[<]>]"

        # Step 2: Print
        output += ".>!>[-]"
    elif il.startswith("LOAD_IMMEDIATE"):
        raw_value: str = il.split()[1]
        if raw_value.isdigit():
            python_value = int(raw_value)
        elif raw_value.startswith('"') and raw_value.endswith('"'):
            python_value = raw_value[1:-1]
        else:
            raise ValueError("Immediate value isn't recognized")

        internal_type: VALUE_TYPES
        value: int

        if isinstance(python_value, str):
            value = ord(python_value)
            internal_type = "char"
        elif isinstance(python_value, int):
            value = python_value
            internal_type = "int"
        else:
            raise ValueError(f"Unknown value type {type(python_value)}: {python_value}")

        mm.push_stack(internal_type)

        output += ">!<[<]"
        output += "+" * value
    else:
        raise ValueError(f"Unrecognized IL command: {il}")

    return output
