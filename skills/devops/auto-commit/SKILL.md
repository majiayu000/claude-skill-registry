---
name: auto-commit
description: Automatically commits and pushes significant changes to git after completing features, fixes, or milestones. This skill should be used proactively by Claude when meaningful work is completed, or invoked manually via /auto-commit. Triggers on feature completion, bug fixes, configuration changes, documentation updates, or when explicitly requested.
---

# Auto-Commit Skill

Automatically stage, commit, and push changes to git when significant work is completed.

## When to Use

This skill activates when:

1. **Feature completion** - A new feature, component, or module is fully implemented
2. **Bug fix** - A bug has been identified and fixed
3. **Configuration/setup changes** - Project configuration, dependencies, or settings modified
4. **Documentation updates** - README, PRD, or other docs created/updated significantly
5. **Refactoring complete** - Code restructuring or cleanup finished
6. **Milestone reached** - A logical checkpoint in multi-step work
7. **User explicitly requests** - Via `/auto-commit` command or asking to commit

## Commit Decision Criteria

Before committing, verify:

- [ ] Changes are complete and functional (not work-in-progress)
- [ ] No obvious errors or broken code being committed
- [ ] Changes form a logical, cohesive unit of work
- [ ] Sensitive files (.env, credentials, secrets) are NOT staged

**Do NOT auto-commit when:**
- Changes are incomplete or experimental
- User is actively iterating on the same files
- Only whitespace or formatting changes
- Uncertain about the scope of changes

## Workflow

### Step 1: Assess Changes

Run git status to see what changed:

```bash
git status
```

Review the changes to understand:
- Which files were modified/added/deleted
- Whether changes are related to a single feature/fix
- If any sensitive files should be excluded

### Step 2: Review Diff

Examine the actual changes:

```bash
git diff
git diff --staged
```

Understand the nature of changes to write an accurate commit message.

### Step 3: Stage Relevant Files

Stage files selectively (preferred) or all changes:

```bash
# Preferred: Stage specific files
git add path/to/file1 path/to/file2

# Or stage all tracked changes
git add -u

# For new files that should be tracked
git add path/to/new/file
```

**Never stage:**
- `.env` files or any file containing secrets
- `node_modules/`, `__pycache__/`, or other dependency directories
- Large binary files unless explicitly intended
- IDE/editor configuration (`.idea/`, `.vscode/` unless project-shared)

### Step 4: Craft Commit Message

Follow conventional commits format:

```
<type>(<scope>): <description>

[optional body with more details]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Formatting, no code change
- `refactor` - Code restructuring
- `test` - Adding/updating tests
- `chore` - Maintenance, dependencies, config

**Examples:**
```
feat(auth): implement user authentication with JWT

Add login/logout endpoints, JWT token generation, and middleware
for protected routes.

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
fix(cart): resolve multi-vendor total calculation

Cart now correctly sums totals across different vendors
and applies shipping per vendor group.

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
docs(prd): create Kuwait marketplace PRD

Comprehensive PRD covering multi-vendor marketplace requirements,
user stories, technical architecture, and MVP scope.

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Step 5: Commit

Create the commit using HEREDOC for proper formatting:

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

<body if needed>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 6: Push to Remote

Push to the current branch:

```bash
git push
```

If the branch has no upstream:

```bash
git push -u origin <branch-name>
```

### Step 7: Confirm Success

Verify the commit and push succeeded:

```bash
git status
git log -1 --oneline
```

Report to the user:
- What was committed (files and summary)
- Commit hash
- Branch pushed to

## Safety Rules

1. **Never force push** (`--force` or `-f`) without explicit user permission
2. **Never commit secrets** - Check for .env, API keys, passwords
3. **Never amend previous commits** unless explicitly requested
4. **Always use Co-Authored-By** to attribute Claude's contribution
5. **Respect .gitignore** - Don't stage ignored files
6. **Check branch** - Confirm you're on the expected branch before pushing

## Proactive Usage

Claude should proactively invoke this skill when:

1. A task is marked complete and files were modified
2. User says "done", "finished", "complete" after implementation work
3. A logical milestone is reached in multi-step work
4. Creating or significantly updating documentation
5. After successful refactoring or bug fixes

Before auto-committing, briefly inform the user:
> "I've completed [description]. Let me commit these changes."

Then proceed with the workflow unless the user objects.

## Manual Invocation

Users can invoke via `/auto-commit` with optional arguments:

```
/auto-commit                    # Commit all staged/unstaged changes
/auto-commit "custom message"   # Use custom commit message
/auto-commit --dry-run          # Show what would be committed without committing
```
