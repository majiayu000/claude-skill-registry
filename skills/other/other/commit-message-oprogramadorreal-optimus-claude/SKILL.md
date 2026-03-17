---
description: This skill suggests conventional commit messages by analyzing staged, unstaged, and untracked git changes — read-only, never commits.
disable-model-invocation: true
---

# Commit Message Suggester

Generate a conventional commit message by analyzing all local git changes (staged, unstaged, and untracked) without performing any commit.

## Workflow

### 1. Gather Change Context

#### Multi-repo workspace detection

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected:
- Run the git commands below inside each child repo (the workspace root has no `.git/`, so git commands must target individual repos)
- Track which repos have changes and which are clean
- Skip repos with no local changes (no staged, unstaged, or untracked files)
- If no repos have changes at all, inform the user and stop

#### Gather changes

Run the following git commands to understand all local changes (in a multi-repo workspace, run these inside each child repo that was detected above):

```bash
# Staged changes
git diff --cached --stat
git diff --cached

# Unstaged changes to tracked files
git diff --stat
git diff

# Untracked files
git status --short
```

### 2. Analyze Changes and Generate Conventional Commit Message

Read `$CLAUDE_PLUGIN_ROOT/skills/commit-message/references/conventional-commit-format.md` and follow its instructions to analyze the gathered changes and generate a conventional commit message.

### 3. Present the Message

Output the suggested commit message in a copyable code block. Do NOT run `git commit`. If the changes naturally split into multiple commits, present each message separately with instructions on which files to stage for each.

In a multi-repo workspace, present each repo's commit message under a heading with the repo directory name (e.g., `## isa-server`). If a repo's changes span multiple concerns, suggest separate commits within that repo's section. If only one repo has changes, still label it with the repo name for clarity.

## Important

- Never commit, stage, or modify any files
- This skill is read-only — it only analyzes and suggests
- When changes are too broad for a single commit, recommend splitting

Recommend the next step based on readiness:
- If the user wants to commit now → `/optimus:commit` to commit (and optionally push)
- If the feature is ready → `/optimus:pr` to create a pull request
- If validation is needed first → `/optimus:verify` to validate end-to-end

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
