---
name: scope-handoffs
description: Use when creating handoff documentation for branched conversations in stay-on-target focused mode
---

# Scope Handoffs

## Overview

Create handoff documentation when a conversation branches to a new topic.

## When to Use

When user selects option (C) "Note for later" during scope drift detection.

## Handoff Document Structure

```markdown
# Handoff: [Topic]

**Created:** [Date]
**From conversation:** [Brief description of original work]

## Summary

[2-3 sentences: What was happening, why we're branching]

## Original Context

- **Approach being used:** [What we were doing]
- **Key files:** [Files involved]
- **Decisions made:** [Important choices]

## New Direction

- **Topic:** [What the new exploration is about]
- **Why considered:** [What prompted this]
- **Questions to explore:** [Open questions]

## Relevant Context

[Any code snippets, decisions, or findings that would help the new conversation]
```

## Location

1. Check CLAUDE.md for `## Handoffs` section with Location
2. If not configured, use `.handoffs/` in project root
3. Ensure directory is gitignored

## Process

1. Ask 1-2 clarifying questions about the new direction
2. Write handoff doc based on conversation context + answers
3. Report: "Handoff saved to [path]. Ready to continue on [original task]."
