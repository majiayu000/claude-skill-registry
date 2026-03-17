---
name: learn
version: 2.0.0
description: "[Utilities] Teach Claude lessons that persist across sessions. Triggers on 'remember this', 'always do', 'never do', 'learn this', 'from now on'. Saves to docs/lessons.md, auto-injected via hook."
activation: user-invoked
allowed-tools: Read, Write, Edit, Glob
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Teach Claude lessons that persist across sessions by saving to memory files.

**Workflow:**
1. **Capture** -- Identify the lesson from user instruction or experience
2. **Save** -- Write to appropriate memory file in `.claude/projects/` or `docs/lessons.md`
3. **Confirm** -- Acknowledge what was saved and where

**Key Rules:**
- Triggers on "remember this", "always do X", "never do Y"
- Save to persistent memory, not just session context
- Check for existing memories before creating duplicates

# Lesson Learning Skill

Teach Claude lessons that persist across sessions. Lessons are saved to `docs/lessons.md` and automatically injected into every prompt and before file edits.

## Usage

### Add a lesson

```
/learn always use the validation framework fluent API instead of throwing ValidationException
/learn never call external APIs in command handlers - use Entity Event Handlers
/learn prefer async/await over .then() chains
```

### List lessons

```
/learn list
```

### Remove a lesson

```
/learn remove 3
```

### Clear all lessons

```
/learn clear
```

## Behavior

1. **`/learn <text>`** — Append `- [YYYY-MM-DD] <text>` to `docs/lessons.md`
2. **`/learn list`** — Read and display all current lessons
3. **`/learn remove <N>`** — Remove lesson entry N (by line number among lesson entries)
4. **`/learn clear`** — Clear all lessons (confirm with user first)
5. **File creation** — If `docs/lessons.md` doesn't exist, create it with header only (`# Learned Lessons`), no HTML comments

## Auto-Inferred Activation

When Claude detects correction phrases in conversation (e.g., "always use X", "remember this", "never do Y", "from now on"), this skill auto-activates via `infer: true`. When auto-inferred (not explicit `/learn`), **confirm with the user before saving**: "Save this as a lesson? [Y/n]"

## Storage

Lessons are stored in `docs/lessons.md` as a simple markdown list:

```markdown
# Learned Lessons

- [2026-02-25] Always use validation framework fluent API
- [2026-02-25] Never throw ValidationException for validation
```

## Injection

Lessons are injected by `lessons-injector.cjs` hook on:

- **UserPromptSubmit** — Every user message (with dedup)
- **PreToolUse(Edit|Write|MultiEdit)** — Before every file edit (always)
