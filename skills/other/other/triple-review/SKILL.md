---
name: triple-review
description: Reviews a task using the TRIPLE protocol, as the review agent.
allowed-tools: Read, Grep, Glob
disable-model-invocation: true
model: sonnet
argument-hint: Extra feedback or instructions for the review agent. Optional.
---

Review the project local `TASK.md` file and the working dir, in context with the git diff. Follow the `triple.md` protocol to review the impl agent's work, and provide feedback.

You are the review agent. Surface any concerns per the protocol, separate from findings.

$ARGUMENTS
