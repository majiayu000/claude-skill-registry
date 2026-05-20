---
name: dapp-sdd:implement
description: Use when executing implementation tasks with commits after each task and reviews after each phase.
---

# Implement Skill

Executes the task list autonomously with quality gates.

## Input

- `.dapp-sdd/tasks.md` - Task list with checkboxes
- `.dapp-sdd/plan.md` - Implementation plan (for context)
- `.dapp-sdd/spec.md` - Specification (for requirements)
- `.dapp-sdd/pr-context.json` - PR metadata

## Process

### For Each Task

1. **Read task** from `.dapp-sdd/tasks.md`
2. **Execute task** using appropriate skills:
   - Contract work → `compact-core:*` skills
   - TypeScript work → standard development
   - Documentation → `readme-and-co:documentation-standards`
3. **Run quality checks:**
   ```bash
   npm run lint
   npm run format:check
   tsc --noEmit
   compact compile contracts/*.compact
   ```
4. **Fix any issues** (zero tolerance policy)
5. **Commit and push:**
   - Use `git-lovely:useful-commits` for message
   - `git add .`
   - `git commit -m "{message}"`
   - `git push`
6. **Mark task complete** in `.dapp-sdd/tasks.md`
7. **Update state** in `.dapp-sdd/pr-context.json`

### For Review Tasks

When encountering a `[REVIEW]` task:

1. **Run Compact review** (if contracts exist):
   ```
   Use compact-reviewer:compact-reviewer agent

   Context: "You are reviewing an example dApp for the Midnight Network.
   This project is intended to demonstrate concepts to developers learning Midnight.

   Be pragmatic with suggestions:
   - Focus on correctness and clarity over production concerns
   - Flag anything that would confuse learners
   - Flag bad practices that learners might copy
   - Accept reasonable shortcuts that keep the example focused
   - Ensure educational comments are accurate"
   ```

2. **Run TypeScript review:**
   ```
   Use devs:code-reviewer agent

   Context: "You are reviewing an example dApp for the Midnight Network.
   This project is intended to demonstrate concepts to developers learning Midnight.

   Be pragmatic with suggestions:
   - Focus on correctness and clarity over production concerns
   - Flag anything that would confuse learners
   - Flag bad practices that learners might copy
   - Accept reasonable shortcuts that keep the example focused
   - Ensure educational comments are accurate"
   ```

3. **Address all issues** raised by either reviewer
4. **Commit fixes** with appropriate message
5. **Mark review complete** in tasks.md

### For Completion Task

When encountering the `[COMPLETE]` task:

1. **Generate summary:**
   - Count completed user stories
   - Count completed tasks
   - List key files created/modified

2. **Post to PR:**
   ```bash
   gh pr comment {prNumber} --body "## Implementation Complete

   ### Summary
   - User Stories: {X} completed
   - Tasks: {Y} completed
   - Phases: {Z} reviewed

   ### Key Files
   - `contracts/{name}.compact` - Smart contract
   - `src/deploy.ts` - Deployment script
   - `src/cli.ts` - CLI interface

   ### Quality
   - All linting checks pass
   - All formatting checks pass
   - All TypeScript checks pass
   - All Compact compilation passes
   - All tests pass

   Ready for final review!"
   ```

3. **Mark PR ready:**
   ```bash
   gh pr ready {prNumber}
   ```

## State Tracking

Update `.dapp-sdd/pr-context.json` after each task:
```json
{
  "owner": "...",
  "repo": "...",
  "branch": "...",
  "prNumber": 42,
  "currentPhase": 2,
  "completedTasks": ["T001", "T002", "T003"],
  "status": "implementing"
}
```

## Error Handling

If a task fails:
1. Log the error
2. Attempt to fix automatically
3. If cannot fix, stop implementation
4. Post error summary to PR as comment
5. Update status to "blocked" in pr-context.json
