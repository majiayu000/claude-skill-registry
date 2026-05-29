---
name: installer
description: 指定したプラグインをインストールする。「プラグインをインストール」「〇〇を追加して」「プラグインを入れて」「〇〇をインストールして」「プラグインを導入」「〇〇を使えるようにして」「新しいプラグインを追加」などで起動。claude plugin install コマンドを使用してインストール。
---

# Plugin Installer

指定したプラグインをインストールします。

## 実行内容

1. `commands/install.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-plugin:install [plugin-name]` を SlashCommand ツールで実行（実装は Commands に委譲）

## ドキュメント参照

- `commands/install.md` - 機能の詳細
- `/shiiman-plugin:install` - 機能の実装

## コマンド連携

実際の処理は `/shiiman-plugin:install` に委譲します（SSOT として扱う）
