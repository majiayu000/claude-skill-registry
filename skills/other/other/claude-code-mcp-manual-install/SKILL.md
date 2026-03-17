---
name: claude-code-mcp-manual-install
description: "Use when adding MCP servers from within a Claude Code session where CLI is unavailable. jq-based ~/.claude.json editing workaround."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-13"
---
# Claude Code 内での MCP サーバー手動インストール

**Extracted:** 2026-02-13
**Context:** Claude Code セッション内から MCP サーバーを追加する際、CLI が使えない場合の回避策

## Problem

Claude Code 内から MCP サーバーを追加しようとすると、2つの障壁がある。

1. `claude mcp add` はネストされた Claude Code セッション内では実行不可
   ```
   Error: Claude Code cannot be launched inside another Claude Code session.
   ```

2. `npx @smithery/cli install` はインタラクティブ入力を要求し、非対話環境で crash する
   ```
   Error [ERR_USE_AFTER_CLOSE]: readline was closed
   ```

## Solution

`~/.claude.json` の `mcpServers` セクションを `jq` で直接編集する。

```bash
# MCP サーバーを追加
jq '.mcpServers.ServerName = {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "package-name"]
}' ~/.claude.json > /tmp/claude.json.tmp && mv /tmp/claude.json.tmp ~/.claude.json

# 追加されたことを確認
jq '.mcpServers | keys' ~/.claude.json
```

### HTTP タイプの場合

```bash
jq '.mcpServers.ServerName = {
  "type": "http",
  "url": "https://example.com/mcp"
}' ~/.claude.json > /tmp/claude.json.tmp && mv /tmp/claude.json.tmp ~/.claude.json
```

## 注意点

- **セッション再起動が必要**: MCP サーバーはセッション開始時にロードされるため、追加後は Claude Code を再起動する
- **~/.claude.json は頻繁に更新される**: Claude Code 自身がメトリクスを書き込むため、Read → Edit パターンでは「file modified since read」エラーが頻発する。jq でアトミックに書き換えるのが確実
- **バックアップ推奨**: 大量のセッション統計データを含むファイルなので、壊すと面倒

## When to Use

- Claude Code セッション中に新しい MCP サーバーを追加したい時
- Smithery CLI が環境依存で動かない時
- 非対話的に MCP サーバーを一括設定したい時
