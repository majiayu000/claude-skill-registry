---
name: dotfiles
description: 'Use when managing dotfiles repository. Triggers: (1) checking dotfiles
  structure or package list, (2) adding or removing packages, (3) setting up dotfiles
  on new machine, (4) syncing changes from othe'
---

---
name: dotfiles
description: Use when managing dotfiles repository. Triggers: (1) checking dotfiles structure or package list, (2) adding or removing packages, (3) setting up dotfiles on new machine, (4) syncing changes from other machines, (5) stow command usage questions.
---

# dotfiles 管理スキル

## 実行方法

パッケージ操作やセットアップはsubagentを起動して実行すること。
構成調査が必要な場合はGemini MCPに委託する。

## 関連ドキュメント

- @structure.md - リポジトリ構成
- @maintenance.md - メンテナンス方針
- @sync.md - 更新の取り込み
- @setup.md - 新規PCセットアップ

## クイックリファレンス

### よく使うコマンド

```bash
# 全パッケージをインストール
./install.sh

# 特定パッケージのみ
./install.sh shell nvim

# ドライラン（変更確認）
./install.sh -n

# パッケージ削除
./install.sh -D shell

# MCPサーバーインストール
~/.claude/scripts/install-mcp.sh
```

### パッケージ追加手順

1. `packages/<name>/` ディレクトリ作成
2. ホームディレクトリからの相対パスで配置
3. `./install.sh <name>` で適用
