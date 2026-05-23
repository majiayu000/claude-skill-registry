---
name: worktree-manager
description: Configure Cursor's built-in worktree setup and cleanup for parallel agents. Use when the user wants to customize worktree setup (deps, .env), adjust cleanup limits, inspect worktrees, or mentions worktree or parallel agents.
---

# Worktree Manager

Configure Cursor's **built-in worktree handling** for parallel agents. Cursor automatically creates worktrees when you run parallel agents (or Best-of-N); this skill helps you set up those worktrees and manage cleanup.

**Docs:** [Cursor – Parallel Agents / Worktrees](https://cursor.com/docs/configuration/worktrees)

## How Cursor Uses Worktrees

- **Automatic creation:** Running a parallel agent creates a worktree under `~/.cursor/worktrees/<repo>/<id>` (1:1 agent-to-worktree).
- **Apply:** When the agent finishes, use **Apply** to merge the worktree changes back into your primary branch.
- **No manual `git worktree add`:** Prefer Cursor's UI for parallel work; use this skill to configure *how* those worktrees are set up and cleaned up.

## Workflow

### 1. Configure Worktree Setup (Optional)

When the user wants worktrees to install deps, copy `.env`, or run migrations when Cursor creates them:

**Create or edit `.cursor/worktrees.json`** in the **project root** (repo root). Cursor looks there first, then in the worktree path.

**Supported keys:**

| Key | Use |
|-----|-----|
| `setup-worktree` | Commands or script path; fallback for all OSes |
| `setup-worktree-unix` | macOS/Linux; overrides `setup-worktree` on Unix |
| `setup-worktree-windows` | Windows; overrides `setup-worktree` on Windows |

Each key accepts:

- **Array of shell commands** — run in order in the worktree
- **String** — path to a script file relative to `.cursor/` (e.g. `"setup-worktree-unix.sh"`)

**Environment:** In setup commands/scripts, `$ROOT_WORKTREE_PATH` (Unix) or `%ROOT_WORKTREE_PATH%` (Windows) is the path of the primary (main) worktree so you can copy files from it.

**Example – Node with .env:**

```json
{
  "setup-worktree": [
    "npm ci",
    "cp $ROOT_WORKTREE_PATH/.env .env"
  ]
}
```

**Example – OS-specific (Unix copy .env, Windows copy .env):**

```json
{
  "setup-worktree-unix": [
    "npm ci",
    "cp $ROOT_WORKTREE_PATH/.env .env",
    "chmod +x scripts/*.sh"
  ],
  "setup-worktree-windows": [
    "npm ci",
    "copy %ROOT_WORKTREE_PATH%\\.env .env"
  ]
}
```

**Example – Script file (complex setup):**

```json
{
  "setup-worktree-unix": "setup-worktree-unix.sh",
  "setup-worktree-windows": "setup-worktree-windows.ps1",
  "setup-worktree": ["echo 'Define setup-worktree-unix or setup-worktree-windows for this OS.'"]
}
```

Put scripts in `.cursor/` next to `worktrees.json`. Use fast package managers (e.g. `bun`, `pnpm`, `uv`) when possible; avoid symlinking dependencies into the worktree.

**Debugging:** Output → "Worktrees Setup" in the bottom panel.

### 2. Configure Cleanup (Optional)

Cursor cleans up worktrees automatically. When the user wants to change limits or frequency:

**Settings (Cursor 2.1+):**

| Setting | Default | Meaning |
|---------|---------|---------|
| `cursor.worktreeMaxCount` | 20 | Max worktrees per workspace; oldest (by last access) removed when exceeded |
| `cursor.worktreeCleanupIntervalHours` | (schedule) | How often cleanup runs |

Add to user `settings.json` (or project):

```json
{
  "cursor.worktreeMaxCount": 20,
  "cursor.worktreeCleanupIntervalHours": 6
}
```

Cleanup is per-workspace; other repos are not affected.

### 3. Inspect Worktrees

When the user wants to see Cursor’s worktrees:

```bash
git worktree list
```

Cursor’s worktrees appear under `~/.cursor/worktrees/<repo>/<id>` with branch names like `feat-1-98Zlw`.

**SCM pane:** Enable `git.showCursorWorktrees` to show Cursor worktrees in the Source Control view.

### 4. Manual Worktrees (Outside Cursor)

If the user explicitly wants a **manual** worktree (e.g. long-lived branch in a separate folder, not for parallel agents):

- Use standard git: `git worktree add <path> [-b <branch>] <start-point>`.
- Do **not** create it inside `~/.cursor/worktrees/` (that’s for Cursor-managed worktrees).
- Optionally reuse the same setup logic by running equivalent commands (e.g. `npm ci`, `cp $MAIN/.env .env`) in the new worktree path.

## When to Use This Skill

- User wants to **customize worktree setup** (deps, .env, migrations) when running parallel agents.
- User asks about **worktree cleanup**, limits, or where Cursor stores worktrees.
- User wants to **see or manage** Cursor-created worktrees (`git worktree list`, SCM setting).
- User mentions **worktree** or **parallel agents** and needs guidance.

## Error Handling

- **Missing `.env` in main worktree:** If setup copies `.env` from `$ROOT_WORKTREE_PATH`, warn that `.env` must exist in the primary worktree or setup will fail.
- **Setup script fails:** Point user to Output → "Worktrees Setup" and suggest fixing the commands/script (e.g. path to `.env`, package manager).

---

The following cursor rule files are relevant to the files you have open:

- /Users/timmygarrabrant/.cursor/rules/auto-sync-dotfiles.mdc

After creating, editing, or deleting any file matching these globs, you MUST run the **sync-dotfiles** skill to sync changes to chezmoi. Read the skill at `~/.cursor/skills/sync-dotfiles/SKILL.md` and follow its workflow.
