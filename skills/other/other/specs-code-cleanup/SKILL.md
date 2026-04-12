---
name: specs-code-cleanup
description: "Provides final code cleanup after task review approval. Removes debug logs, temporary comments, dead code, optimizes imports, and improves readability. Use when asked to clean up code, polish, finalize, tidy up, remove technical debt, or prepare code for completion after review. Not for refactoring logic or fixing bugs—focused solely on cosmetic and hygiene cleanup."
allowed-tools: Task, Read, Write, Edit, Bash, Grep, Glob, TodoWrite, AskUserQuestion
---

# Code Cleanup

## Overview

Performs post-review cosmetic cleanup to make code production-ready. This is the final workflow step after `/specs:task-review` approval.

**Input**: `docs/specs/[id]/tasks/TASK-XXX.md` (reviewed status)  
**Output**: Cleaned code, task marked `completed`

## When to Use

- Use when asked to clean up code, polish, finalize, tidy up, or remove technical debt after review approval.
- Use to prepare code for completion: remove debug logs, dead code, optimize imports, and improve readability.
- Use as the final quality gate in the specification-driven development workflow.
- Not for refactoring logic or fixing bugs — focused solely on cosmetic and hygiene cleanup.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--lang` | No | `java`, `spring`, `typescript`, `nestjs`, `react`, `python`, `general` |
| `--task` | Yes | Path to task file |

## Best Practices

- **Clean, not change**: Only remove or reorganize — never change functionality
- **Preserve behavior**: Code must work exactly the same after cleanup
- **Use project tools**: Prefer `./mvnw spotless:apply`, `npm run lint:fix`, `black`, etc.
- **Use TodoWrite**: Track progress through all 8 phases
- **Stop on failure**: If tests fail, stop and report — do not proceed

See `references/language-patterns.md` for language-specific formatter commands, import ordering, and grep patterns.

## Instructions

### Phase 1: Task Verification

1. Parse `$ARGUMENTS` for parameters:
   - `--lang` (optional): Target language/framework
   - `--task` (required): Task ID or file path
   - `--spec` (optional): Spec folder path (used with task ID)
   
   **Support two formats**:
   - Format 1 (direct path): `--task=docs/specs/001-feature/tasks/TASK-001.md`
   - Format 2 (spec+task): `--spec=docs/specs/001-feature --task=TASK-001`
   
   If Format 2 is used, construct the task file path as: `{spec}/tasks/{task}.md`

2. Read the task file. Verify:
   - Status is `reviewed` or `implemented` (not `completed`)
   - Review report `TASK-XXX--review.md` exists and is approved
3. If not reviewed → stop and tell user to run `/specs:task-review` first
4. Extract task ID, title, and `provides` files

### Phase 2: Identify Files to Clean

1. Read `TASK-XXX--review.md` for files created/modified
2. Read task `provides` field for file paths
3. Verify files exist; build cleanup list
4. Categorize: source files, test files, config files

### Phase 3: Technical Debt Removal

Search files for temporary/debug artifacts with Grep:
- `console.log`, `System.out.println`, `print(`, `// DEBUG:`, `// temp`, `// hack`
- Resolved `TODO`/`FIXME` comments (keep unresolved ones)

Review context for each finding. Remove confirmed debt and document what was removed.

### Phase 4: Import Optimization

1. Run language-specific import optimizer if available (see references)
2. Manually remove unused imports if no tool exists
3. Document files changed

### Phase 5: Code Readability Improvements

1. Run language-specific formatter if available (see references)
2. If no formatter: fix indentation, break long lines (>120), fix spacing
3. Remove dead code only if obviously safe
4. Document changes

### Phase 6: Documentation Verification

1. Verify class/file headers and public API docs
2. Check remaining TODOs are still valid and have context
3. Remove or update outdated comments
4. Document documentation changes

### Phase 7: Final Verification

1. Run linters if available
2. Run tests if available
3. Verify no logic or signature changes were introduced
4. If tests fail → stop and report failures

### Phase 8: Task Completion

1. **Auto-update task status**:
   - Add a `## Cleanup Summary` section to the task file
   - Check any remaining boxes in the DoD section
   - Hooks automatically update status to `completed` and set `completed_date` + `cleanup_date`
   
2. Append `## Cleanup Summary` to task file with:
   - Files cleaned
   - Changes made
   - Verification checklist (linters, tests, no functionality changes)
3. Mark all todos complete

## Examples

### Spring Boot Cleanup

```bash
/developer-kit-specs:specs-code-cleanup --lang=spring --task="docs/specs/001-user-auth/tasks/TASK-001.md"
```

Actions:
1. Verify TASK-001 status is `reviewed`
2. Files: `UserController.java`, `UserService.java`, `UserRepository.java`
3. Remove 5 `System.out.println` and 2 resolved TODOs
4. Run `./mvnw spotless:apply`
5. Run `./mvnw test -q`
6. Mark task `completed`

### TypeScript Cleanup

```bash
/developer-kit-specs:specs-code-cleanup --lang=typescript --task="docs/specs/002-dashboard/tasks/TASK-003.md"
```

Actions:
1. Verify TASK-003 status is `reviewed`
2. Files: `Dashboard.tsx`, `useDashboard.ts`, `Dashboard.test.tsx`
3. Remove 8 `console.log` statements
4. Run `npm run lint:fix` and `npm run format`
5. Run `npm test`
6. Mark task `completed`

## Constraints and Warnings

- Never change logic or signatures during cleanup
- Stop immediately and report if tests fail
- Verify behavior is unchanged before marking complete
