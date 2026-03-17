---
name: triple-plan
description: Helps define a TASK.md for the current task using the TRIPLE protocol, as the lead agent.
allowed-tools: Read, Grep, Glob, Bash
disable-model-invocation: true
argument-hint: What the task is about. Required.
---

Read the `triple.md` protocol and collaborate with the human to produce a `TASK.md` following the template in Phase 1.

You are the lead agent. You can read code, diffs, and run commands (e.g. tests) to understand the codebase, but you do not modify code.

$ARGUMENTS
