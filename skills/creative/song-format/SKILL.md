---
name: Song Spec Format
description: |
  Declarative song specification format for programmatic XM/IT tracker module generation.

  **Trigger phrases:** "song spec", "SONG dict", "generate song from spec",
  "tracker module spec", "song specification", "music spec"

  **Load references when:**
  - Full format details -> `references/song-spec-format.md`
  - Example specs -> `examples/boss_theme.spec.py`

  For instrument synthesis, see `zx-procgen/procedural-instruments`.
  For pattern design philosophy, see `tracker-music/pattern-design`.
version: 1.0.0
---

# Song Spec Format

Declarative specification format for XM/IT tracker modules. The spec defines instruments, patterns, and arrangement - the parser handles all binary generation.

All specs use `.spec.py` extension. The containing folder and dict name (`SONG`) identify the type.

## Quick Start

```python
# .studio/specs/music/theme.spec.py
SONG = {
    "song": {
        "name": "theme",
        "format": "xm",
        "bpm": 120,
        "speed": 6,
        "channels": 4,

        "instruments": [
            {"ref": "../instruments/kick.spec.py"},
            {"ref": "../instruments/bass.spec.py"}
        ],

        "patterns": {
            "main": {
                "rows": 64,
                "notes": {
                    0: [{"row": 0, "note": "C-3", "inst": 0, "vol": 64}],
                    1: [{"row": 0, "note": "C-2", "inst": 1, "vol": 64}]
                }
            }
        },

        "arrangement": [{"pattern": "main", "repeat": 4}],
        "restart_position": 0
    }
}
```

Generate:

```bash
python .studio/generate.py --only music
```

## Spec Structure Overview

| Section | Purpose |
|---------|---------|
| `name`, `title` | Module identification |
| `format` | Output format: `"xm"` or `"it"` |
| `bpm`, `speed` | Tempo (BPM, ticks per row) |
| `channels` | Channel count (XM max 32, IT max 64) |
| `instruments` | Instrument definitions (ref, inline, or WAV) |
| `patterns` | Named patterns with row-based notes |
| `arrangement` | Pattern playback order |
| `automation` | Procedural effects (volume fades, tempo changes) |

## Instruments

Three loading modes:

### External Reference (Recommended)
```python
{"ref": "../instruments/kick.spec.py"}
```
Best for reusable instruments defined in `.studio/specs/instruments/`.

### Inline Synthesis
```python
{
    "name": "bass",
    "synthesis": {"type": "karplus_strong", "damping": 0.994},
    "envelope": {"attack": 0.01, "decay": 0.4},
    "base_note": "C2",
    "output": {"duration": 1.5}
}
```
Self-contained synthesis spec. Good for one-off instruments.

### WAV File
```python
{"wav": "samples/piano.wav", "name": "piano"}
```
Load pre-recorded sample. For complex sounds hard to synthesize.

## Pattern Notes

Row-based note placement (native to tracker format):

```python
"patterns": {
    "verse": {
        "rows": 64,
        "notes": {
            0: [  # Channel 0 (kick)
                {"row": 0, "note": "C-3", "inst": 0, "vol": 64},
                {"row": 16, "note": "C-3", "inst": 0, "vol": 48}
            ],
            1: [  # Channel 1 (snare)
                {"row": 8, "note": "D-3", "inst": 1},
                {"row": 24, "note": "D-3", "inst": 1}
            ]
        }
    }
}
```

### Note Format

| Field | Type | Description |
|-------|------|-------------|
| `row` | int | Row number (0-based, required) |
| `note` | str/int | Note name (`"C-4"`) or MIDI number |
| `inst` | int | Instrument index (0-based) |
| `vol` | int | Volume (0-64, optional) |
| `effect` | int | Effect command hex (optional) |
| `param` | int | Effect parameter (optional) |

### Special Note Values

| Value | Meaning |
|-------|---------|
| `"---"` or `None` | No note |
| `"==="` or `"OFF"` | Note off |
| `"^^^"` or `"CUT"` | Note cut (IT only) |
| `"~~~"` or `"FADE"` | Note fade (IT only) |

### Named Effects

For readability:
```python
{"row": 0, "note": "C-4", "effect_name": "vibrato", "effect_xy": [3, 4]}
```

## Arrangement

Order of pattern playback:

```python
"arrangement": [
    {"pattern": "intro"},
    {"pattern": "verse", "repeat": 2},
    {"pattern": "chorus"},
    {"pattern": "verse", "repeat": 2},
    {"pattern": "outro"}
],
"restart_position": 1  # Skip intro on loop
```

## Automation

Procedural effects applied during generation:

```python
"automation": [
    {
        "type": "volume_fade",
        "pattern": "intro",
        "channel": 0,
        "start_row": 0,
        "end_row": 32,
        "start_vol": 0,
        "end_vol": 64
    },
    {
        "type": "tempo_change",
        "pattern": "chorus",
        "row": 0,
        "bpm": 140
    }
]
```

## IT-Specific Options

```python
"it_options": {
    "stereo": True,
    "global_volume": 128,
    "mix_volume": 48
}
```

IT format provides NNA polyphony, pitch envelopes, and filters not available in XM.

## Parser Location

All parsers are part of the unified `.studio/` infrastructure.

**Source:** `ai_studio_core/templates/project/studio/parsers/`
- `music.py` - Song spec parser (SONG dict → XM/IT file)
- `xm_writer.py`, `xm_types.py` - XM format
- `it_writer.py`, `it_types.py` - IT format
- `sound.py` - Instrument synthesis

**Setup:** Run `/init-procgen` to install/update the unified `.studio/` scaffold.

```bash
python .studio/generate.py --only music
```

## File Organization

All specs use `.spec.py`. The folder determines the type:

```
.studio/
└── specs/
    ├── instruments/
    │   ├── kick.spec.py       # INSTRUMENT dict
    │   ├── bass.spec.py
    │   └── lead.spec.py
    └── music/
        ├── boss_theme.spec.py  # SONG dict
        └── menu_theme.spec.py

generated/
└── music/
    ├── boss_theme.xm
    └── menu_theme.xm
```

## See Also

- `references/song-spec-format.md` - Complete format reference
- `examples/` - Example song specs
- `pattern-design` - Pattern layout best practices
- `zx-procgen/procedural-instruments` - Instrument synthesis
