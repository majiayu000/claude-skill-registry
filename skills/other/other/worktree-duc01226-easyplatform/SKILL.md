---
name: worktree
version: 1.0.0
description: '[Git] Create isolated git worktree for parallel development'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Create isolated git worktrees for parallel feature development with automatic branch naming and env file setup.

**Workflow:**

1. **Get Repo Info** — Run `worktree.cjs info` to detect repo type, base branch, env files
2. **Detect Prefix** — Infer branch prefix from keywords (fix, feat, refactor, docs, etc.)
3. **Convert Slug** — Transform description to kebab-case slug (max 50 chars)
4. **Execute** — Run `worktree.cjs create` with project, slug, prefix, and env files

**Key Rules:**

- For monorepos, ask user which project if not specified
- Always ask which env files to copy via AskUserQuestion
- Handle error codes (BRANCH_CHECKED_OUT, WORKTREE_EXISTS, etc.) gracefully

Create an isolated git worktree for parallel feature development.

## Workflow

### Step 1: Get Repository Info

```bash
node .claude/scripts/worktree.cjs info --json
```

**Response fields:**

- `repoType`: "monorepo" or "standalone"
- `baseBranch`: detected base branch
- `projects`: array of {name, path} for monorepo
- `envFiles`: array of .env\* files found
- `dirtyState`: boolean

### Step 2: Gather Info via AskUserQuestion

**Detect branch prefix from user's description:**

- Keywords "fix", "bug", "error", "issue" → prefix = `fix`
- Keywords "refactor", "restructure", "rewrite" → prefix = `refactor`
- Keywords "docs", "documentation", "readme" → prefix = `docs`
- Keywords "test", "spec", "coverage" → prefix = `test`
- Keywords "chore", "cleanup", "deps" → prefix = `chore`
- Keywords "perf", "performance", "optimize" → prefix = `perf`
- Everything else → prefix = `feat`

**For MONOREPO:** Use AskUserQuestion if project not specified:

```javascript
// If user said "/worktree add auth" but multiple projects exist
AskUserQuestion({
    questions: [
        {
            header: 'Project',
            question: 'Which project should the worktree be created for?',
            options: projects.map(p => ({ label: p.name, description: p.path })),
            multiSelect: false
        }
    ]
});
```

**For env files:** Always ask which to copy:

```javascript
AskUserQuestion({
    questions: [
        {
            header: 'Env files',
            question: 'Which environment files should be copied to the worktree?',
            options: envFiles.map(f => ({ label: f, description: 'Copy to worktree' })),
            multiSelect: true
        }
    ]
});
```

### Step 3: Convert Description to Slug

- "add authentication system" → `add-auth`
- "fix login bug" → `login-bug`
- Remove filler words, kebab-case, max 50 chars

### Step 4: Execute Command

**Monorepo:**

```bash
node .claude/scripts/worktree.cjs create "<PROJECT>" "<SLUG>" --prefix <TYPE> --env "<FILES>"
```

**Standalone:**

```bash
node .claude/scripts/worktree.cjs create "<SLUG>" --prefix <TYPE> --env "<FILES>"
```

**Options:**

- `--prefix` - Branch type: feat|fix|refactor|docs|test|chore|perf
- `--env` - Comma-separated .env files to copy
- `--json` - Output JSON for parsing
- `--dry-run` - Preview without executing

## Commands

| Command  | Usage                        | Description                |
| -------- | ---------------------------- | -------------------------- |
| `create` | `create [project] <feature>` | Create new worktree        |
| `remove` | `remove <name-or-path>`      | Remove worktree and branch |
| `info`   | `info`                       | Get repo info              |
| `list`   | `list`                       | List existing worktrees    |

## Error Codes

| Code                       | Meaning                              | Action                    |
| -------------------------- | ------------------------------------ | ------------------------- |
| `MISSING_ARGS`             | Missing project/feature for monorepo | Ask for both              |
| `MISSING_FEATURE`          | No feature name (standalone)         | Ask for feature           |
| `PROJECT_NOT_FOUND`        | Project not in .gitmodules           | Show available projects   |
| `MULTIPLE_PROJECTS_MATCH`  | Ambiguous project name               | Use AskUserQuestion       |
| `MULTIPLE_WORKTREES_MATCH` | Ambiguous worktree for remove        | Use AskUserQuestion       |
| `BRANCH_CHECKED_OUT`       | Branch in use elsewhere              | Suggest different name    |
| `WORKTREE_EXISTS`          | Path already exists                  | Suggest use or remove     |
| `WORKTREE_CREATE_FAILED`   | Git command failed                   | Show git error            |
| `WORKTREE_REMOVE_FAILED`   | Cannot remove worktree               | Check uncommitted changes |

## Example Session

```
User: /worktree fix the login validation bug

Claude: [Runs: node .claude/scripts/worktree.cjs info --json]
        [Detects: standalone repo, envFiles: [".env.example"]]
        [Detects prefix from "fix" keyword: fix]
        [Converts slug: "login-validation-bug"]

Claude: [Uses AskUserQuestion for env files]
        "Which environment files should be copied?"
        Options: .env.example

User: .env.example

Claude: [Runs: node .claude/scripts/worktree.cjs create "login-validation-bug" --prefix fix --env ".env.example"]

Output: Worktree created at ../worktrees/myrepo-login-validation-bug
        Branch: fix/login-validation-bug
```

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
