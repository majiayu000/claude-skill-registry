---
name: compress-session
description: Compress session conversation into structured summary for system memory. Activate when user says "compress", "compress session", or after significant work. Captures decisions, tools built, breakthroughs, and context that git commits can't preserve.
allowed-tools: Read, Write, Bash
---

# Compress Session

Compress active session into structured summary. Capture decisions, tools built, breakthroughs - the "why" and "how" that git commits don't preserve.

## When to Activate

- User says: "compress", "compress session"
- After significant milestones
- Every ~10 messages in long sessions
- Before ending major work

## Process

### 1. Determine Sequence Number

```bash
ls -t inbox/session-summaries/$(date +%Y-%m-%d)*.md 2>/dev/null | head -1
```

- If files exist: increment (seq2, seq3...)
- If none: this is seq1

### 2. Review Conversation

Identify signal vs. noise:
- **INCLUDE:** Decisions, tools built, breakthroughs, key quotes, context
- **SKIP:** Pleasantries, process discussion without outcome, redundant info

### 3. Write Summary

Create: `inbox/session-summaries/YYYY-MM-DD-HHMM-seqN.md`

```markdown
# Session Capture: YYYY-MM-DD [Sequence N]

**Time:** [Start] - [Current]
**Roles Active:** [List or "general"]
**Messages:** [Approximate range]
**Branch:** [git branch]

---

## Context

[1-3 sentence narrative of what happened this sequence]

---

## Decisions Made

- [Decision 1]
  - Reason: [Why]
- [Decision 2]

---

## Tools/Workflows Built

- **[Name]:** [Description and purpose]

[Or: None this sequence]

---

## Breakthroughs/Insights

- [Insight] - [Significance]

---

## Key Quotes

- "[Quote]" ([Context])

---

## Files Created/Modified

[From git status]
- New: [files]
- Modified: [files]

---

## Next Steps

- [What's coming]

---

**Session compressed. Sequence [N] captured.**
```

### 4. Confirm

```
Session compressed. Sequence [N] captured.
Stored: inbox/session-summaries/YYYY-MM-DD-HHMM-seqN.md
```

## What to Include

- Decisions affecting work/strategy/direction
- Tools/workflows built or planned
- Breakthroughs (creative, technical, conceptual)
- Context explaining *why* decisions were made
- Key quotes revealing intent

## What to Skip

- Conversational filler
- Detailed implementation (git shows that)
- Process discussion without decision
- Speculation that didn't become action

## Tone

- Concise, structured
- Bullet points over paragraphs
- Searchable and scannable
- Neutral observation
