---
name: terminal
description: Terminal emulation = libghostty-vt + tmux + zsh + fzf + ripgrep.
version: 1.0.0
---


# terminal

Terminal emulation and tools powered by libghostty-vt.

## libghostty-vt (Core Terminal Emulation)

> "libghostty-vt is a zero-dependency library that provides an API for parsing
> terminal sequences and maintaining terminal state" — Mitchell Hashimoto

### What is libghostty-vt?

A C-compatible library extracted from Ghostty for embedding terminal emulation:

| Feature | Description |
|---------|-------------|
| Zero dependencies | No libc required |
| SIMD-optimized | Fast parsing of escape sequences |
| Unicode support | Full UTF-8/grapheme handling |
| Memory efficient | Optimized for embedded use |
| Fuzz-tested | Valgrind-verified, production-proven |

### VT Sequence Types

```
┌─────────────────────────────────────────────────────────────┐
│ C0 Control Characters (0x00-0x1F)                           │
│   BEL (0x07) - Bell/alert                                   │
│   BS  (0x08) - Backspace                                    │
│   TAB (0x09) - Horizontal tab                               │
│   LF  (0x0A) - Line feed                                    │
│   CR  (0x0D) - Carriage return                              │
│   ESC (0x1B) - Escape (starts sequences)                    │
├─────────────────────────────────────────────────────────────┤
│ Escape Sequences (ESC + final)                              │
│   ESC 7    - DECSC (save cursor)                            │
│   ESC 8    - DECRC (restore cursor)                         │
│   ESC D    - IND (index/scroll down)                        │
│   ESC M    - RI (reverse index/scroll up)                   │
│   ESC c    - RIS (full reset)                               │
├─────────────────────────────────────────────────────────────┤
│ CSI Sequences (ESC [ params final)                          │
│   CSI n A  - CUU (cursor up n)                              │
│   CSI n B  - CUD (cursor down n)                            │
│   CSI n C  - CUF (cursor forward n)                         │
│   CSI n D  - CUB (cursor backward n)                        │
│   CSI y;x H - CUP (cursor position)                         │
│   CSI n J  - ED (erase display)                             │
│   CSI n K  - EL (erase line)                                │
│   CSI n m  - SGR (select graphic rendition)                 │
├─────────────────────────────────────────────────────────────┤
│ OSC Sequences (ESC ] id ; data ST)                          │
│   OSC 0    - Set window title + icon                        │
│   OSC 7    - Set working directory                          │
│   OSC 8    - Hyperlinks                                     │
│   OSC 52   - Clipboard access                               │
│   OSC 9;4  - Progress reporting (ConEmu)                    │
├─────────────────────────────────────────────────────────────┤
│ External Protocols                                          │
│   Kitty Graphics Protocol (APC)                             │
│   Kitty Color Protocol (OSC 21)                             │
│   Synchronized Output (DEC mode 2026)                       │
└─────────────────────────────────────────────────────────────┘
```

### libghostty-vt Usage Examples

```zig
// Zig API (available now)
const vt = @import("ghostty-vt");

var terminal = vt.Terminal.init(.{
    .rows = 24,
    .cols = 80,
});

// Parse input bytes
terminal.feed(input_bytes);

// Access terminal state
const cursor = terminal.getCursor();
const cell = terminal.getCell(row, col);
```

```c
// C API (coming soon)
#include <ghostty/vt.h>

ghostty_vt_t* vt = ghostty_vt_new(80, 24);
ghostty_vt_feed(vt, input, len);
ghostty_vt_cursor_t cursor = ghostty_vt_get_cursor(vt);
```

### Projects Using libghostty-vt

| Project | Description |
|---------|-------------|
| [zmx](https://github.com/neurosnap/zmx) | Session persistence for terminals |
| [ghostty-web](https://github.com/coder/ghostty-web) | TypeScript/WASM bindings |
| [openmux](https://github.com/monotykamary/openmux) | Terminal multiplexer |
| [Nekotty2](https://github.com/kengonakajima/Nekotty2) | macOS terminal |
| [ghostty_ansi_html](https://github.com/jossephus/ghostty_ansi_html) | ANSI→HTML converter |

### Architecture

```
┌────────────────────────────────────────────────────────┐
│                    Application                          │
│  (Ghostty GUI, zmx, web terminal, IDE, etc.)           │
├────────────────────────────────────────────────────────┤
│                   libghostty-vt                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │  Parser  │→ │  State   │→ │  Screen/Scrollback   │  │
│  │  (SIMD)  │  │ Machine  │  │  (Ring Buffer)       │  │
│  └──────────┘  └──────────┘  └──────────────────────┘  │
├────────────────────────────────────────────────────────┤
│                      PTY Layer                          │
│              (pseudo-terminal interface)                │
└────────────────────────────────────────────────────────┘
```

## Atomic Skills

| Skill | Domain |
|-------|--------|
| tmux | Multiplexer |
| zsh | Shell |
| fzf | Fuzzy finder |
| ripgrep | Search |

## Tmux

```bash
tmux new -s work
# C-b d (detach)
tmux attach -t work
# C-b % (split vertical)
# C-b " (split horizontal)
```

## Fzf

```bash
# File picker
vim $(fzf)

# History
C-r  # fzf history search

# Directory
cd $(find . -type d | fzf)
```

## Ripgrep

```bash
rg "pattern"
rg -t py "import"
rg -l "TODO"
rg --hidden "secret"
```

## Integration

```bash
# fzf + rg
rg --files | fzf | xargs vim
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.