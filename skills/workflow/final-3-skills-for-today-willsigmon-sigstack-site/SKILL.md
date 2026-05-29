---
name: Session Summary Generator
description: Generate comprehensive session summary for Leavn work - commits, metrics, achievements, remaining work, ship readiness
allowed-tools: Bash, Read, Write
---

# Session Summary Generator

Create session wrap-up:

1. **Git stats**:
   ```bash
   git log --oneline --since="today"
   git diff --shortstat {start-commit}
   ```

2. **Count achievements**:
   - Files modified
   - Lines added/deleted
   - Bugs fixed
   - Features completed

3. **Create summary doc**:
   - SESSION_SUMMARY.md
   - Commits list
   - Metrics
   - Achievements
   - Next steps
   - Ship readiness

Use when: Session ending, need summary, planning next work
