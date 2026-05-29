---
name: self-improving-agent
version: 1.0.4
description: Captures learnings, errors, and corrections to enable continuous improvement. Review before major tasks.
author: pskoett
homepage: https://clawhub.ai/pskoett/self-improving-agent
metadata:
  openclaw:
    emoji: 🧠
    category: productivity
---

# Self-Improving Agent

Captures learnings, errors, and corrections to enable continuous improvement. This skill creates a feedback loop where the agent learns from mistakes, user corrections, and discoveries.

## When to Use

1. **A command or operation fails unexpectedly** → Log to ERRORS.md
2. **User corrects Claude** ("No, that's wrong...", "Actually...") → Log to LEARNINGS.md
3. **User requests a capability that doesn't exist** → Log to FEATURE_REQUESTS.md
4. **An external API or tool fails** → Log to ERRORS.md
5. **Claude realizes knowledge is outdated/incorrect** → Log to LEARNINGS.md
6. **A better approach is discovered** → Log to LEARNINGS.md

## Log Files

All logs are stored in `.learnings/`:

| File | Purpose |
|------|---------|
| `LEARNINGS.md` | Corrections, discoveries, better approaches |
| `ERRORS.md` | Command failures, exceptions, unexpected behaviors |
| `FEATURE_REQUESTS.md` | Requested capabilities that don't exist |

## Workflow

### 1. Capture a Learning

When you learn something new or are corrected:

```
1. Read the appropriate log file
2. Append the new learning with timestamp
3. Save the file
```

### 2. Review Before Major Tasks

Before starting significant work:

```
1. Read LEARNINGS.md for relevant past discoveries
2. Read ERRORS.md to avoid repeating mistakes
3. Apply lessons learned to current task
```

### 3. Periodic Consolidation

Weekly or monthly:

```
1. Review all logs
2. Extract high-value learnings to MEMORY.md
3. Clear or archive processed entries
```

## Log Format

### LEARNINGS.md

```markdown
## 2026-02-20 - Docker Compose Network Issue

**Context:** User needed to connect containers
**Discovery:** Use `docker network create` + `external: true` in compose
**Correction:** Previously suggested deprecated `--link` flag
**Apply to:** All Docker networking tasks
```

### ERRORS.md

```markdown
## 2026-02-20 - Git Clone Permission Denied

**Command:** `git clone git@github.com:...`
**Error:** Permission denied (publickey)
**Cause:** SSH key not added to GitHub
**Fix:** Use HTTPS instead, or add SSH key
**Prevention:** Check auth before suggesting SSH
```

### FEATURE_REQUESTS.md

```markdown
## 2026-02-20 - Notion Database Query

**Request:** Query Notion database with filters
**Status:** Not implemented
**Priority:** High
**Notes:** Would need Notion integration skill
```

## Integration with MEMORY.md

High-value learnings should be promoted to MEMORY.md:

- Critical fixes that prevent repeat mistakes
- User preferences discovered through corrections
- Tool-specific quirks and workarounds
- Security or safety lessons

## Example Session

**User:** "Actually, use `gh auth login` not `gh auth status`"

**Agent:**
```
1. Read ~/.openclaw/workspace/skills/self-improving-agent/.learnings/LEARNINGS.md
2. Append:
   ## 2026-02-20 - GitHub CLI Auth Correction
   
   **User correction:** Use `gh auth login` not `gh auth status`
   **Context:** When authenticating GitHub CLI
   **Lesson:** `gh auth login` is the interactive flow; `gh auth status` only checks
   **Apply to:** All GitHub CLI auth tasks
3. Write file
4. Respond: "Noted — I'll use `gh auth login` for GitHub CLI authentication going forward."
```

## Best Practices

- **Be specific** — Include full context, not just the correction
- **Tag with dates** — Helps identify stale learnings
- **Link to tasks** — Reference what you were working on
- **Review regularly** — Don't let learnings go to waste
- **Promote to MEMORY.md** — Important ones become long-term memory

## Related Skills

- **agent-autonomy-kit** — Proactive behavior patterns
- **triple-memory-skill** — Persistent memory system
- **flowmind** — Task and goal management
