---
description: "シンボリックリンクの状態確認・再作成。リンク切れの検出と修復。トリガー: symlink, link, リンク切れ, リンク, シンボリック"
allowed-tools:
  - Bash
  - Read
  - Grep
---

# symlink-manage スキル

dotfilesのシンボリックリンク管理を行う。

## 管理対象のシンボリックリンク

| ターゲット | ソース（laptop repo） |
|-----------|----------------------|
| `~/.zshrc` | `zsh/.zshrc` |
| `~/.aliases` | `zsh/.aliases` |
| `~/.zsh/` | `zsh/.zsh/` |
| `~/.gitconfig` | `git/.gitconfig` |
| `~/.gitmessage` | `git/.gitmessage` |
| `~/.gitignore` | `git/.gitignore_global` |
| `~/.tmux.conf` | `tmux/.tmux.conf` |
| `~/.tigrc` | `tig/.tigrc` |
| `~/.fzf.zsh` | `fzf/.fzf.zsh` |
| `~/.fzf.bash` | `fzf/.fzf.bash` |
| `~/.config/ghostty/config` | `ghostty/config` |
| `~/.config/mise/config.toml` | `mise/config.toml` |
| `~/.claude/` | `claude/` (部分的) |

## コマンド

### 全symlink状態確認

```bash
LAPTOP_DIR="/Users/snkrheadz/ghq/github.com/snkrheadz/laptop"

echo "=== Symlink Status ==="
declare -A SYMLINKS=(
  ["$HOME/.zshrc"]="$LAPTOP_DIR/zsh/.zshrc"
  ["$HOME/.aliases"]="$LAPTOP_DIR/zsh/.aliases"
  ["$HOME/.zsh"]="$LAPTOP_DIR/zsh/.zsh"
  ["$HOME/.gitconfig"]="$LAPTOP_DIR/git/.gitconfig"
  ["$HOME/.gitmessage"]="$LAPTOP_DIR/git/.gitmessage"
  ["$HOME/.gitignore"]="$LAPTOP_DIR/git/.gitignore_global"
  ["$HOME/.tmux.conf"]="$LAPTOP_DIR/tmux/.tmux.conf"
  ["$HOME/.tigrc"]="$LAPTOP_DIR/tig/.tigrc"
  ["$HOME/.fzf.zsh"]="$LAPTOP_DIR/fzf/.fzf.zsh"
  ["$HOME/.fzf.bash"]="$LAPTOP_DIR/fzf/.fzf.bash"
  ["$HOME/.config/ghostty/config"]="$LAPTOP_DIR/ghostty/config"
  ["$HOME/.config/mise/config.toml"]="$LAPTOP_DIR/mise/config.toml"
)

for link in "${!SYMLINKS[@]}"; do
  target="${SYMLINKS[$link]}"
  if [ -L "$link" ]; then
    actual=$(readlink "$link")
    if [ "$actual" = "$target" ]; then
      echo "[OK] $link"
    else
      echo "[WRONG TARGET] $link -> $actual (expected: $target)"
    fi
  elif [ -e "$link" ]; then
    echo "[NOT SYMLINK] $link"
  else
    echo "[MISSING] $link"
  fi
done
```

### 特定symlinkの確認

```bash
ls -la ~/.zshrc
readlink ~/.zshrc
```

### 壊れたsymlinkの検出

```bash
find ~ -maxdepth 3 -type l ! -exec test -e {} \; -print 2>/dev/null
```

### symlinkの再作成（単一ファイル）

```bash
# 例: ~/.zshrc の再作成
rm -f ~/.zshrc
ln -sf /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/.zshrc ~/.zshrc
```

### 全symlinkの再作成（install.sh経由）

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && ./install.sh
```

## 実行フロー

### 状態確認

1. 全symlinkのステータスを確認
2. 壊れたリンクを特定
3. 問題のあるリンクを報告

### 修復

1. 問題のあるsymlinkを特定
2. ユーザーに確認
3. 個別に再作成、または install.sh を推奨

## 使用例

- "symlinkの状態を確認"
- "リンク切れがないかチェック"
- "~/.zshrcのリンクを確認"
- "壊れたリンクを修復"
- "symlinkを再作成"

## safe_ln関数（install.shより）

install.shでは以下の`safe_ln`関数を使用してsymlinkを作成:

```bash
safe_ln() {
  local src="$1"
  local dest="$2"

  # 既存のシンボリックリンクまたはファイルを削除
  if [ -L "$dest" ] || [ -e "$dest" ]; then
    rm -rf "$dest"
  fi

  # 親ディレクトリを作成
  mkdir -p "$(dirname "$dest")"

  # シンボリックリンクを作成
  ln -sf "$src" "$dest"
}
```

## 注意事項

- 既存ファイル（非symlink）がある場合、上書き前にバックアップ推奨
- install.shを使えば全symlinkを一括で再作成可能
- `~/.zsh/` はディレクトリ全体をsymlink
- Claude設定は `claude/` 配下のファイルを個別にsymlink
