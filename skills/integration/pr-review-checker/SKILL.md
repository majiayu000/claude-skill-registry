---
name: pr-review-checker
description: 自分の PR に付いたレビューコメントを確認し、修正対応を実行する（PR作成者向け）。「レビュー対応」「レビューコメント確認」「指摘を修正」「PRコメント確認」などで起動。
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# PR Review Checker

**自分の PR** に付いたレビューコメントを確認し、修正対応を実行します。

> **注意**: 他者の PR をレビューする場合は `pr-reviewer` を使用してください。

## ワークフロー

### 1. レビューコメントの取得

```bash
# PR のレビューコメント取得
gh api repos/{owner}/{repo}/pulls/{pr番号}/comments --jq '.[] | {path: .path, line: .line, body: .body}'

# PR レビュー取得
gh pr view {pr番号} --json reviews
```

### 2. 指摘事項の分類

| 種類 | 対応 |
|------|------|
| 必須修正 | コード修正 |
| 改善提案 | 検討して対応 |
| 質問 | 回答コメント |
| コメント | 確認のみ |

### 3. 対応内容の確認

ユーザーに対応方針を確認:

```
以下の指摘がありました:

1. [必須] {file}:{line} - {comment}
   → 修正予定: {fix_plan}

2. [提案] {file}:{line} - {comment}
   → 対応: {response_plan}

この方針で対応しますか？
```

### 4. 修正の実行

承認後、各指摘に対応:

- コード修正
- コメントへの返信

### 5. 修正コミット

```bash
git add .
git commit -m "fix: レビュー指摘を修正 (#{pr番号})"
git push
```

### 6. 返信コメント

```bash
# 各コメントに返信
gh api repos/{owner}/{repo}/pulls/{pr番号}/comments/{comment_id}/replies \
  --method POST \
  --field body="{reply}"
```

### 7. 結果報告

```
レビュー指摘への対応を完了しました。

修正内容:
- {fix_1}
- {fix_2}

コミット: {commit_hash}
プッシュ済み: ✅

再レビューをお願いしてください。
```

## 重要な注意事項

- ✅ 必須修正は必ず対応
- ✅ 対応内容をコメントで返信
- ✅ 修正後はプッシュ
- ❌ 指摘を無視しない
- ❌ 理由なく却下しない
