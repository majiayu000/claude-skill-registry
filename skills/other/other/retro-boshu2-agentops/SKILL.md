---
name: retro
description: 'Quick-capture a learning. For full retrospectives, use /post-mortem. Trigger phrases: "quick learning", "capture lesson", "retro quick".'
skill_api_version: 1
metadata:
  tier: knowledge
  dependencies: []
context:
  window: fork
output_contract: ".agents/learnings/YYYY-MM-DD-*.md"
---

# Retro Skill

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Quick-capture a learning to the knowledge flywheel. For comprehensive retrospectives with backlog processing, activation, and retirement, use `/post-mortem`.

## Quick Mode

Given `/retro --quick "insight text"` or `/retro "insight text"`:

1. Generate a slug from the content: first meaningful words, lowercase, hyphens, max 50 chars.
2. Write directly to `.agents/learnings/YYYY-MM-DD-quick-<slug>.md`:

```markdown
---
type: learning
source: retro-quick
date: YYYY-MM-DD
maturity: provisional
utility: 0.5
---

# Learning: <Short Title>

**Category**: <auto-classify: debugging|architecture|process|testing|security>
**Confidence**: medium

## What We Learned

<user's insight text>

## Source

Quick capture via `/retro --quick`
```

3. Confirm:

```
Learned: <one-line summary>
Saved to: .agents/learnings/YYYY-MM-DD-quick-<slug>.md

For comprehensive knowledge extraction, use `/post-mortem`.
```

**Done.** Return immediately after confirmation.

## Examples

**User says:** `/retro --quick "macOS cp alias prompts on overwrite — use /bin/cp to bypass"`

**What happens:**
1. Agent generates slug: `macos-cp-alias-overwrite`
2. Agent writes learning to `.agents/learnings/2026-03-03-quick-macos-cp-alias-overwrite.md`
3. Agent confirms: `Learned: macOS cp alias prompts — use /bin/cp`

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Learning too generic | Surface-level capture | Be specific: "auth tokens expire after 1h" not "learned about auth" |
| Duplicate learnings | Same insight captured twice | Check existing learnings with grep before writing |
| Need full retrospective | Quick capture isn't enough | Use `/post-mortem` for comprehensive extraction + processing |
