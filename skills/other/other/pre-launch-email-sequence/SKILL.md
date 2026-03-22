---
name: pre-launch-email-sequence
description: Crafts the pre-launch email sequence for VIPs and main list to build anticipation, drive preview traffic, and prime early conversion.
---

# Pre-Launch Email Sequence

This skill produces a pre-launch cadence that includes Announcement and Reminder emails with preview access and VIP window clarity.

## Input Variables
- [BRAND_BIBLE]
- [PRODUCT_BIBLE]
- [PERSONA_DATA]

## The Protocol
1. Extract launch date, VIP window, preview link.
2. Write Announcement email (T-7 days) with preview CTA.
3. Write Reminder email (T-1 day) with VIP-first promise.
4. Include image slots, button CTAs, and optional A/B subject lines.
5. Provide JSON handoff (dates, segments, links).

## Output Instructions
Render the emails in `templates/pre-launch-email-sequence.md` with clear scheduling and segmentation notes.



## Integration & Technical Specs

### API Specification
- **ID**: `pre-launch-email-sequence`
- **Path**: `skills/pre-launch-email-sequence/templates/pre-launch-email-sequence.md`
- **Context**: Part of *Robust Email Strategy*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `pre-launch-email-sequence.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate pre-launch-email-sequence
```
