---
name: evolving-status
description: View Self-Evolving Loop session status, history, and memory metrics
user-invocable: true
---

# Self-Evolving Loop Status

View status, history, and memory metrics for evolving-loop sessions.

---

## Usage

```bash
# Current session status
/evolving-status

# Detailed view
/evolving-status --detailed

# View specific report
/evolving-status --report analysis
/evolving-status --report validation
/evolving-status --report decision
/evolving-status --report learning
/evolving-status --report patterns

# View event history
/evolving-status --history

# View skill evolution
/evolving-status --evolution

# View memory system
/evolving-status --memory

# View tool dependencies
/evolving-status --dependencies
```

---

## Output Example

```
Status:     in_progress
Phase:      EXECUTE
Iteration:  3 / 50
Started:    2026-01-14T12:00:00Z

Request:    Build REST API with user authentication...

Skill Versions:
   executor: v2
   validator: v1
   fixer: v1

Lifecycle Status:
   executor: task-scoped
   validator: task-scoped
   fixer: task-scoped

Task Type: auth (pattern: auth)

Acceptance Criteria:
   [x] AC-F1: GET /users endpoint
   [x] AC-F2: POST /users endpoint
   [ ] AC-F3: Input validation
```

---

## Views

| Flag | Description |
|------|-------------|
| `--detailed` | Full JSON state |
| `--report <type>` | View specific report |
| `--history` | Last 20 events |
| `--evolution` | Skill version history |
| `--memory` | Memory system metrics |
| `--dependencies` | Tool co-usage graph |

---

## Related

- [/evolving-loop](../evolving-loop/SKILL.md) - Main development loop
- [Architecture](../../../docs/EVOLVING-LOOP-ARCHITECTURE.md) - Detailed design
