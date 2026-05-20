---
name: script-kit-terminal
description: Terminal integration for Script Kit GPUI using Alacritty terminal emulator and portable-pty. Use when working with terminal/, term_prompt.rs, PTY handling, terminal rendering, escape sequences, selection, scrollback, or ANSI colors.
---

# Script Kit Terminal Integration

Embedded terminal functionality using Alacritty's terminal emulator backend and portable-pty for cross-platform PTY support. Enables `await term("command")` in Script Kit scripts.

## Architecture

```
PTY Output -> VTE Parser -> Terminal Grid -> GPUI Render
     ^                           |
     |___ keyboard input ________|
```

### Core Components

| Module | Purpose |
|--------|---------|
| `terminal/mod.rs` | Module exports, `TerminalEvent` enum |
| `terminal/pty.rs` | Cross-platform PTY via portable-pty |
| `terminal/alacritty.rs` | Alacritty term wrapper, escape parsing |
| `terminal/theme_adapter.rs` | Theme-to-terminal color mapping |
| `term_prompt.rs` | GPUI component, keyboard/mouse handling |

### Integration Layer (App Shell)

| Module | Purpose |
|--------|---------|
| `render_prompts/term.rs` | Renders terminal WITH app shell (header/footer) |
| `prompt_handler.rs` | Creates `TermPrompt` entity from SDK messages |
| `app_execute.rs` | Creates `TermPrompt` for quick terminal commands |
| `window_resize.rs` | Layout constants: `MAX_HEIGHT`, `FOOTER_HEIGHT` |

### Height Calculation (CRITICAL)

Terminal content height must account for the app shell footer:

```rust
use crate::window_resize::layout::{MAX_HEIGHT, FOOTER_HEIGHT};

// WRONG - terminal bottom will be cut off by footer
let term_height = MAX_HEIGHT; // 700px

// CORRECT - subtract footer height
let term_height = MAX_HEIGHT - px(FOOTER_HEIGHT); // 700px - 30px = 670px
```

The `TermPrompt::with_height()` receives `content_height` which it uses to calculate terminal rows via `resize_if_needed()`. If this doesn't account for the footer, the bottom ~2 rows are hidden.

## TerminalHandle (alacritty.rs)

Main terminal emulator wrapper. Thread-safe via `Arc<Mutex<>>`.

### Creation

```rust
// Default shell
let term = TerminalHandle::new(cols, rows)?;

// Specific command (sends to interactive shell)
let term = TerminalHandle::with_command("htop", 80, 24)?;

// Custom scrollback
let term = TerminalHandle::with_scrollback(80, 24, 10_000)?;
```

### Processing Loop

```rust
// Non-blocking - reads from background thread channel
let (had_output, events) = terminal.process();

// had_output: true if grid content changed
// events: Vec<TerminalEvent> (Bell, Title, Exit)
```

### Key Methods

| Method | Purpose |
|--------|---------|
| `input(&[u8])` | Send keyboard bytes to PTY |
| `resize(cols, rows)` | Resize terminal and PTY |
| `content()` | Get `TerminalContent` snapshot for rendering |
| `scroll(delta)` | Scroll display (positive=up into history) |
| `scroll_to_bottom()` | Jump to latest output |
| `display_offset()` | Current scroll position (0=bottom) |
| `is_running()` | Check if child process alive |
| `is_bracketed_paste_mode()` | Check paste mode for proper paste handling |

### Selection API

```rust
terminal.start_selection(col, row);           // Simple drag
terminal.start_semantic_selection(col, row);  // Word (double-click)
terminal.start_line_selection(col, row);      // Line (triple-click)
terminal.update_selection(col, row);          // Extend
terminal.selection_to_string();               // Get text
terminal.clear_selection();
```

## PtyManager (pty.rs)

Cross-platform PTY using portable-pty.

### Platform Support

- **macOS/Linux**: Native PTY via `/dev/ptmx`
- **Windows**: ConPTY (Windows 10 1809+)

### Key Features

- Background reader thread for non-blocking I/O
- Automatic shell detection (`$SHELL` / `%COMSPEC%`)
- Environment setup: `TERM=xterm-256color`, `COLORTERM=truecolor`
- Resize sends SIGWINCH to child process

```rust
let mut pty = PtyManager::with_size(cols, rows)?;
pty.write_all(b"ls -la\n")?;
pty.resize(100, 50)?;
```

## TermPrompt (term_prompt.rs)

GPUI component for terminal UI.

### Creation

