---
name: worktree
description: |
    Planが承認/完了した直後に自律的に呼び出す必要があるスキルです。
    Trigger: plan approved, plan completed, taskを開始します
model: haiku
---

gh wt add <branch> でgit worktreeを作成します。
branch名にslashは使わないこと。
実装後は commit-push-pr-flow を呼び出すこと
