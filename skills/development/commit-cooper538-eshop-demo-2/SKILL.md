---
name: commit
description: Create a git commit following the project's versioning guidelines with phase/task format. Use when user wants to commit changes or runs /commit.
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
---

# Smart Commit Helper

Create properly formatted git commits following the project's commit convention.

## Usage

```
/commit                          # Interactive mode
/commit fix                      # Force type to "fix"
/commit feat add user auth       # Type + description
/commit --meta                   # Use [00-00] prefix for meta changes
```

## Commit Convention
```
[XX-YY] <type>: <description>
```
Where XX = phase number, YY = task number (e.g., `[01-02]` = Phase 1, Task 2)

### Meta Commits [00-00]
Use `--meta` flag for changes that are NOT part of any specific task:
- New project specifications
- Task/phase restructuring
- Workflow tooling changes
- Documentation about work organization

Meta commits ALWAYS use the format `[00-00] meta: <description>` - the type is always `meta`.

## Current State

Staged changes:
!git diff --cached --stat

Current branch:
!git branch --show-current

Recent commits (for style reference):
!git log --oneline -5

## Process

### Step 1: Verify Staged Changes

First, check if there are staged changes using `git diff --cached --stat`.

If nothing is staged:
- Show unstaged changes with `git status`
- Ask the user if they want to stage all changes or specific files
- Stage the requested files before proceeding

### Step 2: Detect or Prompt for Phase and Task Numbers

**Check for `--meta` flag first**: If `$ARGUMENTS` contains `--meta`, use `[00-00] meta:` format and skip Steps 2 and 3 (phase/task detection and type detection).

Otherwise, try to auto-detect from (in order):
1. **Branch name** (if not on main): Look for patterns like `phase-01/task-02`, `01-02`
2. **Task files**: Find task with `🔵 in_progress` status in `specification/phase-*/tasks/`
3. **Recent commits**: Check if recent commits follow the `[XX-YY]` format and extract the latest

If detection fails, use AskUserQuestion:
- Ask for phase number (e.g., "01", "02")
- Ask for task number (e.g., "01", "02", "03")

### Step 3: Auto-Detect Commit Type

Analyze the staged diff to determine the type:

| Type | Detection Rules |
|------|----------------|
| `docs` | ALL changed files are `.md`, `.txt`, or XML doc comments only |
| `fix` | Changes contain bug fix patterns, corrections to existing logic |
| `feat` | New files created, new functions/classes/endpoints added (default) |

Present the detected type and allow user to override if they disagree.

### Step 4: Generate Commit Description

Based on the diff analysis, generate a concise description that:
- Describes WHAT changed (not HOW)
- Uses imperative mood ("add", "fix", "update", "implement")
- Stays under 50 characters
- Is specific and meaningful

### Step 5: Summarize Changes and Wait for Approval

**IMPORTANT**: Before committing, ALWAYS present a summary and wait for explicit user approval.

Display to the user:
1. **Staged files** - list of files that will be committed
2. **Change summary** - brief description of what changed (new files, modified logic, etc.)
3. **Proposed commit message** - the full commit message including `[XX-YY] type: description`

Then use `AskUserQuestion` to ask for approval:
- Option 1: "Commit" - proceed with the commit
- Option 2: "Edit message" - let user modify the commit message
- Option 3: "Cancel" - abort the commit

**DO NOT proceed with the commit until user explicitly approves.**

### Step 6: Execute the Commit

Simple commit command:

```bash
git commit -m "[XX-YY] type: description"
```

**IMPORTANT**: Do NOT add Co-Authored-By or any other footers to commit messages.

### Step 7: Confirm Success

After committing:
- Run `git status` to verify
- Show the commit hash and message
- Remind user to push if needed

## Arguments

- `$ARGUMENTS` - Can contain type override, description, and/or flags
  - `/commit` - Interactive mode
  - `/commit fix` - Force type to "fix"
  - `/commit feat add user authentication` - Type + description
  - `/commit --meta` - Use [00-00] meta: format for meta/infrastructure changes
  - `/commit --meta add workflow specs` - Meta commit with description

## Safety Rules

1. NEVER use `git commit --amend` unless user explicitly requests
2. NEVER skip pre-commit hooks (no `--no-verify`)
3. NEVER stage files without user awareness
4. ALWAYS show the final commit message before executing
5. If pre-commit hook fails, inform user and do NOT retry with amend

## Output Format

On success:
```
✅ Committed: [XX-YY] type: description
   Hash: abc1234
   Branch: phase-01/task-02-feature
```

On failure:
```
❌ Commit failed: [reason]
   Action: [what to do next]
```