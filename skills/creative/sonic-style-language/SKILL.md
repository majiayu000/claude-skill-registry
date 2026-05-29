---
name: Audio Style Guide
description: |
  Use this skill when generating audio assets (music, SFX, instruments) and you need consistent style.

  **Triggers:** "audio style", "how should it sound", "sound direction", "music style", "audio mood", "instrument palette", "sonic identity".

  **Before generating:** Check `.studio/sonic-identity.md` for project audio direction. If none exists and user wants consistency, suggest `/establish-sonic-identity`.

  **Load references when:**
  - Detailed style specs → `references/sonic-styles.md`
  - Mood parameter mappings → `references/mood-parameters.md`
  - Instrument database → `references/instrument-palettes.md`
  - Processing/effects chains → `references/processing-signatures.md`
version: 3.1.0
---

# Audio Style Guide

Framework for maintaining consistent audio style across procedurally generated sounds and music.

## Core Elements

| Element | Purpose | Example |
|---------|---------|---------|
| **Sonic Style** | Overall aesthetic | Orchestral, Chiptune, Industrial |
| **Mood Palette** | Emotional character | Tense, Triumphant, Mysterious |
| **Instrument Palette** | Sound sources | `orchestral.strings.epic`, `synth.pad.warm` |
| **Processing Signature** | Effect character | `reverb.hall`, `distortion.warm` |

These combine into **Sonic Specifications** - structured bundles ensuring audio coherence.

---

## Quick Reference: Sonic Styles

| Style | Character | Best For |
|-------|-----------|----------|
| Orchestral | Rich, cinematic | RPGs, adventure, drama |
| Chiptune | Retro, limited | Retro games, pixel art |
| Electronic | Modern, synthetic | Sci-fi, racing |
| Industrial | Harsh, mechanical | Horror, action |
| Ambient | Atmospheric, sparse | Exploration, puzzle |
| Dark Ambient | Unsettling, tense | Horror, mystery |
| Hybrid | Orchestra + electronics | AAA, epic |
| Synthwave | 80s, neon | Retro-futurism |

→ See `references/sonic-styles.md` for detailed specifications.

---

## Quick Reference: Moods

| Mood | Key Tendency | Tempo | Character |
|------|--------------|-------|-----------|
| Triumphant | Major | 100-140 | Resolved, powerful |
| Tense | Minor/dim | 80-120 | Unresolved, building |
| Mysterious | Modal | 60-90 | Ambiguous, sparse |
| Aggressive | Minor | 140-180 | Driving, loud |
| Peaceful | Major | 60-80 | Gentle, open |
| Epic | Major/minor | 80-120 | Building to massive |

→ See `references/mood-parameters.md` for full parameter mappings.

---

## Quick Reference: Instrument Notation

```
category.family.variant

Examples:
  orchestral.strings.epic
  synth.pad.warm
  percussion.electronic.punchy
```

→ See `references/instrument-palettes.md` for complete database.

---

## Genre → Style Mapping

| Game Genre | Primary | Secondary | Mood Tendency |
|------------|---------|-----------|---------------|
| Fantasy RPG | Orchestral | Ambient | Epic, Mysterious |
| Sci-Fi Shooter | Electronic | Hybrid | Aggressive, Tense |
| Horror | Dark Ambient | Industrial | Eerie, Tense |
| Platformer | Chiptune | Acoustic | Playful, Triumphant |
| Racing | Electronic | Synthwave | Aggressive, Frantic |
| Puzzle | Ambient | Lo-Fi | Peaceful, Mysterious |
| Roguelike | Synthwave | Chiptune | Tense, Playful |

---

## Sonic Specification Format

Complete audio direction bundles use this structure:

```yaml
# Sonic Specification
game: "Game Title"

style:
  primary: Orchestral
  secondary: Dark Ambient

mood:
  exploration: Mysterious + Melancholic
  combat: Aggressive + Epic
  menu: Mysterious

instruments:
  primary: [orchestral.strings.epic, orchestral.brass.dark]
  accent: [orchestral.percussion.timpani]
  texture: [synth.pad.evolving]

processing:
  reverb: reverb.hall
  character: warm, cinematic

mix_priorities:
  1: player_feedback
  2: dialogue
  3: combat_sfx
  4: music
  5: ambient
```

---

## Processing Signatures

| Type | Variants | Use For |
|------|----------|---------|
| Reverb | none, room, hall, cathedral | Space/distance |
| Distortion | none, warm, crunch, heavy | Character/aggression |
| Filter | lowpass.warm, highpass.thin | Distance/radio effect |

→ See `references/processing-signatures.md` for effect chains.

---

## Usage Workflow

1. **Check existing direction:** Read `.studio/sonic-identity.md`
2. **Match style to genre:** Use genre mapping table
3. **Select moods:** Primary + secondary for each context
4. **Choose instruments:** From appropriate palette
5. **Apply processing:** Match to style character

## Related Components

- `/establish-sonic-identity` - Create full audio specification
- `sonic-designer` agent - Translate creative intent to specs
- `audio-coherence-reviewer` agent - Validate consistency
