from sys import argv
import cleanup
import tokenizer
import interpreter
from internal_types import OutputTokenType
from memory_manager import MemoryManager

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python gdc_compiler.py <file_path>")
    
    file_path = argv[1] if argv[1].endswith(".gdc") else "code.bee"

    with open(file_path, "r") as file:
        code = file.read()
    
    pre_tokens = cleanup.pre_compiling(code)
    token_lines = [tokenizer.tokenize(t) for t in pre_tokens]

    bf_code = ""
    mm = MemoryManager()
    for line in token_lines:
        output = interpreter.evaluate_tokens(mm, line)
        if type(output) == OutputTokenType:
            bf_code += output.value

    bf_code = cleanup.pre_output(bf_code)

    print(f"Brainfuck code:\n{bf_code}")
