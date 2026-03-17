---
name: sketch-prompt-lab
description: Prompt iteration workflow for kid-friendly, realistic outputs. Use when tuning prompts, selecting styles, or when outputs look too similar to the original sketch.
---

# Sketch Prompt Lab

## Overview
Guide prompt iteration for friendly, realistic outputs while keeping the child’s intent and avoiding unsafe themes.

## Workflow

### 1) Start with a preset
Pick the closest preset from `references/prompt-recipes.md` and keep the safety language intact.

### 2) Adjust one dimension at a time
- **Realism**: “storybook-realistic” → “more realistic textures and lighting.”
- **Color**: “bright cheerful colors” → “soft pastel colors.”
- **Background**: “simple background” → “cozy bedroom or park.”

### 3) Avoid overfitting to the original
If the output matches the sketch too closely, add:
- “Use the sketch as inspiration, but create a new, finished illustration.”
- “Refine shapes and add realistic textures.”

### 4) Enforce guardrails
- Keep “friendly, safe, no weapons.”
- Keep prompts under the configured length limits.

## References
- `references/prompt-recipes.md`
