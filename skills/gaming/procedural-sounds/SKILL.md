---
name: Procedural Sound Generation with NumPy/SciPy
description: |
  Generate sound effects for ZX games using Python synthesis.

  **Spec-Driven Workflow (RECOMMENDED):**
  1. Create `.spec.py` in `.studio/specs/sounds/`
  2. Run `python .studio/generate.py --only sounds`

  **Load references when:**
  - SFX specs → `references/sound-spec-format.md`
  - Example specs → `examples/laser.spec.py`, `examples/explosion.spec.py`
  - Recipes → `references/sfx-recipes/`
  - Manual synthesis → `references/numpy-scipy-building-blocks.md`
  - Quality standards → `references/quality-standards.md`

  **Before generating:** Check `.studio/sonic-identity.md` for audio specs.
version: 4.1.0
---

# Procedural Sound Generation

Generate game sound effects using a **spec-driven workflow**.

```bash
pip install numpy scipy soundfile
```

## Spec-Driven Workflow

**Step 1: Create Spec**
```python
# .studio/specs/sounds/laser.spec.py
SOUND = {
    "sound": {
        "name": "laser",
        "duration": 0.25,
        "layers": [
            {"type": "fm_synth", "carrier_freq": 600, "mod_ratio": 1.5, "mod_index": 6.0},
            {"type": "noise_burst", "duration": 0.02, "amplitude": 0.3}
        ],
        "envelope": {"attack": 0.002, "decay": 0.15, "sustain": 0, "release": 0.08}
    }
}
```

**Step 2: Run Generator**
```bash
python .studio/generate.py --only sounds
```

See `references/sound-spec-format.md` for complete format.

## ZX Audio Requirements

| Spec | Value |
|------|-------|
| Sample Rate | 22050 Hz |
| Bit Depth | 16-bit |
| Channels | Mono |
| Simultaneous | 16 + 1 music |

## Quality Standards (Temp Tier)

**Minimum requirements:**
- 2-3 synthesis layers
- Proper envelope (exp decay, NOT linear)
- Filtering (lowpass sweep or static)
- Richness (harmonics or detuning)
- Normalization (0.9 peak)

**Anti-patterns:**
- Simple sine + linear fade
- Single oscillator, no filtering
- Instant attack (clicks)

See `references/quality-standards.md` for complete checklist.

## Technique Selection

| Technique | Best For |
|-----------|----------|
| Subtractive | Bass, warm, explosive |
| FM | Metallic, bells, digital |
| Additive | Organs, complex tones |
| Karplus-Strong | Plucked strings |

## Recipe Library

| Sound Type | Recipe |
|------------|--------|
| Laser/Zap | `sfx-recipes/laser.py` |
| Explosion | `sfx-recipes/explosion.py` |
| Hit/Impact | `sfx-recipes/hit.py` |
| Coin/Pickup | `sfx-recipes/coin.py` |
| Jump | `sfx-recipes/jump.py` |
| UI Click | `sfx-recipes/ui-click.py` |

**Workflow:** (1) Find closest recipe, (2) Read file, (3) Copy and customize.

## nether.toml Integration

```toml
[[assets.sounds]]
id = "laser"
path = "generated/sounds/laser.wav"
```

```rust
let laser = rom_sound_str("laser");
play_sound(laser);
```

## File Organization

```
.studio/specs/sounds/
├── laser.spec.py
└── explosion.spec.py

generated/sounds/
├── laser.wav
└── explosion.wav
```
