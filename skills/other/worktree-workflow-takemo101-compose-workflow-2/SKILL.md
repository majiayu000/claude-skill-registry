---
name: worktree-workflow
description: Git worktree を使用したホスト環境での並行開発ワークフロー。プラットフォーム固有コード（macOS API等）の開発時に使用。
---

# Worktree ワークフロー

ホスト環境での開発時に Git Worktree を使用してブランチを分離するワークフローです。

## 概要

**用途**: プラットフォーム固有コード（macOS API 等）の開発時に、container-use の代わりにホスト環境で作業する際のブランチ分離。

### container-use vs worktree

| 方式 | 分離レベル | 用途 |
|------|----------|------|
| **container-use** | 完全分離（コンテナ） | 通常の実装作業 |
| **worktree** | ブランチ分離のみ | プラットフォーム固有コード |

### Worktree のメリット

| メリット | 説明 |
|---------|------|
| ブランチ切り替え不要 | 複数機能を並行開発可能 |
| main ブランチがクリーン | 未完成コードを main に残さない |
| 即座に切り替え | `cd` するだけで別機能へ |
| 環境変数自動コピー | `.env` を自動コピー |

## ディレクトリ構成

```
project/                         # メインworktree (main ブランチ)
├── .worktrees/                  # worktree 格納ディレクトリ
│   ├── issue-42-auth/           # feature/issue-42-auth ブランチ
│   │   ├── .env                 # ルートからコピー
│   │   └── ...
│   └── issue-43-dashboard/      # feature/issue-43-dashboard ブランチ
│       └── ...
└── .opencode/
    └── skill/
        ├── create-worktree/
        │   ├── SKILL.md
        │   ├── REFERENCE.md
        │   └── scripts/
        │       └── create_worktree.sh
        └── pr-and-cleanup/
            ├── SKILL.md
            ├── REFERENCE.md
            └── scripts/
                └── pr_and_cleanup.sh
```

## 基本フロー

```
Issue 受け取り → platform-exception? → YES → worktree 作成 → ホスト環境で開発 → CI で検証 → PR 作成 + worktree 削除 → マージ
                                    → NO  → container-use
```

## コマンド

### worktree 作成

```bash
bash .opencode/skill/create-worktree/scripts/create_worktree.sh issue-42-auth
```

**実行結果**:
- ブランチ: `feature/issue-42-auth` を作成
- ディレクトリ: `.worktrees/issue-42-auth/` を作成
- 環境変数: `.env` 等を自動コピー

### PR 作成 + worktree 削除

```bash
cd .worktrees/issue-42-auth
bash ../../.opencode/skill/pr-and-cleanup/scripts/pr_and_cleanup.sh
```

**実行結果**:
- PR を作成（インタラクティブ or 引数指定）
- worktree を削除
- main ブランチに戻る

### オプション

```bash
# タイトル・本文を事前指定
bash ../../.opencode/skill/pr-and-cleanup/scripts/pr_and_cleanup.sh \
  --title "feat: Add macOS notification" \
  --body "Closes #42"

# ドラフト PR として作成
bash ../../.opencode/skill/pr-and-cleanup/scripts/pr_and_cleanup.sh --draft

# PR 作成のみ（worktree は残す）
bash ../../.opencode/skill/pr-and-cleanup/scripts/pr_and_cleanup.sh --pr-only

# worktree 削除のみ（PR 作成済みの場合）
bash ../../.opencode/skill/pr-and-cleanup/scripts/pr_and_cleanup.sh --cleanup-only
```

## トラブルシューティング

### worktree が既に存在する

```bash
git worktree list
git worktree remove .worktrees/<feature-name>
```

### ブランチが既に存在する

スクリプトは既存ブランチを再利用します。新規ブランチを作成したい場合:

```bash
git branch -d feature/<feature-name>
```

### 未コミット変更がある

```bash
git status
git add . && git commit -m "WIP"
# または
git stash
```

## 命名規則

| タイプ | 命名パターン | 例 |
|--------|-------------|-----|
| Issue 実装 | `issue-{number}-{short-desc}` | `issue-42-auth` |
| 機能追加 | `feature-{name}` | `feature-dark-mode` |
| バグ修正 | `fix-{name}` | `fix-memory-leak` |
| ホットフィックス | `hotfix-{name}` | `hotfix-critical-bug` |

## 関連スキル

- [create-worktree](../create-worktree/SKILL.md): worktree 作成の詳細
- [pr-and-cleanup](../pr-and-cleanup/SKILL.md): PR 作成 + クリーンアップの詳細

## 関連ドキュメント

- [platform-exception.md](../../instructions/platform-exception.md): 例外適用の判断基準
- [container-use.md](../../instructions/container-use.md): 通常の実装ワークフロー
