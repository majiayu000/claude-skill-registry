---
description: "dotfiles手動同期。Brewfile更新、変更コミット、プッシュを実行。トリガー: sync, dotfiles sync, 同期, push dotfiles, Brewfile update"
allowed-tools:
  - Bash
  - Read
  - Grep
---

# dotfiles-sync スキル

dotfilesリポジトリを手動で同期する。Brewfile更新、gitleaksスキャン、変更のコミット・プッシュを行う。

## 実行フロー

### Step 1: 現在の状態確認

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && git status
```

### Step 2: Brewfile更新

```bash
brew bundle dump --force --file=/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/Brewfile
```

### Step 3: gitleaksセキュリティスキャン

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && gitleaks detect --source=. --no-git
```

警告が出た場合は同期を中止し、ユーザーに報告する。

### Step 4: 変更確認

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && git diff
```

### Step 5: ステージング・コミット

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && git add -A && git commit -m "chore: auto-sync dotfiles $(date '+%Y-%m-%d %H:%M')"
```

### Step 6: プッシュ

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && git push origin HEAD
```

## 使用例

- "dotfilesを同期して"
- "sync dotfiles"
- "Brewfileを更新してプッシュ"
- "dotfilesの変更をコミット"

## 注意事項

- gitleaksで秘密情報が検出された場合は同期を中断
- コミットメッセージは自動生成（日時付き）
- プッシュ前に必ず変更内容をユーザーに確認
