---
name: git-commit
description: Commit staged changes with conventional commit message. Use when user says "commit changes", "commit this", "save my changes", or wants to create a git commit.
model: haiku
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash, AskUserQuestion
---

# Git Commit

Create a commit with a conventional commit message based on staged changes. Automatically stages all changes and analyzes the diff to generate an appropriate commit message.

## Workflow

Execute these steps in order.

---

### Step 1: Check Repository State

Check for changes to commit:

```bash
git status --porcelain
```

- If output is empty, report: "Nothing to commit. Working directory is clean." and stop.
- If changes exist, continue to Step 2.

---

### Step 2: Stage All Changes

Stage all changes including untracked files:

```bash
git add .
```

Report: "Staged all changes."

---

### Step 3: Analyze Changes

View the staged diff to understand what changed:

```bash
git diff --cached --stat
```

```bash
git diff --cached
```

Analyze the diff to determine:
- The type of change (feat, fix, docs, refactor, etc.)
- The scope (optional, based on affected files/modules)
- A concise description of what changed

---

### Step 4: Construct Commit Message

Build a conventional commit message following this format:

```
<type>(<optional-scope>): <description>

[optional body]
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Formatting, no code change
- `refactor` - Code restructuring without behavior change
- `test` - Adding or updating tests
- `chore` - Maintenance tasks
- `build` - Build system or dependencies
- `ci` - CI configuration
- `perf` - Performance improvement

**Rules:**
- Use imperative mood ("add" not "added")
- Use lowercase
- No trailing period
- Keep description under 72 characters
- Add a body only for complex changes or breaking changes
- Do NOT add co-author, attribution, or "Generated with" lines

---

### Step 5: Create Commit

Create the commit using a heredoc for proper formatting:

```bash
git commit -m "$(cat <<'EOF'
<commit message here>
EOF
)"
```

---

### Step 6: Handle Result

**On success:**
- Report the commit hash: "Committed: {short_hash} - {message}"

**On pre-commit hook failure:**
- Report: "Pre-commit hook failed. The commit was NOT created."
- Explain what the hook reported
- Instruct: "Fix the issues above and run the commit command again. Do NOT use --amend as that would modify the previous commit."

---

## Error Recovery

If the commit fails:
- **Hook failure**: Fix the reported issues, then stage and commit again (do NOT amend)
- **Unstage changes**: `git reset HEAD` to unstage without losing changes

## Notes

- This command stages ALL changes including untracked files
- Pre-commit hooks run automatically; their failures mean no commit was created
- Always create a NEW commit after hook failure, never amend the previous commit
