---
name: terminus-apps
description: Build terminal user interface (TUI) applications using the Terminus library for Lean 4. Use when creating games, interactive tools, or apps with keyboard/mouse input.
---

# Terminus TUI Apps

Build terminal user interface applications in Lean 4 using the Terminus library.

## Quick Start

```lean
import Terminus

structure AppState where
  count : Int := 0
  deriving Repr, Inhabited

def draw (frame : Frame) (state : AppState) : Frame := Id.run do
  let mut buf := frame.buffer.fill Cell.empty
  let msg := s!"Count: {state.count} (arrows to change, q to quit)"
  buf := buf.writeString 2 2 msg (Style.bold.withFg Color.cyan)
  { frame with buffer := buf }

def update (state : AppState) (event : Option Event) : AppState × Bool :=
  match event with
  | some (.key k) =>
    match k.code with
    | .char 'q' => (state, true)
    | .up => ({ state with count := state.count + 1 }, false)
    | .down => ({ state with count := state.count - 1 }, false)
    | _ => (state, false)
  | _ => (state, false)

def main : IO Unit := App.runApp AppState.mk draw update
```

## Architecture (MUV Pattern)

Terminus uses Model-Update-View architecture:

```
┌─────────────────────────────────────────────────────────┐
│                     Game Loop                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│  │  Events  │───→│  Update  │───→│   Draw   │───→ Screen│
│  │  poll    │    │ State→   │    │ Frame→   │           │
│  └──────────┘    │ State×   │    │ Frame    │           │
│       ↑          │ Bool     │    └──────────┘           │
│       │          └──────────┘          ↓                │
│       └────────────────────────────────┘                │
└─────────────────────────────────────────────────────────┘
```

**Key Functions:**
- `draw : Frame → State → Frame` - Render state to frame buffer
- `update : State → Option Event → State × Bool` - Handle input, return (newState, shouldQuit)

## Core Types

| Type | Purpose | Key Operations |
|------|---------|----------------|
| `Style` | Colors + modifiers | `.withFg`, `.withBg`, `.bold`, `.italic`, `.underline` |
| `Color` | Terminal colors | `.red`, `.blue`, `.cyan`, `.rgb r g b`, `.indexed n` |
| `Cell` | Styled character | `Cell.new c`, `Cell.styled c style`, `Cell.empty` |
| `Buffer` | 2D character grid | `.writeString`, `.set`, `.fill`, `.get` |
| `Rect` | Rectangle geometry | `.x`, `.y`, `.width`, `.height`, `.inner`, `.intersect` |
| `Frame` | Render context | `.buffer`, `.area`, `.render widget area` |

### Color Examples

```lean
Color.red                    -- ANSI red
Color.cyan                   -- ANSI cyan
Color.rgb 255 128 0          -- True color orange
Color.indexed 240            -- 256-palette color
Color.ansi .brightBlue       -- Bright blue
```

### Style Examples

```lean
Style.bold                           -- Bold text
Style.default.withFg Color.red       -- Red foreground
Style.bold.withFg Color.cyan         -- Bold cyan
Style.default.withBg Color.blue.withFg Color.white  -- White on blue
```

## Input Handling

### Event Polling

```lean
let event ← Events.poll  -- Non-blocking, returns Event.none if no input

match event with
| .none => ...                    -- No input this frame
| .key k => ...                   -- Keyboard event
| .mouse m => ...                 -- Mouse event
| .resize width height => ...     -- Terminal resized
```

### Key Events

| Property | Type | Description |
|----------|------|-------------|
| `k.code` | `KeyCode` | Key pressed |
| `k.modifiers.ctrl` | `Bool` | Ctrl held |
| `k.modifiers.alt` | `Bool` | Alt held |
| `k.modifiers.shift` | `Bool` | Shift held |

### Common Key Codes

```lean
.char 'a'       -- Letter 'a'
.enter          -- Enter key
.escape         -- Escape key
.space          -- Spacebar
.up, .down, .left, .right  -- Arrow keys
.backspace      -- Backspace
.tab            -- Tab
.f 1            -- F1 (through .f 12)
```

### Common Key Patterns

```lean
match k.code with
| .char 'q' => (state, true)               -- Quit
| .char c => handleChar state c            -- Any character
| .up | .char 'k' => moveUp state          -- Up or vim 'k'
| .down | .char 'j' => moveDown state      -- Down or vim 'j'
| _ => (state, false)                      -- Ignore other keys

-- Ctrl+C check
if k.isCtrlC then return (state, true)
```

