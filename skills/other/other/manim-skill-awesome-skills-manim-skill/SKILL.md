---
name: manim
description: This skill should be used when the user asks to "create an animation", "make a manim video", "animate this concept", "visualize this process", "create a GIF for my blog", "plot a graph", "animate a value", or mentions "manim", "mathematical animation", "code animation", "process visualization", "technical animation", "3D scene", "camera animation", "ValueTracker", "number animation". Provides ManimCE (Community Edition) syntax, patterns, and best practices for creating programmatic animations.
version: 1.5.0
---

# Manim Animation Skill

Create precise, programmatic animations for technical blogs, educational content, and concept visualization using Manim Community Edition (ManimCE).

**Test animations:** https://docs.manim.community/en/stable/examples.html

## Installation (v0.19+)

```bash
# Recommended: uv (no ffmpeg needed since v0.19!)
uv venv && source .venv/bin/activate
uv pip install manim

# Or pip (still works)
pip install manim

# Check installation
manim checkhealth
```

**Note:** v0.19+ uses pyav internally, eliminating the external ffmpeg dependency.

**Virtual environment tip:** If not activated, use `uv run manim ...` instead of `manim`.

### Windows Quick Start (PowerShell)

```powershell
# Install uv (if needed)
python -m pip install --user uv

# Verify uv is on PATH
where uv

# One-off run without creating a venv
uv run --with manim manim checkhealth
```

If `uv` is not found, restart the terminal and run `where uv` again.

## ManimCE vs ManimGL

| Aspect | ManimCE (Recommended) | ManimGL |
|--------|----------------------|---------|
| Package | `pip install manim` | `pip install manimgl` |
| Stability | Stable, well-documented | Experimental, breaking changes |
| Jupyter | Supported (`%%manim` magic) | Limited |
| ffmpeg | Not required (v0.19+) | Required |
| Caching | Supported | Not supported |

**Always use ManimCE** unless reproducing exact 3Blue1Brown videos.

## Core Concepts

### Three Building Blocks

1. **Mobjects** - Mathematical objects displayed on screen (Circle, Text, Code, etc.)
2. **Scenes** - Canvas containing animations, subclass of `Scene`
3. **Animations** - Transformations applied to Mobjects (Create, Write, FadeIn, etc.)

### Basic Scene Structure

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Create mobjects
        circle = Circle(color=BLUE)

        # Animate
        self.play(Create(circle))
        self.wait(1)
```

## Common Mobjects

### Text and Labels

```python
# Plain text
text = Text("Hello", font_size=48)

# With color portions
text = Text("Hello World", t2c={"Hello": RED, "World": BLUE})

# Positioned
label = Text("Label").next_to(circle, UP)
```

### Code Blocks (v0.19+)

```python
# IMPORTANT: Use code_string, NOT code parameter
code = Code(
    code_string="""function example() {
  return 42;
}""",
    language="javascript",       # Specify explicitly (auto-detect is flaky)
    background="rectangle",      # or "window"
    formatter_style="monokai",   # pygments style
)

# Get available styles
styles = Code.get_styles_list()  # ['monokai', 'vim', 'native', ...]
```

### LaTeX

```python
# Simple LaTeX
tex = Tex(r"\LaTeX", font_size=144)

# Math mode (auto-wrapped in $...$)
math = MathTex(r"E = mc^2")

# Multi-line equation
equation = MathTex(r"f(x) &= x^2 \\ g(x) &= x^3")
```

### TeX-Free Numeric Labels (Windows-Safe)

If LaTeX is not installed, avoid `Tex`, `MathTex`, and number mobjects that may trigger TeX rendering (`Integer`, `DecimalNumber`, `Variable` with math labels).

Use plain text labels instead:

```python
value = 42
label = Text(str(value), font_size=24)
```

### Shapes

```python
circle = Circle(radius=1, color=BLUE, fill_opacity=0.5)
square = Square(side_length=2, color=RED)
rect = Rectangle(width=3, height=1.5)
arrow = Arrow(LEFT, RIGHT)
line = Line(ORIGIN, UP * 2)
```

### Graphs and Axes

```python
axes = Axes(
    x_range=[-3, 3, 1],
    y_range=[-5, 5, 1],
    axis_config={"color": BLUE}
)
graph = axes.plot(lambda x: x**2, color=WHITE)
label = axes.get_graph_label(graph, label="x^2")
```

## Animation Patterns

### Basic Animations

```python
# Create vs Write:
# - Create: Simple stroke drawing (use for shapes)
# - Write: Hand-writing effect with border-then-fill (use for text)
self.play(Create(circle))       # For shapes
self.play(Write(text))          # For Text/Tex/MathTex

self.play(FadeIn(mob))          # Fade in
self.play(FadeIn(mob, shift=UP))  # Fade in with direction
self.play(FadeOut(mob))         # Fade out
self.play(GrowFromCenter(mob))  # Grow from center
self.wait(1)                    # Pause 1 second
```

### The .animate Syntax

Prepend `.animate` to any method to animate the change:

```python
# Animate movement
self.play(circle.animate.shift(RIGHT * 2))

