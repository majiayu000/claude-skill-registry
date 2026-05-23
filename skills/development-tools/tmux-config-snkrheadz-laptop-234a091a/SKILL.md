---
description: "tmux設定管理。.tmux.confの確認・編集、キーバインド設定。トリガー: tmux, tmux.conf, ターミナル分割, セッション"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Grep
---

# tmux-config スキル

tmux設定ファイルの確認・編集を行う。

## 管理対象ファイル

| ファイル | 説明 | symlink先 |
|---------|------|-----------|
| `tmux/.tmux.conf` | tmux設定 | `~/.tmux.conf` |

## コマンド

### .tmux.conf確認

```bash
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/tmux/.tmux.conf
```

### symlink状態確認

```bash
ls -la ~/.tmux.conf
```

### tmuxセッション一覧

```bash
tmux list-sessions 2>/dev/null || echo "No running sessions"
```

### tmuxウィンドウ一覧

```bash
tmux list-windows 2>/dev/null || echo "No running sessions"
```

### 設定の再読み込み（tmux内で実行）

```bash
tmux source-file ~/.tmux.conf
```

### tmuxバージョン確認

```bash
tmux -V
```

## .tmux.confの主要設定

### プレフィックスキー

```
# デフォルト: Ctrl+b
# よく使われる変更: Ctrl+a
set -g prefix C-a
unbind C-b
bind C-a send-prefix
```

### ペイン操作

```
# 縦分割: prefix + |
bind | split-window -h
# 横分割: prefix + -
bind - split-window -v
```

### ペイン移動

```
# vim風移動: prefix + h/j/k/l
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R
```

### マウス設定

```
set -g mouse on
```

### コピーモード

```
setw -g mode-keys vi
```

### 外観

```
# ステータスバー
set -g status-style bg=black,fg=white
set -g status-left "[#S] "
set -g status-right "%Y-%m-%d %H:%M"
```

## よく使うキーバインド

| キー | 説明 |
|-----|------|
| `prefix + c` | 新しいウィンドウ作成 |
| `prefix + n` | 次のウィンドウ |
| `prefix + p` | 前のウィンドウ |
| `prefix + ,` | ウィンドウ名変更 |
| `prefix + [` | コピーモード |
| `prefix + ]` | ペースト |
| `prefix + d` | デタッチ |
| `prefix + ?` | キーバインド一覧 |

## 実行フロー

### 設定確認

1. .tmux.confの内容確認
2. symlinkの状態確認
3. 現在のセッション状態確認

### 設定変更

1. 現在の設定を確認
2. 変更内容を提案
3. ファイルを編集
4. `tmux source-file ~/.tmux.conf` で再読み込み

## 使用例

- "tmux設定を確認"
- ".tmux.confの内容を見せて"
- "プレフィックスキーをCtrl+aに変更"
- "マウス操作を有効化"
- "ペインの分割キーを変更"

## tmuxの基本操作

```bash
# 新しいセッション開始
tmux new -s session-name

# 既存セッションにアタッチ
tmux attach -t session-name

# セッション一覧
tmux ls

# セッション終了
tmux kill-session -t session-name
```

## 注意事項

- 設定変更後は `tmux source-file ~/.tmux.conf` で反映
- 一部の設定はtmux再起動が必要
- プラグインマネージャー（TPM）を使う場合は追加設定が必要
- 変更は `tmux/.tmux.conf` に対して行う（symlinkのため `~/.tmux.conf` に反映）
