---
name: vte-escape-sequences
description: ANSI escape sequence parsing with VTE for terminal emulation
---

# vte-escape-sequences

The `vte` crate (version 0.15) provides a state-machine parser for ANSI escape sequences used in terminal emulators. Developed by the Alacritty team, it implements Paul Williams' ANSI parser state machine and is the foundation for terminal emulation in script-kit-gpui.

## Key Types

### `Parser`

The core state machine that parses raw bytes into terminal actions.

```rust
use vte::Parser;

let mut parser = Parser::new();
let mut performer = MyPerformer;

// Advance parser with raw bytes
parser.advance(&mut performer, &bytes);

// Or advance until early termination
let bytes_read = parser.advance_until_terminated(&mut performer, &bytes);
```

**Key methods:**
- `new()` - Create a new parser
- `advance(&mut performer, &[u8])` - Process bytes, calling performer methods
- `advance_until_terminated(&mut performer, &[u8])` - Process until `Perform::terminated()` returns true

### `Perform` Trait

Implement this trait to handle parsed escape sequences:

```rust
pub trait Perform {
    fn print(&mut self, c: char) { }              // Regular printable character
    fn execute(&mut self, byte: u8) { }           // C0/C1 control (e.g., \n, \r, \t)
    fn csi_dispatch(&mut self, params: &Params, intermediates: &[u8], ignore: bool, action: char) { }
    fn esc_dispatch(&mut self, intermediates: &[u8], ignore: bool, byte: u8) { }
    fn osc_dispatch(&mut self, params: &[&[u8]], bell_terminated: bool) { }
    fn hook(&mut self, params: &Params, intermediates: &[u8], ignore: bool, action: char) { }
    fn put(&mut self, byte: u8) { }               // DCS data bytes
    fn unhook(&mut self) { }                      // DCS string terminated
    fn terminated(&self) -> bool { false }        // Early termination check
}
```

### `Params`

Iterator over CSI sequence parameters:

```rust
fn csi_dispatch(&mut self, params: &Params, ...) {
    for param in params.iter() {
        // param is a subparam slice for `:` separated values
        // e.g., SGR 38:2:255:0:0 for RGB colors
    }
}
```

### `vte::ansi` Module Types (via alacritty_terminal)

script-kit-gpui uses these from the `vte::ansi` submodule:

```rust
use vte::ansi::{Color, NamedColor, Processor, Rgb};
```

- **`Rgb`** - RGB color struct with `r`, `g`, `b` fields
- **`Color`** - Enum for terminal colors (Named, Indexed, Rgb)
- **`NamedColor`** - Standard 16 ANSI color names
- **`Processor`** - High-level processor wrapping Parser + Perform

## Usage in script-kit-gpui

The terminal module uses VTE via alacritty_terminal for escape sequence parsing:

### Architecture

```
PTY Output --> VTE Parser --> Term Grid --> GPUI Render
```

### Key Integration Points

**src/terminal/alacritty.rs:**

```rust
use vte::ansi::{Color, NamedColor, Processor, Rgb};

struct TerminalState {
    term: Term<EventProxy>,
    processor: Processor,
}

impl TerminalState {
    fn process_bytes(&mut self, bytes: &[u8]) {
        // VTE 0.15 advance() takes a slice of bytes
        self.processor.advance(&mut self.term, bytes);
    }
}
```

**src/terminal/theme_adapter.rs:**

```rust
use vte::ansi::Rgb;

// Convert hex colors to VTE's Rgb type
pub fn hex_to_rgb(hex: u32) -> Rgb {
    Rgb {
        r: ((hex >> 16) & 0xFF) as u8,
        g: ((hex >> 8) & 0xFF) as u8,
        b: (hex & 0xFF) as u8,
    }
}
```

## ANSI Escape Sequences Reference

### Sequence Structure

```
ESC [ <params> <intermediate> <final>
 ^   ^    ^          ^          ^
 |   |    |          |          +-- Action character (A, B, m, J, etc.)
 |   |    |          +-- Optional intermediate bytes (!, ?, >)
 |   |    +-- Semicolon-separated numbers
 |   +-- CSI introducer '['
 +-- Escape character (0x1B)
```

### Common CSI Sequences

