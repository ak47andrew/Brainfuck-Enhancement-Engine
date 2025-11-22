from typing import Any, Optional


class Macro:
    name: str
    args: dict[str, Any]
    lines: list[str]

    def __init__(self, name: str, args: dict[str, Any]):
        self.name = name
        self.args = args
        self.lines = []

    def add_line(self, line: str):
        self.lines.append(line)

def preprocess(lines: list[str]) -> list[str]:
    macros: Optional[Macro] = None
    output: list[str] = []

    for line in lines:
        if not line.startswith("#"):
            if macros is not None:
                macros.add_line(line)
            else:
                output.append(line)
            continue

        # This is our guy!
        parts = line.removeprefix("#").split() # ["start", "loop", "i", "3", "4"]
        if parts[0] == "start":
            if macros is not None:
                raise ValueError("Nested macro definitions are not allowed!")
            
            match parts[1]:
                case "loop":
                    macros = Macro(parts[1], {
                        "var": parts[2],
                        "start": int(parts[3]),
                        "end": int(parts[4]),
                    })
                case _:
                    raise ValueError(f"Unknown macro name: {parts[1]}")

        
        elif parts[0] == "end":
            if macros is None:
                raise ValueError("No macro started before ending!")
            if macros.name != parts[1]:
                raise ValueError(f"End macro does not match the start macro: {macros.name} != {parts[1]}")
            
            match parts[1]:
                case "loop":
                    if macros.args["var"] != parts[2]:
                        raise ValueError(f"Variable name does not match the start macro: {macros.args['var']} != {parts[2]}")
                    for var in range(macros.args["start"], macros.args["end"] + 1):
                        for line in macros.lines:
                            output.append(line.replace(f"$({macros.args['var']})", str(var)))
                    macros = None
                case _:
                    raise ValueError(f"Unknown macro name: {parts[1]}")  # That's probably will never happen, but just so everyone here is alright
    
    return output
