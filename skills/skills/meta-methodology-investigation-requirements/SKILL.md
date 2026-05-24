---
name: meta-methodology-investigation-requirements
description: Investigation requirement - never speculate about code you haven't read. List files, read completely, base analysis on evidence. Prevents hallucination in coding agents.
---

# Investigation Requirements

> **Quick Guide:** Never speculate about code you haven't opened. List files to examine, read them completely, base analysis strictly on what you find.

---

<critical_requirements>

## CRITICAL: Before Any Implementation

**(Never speculate about code you have not opened)**

**(List the files you need to examine explicitly)**

**(Read each file completely before making claims)**

**(Base analysis strictly on what you find in the files)**

</critical_requirements>

---

<investigation_requirement>

**CRITICAL: Never speculate about code you have not opened.**

Before making any claims or implementing anything:

1. **List the files you need to examine** - Be explicit about what you need to read
2. **Read each file completely** - Don't assume you know what's in a file
3. **Base analysis strictly on what you find** - No guessing or speculation
4. **If uncertain, ask** - Say "I need to investigate X" rather than making assumptions

If a specification references pattern files or existing code:

- You MUST read those files before implementing
- You MUST understand the established architecture
- You MUST base your work on actual code, not assumptions

If you don't have access to necessary files:

- Explicitly state what files you need
- Ask for them to be added to the conversation
- Do not proceed without proper investigation

**This prevents 80%+ of hallucination issues in coding agents.**

</investigation_requirement>

---

<examples>

## What "Investigation" Means

**Good investigation:**

```
I need to examine these files to understand the pattern:
- auth.py (contains the authentication pattern to follow)
- user-service.ts (shows how we make API calls)
- SettingsForm.tsx (demonstrates our form handling approach)

[After reading files]
Based on auth.py lines 45-67, I can see the pattern uses...
```

**Bad "investigation":**

```
Based on standard authentication patterns, I'll implement...
[Proceeds without reading actual files]
```

Always choose the good approach.

</examples>

---

<critical_reminders>

## CRITICAL REMINDERS

**(Never speculate about code you have not opened)**

**(You MUST list files to examine before making claims)**

**(You MUST read each file completely)**

**(You MUST base all analysis strictly on what you find in the files)**

**(This prevents 80%+ of hallucination issues)**

</critical_reminders>
