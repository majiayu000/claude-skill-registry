---
context: fork
---

# /summarize

Summarize a note or set of notes.

## Usage

```
/summarize <note name>
/summarize Meeting - 2025-01-05 MyDataIntegration Review
/summarize all meetings about CloudMigration
/summarize last 5 meetings
```

## Instructions

### Single Note Summary

1. Find the note by name (fuzzy match if needed)
2. Read the full content
3. Generate summary:

```markdown
# Summary: {{note title}}

**Type**: {{type}}
**Date**: {{date if applicable}}

## Key Points

- {{main point 1}}
- {{main point 2}}
- {{main point 3}}

## Decisions Made

- {{decision 1}}

## Action Items

- [ ] {{action 1}}
- [ ] {{action 2}}

## People Involved

{{attendees or people mentioned}}

## Related Notes

{{suggest related notes based on content}}
```

### Multiple Notes Summary (use sub-agents)

For "all meetings about X" or "last N meetings":

**Phase 1: Planning**

- Identify which notes to summarize
- Create list of files to process

**Phase 2: Parallel Processing**
Launch sub-agents using `model: "haiku"` for efficiency:

- Launch sub-agent per note (max 5 parallel)
- Each agent extracts: key points, decisions, actions

**Phase 3: Synthesis**

```markdown
# Summary: {{description of note set}}

**Notes Analysed**: {{count}}
**Date Range**: {{earliest}} to {{latest}}

## Executive Summary

{{2-3 paragraph synthesis of all notes}}

## Key Themes

1. **{{theme 1}}**: {{explanation}}
2. **{{theme 2}}**: {{explanation}}

## All Decisions

| Date | Source | Decision |
| ---- | ------ | -------- |

{{consolidated decisions}}

## Outstanding Actions

| Action | From | Assigned | Due |
| ------ | ---- | -------- | --- |

{{consolidated actions}}

## Progression

{{how topics evolved across the notes}}
```
