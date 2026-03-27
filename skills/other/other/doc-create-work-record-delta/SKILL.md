---
name: doc-create-work-record-delta
description: "{{ 𝚫𝚫𝚫 }} Generate a work record summarizing today's development session"
model: haiku
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash(git:*)"]
---

<task overview="Create a work record by analyzing today's git commits, code changes, and session context.">
<template location="~/.claude/doc-templates/work-record.md" />
<steps>
1. Read the work record template from ~/.claude/doc-templates/work-record.md
2. Establish period of work you need to cover
    - Check docs/work-records/ to see when last work record was created
    - Check date and time now
3. Analyze relevant work:
    - Git commits on main (and branches merged into main)
    - Diffs for each commit
    - Files changed and time patterns
4. Infer session focus, goals, and outcomes from commits and conversation context
5. Generate the work record following the template - DO NOT ask user questions unless:
    - Critical information is missing that cannot be inferred
    - Ambiguity would result in incorrect documentation
6. Present the completed work record for approval
7. Save to docs/work-records/YYYY-MM-DD_HH-MM_[session-focus].md
    - YYYY-MM-DD and HH-MM are date & time when record is created, not when first commit was made
</steps>
<notes>
- Focus on what was accomplished, not just what was committed
- Include code snippets for significant changes
- Tie work to larger goals when possible
</notes>
</task>
