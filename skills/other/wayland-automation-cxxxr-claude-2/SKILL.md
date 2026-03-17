---
name: wayland-automation
description: Wayland環境でのGUI自動化。スクリーンショット取得、テキスト入力、クリップボード操作のパターン集
allowed-tools: Bash, Read
---

# Wayland Automation

Wayland環境（niri compositor）でのGUI自動化パターン集。

## 環境確認

```bash
# Wayland環境であることを確認
echo $WAYLAND_DISPLAY  # -> wayland-1 等

# niriが動作していることを確認
pgrep niri
```

## スクリーンショット

### 基本
```bash
# 画面全体（Claude Code用）
screenshot-for-claude
# -> /tmp/claude-screenshot.png

# 画面全体（カスタムパス）
grim /path/to/screenshot.png

# 特定のモニター
grim -o DP-6 output.png
grim -o eDP-1 laptop.png
```

### 領域選択（slurp必要）
```bash
# インタラクティブに領域選択
grim -g "$(slurp)" region.png

# 座標指定
grim -g "100,100 500x300" region.png
```

### 連続撮影
```bash
# 1秒ごとに5枚
for i in {1..5}; do
  grim "/tmp/shot_$i.png"
  sleep 1
done
```

## テキスト入力（wtype）

### 基本入力
```bash
# 単純なテキスト
wtype "Hello World"

# 日本語（IME経由ではない直接入力）
wtype "こんにちは"

# 複数行（\nは使えない、Enterキーを使う）
wtype "Line 1" && wtype -k Return && wtype "Line 2"
```

### 特殊キー
```bash
# 単一キー
wtype -k Return      # Enter
wtype -k Tab         # Tab
wtype -k Escape      # Escape
wtype -k BackSpace   # Backspace
wtype -k Delete      # Delete
wtype -k space       # Space

# ファンクションキー
wtype -k F1
wtype -k F12

# 矢印キー
wtype -k Up
wtype -k Down
wtype -k Left
wtype -k Right

# その他
wtype -k Home
wtype -k End
wtype -k Page_Up
wtype -k Page_Down
```

### モディファイア付き
```bash
# Ctrl + キー
wtype -M ctrl -k c      # Ctrl+C（コピー）
wtype -M ctrl -k v      # Ctrl+V（ペースト）
wtype -M ctrl -k a      # Ctrl+A（全選択）
wtype -M ctrl -k s      # Ctrl+S（保存）
wtype -M ctrl -k z      # Ctrl+Z（アンドゥ）

# Alt + キー
wtype -M alt -k Tab     # Alt+Tab
wtype -M alt -k F4      # Alt+F4（閉じる）

# Shift + キー
wtype -M shift -k Tab   # Shift+Tab

# Super（Mod）キー
wtype -M logo -k d      # Super+D（ランチャー等）

# 複合
wtype -M ctrl -M shift -k t  # Ctrl+Shift+T
```

### タイミング制御
```bash
# 遅延付き入力（ミリ秒）
wtype -d 50 "slow typing"   # 50ms間隔

# 操作間の待機
wtype "first" && sleep 0.5 && wtype "second"
```

## クリップボード（wl-clipboard）

### コピー
```bash
# テキストをコピー
echo "text to copy" | wl-copy

# ファイル内容をコピー
wl-copy < file.txt

# 画像をコピー
wl-copy --type image/png < image.png

# 現在の選択をコピー（primary selection）
wl-copy --primary "text"
```

### ペースト
```bash
# テキストをペースト
wl-paste

# 特定のMIMEタイプ
wl-paste --type text/plain
wl-paste --type image/png > image.png

# クリップボードの内容を確認
wl-paste --list-types
```

### クリップボード監視
```bash
# クリップボード変更時に実行
wl-paste --watch echo "Clipboard changed"
```

## niri操作

### ウィンドウ操作（niri msg）
```bash
# アクティブウィンドウ情報
niri msg focused-window

# ワークスペース一覧
niri msg workspaces

# ワークスペース切り替え
niri msg action focus-workspace 2

# ウィンドウを閉じる
niri msg action close-window
```

### キーバインド経由
```bash
# アプリランチャー起動（Mod+D）
wtype -M logo -k d

# ターミナル起動（Mod+Return）
wtype -M logo -k Return

# ウィンドウを閉じる（Mod+Q）
wtype -M logo -k q

# フルスクリーン（Mod+F）
wtype -M logo -k f
```

## 実践パターン

### パターン1: アプリ起動して操作
```bash
# 1. ランチャー起動
wtype -M logo -k d
sleep 0.5

# 2. アプリ名入力
wtype "firefox"
sleep 0.3

# 3. 起動
wtype -k Return
sleep 2

# 4. 確認
screenshot-for-claude
```

### パターン2: フォーム入力
```bash
# フィールド間をTabで移動しながら入力
wtype "username"
wtype -k Tab
wtype "password"
wtype -k Tab
wtype -k Return  # 送信
```

### パターン3: テキスト編集
```bash
# 全選択してコピー
wtype -M ctrl -k a
sleep 0.1
wtype -M ctrl -k c

# 内容を取得
content=$(wl-paste)
echo "$content"

# 編集して戻す
echo "$content (edited)" | wl-copy
wtype -M ctrl -k v
```

### パターン4: 設定変更サイクル
```bash
# waybar設定変更の例
edit_waybar() {
  # 1. 現状確認
  screenshot-for-claude

  # 2. 設定編集（外部で実行）
  # Edit ~/.config/waybar/config

  # 3. リロード
  pkill waybar
  sleep 0.5
  waybar &
  sleep 1

  # 4. 結果確認
  screenshot-for-claude
}
```

## トラブルシューティング

### wtype が動作しない
```bash
# 環境変数確認
echo $WAYLAND_DISPLAY
echo $XDG_RUNTIME_DIR

# 権限確認
ls -la $XDG_RUNTIME_DIR/$WAYLAND_DISPLAY
```

### スクリーンショットが黒い
```bash
# grim が正しいseatにアクセスできているか
grim -l  # 利用可能な出力一覧
```

### クリップボードが動作しない
```bash
# wl-clipboard が Wayland に接続できているか
wl-paste --list-types
```

### 日本語入力
```bash
# fcitx5 経由での入力はwtypeでは直接サポートされない
# 代わりにクリップボード経由で入力
echo "日本語テキスト" | wl-copy
wtype -M ctrl -k v
```
