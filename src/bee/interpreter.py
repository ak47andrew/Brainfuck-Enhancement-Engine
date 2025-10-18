from .memory_manager import MemoryManager

def _store_string(data: str) -> str:
    pass

def _store_integer(data: int) -> str:
    pass

def _move_stack_top() -> str:
    output = ""

    # Step 0: Move to the SC cell (index 5)
    output += ">!>>>>>"

    # Step 1: Copy to the cell on the right (6) and to the -1 cell (aka the right border cell of the first stack value)
    output += "[->+>!<+>>>>>>]"

    # Step 2: Restore SC cell
    output += ">[-<+>]"

    # Step 3: Move to the -1 cell
    output += ">!<"

    # Step 4: SPECIAL SAUCE: moving left to the adress
    output += "[[[[<]<+>>[>]]<-]<[<]<-]>"

    return output

def translate(mm: MemoryManager, il: str) -> str:
    output = ""

    if il == "STDOUT_ALL":
        # Step 0: Set output type depending on the type of the variable at the top of the stack
        output += ">!>>>[-]"
        if mm.get_top_stack() == "int":
            output += "+"

        # Step 1: Take top of the stack and move to cell 1 using >!
        output += ">!<[<]>[->!>+<<[<]>]"

        # Step 2: Print
        output += ".>!>[-]"
    elif il.startswith("LOAD_IMMEDIATE"):
        il = il.removeprefix("LOAD_IMMEDIATE ")
        output = _move_stack_top()
        if il.startswith("STRING"):
            il.removeprefix("STRING ")
            output += _store_string(il)
        elif il.startswith("INT"):
            il.removeprefix("INT ")
            output += _store_integer(int(il))

        # raw_value: str = " ".join(il.split()[1:])
        # try:
        #     python_value = int(raw_value)
        # except ValueError as e:
        #     if raw_value.startswith('"') and raw_value.endswith('"'):
        #         python_value = raw_value[1:-1]
        #     else:
        #         raise ValueError("Immediate value isn't recognized") from e

        # internal_type: VALUE_TYPES
        # value: int

        # if isinstance(python_value, str):
        #     value = ord(python_value)
        #     internal_type = "char"
        # else:  # int
        #     value = python_value
        #     internal_type = "int"

        # mm.push_stack(internal_type)

        # output += ">!<[<]"
        # output += "+" * value
    else:
        raise ValueError(f"Unrecognized IL command: {il}")

    return output
