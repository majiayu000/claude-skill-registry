---
name: Sound Vision
description: This skill should be used when the user asks about "sound direction", "audio style", "sonic identity", "music style", "SFX design", "audio mixing", "soundscape", "audio coherence", "audio design document", or discusses establishing or reviewing audio direction. Provides audio direction framework for sonic coherence.
version: 1.0.0
---

# Sound Vision

Establish and maintain sonic coherence through systematic sound direction.

## Three Pillars of Game Audio

1. **Music** - Emotional backbone, pacing, identity
2. **SFX** - Feedback, world-building, immersion
3. **Voice** - Narrative, character, instruction

When one dominates inappropriately, the soundscape fails.

## Sonic Identity

| Dimension | Spectrum |
|-----------|----------|
| Frequency Balance | Bassy ←→ Airy |
| Texture | Synthetic ←→ Organic |
| Processing | Clean ←→ Distorted |
| Reverb | Dry ←→ Wet |
| Dynamics | Compressed ←→ Wide range |
| Attack | Gradual ←→ Punchy |

## Mix Priority Hierarchy

```
PRIORITY 1 (Never duck):
├── Player damage/death feedback
├── Critical gameplay cues
└── Dialogue (when present)

PRIORITY 2 (Light ducking):
├── Player action feedback
├── Immediate threats
└── Important UI

PRIORITY 3 (Duck for 1-2):
├── Ambient world sounds
├── Background music
└── Environmental effects

PRIORITY 4 (Most flexible):
├── Atmospheric layers
└── Distant sounds
```

## Relative Loudness (Music = 0dB reference)

| Element | Range |
|---------|-------|
| Player Actions | +2 to +6dB |
| Enemy Attacks | +0 to +4dB |
| Ambient | -6 to -12dB |
| UI Feedback | +0 to +3dB |
| Dialogue | +6 to +10dB |

## Audio Design Doc Sections

1. **Audio Pillars** - 3-5 sonic principles
2. **Reference Audio** - Games, films, genres
3. **Frequency Allocation** - Which elements own which ranges
4. **Mix Priorities** - Ducking hierarchy
5. **Music Direction** - Instrumentation, genre, adaptivity
6. **SFX Language** - Attack, decay, processing aesthetic

## ZX Considerations

- 8 SFX channels max, 4 music typical
- Balance file size vs quality
- Plan for channel stealing

Store in `.studio/sound-direction.md` or `.studio/creative-direction.md`.

## References

- **`references/mixing-techniques.md`** - Technical mixing
- **`references/adaptive-music.md`** - Dynamic music
- **`references/sound-categories.md`** - SFX categorization
