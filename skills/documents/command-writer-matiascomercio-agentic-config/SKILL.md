---
name: command-writer
description: 'Expert assistant for creating Claude Code custom slash commands. Guides
  command file structure, YAML frontmatter configuration, variable syntax, and best
  practices. Triggers on keywords: writing comma'
---

---
name: command-writer
description: Expert assistant for creating Claude Code custom slash commands. Guides command file structure, YAML frontmatter configuration, variable syntax, and best practices. Triggers on keywords: writing commands, creating commands, slash command, custom command, new command, command template, make command, /command, create command, update command
project-agnostic: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Command Writer Skill

Expert guide for creating Claude Code custom slash commands.

**Official Docs**: https://code.claude.com/docs/en/slash-commands

---

## 1. Quick Reference

### YAML Frontmatter Template
```yaml
---
description: Shows in slash command menu
argument-hint: <arg1> [arg2]
project-agnostic: false  # default; set true only if truly reusable across any project
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---
```

### Minimal Command Template
```markdown
---
project-agnostic: false  # Required - default value
---

Describe what this command does and instruct Claude how to execute it.
```
That's it. Save as `.md` file in correct location.

### File Locations

| Scope | Path | Visibility |
|-------|------|------------|
| Project | `.claude/commands/<name>.md` | Team (committed) |
| Personal Project | `.claude/commands/<name>.md` (gitignored) | You only |
| Global | `~/.claude/commands/<name>.md` | All your projects |

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | No* | Shows in `/` menu (*recommended for complex commands) |
| `allowed-tools` | No | Restrict which tools command can use |
| `argument-hint` | No | Hint shown after command name (e.g., `<issue-number>`) |
| `model` | No | Force specific model for this command |
| `disable-model-invocation` | No | Set `true` for simple text expansion only |
| `project-agnostic` | **Yes** | **Default: `false`**. Set `true` only if command is truly project-agnostic |

### Variable Syntax

| Syntax | Description | Example |
|--------|-------------|---------|
| `$ARGUMENTS` | All text after command | `/deploy $ARGUMENTS` -> "staging --dry-run" |
| `$1`, `$2`, ... | Positional arguments | `/pr $1` -> first word only |
| `@<filepath>` | Include file contents inline | `@src/config.ts` |
| BANG + backticks | Execute bash, include output | `git status` wrapped in BANG-backticks |

> **BANG syntax**: Write exclamation mark (!) followed by backtick-wrapped command, e.g., BANG then backtick-command-backtick

> **WARNING - Documentation Safety**: When DOCUMENTING this syntax in skills or command files, NEVER use the literal pattern (exclamation + backtick). Claude Code's parser executes this pattern during file loading, causing errors. Use safe alternatives: "BANG-backtick", `[BANG-backtick: cmd]`, or text descriptions like "exclamation + backtick".

---

## 2. Validation Checklist

Before saving any command:

- [ ] **Location**: `.claude/commands/` (project) or `~/.claude/commands/` (global)
- [ ] **Extension**: File ends with `.md`
- [ ] **Description**: Present in frontmatter if command is non-trivial
- [ ] **Variables**: Using `$ARGUMENTS` not `{args}` or `{{input}}`
- [ ] **File refs**: Using `@path` not `{{file:path}}`
- [ ] **Bash output**: Using BANG-backtick syntax, not `$(cmd)` or `{{shell:cmd}}`
- [ ] **Safety**: Destructive ops have confirmation gates
- [ ] **Paths**: No hardcoded absolute paths (use relative or variables)
- [ ] **Project-agnostic**: **REQUIRED** - Explicitly set `project-agnostic: false` (default) or `true` (if truly reusable)

---

## 3. Command Patterns

### Pattern 1: Minimal (Simple Prompt Expansion)

**File**: `.claude/commands/explain.md`
```markdown
---
project-agnostic: true  # Reusable across any project
---

Explain the code in the current file. Focus on:
- What it does
- Key design decisions
- Potential improvements
```

Usage: `/explain`

---

### Pattern 2: With Variables

**File**: `.claude/commands/review-file.md`
```markdown
---
description: Review a specific file for code quality
argument-hint: <filepath>
project-agnostic: true  # Reusable across any project
---

Review this file for code quality issues:

@$ARGUMENTS

Check for:
- Bug risks
- Performance issues
- Readability improvements
```

Usage: `/review-file src/auth.ts`

---

### Pattern 3: Full Frontmatter

