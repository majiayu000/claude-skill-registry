---
name: github
description: |
  GitHub操作の統合スキル。issue作成、PR作成、レビュースレッド操作を提供。
  使用ケース:（1）issue作成、（2）PR作成（事前チェック統合）、
  （3）レビューコメント取得、（4）スレッド返信、（5）スレッド解決
---

# GitHub操作スキル

## 操作タイプの選択

1. **Issue作成** → [Issue操作](#issue操作)
2. **PR作成** → [PR操作](#pr操作)
3. **レビュースレッド操作** → [Thread操作](#thread操作)

## Issue操作

### issue作成

`gh issue create`コマンドを使用:

```bash
gh issue create --title "タイトル" --body "本文"
```

**推奨**: document-specialistエージェントで説明文を生成してから使用

## PR操作

### PR作成

事前チェック（fmt/lint/test）を実行してからPRを作成:

```bash
./.claude/skills/github/scripts/pr-create.sh <タイトル> <本文>
```

**注意事項**:
- mainブランチからは実行不可
- PRタイトルにissue番号を含めない
- 本文には `fixed #<issue番号>` を含める

## Thread操作

### スレッド一覧取得

PRの未解決レビューコメントを取得:

```bash
./.claude/skills/github/scripts/thread-list.sh <PR番号>
```

**出力形式** (NDJSON):
```json
{"thread_id": "...", "author": "...", "comment": "..."}
```

### スレッド詳細取得

レビュースレッドの詳細情報を取得:

```bash
./.claude/skills/github/scripts/thread-details.sh <スレッドID> [スレッドID...]
```

**出力情報**:
- スレッドID、解決状態、ファイルパス、行番号
- 各コメント（作成者、本文、作成日時）を時系列順で表示

### スレッド返信

レビュースレッドに返信を投稿:

```bash
echo "コメント内容" | ./.claude/skills/github/scripts/thread-reply.sh <スレッドID>
```

**注意**: 返信先の対象者には `@ユーザー名` 形式でメンションを付与すること

### スレッド解決

レビュースレッドを解決済みに変更:

```bash
./.claude/skills/github/scripts/thread-resolve.sh <スレッドID>
```

## 関連スキル

- **plan-issue**: issue対応タスク作成
- **plan-pr**: PRレビュー対応タスク作成
- **review**: 自己レビュー実施
