from typing import Any, Self
from abc import ABC, abstractmethod
from memory_manager import MemoryManager
import struct


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
        n = self.value
        if n == 0:
            return [0, 0]  # Special case: zero

        # Determine sign and work with absolute value
        sign = 1 if n < 0 else 0
        n_abs = abs(n)

        # Convert to base-256 (little-endian)
        bytes_list = []
        while n_abs > 0:
            bytes_list.append(n_abs % 256)
            n_abs //= 256

        # Return [sign, length, byte0, byte1, ...]
        return [sign, len(bytes_list)] + bytes_list

    @classmethod
    def get_value(cls, mm: MemoryManager) -> Self:
        length = mm.get_value(mm.pointer + 1)
        cells = [mm.get_value(mm.pointer + ind) for ind in range(length + 2)]

        if cells[0] == 0 and cells[1] == 0:
            p = 0  # Special case: zero
        else:
            sign = -1 if cells[0] == 1 else 1
            length = cells[1]

            # Reconstruct the number from base-256 bytes
            result = 0
            for i, byte in enumerate(cells[2:2 + length]):
                result += byte * (256 ** i)

            p = sign * result

        return cls(p)

class FloatType(InternalType):
    value: float

    def __init__(self, value: float):
        super().__init__(value)

    def get_memory_layout(self) -> list:
        # Pack float into 4 bytes using IEEE 754
        packed = struct.pack('>f', self.value)

        # Convert bytes to integer values
        return list(packed)

    @classmethod
    def get_value(cls, mm: MemoryManager) -> Self:
        cells = [mm.get_value(mm.pointer + ind) for ind in range(4)]

        # Convert integer values back to bytes
        byte_data = bytes(cells)

        # Unpack bytes to float
        return cls(struct.unpack('>f', byte_data)[0])

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
