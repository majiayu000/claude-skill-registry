---
name: windows
description: Switch to Windows development mode. Copies docs/CLAUDE-Windows.md to the root CLAUDE.md file, applying Windows/WSL-specific instructions. Use when switching from macOS to a Windows computer.
---

# Windows Skill

Switch the project to Windows development mode by copying the Windows-specific CLAUDE.md configuration to the project root.

## When to Use

Invoke `/windows` when:
- You've switched from a macOS computer to a Windows computer
- You need to ensure CLAUDE.md has Windows/WSL-specific instructions
- Starting a session on Windows after previously working on macOS

## Execution Steps

### Step 1: Read the Windows Configuration

Read `docs/CLAUDE-Windows.md` to get the Windows-specific CLAUDE.md content.

### Step 2: Overwrite Root CLAUDE.md

Write the contents of `docs/CLAUDE-Windows.md` to the root `CLAUDE.md` file, completely replacing its contents.

### Step 3: Confirm the Switch

Provide a brief confirmation to the user:

```
Switched to Windows development mode.

CLAUDE.md now contains Windows/WSL-specific instructions including:
- WSL vs Windows environment warnings
- Safe/unsafe command lists for WSL
- PowerShell recovery instructions
- Prohibited action: pnpm install from WSL

Ready for Windows development.
```

## Important Notes

- This completely overwrites CLAUDE.md - the OS-specific files in docs/ are the source of truth
- Both `docs/CLAUDE-Windows.md` and `docs/mac-claude.md` should be kept in sync via the `/update` skill
- If you've made changes to CLAUDE.md that aren't in the docs/ versions, run `/update` first to sync them
