---
name: commit
description: Guided git commit with atomic commit analysis and conventional commit format
argument-hint: "[--all | --staged | --interactive]"
---

# commit

**Category**: Development

## Usage

```bash
commit [--all | --staged | --interactive]
```

## Arguments

- `--all`: Analyze all uncommitted changes (staged + unstaged)
- `--staged`: Only analyze currently staged changes (default)
- `--interactive`: Guide through staging changes atomically before committing

## Execution Method

This command delegates to the `commit-expert` agent (Haiku model) for fast, cost-effective execution.

**Delegation**: Use the Task tool with:
- `subagent_type`: `"git-workflow:commit-expert"`
- `prompt`: Include the mode (`--staged`, `--all`, or `--interactive`) and current working directory

Example:
```
Task(subagent_type="git-workflow:commit-expert", prompt="Run commit in --staged mode in /path/to/repo")
```

---

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. **Analyze Changes**
   - Run `git status` to understand current state
   - Run `git diff --staged` for staged changes (or `git diff` for all)
   - Identify the files and types of changes

2. **Check for Atomic Commit Violations**
   - Flag if changes span multiple unrelated concerns
   - Warn if mixing features, fixes, refactoring, and style changes
   - Suggest splitting if commit is too large (>300 lines)

3. **Generate Commit Message**
   - Determine appropriate type (feat, fix, docs, etc.)
   - Identify scope from file paths
   - Write clear, imperative description
   - Add body if changes are complex

4. **Present for Approval**
   - Show the proposed commit message
   - Allow editing before committing
   - Execute the commit

## Interactive Flow

### Step 1: Analyze Changes

```
🔍 Analyzing your changes...

Staged changes:
  M  src/auth/login.py (+45, -12)
  M  src/auth/tokens.py (+23, -5)
  A  tests/test_login.py (+89)

Unstaged changes:
  M  src/styles/button.css (+15, -3)
  M  README.md (+20)
```

### Step 2: Atomic Commit Check

```
✅ Good: Changes appear to be a single logical unit
   All changes relate to authentication/login functionality

   OR

⚠️  Warning: Changes may not be atomic

   These appear to be separate concerns:
   1. Authentication changes (src/auth/*)
   2. Style changes (src/styles/button.css)
   3. Documentation (README.md)

   Recommendations:
   - Commit auth changes first: feat(auth): ...
   - Commit style changes: fix(ui): ...
   - Commit docs separately: docs: ...

   Would you like to:
   1. Proceed with current staging (not recommended)
   2. Unstage some files and commit in parts
   3. Show me how to split this commit
```

### Step 3: Generate Commit Message

```
📝 Proposed commit message:

   feat(auth): add JWT refresh token rotation

   Implement automatic token refresh to improve session security.
   Tokens now rotate on each refresh, with old tokens invalidated
   after a 5-minute grace period.

   - Add refresh token rotation logic
   - Update token validation to check rotation status
   - Add tests for token refresh flow

Does this look correct?
   1. Yes, commit with this message
   2. Edit the message
   3. Change the commit type
   4. Cancel
```

### Step 4: Commit Type Selection (if editing)

```
Select commit type:

   1. feat     - New feature
   2. fix      - Bug fix
   3. docs     - Documentation only
   4. style    - Code style (formatting, no logic change)
   5. refactor - Code restructuring (no feature/fix)
   6. perf     - Performance improvement
   7. test     - Adding/fixing tests
   8. build    - Build system or dependencies
   9. ci       - CI/CD configuration
   10. chore   - Maintenance tasks

Current selection: feat

Enter number or type:
```

### Step 5: Scope Selection

```
Suggested scopes based on changed files:
   1. auth (src/auth/*)
   2. api (src/api/*)
   3. No scope

Enter scope or select number: auth
```

### Step 6: Description

```
Write a short description (max 50 chars, imperative mood):

Examples:
   ✅ "add password reset flow"
   ✅ "fix token expiration bug"
   ❌ "added password reset" (past tense)
   ❌ "fixes the token bug" (not imperative)

Description: add JWT refresh token rotation
```

