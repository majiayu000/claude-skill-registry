---
name: sync-dotfiles
description: Sync Cursor skills, agents, rules, and other dotfiles to chezmoi. Use when the user asks to update dotfiles (pull + apply), sync dotfiles, update chezmoi, or push dotfiles; or automatically after creating, editing, or deleting files in ~/.cursor/skills/, ~/.cursor/agents/, or ~/.cursor/rules/.
---

# Sync Dotfiles to chezmoi

**Reference:** See [chezmoi-docs.md](./chezmoi-docs.md) in this skill for command reference.

Choose the right flow from user intent:

## Update vs sync

| User says… | Meaning | Do this |
|------------|--------|--------|
| **Update dotfiles**, pull dotfiles, get latest dotfiles | Fetch from remote and apply | Run **`chezmoi update`** (see [chezmoi-docs.md](./chezmoi-docs.md)). Done. |
| **Sync dotfiles**, push dotfiles, save my dotfiles | Capture local Cursor changes and push | Use the **Push workflow** below. |

## Trigger Conditions

Run this skill **automatically** (without being asked) whenever you have just:
- Created, edited, or deleted a file in `~/.cursor/skills/`
- Created, edited, or deleted a file in `~/.cursor/agents/`
- Created, edited, or deleted a file in `~/.cursor/rules/`

Also run when the user explicitly asks to **update** dotfiles, **sync** dotfiles, **push** dotfiles, or update chezmoi.

## Push workflow (sync / push dotfiles)

When the user wants to save local Cursor changes to the dotfiles repo, use **chezmoi only** (no raw `git` or `cd` to source). All git runs via `chezmoi git` in the source directory.

1. **Capture local changes**

   ```bash
   chezmoi re-add ~/.cursor/skills ~/.cursor/agents ~/.cursor/rules
   ```

   If only skills changed, scope to that path. For new untracked files use `chezmoi add PATH`.

2. **Stage and commit**

   ```bash
   chezmoi git add -A
   chezmoi git -- diff --cached --quiet || chezmoi git -- commit -m "chore: sync cursor config"
   ```

   Use a more specific message when clear (e.g. `chore: add new skill foo-bar`). Put `--` before git flags so chezmoi doesn’t interpret them.

3. **Pull remote and rebase**

   ```bash
   chezmoi git -- pull --rebase
   ```

   Local changes are already committed, so rebase keeps both sides.

4. **Apply merged state**

   ```bash
   chezmoi apply
   ```

5. **Push**

   ```bash
   chezmoi git push
   ```

## Notes

- Never commit files outside `dot_cursor/` without explicit user request.
- If `chezmoi re-add` fails on a new file (not yet tracked), use `chezmoi add` instead.
