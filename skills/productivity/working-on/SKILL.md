---
name: working-on
description: "Set a tracking document as the source of truth for the current feature or task. Use when starting work on a feature, bug fix, or multi-step task that benefits from a persistent record of decisions, discoveries, and progress. Keeps the document updated as work proceeds."
disable-model-invocation: true
arguments: [path]
argument-hint: "[path-to-tracking-doc] [additional instructions]"
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.0"
license: MIT
---

# Working On

You are managing a tracking document that serves as the source of truth for the current task or feature.

The tracking document is: `$path`

## Behavior

Once activated, treat the tracking document as a living record. Update it after:

- Any decision is made (architectural, design, scope, naming, etc.)
- A new problem, bug, or edge case is discovered
- A new sub-feature or requirement emerges
- An issue is raised or resolved
- Any significant implementation work is completed
- A key part of a conversation with the user that would be useful to recall later
- Any time you commit files — a commit is a strong signal that the tracking document should also be reviewed and updated

If in doubt, update the document. It is better to over-document than to lose context.

## Git Handling

Do NOT commit the tracking document unless it already appears in the repository's git history. If the file is not tracked by git, leave it out of any commits.

## Guidelines

- Keep updates concise — bullet points and short paragraphs are preferred over prose
- Use timestamps or date headers when the document spans multiple sessions
- Record the *why* behind decisions, not just the *what*
- When a section becomes stale or irrelevant, move it to an "Archive" or "Resolved" section rather than deleting it
- If the document doesn't exist yet, create it with a sensible structure based on the task at hand
