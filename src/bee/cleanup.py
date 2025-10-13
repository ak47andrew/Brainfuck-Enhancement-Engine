# comment_regex = re.compile(r"#.*$", re.MULTILINE | re.UNICODE)  # FIXME: have an issue with `#` inside of string literals. Readd with fix later


def pre_compiling(code: str) -> list[str]:
    """Cleanup/optimize code before passing it to a tokenizer."""
    # TODO: When I'll have loops and if statements - add lines together

    # Remove comments
    # code = comment_regex.sub("", code)
    code_lines: list[str] = code.splitlines()

    return [line.removesuffix(";") for line in code_lines if line != ""]


def pre_output(code: str) -> str:
    """Cleanup/optimize code after converted to brainfuck."""
    while True:
        init = code
        code = code.replace("<>", "").replace("><", "").replace("+-", "").replace("-+", "")
        if init == code:
            break
    return code
