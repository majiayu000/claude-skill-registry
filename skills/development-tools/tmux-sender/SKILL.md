---
name: tmux-sender
description: tmux の別ペインにコマンドを送信する。「ペインで実行して」「tmuxで送信」などのリクエストで使用。
allowed-tools: Bash(tmux:*)
---

# tmux コマンド送信スキル

## 使い方

tmux のペインにコマンドを送信して実行する場合：

tmux send-keys -t <ペイン番号> '<コマンド>' Enter

## 手順

1. tmux list-panes でペイン一覧を確認
2. tmux send-keys -t <ペイン番号> '<コマンド>' Enter で送信・実行
