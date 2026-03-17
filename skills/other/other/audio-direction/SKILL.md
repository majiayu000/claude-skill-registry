---
name: audio-direction
description: Extract audio entities from narrative text. Use when analyzing music themes, sound effects, ambient audio, motifs, dynamic scoring, and silence as narrative device.
---
# audio-direction

Domain skill for Audio Director. Specific extraction rules and expertise.

## Domain Expertise

- **Music systems**: Themes, motifs, dynamic scoring, adaptive music
- **Sound effects**: Footsteps, impacts, ambient sounds, combat sounds
- **Voice audio**: Voice lines, voice over, dubbing
- **Music control**: Fading, transitions, volume, ducking
- **Audio atmospherics**: Ambient sounds, environmental audio, silence

## Entity Types (10 total)

- **ambient** - Ambient sounds and environmental audio
- **motif** - Musical motifs and leitmotifs associated with characters/themes
- **music_control** - Music control systems (fading, transitions, ducking)
- **music_state** - Music states (combat, exploration, dialogue)
- **music_theme** - Music themes and musical compositions
- **music_track** - Individual music tracks with metadata
- **score** - Musical scores and larger compositions
- **sound_effect** - Sound effects (SFX) for gameplay events
- **soundtrack** - Complete soundtracks and album-style collections
- **silence** - Silence as a narrative device

## Processing Guidelines

When extracting audio entities from chapter text:

1. **Identify audio elements**:
   - Music descriptions (soft, dramatic, ominous)
   - Sound effects mentioned (footsteps, rain, combat)
   - Voice references (speaking, shouting, whispering)
   - Atmospheric sounds (birds, wind, silence)
   - Music themes or motifs

2. **Extract audio details**:
   - Track names, composers, durations
   - Sound effect types and intensities
   - Motifs and musical themes
   - Music states (combat, exploration, dialogue)
   - Volume levels and transitions

3. **Analyze audio context**:
   - Mood and atmosphere through audio
   - Music changes based on situation
   - Audio cues for gameplay events
   - Silence or lack of sound

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Dynamic music**: Music changes based on gameplay context
- **Layering**: Multiple audio elements can play simultaneously
- **Atmosphere**: Audio sets emotional tone and immersion
- **Silence**: Sometimes silence is more powerful than music
- **Cultural context**: Music reflects world's culture
