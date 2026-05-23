---
name: Procedural Instrument Synthesis
description: |
  Generate instrument samples for ZX game music.

  **Spec-Driven Workflow (RECOMMENDED):**
  1. Create `.spec.py` in `.studio/specs/instruments/`
  2. Run `python .studio/generate.py --only instruments`

  **Load references when:**
  - Instrument specs → `procedural-sounds/references/sound-spec-format.md`
  - Example specs → `examples/bass.spec.py`, `examples/lead.spec.py`
  - Karplus-Strong → `references/karplus-strong.md`
  - FM synthesis → `references/fm-synthesis.md`
  - Drum examples → `references/drum-examples.py`

  **Before generating:** Check `.studio/sonic-identity.md` for audio specs.
version: 5.1.0
---

# Procedural Instrument Synthesis

Generate production-quality instrument samples using a **spec-driven workflow**.

## Spec-Driven Workflow

**Step 1: Create Spec**
```python
# .studio/specs/instruments/bass.spec.py
INSTRUMENT = {
    "instrument": {
        "name": "bass",
        "base_note": "C2",
        "synthesis": {
            "type": "karplus_strong",
            "damping": 0.994,
            "brightness": 0.5
        },
        "envelope": {"attack": 0.01, "decay": 0.4, "sustain": 0.3, "release": 0.3},
        "output": {"duration": 1.5, "bit_depth": 16, "loop": True}
    }
}
```

**Step 2: Run Generator**
```bash
python .studio/generate.py --only instruments
```

See `procedural-sounds/references/sound-spec-format.md` for complete format.

## Technique Selection

| Instrument | Technique | Reference |
|------------|-----------|-----------|
| Acoustic Guitar | Karplus-Strong | `karplus-strong.md` |
| Electric Piano | FM Synthesis | `fm-synthesis.md` |
| Bells | FM (inharmonic) | `fm-synthesis.md` |
| Organ | Additive | `additive-synthesis.md` |
| Strings/Pads | Wavetable | `wavetable-synthesis.md` |
| Synth Lead/Bass | Subtractive | `subtractive-synthesis.md` |
| Drums | See examples | `drum-examples.py` |

## Why Basic Synthesis Sounds Chiptuney

| Problem | Why It Sounds Bad |
|---------|-------------------|
| Raw `np.sin()` | Static timbre, no evolution |
| Simple ADSR | Real instruments have complex envelopes |
| Instant attack | Real instruments have transients |
| Single oscillator | Real instruments have multiple components |

## Quality Checklist

- No clicks (attack/release ramps)
- Pitch correct (verify frequency)
- Timbre evolves (envelope on filter/index)
- Attack has character (transient noise)
- Sounds musical (test in context)

## Related Skills

- `procedural-sounds` - SFX synthesis
- `sound-design/sonic-style-language` - Audio style specs
- `tracker-music/xm-format` - XM writer
