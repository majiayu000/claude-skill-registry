---
name: Pattern Design
description: |
  Use this skill when structuring tracker songs - pattern layout, song structure, efficiency, and loop design.

  **Trigger phrases:** "song structure", "pattern layout", "order table", "loop point", "how many patterns", "verse chorus", "song form"

  **Load references when:**
  - Genre-specific templates → `references/genre-templates.md`
  - Loop point techniques → `references/loop-techniques.md`

  For effect usage, use `tracker-fundamentals`.
  For format-specific details, use `xm-format` or `it-format`.
version: 1.1.0
---

# Pattern Design

## Core Concepts

### Pattern vs Order Table

```
Patterns: Unique musical content (A, B, C, D)
Order Table: Sequence of pattern playback

Order: [0, 1, 1, 2, 1, 1, 2, 3, 0]
       [A, B, B, C, B, B, C, D, A]  ← Song structure

Result: A plays once, B twice, C once, B twice again, etc.
```

**Key insight:** Reuse patterns via order table. Never duplicate pattern content.

### Standard Lengths

| Length | Rows | Use Case |
|--------|------|----------|
| Short | 32 | Fills, transitions |
| Standard | 64 | Verses, choruses (default) |
| Extended | 128 | Long sections (rare) |

**Rows per beat:** At speed 6, BPM 125: 4 rows = 1 beat, 16 rows = 1 bar

## Song Structures

### Loop-Based (Game Background Music)

```
Order: [0, 1, 1, 2, 1, 1, 2, 3]
        ↓  ↓←loop back←←←←↓

Pattern 0: Intro (plays once)
Pattern 1: Main A (verse)
Pattern 2: Main B (chorus/variation)
Pattern 3: Transition (leads back to 1)

Restart Position: 1 (skip intro on loop)
```

### Linear (Cutscenes, Jingles)

```
Order: [0, 1, 2]  (End command at pattern 2's end)
No restart - one-shot playback
```

## Pattern Budget

| Song Length | Patterns | Order Length |
|-------------|----------|--------------|
| 30s loop | 2-3 | 4-6 |
| 1min loop | 4-5 | 8-12 |
| 2min loop | 6-8 | 16-24 |

**The 4-Pattern Song:** Most simple tracks need only 4 patterns:
- Pattern 0: Intro
- Pattern 1: Verse/Main
- Pattern 2: Chorus/Variation
- Pattern 3: Bridge/Breakdown

## Section Templates

### Intro Pattern

```
Rows 0-15:  Sparse (drums only, or ambient pad)
Rows 16-31: Add bass
Rows 32-47: Add melody fragment
Rows 48-63: Build to full groove
```

### Main/Verse Pattern

```
Rows 0-15:  Full groove established
Rows 16-31: Groove continues
Rows 32-47: Melodic content
Rows 48-63: Lead into next section
```

### Chorus Pattern

```
Rows 0-15:  Impact! Full energy
Rows 16-31: Hook melody prominent
Rows 32-47: Hook develops
Rows 48-63: Prepare transition
```

## Loop Point Design

### Seamless Loop Requirements

1. **Harmonic continuity** - Last chord leads to first
2. **Rhythmic continuity** - Beat doesn't skip
3. **Timbral continuity** - Same instruments active
4. **Dynamic continuity** - Similar volume levels

### Last 8 Rows Preparation

```
Row 56: Start volume fades (A08)
Row 58: Drum fill or transition start
Row 60: Clear held notes
Row 63: Clean state for loop
```

### Setting Restart Position

```python
module = XmModule(
    # ...
    restart_position=1,  # Skip pattern 0 (intro) on loop
)
```

## 64-Row Grid Reference

```
Rows    | Bar | Beat | Content
--------|-----|------|--------
0-15    | 1   | 1-4  | Phrase A
16-31   | 2   | 1-4  | Phrase A (variation)
32-47   | 3   | 1-4  | Phrase B
48-63   | 4   | 1-4  | Phrase B + transition
```

### Drum Grid (4-on-floor)

```
Row | Beat | Kick | Snare | HH
----|------|------|-------|----
0   | 1.1  | X    |       | X
4   | 1.2  |      |       | X
8   | 1.3  |      | X     | X
12  | 1.4  |      |       | X
16  | 2.1  | X    |       | X
...
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| 20 near-identical patterns | 5 patterns with order repetition |
| Duplicate pattern to change 2 notes | Use sub-patterns or effects |
| Song just cuts and restarts | Fade out, fill, harmonic resolution |
| 256-row sparse patterns | 64-row patterns, order for length |

## Reference Files

- **`references/genre-templates.md`** - Complete templates for dance, ambient, boss battle, etc.
- **`references/loop-techniques.md`** - Advanced loop point techniques, fills, transitions
