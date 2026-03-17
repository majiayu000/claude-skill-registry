---
name: ratchet
description: 'Brownian Ratchet progress gates for RPI workflow. Check, record, verify. Triggers: "check gate", "verify progress", "ratchet status".'
---

# Ratchet Skill

Track progress through the RPI workflow with permanent gates.

## The Brownian Ratchet

```
Progress = Chaos × Filter → Ratchet
```

| Phase | What Happens |
|-------|--------------|
| **Chaos** | Multiple attempts (exploration, implementation) |
| **Filter** | Validation gates (tests, /vibe, review) |
| **Ratchet** | Lock progress permanently (merged, closed, stored) |

**Key insight:** Progress is permanent. You can't un-ratchet.

## Execution Steps

Given `/ratchet [command]`:

### status - Check Current State

```bash
ao ratchet status 2>/dev/null
```

Or check the chain manually:
```bash
cat .agents/ao/chain.jsonl 2>/dev/null | tail -10
```

### check [step] - Verify Gate

```bash
ao ratchet check <step> 2>/dev/null
```

Steps: `research`, `plan`, `implement`, `vibe`, `post-mortem`

### record [step] - Record Completion

```bash
ao ratchet record <step> --output "<artifact-path>" 2>/dev/null
```

Or record manually by writing to chain:
```bash
echo '{"step":"<step>","status":"completed","output":"<path>","time":"<ISO-timestamp>"}' >> .agents/ao/chain.jsonl
```

### skip [step] - Skip Intentionally

```bash
ao ratchet skip <step> --reason "<why>" 2>/dev/null
```

## Workflow Steps

| Step | Gate | Output |
|------|------|--------|
| `research` | Research artifact exists | `.agents/research/*.md` |
| `plan` | Plan artifact exists | `.agents/plans/*.md` |
| `implement` | Code + tests pass | Source files |
| `vibe` | /vibe passes | `.agents/vibe/*.md` |
| `post-mortem` | Learnings extracted | `.agents/retros/*.md` |

## Chain Storage

Progress stored in `.agents/ao/chain.jsonl`:
```json
{"step":"research","status":"completed","output":".agents/research/auth.md","time":"2026-01-25T10:00:00Z"}
{"step":"plan","status":"completed","output":".agents/plans/auth-plan.md","time":"2026-01-25T11:00:00Z"}
{"step":"implement","status":"in_progress","time":"2026-01-25T12:00:00Z"}
```

## Key Rules

- **Progress is permanent** - can't un-ratchet
- **Gates must pass** - validate before proceeding
- **Record everything** - maintain the chain
- **Skip explicitly** - document why if skipping a step
