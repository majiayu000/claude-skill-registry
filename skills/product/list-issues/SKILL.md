---
name: list-issues
description: オープン Issue の一覧を優先順位付きで表示する。「Issue 一覧」「Issue リスト」「オープン Issue」「Issue を見せて」「チケット一覧」「未解決 Issue」「Issue 確認」などで起動。優先度順にソートして表示。
allowed-tools: [Bash]
---

# List Issues

オープン Issue の一覧を優先順位付きで表示します。

## 引数

- `--all`: クローズ済みも含めて表示
- `--mine`: 自分がアサインされたもののみ
- `--help`: ヘルプを表示

## 実行手順

1. `gh issue list` コマンドで Issue 一覧を取得

```bash
# オープンのみ（デフォルト）
gh issue list --json number,title,labels,assignees,createdAt --limit 50

# クローズ済みも含める（--all）
gh issue list --state all --json number,title,labels,assignees,createdAt,state --limit 50

# 自分がアサインされたもの（--mine）
gh issue list --assignee @me --json number,title,labels,assignees,createdAt --limit 50
```

2. 優先順位でソート（ラベル: priority-high > priority-medium > priority-low）

3. 以下の形式で表示

## 出力フォーマット

```
## オープン Issue 一覧

| 優先度 | # | タイトル | ラベル | 担当者 | 作成日 |
|:------:|---|----------|--------|--------|--------|
| 🔴 | #5 | バグ修正 | bug, priority: high | @user | 2024-01-01 |
| 🟡 | #3 | 機能追加 | enhancement | - | 2024-01-02 |
| 🟢 | #1 | ドキュメント | docs, priority: low | @user | 2024-01-03 |

合計: 3 件のオープン Issue
```

## 優先度の判定

| 優先度 | アイコン | 条件 |
|--------|----------|------|
| 高 | 🔴 | `priority: high` ラベル または `bug` ラベル |
| 中 | 🟡 | `priority: medium` ラベル または ラベルなし |
| 低 | 🟢 | `priority: low` ラベル または `documentation` ラベル |

## 重要な注意事項

- ✅ 優先度順にソートして表示
- ✅ 担当者がいない場合は `-` で表示
- ✅ ラベルはカンマ区切りで表示
- ❌ Issue の内容は表示しない（一覧のみ）
