---
name: Sound Effects Design Patterns
description: |
  Use this skill when DESIGNING sound effects - deciding what sounds to create, how to layer them, and what character they should have.

  **Triggers:** "sound effect design", "how to layer SFX", "UI sounds", "impact sound", "weapon sounds", "footsteps", "ambient design".

  **Pipeline position: DESIGN (1 of 3)**
  - For synthesis code (numpy/scipy): use `zx-procgen:procedural-sounds`
  - For quick generation: use `zx-procgen:/generate-sfx`

  **Load references when:**
  - Material sound signatures → `references/material-signatures.md`
  - Layering recipes by category → `references/layering-recipes.md`
  - Variation strategies → `references/variation-strategies.md`
version: 1.3.0
---

# Sound Effects Design

Game SFX communicate information, provide feedback, and enhance immersion. Every sound must serve a purpose.

## Design Philosophy

1. **Functional first** - What information does this convey?
2. **Appropriate scale** - Match visual importance
3. **Distinctive** - Sounds must be distinguishable
4. **Non-fatiguing** - Will be heard thousands of times
5. **Mix-aware** - Must work with music and other SFX

---

## Sound Anatomy

### Temporal Structure
```
[Attack] [Body] [Tail]
  0-50ms  50-500ms  500ms+
```

### Frequency Structure
| Range | Frequencies | Provides |
|-------|-------------|----------|
| Sub | 20-60Hz | Rumble, impact |
| Low | 60-250Hz | Weight, power |
| Mid | 250Hz-4kHz | Character, presence |
| High | 4kHz+ | Detail, definition |

---

## Standard Layering Approach

Most sounds = 3-4 simple layers combined:

| Layer | Focus | Duration | Purpose |
|-------|-------|----------|---------|
| Transient | High | 10-50ms | Timing, definition |
| Body | Mid | 50-200ms | Character, identity |
| Tail | Low/Full | 200ms+ | Space, context |
| Sweetener | Variable | Variable | Polish, uniqueness |

→ See `references/layering-recipes.md` for category-specific breakdowns.

---

## Quick Reference: Categories

### Impacts
- **Variables:** Material, mass, velocity, surface
- **Light:** 50-150ms, quick transient
- **Heavy:** 500ms-3s, layered boom + debris

### Movement (Whooshes)
- **Variables:** Speed, size, direction
- **Core:** Filtered noise with pitch sweep
- **Speed mapping:** Faster = brighter filter cutoff

### UI Sounds
- **Character:** Instant response (< 50ms feel)
- **Family:** All UI sounds should be related
- **Scale:** Small actions = small sounds

### Ambient
- **Looping:** Seamless, non-repetitive
- **Layering:** Multiple different-length loops
- **Role:** Sets mood without demanding attention

→ See `references/material-signatures.md` for material-specific guidance.

---

## Material Quick Reference

| Material | Frequency | Decay | Character |
|----------|-----------|-------|-----------|
| Metal | High mids | Long ring | Clangy, bright |
| Wood | Low mids | Medium | Thuddy, warm |
| Stone | Wide band | Short | Crunchy, solid |
| Flesh | Low mids | Short | Thuddy, soft |
| Glass | Very high | Medium | Shatter, tinkle |

---

## Frequency Allocation (Avoid Masking)

```
Sub (20-80Hz):    Music bass, explosions
Bass (80-250Hz):  Weapon body, footsteps
Low-Mid (250-500Hz): Voices, body of sounds
Mid (500-2kHz):   Primary information
High-Mid (2-6kHz): Presence, attack
High (6kHz+):     Air, sparkle
```

---

## Variation Strategies

Prevent repetition fatigue:

| Method | Memory Cost | Variety |
|--------|-------------|---------|
| Pre-made variations (3-5) | High | Maximum |
| Pitch randomization (±2 semitones) | None | Good |
| Volume randomization (±2 dB) | None | Subtle |
| Layer randomization | Medium | High |

→ See `references/variation-strategies.md` for implementation patterns.

---

## Technical Specs

| Format | Use Case |
|--------|----------|
| WAV 16-bit 44.1kHz | Master/archive |
| WAV 22kHz | Retro consoles |
| OGG | Long sounds (streaming) |

### Memory Budget Template
```
UI:        20 sounds × 5KB  = 100KB
Footsteps: 30 sounds × 10KB = 300KB
Weapons:   50 sounds × 20KB = 1MB
Creatures: 40 sounds × 30KB = 1.2MB
Ambient:   10 loops × 200KB = 2MB
```

---

## Related Components

- `/design-sfx` - Interactive SFX design wizard
- `sfx-architect` agent - Detailed synthesis guidance
- `sonic-style-language` skill - Style consistency
