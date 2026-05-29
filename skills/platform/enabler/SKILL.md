---
name: enabler
description: 指定したプラグインを有効化する。「プラグインを有効化」「〇〇をオンにして」「〇〇を有効にして」「プラグインを有効に」「〇〇を使えるようにして」「プラグインをオンに」「〇〇を有効化して」などで起動。claude plugin enable コマンドを使用して有効化。
---

# Plugin Enabler

無効化されているプラグインを有効化します。

## 実行内容

1. `commands/enable.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-plugin:enable` を SlashCommand ツールで実行（実装は Commands に委譲）

## ドキュメント参照

- `commands/enable.md` - 機能の詳細
- `/shiiman-plugin:enable` - 機能の実装

## コマンド連携

実際の処理は `/shiiman-plugin:enable` に委譲します（SSOT として扱う）
