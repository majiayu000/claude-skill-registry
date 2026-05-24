---
name: issue-reporter
description: 作業進捗をGitHub issueに自動報告します。計画立案時、知見獲得時、問題発覚時にブランチ名からissue番号を抽出し、構造化されたコメントを投稿します。
allowed-tools: Bash Grep Read
---

# Issue Reporter スキル

このスキルは、作業進捗を関連するGitHub issueに自動報告します。

## 起動条件

以下の状況で自動起動します：

1. **計画立案時**: 実装・調査などの計画を立てたとき
2. **知見獲得時**: 新たな知見が得られたとき（特にプロジェクトにとって有益な情報は必須）
3. **問題発覚時**: 新たな問題が発覚したとき
4. **その他**: 記録すべき重要な情報があるとき

## 前提条件

- 現在のブランチ名にissue番号が含まれていること
- `gh` CLIがインストールされ認証済みであること
- リポジトリがGitHubにプッシュされていること

## ブランチ名からのissue番号抽出

> ブランチ命名規則の詳細は `.claude/git-conventions.md` を参照してください。

### サポートされるパターン

**標準パターン（推奨）:**

| パターン例 | 抽出結果 |
|-----------|---------|
| `feat/121-xxx` | 121 |
| `fix/121-xxx` | 121 |
| `refactor/123-xxx` | 123 |
| `docs/101-xxx` | 101 |
| `test/111-xxx` | 111 |
| `chore/222-xxx` | 222 |

**レガシーパターン（後方互換性）:**

| パターン例 | 抽出結果 |
|-----------|---------|
| `feature/111-xxx` | 111 |
| `bugfix/456-xxx` | 456 |

### 抽出ロジック

```bash
# 現在のブランチ名を取得
branch=$(git branch --show-current)

# issue番号を抽出（標準パターン + レガシーパターン対応）
issue_number=$(echo "$branch" | sed -n 's#^\(feat\|fix\|chore\|docs\|refactor\|test\|feature\|bugfix\)/\([0-9]\+\)-.*#\2#p')

# 先頭ゼロを除去（004 -> 4）
if [ -n "$issue_number" ]; then
    issue_number=$((10#$issue_number))
fi
```

## コメント形式

### 計画立案時（Plan）

```markdown
## 📋 実装計画

**作業内容**: [作業の概要]

### 計画

1. [ステップ1]
2. [ステップ2]
3. [ステップ3]

### 予想される課題

- [課題1]
- [課題2]

---
*Posted by Claude Code at YYYY-MM-DD HH:MM*
```

### 知見獲得時（Insight）

```markdown
## 💡 新たな知見

**発見内容**: [発見の概要]

### 詳細

[発見の詳細説明]

### プロジェクトへの影響

- [影響1]
- [影響2]

### 推奨アクション

- [ ] [アクション1]
- [ ] [アクション2]

---
*Posted by Claude Code at YYYY-MM-DD HH:MM*
```

### 問題発覚時（Problem）

```markdown
## ⚠️ 問題発覚

**問題**: [問題の概要]

### 詳細

[問題の詳細説明]

### 再現手順

1. [手順1]
2. [手順2]

### 暫定対応

- [対応1]

### 根本対応（提案）

- [ ] [対応提案1]

---
*Posted by Claude Code at YYYY-MM-DD HH:MM*
```

### その他（Note）

```markdown
## 📝 作業メモ

**内容**: [内容の概要]

### 詳細

[詳細説明]

---
*Posted by Claude Code at YYYY-MM-DD HH:MM*
```

## 実行プロセス

### 1. issue番号の特定

```bash
branch=$(git branch --show-current)
issue_number=$(echo "$branch" | sed -n 's#^\(feat\|fix\|chore\|docs\|refactor\|test\|feature\|bugfix\)/\([0-9]\+\)-.*#\2#p')
if [ -n "$issue_number" ]; then
    issue_number=$((10#$issue_number))
fi
```

