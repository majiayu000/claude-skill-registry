---
name: midi-generation
description: Generate MIDI files with GM instruments and music theory. Use when creating music, composing melodies, or generating MIDI files.
license: MIT
---

# MIDI Generation Skill

Generate MIDI files with proper music theory. **Use the provided Python scripts in `skills/`. Do NOT write custom code.**

## Important Rules

1. **Use provided scripts** in `skills/` directory (Python)
2. **Never write custom Python/JS** for MIDI generation
3. **Install dependencies first**: `pip install midiutil`
4. **Consult music theory resources** when needed (see below)

## Quick Dissonance Rules

**Always follow these to avoid harsh sounds:**

1. **Never play notes 1 semitone apart** (C+C#, E+F, B+C)
2. **Bass plays root or fifth** of the chord
3. **Spread voices across octaves** (don't cluster)
4. **Each track uses different MIDI channel** (automatic)

---

## Music Theory Resources (Read When Needed)

**Only read the resource that matches your current task:**

| When you need... | Read this file |
|------------------|----------------|
| Scales, chords, intervals, cadences | [resources/music-theory.md](resources/music-theory.md) |
| Chord progressions by genre | [resources/chord-progressions.md](resources/chord-progressions.md) |
| Avoiding dissonance, voice spacing | [resources/voice-leading.md](resources/voice-leading.md) |
| **Classical/Baroque counterpoint** | [resources/counterpoint.md](resources/counterpoint.md) |
| Modes (Dorian, Phrygian, etc.) | [resources/modes-scales.md](resources/modes-scales.md) |
| Rhythm, time signatures, syncopation | [resources/rhythm-patterns.md](resources/rhythm-patterns.md) |
| Instrument ranges, combinations | [resources/orchestration.md](resources/orchestration.md) |

### When to Read Each Resource

- **Pop/Rock song** → chord-progressions.md + voice-leading.md
- **Classical piece** → counterpoint.md + orchestration.md
- **Jazz composition** → modes-scales.md + chord-progressions.md
- **Film score** → orchestration.md + modes-scales.md
- **Any composition** → Always check voice-leading.md for dissonance

---

## Workflow

1. **Install dependencies**: `pip install midiutil`
2. **Identify genre/style** → Select appropriate resources
3. **Read relevant theory** → Only the files you need
4. **Choose instruments** → See [midi_types/gm_instruments.py](midi_types/gm_instruments.py)
5. **Create composition JSON**
6. **Use scripts** to generate MIDI

## Python Scripts

| Script | Purpose |
|--------|---------|
| `skills/generate_midi.py` | Generate MIDI (auto-assigns channels per track) |
| `skills/normalize_composition.py` | Validate and normalize input |
| `skills/refine_composition.py` | Adjust length, extend tracks |
| `skills/convert_to_wav.py` | MIDI → WAV (requires FluidSynth) |

## Usage Example

```python
import sys
sys.path.insert(0, '/path/to/midi-skill')

from skills.generate_midi import generate_midi_from_dict

composition = {
    "title": "My Song",
    "bpm": 120,
    "tracks": [
        {
            "instrument": "acoustic-grand-piano",
            "notes": [
                {"pitch": "C4", "duration": "4"},
                {"pitch": "E4", "duration": "4"},
                {"pitch": "G4", "duration": "4"},
                {"pitch": "C5", "duration": "2"}
            ]
        },
        {
            "instrument": "acoustic-bass",
            "notes": [
                {"pitch": "C2", "duration": "2"},
                {"pitch": "G2", "duration": "2"}
            ]
        }
    ]
}

midi_path = generate_midi_from_dict(composition)
print(f"Generated: {midi_path}")
```

## Composition Format

```json
{
  "title": "My Song",
  "bpm": 120,
  "tracks": [
    {
      "instrument": "acoustic-grand-piano",
      "notes": [
        { "pitch": "C4", "duration": "4" },
        { "pitch": "E4", "duration": "4" }
      ]
    },
    {
      "instrument": "acoustic-bass",
      "notes": [
        { "pitch": "C2", "duration": "2" }
      ]
    }
  ]
}
```

## Duration Notation

| Value | Note |
|-------|------|
| `1` | Whole note (4 beats) |
| `2` | Half note (2 beats) |
| `d2` | Dotted half (3 beats) |
| `4` | Quarter note (1 beat) |
| `d4` | Dotted quarter (1.5 beats) |
| `8` | Eighth note (0.5 beats) |
| `16` | Sixteenth note (0.25 beats) |

## Instrument Aliases

| Alias | GM Instrument |
|-------|---------------|
| `piano` | acoustic-grand-piano |
| `guitar` | acoustic-guitar-nylon |
| `bass` | acoustic-bass |
| `strings` | string-ensemble-1 |
| `brass` | brass-section |
| `sax` | alto-sax |

Full list: [midi_types/gm_instruments.py](midi_types/gm_instruments.py)

## Notes

- Max 15 melodic tracks (MIDI channels 0-8, 10-15; ch.9 = drums)
- Output: `output/` directory
- WAV requires: FluidSynth + A320U.sf2 in `soundfonts/`
