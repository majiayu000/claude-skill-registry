---
name: dapp-sdd:tasks
description: Use when generating a task list from an implementation plan, with checkboxes and review tasks.
---

# Tasks Skill

Generates a dependency-ordered task list from the implementation plan.

## Input

- `.dapp-sdd/plan.md` - The phased implementation plan
- `.dapp-sdd/spec.md` - The specification (for reference)

## Output

A task list saved to `.dapp-sdd/tasks.md` with:
- Checkboxes for tracking completion
- Task IDs for reference
- Review tasks at phase boundaries
- Commit tasks after each item

## Task Format

```markdown
# {DApp Name} Tasks

## Phase 1: Project Setup

- [ ] T001 Verify create-mn-app scaffold is complete
- [ ] T002 Configure ESLint with strict rules
- [ ] T003 Configure Prettier for formatting
- [ ] T004 Verify TypeScript strict mode enabled
- [ ] T005 Add `.dapp-sdd/` to `.gitignore`
- [ ] T006 [REVIEW] Run phase 1 code reviews

## Phase 2: Contract Implementation

- [ ] T007 Create contract skeleton `contracts/{name}.compact`
- [ ] T008 Define ledger state variables
- [ ] T009 Implement circuit `{circuit_name}`
- [ ] T010 Add witness functions
- [ ] T011 Verify contract compiles: `compact compile`
- [ ] T012 [REVIEW] Run phase 2 code reviews

## Phase 3: TypeScript Integration

- [ ] T013 Create deployment script `src/deploy.ts`
- [ ] T014 Create CLI interface `src/cli.ts`
- [ ] T015 Configure providers in `src/providers/`
- [ ] T016 Verify TypeScript compiles: `tsc --noEmit`
- [ ] T017 [REVIEW] Run phase 3 code reviews

## Phase 4: Testing

- [ ] T018 Write contract unit tests
- [ ] T019 Write integration tests
- [ ] T020 Verify all tests pass: `npm test`
- [ ] T021 [REVIEW] Run phase 4 code reviews

## Phase 5: Documentation & Polish

- [ ] T022 Update README with usage instructions
- [ ] T023 Add educational comments to contract
- [ ] T024 Add educational comments to TypeScript
- [ ] T025 Final code cleanup
- [ ] T026 [REVIEW] Run final code reviews
- [ ] T027 [COMPLETE] Post completion summary to PR
```

## Task Types

| Prefix | Meaning |
|--------|---------|
| (none) | Regular implementation task |
| `[REVIEW]` | Review gate - run both reviewers |
| `[COMPLETE]` | Final task - post to PR and mark ready |

## Process

1. Load plan from `.dapp-sdd/plan.md`
2. Extract tasks from each phase
3. Assign sequential task IDs (T001, T002, ...)
4. Add review tasks at end of each phase
5. Add completion task at very end
6. Save to `.dapp-sdd/tasks.md`

## Task Execution Notes

When executing tasks:
- Each task gets committed and pushed after completion
- Use `git-lovely:useful-commits` for commit messages
- Review tasks invoke both reviewers with pragmatic instructions
- Quality checks run before every commit
