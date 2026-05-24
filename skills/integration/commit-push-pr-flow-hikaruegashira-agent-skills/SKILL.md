---
name: commit-push-pr-flow
description: |
    タスク完了後に自律的に実行する必要があるフロースキルです。
    Trigger: task completed, ready to submit code
model: haiku
---

Commit, push, and open a pr

- create branch(if current branch in default) and pr
- following pr template
- description in japanese
- 提出後は gh pr view --web で差分を共有して完了してください
- 完了後 review-flow を呼び出します
