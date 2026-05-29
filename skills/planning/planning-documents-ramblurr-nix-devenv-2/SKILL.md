---
name: Planning Documents
description: Naming conventions for planning documents in prompts/. Use when creating plans, PRDs, research reports, idea capture or other workflow documents. Triggers on (1) creating new planning documents, (2) naming PRDs or research reports, (3) questions about document organization in prompts/.
---

# Planning Documents

All workflow documents live in `prompts/` with a structured naming scheme.

## Primary Documents (PRDs)

Pattern: `prompts/NNN-concept.md`

| Component | Description | Example |
|-----------|-------------|---------|
| `NNN` | Three-digit sequence number | 025 |
| `concept` | Kebab-case description | compositor, event-parsing |

No underscores in the primary document name.

Examples:
- `prompts/025-compositor.md`
- `prompts/010-event-parsing.md`

## Supporting Documents

| Pattern | Purpose | Example |
|---------|---------|---------|
| `NNN-concept_report.md` | Research findings | `025-compositor_report.md` |
| `NNN-concept_library_report.md` | Library-specific research | `025-compositor_textual_report.md` |
| `NNN-concept_idea.md` | Some idea/brainstorm capture | `011-cli-api_idea2.md` |

## Determining Next Sequence Number

Check existing documents:

```bash
ls prompts/*.md | sort -t- -k1 -n | tail -5
```

Use the next available three-digit number.
