---
name: pyxel-patterns
description: Pyxel retro game engine patterns - pixel art, game loops, sprite/tilemap, MML audio, resource management, and web deployment
---

# Pyxel Patterns

Patterns and best practices for building retro-style games with [Pyxel](https://github.com/kitao/pyxel) — a Python game engine with deliberate retro constraints.

## When to Use

- Building retro/pixel art games with Python
- Prototyping game mechanics quickly
- Creating browser-playable games (WASM export)
- Teaching game development fundamentals

## Retro Constraints

Pyxel enforces retro limitations by design:

| Constraint | Limit |
|-----------|-------|
| Colors | 16-color palette (customizable) |
| Screen | Default 256x256 (configurable) |
| Image banks | 3 banks (0-2), 256x256 each |
| Tilemaps | 8 maps, 256x256 tiles each |
| Sound channels | 4 simultaneous |
| Sound/Music | 64 user-definable sounds, 8 musics |
| Input | Keyboard + Mouse + Gamepad (up to 2) |

These constraints are features, not bugs. They force creative solutions and authentic retro aesthetics.

## Game Loop Pattern

```python
import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="My Game")
        # Load resources
        pyxel.load("assets.pyxres")
        # Initialize game state
        self.player_x = 72
        self.player_y = 56
        self.score = 0
        # Start game loop
        pyxel.run(self.update, self.draw)

    def update(self):
        """Called every frame - handle input and game logic"""
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Movement
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)

    def draw(self):
        """Called every frame - render everything"""
        pyxel.cls(0)  # Clear screen (color 0)
        pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 0)
        pyxel.text(5, 4, f"SCORE: {self.score}", 7)

App()
```

## Input Handling

```python
# Button states
pyxel.btn(key)      # True while held
pyxel.btnp(key)     # True on press (with optional repeat)
pyxel.btnr(key)     # True on release
pyxel.btnv(key)     # Analog value (gamepad)

# Mouse
pyxel.mouse_x       # Current X position
pyxel.mouse_y       # Current Y position
pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

# Common pattern: 8-directional movement
dx = pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT)
dy = pyxel.btn(pyxel.KEY_DOWN) - pyxel.btn(pyxel.KEY_UP)
```

## Drawing API

```python
# Primitives
pyxel.cls(col)                    # Clear screen
pyxel.pset(x, y, col)            # Pixel
pyxel.line(x1, y1, x2, y2, col)  # Line
pyxel.rect(x, y, w, h, col)      # Filled rectangle
pyxel.rectb(x, y, w, h, col)     # Rectangle border
pyxel.circ(x, y, r, col)         # Filled circle
pyxel.circb(x, y, r, col)        # Circle border

# Sprites (from image bank)
pyxel.blt(x, y, img, u, v, w, h, colkey)
# img: image bank (0-2)
# u, v: source position in bank
# w, h: size (negative = flip)
# colkey: transparent color

# Tilemap
pyxel.bltm(x, y, tm, u, v, w, h, colkey)

# Text
pyxel.text(x, y, string, col)
```

## Sprite Animation

```python
class AnimatedSprite:
    def __init__(self, frames, speed=5):
        self.frames = frames  # [(u, v, w, h), ...]
        self.speed = speed
        self.frame_index = 0
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= self.speed:
            self.counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw(self, x, y, img=0, colkey=0):
        u, v, w, h = self.frames[self.frame_index]
        pyxel.blt(x, y, img, u, v, w, h, colkey)
```

## Collision Detection

```python
def aabb_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    """Axis-aligned bounding box collision"""
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)

def point_in_rect(px, py, rx, ry, rw, rh):
    """Point inside rectangle"""
    return rx <= px < rx + rw and ry <= py < ry + rh
```

## Sound & Music (MML)

```python
# Define sounds using MML (Music Macro Language)
pyxel.sounds[0].set(
    "e2e2c2g1 g1g1c2e2 d2d2d2g2 e2e2e2c2",  # notes
    "p",                                         # tones: t(riangle) s(quare) p(ulse) n(oise)
    "6",                                         # volumes (0-7)
    "nnnf",                                      # effects: n(one) s(lide) v(ibrato) f(adeout)
    25                                           # speed
)

# Play sound
pyxel.play(ch, snd)     # ch: channel (0-3), snd: sound index
pyxel.playm(msc)        # Play music (0-7)
pyxel.stop(ch)          # Stop channel (-1 for all)
```

## Resource Management

```python
# Create resources with Pyxel Editor
# Terminal: pyxel edit assets.pyxres

# Load in code
pyxel.load("assets.pyxres")

# Or create programmatically
pyxel.images[0].load(0, 0, "sprite_sheet.png")

# Resource file contains:
# - Image banks (sprites, backgrounds)
# - Tilemaps (level layouts)
# - Sounds (SFX)
# - Music (BGM)
```

## Scene Management

```python
class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current = None

    def add(self, name, scene):
        self.scenes[name] = scene

    def switch(self, name):
        self.current = self.scenes[name]
        if hasattr(self.current, 'enter'):
            self.current.enter()

    def update(self):
        if self.current:
            self.current.update()

    def draw(self):
        if self.current:
            self.current.draw()

# Usage
class TitleScene:
    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            scene_mgr.switch("game")

    def draw(self):
        pyxel.cls(0)
        pyxel.text(50, 50, "PRESS ENTER", pyxel.frame_count % 16)
```

## Packaging & Distribution

```bash
# Package as standalone executable
pyxel package APP_DIR STARTUP_SCRIPT

# Convert to executable
pyxel app2exe APP.pyxapp

# Convert to HTML (browser-playable via WASM)
pyxel app2html APP.pyxapp

# The HTML output uses Pyodide/Emscripten WASM
# Works in modern browsers without Python installed
```

## Performance Tips

- Keep `update()` and `draw()` fast (target 30fps default)
- Use tilemaps for static backgrounds instead of drawing each tile
- Pool objects (bullets, particles) instead of creating/destroying
- Minimize Python object creation in the game loop
- Use `pyxel.frame_count` for timing instead of tracking your own counter
- Pre-calculate values that don't change per frame

## Common Game Patterns

### Particle System
```python
class Particle:
    __slots__ = ['x', 'y', 'vx', 'vy', 'life', 'col']

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = pyxel.rndf(-1, 1)
        self.vy = pyxel.rndf(-2, 0)
        self.life = pyxel.rndi(10, 30)
        self.col = pyxel.rndi(8, 10)

particles = []
# In update: spawn, move, remove dead
# In draw: pyxel.pset(p.x, p.y, p.col)
```

### Camera Scrolling
```python
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def follow(self, target_x, target_y):
        self.x = target_x - pyxel.width // 2
        self.y = target_y - pyxel.height // 2

# In draw: offset all positions by -camera.x, -camera.y
```
