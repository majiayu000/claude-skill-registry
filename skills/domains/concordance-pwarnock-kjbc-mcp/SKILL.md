---
name: Strong's Concordance Lookup
description: Use this skill when the user asks about biblical Greek or Hebrew words, Strong's numbers, original language meanings, word etymology in Scripture, or concordance lookups
version: 1.0.0
---

# Strong's Concordance Lookup

You have access to Strong's Concordance via the KJBC MCP server. Use these tools to provide grounded biblical language information.

## Available Tools

### `mcp__kjbc__word` - Search by English word
Find Strong's numbers for any English word in the KJV.

**Parameters:**
- `word` (required): English word to search
- `language`: "greek" (default) or "hebrew"
- `show_verses`: Include verse references (default: false)

**Example:** To find Greek words for "love", call `mcp__kjbc__word` with `{"word": "love", "language": "greek"}`

### `mcp__kjbc__entry` - Get Strong's definition
Look up the full definition for a Strong's number.

**Parameters:**
- `entry_number` (required): Strong's number (e.g., "G26", "H7965")
- `language`: "greek" (default) or "hebrew"

**Example:** To get the definition of agape, call `mcp__kjbc__entry` with `{"entry_number": "G26", "language": "greek"}`

### `mcp__kjbc__langs` - List languages
Returns available languages (Greek, Hebrew).

## When to Use

Use these tools when the user asks about:
- Original Greek or Hebrew words behind English translations
- Word definitions or etymology in biblical texts
- Strong's numbers or concordance lookups
- Comparing different Greek/Hebrew words translated the same way in English

## Response Guidelines

When providing concordance information:
1. State the Strong's number (e.g., G26)
2. Give the transliterated word (e.g., "agape")
3. Include pronunciation if available
4. Provide the definition
5. Note any relevant context about word usage

Do not speculate beyond what the concordance provides. The data is factual reference material.