### Mouse Events

```lean
match event with
| .mouse m =>
  if m.isLeftClick then
    handleClick state m.x m.y
  else if m.isScroll then
    handleScroll state m.button
  else
    (state, false)
```

## Terminal Lifecycle

### Simple: App.runApp

```lean
def main : IO Unit := App.runApp initialState draw update
```

Handles setup/teardown automatically. Good for most apps.

### Custom Loop (for timing context)

```lean
def tick (term : Terminal) (state : GameState) : IO (Terminal × GameState × Bool) := do
  let event ← Events.poll
  let (newState, shouldQuit) := update state (some event)
  let frame := Frame.new term.area
  let frame := draw frame newState
  let term := term.setBuffer frame.buffer
  let term ← term.flush frame.commands
  pure (term, newState, shouldQuit)

partial def runLoop (term : Terminal) (state : GameState) : IO Unit := do
  let (term, state, shouldQuit) ← tick term state
  if shouldQuit then return
  IO.sleep 16  -- ~60 FPS
  runLoop term state

def run : IO Unit := do
  let initialState := GameState.new
  Terminal.setup
  try
    let term ← Terminal.new
    runLoop term initialState
  finally
    Terminal.teardown
```

## Rendering

### Buffer Operations

```lean
-- Clear buffer
buf := buf.fill Cell.empty

-- Write text
buf := buf.writeString x y "Hello" Style.bold

-- Write styled text
buf := buf.writeString x y "Error" (Style.default.withFg Color.red)

-- Set single cell
buf := buf.set x y (Cell.styled '█' (Style.default.withFg Color.blue))

-- Write with bounds checking
buf := buf.writeStringBounded x y maxWidth "Long text..." style
```

### Centering Content

```lean
let area := frame.area
let contentWidth := 40
let contentHeight := 10
let startX := (area.width - contentWidth) / 2
let startY := (area.height - contentHeight) / 2
```

### Drawing Borders

```lean
def drawBorder (buf : Buffer) (x y w h : Nat) (style : Style) : Buffer := Id.run do
  let mut b := buf
  -- Corners
  b := b.writeString x y "╭" style
  b := b.writeString (x + w - 1) y "╮" style
  b := b.writeString x (y + h - 1) "╰" style
  b := b.writeString (x + w - 1) (y + h - 1) "╯" style
  -- Horizontal lines
  for i in [1 : w - 1] do
    b := b.writeString (x + i) y "─" style
    b := b.writeString (x + i) (y + h - 1) "─" style
  -- Vertical lines
  for i in [1 : h - 1] do
    b := b.writeString x (y + i) "│" style
    b := b.writeString (x + w - 1) (y + i) "│" style
  b
```

## Widgets

| Widget | Purpose | Key Properties |
|--------|---------|----------------|
| `Block` | Bordered container | `.title`, `.borderType`, `.borderStyle` |
| `Paragraph` | Multi-line text | `.lines`, `.alignment`, `.wrapMode` |
| `ListWidget` | Selectable list | `.items`, `.selected`, `.highlightStyle` |
| `Table` | Tabular data | columns, rows, header |
| `Gauge` | Progress bar | ratio, label, style |
| `Canvas` | Pixel drawing | points, lines, shapes |
| `Tabs` | Tab bar | titles, selected |
| `Tree` | Hierarchical view | nodes, expanded state |

### Widget Rendering

```lean
-- Create widget
let block := Block.rounded
  |>.withTitle "My App"
  |>.withTitleStyle Style.bold
  |>.withBorderStyle (Style.default.withFg Color.cyan)

let para := Paragraph.fromLines ["Line 1", "Line 2"]
  |>.centered
  |>.withStyle Style.bold
  |>.withBlock block

-- Render to frame
let frame := frame.render para contentArea
```

## Layout System

### Constraints

```lean
Constraint.fixed 10      -- Exactly 10 cells
Constraint.percent 50    -- 50% of available space
Constraint.min 5         -- At least 5 cells
Constraint.max 20        -- At most 20 cells
Constraint.fill          -- Take remaining space
```

### Splitting Areas

