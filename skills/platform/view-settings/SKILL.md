---
name: view-settings
description: プロジェクトの Claude Code 設定を表示する。「設定を見せて」「現在の設定」「settings 確認」「設定情報」「Claude の設定を表示」「設定を確認」「settings を見たい」などで起動。
allowed-tools: [Read, Glob]
---

# View Settings

プロジェクトの Claude Code 設定を表示します。

## 実行手順

1. 以下のファイルを読み込む:
   - `.claude/settings.json`（プロジェクト設定）
   - `.claude/settings.local.json`（ローカル設定、存在する場合のみ）

2. 設定内容をセクション別に整形して表示

### 出力フォーマット

```markdown
## 現在の設定

### ソース

| ファイル | 状態 |
|----------|------|
| .claude/settings.json | ✅ 存在 |
| .claude/settings.local.json | ❌ なし |

### Permissions

**Allow:**
- Bash(git status:*)
- Bash(npm:*)

**Deny:**
- Bash(rm -rf:*)

### Hooks

| イベント | 件数 |
|----------|------|
| PreToolUse | 2 |
| PostToolUse | 1 |

### 環境変数（env）

| 変数名 | 値 |
|--------|-----|
| NODE_ENV | development |

### マーケットプレイス（extraKnownMarketplaces）

| 名前 | ソース |
|------|--------|
| shiiman-claude-code-plugins | directory: . |

### プラグイン（enabledPlugins）

| プラグイン | 状態 |
|------------|------|
| shiiman-plugin@shiiman-claude-code-plugins | ✅ 有効 |

### その他の設定

| 設定 | 値 |
|------|-----|
| model | opus |
```

### 表示項目

| 項目 | 説明 |
|------|------|
| permissions | allow/deny リスト |
| hooks | イベント別の件数サマリ |
| env | 環境変数 |
| extraKnownMarketplaces | 追加マーケットプレイス |
| enabledPlugins | 有効なプラグイン |
| model | 使用モデル |
| その他 | 上記以外の設定 |

### 重要な注意事項

- ✅ settings.json と settings.local.json の両方を確認
- ✅ 存在しないファイルは「なし」と表示
- ✅ 空のセクションは省略
- ✅ 機密情報（API キーなど）がある場合はマスク表示
- ❌ 設定の変更は行わない（表示のみ）
