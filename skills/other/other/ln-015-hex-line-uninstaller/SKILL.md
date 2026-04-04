---
name: ln-015-hex-line-uninstaller
description: "Removes hex-line hooks, output style, and cached files from the system. Use when hex-line MCP needs to be fully uninstalled."
license: MIT
model: claude-haiku-4-5
---

> **Paths:** File paths are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# Hex-Line Uninstaller

**Type:** L3 Worker
**Category:** 0XX Shared

Removes all hex-line artifacts from the system. Standalone — no coordinator dependency.

---

## What It Removes

| Artifact | Location | Action |
|----------|----------|--------|
| Hook script | `~/.claude/hex-line/hook.mjs` | Delete file |
| Hook entries | `~/.claude/settings.json` → `hooks` | Remove entries matching "hex-line" signature |
| Output style file | `~/.claude/output-styles/hex-line.md` | Delete file |
| Output style setting | `~/.claude/settings.json` → `outputStyle` | Clear only if value is `"hex-line"` |
| Hook directory | `~/.claude/hex-line/` | Delete if empty after hook removal |

---

## Steps

### 1. Remove hook entries from settings.json

```
Read ~/.claude/settings.json
For each event in hooks (SessionStart, PreToolUse, PostToolUse):
  Find entry where hooks[].command contains "hex-line"
  Remove that entry
  If event array is empty, delete the key
If hooks object is empty, delete it
Write back
```

### 2. Clear output style

```
If settings.json.outputStyle === "hex-line":
  Delete the outputStyle key
  Write back
```

### 3. Delete installed files

```bash
rm -f ~/.claude/hex-line/hook.mjs
rmdir ~/.claude/hex-line 2>/dev/null   # only if empty
rm -f ~/.claude/output-styles/hex-line.md
```

### 4. Verify

```bash
# Confirm no hex-line references remain
grep -r "hex-line" ~/.claude/settings.json || echo "Clean"
test ! -f ~/.claude/hex-line/hook.mjs && echo "Hook removed"
test ! -f ~/.claude/output-styles/hex-line.md && echo "Style removed"
```

---

## Notes

- Does NOT remove the MCP server itself (`npm uninstall -g @levnikolaevich/hex-line-mcp` is separate)
- Does NOT touch per-project `.claude/settings.local.json` (autoSync already cleans those)
- Safe to run multiple times (idempotent)
- After uninstall, restart Claude Code for changes to take effect

## Definition of Done

- [ ] No hex-line entries in `~/.claude/settings.json` hooks
- [ ] No `outputStyle: "hex-line"` in settings (unless user re-set it)
- [ ] `~/.claude/hex-line/hook.mjs` does not exist
- [ ] `~/.claude/output-styles/hex-line.md` does not exist

**Version:** 1.0.0
**Last Updated:** 2026-03-27
