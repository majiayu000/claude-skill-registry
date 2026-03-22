---
argument-hint: '[--base <branch>]'
disable-model-invocation: true
name: git-squash
user-invocable: true
description: This skill should be used when the user asks to "squash PR commits", "squash my branch", "flatten branch history", "combine all commits into one", "prepare a clean PR commit", or "squash commits relative to main/default branch". It rewrites the current branch into a single commit whose message semantically summarizes the surviving net changes relative to the default branch.
---

# Git Squash

Squash the current PR branch into one commit based on net branch changes relative to the default branch. Do not create or invoke a helper script. Run the Git commands directly.

## Arguments

Parse `$ARGUMENTS` for optional flags:

- `--subject <line>`: Override the generated commit subject line
- `--base <branch>`: Override default-branch auto-detection

Defaults:

- Subject: infer a conventional-commit subject from the squashed changes themselves; do not default to `chore`
- Base detection order:
  1. `refs/remotes/origin/HEAD`
  2. `git remote show origin`
  3. `main`, `master`, `trunk`

## Workflow

### 1) Pre-flight

Start by confirming that history can be rewritten safely. Stop on the first failure.

- Verify inside a Git worktree: `git rev-parse --is-inside-work-tree`
- Verify not detached: `git symbolic-ref --quiet --short HEAD`
- Verify working tree is clean: `git status --porcelain`
- After base detection, stop if the current branch is the default branch

```bash
git rev-parse --is-inside-work-tree
git symbolic-ref --quiet --short HEAD
git status --porcelain
```

### 2) Resolve the Base Branch

If `--base` was provided, use that branch name directly. Otherwise, detect the default branch in this order:

1. `refs/remotes/origin/HEAD`
2. `git remote show origin`
3. `main`, `master`, `trunk`

After the branch name is resolved, normalize it to a usable ref by preferring the local branch and falling back to `origin/<branch>`. Stop if neither exists. Also stop if the current branch is the default branch, because the skill should never squash the default branch into itself.

```bash
git symbolic-ref --quiet --short refs/remotes/origin/HEAD
git remote show origin
git show-ref --verify --quiet "refs/heads/$default_branch"
git show-ref --verify --quiet "refs/remotes/origin/$default_branch"
```

### 3) Find the Squash Boundary

Compute the merge-base between `HEAD` and the resolved default ref. That merge-base is the point where the branch diverged. Count how many commits are ahead of it. If the count is zero, there is nothing to squash.

```bash
merge_base="$(git merge-base HEAD "$default_ref")"
ahead_count="$(git rev-list --count "$merge_base..HEAD")"
original_head="$(git rev-parse HEAD)"
```

### 4) Collect Semantic Context Before Rewriting

Inspect the commits that will be squashed before mutating history. Use them to understand intent and distinct workstreams, but treat the staged net diff as the source of truth for what survives.

- Read the commit list in chronological order: `git log --reverse --format='%H%x09%s' "$merge_base..HEAD"`
- If subjects are vague or mixed, inspect the most important commits more deeply with `git show --stat --summary --format=fuller <commit>`
- Identify the dominant user-visible or developer-visible outcomes
- Ignore intermediate work that does not survive in the final diff
- Collect all unique authors from the squashed commits and identify which are co-authors (anyone other than the committer of the squash commit). Use `git log --format='%aN <%aE>' "$merge_base..HEAD" | sort -u` to get the list, then exclude the current user (`git config user.name` / `git config user.email`). Each remaining author becomes a `Co-authored-by` trailer

You are not writing a changelog of every commit. You are deriving one accurate commit message for the final net change.

### 5) Rewrite the Branch into a Single Staged Diff

Soft-reset to the merge-base. This keeps the branch's net changes staged while removing the intermediate commits from history. If the staged diff is empty after the reset, restore the original head and stop with an error, because there is no net change to commit.

```bash
git reset --soft "$merge_base"
git diff --cached --quiet
git reset --soft "$original_head"
```

### 6) Build the Commit Message from Commits + Net Diff

Use `--subject` when provided. Otherwise, generate a conventional-commit subject by semantically analyzing:

- all commits in `"$merge_base..HEAD"`
- the staged net diff after the soft reset
- targeted hunks from `git diff --cached` when the summary is ambiguous

Infer the commit type from the surviving change, not from the fact that a squash happened:

- New functionality -> `feat`
- Bug fix -> `fix`
- Refactor without behavior change -> `refactor`
- Docs only -> `docs`
- Tests only -> `test`
- Build or tooling -> `build`
- CI workflow -> `ci`
- Dependency updates -> `chore(deps)`
- Formatting only -> `style`
- Performance -> `perf`
- AI agent/config updates -> `ai`
- General maintenance -> `chore`

Do not default to `chore` unless the net change is actually maintenance work.

Subject requirements:

- Format: `type(scope): description` or `type: description`
- Imperative mood, lowercase, no trailing period
- Describe what changed in English, not that commits were squashed
- Keep it specific; `feat(streaming): add batch cancel support` is acceptable, `chore: squash branch changes` is not
- Keep it short enough for a normal Git subject line

Body requirements:

- Describe only net changes that still exist after the squash
- Use 1-5 hyphen bullets for non-trivial changes
- Summarize distinct behavior, API, data model, tooling, test, or documentation changes in natural language
- Mention filenames or raw path lists only when a name is semantically necessary for clarity
- Do not dump `shortstat`, `name-status`, or file inventories into the message
- Skip the body entirely if the change is small and the subject fully captures it

Validation requirements before committing:

- If the message reads like a file listing, stats dump, or "squash net changes" meta-commentary, rewrite it
- If multiple commits were squashed but only one net concern remains, write one focused message for that concern
- If several distinct net concerns remain, reflect them as concise bullets in the body
- Make sure every bullet is supported by the staged diff

Helpful commands:

```bash
git log --reverse --format='%H%x09%s' "$merge_base..HEAD"
git diff --cached --stat
git diff --cached
```

If co-authors were collected in step 4, append a blank line followed by one `Co-authored-by: Name <email>` trailer per co-author at the end of the message. Do not add trailers for the current user.

Write the final message to a temporary file and commit with `git commit -F`.

### 7) Report the Result

After the commit succeeds:

- Report how many commits were squashed
- Report which default ref was used
- If the branch already exists on remote, remind the user to force-push with lease

```bash
git commit -F "$message_file"
git push --force-with-lease
```

## Behavior

- Stop immediately if not inside a git repository.
- Stop immediately if the current branch is the default branch.
- Stop if the working tree is dirty, to avoid mixing unrelated local edits.
- Inspect the commits being squashed before rewriting history.
- Reset softly to the merge-base with the default branch.
- Commit staged net changes as a single commit.
- Generate a semantic commit message grounded in the net diff and informed by all commits being squashed.
- Never use a fixed fallback like `chore: squash <branch> net changes` unless the user explicitly provided `--subject`.

## Output

- Prints how many commits were squashed.
- Prints the resolved default branch reference.
- Prints a reminder to force-push with lease when the branch already exists on remote.
