from bee.memory_manager import MemoryManager, VALUE_TYPES

def translate(mm: MemoryManager, il: str) -> str:
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
        # TODO: maybe split into lower-level opcodes? PUT and PRINT are pretty similar
        # Step 0: Set output type depending on the type of the variable at the top of the stack
        output += ">!>>>[-]"
        if mm.get_top_stack() == "int":
            output += "+"

        # Step 1: Take top of the stack and move to cell 1 using >!
        output += ">!<[<]>[->!>+<<[<]>]"

        # Step 2: Print
        output += ".>!>[-]"
    elif il.startswith("LOAD_IMMEDIATE"):
        raw_value: str = " ".join(il.split()[1:])
        try:
            python_value = int(raw_value)
        except ValueError as e:
            if raw_value.startswith('"') and raw_value.endswith('"'):
                python_value = raw_value[1:-1]
            else:
                raise ValueError("Immediate value isn't recognized") from e

        internal_type: VALUE_TYPES
        value: int

        if isinstance(python_value, str):
            value = ord(python_value)
            internal_type = "char"
        else:  # int
            value = python_value
            internal_type = "int"

        mm.push_stack(internal_type)

        output += ">!<[<]"
        output += "+" * value
    else:
        raise ValueError(f"Unrecognized IL command: {il}")

    return output