### 2. issueの存在確認

```bash
gh issue view "$issue_number" --json state,title 2>/dev/null
```

### 3. コメントの投稿

```bash
gh issue comment "$issue_number" --body "$comment_body"
```

## エラーハンドリング

### mainブランチ等（issue番号なし）の場合

issue番号が検出できないブランチ（main, develop等）の場合は、ブランチ切り替えを提案します：

```
⚠️ issue番号が検出できません

現在のブランチ: main

issueに紐づいたブランチに切り替えることを推奨します。

対応中のissueがある場合:
  git checkout -b feat/<issue番号>-<説明>

例:
  git checkout -b feat/121-fix-embed-error
```

### issueが存在しない場合

```
⚠️ Issue #XXX が見つかりません

ブランチ名から抽出したissue番号に対応するissueが存在しません。

考えられる原因：
- issueが削除された
- issueが別のリポジトリにある
- ブランチ名のフォーマットが想定と異なる

現在のブランチ: [branch_name]
抽出したissue番号: [issue_number]
```

### gh未認証の場合

```
⚠️ GitHub CLI認証が必要です

gh CLIの認証が必要です。以下のコマンドで認証してください：

  gh auth login

その後、再度コメントを投稿できます。
```

## 自動起動の判断基準

スキルは以下の状況を検知して自動的に報告します：

| シナリオ | 報告タイプ |
|---------|-----------|
| TodoWriteで複数タスクを作成した直後 | Plan |
| API仕様・実装パターンを発見した際 | Insight |
| テスト失敗の原因を特定した際 | Problem |
| ブロッカーを発見した際 | Problem |
| 設計変更を決定した際 | Insight |

## 重複防止

以下の場合はコメントを投稿しません：

- 同一セッション内で既に同様の内容を報告済み
- 軽微な進捗（単なるファイル読み取りや軽微な調査）
- まだ結論が出ていない調査途中

## 使用例

### 例1: 計画立案後のコメント

```bash
gh issue comment 121 --body "$(cat <<'EOF'
## 📋 実装計画

**作業内容**: note.com埋め込みサーバーエラーの修正

### 計画

1. エラー発生箇所の特定（api/v1/embed）
2. レスポンス形式の調査
3. エラーハンドリングの実装
4. E2Eテストの追加

### 予想される課題

- 埋め込みAPIの仕様が非公開
- レート制限の可能性

---
*Posted by Claude Code at 2026-01-13 10:30*
EOF
)"
```

### 例2: 知見獲得後のコメント

```bash
gh issue comment 121 --body "$(cat <<'EOF'
## 💡 新たな知見

**発見内容**: 埋め込みAPIはキーを使用してリゾルブする必要がある

### 詳細

`api.note.com/v1/embed/resolve` エンドポイントは、
note_keyを使用してURLから埋め込み可能なコンテンツを取得します。

レスポンス形式:
```json
{
  "data": {
    "html": "<iframe...>",
    "provider_name": "YouTube"
  }
}
```

### プロジェクトへの影響

- 現在の直接埋め込み方式を変更する必要がある
- API経由での処理に移行すべき

### 推奨アクション

- [ ] embed_resolver モジュールの作成
- [ ] 既存の埋め込み処理をリファクタリング

---
*Posted by Claude Code at 2026-01-13 11:45*
EOF
)"
```

## 注意事項

- **機密情報を含めない**: APIキー、認証情報、個人情報をコメントに含めない
- **簡潔に**: 長すぎるコメントは避け、要点を絞る
- **構造化**: テンプレートに従って構造化されたコメントを作成
- **タイムスタンプ**: コメントには必ずタイムスタンプを含める

## チェックリスト

コメント投稿前に確認：

- [ ] ブランチにissue番号が含まれているか
- [ ] issueが存在し、アクセス可能か
- [ ] コメント内容が適切なテンプレートに従っているか
- [ ] 機密情報が含まれていないか
- [ ] 重複したコメントではないか
