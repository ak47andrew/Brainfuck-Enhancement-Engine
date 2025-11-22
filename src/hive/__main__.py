from sys import argv
from typing import Any

from .interpreter import translate
from .memory_manager import MemoryManager
from .tokenizer import tokenize, Token
from .intermidiate_language import convert_to_il, optimize_il
from .cleanup import pre_compiling, pre_output

def process_args() -> dict[str, Any] | None:
    args = argv[1:]
    if not args:
        return None

    if "--debug" in args:
        debug = True
        args.remove("--debug")
    else:
        debug = False

    return (
        None
        if len(args) != 1
        else {
            "file": args[0],
            "debug": debug,
        }
    )

if __name__ == "__main__":
    config = process_args()
    if config is None:
        print("Usage: bee <filename> [--debug]")
        exit(1)

    # Step 0. Get file
    with open(config["file"], "r") as f:
        code = f.read()
    if config["debug"]:
        print(f"Read file successfully. Got: {code}\n")

    # Step 1. Get individual lines
    lines = pre_compiling(code)
    if config["debug"]:
        print(f"Pre-compiling file successfully. Got:\n{"\n".join(lines)}\n")

    # Step 2. Tokenize them
    tokens: list[Token] = []
    for idx, line in enumerate(lines):
        try:
            tokens.append(tokenize(line))
        except Exception as e:
            print(f"Error tokenizing line {idx+1}: {line}\n{e}")
            if config.get("debug"):
                import traceback
                traceback.print_exc()
    if config["debug"]:
        print(f"Tokenizing file successfully. Got:\n{"\n".join(map(str, tokens))}\n")

    # Step 3. Convert to IL
    il: list[str] = []
    for token in tokens:
        il.extend(convert_to_il(token))
    if config["debug"]:
        print(f"Converted AST successfully. Got:\n{"\n".join(il)}\n")

    # Step 4. Optimize IL
    il = optimize_il(il)
    if config["debug"]:
        print(f"Optimized IL successfully. Got:\n{"\n".join(il)}\n")

    mm = MemoryManager()

    bf_code = "".join(translate(mm, op) + "\n" for op in il)
    if config["debug"]:
        print(f"Translated IL successfully. Unoptimized bf code:\n{bf_code}\n")

    # Step 6. Optimize brainfuck
    bf_code = pre_output(bf_code)

    if config["debug"]:
        print("Brainfuck code:")
    print(bf_code)
