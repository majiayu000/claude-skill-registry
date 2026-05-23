---
name: hotfix
description: 'Execute the hotfix workflow when the user asks `hotfix` or `/hotfix`: create a hotfix branch from main, guide fix+checks, open PR to main, and confirm patch release.'
---

# Hotfix Workflow

本番障害向けのホットフィックスフローを開始し、`hotfix/*` ブランチ作成からパッチリリース確認までを案内する。

## Preflight

- `git status --short` が空であること
- `main` ブランチが存在すること
- `gh auth status` が成功すること

## 実行内容

1. 前提条件チェック
2. `main` から `hotfix/*` ブランチ作成
3. 修正・品質チェック・PR作成・リリース確認の手順提示

## 使用方法

### パターンA: Issue番号を指定

```bash
./scripts/release/create-hotfix.sh 42
# -> hotfix/42
```

### パターンB: 説明を指定

```bash
./scripts/release/create-hotfix.sh fix-critical-bug
# -> hotfix/fix-critical-bug
```

### パターンC: 対話式

```bash
./scripts/release/create-hotfix.sh
```

## 修正後の流れ

```bash
# 1) 修正実装
git add .
git commit -m "fix: 緊急修正の説明"

# 2) 品質チェック
make quality-checks

# 3) プッシュ + PR
git push -u origin hotfix/xxx
gh pr create --base main --head hotfix/xxx \
  --title "fix: 緊急修正の説明" \
  --label "hotfix,auto-merge"

# 4) リリース確認
gh release view
```

## 注意

- 緊急修正以外の変更を含めない
- Conventional Commits で `fix:` プレフィックスを使う
- main マージ後はパッチ版（例: v1.2.4）が自動作成される
