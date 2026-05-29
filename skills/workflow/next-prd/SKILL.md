---
name: next-prd
description: Auto-detect and implement the next PRD in dependency order
---

# Next PRD Skill

Automatically find the next unblocked PRD and begin implementation.

## Workflow

1. **Read status.md**: Load `wiki/status.md` to get the full PRD inventory
2. **Build dependency graph**: Parse the Dependencies column for each PRD
3. **Find next PRD**: Select the first PRD that is:
   - Status is `Draft` (in `wiki/inbox/`)
   - All dependencies are `Completed`
   - Following the implementation order from CLAUDE.md:
     ```
     PRD-001 → 002 → 003 → 004+005 → 006 → 007 → 008 → 009 → 010 → 011+012 → 013 → 014 → 015 → 016
     ```
4. **Move to active**: Use `/move-prd` to move from inbox to active
5. **Read the PRD**: Load the full document
6. **Implement tasks sequentially**: For each task in Section 6:
   - Read the task annotations
   - Implement following constraints
   - Run verification command
   - Move to next task
7. **Check completion**: Run `/check-prd` when all tasks are done
8. **Move to completed**: If all criteria pass, move to completed

## Dependency Resolution

```
If PRD-005 depends on PRD-003:
  - PRD-003 must be "Completed" before PRD-005 can start
  - If PRD-003 is "In Progress", report it and stop
  - If PRD-003 is "Draft", implement it first
```

## Agent Routing

Route tasks to the appropriate specialist agent based on file paths:

| Path Pattern                       | Agent       |
| ---------------------------------- | ----------- |
| `apps/api/`                        | `/backend`  |
| `apps/web/`, `packages/shared/ui/` | `/frontend` |
| `packages/database/`               | `/database` |
| `*test*`, `*.test.*`               | `/testing`  |
| `packages/auth/`, security-related | `/security` |
| `.github/workflows/`, deployment   | `/devops`   |
| `apps/docs/`, `wiki/`, docs        | `/docs`     |

## Output

Report progress after each task:

```markdown
## Next PRD: PRD-NNN — Title

### Progress

- [x] Task 1: Description — DONE
- [x] Task 2: Description — DONE
- [ ] Task 3: Description — IN PROGRESS
- [ ] Task 4: Description — PENDING

### Current: Task 3

Working on: [description of what's being done]
```

## Error Handling

- If no unblocked PRDs exist: Report "All PRDs are either completed or blocked"
- If a task fails verification: Stop and report the failure
- If dependencies are circular: Report the cycle and stop
