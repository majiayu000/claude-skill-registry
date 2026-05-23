---
name: XM Format (FastTracker 2)
description: |
  Use this skill for XM file generation - the simpler of the two tracker formats. Provides Python library for programmatic XM creation.

  **Trigger phrases:** "generate XM", "write XM file", "XM module", "FastTracker", "procedural XM", "XM effects"

  **Load references when:**
  - Effect command details → `references/xm-effects.md`
  - Binary format details → `references/xm-format-spec.md`

  **Use XM when:**
  - Simpler songs with ≤32 channels
  - Smaller file size preferred
  - Don't need NNA polyphony or pitch envelopes

  **Use IT instead when:** Need >32 channels, NNA, pitch envelopes, or resonant filters.

  For composition philosophy, use `tracker-fundamentals`.
  For music theory, use `sound-design:music-composition`.
version: 1.1.0
---

# XM Format (FastTracker 2)

## Overview

XM is the simpler and more compact format. Ideal for most game music needs.

**Key limits:**
- Up to 32 channels
- Note range: C-0 to B-7 (8 octaves)
- Volume and panning envelopes only (no pitch envelope)

## Quick Start

```python
from xm_writer import XmModule, XmPattern, XmNote, XmInstrument, write_xm

# Create pattern
pattern = XmPattern.empty(64, num_channels=4)
pattern.set_note(0, 0, XmNote.play("C-4", instrument=1, volume=64))

# Create module with embedded samples
module = XmModule(
    name="My Song",
    num_channels=4,
    default_speed=6,
    default_bpm=125,
    order_table=[0],
    restart_position=0,
    patterns=[pattern],
    instruments=[XmInstrument.for_zx("kick", kick_bytes)],
)

write_xm(module, "output.xm")
```

## Core API

### XmNote

```python
XmNote.play("C-4", instrument=1, volume=64)  # Note on
XmNote.off()                                  # Note off
note_from_name("C#4")                         # Name to value
```

### XmPattern

```python
pattern = XmPattern.empty(64, num_channels=4)
pattern.set_note(row, channel, note)
```

### XmInstrument

```python
XmInstrument.for_zx("kick", sample_bytes)  # Convenience for 22050 Hz

# Full control:
XmInstrument(
    name="kick",
    sample_data=kick_bytes,   # 16-bit signed PCM
    sample_rate=22050,        # Auto-calculates pitch correction
    sample_loop_type=0,       # 0=one-shot, 1=forward, 2=ping-pong
)
```

### XmModule

```python
XmModule(
    name="Song Name",
    num_channels=4,           # 1-32
    default_speed=6,          # Ticks per row
    default_bpm=125,          # Tempo
    restart_position=0,       # Loop point in order table
    order_table=[0, 1, 0, 2], # Pattern sequence
    patterns=[...],
    instruments=[...],
)
```

## Common Effects

| Effect | Hex | Usage |
|--------|-----|-------|
| Arpeggio | 0 | `.with_effect(0, 0x37)` (minor chord) |
| Porta Up | 1 | `.with_effect(1, 0x10)` |
| Porta Down | 2 | `.with_effect(2, 0x10)` |
| Tone Porta | 3 | `.with_effect(3, 0x10)` |
| Vibrato | 4 | `.with_effect(4, 0x34)` |
| Vol Slide | 10 | `.with_effect(10, 0x0F)` (down) |
| Speed/Tempo | 15 | `.with_effect(15, 6)` if <32, else BPM |

See `references/xm-effects.md` for complete list.

## Pitch Correction

XM expects 8363 Hz samples at C-4. For 22050 Hz ZX samples:

```python
# Recommended: Use convenience constructor
XmInstrument.for_zx("kick", data)

# Or set sample_rate:
XmInstrument(name="kick", sample_rate=22050, sample_data=data)
```

## Volume Column

Values 0-64 set volume directly. Values 65+ are effects:

| Range | Effect |
|-------|--------|
| 0x10-0x50 | Set volume 0-64 |
| 0x60-0x6F | Volume slide down |
| 0x70-0x7F | Volume slide up |
| 0xC0-0xCF | Set panning |
| 0xF0-0xFF | Tone portamento |

## Validation

```python
from xm_writer import validate_xm
validate_xm("output.xm")  # Raises ValueError if invalid
```

## Nethercore Integration

```toml
[[assets.trackers]]
id = "boss_theme"
path = "music/boss_theme.xm"
```

```rust
let music = rom_tracker(b"boss_theme", 10);
music_play(music, 0.8, 1);
```

## Parser Location

The XM writer is part of the unified `.studio/` infrastructure.

**Source:** `ai_studio_core/templates/project/studio/parsers/`
- `xm_writer.py` - XM file writing
- `xm_types.py` - XM data structures

**Setup:** Run `/init-procgen` to install the `.studio/` scaffold (generator + parsers).

## Project Structure

```
project/
├── .studio/parsers/
│   ├── xm_writer.py     # Downloaded via /init-procgen
│   └── xm_types.py
├── .studio/specs/music/
│   └── song_name.spec.py
└── generated/music/
    └── song_name.xm     # Output (gitignored)
```

## API Reference Files

- **`.studio/parsers/xm_types.py`** - API surface (~250 lines, READ THIS)
- **`.studio/parsers/xm_writer.py`** - Binary packing (just import, don't read)
- **`references/xm-effects.md`** - Complete effect reference
- **`references/xm-format-spec.md`** - Binary format specification
