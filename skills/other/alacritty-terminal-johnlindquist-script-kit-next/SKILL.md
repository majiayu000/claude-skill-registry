---
name: alacritty-terminal
description: Terminal emulation library from Alacritty for VT100/xterm compatible terminal embedding
version: "0.25"
---

# alacritty-terminal

`alacritty_terminal` is the terminal emulation library extracted from the Alacritty GPU-accelerated terminal emulator. Script-kit-gpui uses version 0.25 (matching Zed's version) to provide full VT100/xterm/ANSI terminal emulation.

## Architecture Overview

```
PTY Output --> VTE Parser --> Term Grid --> Render
                   |              |
                   v              v
              Escape Seq     Cell Storage
              Processing    (scrollback)
```

The library handles:
- Escape sequence parsing via VTE (Virtual Terminal Emulator)
- Terminal grid management with scrollback
- Cell attributes (colors, bold, italic, etc.)
- Selection handling
- Terminal modes (application cursor, bracketed paste, etc.)

## Key Types

### Term<T> - The Terminal Emulator

The main terminal type, generic over an `EventListener`:

```rust
use alacritty_terminal::term::{Term, Config as TermConfig};
use alacritty_terminal::event::EventListener;

// Create a terminal with event listener
let config = TermConfig {
    scrolling_history: 10_000,  // scrollback lines
    ..TermConfig::default()
};

let term: Term<EventProxy> = Term::new(config, &size, event_proxy);
```

**Key fields:**
- `is_focused: bool` - Controls cursor appearance
- `selection: Option<Selection>` - Current text selection
- `vi_mode_cursor: ViModeCursor` - Vi mode cursor position

**Key methods:**
- `grid()` / `grid_mut()` - Access the underlying grid
- `resize(size)` - Resize terminal dimensions
- `scroll_display(Scroll)` - Scroll the viewport
- `selection_to_string()` - Get selected text
- `mode()` - Get current terminal modes (TermMode)
- `renderable_content()` - Get content optimized for rendering

### Grid<T> - 2D Cell Storage

Optimized storage for terminal content:

```rust
use alacritty_terminal::grid::{Grid, Dimensions, Scroll};
use alacritty_terminal::index::{Line, Column, Point};

let grid = term.grid();

// Access by Line (row)
let row = &grid[Line(0)];  // First visible row

// Access by Point (row + column)
let cell = &grid[Point::new(Line(0), Column(5))];

// Cursor position
let cursor_point = grid.cursor.point;
```

**Scroll enum variants:**
```rust
use alacritty_terminal::grid::Scroll;

Scroll::Delta(i32)    // Relative scroll by lines
Scroll::PageUp        // Scroll one page up
Scroll::PageDown      // Scroll one page down  
Scroll::Top           // Scroll to top of history
Scroll::Bottom        // Scroll to bottom (latest)
```

### Cell - Single Character with Attributes

```rust
use alacritty_terminal::term::cell::{Cell, Flags};
use vte::ansi::Color;

// Cell fields
let cell: &Cell = &grid[point];
cell.c          // char - the character
cell.fg         // Color - foreground color
cell.bg         // Color - background color
cell.flags      // Flags - attributes (bold, italic, etc.)
cell.hyperlink()  // Option<&Hyperlink>
```

**Cell Flags (bitflags):**
```rust
use alacritty_terminal::term::cell::Flags;

Flags::BOLD
Flags::ITALIC
Flags::UNDERLINE
Flags::DOUBLE_UNDERLINE
Flags::UNDERCURL
Flags::DOTTED_UNDERLINE
Flags::DASHED_UNDERLINE
Flags::STRIKEOUT
Flags::INVERSE         // Swap fg/bg
Flags::HIDDEN
Flags::DIM
Flags::WIDE_CHAR       // Part of wide character
Flags::WIDE_CHAR_SPACER // Spacer after wide char
```

### Index Types - Line, Column, Point

```rust
use alacritty_terminal::index::{Line, Column, Point, Direction};

// Line uses i32 (can be negative for scrollback)
let line = Line(0);           // First visible line
let scrollback = Line(-100);  // 100 lines into scrollback

// Column uses usize
let col = Column(10);

// Point combines both
let point = Point::new(Line(0), Column(5));
// Or use AlacPoint alias for disambiguation
let point = AlacPoint::new(Line(0), Column(5));

// Direction for navigation/selection
Direction::Left
Direction::Right
```

### Selection - Text Selection State

```rust
use alacritty_terminal::selection::{Selection, SelectionType};
use alacritty_terminal::index::{Point, Direction};

// Create selection
let selection = Selection::new(
    SelectionType::Simple,  // Normal character selection
    point,                  // Starting point
    Direction::Left,        // Initial direction
);

// Selection types
SelectionType::Simple    // Character-by-character
SelectionType::Semantic  // Word selection (double-click)
SelectionType::Lines     // Line selection (triple-click)
SelectionType::Block     // Block/rectangular selection

// Update selection endpoint
selection.update(new_point, Direction::Right);

// Get selection range for a term
if let Some(range) = selection.to_range(&term) {
    for point in range.iter() {
        // Process selected points
    }
}
```

### EventListener - Terminal Events

```rust
use alacritty_terminal::event::{Event, EventListener};

struct MyEventProxy { /* ... */ }

impl EventListener for MyEventProxy {
    fn send_event(&self, event: Event) {
        match event {
            Event::Bell => { /* Terminal bell */ }
            Event::Title(title) => { /* Window title change */ }
            Event::ResetTitle => { /* Reset title */ }
            Event::Exit => { /* Terminal requested exit */ }
            Event::ChildExit(code) => { /* Child process exited */ }
            Event::Wakeup => { /* New content available */ }
            Event::PtyWrite(text) => { /* Data to write to PTY */ }
            Event::MouseCursorDirty => { /* Cursor changed */ }
            Event::CursorBlinkingChange => { /* Blink state changed */ }
            Event::ClipboardStore(clipboard, data) => { /* Store to clipboard */ }
            Event::ClipboardLoad(clipboard, format) => { /* Load from clipboard */ }
            Event::ColorRequest(index, format) => { /* Query color */ }
            Event::TextAreaSizeRequest(format) => { /* Query size */ }
        }
    }
}
```

### TermMode - Terminal State Flags

```rust
use alacritty_terminal::term::TermMode;

let mode = term.mode();

// Check modes
mode.contains(TermMode::BRACKETED_PASTE)  // Wrap paste in escape sequences
mode.contains(TermMode::SHOW_CURSOR)      // Cursor visible
mode.contains(TermMode::APP_CURSOR)       // Application cursor keys
mode.contains(TermMode::APP_KEYPAD)       // Application keypad mode
mode.contains(TermMode::MOUSE_REPORT_CLICK)  // Mouse click reporting
mode.contains(TermMode::ALT_SCREEN)       // Alternate screen buffer
```

## Usage in script-kit-gpui

### Terminal Creation Pattern

```rust
// From src/terminal/alacritty.rs
use alacritty_terminal::term::{Term, Config as TermConfig};
use vte::ansi::Processor;

struct TerminalState {
    term: Term<EventProxy>,
    processor: Processor,
}

impl TerminalState {
    fn new(config: TermConfig, size: &TerminalSize, event_proxy: EventProxy) -> Self {
        Self {
            term: Term::new(config, size, event_proxy),
            processor: Processor::new(),
        }
    }
    
    // Process PTY output through VTE parser
    fn process_bytes(&mut self, bytes: &[u8]) {
        self.processor.advance(&mut self.term, bytes);
    }
}
```

### Implementing Dimensions Trait

Required for Term::new() and Term::resize():

```rust
use alacritty_terminal::grid::Dimensions;

struct TerminalSize {
    cols: usize,
    rows: usize,
}

impl Dimensions for TerminalSize {
    fn total_lines(&self) -> usize { self.rows }
    fn screen_lines(&self) -> usize { self.rows }
    fn columns(&self) -> usize { self.cols }
}
```

### Reading Grid Content for Rendering

```rust
// Iterate visible lines
for line_idx in 0..term.screen_lines() {
    let row = &grid[Line(line_idx as i32)];
    
    for col_idx in 0..term.columns() {
        let cell = &row[Column(col_idx)];
        
        // Get character
        let c = cell.c;
        
        // Resolve colors
        let fg = resolve_color(&cell.fg, theme);
        let bg = resolve_color(&cell.bg, theme);
        
        // Check attributes
        if cell.flags.contains(Flags::BOLD) { /* ... */ }
        if cell.flags.contains(Flags::WIDE_CHAR) { /* ... */ }
    }
}
```

### Color Resolution

Colors can be Named, Indexed (0-255), or Spec (direct RGB):

```rust
use vte::ansi::{Color, NamedColor, Rgb};

fn resolve_color(color: &Color, theme: &Theme) -> Rgb {
    match color {
        Color::Named(named) => match named {
            NamedColor::Foreground => theme.foreground,
            NamedColor::Background => theme.background,
            NamedColor::Black => theme.ansi[0],
            NamedColor::Red => theme.ansi[1],
            // ... etc for all 16 ANSI colors
            NamedColor::BrightBlack => theme.ansi[8],
            // ... etc for bright variants
        },
        Color::Indexed(idx) => resolve_indexed(*idx, theme),
        Color::Spec(rgb) => *rgb,
    }
}

fn resolve_indexed(idx: u8, theme: &Theme) -> Rgb {
    match idx {
        0..=15 => theme.ansi[idx as usize],
        16..=231 => {
            // 6x6x6 color cube
            let idx = idx - 16;
            let r = (idx / 36) % 6;
            let g = (idx / 6) % 6;
            let b = idx % 6;
            let to_val = |v| if v == 0 { 0 } else { 55 + v * 40 };
            Rgb { r: to_val(r), g: to_val(g), b: to_val(b) }
        }
        232..=255 => {
            // Grayscale ramp
            let gray = 8 + (idx - 232) * 10;
            Rgb { r: gray, g: gray, b: gray }
        }
    }
}
```

### Scroll Operations

```rust
use alacritty_terminal::grid::Scroll;

// Scroll by lines
term.scroll_display(Scroll::Delta(-5));  // Up 5 lines
term.scroll_display(Scroll::Delta(5));   // Down 5 lines

// Page scroll  
term.scroll_display(Scroll::PageUp);
term.scroll_display(Scroll::PageDown);

// Jump to ends
term.scroll_display(Scroll::Top);     // Top of scrollback
term.scroll_display(Scroll::Bottom);  // Latest output

// Get current scroll position
let offset = term.grid().display_offset();  // 0 = at bottom
```

### Selection Handling

```rust
use alacritty_terminal::selection::{Selection, SelectionType};
use alacritty_terminal::index::{Point, Line, Column, Direction};

// Start selection on mouse down
fn start_selection(term: &mut Term<T>, col: usize, row: usize) {
    let point = Point::new(Line(row as i32), Column(col));
    term.selection = Some(Selection::new(
        SelectionType::Simple,
        point,
        Direction::Left,
    ));
}

// Double-click for word selection
fn start_word_selection(term: &mut Term<T>, col: usize, row: usize) {
    let point = Point::new(Line(row as i32), Column(col));
    term.selection = Some(Selection::new(
        SelectionType::Semantic,  // Word boundaries
        point,
        Direction::Left,
    ));
}

// Update on mouse drag
fn update_selection(term: &mut Term<T>, col: usize, row: usize) {
    if let Some(ref mut sel) = term.selection {
        let point = Point::new(Line(row as i32), Column(col));
        sel.update(point, Direction::Right);
    }
}

// Get selected text
fn get_selection(term: &Term<T>) -> Option<String> {
    term.selection_to_string()
}

// Clear selection
term.selection = None;
```

### Bracketed Paste Mode

```rust
// Check if bracketed paste is enabled
if term.mode().contains(TermMode::BRACKETED_PASTE) {
    // Wrap pasted text in escape sequences
    let wrapped = format!("\x1b[200~{}\x1b[201~", text);
    pty.write_all(wrapped.as_bytes())?;
} else {
    pty.write_all(text.as_bytes())?;
}
```

## Anti-patterns

### Don't Mix Line Index Types

```rust
// WRONG: Using usize directly
let row = &grid[5];  // Won't compile - needs Line type

// CORRECT: Use Line wrapper
let row = &grid[Line(5)];
```

### Don't Ignore Wide Characters

```rust
// WRONG: Assuming all cells are single-width
for col in 0..width {
    render_cell(&grid[Line(row)][Column(col)]);
}

// CORRECT: Check for wide char spacers
for col in 0..width {
    let cell = &grid[Line(row)][Column(col)];
    if cell.flags.contains(Flags::WIDE_CHAR_SPACER) {
        continue;  // Skip spacer cells
    }
    let width = if cell.flags.contains(Flags::WIDE_CHAR) { 2 } else { 1 };
    render_cell(cell, width);
}
```

### Don't Forget to Process VTE

```rust
// WRONG: Writing to term directly won't parse escape sequences
term.input("Hello");  // This method doesn't exist!

// CORRECT: Use VTE processor to parse PTY output
let mut processor = Processor::new();
processor.advance(&mut term, pty_bytes);
```

### Don't Hold Lock During PTY I/O

```rust
// WRONG: Blocking I/O with lock held
let mut state = terminal_state.lock().unwrap();
let bytes = pty.read_blocking(&mut buffer)?;  // Blocks!
state.process_bytes(&bytes);

// CORRECT: Read in background, process with brief lock
// Background thread:
let bytes = pty.read_blocking(&mut buffer)?;
tx.send(bytes)?;

// Main thread:
while let Ok(bytes) = rx.try_recv() {
    let mut state = terminal_state.lock().unwrap();
    state.process_bytes(&bytes);
}  // Lock released quickly
```

### Don't Assume Positive Line Numbers

```rust
// WRONG: Assuming lines are always positive
let line = row as i32;  // May need negative for scrollback

// CORRECT: Account for display offset
let display_offset = grid.display_offset() as i32;
let line = Line(row as i32 - display_offset);
```

## Related Dependencies

- `vte` (0.13) - Virtual Terminal Emulator parser
  - `vte::ansi::Processor` - Parses escape sequences
  - `vte::ansi::Color`, `Rgb`, `NamedColor` - Color types
  - `vte::ansi::Handler` - Trait implemented by Term

## References

- [docs.rs/alacritty_terminal/0.25.0](https://docs.rs/alacritty_terminal/0.25.0)
- [Alacritty GitHub](https://github.com/alacritty/alacritty)
- [VTE crate](https://docs.rs/vte/0.13.0)
- Script-kit-gpui usage: `src/terminal/alacritty.rs`
