from typing import Any
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors

class BrainfuckTape:
    def __init__(
        self,
        ax,  # Add axes parameter
        length=10,
        cell_size=1.0,
        current_pos=0,
        initial_values=None,
        show_index=True,
    ):
        self.ax = ax
        self.length = length
        self.cell_size = cell_size
        self.current_pos = current_pos
        self.total_cells = 2 * length + 1
        
        # Initialize cell values
        self.cell_values = {}
        for i in range(-self.length, self.length + 1):
            self.cell_values[i] = 0
        
        # Initialize with provided values if any
        if initial_values:
            for i, val in enumerate(initial_values):
                idx = i - len(initial_values) // 2
                if -self.length <= idx <= self.length:
                    self.cell_values[idx] = val
        
        # Define special cells
        self.special_cells = {
            0: {"color": "blue", "label": "in"},
            1: {"color": "green", "label": "out"},
            2: {"color": "orange", "label": "err"},
            3: {"color": "purple", "label": "fmt"},
            4: {"color": "pink", "label": "rdy"}
        }
        
        # Store visual elements
        self.cell_patches = {}
        self.value_texts = {}
        self.index_texts = {}
        self.special_labels = {}
        self.highlight_rect = None
        
        # Create initial visualization
        self.create_tape()
    
    def create_tape(self):
        """Create the initial tape visualization"""
        # Clear the axes
        self.ax.clear()
        
        # Set black background
        self.ax.set_facecolor('black')
        self.ax.figure.set_facecolor('black')
        
        # Set up the axes with centered view
        margin = self.cell_size
        self.ax.set_xlim(-self.length * self.cell_size - margin, 
                        self.length * self.cell_size + margin)
        self.ax.set_ylim(-self.cell_size - margin, 
                        self.cell_size * 2 + margin)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        # Create all visual elements
        for i in range(-self.length, self.length + 1):
            x_pos = i * self.cell_size
            
            # Create cell rectangle
            if i in self.special_cells:
                color = self.special_cells[i]["color"]
                facecolor = mcolors.to_rgba(color, alpha=0.3)
            else:
                facecolor = mcolors.to_rgba('white', alpha=0.1)
                
            rect = Rectangle(
                (x_pos - self.cell_size/2, -self.cell_size/2), 
                self.cell_size, 
                self.cell_size,
                linewidth=2,
                edgecolor='white',
                facecolor=facecolor
            )
            self.ax.add_patch(rect)
            self.cell_patches[i] = rect
            
            # Value text (white for better contrast on black)
            value_text = self.ax.text(
                x_pos, 0, 
                str(self.cell_values[i]),
                fontsize=12,
                ha='center',
                va='center',
                color='white'
            )
            self.value_texts[i] = value_text
            
            # Index text (yellow for better contrast)
            index_text = self.ax.text(
                x_pos, self.cell_size * 0.8,
                str(i),
                fontsize=10,
                color='yellow',
                ha='center',
                va='center'
            )
            self.index_texts[i] = index_text
        
        # Create special labels
        for cell_index, info in self.special_cells.items():
            if -self.length <= cell_index <= self.length:
                x_pos = cell_index * self.cell_size
                label = self.ax.text(
                    x_pos, self.cell_size * 1.6,
                    info["label"],
                    fontsize=10,
                    color=info["color"],
                    ha='center',
                    va='center'
                )
                self.special_labels[cell_index] = label
        
        # Create initial highlight
        self.update_highlight()
    
    def update_tape(self):
        """Update the tape visualization without recreating artists"""
        # Update all value texts
        for i in range(-self.length, self.length + 1):
            self.value_texts[i].set_text(str(self.cell_values[i]))
        
        # Update highlight
        self.update_highlight()
    
    def update_highlight(self):
        """Update the current cell highlight"""
        # Remove old highlight if it exists
        if self.highlight_rect:
            self.highlight_rect.remove()
            
        # Create new highlight
        x_pos = self.current_pos * self.cell_size
        self.highlight_rect = Rectangle(
            (x_pos - self.cell_size * 0.55, -self.cell_size * 0.55),
            self.cell_size * 1.1,
            self.cell_size * 1.1,
            linewidth=4,
            edgecolor='red',
            facecolor=mcolors.to_rgba('red', alpha=0.3),
            zorder=5
        )
        self.ax.add_patch(self.highlight_rect)
    
    def set_value(self, value, pos=None):
        """Set value at current position or specified position"""
        if pos is None:
            pos = self.current_pos
        
        self.cell_values[pos] = value % 256
    
    def increment_value(self, amount=1, pos=None):
        """Increment value at current position or specified position"""
        if pos is None:
            pos = self.current_pos
        
        new_value = (self.cell_values[pos] + amount) % 256
        self.set_value(new_value, pos)
    
    def decrement_value(self, amount=1, pos=None):
        """Decrement value at current position or specified position"""
        if pos is None:
            pos = self.current_pos
        
        new_value = (self.cell_values[pos] - amount) % 256
        self.set_value(new_value, pos)
    
    def move_right(self, steps=1):
        """Move current position to the right"""
        self.current_pos = min(self.current_pos + steps, self.length)
    
    def move_left(self, steps=1):
        """Move current position to the left"""
        self.current_pos = max(self.current_pos - steps, -self.length)
    
    def jump_to_zero(self):
        """Special NJ operation: jump directly to cell 0 (stdin)"""
        self.current_pos = 0
    
    def get_current_value(self):
        """Get value at current position"""
        return self.cell_values[self.current_pos]


