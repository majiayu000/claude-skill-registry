---
name: decisions
description: Load past architectural decisions. Use when making new decisions to ensure consistency.
allowed-tools: Read, Glob
---

# Decisions Skill

Understanding and respecting past decisions.

## When to Load This Skill

- Making architectural decisions
- Choosing between approaches
- Questioning existing patterns

## Decision Records

@memory/knowledge/decisions/

Each decision file contains:
- Context: Why decided
- Options: What was considered
- Decision: What was chosen
- Rationale: Why chosen
- Consequences: What follows

## How to Use

### Before Making a Decision

1. Check if similar decision exists:
```
Glob("memory/knowledge/decisions/*.json")
```

2. If exists:
   - Read the decision
   - Understand the rationale
   - Either follow or document why diverging

3. If not exists:
   - Make and document the decision

### Recording a Decision

```json
{"knowledge_updates":[{"category":"decision","content":"Decision: Use X over Y | Context: Needed to solve Z | Rationale: X better because...","confidence":"certain"}]}
```

## Decision Format

```json
{"id":"DEC-001","title":"Short title","date":"YYYY-MM-DD","status":"accepted|deprecated|superseded","context":"Why this decision was needed","options":[{"option":"Option A","pros":["list"],"cons":["list"]},{"option":"Option B","pros":["list"],"cons":["list"]}],"decision":"Which was chosen","rationale":"Why this option","consequences":["What follows"]}
```