# Animate scaling
self.play(square.animate.scale(2))

# Animate color change
self.play(text.animate.set_color(RED))

# Chain animations
self.play(mob.animate.shift(UP).scale(0.5).set_color(BLUE))
```

### Transform Animations

```python
# Morph one shape into another
self.play(Transform(square, circle))

# Replace (keeps reference to new object)
self.play(ReplacementTransform(old, new))
```

### Simultaneous Animations

```python
# Multiple objects at once
self.play(
    Create(circle),
    Write(text),
    FadeIn(arrow),
    run_time=2
)
```

## Positioning

### Direction Constants

```python
UP, DOWN, LEFT, RIGHT, ORIGIN
UL, UR, DL, DR  # Corners (Up-Left, etc.)
```

### Positioning Methods

```python
# Absolute position
mob.move_to(ORIGIN)
mob.move_to(LEFT * 3 + UP * 2)

# Relative to another object
label.next_to(circle, UP, buff=0.5)

# Shift from current position
mob.shift(RIGHT * 2)

# Align edges
mob.align_to(other, UP)  # Align top edges
```

### Grouping

```python
group = VGroup(circle, square, text)
group.arrange(RIGHT, buff=0.5)           # Horizontal layout
group.arrange(DOWN, aligned_edge=LEFT)   # Vertical, left-aligned

# Grid layout
boxes = VGroup(*[Square() for _ in range(6)])
boxes.arrange_in_grid(rows=2, cols=3, buff=0.5)
```

## Colors

```python
# Named colors
RED, BLUE, GREEN, YELLOW, WHITE, BLACK, GRAY
ORANGE, PINK, PURPLE, TEAL, GOLD

# Shades (A=lightest, E=darkest)
BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E
GRAY_A, GRAY_B, GRAY_C, GRAY_D, GRAY_E

# Hex colors
color = "#61DAFB"

# Color modules (v0.19+)
from manim.utils.color import X11, XKCD
beige = X11.BEIGE      # '#F5F5DC'
mango = XKCD.MANGO     # '#FFA62B'
```

## Rendering Commands

```bash
# One-off render with uv (no manual venv activation)
uv run --with manim manim -pql scene.py SceneName

# Preview with low quality (fast)
manim -pql scene.py SceneName

# High quality render
manim -pqh scene.py SceneName

# Export as GIF (good for blogs)
manim -qm --format=gif scene.py SceneName

# Quality flags
# -ql  480p15 (preview)
# -qm  720p30 (medium)
# -qh  1080p60 (high)
# -qk  4K60 (production)

# Debugging options
manim -pql -s scene.py SceneName     # Output last frame only (fastest)
manim -pql -n 1,3 scene.py SceneName # Render animations 1-3 only
manim --dry_run scene.py SceneName   # No output, just check errors
```

### Jupyter Notebook

Use the `%%manim` magic command:

```python
%%manim -qm -v WARNING MyScene

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

See `references/advanced.md` for full Jupyter usage details.

## Best Practices

### Keep Animations Focused

For blog posts, create short, focused animations (5-15 seconds) that illustrate one concept. Let surrounding text provide context.

### Use Helper Functions

```python
def create_node(label, color):
    """Reusable node factory."""
    rect = RoundedRectangle(width=2, height=1, color=color, fill_opacity=0.3)
    text = Text(label, font_size=20)
    text.move_to(rect)
    return VGroup(rect, text)
```

### Performance Tips

- Use `-ql` during development, render high quality only when ready
- Prefer `Text` over `Tex` when LaTeX isn't needed (faster)
- Use caching: Manim automatically caches partial renders
- Use `-s` to quickly preview the final frame

### Scene Organization

```python
class MyAnimation(Scene):
    def construct(self):
        self.show_intro()
        self.show_main_concept()
        self.show_conclusion()

    def show_intro(self):
        # Intro animations
        pass
```

## Additional Resources

### Reference Files

For detailed syntax and patterns:
- **`references/mobjects.md`** - Complete Mobject reference (shapes, text, code, graphs, 3D primitives, numbers, positioning)
- **`references/animations.md`** - All animation types, Transform vs ReplacementTransform, timing control
- **`references/advanced.md`** - Camera, 3D, ValueTracker, updaters, config, common mistakes, plugins
- **`references/blog-patterns.md`** - Common patterns for technical blog animations

### Example Files

Working examples in `examples/`:
- **`examples/basic_scene.py`** - Minimal scene template
- **`examples/flowchart.py`** - Animated flowchart pattern
- **`examples/state_diagram.py`** - State transition visualization
- **`examples/quicksort.py`** - Quicksort bar animation (algorithm visualization template)

### External Resources

- **Official Docs:** https://docs.manim.community/en/stable/
- **Example Gallery:** https://docs.manim.community/en/stable/examples.html
- **GitHub:** https://github.com/ManimCommunity/manim
- **Discord:** Community support and #beginner-resources channel
