---
name: session-journal
description: Use at session start for context warm-up and during work to capture decisions
---

# Session Journal

## Overview

Maintains session continuity by logging decisions, progress, and rationale.

**Core principle:** Check for project lessons at start, log significant decisions during work.

**Announce at start:** "Applying session-journal skill for context warm-up."

## The Process

### At Session Start

1. Check `<workspace>/.ai-memory/lessons/` for project lessons
2. If found: Load relevant lessons for current context
3. Announce: "Loaded [N] project lessons" or "No prior lessons found"

### During Work

Log significant decisions to `brain/<conversation-id>/sessions/<YYYY-MM-DD>.md`:

```markdown
## Decisions
- **HH:MM** - [Decision]: [Rationale]
```

Only log when:
- Choosing between alternatives
- Making architectural decisions
- Deviating from expected approach

### At Session End

1. Summarize accomplishments
2. Note open threads
3. Check if patterns emerged → trigger `lessons-capture` if so

## Session Log Format

```markdown
# Session: YYYY-MM-DD

## Lessons Loaded
[List of project lessons applied]

## Decisions
- **14:32** - Chose Redis over Memcached: Better pub/sub for realtime
- **15:07** - Used existing auth pattern from lesson `auth-jwt.md`

## Open Threads
- [ ] Need to verify rate limiting behavior
```

## Discrepancy Handling

If a loaded lesson contradicts current MCP data (Jira, Confluence):

1. Flag: `> [!WARNING] Lesson X says Y but MCP says Z`
2. Use MCP data for this session
3. At session end, prompt: "Update lesson?"

## Common Mistakes

- Logging every small decision (keep it scannable)
- Forgetting to note WHY a decision was made
- Not checking for project lessons at session start
- Silently overriding lessons without flagging

## Checklist

Before ending session:

- [ ] Significant decisions logged with rationale
- [ ] Open threads documented
- [ ] Any discrepancies flagged and addressed
