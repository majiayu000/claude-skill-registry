---
name: voice-and-tone
description: Defines brand voice persona and tone calibration using persona and positioning data to produce a reusable meta-prompt for copywriting.
---

# Voice and Tone

This skill constructs the Golden Voice Prompt based on persona culture, lingo, empathy, and emotional targets.

## Input Variables
- [PERSONA_DATA]
- [PRODUCT_POSITIONING]

## The Protocol
1. Select three tone descriptors.
2. Define Voice Persona (peer identity).
3. Specify culture references and lingo.
4. Set empathy statements addressing unique challenges.
5. Select four target emotions.
6. Compose the meta-prompt in exact template form.

## Output Instructions
Render into `templates/voice-and-tone.md`. Keep the template structure intact with filled descriptors.



## Integration & Technical Specs

### API Specification
- **ID**: `voice-and-tone`
- **Path**: `skills/voice-and-tone/templates/voice-and-tone.md`
- **Context**: Part of *Product Detailing*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `voice-and-tone.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate voice-and-tone
```
