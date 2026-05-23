---
name: faion-roadmap
user-invocable: false
description: "Analyze progress, reprioritize backlog, add features. Triggers: roadmap, backlog review, progress."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), AskUserQuestion
---

# Roadmap & Backlog Management

**Communication: User's language. Docs: English.**

## When to Use

- After completing features → progress review
- New ideas → add to backlog
- Priorities changed → reprioritize
- Weekly/sprint → roadmap sync

## Pipeline

```
ANALYZE → REVIEW PRIORITIES → ADD FEATURES → UPDATE BACKLOG
```

## Phase 1: Analyze Progress

```bash
# Count features by status
ls aidocs/sdd/{project}/features/done/
ls aidocs/sdd/{project}/features/backlog/
ls aidocs/sdd/{project}/features/*/tasks/done/
```

Report: done, in-progress, backlog counts

## Phase 2: Review Priorities

```python
AskUserQuestion([
    {"question": "Пріоритети актуальні?", "options": [
        {"label": "Так", "description": "Продовжуємо"},
        {"label": "Треба змінити", "description": "Перепріоритизуємо"}
    ]}
])
```

If change needed → reorder features

## Phase 3: Add New Features

For each new idea:
1. Discuss scope via Socratic dialogue
2. Create `backlog/{NN}-{name}/spec.md`
3. Add to roadmap.md

## Phase 4: Update Roadmap

```markdown
# Roadmap: {project}

## Current Sprint
- [ ] {feature} — {status}

## Backlog (prioritized)
1. {NN}-{feature}: {one-liner}
2. ...

## Done
- {NN}-{feature} ✓

## Risks
- {risk}: {mitigation}
```

## Output

Updated `roadmap.md` with priorities, milestones, risks
