class Tape:
    pointer: int
    used_cells: set[int]

    def __init__(self):
        self.used_cells = set()
        self.pointer = 0

    def set_cells(self, indexes: list[int]):
        self.used_cells = self.used_cells.union(indexes)

    def move_pointer(self, index: int):
        self.pointer = index

class MemoryManager:
    tape: Tape

    def __init__(self):
        self.tape = Tape()
