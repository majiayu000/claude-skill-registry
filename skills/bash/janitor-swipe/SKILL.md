---
name: janitor-swipe
description: "Tinder for your Claude Code skills. Reviews a sorted deck of every installed skill and lets you swipe keep / delete / skip on each one. Use when the user wants to bulk-clean their skill collection, triage unused skills, or do interactive skill cleanup."
metadata:
  version: 1.4.0
---

# Janitor Swipe — interactive skill triage

A bash TUI that puts every installed skill into a sorted deck and lets the user swipe keep / delete / skip on each card. The deck is sorted "most likely waste first" — heavy, never-used skills appear at the top, so most users hit `← delete` a few times and quit before reviewing the whole list.

## How to Run

**Important:** the swipe TUI needs an interactive terminal. Inside Claude Code, the Bash tool's stdin is non-interactive, so the keypress reader can't work. The user must invoke it via the `!` prefix so the command runs in their actual shell:

```
!bash ~/.claude/skills/skills-janitor/scripts/swipe.sh
```

When the user asks for `/janitor-swipe`, tell them to run that command in their terminal. Do NOT try to run it yourself via the Bash tool — it will error with "needs an interactive terminal".

## What the User Sees

Each card shows:
- Skill name + position in deck (e.g. `[3 / 47]`)
- Token cost (raw + % of context budget)
- Usage count and last invoked date
- Scope (`user`, `project`, `plugin · <plugin-name>`, etc.)
- 3-line truncated description
- Verdict label (e.g. *"Heavy + unused — likely dead weight"*)

Controls:
- `←` / `h` / `d` — stage for delete
- `→` / `l` / `k` — keep
- `↓` / `j` / `s` / space — skip
- `u` — undo (back up one card, clear its decision)
- `i` — inspect (show full SKILL.md description)
- `q` / Esc — quit (still shows summary for decisions made so far)

## Scope-Aware Behavior

This is the critical correctness point — the swipe doesn't lie about what it can delete:

| Scope | What happens on swipe left |
|---|---|
| `user`, `project`, `codex-user`, `codex-project` | Path is staged for `rm -rf` (or unlink if symlink) |
| `plugin`, `plugin-source` | NOT deleted — flagged under "Plugins to review" at the apply screen, with a hint to run `/plugin uninstall <plugin>` if enough skills from that plugin were swiped |

## Apply Screen

After the last card (or `q`), the user sees a summary and is prompted:

- `y` — apply deletions immediately
- `N` — cancel
- `save` — write decisions to `~/.skills-janitor/swipe-<timestamp>.json` for later application via `swipe.sh --apply <file>`

Every deletion is logged to `~/.skills-janitor/log.jsonl` with the path and frontmatter snapshot.

## Edge Cases

- No skills installed → exits 0 with a message
- Terminal < 50 cols or < 22 rows → exits 1 with a message
- No TTY → exits 1 with a message pointing the user at `/janitor-report` or `/janitor-value` for list-form output
- Symlinks → `rm` the link itself, never follow to the target

## Related Skills

- `/janitor-report` — same data as a non-interactive list
- `/janitor-value` — combined token + usage view (the data underneath the swipe deck)
- `/janitor-fix --prune` — automated broken-symlink cleanup, no interactive review
