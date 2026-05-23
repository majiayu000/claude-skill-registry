---
name: Creative Vision
description: This skill should be used when the user asks about "creative vision", "game vision", "creative direction", "overall feel", "creative pillars", "design intent", "vision alignment", "creative drift", "game identity", "player experience", "emotional design", or discusses establishing the overall creative direction and ensuring implementation matches vision. Provides creative direction framework for holistic project coherence.
version: 1.0.0
---

# Creative Vision

Establish and maintain creative coherence by defining core vision and ensuring all disciplines serve it.

## The Vision Hierarchy

```
         Creative Vision (What experience do we create?)
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
Art Vision    Sound Vision    Tech Vision
    │               │               │
 [Assets]       [Audio]         [Code]
```

## Creative Pillars

Define 3-5 non-negotiable experience principles:

```
PILLAR: [Short Name]
STATEMENT: [What this means for the player]
MANIFESTS AS:
- Art: [How art supports this]
- Sound: [How sound supports this]
- Code: [How mechanics support this]
```

**Example:**
```
PILLAR: Atmospheric Dread
STATEMENT: Players should feel isolated and vulnerable
MANIFESTS AS:
- Art: Dark palettes, obscured vision, decay
- Sound: Sparse, ambient, silence as tool
- Code: Limited resources, no map, permadeath
```

## Experience Promise

One-paragraph core experience:

```
In [GAME], players experience [CORE EMOTION] through
[PRIMARY MECHANIC]. The world evokes [ATMOSPHERE] while
players [CORE VERB]. Success feels like [SUCCESS EMOTION]
and failure teaches [FAILURE LESSON].
```

## Vision Document Sections

1. **Experience Promise** - One paragraph
2. **Creative Pillars** - 3-5 with manifestations
3. **Emotional Journey** - Start → Early → Mid → Late → End
4. **Target Audience** - Primary, Secondary, Not For
5. **Reference Works** - Games, films, art with aspects to draw
6. **Anti-Patterns** - What to explicitly avoid

## Vision Alignment Check

For any work, map to pillars:
- **Supports** - Actively reinforces
- **Neutral** - Doesn't affect
- **Conflicts** - Works against (drift indicator)

Ask: Does this reinforce the experience promise? Evoke intended emotions? Suit the audience?

## Detecting Creative Drift

**Warning signs:**
- Style inconsistency with established work
- Emotional tone mismatch
- Features that don't serve pillars
- Scope changes without pillar review

**Response:** Acknowledge → Trace origin → Evaluate (evolution vs loss?) → Decide → Document

## Director Coordination

| Situation | Primary Director |
|-----------|------------------|
| New feature | Creative |
| Asset review | Art/Sound |
| Performance issue | Tech |
| Milestone review | Creative + All |

Store vision in `.studio/creative-direction.md`.

## References

- **`references/pillar-design.md`** - Crafting effective pillars
- **`references/emotional-design.md`** - Designing emotional experiences
