---
name: stackit
description: Manage stacked Git branches with Stackit. Use when creating/managing
  stacked branches, submitting PRs for branch stacks, navigating branch trees, rebasing
  stacks, syncing with main/trunk, troubleshoot
---

---
name: stackit
description: Manage stacked Git branches with Stackit. Use when creating/managing stacked branches, submitting PRs for branch stacks, navigating branch trees, rebasing stacks, syncing with main/trunk, troubleshooting stack issues, absorbing changes, resolving rebase conflicts, or any workflow involving dependent Git branches. Keywords stackit, stacked changes, stacked PRs, branch stack, restack, absorb, git stack.
allowed-tools: Bash(stackit:*), Bash(git:*), Bash(~/.claude/skills/stackit/scripts/*:*), Read, Grep, Glob
version: {{VERSION}}
---

# Stackit - Stacked Branch Management

You are an expert at using Stackit to manage stacked Git branches. Stackit helps developers break large features into small, focused PRs that stack on top of each other. Stacks can be linear chains or branch into tree structures when you need parallel work paths that share a common base.

## Before Any Operation

**Always run `command stackit log --no-interactive` first** to understand:
- Current branch position in the stack
- Parent/child relationships
- Which branches need attention

**CRITICAL: Non-Interactive Mode**
When calling `command stackit` commands, **ALWAYS** include the `--no-interactive` flag. This ensures the command fails or proceeds according to defaults rather than hanging for user input. For commands that require confirmation, include the `--force` flag (for absorb) or `--yes` flag (for undo/merge) in addition to `--no-interactive`.

**Check for project conventions:**
- Read `README.md` and `CONTRIBUTING.md` for project-specific guidelines before generating commit messages or branch names.
- Follow documented commit message formats, PR templates, and workflows.
- Respect any branching or testing requirements specified.

## Quick Health Check

Run the stack analyzer to check health and get actionable suggestions:
```bash
bash ~/.claude/skills/stackit/scripts/analyze_stack.sh
```

> **Note:** All stackit commands below should be called with `command stackit ... --no-interactive`.

## Core Workflows

### Creating a New Branch

**Key difference from git:** Unlike git where you create a branch first then commit, stackit creates the branch and commits in one step. This allows automatic branch name generation from the commit message.

1. **Stage changes:** `git add <files>` or use `--all` flag
2. **Generate commit message** after checking `README.md` / `CONTRIBUTING.md`; follow project conventions if documented, otherwise write a clear, descriptive summary.
3. **Create branch with commit** (branch name auto-generated from message, respects `branch.pattern` config):
   ```bash
   # Preferred: pipe format (handles multi-line messages and special characters)
   echo "feat: add user authentication" | command stackit create --no-interactive

   # With explicit branch name
   echo "feat: add user authentication" | command stackit create my-branch --no-interactive

   # Stage all changes and create in one command
   echo "feat: add user authentication" | command stackit create --all --no-interactive
   ```
4. If currently on trunk (e.g., main/master), warn and confirm or switch to a feature branch before creating.
5. Show stack: `command stackit log --no-interactive`

### Adding More Commits to a Branch

**A stacked branch can have multiple commits.** You don't need to create a new branch for every commit:

- **Add another commit:** Make changes, stage them, then use `git commit` as normal
- **Amend the current commit:** `command stackit modify` (like `git commit --amend`)
- **Absorb changes into the right commits:** Stage fixes across multiple commits, then `command stackit absorb` automatically amends each change to the correct commit

When to use multiple commits vs new branches:
- **Same logical change:** Multiple commits in one branch (e.g., implementation + tests)
- **Separate reviewable units:** Create a new stacked branch with `command stackit create`

### Submitting PRs

1. Check stack state: `command stackit log --no-interactive`
2. Submit options:
   - Current + ancestors: `command stackit submit --no-interactive`
   - Entire stack: `command stackit submit --stack --no-interactive`
   - As drafts: `command stackit submit --draft --no-interactive`

### Syncing with Main

1. Sync with trunk and cleanup: `command stackit sync --no-interactive`
2. If branches were deleted: `command stackit restack --no-interactive`

### Fixing Issues

- **Rebase conflicts:** Resolve files, then `command stackit continue --no-interactive`
- **Absorb conflicts:** See [workflows/absorb-conflict.md](workflows/absorb-conflict.md) or use `command stackit absorb --show-conflict --no-interactive`
- **Abort operation:** `command stackit abort --no-interactive`
- **Undo last command:** `command stackit undo --no-interactive --yes`
- **Stack health issues:** See [workflows/fix-absorb.md](workflows/fix-absorb.md) or run `/stack-fix`
- **Intelligent folding:** See [workflows/stack-fold.md](workflows/stack-fold.md) or run `/stack-fold`

## Commit Message Examples

Generate commit messages following these patterns:

**Example 1: Feature addition**
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware.
Supports refresh tokens and role-based access.
```

**Example 2: Bug fix**
```
fix(cache): prevent race condition in invalidation

Add mutex locking around cache clear operations.
Fixes issue where concurrent requests could see stale data.
```

**Example 3: Multiple changes**
```
chore: update dependencies and refactor errors

- Upgrade lodash to 4.17.21
- Standardize error response format
- Add error codes for API responses
```

**Format:**
- Follow project conventions from README.md/CONTRIBUTING.md if documented
- Otherwise: clear, descriptive subject line + blank line + explanation of "why"
- Some projects use conventional commits: `type(scope): description`

## Command Reference

For detailed command information, see:
- **Navigation:** [commands/navigation.md](commands/navigation.md) - log, checkout, up, down, trunk
- **Branch operations:** [commands/branch.md](commands/branch.md) - create, modify, absorb, delete
- **Stack operations:** [commands/stack.md](commands/stack.md) - restack, submit, sync, foreach
- **Recovery & utilities:** [commands/recovery.md](commands/recovery.md) - undo, continue, abort, doctor

Quick reference: [reference.md](reference.md)

## Detailed Workflows

For complex operations requiring multiple steps:
- **Fixing compilation errors after absorb:** [workflows/fix-absorb.md](workflows/fix-absorb.md)
- **Resolving conflicts during rebase:** [workflows/conflict-resolution.md](workflows/conflict-resolution.md)
- **Resolving absorb conflicts:** [workflows/absorb-conflict.md](workflows/absorb-conflict.md)

## Auto-Generation Guidelines

### Branch Names
Branch names are **optional** - stackit auto-generates from commit message:
- Only provide if user explicitly requests a specific name
- Auto-generated format: kebab-case from commit message
- Example: "Add user authentication" → "add-user-authentication"

### Commit Messages
When generating commit messages:
1. Check README.md and CONTRIBUTING.md for project guidelines
2. Follow documented conventions if available
3. If no conventions documented, write a clear, descriptive message
4. **Use pipe format:** `echo "message" | command stackit create --no-interactive`

**Validation loop:**
- Generate message
- Verify: Clear description? Follows project conventions (if documented)?
- If fails: revise and re-validate
- Only proceed when message meets quality standards

### PR Descriptions
When generating PR descriptions:
1. Check for .github/pull_request_template.md or CONTRIBUTING.md
2. Follow project-specific templates if available
3. Default format:
   ```markdown
   ## Summary
   - Bullet point summary of changes

   ## Test Plan
   - [ ] Specific testing steps
   - [ ] Verification procedures

   [Additional sections per project templates]
   ```

**Validation before submission:**
- Title is clear and descriptive?
- Body has meaningful content (not placeholders)?
- Test plan is specific?

## FORBIDDEN Commands

When working with stacks, NEVER use these git commands:

| FORBIDDEN | USE INSTEAD |
|-----------|-------------|
| `git commit` (for new branches) | `command stackit create` |
| `git checkout -b` | `command stackit create` |
| `gh pr create` | `command stackit submit` |
| `git rebase` | `command stackit restack` |

**Exception:** `git commit` is allowed ONLY when adding additional commits to an existing stacked branch.

## Important Rules

1. **NEVER use `git commit` to create new stacked branches** - always use `command stackit create`
2. **Stage changes BEFORE running `command stackit create`** - it requires staged changes to work correctly
3. **Check state before destructive operations** - run `command stackit log` first
4. **Always validate after absorb** - absorb can cause compilation errors, see fix-absorb workflow
5. **Handle conflicts gracefully** - guide user through resolution, see conflict-resolution workflow
6. **Keep PRs small and focused** - suggest splitting if too large
7. **Use validation loops** - for commit messages, PR descriptions, and post-absorb builds

## Version {{VERSION}} Changes

New features:
- Progressive disclosure with organized reference files
- Workflow checklists for complex operations (fix-absorb, conflict resolution)
- Utility scripts for stack analysis
- Enhanced slash commands with validation loops
- New `/stack-absorb` and `/stack-fold` commands
- Expanded commit message examples
- Better error recovery patterns

Migration:
- Re-run `stackit agent install --force` to update files
- No breaking changes to existing workflows
