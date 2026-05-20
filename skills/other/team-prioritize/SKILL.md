---
name: team-prioritize
description: "[Team] Order backlog items using RICE, MoSCoW, or Value-Effort frameworks. Use when prioritizing backlog, ranking features, or ordering work items. Triggers on keywords like "prioritize", "RICE score", "MoSCoW", "rank backlog", "order by value"."
argument-hint: "[rice|moscow|value-effort] [scope:all|sprint|feature-{name}]"
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, TodoWrite
---

# Backlog Prioritization

Order backlog items using data-driven prioritization frameworks.

## When to Use
- Sprint planning needs ordered backlog
- Stakeholder requests priority ranking
- Feature roadmap ordering

## Pre-Workflow

### Activate Skills

- Activate `product-owner` skill for prioritization frameworks (RICE, MoSCoW, Value/Effort)

## Quick Reference

### Frameworks

#### RICE Score
```
Score = (Reach x Impact x Confidence) / Effort

Reach: Users affected per quarter
Impact: 0.25 | 0.5 | 1 | 2 | 3
Confidence: 0.5 | 0.8 | 1.0
Effort: Person-months
```

#### MoSCoW
- **Must Have:** Critical, non-negotiable (release blocker)
- **Should Have:** Important, not vital
- **Could Have:** Nice to have
- **Won't Have:** Out of scope (not this release)

#### Value vs Effort
```
High Value + Low Effort = Quick Wins (do first)
High Value + High Effort = Strategic (plan carefully)
Low Value + Low Effort = Fill-ins (if time permits)
Low Value + High Effort = Time sinks (avoid)
```

### Workflow
1. Read PBIs from `team-artifacts/pbis/`
2. Filter by scope if specified; exclude done/rejected items
3. Apply selected framework
4. Sort by score/classification; assign numeric priority (1 = highest)
5. Update PBI frontmatter priority
6. Output ordered list with scores

### Output
- Priority field: Numeric 1-999 (not High/Med/Low)
- Console: Ordered table with scores

## Report Template

```markdown
## Backlog Priority - {Date}

**Framework:** {framework}
**Scope:** {scope}

| Rank | PBI     | Score   | Rationale |
| ---- | ------- | ------- | --------- |
| 1    | {title} | {score} | {why}     |
```

### Related
- **Role Skill:** `product-owner`

## Example

```bash
/team-prioritize rice
/team-prioritize moscow scope:sprint
```

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
