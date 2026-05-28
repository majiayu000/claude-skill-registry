---
name: remove-mcp
description: MCP サーバーを削除する。「MCP 削除」「MCP を外して」「MCP サーバー削除」「mcp remove」「MCP を消して」「MCP サーバーをアンインストール」「MCP を取り除いて」などで起動。
allowed-tools: [Bash, AskUserQuestion]
---

# Remove MCP

MCP サーバーを削除します。

## 実行手順

1. まず `claude mcp list` で現在のサーバー一覧を表示
2. ユーザーに削除対象のサーバー名を確認
3. `claude mcp remove <name>` コマンドを実行
4. 削除完了メッセージを表示

### 削除確認フォーマット

```markdown
## MCP サーバー削除

現在インストールされているサーバー:

| 名前 | スコープ |
|------|----------|
| github | user |
| filesystem | project |

削除するサーバー名を入力してください。
```

### 出力フォーマット（削除完了時）

```markdown
## 削除完了

MCP サーバー「github」を削除しました。

現在のサーバー数: 1
```

### 重要な注意事項

- ✅ 削除前に現在のサーバー一覧を表示
- ✅ 削除前に確認を求める
- ✅ 削除後に残りのサーバー数を表示
- ❌ 複数サーバーの一括削除は行わない（1つずつ確認）
