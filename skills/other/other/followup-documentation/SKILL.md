---
name: followup-documentation
description: Evaluate whether changes need CLAUDE.md, rules, or skill updates
user-invocable: true
disable-model-invocation: true
---
Review the current plan or recent changes and evaluate whether they require documentation updates to `CLAUDE.md`, `.claude/rules/`, or `.claude/skills/`.

## The Brevity Constraint

The brevity of these files is hard-won. Every line costs context tokens in every session (for CLAUDE.md and rules) or every skill invocation (for skills). Do not add content without passing this test:

> **"Would removing this cause Claude to make mistakes?"**

If the answer is no — if Claude would figure it out from the code, from static analysis, or from common sense — don't add it. Prefer building static analysis checks (`tests/check_*.ps1`, auto-discovered by pre-gate) over adding rules. Machines enforce; rules explain judgment.

## What to Evaluate

### CLAUDE.md changes

CLAUDE.md is for "tattoo" rules needed in every session. Only propose additions here if the change introduces something Claude would get wrong every time without being told:
- New global scoping patterns that break AHK conventions
- New tool names or changed tool flags
- New architectural constraints that affect all work

### Rules file changes (`.claude/rules/`)

Rules files are domain-specific — loaded contextually, not every session. Propose changes here for:
- New domain knowledge that applies whenever working in that area (e.g., a new komorebi quirk goes in `komorebi.md`)
- Changed architecture that invalidates existing rules (e.g., process model change needs `architecture.md` update)
- New pitfall patterns (e.g., a new AHK v2 gotcha goes in `ahk-patterns.md`)

### Skill changes (`.claude/skills/`)

Skills are loaded only when invoked. Propose changes here for:
- Review skills whose scope, file references, or Known Safe patterns are affected by the changes
- Action skills (release, ship) whose steps changed
- New skills warranted by the changes (rare — only if a new recurring workflow emerged)

## Output Format

| File | Section | Change Type | What | Why |
|------|---------|-------------|------|-----|
| `architecture.md` | Process Roles | Update | Add new producer role | New producer added, Claude needs to know it exists |
| `ahk-patterns.md` | — | No change | — | Changes don't introduce new AHK patterns |
| `review-latency` | Explore Strategy | Update | Add new file to Path 1 agent list | New producer file is on the hot path |
| `CLAUDE.md` | — | No change | — | Nothing here rises to "every session" level |

For each proposed addition, include the exact text to add and where it goes. Keep it as short as possible — one line if one line suffices.

For each "no change" verdict on a file that might seem like it needs updating, briefly explain why it doesn't. This prevents the next reviewer from re-asking the same question.
