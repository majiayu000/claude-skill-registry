---
name: creating-worktree
description: Creates isolated git worktrees in .worktrees/ with intelligent branch naming, auto-incrementing, and commit type detection (feat/fix/refactor). Supports manual descriptions and auto-generation from uncommitted git changes. Use when user requests to create worktree, start isolated work, parallel development, run /worktree command, or mentions "worktree".
model: haiku
---

# Git Worktree Creation Workflow

Create isolated git worktrees in `.worktrees/` with intelligent branch naming. Combines worktree isolation with the same naming convention as the `creating-branch` skill.

## Usage

This skill is invoked when:
- User runs `/worktree` or `/git:worktree` command
- User requests to create a worktree for isolated work

## Two Operation Modes

### Mode 1: With Description (Manual)

The command takes a description and automatically detects the commit type.

**Format**: `/worktree <description>`

**Examples**:
```bash
/worktree add user authentication
# Worktree: .worktrees/user-authentication
# Branch:   feat/001-user-authentication

/worktree fix login bug
# Worktree: .worktrees/login-bug
# Branch:   fix/002-login-bug

/worktree refactor auth service
# Worktree: .worktrees/auth-service
# Branch:   refactor/003-auth-service
```

### Mode 2: Auto-Generate from Changes (No Arguments)

When no arguments provided and no sdlc-develop specs exist, analyze uncommitted changes to generate names automatically.

**Format**: `/worktree` (no arguments)

**Process**:
1. Check for sdlc-develop specs (see Mode 3)
2. If no specs, check for uncommitted changes (both staged and unstaged)
3. If no changes exist, display error and require description
4. If changes exist, analyze to generate description
5. Create worktree with auto-generated names

### Mode 3: From SDLC-Develop Spec (Arkhe Integration)

When no arguments provided and sdlc-develop specs exist, create worktree linked to an existing feature spec.

**Detection Flow:**
1. Check if `.arkhe.yaml` exists -> read `develop.specs_dir` (default: `arkhe/specs`)
2. Scan `{specs_dir}/` for existing spec directories
3. If specs found -> present selection via `AskUserQuestion`
4. Use spec directory name for worktree and branch names

## Naming Convention

This skill produces **dual names**:

| Component | Format | Example |
|-----------|--------|---------|
| **Worktree directory** | `.worktrees/{keywords}` | `.worktrees/user-authentication` |
| **Git branch** | `{type}/{number}-{keywords}` | `feat/001-user-authentication` |

The directory uses just keywords (tab-completion friendly). The branch uses the full conventional format (consistent with `/create-branch`).

## Commit Type Detection

Automatically detect commit types from keywords in the description:

| Type | Keywords |
|------|----------|
| **feat** | add, create, implement, new, update, improve |
| **fix** | fix, bug, resolve, correct, repair |
| **refactor** | refactor, rename, reorganize |
| **chore** | remove, delete, clean, cleanup |
| **docs** | docs, document, documentation |

If no keyword is detected, defaults to `feat`.

## Keyword Extraction

1. Split description into words
2. Remove stopwords: the, a, an, for, to, in, on, at, by, with, from, and, or, but, this, that
3. Remove commit type keywords (add, fix, create, etc.)
4. Keep first 2-3 meaningful words
5. Convert to lowercase, join with hyphens

## Workflow Steps

### Step 1: Parse Arguments and Determine Mode

```bash
# Check for arguments
DESCRIPTION="$ARGUMENTS"
```

If `$ARGUMENTS` is provided -> Mode 1 (manual)
If empty -> check for `.arkhe.yaml` specs (Mode 3), then fall back to auto-generate (Mode 2)

For Mode 2 (auto-generate):
```bash
# Check for uncommitted changes
CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null; git diff --cached --name-only 2>/dev/null)
```
If no changes, display error: "No arguments and no uncommitted changes. Provide a description: `/worktree <description>`"

If changes exist, analyze filenames/paths to generate a description.

### Step 2: Generate Names

**Detect commit type** from description keywords (see table above). Default to `feat`.

**Extract keywords**: Filter stopwords from description, keep first 2-3 meaningful words, hyphenate.

**Find next sequential number**:
```bash
# Scan ALL branches (shared number space with /create-branch)
MAX_NUM=$(git branch --list | grep -oE '/[0-9]{3}-' | grep -oE '[0-9]{3}' | sort -n | tail -1)
NEXT_NUM=$(printf "%03d" $((10#${MAX_NUM:-0} + 1)))
```

**Assemble names**:
- Worktree directory: `KEYWORDS` (e.g., `user-authentication`)
- Git branch: `TYPE/NUMBER-KEYWORDS` (e.g., `feat/001-user-authentication`)

### Step 3: Validate Worktree Directory

```bash
# Check directory doesn't already exist
ls .worktrees/$KEYWORDS 2>/dev/null
```

If it exists, report the conflict and stop. Suggest either a different description or removing the existing worktree.

Also check if the branch already exists:
```bash
git branch --list "$TYPE/$NEXT_NUM-$KEYWORDS"
```

If the branch exists, increment the number and retry.

### Step 4: Safety Check - Git Ignore

Verify `.worktrees/` is git-ignored:

```bash
git check-ignore -q .worktrees 2>/dev/null
```

If NOT ignored (exit code non-zero), add `.worktrees/` to `.gitignore`:

```bash
echo '\n# Worktrees\n.worktrees/' >> .gitignore
git add .gitignore && git commit -m "chore: add .worktrees/ to .gitignore"
```

### Step 5: Ask Base Branch

Use `AskUserQuestion` to ask which branch to base the worktree on:

- **main (Recommended)** -- Create from the main branch
- **Current branch** -- Create from the currently checked out branch
- **Other** -- User specifies a different branch name

### Step 6: Create Worktree

```bash
mkdir -p .worktrees
git worktree add ".worktrees/$KEYWORDS" -b "$TYPE/$NEXT_NUM-$KEYWORDS" "$BASE_BRANCH"
```

Where `$BASE_BRANCH` is `main`, `HEAD`, or the user-specified branch.

### Step 7: Confirm Success

Report:
- Worktree path: `.worktrees/<keywords>`
- Git branch: `<type>/<number>-<keywords>` (based on `<base-branch>`)
- List worktrees: `git worktree list`
- Remove when done: `git worktree remove .worktrees/<keywords>`

## Important Notes

- **Sequential Numbering**: Shared number space with `/create-branch` -- scans all branches
- **Keyword Extraction**: Filters common words, keeps 2-3 meaningful terms
- **Lowercase Convention**: All names are lowercase with hyphens
- **Conventional Commits**: Branch names align with conventional commit types
- **Dual Naming**: Directory name differs from branch name for usability

## Supporting Documentation

- **[WORKFLOW.md](WORKFLOW.md)** - Detailed step-by-step process
- **[EXAMPLES.md](EXAMPLES.md)** - Real-world examples for all worktree types
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
