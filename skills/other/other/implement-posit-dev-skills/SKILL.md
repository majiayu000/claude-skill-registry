---
name: implement
description: "Orchestrates implementation of a plan file by delegating work to subagents in parallel. Verifies git branch state, tracks progress, and ensures high-quality implementation. Invoke with a plan file path and optional model override: /implement plans/my-plan.md [--model sonnet]"
disable-model-invocation: true
arguments: [path]
argument-hint: "[plan-file-path] [--model sonnet|haiku|opus]"
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "2.0"
license: MIT
---

# Implementation Orchestrator

Plan file: `$path`

Read your instructions from the appropriate reference file before proceeding:

- If you have access to Agent, TaskCreate, TaskUpdate, TaskList tools: Read `references/claude-code.md`
- Else if you have access to task and read_agent tools: Read `references/copilot-cli.md`
- Otherwise: Read `references/generic.md`
