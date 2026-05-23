---
name: handoff
description: Use handoff tools for session continuity. Create handoffs at end of session, read handoffs at start, search past handoffs for context. Trigger words - "handoff", "end session", "wrap up", "continue from", "where we left off", "context high", "running low", "before I forget".
---

# Handoff Skill

> "Session continuity through structured handoffs"

## Proactive Triggers

### MUST Create Handoff When:
- Context > 80% and significant work done
- User says: "wrap up", "end session", "that's all", "done for now"
- User says: "before I forget", "note this down"
- Session has 3+ commits without handoff today

### SHOULD Read Handoff When:
- Session starts and recent handoff exists
- User says: "where were we", "continue from", "last time"
- User references previous work

### SHOULD Search Handoffs When:
- User asks about past work on a topic
- User says: "did we work on", "when did we", "find the handoff"

## Tool Usage

### handoff_create
```javascript
handoff_create({
  done: ["Completed X", "Fixed Y"],
  pending: ["Test X", "Review Y"],
  context: "Branch: feature/x, Issue: #123",
  title: "Feature X Progress",
  context_percent: 85
})
```

### handoff_read
```javascript
handoff_read({ limit: 1 })  // Latest
handoff_read({ limit: 3 })  // Recent 3
```

### handoff_search
```javascript
handoff_search({
  query: "authentication",
  limit: 5
})
```

## Commands Available

| Command | Action |
|---------|--------|
| `/handoff` | Create handoff interactively |
| `/handoff-read` | Read latest handoff |
| `/handoff-search [query]` | Search past handoffs |
| `/handoff-help` | Show all options |

## Integration Map

```
┌──────────────────────────────────────────┐
│            Session Lifecycle              │
├──────────────────────────────────────────┤
│ START → handoff_read (auto via hook)     │
│                                          │
│ WORK  → claude-mem (auto via worker)     │
│       → Oracle (consult for decisions)   │
│                                          │
│ END   → handoff_create (manual/reminder) │
└──────────────────────────────────────────┘
```

| System | Question | Auto |
|--------|----------|------|
| **handoff** | "Where were we?" | Hook on start |
| **claude-mem** | "What happened?" | Background worker |
| **Oracle** | "What should I do?" | On-demand |

## Quick Reference

| Context | Action |
|---------|--------|
| High context (>80%) | Prompt to create handoff |
| No handoff today + commits | Reminder on Stop |
| User asks about past | Search handoffs |
| Session start | Auto-show latest handoff |
