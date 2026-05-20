---
name: cinematic-direction
description: Extract cinematic entities from narrative text. Use when analyzing cutscenes, camera paths, transitions, fades, flashbacks, and cinematic pacing.
---
# cinematic-direction

Domain skill for Cinematic Director. Specific extraction rules and expertise.

## Domain Expertise

- **Cutscene direction**: Camera angles, pacing, narrative delivery
- **Camera work**: Pan, zoom, shake, tracking, flythroughs
- **Transitions**: Fade, wipe, cut, dissolve
- **Flashbacks**: Narrative structure, memory sequences
- **Cinematic timing**: Pacing, tension buildup, release

## Entity Types (6 total)

- **cutscene** - Cutscenes and scripted sequences
- **cinematic** - General cinematic events
- **camera_path** - Camera paths and movements
- **transition** - Transitions between scenes
- **fade** - Fade effects
- **flashback** - Flashbacks and memory sequences

## Processing Guidelines

When extracting cinematic entities from chapter text:

1. **Identify cinematic elements**:
   - Cutscene descriptions or scripted events
   - Camera movements or angles mentioned
   - Transitions between scenes
   - Flashbacks or memory recalls
   - Fade effects or visual transitions

2. **Extract cinematic details**:
   - Camera types (fixed, tracking, handheld)
   - Camera movements (pan, zoom, dolly, shake)
   - Transition types and durations
   - Flashback content and triggers
   - Fade in/out effects

3. **Analyze cinematic context**:
   - Narrative function of cinematic moments
   - Emotional impact of camera choices
   - Pacing and tension through editing
   - Storytelling through visuals

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Player control**: Cinematics should give control back quickly
- **Skipping**: Important story cinematics vs skippable content
- **Consistency**: Camera language should be consistent
- **Pacing**: Cinematics shouldn't overstay welcome
- **Visual storytelling**: Show, don't always tell
