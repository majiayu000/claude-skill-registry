# MCP Lister

インストール済みの MCP サーバー一覧を表示するスキル。「MCP 一覧」「MCP サーバー確認」「インストール済み MCP」「MCP を見せて」「mcp list」「MCP サーバー一覧」「利用可能な MCP」などで起動。

## スキル情報

```yaml
name: mcp-lister
description: インストール済みの MCP サーバー一覧を表示するスキル。「MCP 一覧」「MCP サーバー確認」「インストール済み MCP」「MCP を見せて」「mcp list」「MCP サーバー一覧」「利用可能な MCP」などで起動。
allowedTools:
  - Bash
```

## Claude への指示

### 実行手順

1. `claude mcp list` コマンドを実行
2. 結果を整形して表示

### 出力フォーマット

```markdown
## インストール済み MCP サーバー

| 名前 | スコープ | 状態 |
|------|----------|------|
| github | user | ✅ 有効 |
| filesystem | project | ✅ 有効 |
| context7 | user | ✅ 有効 |

合計: 3 サーバー
```

### スコープの説明

| スコープ | 説明 |
|----------|------|
| user | ユーザー全体で利用可能 |
| project | 現在のプロジェクトのみ |

### 重要な注意事項

- ✅ `claude mcp list` の出力を整形
- ✅ MCP サーバーがない場合は「MCP サーバーは設定されていません」と表示
- ✅ 各サーバーの状態を表示
- ❌ MCP サーバーの追加・削除は行わない（表示のみ）
