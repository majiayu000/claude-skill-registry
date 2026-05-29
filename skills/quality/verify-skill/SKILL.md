---
name: verify
description: Use before claiming work is complete - runs tests, checks git status, verifies changelog
---

# Verification Before Completion

Run this before saying "task complete" or "done".

## Current Status (Pre-injected)

### Test Results
!`cd src-tauri && cargo test 2>&1 | tail -30`

### Git Status
!`git status`

### Changelog Preview
!`head -25 CHANGELOG.md`

## Checklist

Based on the pre-injected data above:

1. **Tests Pass** - Check "Test Results" section. Do NOT proceed if tests fail.
2. **Code Committed** - Check "Git Status" section. All work-related files should be committed.
3. **Changelog Updated** - Check "Changelog Preview". [Unreleased] section should have entry for this work (skip for internal docs like CLAUDE.md, _tasks/).

If changelog missing for user-visible changes, run /changelog.

See CLAUDE.md for project constraints.
