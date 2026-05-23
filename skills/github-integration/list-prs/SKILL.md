---
name: list-prs
description: オープン PR の一覧を優先順位付きで表示する。「PR 一覧」「PR リスト」「オープン PR」「PR を見せて」「プルリク一覧」「レビュー待ち PR」「PR 確認」などで起動。レビュー状態と優先度順にソートして表示。
allowed-tools: [Bash]
---

# List PRs

オープン PR の一覧を優先順位付きで表示します。

## 引数

- `--all`: マージ済みも含めて表示
- `--mine`: 自分が作成したもののみ
- `--help`: ヘルプを表示

## 実行手順

1. `gh pr list` コマンドで PR 一覧を取得

```bash
# オープンのみ（デフォルト）
gh pr list --json number,title,headRefName,author,reviewDecision,updatedAt --limit 50

# マージ済みも含める（--all）
gh pr list --state all --json number,title,headRefName,author,reviewDecision,updatedAt,state --limit 50

# 自分が作成したもの（--mine）
gh pr list --author @me --json number,title,headRefName,author,reviewDecision,updatedAt --limit 50
```

2. レビュー状態と優先順位でソート

3. 以下の形式で表示

## 出力フォーマット

```
## オープン PR 一覧

| 状態 | # | タイトル | ブランチ | レビュー | 作成者 | 更新日 |
|:----:|---|----------|----------|----------|--------|--------|
| 🔄 | #10 | feat: 新機能 | feature/5 | ⏳ 待機中 | @user | 2024-01-01 |
| ✅ | #8 | fix: バグ修正 | fix/bug | ✅ 承認済 | @user | 2024-01-02 |
| ⚠️ | #6 | docs: 更新 | docs/update | ❌ 要修正 | @user | 2024-01-03 |

合計: 3 件のオープン PR
```

## 状態アイコン

| アイコン | 状態 | 条件 |
|----------|------|------|
| 🔄 | レビュー待ち | `reviewDecision` が null または REVIEW_REQUIRED |
| ✅ | 承認済み | `reviewDecision` が APPROVED |
| ⚠️ | 変更要求あり | `reviewDecision` が CHANGES_REQUESTED |
| 🚧 | ドラフト | `isDraft` が true |

## レビュー状態アイコン

| アイコン | 状態 |
|----------|------|
| ⏳ 待機中 | レビュー未依頼またはレビュー中 |
| ✅ 承認済 | 承認済み（マージ可能） |
| ❌ 要修正 | 変更要求あり |

## 重要な注意事項

- ✅ レビュー状態順にソートして表示
- ✅ ブランチ名を表示して関連 Issue を推測可能に
- ✅ 更新日順でソート
- ❌ PR の内容は表示しない（一覧のみ）
