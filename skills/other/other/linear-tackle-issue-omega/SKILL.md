---
name: linear-tackle-issue-omega
description: "{{ 𝛀𝛀𝛀 }} Tackle a task from Linear"
model: opus
disable-model-invocation: true
allowed-tools: ["mcp__plugin_linear_linear__get_issue", "mcp__plugin_linear_linear__save_issue", "mcp__plugin_linear_linear__list_issues", "Read", "Glob", "Grep", "Edit", "Write", "Bash(git:*)"]
argument-hint: [desired outcome]
---

Get the details of issue `FOU-$ARGUMENTS` from Linear, then begin working on it. If the issue is indicative of a wider issue, correct the wider issue.
