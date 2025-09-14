class MemoryManager:
    tape: list[int]
    used: list[int]
    pointer: int

    def __init__(self):
        self.tape = [0]
        self.used = []
        self.pointer = 0
    
    def get_value(self, index: int | None = None) -> int:
        """Get value of the given cell by its index"""
        if index is None:
            index = self.pointer
        if index >= len(self.tape):
            return 0 # Cell not yet allocated, so return 0 (it'll be initialized with 0)

        return self.tape[index]

    def set(self, values: list[int]):
        # TODO: change to new algorythm that returns shorter bf code. For now it just works
        init_pos = self.pointer
        output_bf = ""
        for value in values:
            if value < 0 or value > 255:
                raise ValueError("This value can't be stored in memory. Brainfuck stores data in 8-bit unsigned integers")
            output_bf += self._set(value)
            output_bf += self.go(self.pointer + 1)
        output_bf += self.go(init_pos)
        return output_bf
    
    def _set(self, value: int) -> str:
        index = self.pointer
        """Set value of the cell that pointer is currently pointing to"""
        if index >= len(self.tape):
            # This changes the cell so we need to allocate
            self.tape.extend([0] * (index - len(self.tape) + 1))
        
        diff_value = value - self.tape[index]

        self.tape[index] = value
        if index not in self.used:
            self.used.append(index)
            self.used.sort()

        return ("+" if diff_value >= 0 else "-") * abs(diff_value)
    
    def go(self, index: int) -> str:
        """Move the pointer to the given cell by its index"""
        
        diff_move = index - self.pointer
        self.pointer = index

        return (">" if diff_move >= 0 else "<") * abs(diff_move)

    def get_index(self, value: int) -> int:
        """Get the index of the first occurrence of the given value in the tape

        Return -1 if the value is not found in the tape"""
        try:
            return self.tape.index(value)
        except ValueError:
            return -1
    
    def get_unused(self, n: int) -> int:
        """Find the first cell with an unallocated/unused gap of size N"""
        if n <= 0:
            raise ValueError("N must be a positive integer")
        if not self.used:
            return 0
        
        if self.used[0] > 0 and self.used[0] >= n:
            return 0
        
        for i in range(len(self.used) - 1):
            gap_size = self.used[i+1] - self.used[i] - 1
            if gap_size >= n:
                return self.used[i] + 1
        
        return len(self.tape)
