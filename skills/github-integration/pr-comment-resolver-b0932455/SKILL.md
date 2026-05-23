---
name: pr-comment-resolver
description: |
  PRのすべてのコメント（レビューコメント、一般コメント、インラインコメント）を取得し、
  種類別（指摘/質問/提案/承認）に分類、優先順位をつけて対応を実行するスキル。
  対応完了後はコメントへの返信も行う。

  トリガー条件:
  - 「PRのコメントに対応して」「PR #N のレビューコメントを処理して」
  - 「PRのフィードバックを解決して」「レビュー指摘を修正して」
  - PRレビュー後に指摘事項への対応が必要な時
  - 「/pr-comment-resolver」「/resolve-pr-comments」
---

# PR Comment Resolver

PRコメントを収集・分類し、優先順位に従って対応を実行する。

## ワークフロー

```
1. Collect   → 全コメント取得
2. Classify  → カテゴリ分類（must/question/should/could/note）
3. Prioritize → 優先順位付け
4. Execute   → 対応実行（修正/回答）
5. Reply     → コメント返信
```

## Step 1: コメント収集

```bash
# PR情報取得
gh pr view {pr_number} --json number,title,body,author,state

# 一般コメント
gh api repos/{owner}/{repo}/issues/{pr_number}/comments

# レビューコメント（インライン）
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments

# レビュー本体
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews
```

## Step 2: 分類

分類ルールの詳細は [references/comment-classification.md](references/comment-classification.md) 参照。

| カテゴリ | 優先度 | 対応 |
|----------|--------|------|
| `must` | 1 | 必須修正（セキュリティ、ブロッカー） |
| `question` | 2 | 回答必須 |
| `should` | 3 | 推奨修正 |
| `could` | 4 | 任意対応 |
| `note` | 5 | 対応不要 |

## Step 3: 優先順位付け

```yaml
priority_order:
  1. must（セキュリティ > データ整合性 > 機能）
  2. question（設計意図 > 実装詳細）
  3. should
  4. could
```

## Step 4: 対応実行

### 修正が必要な場合

1. 該当ファイルを読み取り
2. 指摘内容を理解
3. 修正を実施
4. テスト実行（該当する場合）
5. コミット

### 回答が必要な場合

1. 質問内容を理解
2. コードベースを調査
3. 回答を作成

## Step 5: 返信

返信テンプレートは [references/response-templates.md](references/response-templates.md) 参照。

```bash
# レビューコメントへの返信
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="修正しました。 ✅ commit: {sha}"

# 一般コメントへの返信
gh pr comment {pr_number} --body "回答内容"
```

## 出力形式

```yaml
pr_comment_resolution:
  pr_ref: "owner/repo#123"
  summary:
    total: 10
    resolved: 8
    pending: 2

  resolved:
    - id: "comment_123"
      category: must
      action: "コード修正"
      commit: "abc1234"
      reply_sent: true

    - id: "comment_456"
      category: question
      action: "回答"
      reply_sent: true

  pending:
    - id: "comment_789"
      category: should
      reason: "追加調査が必要"
      next_action: "設計確認後に対応"
```

## 使用例

```
User: PR #45 のコメントに対応して

Claude:
## PR Comment Resolver 実行中...

### Step 1: コメント収集
PR #45: "ユーザー検索API追加"
- 一般コメント: 2件
- レビューコメント: 5件
- レビュー: 1件（CHANGES_REQUESTED）

### Step 2: 分類結果

| # | カテゴリ | 作者 | 内容 |
|---|---------|------|------|
| 1 | must | @reviewer | SQLインジェクション対策 |
| 2 | question | @reviewer | この設計の意図は？ |
| 3 | should | @reviewer | ページネーション追加 |
| 4 | note | @reviewer | LGTM |

### Step 3: 対応中...

#### [1/3] must: SQLインジェクション対策
src/api/users.ts:45 を修正中...
✅ 修正完了 (commit: abc1234)
✅ 返信送信完了

#### [2/3] question: 設計意図の説明
回答を作成中...
✅ 返信送信完了

#### [3/3] should: ページネーション追加
src/api/users.ts を修正中...
✅ 修正完了 (commit: def5678)
✅ 返信送信完了

### 完了サマリー
- 対応完了: 3/3
- コミット: 2件
- 返信: 3件
```

## ガードレール

1. **セキュリティ指摘は最優先**: must/セキュリティは必ず最初に対応
2. **確認なしの大規模変更禁止**: 影響範囲が大きい場合はユーザーに確認
3. **テスト実行**: 修正後は関連テストを実行
4. **返信必須**: 対応した指摘には必ず返信
