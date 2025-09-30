#!/usr/bin/python
#
# Custom Brainfuck Interpreter (Modified per DEVLOG-0002)
# Based on original by Sebastian Kaspari
# Modifications by: Reborn
#
# Usage: ./brainfuck.py [FILE]

import sys
import threading
import queue
import time

try:
    from msvcrt import getch
except ImportError:
    # Fallback for Unix-like systems
    def getch():
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class InputThread(threading.Thread):
    def __init__(self, input_queue):
        super().__init__()
        self.input_queue = input_queue
        self.daemon = True
        self.running = True
        self.is_ctrl_c = False

    def run(self):
        while self.running:
            try:
                # Get character (blocking)
                char = getch()
                if char in [b'\x03', b'\x1a']:
                    self.running = False
                    self.is_ctrl_c = True
                if char:
                    self.input_queue.put(ord(char))
                # Small delay to prevent CPU spinning
                time.sleep(0.01)
            except:
                break

    def stop(self):
        self.running = False


class NJBrainfuckInterpreter:
    def __init__(self):
        self.cells = {}
        for i in range(-1000, 1001):  # Pre-initialize a range of cells
            self.cells[i] = 0

        self.input_queue = queue.Queue()
        self.input_thread = InputThread(self.input_queue)
        self.codeptr = 0
        self.cellptr = 0
        self.bracemap = {}

        # Initialize special cells
        self.cells[3] = 0  # Stdout format flag (0=ASCII, 1=number)
        self.update_input_status()

        # Start input thread
        self.input_thread.start()

    def update_input_status(self):
        """Update stdin readiness flag (cell 4)"""
        self.cells[4] = 1 if self.input_queue.empty() else 0

    def execute(self, filename):
        try:
            with open(filename, "r") as f:
                code = f.read()
            return self.evaluate(code)
        except Exception as e:
            print(f"Error: {e}")
            return 1
        finally:
            self.input_thread.stop()

    def evaluate(self, code):
        code = self.cleanup(list(code))
        self.bracemap = self.buildbracemap(code)

        while self.codeptr < len(code):
            self.update_input_status()

            if not self.input_thread.running:
                print("Input thread terminated, shutting down")
                if self.input_thread.is_ctrl_c:
                    print("Process was terminated via Ctrl + C or Ctrl + Z")
                    self.cells[2] = 130
                break

            command = code[self.codeptr]
            # print(len(self.input_queue.queue))
            # print(self.cells[0])
            # print(self.cells[1])
            # print(self.cells[4])
            # print()
            # time.sleep(0.01)

            # Handle multi-character commands first
            if (self.codeptr + 1 < len(code) and
                    command == ">" and code[self.codeptr + 1] == "!"):
                self.cellptr = 0  # Jump to stdin cell
                self.codeptr += 1  # Skip the '!' character

            # Standard commands
            elif command == ">":
                self.cellptr += 1
                # Extend cells dictionary if needed
                if self.cellptr not in self.cells:
                    self.cells[self.cellptr] = 0

            elif command == "<":
                self.cellptr -= 1
                # Extend cells dictionary if needed
                if self.cellptr not in self.cells:
                    self.cells[self.cellptr] = 0

            elif command == "+":
                if self.cellptr != 4:  # Protect stdin and stdin status cells
                    self.cells[self.cellptr] = (self.cells[self.cellptr] + 1) % 256

            elif command == "-":
                if self.cellptr != 4:  # Protect stdin and stdin status cells
                    self.cells[self.cellptr] = (self.cells[self.cellptr] - 1) % 256

            elif command == "[" and self.cells[self.cellptr] == 0:
                self.codeptr = self.bracemap[self.codeptr]

            elif command == "]" and self.cells[self.cellptr] != 0:
                self.codeptr = self.bracemap[self.codeptr]

            elif command == ".":
                # Output from stdout cell (index 1) based on format flag (index 3)
                if self.cells[3] == 0:  # ASCII output
                    char = self.cells[1]
                    if 0 <= char <= 255:
                        sys.stdout.write(chr(char))
                    else:
                        sys.stdout.write(str(char))
                else:  # Numeric output
                    sys.stdout.write(str(self.cells[1]))
                sys.stdout.flush()

            elif command == ",":
                # Read into stdin cell (index 0) from input queue
                try:
                    # Non-blocking get from queue
                    char_value = self.input_queue.get_nowait()
                    self.cells[0] = char_value
                except queue.Empty:
                    # No input available
                    self.cells[0] = 0

                self.update_input_status()

            self.codeptr += 1

        # Return termination code from cell 2
        return self.cells[2]

    def cleanup(self, code):
        # Keep only valid commands including '!' for the special jump
        cleaned = []
        i = 0
        while i < len(code):
            if code[i] in ['.', ',', '[', ']', '<', '>', '+', '-', '!', "#"]:
                # Handle the special case of ">!" as a single unit
                if (i + 1 < len(code) and
                        code[i] == ">" and code[i + 1] == "!"):
                    cleaned.append(">")
                    cleaned.append("!")
                    i += 1  # Skip the next character since we handled it
                else:
                    cleaned.append(code[i])
            i += 1
        return ''.join(cleaned)

    def buildbracemap(self, code):
        temp_bracestack, bracemap = [], {}

        for position, command in enumerate(code):
            if command == "[":
                temp_bracestack.append(position)
            if command == "]":
                if not temp_bracestack:
                    raise SyntaxError("Unmatched ']'")
                start = temp_bracestack.pop()
                bracemap[start] = position
                bracemap[position] = start

        if temp_bracestack:
            raise SyntaxError("Unmatched '['")

        return bracemap


def main():
    if len(sys.argv) == 2:
        interpreter = NJBrainfuckInterpreter()
        exit_code = interpreter.execute(sys.argv[1])
        sys.exit(exit_code)
    else:
        print("Usage:", sys.argv[0], "filename")
        sys.exit(1)


if __name__ == "__main__":
    main()