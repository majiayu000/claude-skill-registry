---
name: implement-task
description: Implement a specific task from a PRD following its annotations
---

# Implement Task Skill

Implement a specific task from a PRD's Implementation Plan (Section 6).

## Arguments

The user provides:

- PRD number (e.g., `PRD-005`) or path
- Task number (e.g., `Task 3`)

If not given, ask which PRD and task to implement.

## Workflow

1. **Locate PRD**: Find the file in `wiki/inbox/`, `wiki/active/`, or `wiki/completed/`
2. **Read Section 6**: Find the task table and Claude Code Task Annotations
3. **Read annotations**: Extract Context needed, Constraints, Done state, Verification command
4. **Read context files**: Read every file listed in "Context needed"
5. **Check dependencies**: Ensure dependent tasks are completed
6. **Implement**: Follow the constraints strictly
7. **Verify**: Run the verification command
8. **Report**: State what was done and verification results

## Annotation Format

Each task annotation looks like:

```markdown
**Task N (Name)**:

- **Context needed**: [files to read]
- **Constraints**: [what NOT to do]
- **Done state**: [completion criteria]
- **Verification command**: [shell command]
```

## Implementation Rules

- **Read ALL context files** before writing any code
- **Follow ALL constraints** — they exist for a reason
- **Check dependencies** — don't implement Task 3 if Task 2 isn't done
- **Match existing patterns** — read reference files and follow conventions
- **Run verification** — the task isn't done until the command passes

## After Implementation

- If the task is the last one in the PRD, suggest running `/check-prd` to verify all success criteria
- If the PRD is in `wiki/inbox/`, suggest moving it to `wiki/active/` with `/move-prd`

## Common Verification Commands

| Command                   | What it checks                   |
| ------------------------- | -------------------------------- |
| `bun turbo type-check`    | TypeScript across all workspaces |
| `bun turbo lint`          | ESLint across all workspaces     |
| `bun test --cwd apps/api` | API tests                        |
| `bun test --cwd apps/web` | Web tests                        |
| `bun turbo build`         | Full build                       |
| `bun turbo test`          | All tests                        |

## Error Handling

If the verification command fails:

1. Read the error output carefully
2. Fix the issue
3. Re-run verification
4. If stuck, report what failed and suggest next steps
