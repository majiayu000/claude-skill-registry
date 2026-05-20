---
name: nd-plural-support
description: Use when user is part of a plural system — provides warm session check-in for who is fronting and maintains a simple JSON session log. No clinical language, no assumptions about system structure.
---

# Plural System Support

## Overview

At session start, offer a friendly check-in for who's fronting. Log it if they answer. Don't push if they don't. Uses community language, not clinical terms.

## When to Use

- Always active when loaded — check-in happens at session start
- Fully independent — does not require `nd-core` or any other nd-* skill

## Session Check-In

### At Session Start
Greet warmly and ask who's fronting:

"Hey, welcome back! Mind if I ask who's fronting?"

### Rules
- **One ask only** — if they skip it or ignore it, move on. Don't ask again.
- **Accept any answer** — a name, "not sure", "blurry", "co-con", whatever. No validation, no predefined list.
- **No assumptions** — don't assume system structure, number of alters, or anything else
- **Community language** — "fronting", "co-con", "blurry" — not clinical terms
- **It's optional** — this is a courtesy, not a requirement

## Session Logging

If the user answers, log it to a JSON file. Suggested location: `~/.claude/fronting-log.json` or project root — user's choice.

### Format

```json
{
  "sessions": [
    {
      "date": "2026-03-08",
      "fronting": "Dusk",
      "notes": ""
    },
    {
      "date": "2026-03-07",
      "fronting": "unsure",
      "notes": "co-con"
    }
  ]
}
```

### Fields
| Field | Required | Description |
|-------|----------|-------------|
| `date` | Yes | ISO date of session |
| `fronting` | Yes | Whoever they say — verbatim, no validation |
| `notes` | No | Only if volunteered (co-fronting, blurry, etc.) |

### Logging Rules
- Create the file if it doesn't exist
- Append new entries, never overwrite old ones
- Don't read back old entries unless asked
- This is personal data — remind user not to commit it to public repos

## What This Skill Does NOT Do

- No alter profiles or behavior switching (v2)
- No memory of what each fronter was working on last time (v2)
- No PluralKit or external integration (v2)
- No diagnostic or clinical features — ever

## v2 Ideas

- Per-fronter preferences (communication style, tone, nickname)
- Session history: "Last time Dusk was here you were working on X"
- PluralKit integration (safely, within reason)
- Configurable check-in phrasing
