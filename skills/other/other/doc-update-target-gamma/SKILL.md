---
name: doc-update-target-gamma
description: "{{ ƔƔƔ }} Update existing documentation to reflect recent code changes"
model: sonnet
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Bash(git:*)"]
argument-hint: [doc name, e.g., Technical-Overview]
---

Analyze recent code changes and update the specified documentation file.

## Steps
1. Identify doc to update (from argument, or check ~/.claude/doc-reminders.txt)
2. Review recent commits (git log -10 --oneline) and relevant diffs
3. Read existing doc to understand structure and style
4. Identify specific updates needed (outdated sections, new sections, examples)
5. Generate updates preserving existing structure; show diff
6. Apply on approval; remove from doc-reminders.txt if applicable

## Notes
- Match existing documentation style
- Don't remove content unless obsolete
- Update timestamps in doc frontmatter
