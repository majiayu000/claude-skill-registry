---
description: Creates and switches to a new, conventionally named branch — derives the name from an inline description, conversation context, or local git diffs. Preserves all local changes. Never commits or pushes. Use when you want a properly named branch for new or in-progress work.
disable-model-invocation: true
---

# Branch

Create and switch to a new, conventionally named branch. Works in two common scenarios:

1. **In-progress work** — you have uncommitted local changes and want to move them to a properly named branch. All local changes (staged, unstaged, and untracked files) are preserved exactly as they are.
2. **Starting fresh** — you are on a clean main/master/develop branch and want to create a new branch before starting work (e.g., `/optimus:branch "add user authentication"`).

The branch name is derived from the first available context: an inline description, conversation history, or local git diffs. Never commits, pushes, stages, or modifies anything — purely a local branch operation.

## Workflow

### 1. Multi-repo Detection

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected:
- Run the git commands below inside each child repo (the workspace root has no `.git/`, so git commands must target individual repos)
- Identify which repos have local changes (`git status --short` is non-empty)
- If **one repo** has changes, target it silently
- If **multiple repos** have changes, use `AskUserQuestion` — header "Target repo", question "Multiple repos have local changes. Which repo should get the new branch?": list each repo as an option
- If **no repos** have changes: the user may be starting fresh. If an inline description or conversation context identifies a target repo, use it. If ambiguous, ask which repo to target. If no context at all, inform the user and stop

### 2. Gather Context

Record the current branch:

```bash
git rev-parse --abbrev-ref HEAD
```

Determine a meaningful description for the branch from the **first source that provides enough signal** (check in this priority order):

1. **Inline description** — if the user provided text with the invocation (e.g., `/optimus:branch "fix login timeout"`), use it directly
2. **Conversation context** — scan the current conversation for the user's task intent, problem description, or feature request. Extract the core action and subject.
3. **Git diff analysis** (only if sources 1 and 2 were insufficient) — check for local changes first:

```bash
git status --short
```

If there are local changes, analyze them to infer intent:

```bash
# File-level overview
git diff --stat
git diff --cached --stat

# Content details (for deeper analysis if file names alone are ambiguous)
git diff
git diff --cached
```

When analyzing diffs, look for:
- File paths that reveal the domain (e.g., `src/auth/` → authentication, `tests/` → testing)
- Test-only changes, documentation-only changes, config-only changes — these map directly to branch types in the shared reference

If **no source provides enough signal** to generate a meaningful name (no inline description, no conversation context, and either no local changes or changes too ambiguous to interpret), inform the user:

```
Could not determine a meaningful branch name from the conversation or local changes.
Provide a description, e.g., `/optimus:branch "add user authentication"`
```

Then **stop** — do not create a branch with a generic or meaningless name.

### 3. Derive Branch Name

Read `$CLAUDE_PLUGIN_ROOT/skills/commit/references/branch-naming.md` for the naming convention. Use the **Type Detection Keywords** section to determine `<type>` from context, and apply the **Slug Rules** to generate `<slug>`.

**Handle collisions**: if `git show-ref --verify --quiet refs/heads/<branch-name>` succeeds (branch exists), append `-2` to the slug. If that also exists, try `-3`, and so on up to `-9`. If all collide, inform the user and stop.

### 4. Create Branch

```bash
git checkout -b <branch-name>
```

Report (adapt based on whether local changes exist):

```
## Branch

Created `<branch-name>` from `<original-branch>`.
Local changes preserved (nothing committed or pushed).
```

If the working tree was clean (no local changes), omit the "Local changes preserved" line:

```
## Branch

Created `<branch-name>` from `<original-branch>`.
```

### 5. Next Step

Recommend the next step based on context:
- If the user seems to be starting new work → `/optimus:tdd` to build the feature test-first
- If changes look ready to commit → `/optimus:commit` to stage, commit, and optionally push
- If parallel work is needed → `/optimus:worktree` for an isolated workspace
- Default → `/optimus:commit` when ready

Tell the user the closing tip per `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md` "Closing tip wording" — use **Variant B** with `<continuation-skill(s)>` = `/optimus:commit` and `<non-continuation-examples>` = `/optimus:tdd`, `/optimus:worktree`, etc.

## Important

- **Preserve all local changes** — `git checkout -b` carries staged, unstaged, and untracked files to the new branch untouched. Do not run `git stash`, `git add`, `git reset`, or any command that alters the working tree or index
- Never commit or push
- Never modify any files
- This skill is a fast local operation — avoid unnecessary commands or questions
- Only use `AskUserQuestion` when multiple repos have changes or when context is truly insufficient
