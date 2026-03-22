---
name: short-form-hook-generator
description: Generates 15-second viral hooks for TikTok/Reels/Shorts based on ad copy soundbytes.
---

# Short Form Hook Generator

This skill extracts and refines "scroll-stopping" moments for short-form video content.

## Input Variables
- [AD_CAMPAIGN_DOSSIER] (from pre-launch-ads)
- [MDS] (Messaging Direction Summary)

## The Protocol
1.  **Soundbyte Extraction**: Identify punchy sentences from the Ad Copy that are under 5 seconds when spoken.
2.  **Visual Pairing**: For each hook, describe the visual action that happens immediately (the "Pattern Interrupt").
3.  **Hook Categories**: Generate hooks in these buckets:
    - **Negative/Warning**: "Stop doing this..."
    - **Curiosity/Secret**: "The #1 reason..."
    - **Outcome/Benefit**: "How I got [Result] in [Time]..."
    - **Visual Oddity**: (Describing a weird visual) "What is this thing?"
4.  **Scripting**: Write the first 15 seconds of the script.

## Output Instructions
Render into `templates/viral-hooks.md`.


## Integration & Technical Specs

### API Specification
- **ID**: `short-form-hook-generator`
- **Path**: `skills/short-form-hook-generator/templates/viral-hooks.md`
- **Context**: Part of *Social & Community*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `viral-hooks.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate short-form-hook-generator
```
