def pre_compiling(code: str) -> list[str]:
    """Cleanup/optimize code before passing it to a tokenizer."""
    # TODO: When I'll have loops and if statements - add lines together
    # TODO: rewrite this to work with multilines and stuff like that. For now it's just shit :(

    # Remove comments
    # code = comment_regex.sub("", code)
    code_lines: list[str] = code.splitlines()

    return [line.removesuffix(";") for line in code_lines if line != ""]
