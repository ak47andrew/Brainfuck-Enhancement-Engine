class InternalType: pass

class StringType(InternalType):
    value: str

    def __init__(self, value: str):
        self.value = value
    
    def __str__(self) -> str:
        return self.value

class OutputTokenType(InternalType):
    value: str

    def __init__(self, value: str):
        self.value = value
    
    def __str__(self) -> str:
        return f"Output({self.value})"
