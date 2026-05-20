---
name: pr
description: PR作成Skill。仕様レビュー用または実装レビュー用のPRを作成。/spec や spec-workflow から呼び出される。
---

# /pr Skill - プルリクエスト作成

SDDワークフローにおけるPR作成を担当するSkill。
仕様策定・実装それぞれのフェーズで適切なPRを作成します。

## 発動条件

- `/pr` コマンドで明示的に呼び出し
- `/spec` Skill から自動呼び出し（仕様策定完了時）
- `spec-workflow` Skill から自動呼び出し（実装完了時）

## PRタイトル規則

### 仕様策定用

```
spec: {アクションタイトル}
```

例: `spec: ユーザー認証機能の仕様策定`

### 実装用

```
impl: {アクションタイトル}
```

例: `impl: ユーザー認証機能の実装`

## ワークフロー

```
┌─────────────────────────────────────────────────┐
│  1. 変更確認                                    │
│     - git status で変更内容を確認               │
│     - git diff で差分を確認                     │
│                                                 │
│  2. コミット確認                                │
│     - 未コミットの変更があればコミット          │
│     - コミットメッセージを生成                  │
│                                                 │
│  3. リモートへプッシュ                          │
│     git push -u origin {branch-name}            │
│                                                 │
│  4. PR内容生成                                  │
│     - タイトル: 規則に従って生成                │
│     - サマリー: 変更内容の要約                  │
│     - テストプラン: 検証項目                    │
│                                                 │
│  5. ユーザー確認                                │
│     「このPRを作成しますか？」                  │
│                                                 │
│  6. PR作成                                      │
│     gh pr create                                │
│                                                 │
│  7. 完了通知                                    │
│     PR URLを表示                                │
└─────────────────────────────────────────────────┘
```

## パラメータ

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| type | Yes | PRタイプ | `spec` or `impl` |
| action-id | No | アクションID（ブランチ名から自動取得可） | `001-01-01` |
| base | No | ベースブランチ（デフォルト: main） | `main` |

## PRテンプレート

### 仕様策定用

```markdown
## Summary

- {アクションID} の仕様を策定
- {生成したファイル一覧}

## 変更内容

- specs/phases/{id}.md: フェーズ定義
- specs/tasks/{id}.md: タスク定義
- specs/actions/{id}.md: アクション定義

## レビュー観点

- [ ] ユーザーストーリーが明確か
- [ ] ACがEARS記法で記述されているか
- [ ] 依存関係が整理されているか
- [ ] スコープが適切か

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### 実装用

```markdown
## Summary

- {アクションID} を実装
- {実装した機能の概要}

## 変更内容

- {変更ファイル一覧}

## Test plan

- [ ] 全ACのテストが通過
- [ ] TDDサイクルを遵守
- [ ] スコープ外の変更なし

## AC確認

- [x] {AC1}
- [x] {AC2}
- [x] {AC3}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## 使用例

### 直接呼び出し

```
ユーザー: /pr

Claude: 現在のブランチ: impl/001-01-01-user-auth

        以下のPRを作成しますか？

        タイトル: impl: ユーザー認証機能の実装
        ベース: main

        ## Summary
        - 001-01-01 を実装
        - ログイン/ログアウト機能

        ## Test plan
        - [ ] 全ACのテストが通過
        ...

ユーザー: OK

Claude: ✅ PRを作成しました
        URL: https://github.com/user/repo/pull/123
```

### /spec からの自動呼び出し

```
[/spec Skill 内部]
→ ファイル生成完了後に /pr を発火
→ type: spec
→ 仕様レビュー用PRを作成
```

### spec-workflow からの自動呼び出し

```
[spec-workflow Skill 内部]
→ 実装完了・AC全チェック後に /pr を発火
→ type: impl
→ 実装レビュー用PRを作成
```

## 実行コマンド

```bash
# 変更確認
git status
git diff

# コミット（必要な場合）
git add .
git commit -m "..."

# プッシュ
git push -u origin {branch-name}

# PR作成
gh pr create --title "{title}" --body "{body}"
```

## エラーハンドリング

### 変更がない場合

```
Claude: コミットする変更がありません。

対応案:
1. 作業を続ける
2. 既存のコミットでPRを作成

どれを選択しますか？
```

### リモートに既にPRがある場合

```
Claude: このブランチには既にPRが存在します。
        URL: https://github.com/user/repo/pull/123

対応案:
1. 既存のPRを更新（追加コミットをプッシュ）
2. 既存のPRを閉じて新規作成

どれを選択しますか？
```

### gh CLI が未認証の場合

```
Claude: GitHub CLIが認証されていません。

以下のコマンドで認証してください:
gh auth login
```

## 禁止事項

- ユーザー確認なしのPR作成
- テスト未通過でのPR作成（impl時）
- 空のPR作成
- ベースブランチへの直接プッシュ
