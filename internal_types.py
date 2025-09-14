from typing import Any, Self
from abc import ABC, abstractmethod
from memory_manager import MemoryManager


class InternalType(ABC):
    value: Any

    def __init__(self, value: Any) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)

    @abstractmethod
    def get_memory_layout(self) -> list: ... # Implement this method

    @classmethod
    @abstractmethod
    def get_value(cls, mm: MemoryManager) -> Self:
        """
        Caution! Before calling this method pointer of MemoryManager should be set to the first address variable is
        stored in memory
        """
        ...

class StringType(InternalType):
    value: str

    def __init__(self, value: str):
        super().__init__(value)
    
    def get_memory_layout(self) -> list:
        return [len(self.value)] + [ord(c) for c in self.value]

    @classmethod
    def get_value(cls, mm: MemoryManager) -> Self:
        str_length = mm.get_value()
        string = "".join([chr(mm.get_value(mm.pointer + i)) for i in range(1, str_length + 1)])
        return cls(string)

class IntegerType(InternalType):
    value: int

    def __init__(self, value: int):
        super().__init__(value)
    
    def get_memory_layout(self) -> list:
        if self.value < 0 or self.value > 255:
            raise ValueError("Values out of 0-255 range can't be set as a variable. This will be fixed in the next version")  # TODO
        return [self.value]

    @classmethod
    def get_value(cls, mm: MemoryManager) -> Self:
        return cls(mm.get_value())

class FloatType(InternalType):
    value: float

    def __init__(self, value: float):
        super().__init__(value)

    def get_memory_layout(self) -> list:
        raise ValueError("Floats can't yet be stored in memory. This will be fixed in a newer versions")  # TODO

    @classmethod
    def get_value(cls, mm: MemoryManager) -> Self:
        raise ValueError("Floats can't yet be stored in memory. This will be fixed in a new version")

class BooleanType(InternalType):
    value: bool

    def __init__(self, value: bool):
        super().__init__(value)

    def __str__(self) -> str:
        return super().__str__().lower()
    
    def get_memory_layout(self) -> list:
        return [int(self.value)]

    @classmethod
    def get_value(cls, mm: MemoryManager) -> Self:
        return cls(bool(mm.get_value()))

class OutputTokenType(InternalType):
    value: str

    def __init__(self, value: str):
        super().__init__(value)
    
    def __str__(self) -> str:
        return f"Output({self.value})"
    
    def get_memory_layout(self) -> list:
        raise ValueError("If you want to store OutputTokenType, something went horribly wrong")

    @classmethod
    def get_value(cls, mm: MemoryManager) -> Self:
        raise ValueError("If you want to load OutputTokenType, something went horribly wrong")
