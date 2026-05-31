---
description: Stages, commits, and optionally pushes local changes with a conventional commit message — analyzes diffs, generates the message, confirms with the user, and commits. On protected branches, offers to create a feature branch automatically. Multi-repo aware. Use when ready to commit work in one step.
disable-model-invocation: true
---

# Commit

Stage, commit, and optionally push local changes with a conventional commit message. Commits on the current branch — or, if the current branch is protected, offers to create a feature branch automatically.

## Workflow

### 1. Gather Change Context

Read `$CLAUDE_PLUGIN_ROOT/skills/commit/references/gather-changes.md` and follow the procedure (multi-repo detection + git commands).

### 2. Analyze Changes and Generate Conventional Commit Message

Read `$CLAUDE_PLUGIN_ROOT/skills/commit-message/references/conventional-commit-format.md` and follow its instructions to analyze the gathered changes and generate a conventional commit message.

If changes span multiple concerns, use `AskUserQuestion` to ask whether to commit everything together or split into separate commits. If splitting, process each commit separately through steps 3–7.

In a multi-repo workspace, process each repo with changes through steps 2–7 independently.

### 3. Handle Untracked Files

If `git status --short` shows untracked files (`??`):
- List them for the user
- Warn about any that look like secrets (`.env`, `*.key`, `*.pem`, `*.pfx`, `credentials.*`, `secrets.*`, `*.sqlite`, `*.db`)
- Use `AskUserQuestion` — header "Untracked files", question "Include these untracked files in the commit?":
  - **"Include all"** — stage all untracked files
  - **"Exclude all"** — stage only tracked files with changes
  - **"Let me choose"** — present each file individually

### 4. Branch and Push-Safety Check

Get the current branch:

```bash
git rev-parse --abbrev-ref HEAD
```

Check if `.claude/hooks/restrict-paths.sh` exists. In a multi-repo workspace, check two locations (child repo level first, then workspace root):

1. `<child-repo>/.claude/hooks/restrict-paths.sh`
2. `<workspace-root>/.claude/hooks/restrict-paths.sh`

Use the first one found (child repo level takes precedence). In a single-repo project, check `.claude/hooks/restrict-paths.sh` at the project root.

If found, read the file and extract the `PROTECTED_BRANCHES` array to determine whether the current branch is protected. Remember this result for step 5.

If the hook file does not exist at any checked location, assume the branch is safe for all operations.

#### Generate feature branch name (protected branches only)

If the current branch is protected, generate a feature branch name. Read `$CLAUDE_PLUGIN_ROOT/skills/commit/references/branch-naming.md` for the naming convention. The `<type>` comes from the conventional commit message generated in step 2; the `<description>` is the slugified subject line. Remember this name for step 5.

### 5. Preview and Confirm

Present a summary for each repo (in multi-repo, use a heading per repo — e.g., `## repo-name`):

- **Branch**: current branch name
- **Commit message**: the full generated conventional commit message (subject line + body when the body is present — never truncate to subject-only)
- **Files**: list of files that will be staged

Then use `AskUserQuestion` — header "Action", question "How would you like to proceed?":

**If the current branch is NOT protected:**

- **"Commit and push"** — commit and push to the current branch
- **"Commit only"** — commit without pushing
- **"Edit message"** — let the user provide an adjusted message, then re-present this step
- **"Cancel"** — abort without making any changes

**If the current branch IS protected** (replace the first two options with feature-branch alternatives):

- **"Create branch `<name>`, commit, and push"** — create a new feature branch from the current branch, switch to it, commit, and push
- **"Create branch `<name>` and commit only"** — create a new feature branch, switch to it, and commit without pushing
- **"Edit message"** — let the user provide an adjusted message, regenerate the feature branch name (step 4), then re-present this step
- **"Cancel"** — abort without making any changes

### 6. Stage and Commit

If the user chose a "Create branch" option in step 5, create and switch to the feature branch first:

```bash
git checkout -b <branch-name>
```

If branch creation fails (e.g., the branch already exists), report the error and let the user choose a different name or cancel.

Stage the files determined in steps 1 and 3:

```bash
git add <specific files>
```

Prefer `git add <specific files>` over `git add -A`. Never stage files that look like secrets.

Commit with the confirmed message. Use a heredoc to preserve multi-line messages (subject + body):

```bash
git commit -m "$(cat <<'EOF'
<message>
EOF
)"
```

If the commit fails for any reason, report the error to the user and stop — do not proceed to the push step.

### 7. Push (if requested)

Only if the user chose an option that includes pushing in step 5:

```bash
git push
```

If there is no upstream tracking branch:

```bash
git push -u origin <branch>
```

If the push fails for any reason, report the error to the user.

### 8. Report and Next Step

Present a summary of what was done (in a multi-repo workspace, show a combined summary across all repos):
- Created branch: `<branch-name>` (only if a feature branch was created in step 6)
- Committed: `<short-hash> <commit message>` (per repo in multi-repo)
- Pushed to: `origin/<branch>` (if push was performed)

If a feature branch was created, inform the user: "You are now on `<branch-name>`. You can keep working on this branch, or use `/optimus:pr` to create a pull request."

Otherwise, recommend the next step based on readiness:
- If a pull request is needed → `/optimus:pr` to create or update a PR.
- Otherwise → the commit is complete; suggest continuing work on this branch (or running `/optimus:code-review` once more changes accumulate). Then emit the closing tip per `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md` "Closing tip wording" — use **Variant C** (default).

When `/optimus:pr` is the recommended next step (either branch above), emit the closing tip per `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md` "Closing tip wording" — use **Variant A** with `<continuation-skill(s)>` = `/optimus:pr` and `<non-continuation-examples>` = `/optimus:code-review`, etc.
