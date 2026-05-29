---
name: updater
description: 指定したプラグインを最新バージョンに更新する。「プラグインを更新」「〇〇をアップデート」「最新版にして」「プラグインをアップデート」「〇〇を更新して」「プラグインを最新に」「〇〇のバージョンを上げて」「全部アップデート」「プラグイン全部更新」「まとめて更新」などで起動。claude plugin update コマンドを使用して更新。
---

# Plugin Updater

インストール済みのプラグインを最新バージョンに更新します。

## 実行内容

1. `commands/update.md` を Read ツールで参照（SSOT として扱う）
2. `/shiiman-plugin:update` を SlashCommand ツールで実行（実装は Commands に委譲）

## ドキュメント参照

- `commands/update.md` - 機能の詳細
- `/shiiman-plugin:update` - 機能の実装

## コマンド連携

実際の処理は `/shiiman-plugin:update` に委譲します（SSOT として扱う）

### 一括更新の場合

「全部アップデート」「プラグイン全部更新」「まとめて更新」などの場合は、`/shiiman-plugin:update --all` を実行します。
