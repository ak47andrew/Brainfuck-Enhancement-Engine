from manim import * # pyright: ignore[reportWildcardImportFromLibrary]
from pathlib import Path
from sys import argv, path
from typing import Any, Optional
import manimpango
import re
import numpy as np
path.append(str(Path(__file__).parent.parent))
import bee

FONT = "JetBrainsMono Nerd Font"
def get_font():
    all_fonts = manimpango.list_fonts()
    if FONT in all_fonts:
        return FONT
    else:
        return all_fonts[0]

def get_first_and_last_line(string: str) -> tuple[str, str]:
    s = string.splitlines()
    return s[0].rstrip("\n"), s[-1].rstrip("\n")

def compress(text):
    return re.sub(r'\++', lambda match: f"+(x{len(match.group())})" if len(match.group()) > 1 else "+", text)

class TokenViz(VGroup):
    def __init__(
        self,
        token_type: Any,
        value: Any,
        args: Optional[list] = None,
        width_scale: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.token_type = token_type
        self.value = value
        self.args = args
        self.width_scale = width_scale
        
        self.create_visualization()
    
    def create_visualization(self):
        # Main token container
        main_rect = RoundedRectangle(
            corner_radius=0.1,
            height=1.2,
            width=3 * self.width_scale,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLUE_D,
            fill_opacity=0.3
        )
        
        # Token type and value
        type_text = Text("type:", font_size=20, color=YELLOW).next_to(main_rect.get_top(), DOWN, buff=0.1)
        type_value = Text(str(self.token_type), font_size=18, color=WHITE).next_to(type_text, RIGHT, buff=0.1)
        
        value_text = Text("value:", font_size=20, color=YELLOW).next_to(type_text, DOWN, buff=0.1)
        value_value = Text(str(self.value), font_size=18, color=WHITE).next_to(value_text, RIGHT, buff=0.1)
        
        # Args indicator
        args_text = Text("args:", font_size=20, color=YELLOW).next_to(value_text, DOWN, buff=0.1)
        
        # Create header group
        header_group = VGroup(type_text, type_value, value_text, value_value, args_text)
        header_group.move_to(main_rect.get_center())
        
        self.add(main_rect, header_group)
        
        # Handle args visualization
        if self.args is None:
            # None args - show "None"
            args_value = Text("None", font_size=18, color=RED).next_to(args_text, RIGHT, buff=0.1)
            self.add(args_value)
        else:
            if len(self.args) == 0:
                # Empty list - show empty brackets
                args_value = Text("[]", font_size=18, color=GREEN).next_to(args_text, RIGHT, buff=0.1)
                self.add(args_value)
            else:
                # Non-empty list - create recursive visualization
                args_value = Text(f"[{len(self.args)} items]", font_size=16, color=GREEN_C).next_to(args_text, RIGHT, buff=0.1)
                self.add(args_value)
                
                # Create args container below main token
                args_container = self.create_args_container()
                args_container.next_to(main_rect, DOWN, buff=0.3)
                self.add(args_container)
    
    def create_args_container(self) -> VGroup:
        """Create visualization for args list"""
        container = VGroup()
        
        if not self.args:
            return container
            
        # Create title for args section
        args_title = Text("Arguments:", font_size=18, color=ORANGE)
        container.add(args_title)
        
        # Create each argument token recursively
        arg_tokens = VGroup()
        for i, arg in enumerate(self.args):
            # Scale down for recursive visualization
            arg_viz = TokenViz(
                arg.token_type,
                arg.value,
                arg.args,
                width_scale=0.7
            )
            
            # Arrange in grid (2 columns)
            if i % 2 == 0:
                arg_viz.next_to(args_title, DOWN, buff=0.2)
                if i > 0:
                    arg_viz.next_to(arg_tokens[-1], DOWN, buff=0.2)
            else:
                arg_viz.next_to(arg_tokens[-1], RIGHT, buff=0.3)
            
            arg_tokens.add(arg_viz)
        
        container.add(arg_tokens)
        
        # Add bounding box around args
        args_box = SurroundingRectangle(
            container,
            corner_radius=0.1,
            stroke_color=ORANGE,
            stroke_width=1.5,
            fill_color=ORANGE,
            fill_opacity=0.1
        )
        container.add_to_back(args_box)
        
        return container

class CustomAnimation(Scene):
    def __init__(self, code: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.code = code
    
    def construct(self):
        # Step 1: plain code
        code = Code(
            code_string=self.code,
            language="python",
            tab_width=4,
            paragraph_config=dict(
                font_size=20,
                font=get_font()
            )
        ).to_edge(UP)

        self.add(code)
        self.play(Write(code))
        self.wait(BIG_DELAY)
        
        # Step 2: Pre compile
        self.lines = bee.cleanup.pre_compiling(self.code)
        lines = Paragraph(
            *[
                "[",
                *["\t" + i + "," for i in self.lines],
                "]"
            ],
            tab_width=4,
            font_size=20,
            font=get_font()
        ).to_edge(UP)
        
        self.play(ReplacementTransform(code, lines))
        self.wait(BIG_DELAY)
        
        self.play(FadeOut(lines))
        self.wait(SMALL_DELAY)
        
        mm = bee.memory_manager.MemoryManager()
        for line in self.lines:
            line_viz = Text(line, font=get_font())
            self.play(FadeIn(line_viz))
            self.wait(BIG_DELAY)
            
            self.play(line_viz.animate.to_edge(UP))
            self.wait(SMALL_DELAY)
            
            token: bee.tokenizer.Token = bee.tokenizer.tokenize(line)
            token_viz = TokenViz(token.token_type, token.value, token.args)
            
            self.play(FadeIn(token_viz))            
            self.wait(BIG_DELAY)
            
            il: list[str] = bee.intermidiate_language.convert_to_il(token)
            il_viz = Paragraph(
                *il,
                alignment="left",
                font=get_font()
            )
            il_viz.next_to(line_viz, DOWN)
            
            self.play(ReplacementTransform(token_viz, il_viz), line_viz.animate.set_color("#2e2f30"))
            self.wait(BIG_DELAY)
            
            self.scroll(il_viz)
            self.wait(SMALL_DELAY)

            self.play(FadeOut(il_viz), line_viz.animate.set_color("#FFF"))
            self.wait(SMALL_DELAY)
            
            total = []
            for ilx in il:
                ilx_viz = Text(ilx, font=get_font())
                ilx_viz.next_to(line_viz, DOWN)
                self.play(Write(ilx_viz))
                self.wait(SMALL_DELAY)
                
                bf_code = bee.interpreter.translate(mm, ilx)
                bf_code = compress(bf_code)
                bf_viz = Text(bf_code, font=get_font())
                bf_viz.next_to(ilx_viz, DOWN).shift(2 * DOWN)

                arrow = Arrow(ilx_viz.get_bottom(), bf_viz.get_top())
                self.add(arrow)
                self.wait(BIG_DELAY)

                self.play(Write(bf_viz))
                self.wait(BIG_DELAY)
                
                total.append(bf_code)
                
                self.play(
                    FadeOut(ilx_viz, bf_viz, arrow)
                )
                self.wait(BIG_DELAY)

            total_viz = Paragraph(*total, font=get_font())
            total_viz.to_edge(UP)
            self.play(Write(total_viz), line_viz.animate.set_color("#2e2f30"))

            self.scroll(total_viz)
            self.wait(SMALL_DELAY)

            self.wait(BIG_DELAY)
            self.play(FadeOut(total_viz, line_viz))
            

        self.wait(1)
    
    def scroll(self, text):
        # 2. Determine the movement distance
        # Find the center point of the first line 
        first_line_center_y = -2.5
 
        # Find the center point of the last line
        last_line_center_y = text.get_bottom()[1]
        
        # Total distance to scroll down
        scroll_distance = first_line_center_y - last_line_center_y
        
        print(scroll_distance)
        if scroll_distance < 0:
            return

        # 3. Calculate the animation duration
        # Set your desired speed in units per second.
        scroll_speed = 1.0  # units/second
        scroll_duration = scroll_distance / scroll_speed

        # 4. Perform the animations
        # Scroll down
        self.play(
            text.animate.shift(scroll_distance * UP),
            run_time=scroll_duration
        )
        
        # Pause for half a second
        self.wait(BIG_DELAY)
        
        # Scroll back up to the original position
        self.play(
            text.animate.shift(scroll_distance * DOWN),
            run_time=scroll_duration
        )

        
SMALL_DELAY = 0.2
BIG_DELAY = 0.5
if __name__ == "__main__":
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} <Bee file>")
        exit(1)
        
    config.quality = "low_quality"  # Add this line
    config.frame_rate = 30  # Reduce frame rate

    try:
        data = Path(argv[1]).read_text()
        
        scene = CustomAnimation(data)
        scene.render(False)

    except Exception as e:
        print(f"Usage: python {argv[0]} <Bee file>\n-----\nExcpetion occured: {e}")
        raise e
        exit(1)