```lean
-- Vertical split
let sections := vsplit area [.fixed 3, .fill, .fixed 1]
-- sections[0] = header (3 rows)
-- sections[1] = content (remaining)
-- sections[2] = footer (1 row)

-- Horizontal split
let cols := hsplit area [.percent 30, .fill]
-- cols[0] = left sidebar (30%)
-- cols[1] = main content (70%)
```

## Common Patterns

### Game State Template

```lean
structure GameState where
  board : Array (Array Cell)
  cursor : Nat × Nat
  score : Nat
  gameOver : Bool
  paused : Bool
  rng : StdGen
  deriving Repr, Inhabited

def GameState.new (seed : UInt64) : GameState := {
  board := Array.mkArray 10 (Array.mkArray 10 Cell.empty)
  cursor := (0, 0)
  score := 0
  gameOver := false
  paused := false
  rng := mkStdGen seed.toNat
}
```

### Universal Key Handling

```lean
def update (state : GameState) (event : Option Event) : GameState × Bool :=
  match event with
  | none => (state, false)
  | some (.key k) =>
    -- Always allow quit
    if k.code == .char 'q' || k.isCtrlC then
      return (state, true)
    -- Always allow restart
    if k.code == .char 'r' then
      return (GameState.new state.seed, false)
    -- Block input if paused/game over
    if state.paused || state.gameOver then
      return (state, false)
    -- Handle game input
    handleGameInput state k
  | _ => (state, false)
```

### Overlay Dialogs

```lean
def renderOverlay (buf : Buffer) (msg : String) (area : Rect) : Buffer := Id.run do
  let w := msg.length + 4
  let h := 5
  let x := (area.width - w) / 2
  let y := (area.height - h) / 2
  let mut b := buf
  -- Semi-transparent background
  for dy in [0 : h] do
    for dx in [0 : w] do
      b := b.set (x + dx) (y + dy) (Cell.styled ' ' (Style.default.withBg Color.black))
  -- Border and message
  b := drawBorder b x y w h Style.bold
  b := b.writeString (x + 2) (y + 2) msg Style.bold
  b
```

### Animation Timing

```lean
structure AnimState where
  timer : Nat := 0
  phase : Nat := 0

def tickAnim (anim : AnimState) : AnimState :=
  if anim.timer > 0 then
    { anim with timer := anim.timer - 1 }
  else
    { anim with phase := (anim.phase + 1) % 4, timer := 5 }
```

## Complete Templates

### Game App

```lean
import Terminus

namespace MyGame

structure GameState where
  score : Nat := 0
  gameOver : Bool := false
  deriving Repr, Inhabited

def draw (frame : Frame) (state : GameState) : Frame := Id.run do
  let mut buf := frame.buffer.fill Cell.empty
  buf := buf.writeString 2 1 s!"Score: {state.score}" Style.bold
  if state.gameOver then
    buf := buf.writeString 2 3 "GAME OVER - Press R to restart"
      (Style.bold.withFg Color.red)
  { frame with buffer := buf }

def update (state : GameState) (event : Option Event) : GameState × Bool :=
  match event with
  | some (.key k) =>
    match k.code with
    | .char 'q' => (state, true)
    | .char 'r' => (GameState.mk, false)
    | .space => ({ state with score := state.score + 1 }, false)
    | _ => (state, false)
  | _ => (state, false)

end MyGame

def main : IO Unit := App.runApp MyGame.GameState.mk MyGame.draw MyGame.update
```

### CLI + TUI Hybrid

```lean
import Terminus
import Parlance

namespace MyTool

-- CLI mode (default)
def runCli (args : List String) : IO Unit := do
  IO.println "CLI mode - use 'mytool tui' for interactive"

-- TUI mode
def runTui : IO Unit := do
  App.runApp initialState draw update

def main (args : List String) : IO Unit := do
  if args.contains "tui" then
    runTui
  else
    runCli args

end MyTool
```

## Projects Using Terminus

Reference implementations in this workspace:
- `apps/blockfall` - Tetris clone with animations
- `apps/minefield` - Minesweeper with flood-fill
- `apps/solitaire` - Card game with undo
- `apps/tracker` - Issue tracker CLI with TUI mode
- `apps/lighthouse` - File browser
- `apps/enchiridion` - Documentation viewer

## lakefile.lean Setup

```lean
require terminus from git "https://github.com/nathanial/terminus" @ "v0.0.1"

@[default_target]
lean_lib MyApp

lean_exe myapp where
  root := `Main
```
