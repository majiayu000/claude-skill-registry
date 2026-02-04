---
description: "Git設定ファイル管理。.gitconfig、.gitmessage、.gitignoreの確認・編集。トリガー: git config, gitconfig, gitmessage, gitignore, git設定"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Grep
---

# git-config スキル

dotfilesリポジトリで管理しているGit設定ファイルの確認・編集を行う。

## 管理対象ファイル

| ファイル | 説明 | symlink先 |
|---------|------|-----------|
| `git/.gitconfig` | Gitグローバル設定 | `~/.gitconfig` |
| `git/.gitmessage` | コミットメッセージテンプレート | `~/.gitmessage` |
| `git/.gitignore_global` | グローバルgitignore | `~/.gitignore` |

## コマンド

### 現在のGit設定確認

```bash
git config --list --show-origin | head -30
```

### .gitconfig の確認

```bash
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/git/.gitconfig
```

### .gitmessage の確認

```bash
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/git/.gitmessage
```

### .gitignore_global の確認

```bash
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/git/.gitignore_global
```

### 特定の設定値確認

```bash
git config --global user.name
git config --global user.email
git config --global core.editor
```

### symlinkの状態確認

```bash
ls -la ~/.gitconfig ~/.gitmessage ~/.gitignore
```

## .gitconfig の主要セクション

### [user]

```
[user]
  name = Your Name
  email = your@email.com
```

### [core]

```
[core]
  editor = vim
  excludesfile = ~/.gitignore
  autocrlf = input
  pager = delta
```

### [alias]

```
[alias]
  st = status
  co = checkout
  br = branch
  ci = commit
  ...
```

### [commit]

```
[commit]
  template = ~/.gitmessage
```

### [delta] (diff pager)

```
[delta]
  navigate = true
  side-by-side = true
  ...
```

## 実行フロー

### 設定確認

1. 現在のGit設定を表示
2. symlinkが正しく設定されているか確認
3. 設定値をユーザーに報告

### 設定変更

1. 変更対象ファイルを確認
2. 変更内容をユーザーに提案
3. ファイルを編集
4. 変更後の設定を確認

## 使用例

- "git configを確認"
- ".gitconfigの内容を見せて"
- "コミットテンプレートを編集"
- "gitignoreにパターンを追加"
- "エディタをvimに変更"

## Git設定の優先順位

1. ローカル（リポジトリ内 `.git/config`）
2. グローバル（`~/.gitconfig`）
3. システム（`/etc/gitconfig`）

## 注意事項

- 変更は `git/.gitconfig` に対して行う（symlinkのため `~/.gitconfig` に反映）
- 機密情報（トークン等）は直接書かない
- 変更後は新しいターミナルまたは `source ~/.zshrc` で反映確認
- エイリアスは oh-my-zsh の git プラグインと競合しないか確認
