---
name: mds-messaging-direction-summary
description: Produces the Messaging & Direction Summary covering product pitch, features/benefits, use cases, audiences, value props, objections, brand pitch, competitive notes, USP, desired emotions.
---

# Messaging & Direction Summary (MDS)

This skill compiles the MDS document used as the source of truth for campaign messaging.

## Input Variables
- [PRODUCT_BIBLE]
- [PERSONA_DATA]
- [COMPETITOR_DATA]

## The Protocol
1. Product Pitch: succinct hero description.
2. Features & Benefits: detailed list with why it matters.
3. Use Cases: specific scenes and contexts.
4. Target Audiences: demographics and interests.
5. Value Propositions: functional, emotional, self-expressive reasons.
6. Potential Objections: concerns and rebuttals.
7. Brand Pitch: mission and ethos.
8. Competitive Notes: similarities and differences.
9. USP: unique claim and supporting proof.
10. Desired Emotional Response: target feelings.

## Output Instructions
Render into `templates/mds.md`. Do not omit sections. Include a handoff JSON block.



## Integration & Technical Specs

### API Specification
- **ID**: `mds-messaging-direction-summary`
- **Path**: `skills/mds-messaging-direction-summary/templates/mds.md`
- **Context**: Part of *Product Detailing*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `mds.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate mds-messaging-direction-summary
```
