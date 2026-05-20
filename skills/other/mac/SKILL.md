---
name: mac
description: Switch to macOS development mode. Copies docs/mac-claude.md to the root CLAUDE.md file, applying macOS-specific instructions. Use when switching from Windows to a macOS computer.
---

# Mac Skill

Switch the project to macOS development mode by copying the macOS-specific CLAUDE.md configuration to the project root.

## When to Use

Invoke `/mac` when:
- You've switched from a Windows computer to a macOS computer
- You need to ensure CLAUDE.md has macOS-specific instructions
- Starting a session on macOS after previously working on Windows

## Execution Steps

### Step 1: Read the macOS Configuration

Read `docs/mac-claude.md` to get the macOS-specific CLAUDE.md content.

### Step 2: Overwrite Root CLAUDE.md

Write the contents of `docs/mac-claude.md` to the root `CLAUDE.md` file, completely replacing its contents.

### Step 3: Confirm the Switch

Provide a brief confirmation to the user:

```
Switched to macOS development mode.

CLAUDE.md now contains macOS-specific instructions including:
- All pnpm/npm commands available (no WSL restrictions)
- Direct development environment (no platform conflicts)
- Standard setup instructions

Ready for macOS development.
```

## Important Notes

- This completely overwrites CLAUDE.md - the OS-specific files in docs/ are the source of truth
- Both `docs/CLAUDE-Windows.md` and `docs/mac-claude.md` should be kept in sync via the `/update` skill
- If you've made changes to CLAUDE.md that aren't in the docs/ versions, run `/update` first to sync them
