import time

def evaluate(code: str):
    code     = cleanup(list(code))
    bracemap = buildbracemap(code)

    cells, codeptr, cellptr = [0], 0, 0

    while codeptr < len(code):
        command = code[codeptr]

        if command == ">":
            cellptr += 1
            if cellptr == len(cells): cells.append(0)

        if command == "<":
            cellptr = 0 if cellptr <= 0 else cellptr - 1

        if command == "+":
            cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

        if command == "-":
            cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

        if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
        if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
        if command == ".": print(chr(cells[cellptr]), end="")
        if command == "@": 
            print("===Debug info===")
            print(f"Cell value: {chr(cells[cellptr])}")
            print(f"Cell value [numerical]: {cells[cellptr]}")
            print(f"Current code pointer: {codeptr}")
            print(f"Current cell pointer: {cellptr}")
            print(f"Cells length: {len(cells)}")
            filename = f"debug-{time.time()}.txt"
            with open(filename, "w") as f:
                f.write(str(cells))
            print(f"Saved to {filename}")
        if command == ",": cells = handle_input(cells, cellptr)

        codeptr += 1


def cleanup(code: list[str]):
    return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-', '@'], code))

def handle_input(l: list[int], ptr: int) -> list[int]:
    g = input()
    for i, c in enumerate(g):
        l[ptr + i] = ord(c)
    return l

def buildbracemap(code: str):
    temp_bracestack, bracemap = [], {}

    for position, command in enumerate(code):
        if command == "[": temp_bracestack.append(position)
        if command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start

    return bracemap
