import pathlib
from sys import argv

if __name__ == "__main__":
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} <NJ file>")
        exit(1)

    try:
        data = pathlib.Path(argv[1]).read_text()
    except Exception as e:
        print(f"Usage: python {argv[0]} <NJ file>\n-----\nExcpetion occured: {e}")
        exit(1)
