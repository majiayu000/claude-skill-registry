---
name: principal-workflow
description: Run the AWK principal workflow (awkit kickoff, principal loop, dispatch worker, check results, review/merge PR). Triggers: awkit kickoff, start-work, NEXT_ACTION, review pr, dispatch worker, autonomous workflow, generate tasks, create task.
allowed-tools: Read, Grep, Glob, Bash
---

# Principal Workflow

AWK 自動化工作流的主控 Skill。

## 前提

Preflight 已由 `awkit kickoff` 完成，Session 已初始化。

## 啟動

**必須 Read** `phases/main-loop.md` 並進入主循環。

## 自我檢查

每進入一個 Phase 或執行一個 Task，輸出：
```
[PRINCIPAL] <timestamp> | <phase/task> | loaded: <filename>
```
