---
name: worktree-sync
description: "Sync all git worktrees and Claude Code settings across machines — use at start or end of day to checkpoint work. Commits uncommitted changes with contextual WIP messages, pulls with rebase, pushes, and reports conflicts for resolution."
user-invocable: true
allowed-tools: ["Bash(git add *)", "Bash(git commit *)", "Bash(git -C * add *)", "Bash(git -C * commit *)", "Bash(git -C * pull *)", "Bash(git -C * push *)", "Bash(git -C * rebase *)", "Bash(git pull *)", "Bash(git push *)", "Bash(git rebase *)", "Bash(git worktree *)", "Bash(~/.claude/bin/claude-sync *)", "Bash(uvx cc-search-chats:*)", "Bash(claude update *)", "Bash(~/.claude/bin/plugin-refresh *)"]
---

# Worktree Sync

Checkpoint all git worktrees and Claude Code settings in one operation. Designed for multi-machine development — push all work before leaving one machine, pull it on another.

## Subagent Autonomy Boundary

Subagents cannot consult the user. Err on the side of halting.

**Subagents do (local, reversible):**
- Check worktree status
- Gather context via cc-search-chats
- Stage and commit WIP locally

**Subagents do NOT (remote-visible, irreversible, or requires judgment):**
- Push to remote
- Resolve rebase conflicts
- Force anything
- Make decisions about detached HEADs, missing upstreams, or unexpected state

**If anything unexpected happens, the subagent STOPS and reports back.** The main agent presents ALL results to the user before taking any remote-visible action.

## Workflow

Execute these steps in order. Do not skip steps.

### Step 1: Discover Worktrees

```bash
git worktree list
```

Parse each line to extract the worktree path and branch name. Every listed worktree participates in the sync (including the main worktree). If a worktree has a detached HEAD, note it for the summary but do not launch a subagent for it.

### Step 2: Pull Claude Code Settings and Update CLI

```bash
~/.claude/bin/claude-sync pull
```

If `~/.claude/bin/claude-sync` is not found, warn and skip. Continue with git sync.

After settings are pulled, update the Claude CLI and refresh plugins:

```bash
claude update 2>&1 || echo "warning: claude update failed"
~/.claude/bin/plugin-refresh 2>&1 || echo "warning: plugin-refresh failed"
```

`claude update` downloads the latest CLI binary (takes effect on next launch). `plugin-refresh` pulls latest marketplace sources, clears plugin cache, and reinstalls all plugins — see `~/.claude/bin/plugin-refresh` for details. Both are non-fatal; warn and continue if either fails.

### Step 3: Gather State and Commit WIP (Parallel Subagents)

Launch one Task agent per worktree, all in a **single message** for parallel execution. Use `subagent_type: "denubis-basic-agents:haiku-general-purpose"`.

Each subagent gathers state and commits locally. It does NOT pull or push.

Give each subagent this prompt (substitute the worktree path and branch name):

<worktree-sync-agent-prompt>
Gather state and checkpoint the git worktree at `{WORKTREE_PATH}` on branch `{BRANCH_NAME}`.

You are preparing this worktree for sync. You handle LOCAL operations only. Do NOT pull, push, or interact with the remote.

Execute these steps in order. If any step fails unexpectedly, STOP and report the error.

**1. Check for uncommitted changes:**

```bash
git -C {WORKTREE_PATH} status --porcelain
```

**2. Check remote tracking status:**

```bash
git -C {WORKTREE_PATH} rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>&1
```

Report whether the branch has an upstream or not.

**3. If there are uncommitted changes, check for sensitive files:**

```bash
git -C {WORKTREE_PATH} status --short
```

Scan the file list for sensitive patterns: `.env`, `credentials`, `secret`, `.key`, `.pem`, `token`. If ANY match, STOP — do not stage or commit. Report `STATUS: SENSITIVE_FILES` with the list of flagged files, so the main agent can ask the user.

**4. If no sensitive files, gather context and commit:**

Search for recent session context about this branch:

```bash
uvx cc-search-chats search "{BRANCH_NAME}" --days 7 --json 2>/dev/null || echo "NO_RESULTS"
```

Check what files changed:

```bash
git -C {WORKTREE_PATH} diff --stat
git -C {WORKTREE_PATH} diff --cached --stat
```

Stage all changes:

```bash
git -C {WORKTREE_PATH} add -A
```

Commit with a contextual WIP message. The commit message MUST follow this structure:
- First line: `WIP: {BRANCH_NAME} — {1-sentence summary of work in progress}`
- Blank line
- Body: 2-3 bullet points describing what changed, drawn from cc-search-chats context and/or git diff --stat
- If cc-search-chats returned nothing, describe changes from the diff stat only
- End with the co-author line

Use a HEREDOC for the message:

```bash
git -C {WORKTREE_PATH} commit -m "$(cat <<'EOF'
WIP: {BRANCH_NAME} — {summary}

- {detail 1}
- {detail 2}

Automatic checkpoint commit.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

**5. Report:**

Return a structured report with ALL of these fields:

```
WORKTREE: {WORKTREE_PATH}
BRANCH: {BRANCH_NAME}
HAS_UPSTREAM: yes | no
STATUS: CLEAN | COMMITTED | SENSITIVE_FILES | ERROR
COMMITTED_FILES: {list of files, or "none"}
SENSITIVE_FILES: {list of flagged files, or "none"}
ERROR_DETAIL: {description if ERROR, or "none"}
```

If CLEAN: no local changes were found, nothing to commit.
If COMMITTED: local changes were staged and committed. List the files.
If SENSITIVE_FILES: uncommitted changes include sensitive-looking files. List ALL uncommitted files and flag which ones triggered the halt. Do not stage or commit anything.
If ERROR: something unexpected happened. Describe it.
</worktree-sync-agent-prompt>

### Step 4: Present Results to User

After all subagents complete, present a summary table:

| Worktree | Branch | Local Status | Has Upstream | Committed Files |
|----------|--------|--------------|--------------|-----------------|
| /path/to/main | main | CLEAN | yes | — |
| /path/to/.worktrees/feature | feature | COMMITTED | yes | 3 files |

For any COMMITTED worktrees, list the committed files.

For any SENSITIVE_FILES worktrees, show the flagged files and ask the user:
- Include all files (stage and commit everything)
- Exclude sensitive files (add them to `.gitignore` or stage selectively)
- Skip this worktree entirely

If the user chooses to include or exclude, the main agent handles the commit directly (not a subagent) since this requires judgment.

For any ERROR worktrees, show the error details and ask the user how to proceed.

**Ask the user:** "Ready to pull --rebase and push all worktrees?" Wait for confirmation before proceeding.

### Step 5: Pull and Push (Main Agent, Sequential)

For each worktree that the user confirmed, execute in the main agent context (NOT in subagents):

**5a. Pull with rebase:**

```bash
git -C {WORKTREE_PATH} pull --rebase
```

If the pull succeeds cleanly, proceed to 5b.

If the pull fails due to rebase conflicts:
1. **DO NOT** abort the rebase automatically
2. Show the user which files conflict:
   ```bash
   git -C {WORKTREE_PATH} diff --name-only --diff-filter=U
   ```
3. Ask the user how they want to proceed:
   - Resolve conflicts now (help them file by file)
   - Abort the rebase (`git -C {path} rebase --abort`) and defer
4. If resolving: help with each file, stage resolved files, `git rebase --continue`, then push
5. If aborting: note the branch needs attention later, move to next worktree

**5b. Push:**

```bash
git -C {WORKTREE_PATH} push
```

If the branch has no upstream:

```bash
git -C {WORKTREE_PATH} push -u origin {BRANCH_NAME}
```

If push is rejected (non-fast-forward), tell the user and ask how to proceed. Never force push.

### Step 6: Push Claude Code Settings

After all worktrees are synced:

```bash
~/.claude/bin/claude-sync push
```

### Step 7: WIP Audit

After all worktrees are synced, check for stray WIP commits that shouldn't be there. WIP commits on feature branches are expected (they'll be squashed at merge). WIP commits on main or merged branches are problems.

**7a. Check main/protected branches for WIP commits:**

```bash
git -C {MAIN_WORKTREE} log --oneline --grep="^WIP:" -20
```

If any WIP commits are on main, warn the user: "Found N WIP commits on main. These may have been merged without squashing."

List them so the user can decide whether to revert or squash them.

**7b. Check for merged branches with lingering WIP commits:**

```bash
git branch --merged main
```

For each merged branch (excluding main itself), check for WIP commits:

```bash
git log --oneline --grep="^WIP:" main..{BRANCH_NAME}
```

If a merged branch has WIP commits AND is fully merged into main, it's stale — the branch can be deleted. Report: "Branch `{name}` is fully merged into main but still exists with N WIP commits. Safe to delete."

Ask the user if they want to clean up stale merged branches (delete local + remote tracking).

### Step 8: Final Summary

Present the final state of all worktrees:

| Worktree | Branch | Result |
|----------|--------|--------|
| /path/to/main | main | Synced |
| /path/to/.worktrees/feature | feature | Synced (3 files committed) |
| /path/to/.worktrees/other | other | Deferred — rebase conflict |

Note any deferred conflicts that need attention in a future session.

## Edge Cases

| Situation | Action |
|-----------|--------|
| Detached HEAD | Skip, warn user in summary |
| No remote tracking | Report in summary, ask user before push -u |
| Empty worktree list | Report "no worktrees found", run only claude-sync |
| cc-search-chats unavailable | Subagent falls back to `git diff --stat` for commit context |
| `~/.claude/bin/claude-sync` not found | Warn and skip settings sync, continue with git |
| Worktree path doesn't exist | Report ERROR, skip, continue with others |
| Sensitive files detected | Subagent halts before staging. Main agent asks user: include, exclude, or skip |