| Sequence | Description | Perform Method |
|----------|-------------|----------------|
| `ESC[<n>A` | Cursor up n lines | `csi_dispatch` action='A' |
| `ESC[<n>B` | Cursor down n lines | `csi_dispatch` action='B' |
| `ESC[<n>C` | Cursor forward n cols | `csi_dispatch` action='C' |
| `ESC[<n>D` | Cursor back n cols | `csi_dispatch` action='D' |
| `ESC[<r>;<c>H` | Move cursor to row;col | `csi_dispatch` action='H' |
| `ESC[J` | Clear screen (0=below, 1=above, 2=all) | `csi_dispatch` action='J' |
| `ESC[K` | Clear line (0=right, 1=left, 2=all) | `csi_dispatch` action='K' |
| `ESC[<n>m` | Set Graphics Rendition (SGR) | `csi_dispatch` action='m' |

### SGR (Select Graphic Rendition) Codes

| Code | Effect |
|------|--------|
| 0 | Reset all attributes |
| 1 | Bold/bright |
| 2 | Dim/faint |
| 3 | Italic |
| 4 | Underline |
| 7 | Inverse/reverse video |
| 8 | Hidden |
| 9 | Strikethrough |
| 22 | Normal intensity (not bold/dim) |
| 23 | Not italic |
| 24 | Not underlined |
| 27 | Not inverse |
| 29 | Not strikethrough |

### Color Codes

**Basic Colors (30-37 fg, 40-47 bg):**
| Code | Color |
|------|-------|
| 30/40 | Black |
| 31/41 | Red |
| 32/42 | Green |
| 33/43 | Yellow |
| 34/44 | Blue |
| 35/45 | Magenta |
| 36/46 | Cyan |
| 37/47 | White |
| 39/49 | Default |

**Bright Colors (90-97 fg, 100-107 bg):**
Same as above but bright variants.

**256 Color Mode:**
- `ESC[38;5;<n>m` - Foreground
- `ESC[48;5;<n>m` - Background
- n = 0-15 standard, 16-231 color cube, 232-255 grayscale

**24-bit RGB:**
- `ESC[38;2;<r>;<g>;<b>m` - Foreground
- `ESC[48;2;<r>;<g>;<b>m` - Background

### C0 Control Characters

| Byte | Name | Action |
|------|------|--------|
| 0x07 | BEL | Bell |
| 0x08 | BS | Backspace |
| 0x09 | HT | Horizontal Tab |
| 0x0A | LF | Line Feed |
| 0x0D | CR | Carriage Return |

These trigger `execute()` in the Perform trait.

### OSC (Operating System Command)

Format: `ESC ] <code> ; <data> BEL` or `ESC ] <code> ; <data> ST`

| Code | Purpose |
|------|---------|
| 0 | Set icon name and window title |
| 1 | Set icon name |
| 2 | Set window title |
| 4 | Change color (palette) |
| 52 | Clipboard operations |

Triggers `osc_dispatch()` in Perform.

## The Perform Trait

### Method Dispatch Flow

```
Byte Stream
    |
    v
+--------+
| Parser |
+--------+
    |
    +---> print(char)          <- Regular text
    |
    +---> execute(byte)        <- Control chars (0x00-0x1F)
    |
    +---> csi_dispatch(...)    <- ESC [ ... sequences
    |
    +---> esc_dispatch(...)    <- ESC ... sequences
    |
    +---> osc_dispatch(...)    <- ESC ] ... sequences
    |
    +---> hook/put/unhook      <- DCS sequences
```

### Example Implementation

```rust
struct MyTerminal {
    cursor_x: usize,
    cursor_y: usize,
}

impl vte::Perform for MyTerminal {
    fn print(&mut self, c: char) {
        // Draw character at cursor, advance cursor
    }

    fn execute(&mut self, byte: u8) {
        match byte {
            0x07 => self.bell(),
            0x08 => self.backspace(),
            0x0A => self.line_feed(),
            0x0D => self.carriage_return(),
            _ => {}
        }
    }

    fn csi_dispatch(&mut self, params: &Params, _intermediates: &[u8], _ignore: bool, action: char) {
        let params: Vec<u16> = params.iter()
            .flat_map(|p| p.iter().copied())
            .collect();
        
        match action {
            'H' | 'f' => {
                // Cursor position: ESC[<row>;<col>H
                let row = params.get(0).copied().unwrap_or(1) as usize;
                let col = params.get(1).copied().unwrap_or(1) as usize;
                self.cursor_y = row.saturating_sub(1);
                self.cursor_x = col.saturating_sub(1);
            }
            'm' => self.handle_sgr(&params),
            'J' => self.clear_screen(params.get(0).copied().unwrap_or(0)),
            _ => {}
        }
    }
}
```

