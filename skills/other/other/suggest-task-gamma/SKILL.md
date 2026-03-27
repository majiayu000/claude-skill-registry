---
name: suggest-task-gamma
description: "{{ ƔƔƔ }} Suggest the next logical task based on codebase analysis"
model: sonnet
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Bash(npm:*)", "Bash(bun:*)", "Bash(pnpm:*)", "Bash(deno:*)"]
argument-hint: [optional focus area]
---

Analyse the current state of the codebase, then compare it to the project documentation. Suggest the next logical task I can complete.

## Rules
1. If the task will take longer than 45 minutes, subdivide it and suggest the first subtask.
2. If $ARGUMENTS contains content, focus suggestions on that area.
3. Conserve tokens by being selective in which files you read.
4. Where possible, use dev scripts in @./package.json & @./scripts rather than reading file content.
5. After suggesting the task, add a **"When complete, you'll be able to:"** section. Describe concretely and specifically what the user will see on screen or be able to do in the app that they cannot do right now. Focus on observable behaviour, not implementation detail.

<focus value="$ARGUMENTS" />
