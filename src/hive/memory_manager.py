from typing import Literal
from collections import deque

VALUE_TYPES = Literal["int", "char", "none"]

class Variable:
    name: str
    variable_type: VALUE_TYPES

    def __init__(self, name: str, variable_type: VALUE_TYPES):
        self.name = name
        self.variable_type = variable_type


class MemoryManager:
    heap: list[Variable]
    stack: deque[VALUE_TYPES]

    def __init__(self):
        self.heap = []
        self.stack = deque()

    def push_stack(self, value: VALUE_TYPES):
        self.stack.append(value)

    def pop_stack(self) -> VALUE_TYPES:
        if not self.stack:
            raise IndexError("pop_stack called on empty stack")
        return self.stack.pop()

    def get_top_stack(self) -> VALUE_TYPES:
        if not self.stack:
            raise IndexError("Cannot get top of empty stack")
        return self.stack[-1]

    def store_var(self, name: str, value: VALUE_TYPES):
        self.heap.append(Variable(name, value))

    def get_stack_size(self) -> int:
        return len(self.stack)