```rust
TermPrompt::with_height(
    id: String,
    command: Option<String>,        // Optional initial command
    focus_handle: FocusHandle,
    on_submit: SubmitCallback,      // Callback on exit/escape
    theme: Arc<Theme>,
    config: Arc<Config>,
    content_height: Option<Pixels>, // Explicit height (GPUI entities don't inherit flex)
) -> anyhow::Result<Self>
```

### Refresh Timer

Runs at 60fps (`REFRESH_INTERVAL_MS = 16`). Handles:
- Polling `terminal.process()`
- Auto-scroll when at bottom
- Bell flash timeout
- Title updates

### Keyboard Handling

| Key | Action |
|-----|--------|
| Escape | Cancel/close |
| Ctrl+C | SIGINT (0x03) or copy if selection |
| Cmd+C | Copy selection, or SIGINT if none |
| Cmd+V | Paste (with bracketed paste mode support) |
| Shift+PageUp/Down | Scroll history |
| Shift+Home/End | Scroll to top/bottom |
| Arrow keys | Send escape sequences (`\x1b[A/B/C/D`) |

### Cell Dimensions

```rust
const BASE_FONT_SIZE: f32 = 14.0;
const LINE_HEIGHT_MULTIPLIER: f32 = 1.3;
const BASE_CELL_WIDTH: f32 = 8.5;  // Conservative for Menlo

// Scaled to config font size
fn cell_width(&self) -> f32 {
    BASE_CELL_WIDTH * (self.font_size() / BASE_FONT_SIZE)
}
```

### Render Optimization

Batches consecutive cells with same styling to reduce element count from ~2400 (80x30) to ~50-100 per frame.

## ThemeAdapter (theme_adapter.rs)

Maps Script Kit theme to terminal colors.

### Color Mapping

| Theme Property | Terminal Use |
|----------------|--------------|
| `background.main` | Terminal background |
| `text.primary` | Default foreground |
| `accent.selected` | Cursor |
| `accent.selected_subtle` | Selection background |
| `terminal.*` | All 16 ANSI colors |

### Focus Dimming

```rust
adapter.update_for_focus(false);  // Dim colors 30% toward gray
adapter.update_for_focus(true);   // Restore original
```

## TerminalEvent

```rust
pub enum TerminalEvent {
    Output(String),     // Content for rendering
    Bell,               // BEL character (\x07)
    Title(String),      // OSC title change
    Exit(i32),          // Process exit code
}
```

## TerminalContent

Snapshot for rendering:

```rust
pub struct TerminalContent {
    pub lines: Vec<String>,                    // Plain text
    pub styled_lines: Vec<Vec<TerminalCell>>,  // Per-cell styling
    pub cursor_line: usize,
    pub cursor_col: usize,
    pub selected_cells: Vec<(usize, usize)>,   // Selection coordinates
}
```

## CellAttributes

Bitflags for text styling:

```rust
const BOLD           = 0b0000_0000_0000_0001;
const ITALIC         = 0b0000_0000_0000_0010;
const UNDERLINE      = 0b0000_0000_0000_0100;
const DOUBLE_UNDERLINE = 0b0000_0000_0000_1000;
const UNDERCURL      = 0b0000_0000_0001_0000;
const STRIKEOUT      = 0b0000_0000_1000_0000;
const INVERSE        = 0b0000_0001_0000_0000;
const DIM            = 0b0000_0100_0000_0000;
```

## 256-Color Palette

Resolved in `resolve_indexed_color()`:

- **0-15**: ANSI colors from theme
- **16-231**: 6x6x6 color cube
- **232-255**: 24 grayscale shades

## Common Patterns

### Send Control Characters

```rust
// Ctrl+C (SIGINT)
terminal.input(&[0x03])?;

// Ctrl+D (EOF)
terminal.input(&[0x04])?;

// Ctrl+Z (SIGTSTP)
terminal.input(&[0x1A])?;
```

### Escape Sequences

```rust
// Arrow keys
terminal.input(b"\x1b[A")?;  // Up
terminal.input(b"\x1b[B")?;  // Down
terminal.input(b"\x1b[C")?;  // Right
terminal.input(b"\x1b[D")?;  // Left

// Function keys
terminal.input(b"\x1bOP")?;  // F1
terminal.input(b"\x1b[15~")?; // F5
```

### Bracketed Paste

```rust
if terminal.is_bracketed_paste_mode() {
    let wrapped = format!("\x1b[200~{}\x1b[201~", text);
    terminal.input(wrapped.as_bytes())?;
} else {
    terminal.input(text.as_bytes())?;
}
```

## Thread Safety

- `TerminalHandle.state`: `Arc<Mutex<TerminalState>>`
- Background PTY reader thread communicates via `mpsc::channel`
- `reader_stop_flag`: `AtomicBool` for clean shutdown
- Safe to call `content()` from render thread while processing I/O
