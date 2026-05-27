---
name: disabler
description: 指定したプラグインを無効化する。「プラグインを無効化」「〇〇をオフにして」「〇〇を無効にして」「プラグインを無効に」「〇〇を止めて」「プラグインをオフに」「〇〇を無効化して」などで起動。claude plugin disable コマンドを使用して無効化。
---

# Plugin Disabler

有効なプラグインを無効化します。

## 実行内容

1. `commands/disable.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-plugin:disable` を SlashCommand ツールで実行（実装は Commands に委譲）

## ドキュメント参照

- `commands/disable.md` - 機能の詳細
- `/shiiman-plugin:disable` - 機能の実装

## コマンド連携

実際の処理は `/shiiman-plugin:disable` に委譲します（SSOT として扱う）
