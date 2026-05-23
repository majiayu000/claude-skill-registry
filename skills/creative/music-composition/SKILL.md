---
name: Music Composition Reference
description: |
  Use this skill when DESIGNING music content - choosing keys, chord progressions, tempos for specific contexts.

  **Triggers:** "chord progression", "what key for", "tempo for", "music theory", "leitmotif", "adaptive music", "loop design", "listener fatigue", "hours of play", "background music", "supportive music", "music mix space".

  **Pipeline position: DESIGN (1 of 3)**
  - For tracker file creation: use `tracker-music` plugin
  - For instrument synthesis: use `zx-procgen:procedural-instruments`

  **Load references when:**
  - Chord progressions by emotion → `references/chord-progressions.md`
  - Adaptive music patterns → `references/adaptive-patterns.md`
  - Genre-specific templates → `references/genre-templates.md`
version: 1.4.0
---

# Music Composition for Games

Game music must loop seamlessly, respond to gameplay, and support rather than dominate the experience.

## Core Principles

1. **Supportive** - Enhances, doesn't distract
2. **Loopable** - Most game music repeats indefinitely
3. **Adaptive** - Responds to game state
4. **Memorable** - Themes should be recognizable
5. **Efficient** - Work within platform constraints

---

## Extended Duration Design

Players hear tracks for **hours**. Favor texture/rhythm over hooks. Leave 30-40% frequency space for SFX/dialogue. Avoid harsh 2-4kHz, constant highs, unvarying dynamics.

**Invisible music principle:** Best game music is felt, not noticed—you don't hum it, but you don't tire of it.

---

## Supportive Music Philosophy

Music serves **player's emotional state**, not composer's vision. If player notices music mid-combat, you may have distracted them.

| Context | Music's Job | NOT the Job |
|---------|-------------|-------------|
| Combat | Amplify adrenaline | Be the star |
| Exploration | Create atmosphere | Demand attention |
| Story/dialogue | Underscore, stay low | Compete for attention |

---

## Quick Reference: Keys by Mood

| Mood | Common Keys | Mode |
|------|-------------|------|
| Triumphant | C, G, D Major | Ionian, Lydian |
| Tense | Am, Dm, Em | Aeolian, Phrygian |
| Mysterious | Dm, Em (modal) | Dorian, Mixolydian |
| Melancholic | Am, Bm, F#m | Aeolian |
| Aggressive | Cm, Gm, Em | Phrygian |
| Peaceful | C, F, G Major | Ionian, Lydian |
| Epic | D, G or Dm, Gm | Depends on context |

---

## Quick Reference: Tempos

| Context | BPM | Character |
|---------|-----|-----------|
| Menu | 80-110 | Inviting |
| Exploration | 70-100 | Relaxed |
| Puzzle | 80-110 | Thoughtful |
| Combat | 140-170 | Intense |
| Boss | 150-190 | Climactic |
| Stealth | 60-90 | Tense |
| Victory | 100-140 | Triumphant |

---

## Common Chord Progressions

**Triumphant:** `I - IV - V - I` or `I - V - vi - IV`

**Tense:** `i - bVI - bVII - i` or `i - iv - bVII - bVI`

**Mysterious:** `i - bVII - bVI - bVII` or modal vamps

**Epic Build:** `i - bVI - bIII - bVII`

→ See `references/chord-progressions.md` for extended database.

---

## Song Structures

### Loop-Based (Gameplay)
```
[Intro] → [A] → [B] → [A'] → [Loop to A]
  4        8      8      8    bars
```

### Boss Battle
```
[Intro] → [Phase1] → [Build] → [Phase2] → [Loop]
  4         16          4        16       bars
```

### Layered (Adaptive)
```
Layer 1: Ambient pad (always)
Layer 2: Rhythm (add at intensity 0.3)
Layer 3: Melody (add at intensity 0.6)
Layer 4: Full power (add at intensity 0.9)
```

→ See `references/adaptive-patterns.md` for implementation details.

---

## Seamless Loop Checklist

1. **Harmonic:** Last chord leads to first
2. **Rhythmic:** Beat doesn't skip
3. **Melodic:** No jarring jumps
4. **Timbral:** Same instruments active
5. **Dynamic:** Similar volume levels

---

## Leitmotif Design

Effective leitmotifs are:
- **Short:** 4-8 notes maximum
- **Distinctive:** Unique interval pattern
- **Flexible:** Works in major AND minor
- **Memorable:** Singable/hummable

**Transformation techniques:**
- Melodic: Change to minor/major
- Rhythmic: Change note durations
- Instrumental: Different instruments for contexts

---

## Genre Patterns

| Genre | Structure | Key Elements |
|-------|-----------|--------------|
| Orchestral | Theme + Variations | Full dynamics, counterpoint |
| Electronic | Build + Drop | Sidechain, filter sweeps |
| Chiptune | Simple loops | Arpeggios, limited polyphony |
| Ambient | Evolving texture | No clear rhythm, long reverb |

→ See `references/genre-templates.md` for detailed patterns.

---

## Practical Workflow

1. **Context:** What's happening on screen?
2. **Parameters:** Key, tempo, duration
3. **Foundation:** Chords, bass, rhythm
4. **Identity:** Main melody/theme
5. **Polish:** Loop point, mix, test

## Related Components

- `/design-soundtrack` - Interactive composition wizard
- `music-architect` agent - Detailed composition help
- `sonic-style-language` skill - Style/mood parameters
