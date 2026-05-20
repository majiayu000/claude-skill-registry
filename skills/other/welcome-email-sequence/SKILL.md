---
name: welcome-email-sequence
description: Builds a two-part VIP Welcome Email Sequence aligned to brand voice and product context. Mirrors proven structure and tone while adapting content to the current campaign.
---

# Welcome Email Sequence

This skill acts as an Email Strategist. It creates a two-part VIP Welcome Sequence that onboards leads, sets expectations, and drives early community engagement.

## Input Variables
- [BRAND_BIBLE]: Voice, Guardrails, Tone descriptors
- [PRODUCT_BIBLE]: Features, Materials, Specs, Benefits
- [PERSONA_DATA]: Name, frustrations, anti-goals, emotional drivers

## The Protocol

### Phase 1: Context Loading
1. Absorb [BRAND_BIBLE], [PRODUCT_BIBLE], [PERSONA_DATA].
2. Extract top 3 emotional drivers and top 3 technical claims.

### Phase 2: Style Emulation
3. Calibrate voice to Brand Bible tone descriptors and Voice Persona.
4. Define subject line variants for Email 1 and Email 2.

### Phase 3: Sequence Construction
5. Email 1: VIP confirmation and community invitation. Include discount promise, early access, and private group CTA.
6. Email 2: VIP reconfirmation and reminder. Reinforce benefits and group CTA.

### Phase 4: QA and Handoff
7. Check clarity, brevity, and action flow. Ensure compliance with guardrails.
8. Populate JSON handoff for downstream targeting.

## Output Instructions
Render the sequence in `templates/welcome-email-sequence.md`. Do not truncate key sections. Include subject alternatives and CTAs.



## Integration & Technical Specs

### API Specification
- **ID**: `welcome-email-sequence`
- **Path**: `skills/welcome-email-sequence/templates/welcome-email-sequence.md`
- **Context**: Part of *Robust Email Strategy*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `welcome-email-sequence.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate welcome-email-sequence
```