class MatplotlibBrainfuckAnimator:
    def __init__(self, code_data: str, input_data: str):
        self.code_data = code_data
        self.input_data = input_data
        self.animation_speed = 500  # milliseconds between frames
        
        # Set up the figure with just one axes for the tape
        self.fig, self.tape_ax = plt.subplots(1, 1, figsize=(12, 6))
        
        # Set black background for the entire figure
        self.fig.set_facecolor('black')
        self.fig.suptitle("NJ Interpreter Visualization", fontsize=16, color='white')
        
        # Initialize tape
        self.tape = BrainfuckTape(self.tape_ax)
        
        # Animation state
        self.output = ""
        self.codeptr = 0
        self.cellptr = 0
        self.cells = {i: 0 for i in range(-1000, 1001)}
        self.bracemap = self.buildbracemap(self.code_data)
        self.animation_running = True
        
    def buildbracemap(self, code: str):
        """Build bracket mapping for loop handling"""
        temp_bracestack = []
        bracemap = {}

        for position, command in enumerate(code):
            if command == "[":
                temp_bracestack.append(position)
            elif command == "]":
                if not temp_bracestack:
                    raise SyntaxError("Unmatched ']'")
                start = temp_bracestack.pop()
                bracemap[start] = position
                bracemap[position] = start

        if temp_bracestack:
            raise SyntaxError("Unmatched '['")

        return bracemap
    
    def update_input_status(self):
        """Update the input status cell"""
        new_value = 1 if self.input_data else 0
        if self.cells[4] != new_value:
            self.cells[4] = new_value
            self.tape.set_value(new_value, 4)
            return True
        return False
    
    def execute_step(self, frame):
        """Execute one step of the Brainfuck code"""
        if not self.animation_running or self.codeptr >= len(self.code_data):
            self.animation_running = False
            # Show output when animation completes
            if self.output:
                print(f"Final Output: {self.output}")
            return []
        
        # Update input status
        if self.update_input_status():
            self.tape.update_tape()
        
        command = self.code_data[self.codeptr]
        
        # Handle multi-character commands first
        if (self.codeptr + 1 < len(self.code_data) and
                command == ">" and self.code_data[self.codeptr + 1] == "!"):
            print("Hit >!")
            self.tape.jump_to_zero()
            self.cellptr = 0
            self.codeptr += 1
            self.tape.update_tape()
        
        elif command == ">":
            self.cellptr += 1
            self.tape.move_right()
            self.tape.update_tape()
        
        elif command == "<":
            self.cellptr -= 1
            self.tape.move_left()
            self.tape.update_tape()
        
        elif command == "+":
            if self.cellptr != 4:  # Protect stdin status cell
                self.cells[self.cellptr] = (self.cells[self.cellptr] + 1) % 256
                self.tape.increment_value()
                self.tape.update_tape()
        
        elif command == "-":
            if self.cellptr != 4:  # Protect stdin status cell
                self.cells[self.cellptr] = (self.cells[self.cellptr] - 1) % 256
                self.tape.decrement_value()
                self.tape.update_tape()
        
        elif command == "[" and self.cells[self.cellptr] == 0:
            self.codeptr = self.bracemap[self.codeptr]
        
        elif command == "]" and self.cells[self.cellptr] != 0:
            self.codeptr = self.bracemap[self.codeptr]
        
        elif command == ".":
            print(". hit")
            # Output from stdout cell (index 1) based on format flag (index 3)
            if self.cells[3] == 0:  # ASCII output
                char = self.cells[self.cellptr]
                self.output += chr(char) if 0 <= char <= 255 else str(char)
            else:  # Numeric output
                self.output += str(self.cells[1])
            print(f"Output is now: {self.output}")
        
        elif command == ",":
            if self.input_data:
                char_value = ord(self.input_data[0])
                self.cells[0] = char_value
                self.input_data = self.input_data[1:]
                self.tape.set_value(char_value, 0)
                self.tape.update_tape()
        
        self.codeptr += 1
        
        return []
    
    def animate(self):
        """Run the animation"""
        # Create animation
        anim = animation.FuncAnimation(
            self.fig, 
            self.execute_step,
            interval=self.animation_speed,
            blit=False,
            repeat=False,
            cache_frame_data=False,
            save_count=len(self.code_data) * 2
        )
        
        plt.tight_layout()
        
        # Save the animation
        print("Saving animation to Pipi.mp4...")
        anim.save("Pipi.mp4", writer='ffmpeg', fps=2)
        print("Animation saved!")
        
        # Also display the final output
        if self.output:
            print(f"Program Output: {self.output}")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <NJ file> [input]")
        sys.exit(1)
        
    try:
        data = Path(sys.argv[1]).read_text()
        input_data = " ".join(sys.argv[2:]).strip('"') if len(sys.argv) > 2 else ""
        
        animator = MatplotlibBrainfuckAnimator(data, input_data)
        animator.animate()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
