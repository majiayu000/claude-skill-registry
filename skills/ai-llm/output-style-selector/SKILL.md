---
name: output-style-selector
description: Automatically choose the best output style (tables, bullets, YAML, HTML, concise) to improve scanability and save tokens
version: 0.1.0
tags: [formatting, context]
triggers:
  - style
  - format
  - output style
---

# Output Style Selector

## Purpose
Select a response style that maximizes readability and minimizes back-and-forth.

## Behavior
1. Infer intent from prompt keywords and task type.
2. Choose one of: table-based, bullet-points, yaml-structured, html-structured, genui, ultra-concise, markdown-focused.
3. Emit a short “Style Block” (1–2 lines) describing the chosen style.
4. Respect overrides: `[style: <name>]` or `[style: off]`.

## Guardrails
- Only inject when helpful; avoid long style instructions.
- Keep the Style Block compact.

## Integration
- `UserPromptSubmit` and sub-agent prompts (documentation, reviewer, PM).

## Example Style Block
> Style: Table Based. Use a summary paragraph and then tables for comparisons and actions.