### Step 7: Body (Optional)

```
Add a commit body? (Explain what and why)

   1. Yes, add details
   2. No, subject line is sufficient

[If yes]
Enter commit body (empty line to finish):
> Implement automatic token refresh to improve session security.
> Tokens now rotate on each refresh, with old tokens invalidated
> after a 5-minute grace period.
>
```

### Step 8: Execute Commit

```
📋 Final commit message:

feat(auth): add JWT refresh token rotation

Implement automatic token refresh to improve session security.
Tokens now rotate on each refresh, with old tokens invalidated
after a 5-minute grace period.

Confirm commit? (yes/no/edit): yes

✅ Committed: abc1234
   feat(auth): add JWT refresh token rotation

   3 files changed, 157 insertions(+), 17 deletions(-)
```

## Interactive Staging Mode (--interactive)

When using `--interactive`, guide users through staging atomic commits:

```
🎯 Interactive Atomic Commit Mode

Analyzing all changes to help you create atomic commits...

Found 5 modified files with different concerns:

Group 1: Authentication (recommended first commit)
   M  src/auth/login.py
   M  src/auth/tokens.py
   A  tests/test_login.py

Group 2: UI Fixes
   M  src/styles/button.css

Group 3: Documentation
   M  README.md

Stage Group 1 for commit? (yes/no/show diff): yes

[Stages files, then proceeds to commit flow]
```

## Validation Rules

The command should enforce:

1. **Message Length**
   - Subject: Max 72 characters (warn at 50)
   - Body lines: Max 72 characters

2. **Format**
   - Type is valid conventional commit type
   - Uses imperative mood
   - No period at end of subject

3. **Content Quality**
   - Reject vague messages: "fix", "update", "changes", "WIP"
   - Require specificity: "fix what?", "update what?"

4. **Atomic Check**
   - Warn if >5 files changed
   - Warn if >300 lines changed
   - Warn if multiple file types with different purposes

5. **No AI Tool Attribution**
   - NEVER include "Generated with Claude Code" or similar AI attribution
   - NEVER include "Co-Authored-By: Claude" or any AI co-author footer
   - NEVER include emojis like 🤖 indicating AI generation
   - Commit messages should appear as human-written, professional commits

## Error Handling

```
❌ No changes to commit
   Run `git status` to see the current state.

❌ Commit message too vague
   "fix bug" is not specific enough.
   Please describe what was fixed: "fix(auth): correct token expiration check"

❌ Not in a git repository
   Initialize with `git init` or navigate to a git repository.

⚠️  Unstaged changes will not be included
   Stage with `git add <file>` or use `commit --all`
```

## Quick Commit Shortcuts

For experienced users, support quick patterns:

```bash
# Quick feature commit
commit feat auth "add password reset"

# Quick fix commit
commit fix api "handle null response"

# Quick docs commit
commit docs "update API documentation"
```

## Integration with Git Hooks

Suggest installing hooks for enforcement:

```
💡 Tip: Install git hooks to enforce commit standards automatically.

   Would you like to set up:
   1. commit-msg hook (validate message format)
   2. pre-commit hook (run tests/linting)
   3. Both
   4. Skip for now
```

## Example Outputs

### Simple Commit

```
$ commit

🔍 Analyzing staged changes...

   M  src/utils/helpers.py (+12, -3)

✅ Single file change - good atomic commit

📝 Proposed: fix(utils): handle edge case in date parser

Commit? (yes/edit/cancel): yes

✅ Committed: def4567
```

### Complex Commit Needing Split

```
$ commit --all

🔍 Analyzing all changes...

⚠️  Multiple concerns detected:

   Authentication:
      M  src/auth/login.py
      M  src/auth/session.py

   Unrelated UI fix:
      M  src/components/Header.vue

   Documentation:
      M  docs/API.md

Recommendation: Split into 3 commits

   1. Stage auth files → feat(auth): ...
   2. Stage Header.vue → fix(ui): ...
   3. Stage API.md → docs(api): ...

Would you like help staging these separately? (yes/no)
```
