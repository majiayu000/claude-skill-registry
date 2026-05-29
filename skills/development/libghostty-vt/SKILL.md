---
name: libghostty-vt
description: 'libghostty-vt'
version: 1.0.0
---

# libghostty-vt

Zero-dependency VT sequence parser from Ghostty. Mitchell Hashimoto's embeddable terminal core.

## Status

**NOT YET RELEASED** (as of 2025-09) - Zig API available for testing, C API coming.

## What It Is

`libghostty-vt` extracts Ghostty's proven VT parsing into a standalone library:
- Parse ANSI/VT sequences
- Maintain terminal state
- Zero dependencies (no libc required!)
- SIMD-optimized (>100 MB/s plain text)

## Architecture

```
Raw Bytes → UTF8Decoder → Parser (DFA) → Stream → Actions
                           │
                     State Machine
                     (14 states)
```

### Parser States

| State | Purpose |
|-------|---------|
| `ground` | Normal text printing |
| `escape` | ESC detected (0x1B) |
| `csi_entry` | CSI sequence start |
| `csi_param` | Parsing CSI parameters |
| `osc_string` | OSC data collection |
| `dcs_passthrough` | DCS data collection |

### Action Types

```zig
const Action = union(enum) {
    print: u21,              // Unicode codepoint
    execute: u8,             // C0/C1 control
    csi_dispatch: CSI,       // Control Sequence Introducer
    esc_dispatch: ESC,       // Escape sequence
    osc_dispatch: *osc.Parser,
    dcs_hook: DCS,
    dcs_put: u8,
    dcs_unhook: void,
};
```

## Key Files (ghostty-org/ghostty)

```
src/terminal/Parser.zig      # State machine
src/terminal/stream.zig      # Stream wrapper + SIMD
src/terminal/osc.zig         # OSC parser
src/terminal/parse_table.zig # Compile-time transition table
src/simd/vt.zig              # SIMD acceleration
```

## Performance

| Optimization | Impact |
|--------------|--------|
| Pre-computed state table | O(1) transitions |
| SIMD text processing | 10-100x for plain text |
| Fast-path CSI parsing | Skips state machine |
| Fixed-size buffers | No allocation |

## Use Cases

- Terminal emulators (tmux, zellij, Ghostty)
- IDE terminals (VS Code, JetBrains)
- Cloud terminals (Vercel, Render)
- TUI frameworks
- Terminal recording/playback

## When Available

```bash
# Future installation (not yet available)
# Zig
zig fetch --save git+https://github.com/ghostty-org/libghostty-vt

# C (when released)
# pkg-config --cflags --libs libghostty-vt
```

## Example (Future API)

```zig
const vt = @import("libghostty-vt");

var parser = vt.Parser.init();
var stream = vt.Stream(MyHandler).init(&parser, &handler);

// Process bytes
for (input) |byte| {
    if (stream.next(byte)) |action| {
        switch (action) {
            .print => |cp| handler.print(cp),
            .csi_dispatch => |csi| handler.handleCSI(csi),
            // ...
        }
    }
}
```

## Sources

- https://mitchellh.com/writing/libghostty-is-coming
- https://ghostty.org/docs/about
- https://github.com/ghostty-org/ghostty
- https://vt100.net/emu/dec_ansi_parser

## GF(3) Assignment

```
Trit: +1 (PLUS) - Generator/Parser
Hue: 180° (cyan - terminal green vibes)
```

Triads:
- `libghostty-vt (+1)` × `vterm (0)` × `terminfo (-1)` = 0 ✓
- `libghostty-vt (+1)` × `tmux (0)` × `escape-sequence-validator (-1)` = 0 ✓
