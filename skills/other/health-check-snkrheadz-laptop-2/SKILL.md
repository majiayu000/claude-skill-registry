---
description: "dotfiles全体の健全性チェック。シンボリックリンク、設定ファイル、依存関係の状態確認。トリガー: 健全性, 診断, check, health, dotfiles状態"
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# health-check スキル

dotfilesリポジトリ全体の健全性をチェックする。

## チェック項目

### 1. シンボリックリンクの状態

```bash
# すべての期待されるsymlinkの確認
for link in ~/.zshrc ~/.aliases ~/.gitconfig ~/.gitmessage ~/.gitignore ~/.tmux.conf ~/.tigrc ~/.fzf.zsh ~/.fzf.bash; do
  if [ -L "$link" ]; then
    target=$(readlink "$link")
    if [ -e "$target" ]; then
      echo "[OK] $link -> $target"
    else
      echo "[BROKEN] $link -> $target (target does not exist)"
    fi
  elif [ -e "$link" ]; then
    echo "[NOT SYMLINK] $link exists but is not a symlink"
  else
    echo "[MISSING] $link does not exist"
  fi
done
```

### 2. .zsh ディレクトリの確認

```bash
# zsh functions と configs の確認
ls -la ~/.zsh/functions/ 2>/dev/null | head -10
ls -la ~/.zsh/configs/ 2>/dev/null | head -10
ls -la ~/.zsh/configs/pre/ 2>/dev/null | head -10
ls -la ~/.zsh/configs/post/ 2>/dev/null | head -10
```

### 3. Claude設定の確認

```bash
# Claude Code設定の確認
for item in ~/.claude/settings.json ~/.claude/statusline.sh ~/.claude/CLAUDE.md ~/.claude/hooks ~/.claude/agents; do
  if [ -L "$item" ] || [ -e "$item" ]; then
    echo "[OK] $item exists"
  else
    echo "[MISSING] $item"
  fi
done
```

### 4. Ghostty設定の確認

```bash
ls -la ~/.config/ghostty/config 2>/dev/null
```

### 5. mise設定の確認

```bash
ls -la ~/.config/mise/config.toml 2>/dev/null
mise list 2>/dev/null | head -10
```

### 6. Homebrewの状態

```bash
brew doctor 2>&1 | head -20
```

### 7. pre-commitフックの状態

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && ls -la .git/hooks/pre-commit 2>/dev/null
```

### 8. auto-syncの状態

```bash
launchctl list | grep dotfiles
ls -la ~/Library/LaunchAgents/com.user.dotfiles-sync.plist 2>/dev/null
```

### 9. secrets.envの存在確認

```bash
ls -la ~/.secrets.env 2>/dev/null
```

## 実行フロー

### フルヘルスチェック

1. すべてのsymlinkをチェック
2. zsh設定構造を確認
3. Claude設定を確認
4. 外部ツール設定を確認
5. Homebrew状態を確認
6. auto-sync状態を確認
7. セキュリティ設定を確認
8. 結果サマリーを報告

## 使用例

- "dotfilesの状態を確認"
- "健全性チェックを実行"
- "設定が正しくリンクされているか確認"
- "health check"
- "dotfiles診断"

## 出力形式

```
## dotfiles健全性レポート

### シンボリックリンク: X/Y OK
- [OK] ~/.zshrc
- [BROKEN] ~/.tmux.conf

### 設定ファイル: X/Y OK
...

### 依存ツール: X/Y OK
...

### 総合評価: HEALTHY / NEEDS ATTENTION / CRITICAL
```

## 注意事項

- 壊れたsymlinkは `install.sh` で再作成可能
- Homebrewの問題は `brew doctor` の指示に従う
- auto-syncが動いていない場合は launchd を確認
