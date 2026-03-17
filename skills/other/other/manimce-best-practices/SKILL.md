---
name: manimce-best-practices
description: |
  Trigger when: (1) User mentions "manim" or "Manim Community" or "ManimCE", (2) Code contains `from manim import *`, (3) User runs `manim` CLI commands, (4) Working with Scene, MathTex, Create(), or ManimCE-specific classes.

  Best practices for Manim Community Edition - the community-maintained Python animation engine. Covers Scene structure, animations, LaTeX/MathTex, 3D with ThreeDScene, camera control, styling, and CLI usage.

  NOT for ManimGL/3b1b version (which uses `manimlib` imports and `manimgl` CLI).
---

## How to use

Read individual rule files for detailed explanations and code examples:

### Core Concepts
- [rules/scenes.md](rules/scenes.md) - Scene structure, construct method, and scene types
- [rules/mobjects.md](rules/mobjects.md) - Mobject types, VMobject, Groups, and positioning
- [rules/animations.md](rules/animations.md) - Animation classes, playing animations, and timing

### Creation & Transformation
- [rules/creation-animations.md](rules/creation-animations.md) - Create, Write, FadeIn, DrawBorderThenFill
- [rules/transform-animations.md](rules/transform-animations.md) - Transform, ReplacementTransform, morphing
- [rules/animation-groups.md](rules/animation-groups.md) - AnimationGroup, LaggedStart, Succession

### Text & Math
- [rules/text.md](rules/text.md) - Text mobjects, fonts, and styling
- [rules/latex.md](rules/latex.md) - MathTex, Tex, LaTeX rendering, and coloring formulas
- [rules/text-animations.md](rules/text-animations.md) - Write, AddTextLetterByLetter, TypeWithCursor

### Styling & Appearance
- [rules/colors.md](rules/colors.md) - Color constants, gradients, and color manipulation
- [rules/styling.md](rules/styling.md) - Fill, stroke, opacity, and visual properties

### Positioning & Layout
- [rules/positioning.md](rules/positioning.md) - move_to, next_to, align_to, shift methods
- [rules/grouping.md](rules/grouping.md) - VGroup, Group, arrange, and layout patterns

### Coordinate Systems & Graphing
- [rules/axes.md](rules/axes.md) - Axes, NumberPlane, coordinate systems
- [rules/graphing.md](rules/graphing.md) - Plotting functions, parametric curves
- [rules/3d.md](rules/3d.md) - ThreeDScene, 3D axes, surfaces, camera orientation

### Animation Control
- [rules/timing.md](rules/timing.md) - Rate functions, easing, run_time, lag_ratio
- [rules/updaters.md](rules/updaters.md) - Updaters, ValueTracker, dynamic animations
- [rules/camera.md](rules/camera.md) - MovingCameraScene, zoom, pan, frame manipulation

### Configuration & CLI
- [rules/cli.md](rules/cli.md) - Command-line interface, rendering options, quality flags
- [rules/config.md](rules/config.md) - Configuration system, manim.cfg, settings

### Shapes & Geometry
- [rules/shapes.md](rules/shapes.md) - Circle, Square, Rectangle, Polygon, and geometric primitives
- [rules/lines.md](rules/lines.md) - Line, Arrow, Vector, DashedLine, and connectors

## Working Examples

Complete, tested example files demonstrating common patterns:

- [examples/basic_animations.py](examples/basic_animations.py) - Shape creation, text, lagged animations, path movement
- [examples/math_visualization.py](examples/math_visualization.py) - LaTeX equations, color-coded math, derivations
- [examples/updater_patterns.py](examples/updater_patterns.py) - ValueTracker, dynamic animations, physics simulations
- [examples/graph_plotting.py](examples/graph_plotting.py) - Axes, functions, areas, Riemann sums, polar plots
- [examples/3d_visualization.py](examples/3d_visualization.py) - ThreeDScene, surfaces, 3D camera, parametric curves

## Scene Templates

Copy and modify these templates to start new projects:

- [templates/basic_scene.py](templates/basic_scene.py) - Standard 2D scene template
- [templates/camera_scene.py](templates/camera_scene.py) - MovingCameraScene with zoom/pan
- [templates/threed_scene.py](templates/threed_scene.py) - 3D scene with surfaces and camera rotation

## Quick Reference

### Basic Scene Structure
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Create mobjects
        circle = Circle()

        # Add to scene (static)
        self.add(circle)

        # Or animate
        self.play(Create(circle))

        # Wait
        self.wait(1)
```

### Render Command
```bash
# Basic render with preview
manim -pql scene.py MyScene

# Quality flags: -ql (low), -qm (medium), -qh (high), -qk (4k)
manim -pqh scene.py MyScene
```

### Key Differences from 3b1b/ManimGL

| Feature | Manim Community | 3b1b/ManimGL |
|---------|-----------------|--------------|
| Import | `from manim import *` | `from manimlib import *` |
| CLI | `manim` | `manimgl` |
| Math text | `MathTex(r"\pi")` | `Tex(R"\pi")` |
| Scene | `Scene` | `InteractiveScene` |
| Package | `manim` (PyPI) | `manimgl` (PyPI) |

### Jupyter Notebook Support

Use the `%%manim` cell magic:

```python
%%manim -qm MyScene
class MyScene(Scene):
    def construct(self):
        self.play(Create(Circle()))
```

### Common Pitfalls to Avoid

1. **Version confusion** - Ensure you're using `manim` (Community), not `manimgl` (3b1b version)
2. **Check imports** - `from manim import *` is ManimCE; `from manimlib import *` is ManimGL
3. **Outdated tutorials** - Video tutorials may be outdated; prefer official documentation
4. **manimpango issues** - If text rendering fails, check manimpango installation requirements. **Required System Libs**: `libpango1.0-dev`, `libcairo2-dev`, `libffi-dev`, `ffmpeg`.
5. **PATH issues (Windows)** - If `manim` command not found, use `python -m manim` or check PATH
6. **Directory Context** - Always `cd` into the directory containing your `.py` script before rendering to ensure media paths are resolved correctly relative to the project root.

### Installation

```bash
# Install Manim Community
pip install manim

# Check installation
manim checkhealth

# Required OS Packages (Linux)
# sudo apt-get install libpango1.0-dev libcairo2-dev libffi-dev ffmpeg
```

### Useful Commands

```bash
manim -pql scene.py Scene    # Preview low quality (development)
manim -pqh scene.py Scene    # Preview high quality
manim --format gif scene.py  # Output as GIF
manim checkhealth            # Verify installation
manim plugins -l             # List plugins
```
