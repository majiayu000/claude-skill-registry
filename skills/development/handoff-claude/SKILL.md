---
name: handoff-claude
description: Delegate tasks to other authorized Claude Code instances (separate accounts/profiles like claude-z-1, claude-z-2) via headless `claude -p`. Use when you need parallel execution on a second account's quota, account isolation, or background workers that don't consume this session's context.
user-invocable: true
---

# Handoff to Another Claude Code Instance

Delegate tasks to **other Claude Code instances running under different accounts** (e.g. `claude-z-1`, `claude-z-2`, `claude-z-3`) using headless mode (`claude -p`). Each instance has its own authorization, quota, and session state — they never conflict with your current session.

---

## When to Use

| Use another Claude instance for | Keep in this session |
|--------------------------------|----------------------|
| Parallel independent tasks (fan-out) | The task you're actively directing |
| Work billed to a different account/quota | Anything needing this session's context |
| Long background jobs (tests, refactors) | Architecture decisions |
| Isolated experiments (different config/permissions) | Final review & merge |

**vs `/handoff-codex` / `/handoff-gemini`:** use those to leverage a *different model vendor's* strengths; use `/handoff-claude` when you want *full Claude Code capability* (tools, hooks, skills) on a separate account.

---

## One-Time Setup (per profile)

Each profile is just a separate `CLAUDE_CONFIG_DIR`. Credentials, session history, and settings are fully isolated per directory. Per the official docs, `CLAUDE_CONFIG_DIR` is the supported multi-account isolation mechanism: it scopes `settings.json`, the `projects/` directory (session history), and authentication (`.claude.json`) into that profile's directory — so profiles never share config, sessions, or logins.

### 1. Create a wrapper command

```bash
mkdir -p ~/bin ~/.claude-profiles

cat > ~/bin/claude-z-1 << 'EOF'
#!/usr/bin/env bash
# Claude Code profile "z-1" — isolated auth, sessions, and settings
CLAUDE_CONFIG_DIR="$HOME/.claude-profiles/z-1" exec claude "$@"
EOF
chmod +x ~/bin/claude-z-1

# Ensure ~/bin is on PATH (add to ~/.zshrc or ~/.bashrc if missing)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
```

Repeat for `claude-z-2`, `claude-z-3`, ... (one wrapper + one config dir each).

### 2. Authenticate the profile (once)

```bash
claude-z-1 auth login     # opens browser — sign in with that profile's account
claude-z-1 auth status    # verify: should show loggedIn: true + the account email
```

> Each config dir stores its own credentials. Logging in to `claude-z-1` never touches your default `~/.claude` login or any other profile.

### 3. Verify isolation

```bash
claude auth status        # your default account
claude-z-1 auth status    # profile z-1's account — different login, no conflict
```

---

## Delegating Tasks

### Single task (headless)

```bash
claude-z-1 -p "Add input validation to src/api/users.ts, then run the tests" \
  --permission-mode acceptEdits \
  --output-format json
```

- `-p / --print` — run non-interactively, print result, exit
- `--permission-mode acceptEdits` — auto-approve file edits (keep command approval)
- `--output-format json` — machine-readable result (or `text`, `stream-json`)
- `--model sonnet` — optionally pin a cheaper/faster model for simple tasks
- `--add-dir <path>` — grant the child access to an extra directory beyond its working directory

### Parallel fan-out without conflicts

Auth/session state never conflicts (separate config dirs). For **file** conflicts in the same repo, give each instance its own git worktree:

```bash
git worktree add ../proj-task-a -b task-a
git worktree add ../proj-task-b -b task-b

(cd ../proj-task-a && claude-z-1 -p "Implement feature A per docs/spec-a.md" --permission-mode acceptEdits) > /tmp/task-a.log 2>&1 &
(cd ../proj-task-b && claude-z-2 -p "Implement feature B per docs/spec-b.md" --permission-mode acceptEdits) > /tmp/task-b.log 2>&1 &
wait

# Review each branch, then merge
git worktree list
```

### Check results

```bash
# JSON output includes result, cost, duration, session_id
jq -r '.result' /tmp/task-a.log

# Resume a delegated session interactively if it needs guidance
claude-z-1 --resume    # picker shows that profile's sessions only
```

---

## Handoff Checklist

1. **Prepare context** — headless instances don't share your conversation. Put requirements in a file (`docs/spec-a.md`) or inline in the prompt.
2. **Pick isolation level** — same directory is fine for read-only/analysis tasks; use a worktree when the task writes files you're also touching.
3. **Set permissions deliberately** — prefer `--permission-mode acceptEdits`. Use `--dangerously-skip-permissions` only in sandboxes/containers you trust.
4. **Collect & review** — always review delegated diffs (`git -C ../proj-task-a diff main`) before merging.

---

## Notes & Limits

- Running `claude -p` from inside a Claude Code session works (child processes are marked with `CLAUDECODE` / `CLAUDE_CODE_CHILD_SESSION` env vars and are fully independent), though nesting isn't formally documented — treat as inferred capability.
- Each profile consumes **its own account's quota/plan** — that's the point, but confirm the account is authorized for the work you delegate.
- Profiles do not share MCP servers, plugins, or settings unless you configure them in that profile's config dir (or pass `--settings` / `--mcp-config` per call).
- Don't run two instances in auto-loop mode on the same `.auto-loop/` state directory — one loop per worktree.
