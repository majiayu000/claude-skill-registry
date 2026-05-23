---
name: Tracker Music Fundamentals
description: |
  Use this skill when generating tracker music to understand WHY to use specific techniques. This is the philosophy layer that separates amateur from polished output.

  **Pipeline position: COMPOSITION (3 of 3)**
  - For music theory (modes, progressions): use `sound-design:music-composition`
  - For instrument synthesis: use `zx-procgen:procedural-instruments`

  **Trigger phrases:** "why use vibrato", "when to use effects", "make it sound professional", "tracker polish", "humanize the music", "sound less mechanical"

  **Load references when:**
  - Effect combinations/mood mapping → `references/effect-philosophy.md`
  - Sample budget/reuse strategies → `references/sample-economy.md`
  - Channel layout patterns → `references/channel-allocation.md`
  - Quality checklist → `references/quality-checklist.md`

  For format-specific implementation, use `xm-format` or `it-format` skills.
version: 1.2.0
---

# Tracker Music Fundamentals

## Core Philosophy

Tracker music is **constraint-driven art**. Limited channels, limited polyphony, limited effects - but these constraints create a distinctive aesthetic. The goal isn't to simulate an orchestra; it's to create music that sounds *intentional* within tracker limitations.

**Three Pillars:**
1. **Economy** - Maximum musical impact with minimum resources
2. **Expression** - Effects as musical expression, not decoration
3. **Flow** - Seamless playback with intentional dynamics

## Amateur vs Polished

| Amateur | Polished |
|---------|----------|
| Flat velocity throughout | Velocity variation on repeating notes |
| Effects used randomly | Effects serve musical purpose |
| Copy-paste patterns | Pattern variations with small changes |
| Abrupt note endings | Volume fades and release tails |
| Mechanical timing | Slight groove variations |

## Effect Quick Reference

Effects aren't decoration - they're **musical expression encoded as data**.

| Effect | When to Use | When NOT to Use |
|--------|-------------|-----------------|
| Vibrato (H/4) | Sustained leads 8+ rows | Drums, bass, short notes |
| Portamento (G/3) | Melodic transitions, emphasis | Drums, staccato |
| Arpeggio (J/0) | Chords on limited channels | When spare channels exist |
| Volume Slide (D/A) | Fades, swells, dynamics | Steady bass lines |
| Pitch Slide (E-F/1-2) | Kick punch, synth attacks | Acoustic instruments |
| Retrigger (Q/E9x) | Snare rolls, builds | Sustained passages |

### Effect Application Patterns

```python
# Vibrato for warmth (delay entry for natural feel)
row 0:  C-4 01 -- ---   # Clean attack
row 4:  --- -- -- H24   # Vibrato enters (speed 2, depth 4)

# Portamento for emphasis (slide INTO important notes)
row 0:  C-4 01 40 ---   # Setup note
row 8:  E-4 01 40 G10   # Slide UP to target

# Punchy kick with pitch drop
row 0:  C-5 01 40 E40   # Start high, slide down fast
```

## Human Feel Techniques

### Velocity Variation

Never use the same velocity for repeating notes:

```python
# Pattern for natural feel
velocities = [48, 40, 44, 36, 48, 38, 46, 40]
for i, row in enumerate(range(0, 64, 4)):
    vol = velocities[i % len(velocities)]
    pattern.set_note(row, ch, ItNote.play("C-4", inst, vol))
```

### Ghost Notes

Quiet notes between main hits add life:

```python
for row in range(0, 64, 2):
    if row % 4 == 0:
        pattern.set_note(row, ch, note.with_volume(48))  # Main
    else:
        pattern.set_note(row, ch, note.with_volume(24))  # Ghost
```

### Groove/Swing

Use note delay (SDx) for swing feel:

```python
for row in range(0, 64, 4):
    if (row // 4) % 2 == 1:
        note = note.with_effect(19, 0xD2)  # SD2: delay odd hits
    pattern.set_note(row, ch, note)
```

## Pattern Variation Principles

### The 4-Bar Rule

Never loop the same 4 bars more than twice without variation.

**Variation techniques:**
1. **Add/remove a note** - Same pattern, one element different
2. **Velocity change** - Same notes, different emphasis
3. **Fill on 4th bar** - Drum fill every 4th repetition
4. **Effect variation** - Add vibrato/slide on repeat
5. **Octave shift** - Same melody, different register

## Typical 8-Channel Layout

| Ch | Role | Character |
|----|------|-----------|
| 1 | Kick | Low, punchy |
| 2 | Snare | Mid, snappy |
| 3 | Hi-hat | High, short |
| 4 | Bass | Low synth |
| 5-6 | Leads | Main melody |
| 7 | Pad/Chord | Harmony |
| 8 | FX | Risers, impacts |

## Reference Files

- **`references/effect-philosophy.md`** - Deep dive on effect combinations, mood mapping
- **`references/sample-economy.md`** - Loop points, sample sharing, size optimization
- **`references/channel-allocation.md`** - Detailed channel strategies by genre
- **`references/quality-checklist.md`** - Pre-release validation checklist
