---
name: commit-push-pr-flow
description: タスク完了後に自動的に実行する必要があるフロースキルです
model: haiku
---

Commit, push, and open a PR

## 手順
1. `git status` で変更を確認
2. 変更内容からConventional Commits形式のメッセージを生成
3. `git add .` でステージング（.env等の機密ファイルがないか確認）
4. `git commit -m "生成したメッセージ"`
5. `git push -u origin HEAD`
6. `gh pr create --title "PRタイトル" --body "説明（日本語）"`
7. `gh pr view --web` で結果を共有して完了

## 注意
- PRタイトルにイシュー番号を含める（例: [YOUR_PREFIX]-15: ...）
- 説明は日本語で記述
