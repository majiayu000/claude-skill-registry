---
name: icon-lookup
description: >-
  Workaround for Claude Code filtering BMP PUA Unicode (U+E000-U+F8FF). Supplementary PUA Nerd Font icons like 󰊤 󱃾 󰁹 (U+F0000+, e.g. nf-md-github, nf-md-kubernetes, nf-md-battery) can be written directly. BMP PUA icons (Powerline, Font Awesome, Devicons) require placeholder syntax like {{ U+E0A0 }} or {{ nf-fa-star }} (without spaces), which hooks auto-convert. Invoke when reading or writing Starship configs, tmux themes, shell prompts, or statuslines.
---

# BMP PUA Unicode Workaround

Claude Code filters Unicode characters in the BMP Private Use Area (U+E000-U+F8FF), which includes most Nerd Font icons. This skill provides tools for working with these icons.

## Quick Reference

| Range                          | Status                          | Examples                                    |
| ------------------------------ | ------------------------------- | ------------------------------------------- |
| U+E000-U+F8FF (BMP PUA)        | **Filtered** - use placeholders | Powerline, Devicons, Font Awesome, Octicons |
| U+F0000+ (Supplementary PUA-A) | Works directly                  | Material Design Icons (nf-md-*)             |

## Automatic Features

**When reading files:** A PostToolUse hook automatically identifies all PUA characters, showing icon names, codepoints, and whether they're filtered.

**When writing files:** A PostToolUse hook automatically converts placeholder syntax to actual Unicode characters.

## Placeholder Syntax

When writing icons in the filtered BMP PUA range, use placeholder syntax:

- By codepoint: `{{ U+E0A0 }}` (without the spaces)
- By name: `{{ nf-fa-star }}` (without the spaces)

## Icon Lookup

Search for icons by name:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lookup-icon.py "<search query>"
```

Example searches:

- `git branch` → finds git-related icons
- `folder` → finds folder/directory icons
- `wizard` → finds wizard icons

## Character Identification

Identify a specific character:

```bash
# Direct argument (this is nf-md-battery, a Supplementary PUA icon)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/identify-icons.py -c "󰁹"

# From stdin
echo "󰁹" | python3 ${CLAUDE_PLUGIN_ROOT}/scripts/identify-icons.py -
```

## Workflow

1. **Reading files** - Hook automatically shows icon info; use this to understand what icons are present
2. **Writing icons** - Search with lookup script, then use placeholder syntax for filtered icons
3. **Comparing icons** - Use identify script to check if two characters are the same icon
4. **Material Design Icons** (U+F0000+) can be written directly without placeholders

## Manual Conversion

If placeholders weren't converted (e.g., hook didn't run):

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/convert-placeholders.py /path/to/file
```
