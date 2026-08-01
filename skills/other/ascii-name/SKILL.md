---
name: ascii-name
description: Print a name or word as large ASCII block letters. Use when the user runs /ascii-name, optionally followed by the text to render.
allowed-tools: []
---

# /ascii-name — Your Name in Lights

You render text as large ASCII block letters, the way the Architecture Studio README renders its own name.

## Steps

1. If the user gave text after the command, use it. Otherwise ask: "Whose name are we putting in lights?"
2. Draw the text in block capitals, 6 rows tall, built from `█ ╗ ╔ ╝ ╚ ║ ═` characters, inside a code block so the spacing holds.
3. Offer one alternate style if they want it (outline, small caps, or a different character set).

## Rules

- Keep it under 80 characters wide — break long names onto two lines rather than shrinking.
- No commentary before the art. The art is the answer.
