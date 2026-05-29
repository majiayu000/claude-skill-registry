---
description: "バックアップ確認とロールバック。dotfiles設定を以前の状態に復元。トリガー: rollback, backup, restore, 復元, 元に戻す"
allowed-tools:
  - Bash
  - Read
---

# dotfiles-rollback スキル

dotfilesのバックアップ確認と以前の状態への復元を行う。

## バックアップの仕組み

- バックアップ場所: `~/.dotfiles_backup/<timestamp>/`
- 最後のバックアップ記録: `~/.dotfiles_last_backup`
- `install.sh` 実行時に自動作成

## 利用可能なコマンド

### バックアップ一覧確認

```bash
ls -la ~/.dotfiles_backup/
```

### 最後のバックアップ確認

```bash
cat ~/.dotfiles_last_backup
```

### 特定バックアップの内容確認

```bash
ls -la ~/.dotfiles_backup/<timestamp>/
```

### バックアップファイルの中身確認

```bash
cat ~/.dotfiles_backup/<timestamp>/<filename>
```

### 現在のシンボリックリンク確認

```bash
ls -la ~/.zshrc ~/.gitconfig ~/.tmux.conf
```

### rollback.sh実行（対話的）

```bash
/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/rollback.sh
```

### 特定バックアップを指定してロールバック

```bash
/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/rollback.sh <timestamp>
```

## バックアップ対象ファイル

| ファイル | 説明 |
|---------|------|
| `~/.zshrc` | zshメイン設定 |
| `~/.aliases` | エイリアス |
| `~/.gitconfig` | Git設定 |
| `~/.gitmessage` | コミットテンプレート |
| `~/.gitignore` | グローバルgitignore |
| `~/.git_template` | Gitテンプレート |
| `~/.tmux.conf` | tmux設定 |
| `~/.tigrc` | tig設定 |
| `~/.fzf.zsh` | fzf設定(zsh) |
| `~/.fzf.bash` | fzf設定(bash) |
| `~/.zsh/` | zshディレクトリ |
| `~/.claude/statusline.sh` | Claude statusline |

## 実行フロー

### バックアップ状態確認

1. バックアップディレクトリ一覧を取得
2. 各バックアップのタイムスタンプと内容を報告
3. 現在の設定との差分を確認（必要に応じて）

### ロールバック実行

1. 利用可能なバックアップを提示
2. ユーザーにロールバック先を確認
3. `rollback.sh` を実行
4. 結果を報告

## 使用例

- "バックアップを確認"
- "ロールバックしたい"
- "以前の設定に戻す"
- "最後のバックアップはいつ？"
- "gitconfigを元に戻す"

## rollback.shの動作

1. auto-syncを無効化（launchdアンロード）
2. シンボリックリンクを削除
3. バックアップからファイルを復元

## 注意事項

- ロールバックは確認プロンプトあり（y/N）
- ロールバック後はターミナル再起動が必要
- auto-syncも無効化される
- 復元後に再度`install.sh`で最新状態に戻せる
