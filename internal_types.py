from typing import Any


class InternalType:
    value: Any

    def __init__(self, value: Any) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)

class StringType(InternalType):
    value: str

    def __init__(self, value: str):
        self.value = value

class IntegerType(InternalType):
    value: int

    def __init__(self, value: int):
        self.value = value

class FloatType(InternalType):
    value: float

    def __init__(self, value: float):
        self.value = value

class BooleanType(InternalType):
    value: bool

    def __init__(self, value: bool):
        self.value = value

    def __str__(self) -> str:
        return super().__str__().lower()

class OutputTokenType(InternalType):
    value: str

    def __init__(self, value: str):
        self.value = value
    
    def __str__(self) -> str:
        return f"Output({self.value})"
