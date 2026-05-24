---
name: triple-approve
description: Finalises a reviewed task — creates PR and merges using the TRIPLE protocol, as the lead agent.
allowed-tools: Read, Grep, Glob, Bash
disable-model-invocation: true
argument-hint: Extra instructions for the lead agent. Optional.
---

Read the project local `TASK.md` and the `triple.md` protocol. Follow Phase 4 (Finalise) to create a PR and merge.

Look for repo-specific PR/merge commands in `AGENTS.md`.

You are the lead agent. You can read code, diffs, and run commands but you do not modify code.

$ARGUMENTS
