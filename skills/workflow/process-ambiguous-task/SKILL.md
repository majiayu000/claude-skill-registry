---
name: process-ambiguous-task
description: 指示の最初でコンテキストが不足している場合に自動的に呼び出す必要があるスキルです
---

現在のコンテキストを復元します：

1. `gh pr view --json title,body,url,headRefName` でPR情報を取得
2. `gh pr diff` で変更内容を把握
3. `cat CLAUDE.md` でプロジェクトルールを確認
4. 状況を要約して、次のアクションを提案