**File**: `.claude/commands/refactor.md`
```markdown
---
description: Refactor code with specific pattern
argument-hint: <pattern> <filepath>
allowed-tools:
  - Read
  - Edit
  - Grep
project-agnostic: true  # Reusable across any project
---

Apply refactoring pattern "$1" to file:

@$2

## Patterns
- `extract-function`: Extract repeated code into functions
- `simplify-conditionals`: Reduce nested if/else
- `add-types`: Add TypeScript types to untyped code

## Rules
- Preserve behavior exactly
- Add tests if missing
- Run existing tests after changes
```

Usage: `/refactor extract-function src/utils.ts`

---

### Pattern 4: Git Operations (Safety-Critical)

**File**: `.claude/commands/release.md`
```markdown
---
description: Create release branch and tag
argument-hint: <version>
project-agnostic: false  # Expects project-specific version files (package.json, etc.)
allowed-tools:
  - Bash
  - Read
---

# Release Command

Create release for version: $ARGUMENTS

## Pre-Flight Checks

1. **Verify clean state**:
   - Run: git status --porcelain (via BANG-backtick)
   - Must be empty; if dirty: STOP and list uncommitted changes

2. **Verify branch**:
   - Run: git branch --show-current (via BANG-backtick)
   - Must be `main` or `master`
   - If not: STOP with "Switch to main branch first"

3. **Verify version format**:
   - Must match `vX.Y.Z` (semver)
   - If invalid: STOP with format instructions

## Confirmation Gate

**STOP HERE** and show user:
```
Release Summary:
- Version: $ARGUMENTS
- Branch: [current branch]
- Last commit: [short hash + message]

Proceed? (yes/no)
```

Wait for explicit "yes" before continuing.

## Execution (only after confirmation)

1. Create release branch:
   ```bash
   git checkout -b release/$ARGUMENTS
   ```

2. Update version files:
   - package.json (if exists)
   - pyproject.toml (if exists)
   - VERSION file (if exists)

3. Commit version bump:
   ```bash
   git add -A
   git commit -m "chore: bump version to $ARGUMENTS"
   ```

4. Create annotated tag:
   ```bash
   git tag -a $ARGUMENTS -m "Release $ARGUMENTS"
   ```

5. Show next steps (DO NOT auto-push):
   ```
   Release prepared locally. To publish:
   git push origin release/$ARGUMENTS
   git push origin $ARGUMENTS
   ```

## Abort Conditions
- Any git command fails: STOP immediately
- User says "no" at confirmation: STOP and revert any changes
- Version already exists: STOP with error
```

Usage: `/release v2.1.0`

---

## 4. Writing Effective Commands

### Frontmatter Best Practices

```yaml
---
# REQUIRED: Explicit project-agnostic declaration
project-agnostic: false  # default - most commands are project-specific
# OR
project-agnostic: true   # only if truly reusable across any project

# GOOD: Clear, actionable description
description: Generate unit tests for a function

# BAD: Vague or missing
description: Tests
---
```

- **project-agnostic**: **REQUIRED** - Must be explicitly set. Default is `false`
- **description**: Verb phrase describing outcome
- **argument-hint**: Show expected format (`<issue-id>`, `<file> [options]`)
- **allowed-tools**: Restrict to minimum needed (security + focus)

### Variable Usage

```markdown
# All arguments as single string
Process this request: $ARGUMENTS

# Positional arguments
Compare $1 (old) with $2 (new)

# File inclusion (contents inline)
Analyze this code:
@src/main.py

# Dynamic context from shell (BANG-backtick syntax)
Current git state:
[use exclamation + backtick-wrapped: git log --oneline -5]
```

### Safety Patterns

**Confirmation Gate** (for destructive operations):
```markdown
## Confirmation Required

Before proceeding, show:
- What will be modified/deleted
- Estimated impact

Ask: "Proceed with [action]? Type 'yes' to confirm"

WAIT for explicit "yes". Any other response = abort.
```

**Branch Protection**:
```markdown
## Branch Check

Current branch: [BANG-backtick: git branch --show-current]

If branch is `main`, `master`, or `production`:
- STOP immediately
- Error: "Cannot run on protected branch"
```

**Auth/Permission Check**:
```markdown
## Permission Check

Verify access before proceeding:
[BANG-backtick: aws sts get-caller-identity 2>&1]

If error or wrong account: STOP with instructions.
```

### Section Structure

Recommended sections for complex commands:

