import re

comment_regex = re.compile(r"#.*$", re.MULTILINE | re.UNICODE)

def pre_compiling(code: str) -> list[str]:
    """Cleanup/optimize code before passing it to a tokenizer."""
    
    # Remove comments
    code = comment_regex.sub("", code)
    
    # Remove all newlines
    code = code.replace("\n", "")

    # Split by semicolons and return to turn into tokens
    return [token for token in code.split(";") if token.strip() != ""]


def pre_output(code: str) -> str:
    """Cleanup/optimize code after converted to brainfuck."""
    while True:
        init = code
        code = code.replace("<>", "").replace("><", "").replace("+-", "").replace("-+", "")
        if init == code:
            break
    return code
