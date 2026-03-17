---
name: gtd
description: Autonomous task execution from GTD.md items. Use when processing GTD tasks, call prep, outreach, or podcast preparation.
---

# GTD Runner Skill

Autonomous task execution from GTD.md items.

## Trigger

- Command: `/cyber-gtd`
- Default: plan-first (show before execute)

## Workflow

1. Read `@GTD.md` → extract items from `# Next`
2. For each item:
   - Classify → match pattern to workflow
   - Lookup entities via database: `bun scripts/db/query.ts find-entity "<name>"`
   - Plan actions
3. Show plan → ask to execute
4. Execute approved items sequentially (one at a time)
5. Output: `~/CybosVault/private/content/work/MMDD-<slug>.md`

## Classification → Routing

| Pattern | Confidence | Workflow |
|---------|------------|----------|
| "ask for call", "message", "email", "reach out" | High | → workflows/outreach.md |
| "call with", "meeting", "X <> Y", "sync" | High | → workflows/call-prep.md |
| "podcast" | High | → workflows/podcast.md |
| company name, "research", "DD", "look into" | Medium | → workflows/research.md |
| **no match** | Low | Best judgment → log to learnings.md |

## Entity Lookup

Query database for entity context:

1. Parse item for names (people, companies)
2. Run: `bun scripts/db/query.ts find-entity "<name>" --json`
3. If found, get full context: `bun scripts/db/query.ts entity <slug> --json`
4. Entity context includes:
   - Recent interactions (calls, emails, telegram)
   - Deal associations
   - Pending items
5. If not found + confident it's an entity:
   - High confidence (company with domain) → auto-create stub
   - Medium confidence → ask: "Create entity file for X?"

## Output Format

All outputs to `~/CybosVault/private/content/work/MMDD-<slug>.md`:

```markdown
# Task: [Task Description]

**Status:** Pending Approval | Completed | Incomplete
**Created:** YYYY-MM-DD HH:MM
**GTD Item:** [Original text from GTD.md]
**Workflow:** [Which workflow handled this]

---

## Context

**Entity:** [Name]
- Type: [person/org]
- Deal: [link if exists]
- Previous calls: [N calls found]

**Key Info:**
[Relevant context from calls, deals, entity files]

---

## Draft

[Message/agenda/questions/etc]

---

## Pending Actions

- [ ] Send via Gmail to email@example.com
- [ ] Alternative: Telegram @handle

---

## Execution Log

- HH:MM - [action taken]
```

## Staged Execution

Agent completes what it can autonomously:
- Research and context gathering
- Draft creation
- Preparation work

Then queues actions requiring approval:
- Sending messages (Gmail, Telegram)
- Scheduling meetings
- Any external action

## Suggestions

When processing tasks, if you notice 3+ similar patterns that don't have
a dedicated workflow, suggest: "I've seen '[pattern]' multiple times.
Want me to create a workflow for it?"

## Self-Improvement

Log all task executions to `@learnings.md` for pattern analysis.
