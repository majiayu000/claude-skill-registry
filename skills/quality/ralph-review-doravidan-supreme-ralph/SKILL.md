---
name: ralph-review
description: Review RALPH worktree changes before merging
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
---

# RALPH-REVIEW - Review Worktree Changes

Review all changes made in a RALPH worktree before merging to main.

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-review` | Review current/only worktree |
| `/ralph-review {spec-name}` | Review specific worktree |
| `/ralph-review --full` | Show full diff (not just stats) |
| `/ralph-review --files` | List changed files only |

## Triggers

- `/ralph-review`
- "review worktree"
- "show ralph changes"
- "review before merge"

## Process

### Step 1: Select Worktree

If multiple worktrees exist:

```
? Which worktree do you want to review?
  ○ ralph/user-authentication (4 commits, 12 files)
  ○ ralph/payment-integration (2 commits, 5 files)
```

### Step 2: Show Overview

```
╔════════════════════════════════════════════════════════════════╗
║                    Worktree Review                              ║
║                    ralph/user-authentication                    ║
╚════════════════════════════════════════════════════════════════╝

Worktree Path: .worktrees/user-authentication
Branch: ralph/user-authentication
Base: main (diverged 4 commits ago)

PRD Progress:
  ✓ US-001: Create User model (complete)
  ✓ US-002: Password hashing (complete)
  ○ US-003: JWT utilities (pending)
  ○ US-004: Auth routes (pending)

Commits: 4
  abc1234 feat: ST-001-1 - Create User type definitions
  def5678 feat: ST-001-2 - Create Zod validation schema
  ghi9012 feat: ST-001-3 - Create User service layer
  jkl3456 feat: ST-001-4 - Add unit tests
```

### Step 3: File Summary

```
Files Changed: 12

New files (8):
  + src/types/user.ts
  + src/schemas/user.schema.ts
  + src/services/user.service.ts
  + tests/services/user.service.test.ts
  + src/utils/password.ts
  + src/utils/jwt.ts
  + tests/utils/password.test.ts
  + tests/utils/jwt.test.ts

Modified files (4):
  ~ src/types/index.ts (+2 -0)
  ~ src/services/index.ts (+1 -0)
  ~ src/utils/index.ts (+2 -0)
  ~ package.json (+2 -0)

Diff stats:
  +342 lines added
  -12 lines removed
```

### Step 4: Quality Status

```
Quality Gates (in worktree):
  ✓ Typecheck: passed
  ✓ Lint: passed (0 warnings)
  ✓ Tests: passed (8 new, 42 total)

Code Coverage:
  Statements: 87% (+3%)
  Branches: 82% (+5%)
  Functions: 91% (+2%)
  Lines: 87% (+3%)
```

### Step 5: Detailed Review Options

```
? What would you like to review?
  ○ Show full diff (all changes)
  ○ Review specific file
  ○ Show commit details
  ○ Run tests again
  ○ Continue to merge (/ralph-merge)
  ○ Done reviewing
```

### Full Diff Mode

With `/ralph-review --full`:

```bash
# Show diff against main
git diff main...ralph/{spec-name}
```

Output:

```diff
diff --git a/src/types/user.ts b/src/types/user.ts
new file mode 100644
--- /dev/null
+++ b/src/types/user.ts
@@ -0,0 +1,15 @@
+export interface User {
+  id: string;
+  email: string;
+  passwordHash: string;
+  createdAt: Date;
+  updatedAt: Date;
+}
+
+export interface CreateUserInput {
+  email: string;
+  password: string;
+}
...
```

### Review Specific File

```
? Which file do you want to review?
  ○ src/types/user.ts (new, +15 lines)
  ○ src/schemas/user.schema.ts (new, +42 lines)
  ○ src/services/user.service.ts (new, +87 lines)
  ○ src/types/index.ts (modified, +2 lines)
```

Show the selected file diff with context.

## Output Format

```
╔════════════════════════════════════════════════════════════════╗
║                    Review Summary                               ║
╚════════════════════════════════════════════════════════════════╝

Worktree: ralph/user-authentication
Status: Ready to merge

Summary:
  - 4 commits with clear messages
  - 12 files changed (8 new, 4 modified)
  - All quality gates passing
  - 8 new tests added
  - Code coverage improved

Recommendations:
  ✓ Changes look good to merge
  ⚠ Consider adding integration tests

Actions:
  /ralph-merge    - Merge to main
  /ralph-discard  - Abandon changes
```

## Warnings

Show warnings for potential issues:

```
⚠ Warnings:

1. Large commit detected:
   ghi9012 (+87 lines) - Consider splitting in future

2. Missing test coverage:
   src/utils/jwt.ts - verifyToken() not tested

3. TODO comments found:
   src/services/user.service.ts:45 - TODO: Add rate limiting
```

## Error Handling

| Error | Action |
|-------|--------|
| No worktrees | Direct to `/ralph-run` |
| Worktree not found | List available worktrees |
| Main branch ahead | Warn about potential conflicts |