## Parser State Machine

VTE implements the state machine from [vt100.net/emu/dec_ansi_parser](https://vt100.net/emu/dec_ansi_parser):

### States

1. **Ground** - Normal text input, calls `print()` for printable chars
2. **Escape** - After ESC, waiting for sequence type
3. **CSI Entry** - After `ESC[`, collecting parameters
4. **CSI Param** - Collecting numeric parameters
5. **CSI Intermediate** - After intermediate bytes (?, !, >)
6. **OSC String** - Collecting OSC data
7. **DCS Entry/Param/Intermediate/Passthrough** - Device Control String states

### UTF-8 Support

VTE handles UTF-8 decoding internally. Multi-byte sequences are collected and delivered as complete `char` values to `print()`.

### Early Termination

Use `terminated()` for synchronized updates:

```rust
impl Perform for MyTerminal {
    fn terminated(&self) -> bool {
        // Return true to stop parsing (e.g., after sync marker)
        self.sync_complete
    }
}

// Then use:
let bytes_consumed = parser.advance_until_terminated(&mut performer, &bytes);
// Process remaining bytes[bytes_consumed..] later
```

## Anti-patterns

### 1. Blocking in Perform Methods

**Bad:**
```rust
fn print(&mut self, c: char) {
    self.gpu_draw(c).await; // Don't block!
}
```

**Good:**
```rust
fn print(&mut self, c: char) {
    self.buffer.push(c); // Buffer, render later
}
```

### 2. Ignoring the `ignore` Flag

**Bad:**
```rust
fn csi_dispatch(&mut self, params: &Params, _intermediates: &[u8], _ignore: bool, action: char) {
    // Always process...
}
```

**Good:**
```rust
fn csi_dispatch(&mut self, params: &Params, _intermediates: &[u8], ignore: bool, action: char) {
    if ignore {
        return; // Malformed sequence, skip
    }
    // Process valid sequence...
}
```

### 3. Hardcoding Parameter Defaults

**Bad:**
```rust
fn csi_dispatch(&mut self, params: &Params, ..., action: char) {
    match action {
        'A' => self.cursor_up(params[0]), // Panics on empty params!
    }
}
```

**Good:**
```rust
fn csi_dispatch(&mut self, params: &Params, ..., action: char) {
    let params: Vec<u16> = params.iter().flat_map(|p| p.iter().copied()).collect();
    match action {
        'A' => self.cursor_up(params.get(0).copied().unwrap_or(1)),
    }
}
```

### 4. Not Handling Subparameters

**Bad:**
```rust
// Ignores 38:2:R:G:B syntax for true color
let params: Vec<u16> = params.iter().next().map(|p| p[0]).collect();
```

**Good:**
```rust
// Handle both semicolon and colon separated params
for subparams in params.iter() {
    // subparams is a slice for colon-separated values
    match subparams {
        &[38, 2, r, g, b] => self.set_fg_rgb(r, g, b),
        &[38, 5, idx] => self.set_fg_indexed(idx),
        // ...
    }
}
```

### 5. Creating Parser Per Parse

**Bad:**
```rust
fn process(&mut self, bytes: &[u8]) {
    let mut parser = Parser::new(); // New parser loses state!
    parser.advance(&mut self.performer, bytes);
}
```

**Good:**
```rust
struct Terminal {
    parser: Parser,
    state: TermState,
}

fn process(&mut self, bytes: &[u8]) {
    self.parser.advance(&mut self.state, bytes);
}
```

## Integration with alacritty_terminal

In script-kit-gpui, VTE is used indirectly through `alacritty_terminal`:

```rust
// alacritty_terminal provides Processor which wraps VTE Parser
use vte::ansi::Processor;

struct TerminalState {
    term: Term<EventProxy>,
    processor: Processor,
}

impl TerminalState {
    fn process_bytes(&mut self, bytes: &[u8]) {
        // Processor handles parsing and calls Term's Handler impl
        self.processor.advance(&mut self.term, bytes);
    }
}
```

The `Term` type from alacritty_terminal implements the equivalent of VTE's `Perform` trait, handling all escape sequences and updating the terminal grid.
