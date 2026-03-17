---
name: oracle-incubate
description: Track and nurture knowledge maturation. Use when user mentions "incubate", "mature", "grow knowledge", "promotion", "level up learning". Auto-trigger at end of sessions or when pattern is repeated multiple times.
---

# Oracle Incubate Skill

> Track knowledge as it grows from observation to wisdom

## Purpose

Oracle-incubate monitors knowledge maturation and suggests when learnings are ready to "level up" in the maturity hierarchy.

## Knowledge Maturity Levels

```
🥒 Observation  →  🌱 Learning  →  🌿 Pattern  →  🌳 Principle  →  🔮 Wisdom
     (raw)          (tested)       (repeated)      (universal)      (core)
```

## Proactive Triggers

### MUST Use Incubate When:

**Session End:**
- After significant work session
- After retrospective (rrr)
- User says "wrap up", "end session"

**Pattern Recognition:**
- User says: "this keeps happening", "I always do this"
- User says: "we keep learning this", "another time"
- Same topic appears 3+ times in Oracle

**Promotion Signals:**
- User says: "this is definitely a pattern now"
- User says: "we should remember this"
- User says: "level up", "mature", "promote"

### SHOULD Use Incubate When:

- Reviewing past learnings
- After successful problem resolution
- When consolidating session insights

## Incubation Workflow

### 1. Scan for Maturation Candidates

```javascript
// Search for learnings that might be ready to level up
oracle_search({
  type: "learning",
  limit: 20
})
```

Look for:
- Learnings referenced multiple times
- Learnings proven in different contexts
- Learnings that led to decisions

### 2. Suggest Promotions

Present findings to user:

```markdown
## 🌱 Incubation Report

### Ready for Promotion?

| Learning | Current | Times Used | Suggest → |
|----------|---------|------------|-----------|
| "Always validate webhooks" | 🌱 | 5x | 🌿 Pattern |
| "Subagents for bulk work" | 🌿 | 10x | 🌳 Principle |

### Still Incubating

- "New API auth pattern" (🥒, tested 1x)
- "TypeScript strict mode" (🌱, tested 2x)
```

### 3. Promote with Confidence

```javascript
oracle_learn({
  pattern: "Existing pattern with refinement",
  stage: "pattern",        // promoted from "learning"
  confidence: "high",
  times_validated: 5,
  teachable: true,
  promotion_date: "2026-01-02",
  promoted_from: "learning"
})
```

## Maturity Criteria

| From | To | Criteria |
|------|----|----------|
| 🥒 → 🌱 | Observation → Learning | Worked once, not disproven |
| 🌱 → 🌿 | Learning → Pattern | Used 3+ times, consistent results |
| 🌿 → 🌳 | Pattern → Principle | Context-independent, universally true |
| 🌳 → 🔮 | Principle → Wisdom | Changed behavior fundamentally |

## Dashboard Command

When user asks "show knowledge maturity" or "incubation status":

```markdown
## 🌡️ Knowledge Maturity Dashboard

### By Stage
| Stage | Count | Ready to Promote |
|-------|-------|------------------|
| 🥒 Observations | 15 | 3 (tested once) |
| 🌱 Learnings | 42 | 8 (3+ uses) |
| 🌿 Patterns | 23 | 2 (universal) |
| 🌳 Principles | 12 | 1 (core) |
| 🔮 Wisdom | 5 | - |

### Recent Activity
- 🌱→🌿 "Subagent delegation" promoted (Dec 2025)
- 🥒→🌱 "TypeScript strict mode" validated (Jan 2026)

### Oldest Unreviewed
- "API versioning strategy" (🌱, 45 days)
- "Error boundary pattern" (🌱, 30 days)
```

## Integration with Oracle

| Tool | Incubate Role |
|------|---------------|
| `oracle_learn` | Add maturity metadata when capturing |
| `oracle_search` | Find promotion candidates |
| `oracle_consult` | Consider maturity level in guidance |

## Incubation Prompts

### At Session End
```
"Before we wrap up, let me check Oracle for maturing knowledge..."

[Run incubation scan]

"Found 2 learnings that might be ready to promote. Would you like to review?"
```

### After Multiple Uses
```
"I noticed we've used the 'subagent for bulk work' pattern 5 times now.
Currently marked as 🌱 Learning. Promote to 🌿 Pattern?"
```

### On Manual Request
```
"Showing knowledge maturity dashboard..."
[Display dashboard]
"3 items ready for promotion review."
```

## Future: Automation Hooks

Phase B establishes tracking. Future phases may add:
- Auto-promotion thresholds (3 uses = auto-suggest)
- Maturity decay (unused patterns demote)
- Cross-project pattern detection
- Teaching material generation (Phase C)

## Quick Reference

| User Says | Action |
|-----------|--------|
| "incubation status" | Show dashboard |
| "what's maturing?" | List promotion candidates |
| "promote this to pattern" | Update with oracle_learn |
| "wrap up session" | Run incubation scan |
| "this keeps happening" | Check if pattern exists, suggest capture |
