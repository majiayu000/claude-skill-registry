---
name: sync
description: >-
  MANDATORY sync rules for CLAUDE.md and agents.md files. This skill MUST be
  activated whenever editing CLAUDE.md, agents.md, backend/CLAUDE.md, or
  backend/AGENTS.md. Failure to sync causes drift between AI tools.
---

# Documentation Synchronization

## Root Files
`CLAUDE.md` and `agents.md` MUST stay 100% in sync.

## Backend Files
`backend/CLAUDE.md` and `backend/AGENTS.md` MUST stay 100% in sync.

## When to Sync
Any change to either file must be mirrored to the other:
- `CLAUDE.md` / `agents.md` - Root project instructions
- `backend/CLAUDE.md` / `backend/AGENTS.md` - Backend-specific instructions

## Why Both Files Exist
- Different AI tools look for different filenames
- Claude Code: prefers `CLAUDE.md`
- Cursor: prefers `AGENTS.md`
- Keeping both ensures consistent behavior across all tools
