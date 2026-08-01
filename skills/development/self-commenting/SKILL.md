---
name: self-commenting
description: 'AI-native code commenting system with grep-searchable AICODE-* markers
  for cross-session memory. Use when: working with code files, leaving notes for future
  sessions, breaking down complex tasks, docu'
---

---
name: self-commenting
description: AI-native code commenting system with grep-searchable AICODE-* markers for cross-session memory. Use when: working with code files, leaving notes for future sessions, breaking down complex tasks, documenting non-obvious logic, recording bug fixes. Triggers: start coding session, edit code, complex logic, leave note, todo for later, debug session, bug fix, AICODE markers, self-commenting.
allowed-tools: Read, Write, Bash(grep:*)
---

# Self-Commenting

Long-term memory layer in code using grep-searchable AICODE-* markers.

## Process

**SCAN → WORK → ANNOTATE**

## Step 1: Scan

Before modifying any file, find existing markers:

```bash
grep -rn "AICODE-" <file-or-directory>
```

Read markers to understand previous context and pending tasks.

## Step 2: Work

Edit code normally.

## Step 3: Annotate

Add markers for cross-session memory:

- `AICODE-NOTE` — critical implementation details
- `AICODE-TODO` — pending tasks to complete
- `AICODE-FIX` — non-trivial bug solutions (problem → cause → fix)

See `references/conventions.md` for format, language syntax, and examples.

## Decision Rules

### Add AICODE-NOTE when:
- Non-obvious algorithm or approach
- External API constraints
- Complex state management
- Integration quirks

### Add AICODE-TODO when:
- Task out of current scope
- Needs more information
- Depends on other work

### Add AICODE-FIX when:
- Bug solution was non-trivial
- Root cause wasn't obvious
- Similar bugs might occur elsewhere

### Skip markers when:
- Code is self-explanatory
- Standard pattern usage
- Trivial one-line fix

## Session Workflow

**Start:** `grep -rn "AICODE-" src/`

**Before debugging:** Check for similar `AICODE-FIX` in codebase

**End:** Add TODO for incomplete work, NOTE for key decisions, FIX for solved bugs