1. **Context** - What this does, when to use
2. **Pre-Flight Checks** - Validations before action
3. **Confirmation Gate** - User approval point
4. **Execution** - Step-by-step actions
5. **Rollback** - How to undo if needed
6. **Next Steps** - What user should do after

---

## 5. Anti-Patterns

### Missing Description

```markdown
# BAD: No frontmatter, unclear purpose
Do the thing with $ARGUMENTS
```

```markdown
# GOOD: Clear intent
---
description: Deploy to specified environment
argument-hint: <env>
project-agnostic: false  # Requires project-specific deployment scripts
---

Deploy application to $ARGUMENTS environment...
```

### Incorrect Variable Syntax

```markdown
# BAD: Wrong syntax (won't work)
Process {{input}}
Read file: ${filepath}
Run: $(git status)

# GOOD: Correct Claude Code syntax
Process $ARGUMENTS
Read file: @$1
Run: [BANG-backtick: git status]
```

### No Confirmation for Destructive Ops

```markdown
# BAD: Immediate deletion
Delete all files matching: $ARGUMENTS
[BANG-backtick: rm -rf $ARGUMENTS]

# GOOD: Confirmation required
## Files to Delete
[BANG-backtick: find . -name "$ARGUMENTS" -type f]

**CONFIRM**: Type "yes" to delete these files.
[Wait for confirmation before any rm command]
```

### Hardcoded Paths

```markdown
# BAD: Won't work on other machines
Read config: @/Users/john/project/config.json

# GOOD: Relative or variable
Read config: @./config.json
Read config: @$1
```

### Unmarked Project-Specific Commands

```markdown
# BAD: References project structure without declaring
---
description: Run our custom linter
---
Run ./scripts/custom-lint.sh on $ARGUMENTS
```

```markdown
# GOOD: Declares project-specific nature
---
description: Run our custom linter
project-agnostic: false
---
# Note: Requires ./scripts/custom-lint.sh from this project
Run ./scripts/custom-lint.sh on $ARGUMENTS
```

### Over-Permissive Tools

```markdown
# BAD: Full access for simple task
---
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - WebFetch
---
Just format this JSON: $ARGUMENTS

# GOOD: Minimal permissions
---
allowed-tools:
  - Read
---
Just format this JSON: $ARGUMENTS
```

### Missing Error Handling

```markdown
# BAD: Assumes success
Run migration then deploy.

# GOOD: Handle failures
1. Run migration: [BANG-backtick: npm run migrate]
2. If migration fails: STOP, show error, suggest rollback
3. Only if migration succeeds: proceed to deploy
```

### Unsafe Bash Syntax in Documentation

```markdown
# BAD: Literal pattern triggers execution during file load
# Example of git status using exclamation-backtick syntax...
# (the literal pattern causes: "Error: Bash command failed")

# GOOD: Use safe alternatives in documentation
# Example of git status using BANG-backtick syntax...
# Or: [BANG-backtick: git status]
# Or: "exclamation mark followed by backtick-wrapped command"
```

**Why This Matters**: When skill or command files contain the literal exclamation + backtick pattern (even in examples or comments), Claude Code's parser executes it as bash during file loading. This causes immediate errors and prevents the file from loading properly.

**Safe Documentation Patterns**:
- Use "BANG-backtick" as a text placeholder
- Use `[BANG-backtick: cmd]` format in examples
- Write "exclamation + backtick" in prose
- Never combine the actual symbols in documentation

---

## 6. Pre-Share Checklist

Before committing or sharing a command:

- [ ] Tested with various inputs (happy path + edge cases)
- [ ] Description accurately reflects behavior
- [ ] No secrets/tokens hardcoded
- [ ] Paths are relative or parameterized
- [ ] Destructive operations have confirmation gates
- [ ] Protected branches are guarded
- [ ] Error cases handled gracefully
- [ ] Rollback instructions included (if applicable)
- [ ] Follows team naming conventions
- [ ] Documentation matches implementation
- [ ] `project-agnostic` **explicitly set** (true for reusable, false for project-specific) - **REQUIRED**

---

## Quick Examples

| Command | Purpose | Key Feature |
|---------|---------|-------------|
| `/explain` | Explain current file | Minimal, no args |
| `/review $1` | Review specific file | File reference |
| `/test $ARGUMENTS` | Generate tests | Variable args |
| `/deploy $1` | Deploy to env | Confirmation gate |
| `/release $1` | Create release | Full safety pattern |
