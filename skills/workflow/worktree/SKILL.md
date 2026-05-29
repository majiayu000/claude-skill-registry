---
description: Creates a git worktree for isolated parallel development — new branch in a separate directory with project setup and test baseline. Enables multiple Claude Code sessions on different tasks simultaneously. Multi-repo aware. Use when you need to work on something else without disturbing current work.
disable-model-invocation: true
---

# Worktree

Create a git worktree for isolated parallel development. Sets up a new branch in a separate directory (`.worktrees/`) with project setup and test baseline, so the main workspace stays untouched. Each worktree can host an independent Claude Code session.

## Workflow

### 1. Multi-repo Detection

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected:
- Run the git commands below inside each child repo (the workspace root has no `.git/`, so git commands must target individual repos)
- If the user specified a target repo (inline or in conversation), use it
- If ambiguous, use `AskUserQuestion` — header "Target repo", question "Which repo should the worktree be created for?": list each repo as an option

### 2. Worktree Detection Guard

Read `$CLAUDE_PLUGIN_ROOT/skills/worktree/references/worktree-setup.md` and run the **worktree detection guard** from that reference. If the guard detects you are already inside a linked worktree, inform the user:

```
Already running inside a worktree (`<worktree-path>`).
To create another worktree, run this skill from the main workspace instead.
```

Then **stop** — do not create recursive worktrees.

### 3. Gather Context and Branch Name

Record the current branch:

```bash
git rev-parse --abbrev-ref HEAD
```

Determine a meaningful description for the branch from the **first source that provides enough signal** (check in this priority order):

1. **Inline description** — if the user provided text with the invocation (e.g., `/optimus:worktree "fix login timeout"`), use it directly
2. **Conversation context** — scan the current conversation for the user's task intent, problem description, or feature request

If neither source provides enough signal, use `AskUserQuestion` — header "Worktree scope", question "What will you work on in the new worktree?":
- **New feature** — "Implement a new capability"
- **Bug fix** — "Fix a bug or issue"
- **Other** — "Describe the task"

Read `$CLAUDE_PLUGIN_ROOT/skills/commit/references/branch-naming.md` for the naming convention. Determine `<type>` and generate the slug from the description.

**Handle collisions**: if `git show-ref --verify --quiet refs/heads/<branch-name>` succeeds (branch exists), append `-2` to the slug. If that also exists, try `-3`, and so on up to `-9`. If all collide, inform the user and stop.

Create the branch without switching to it:

```bash
git branch <branch-name>
```

### 4. Create Worktree

Follow the **setup procedure** from `$CLAUDE_PLUGIN_ROOT/skills/worktree/references/worktree-setup.md` using `<branch-name>` and `<original-branch>` from Step 3. The procedure handles:
- Deriving the worktree directory name
- Creating `.worktrees/` and ensuring it is gitignored
- Creating the worktree: `git worktree add .worktrees/<worktree-dir> <branch-name>`
- Running project setup in the worktree (npm install, pip install, cargo build, etc.)
- Verifying the test baseline

If worktree creation fails, report the error with diagnostic information and stop.

### 5. Report and Next Steps

```
## Worktree Created

Working directory: `.worktrees/<worktree-dir>`
Branch: `<branch-name>` (from `<original-branch>`)
Main workspace: `<original-branch>` (unchanged)
Tests: passing / no test command detected

### Open the worktree

**VSCode** (recommended — each worktree gets its own window, terminal, and file watchers):
- Source Control panel → right-click the worktree → "Open Worktree in New Window"
- Or from terminal: `code .worktrees/<worktree-dir>`
- Or Command Palette → "Git: Open Worktree in New Window"

**Claude Code CLI**: `cd .worktrees/<worktree-dir> && claude`

### Cleanup

When done: `git worktree remove .worktrees/<worktree-dir>`
```

Recommend running `/optimus:tdd` in the new worktree for test-driven development, or `/optimus:init` if the worktree needs project setup.

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.

## Important

- Never commit or push anything in the main workspace
- The main workspace branch is always restored to `<original-branch>`
- Worktrees are created inside `.worktrees/` (gitignored) to keep the project root clean
