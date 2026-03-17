---
name: dev-workflow-prepare-commit
description: Prepare code for commit with quality checks and conventional commit message generation. Use when the user asks to prepare a commit, review changes before committing, or wants a thorough pre-commit check including lint, tests, and code review.
---

# Prepare Commit

Thoroughly prepare and validate changes before creating a commit.

## Workflow

### Step 1: Check for Unstaged Changes

```bash
git status
```

**If there are unstaged changes:**

**ALWAYS use the AskQuestion tool** to prompt the user. Show the user which files are unstaged, then use AskQuestion:

- Title: "Unstaged Changes Detected"
- Question: "The following files have unstaged changes: [list files]. Are these intentionally left unstaged?"
- Options:
  - id: "leave", label: "Yes, leave them unstaged"
  - id: "stage", label: "No, stage all changes"
  - id: "review", label: "Let me review"

Based on the response:

- "leave" → Continue to Step 2
- "stage" → Run `git add -A` then continue
- "review" → Show the diff and wait for guidance

### Step 2: Review Staged Changes for Best Practices

```bash
git diff --staged
```

Review all staged changes and check for:

- **Code quality**: Clean, readable code following project conventions
- **Security**: No hardcoded secrets, API keys, or credentials
- **Debug artifacts**: No `console.log`, `debugger`, or commented-out code that shouldn't be committed
- **Completeness**: No TODO comments for things that should be done now
- **Test coverage**: Changes should have corresponding tests if applicable

**If issues are found:**

Categorize issues by severity:

- **Critical issues**: Security concerns (hardcoded secrets, API keys, credentials), sensitive data exposure
- **Minor issues**: Extra blank lines, console.log statements, debugger statements, minor formatting issues, TODO comments

Report each issue clearly with file, line reference, and severity.

**For critical issues only:**

**ALWAYS use the AskQuestion tool:**

- Title: "Critical Issues Found"
- Question: "Found critical security/data issues that should not be committed: [list issues]. How would you like to proceed?"
- Options:
  - id: "fix", label: "Fix the issues"
  - id: "abort", label: "Abort"

Do NOT offer "Proceed anyway" for critical issues.

Based on the response:

- "fix" → Fix each issue, then re-run this step
- "abort" → Stop the workflow

**For minor issues only (or after critical issues are resolved):**

**ALWAYS use the AskQuestion tool:**

- Title: "Minor Issues Found"
- Question: "Found the following minor issues in staged changes:\n\n[list issues]\n\nWould you like me to fix these?"
- Options:
  - id: "fix", label: "Yes, fix them"
  - id: "proceed", label: "No, proceed anyway"
  - id: "review", label: "Let me review first"
  - id: "abort", label: "Abort"

Based on the response:

- "fix" → Fix each minor issue automatically, then re-run this step
- "proceed" → Continue to Step 3 without fixing
- "review" → Show detailed diff of proposed fixes before applying
- "abort" → Stop the workflow

### Step 3: Run Linter

```bash
npm run lint
```

**If lint errors exist:**

**ALWAYS use the AskQuestion tool:**

- Title: "Lint Errors Found"
- Question: "Linting found errors: [summary of errors]. How would you like to proceed?"
- Options:
  - id: "auto", label: "Fix automatically"
  - id: "manual", label: "Fix manually"
  - id: "proceed", label: "Proceed anyway (not recommended)"
  - id: "abort", label: "Abort"

Based on the response:

- "auto" → Run `npm run lint -- --fix` and re-check
- "manual" → Fix each error, then re-run lint
- "proceed" → Continue to Step 4 (not recommended)
- "abort" → Stop the workflow

### Step 4: Run Tests

Use the unit-test-runner subagent to run tests, or run directly:

```bash
npm test
```

**If tests fail:**

**ALWAYS use the AskQuestion tool:**

- Title: "Test Failures"
- Question: "Some tests are failing: [summary of failures]. How would you like to proceed?"
- Options:
  - id: "fix", label: "Fix the tests"
  - id: "abort", label: "Abort"

Do NOT proceed with failing tests unless explicitly overridden by the user.

Based on the response:

- "fix" → Investigate and fix failing tests, then re-run
- "abort" → Stop the workflow

### Step 5: Generate Commit Message

Analyze the staged changes to create a conventional commit message.

```bash
git diff --staged --stat
git diff --staged
```

**Conventional Commits Format:**

```
<type>: <short description>
```

**Types:**
| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Build, config, or tooling changes |

**Guidelines:**

- Keep the message short and focused on the main idea
- Maximum 80 characters total
- Do NOT include scope in parentheses (no `feat(auth):`, just `feat:`)
- Use imperative mood ("add feature" not "added feature")
- Focus on the "what" at a high level, not implementation details
- **NEVER add co-author trailers** - no `Co-authored-by:` lines of any kind

**Examples:**

- `refactor: migrate queries to suspense`
- `feat: add dark mode toggle`
- `fix: resolve login redirect loop`

### Step 6: Confirm and Commit

**ALWAYS use the AskQuestion tool** to present the generated commit message:

- Title: "Confirm Commit Message"
- Question: "Ready to commit with this message:\n\n[generated message]\n\nProceed?"
- Options:
  - id: "commit", label: "Commit"
  - id: "edit", label: "Edit message"
  - id: "abort", label: "Abort"

Based on the response:

- "commit" → Execute the commit
- "edit" → Ask user for modifications, then commit
- "abort" → Stop without committing

**Execute the commit:**

> **CRITICAL: NO CO-AUTHOR TRAILERS**
>
> Do NOT add any `Co-authored-by` trailers to the commit. The commit message must contain ONLY the type and short description - nothing else. No trailers, no co-author attribution, no additional metadata.

```bash
git commit -m "<type>: <short description>"
```

- Use ONLY the `-m` flag
- Do NOT use `--trailer`
- Do NOT use `--author`
- Do NOT append any `Co-authored-by:` lines
- The message should be exactly: `<type>: <short description>`

**Verify success:**

```bash
git status
git log -1 --oneline
```

Confirm the commit was created successfully.

### Step 7: Offer to Push

After a successful commit, **ALWAYS use the AskQuestion tool:**

- Title: "Push Changes?"
- Question: "Commit created successfully. Would you like to push to remote?"
- Options:
  - id: "push", label: "Yes, push now"
  - id: "later", label: "No, I'll push later"

Based on the response:

- "push" → Run `git push` and confirm success
- "later" → End the workflow

**If pushing:**

```bash
git push
```

Confirm the push was successful and show the remote branch status.

## Early Exit Conditions

Stop the workflow immediately if:

- User chooses "Abort" at any step
- Tests fail and user doesn't want to fix them
- Critical security issues are found in staged changes (e.g., API keys)

## Notes

- This skill focuses on preparing a single, high-quality commit
- Optionally pushes to remote after commit if user confirms
- Always respect user choices at each confirmation step
