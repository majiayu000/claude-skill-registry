---
name: context_mastery
description: Advanced token optimization and context management strategies.
allowed-tools: Read, Grep, Find
---

# Context Mastery & Token Optimization Protocol

## 1. The "Grep-First" Rule (Token Saver)

- **Problem**: `read_file` on a 2000-line file consumes ~500-1000 tokens instantly.
- **Solution**: Always use `grep` or `read_file_range` first to inspect specific functions or imports.
- **Banned**: `cat` or `read_file` on entire directories or massive files (e.g., `package-lock.json`, giant logs) unless absolutely necessary.

## 2. Incremental Summarization

- **Trigger**: When the conversation exceeds ~20 turns or you feel the context window filling.
- **Action**:
  1.  Summarize what has been achieved in the last 10 turns.
  2.  Write it to `scratchpad.md` or `active_task.md`.
  3.  Explicitly state "I am clearing internal context of validated steps" (if tool allows) or just rely on the scratchpad for future lookup.

## 3. Focused Context Loading

- **Don't**: "Read all files in `src/` to understand the project." (Too expensive).
- **Do**:
  1.  Read `CLAUDE.md` / `README.md`.
  2.  Read directory listing `ls -R`.
  3.  Selectively read _only_ the interfaces (`types.ts`) or entry points (`index.ts`) related to the current task.

## 4. Context Efficiency Checklist

- [ ] Did I use `grep` instead of reading the whole file?
- [ ] Did I check if I already have this info in `MEMORY.md`?
- [ ] Is my next prompt efficient? (Avoid repeating massive code blocks back to the user).
