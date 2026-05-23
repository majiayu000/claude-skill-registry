---
name: test-task-in-fork
description: Test if Task tool works in forked skill context
allowed-tools: Read, Write, Grep, Glob, Bash, TodoWrite, Task, Skill
model: claude-opus-4-5
permissionMode: dontAsk
context: fork
---

# Test Task Tool in Fork

**Goal**: Verify if Task tool is available in forked skill context.

## Task

1. List your available tools by trying to use Task tool
2. If Task is available, spawn an Explore subagent to find README.md files
3. Write results to: `earnings-analysis/test-outputs/task-in-fork-result.txt`

Include:
- Whether Task tool was available
- If yes, the subagent result
- If no, what tools ARE available
