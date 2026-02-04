---
name: mcp
description: >
  Model Context Protocol (MCP) サーバーの作成・管理ガイド。カスタムツールの追加方法。
  使用タイミング: (1) Claude Codeにカスタムツールを追加したい時 (2) 外部サービス連携時
  (3) プロジェクト固有の自動化ツールを作りたい時 (4) MCPサーバーの設定方法を知りたい時。
  トリガー例: 「MCPサーバーを作って」「カスタムツールを追加」「MCP設定」
  「外部APIをツール化」「テストランナーMCP」
---

# mcp - MCP Server 作成

Model Context Protocol (MCP) サーバーの作成・管理。

---

## 概要

MCP は Claude Code にカスタムツールを追加するためのプロトコル。

**用途**:
- プロジェクト固有のツール提供
- 外部サービス連携
- 自動化タスク

---

## 基本構造

```javascript
// scripts/mcp/my-tool.js
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "my-tool", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// ツール一覧
server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "my_custom_tool",
      description: "カスタムツールの説明",
      inputSchema: {
        type: "object",
        properties: {
          param1: { type: "string", description: "パラメータ1" },
        },
        required: ["param1"],
      },
    },
  ],
}));

// ツール実行
server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "my_custom_tool") {
    const result = await doSomething(args.param1);
    return { content: [{ type: "text", text: JSON.stringify(result) }] };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// サーバー起動
const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## 設定

### プロジェクトレベル (.mcp.json)

```json
{
  "mcpServers": {
    "my-tool": {
      "command": "node",
      "args": ["scripts/mcp/my-tool.js"]
    }
  }
}
```

### ユーザーレベル (~/.claude/settings.json)

```json
{
  "mcpServers": {
    "my-global-tool": {
      "command": "node",
      "args": ["/path/to/tool.js"]
    }
  }
}
```

---

## 実用例

### テストランナー

```javascript
server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "run_tests",
      description: "ユニットテストを実行",
      inputSchema: {
        type: "object",
        properties: {
          pattern: { type: "string", description: "テストパターン" },
        },
      },
    },
  ],
}));

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "run_tests") {
    const pattern = request.params.arguments?.pattern || "";
    const result = await runTests(pattern);
    return { content: [{ type: "text", text: result }] };
  }
});

async function runTests(pattern) {
  const { execSync } = await import("child_process");
  try {
    const output = execSync(`npm test -- ${pattern}`, { encoding: "utf-8" });
    return output;
  } catch (error) {
    return error.stdout + error.stderr;
  }
}
```

### DB クエリ

```javascript
{
  name: "query_database",
  description: "データベースにクエリを実行",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string", description: "SQL クエリ" },
    },
    required: ["query"],
  },
}
```

---

## コンテキスト節約

使わないMCPサーバーを無効化してコンテキストを節約:

```json
// .mcp.json
{
  "mcpServers": {
    "frequently-used": { "command": "node", "args": ["tool1.js"] }
  },
  "disabledMcpServers": [
    "rarely-used-tool",
    "heavy-context-tool"
  ]
}
```

---

## デバッグ

```bash
# 直接実行
node scripts/mcp/my-tool.js

# ログ確認
DEBUG=mcp* node scripts/mcp/my-tool.js

# Claude Code で確認
# /mcp コマンドで接続状態を確認
```

---

## ベストプラクティス

1. **エラーハンドリング**: 常に try-catch で囲む
2. **タイムアウト**: 長時間処理は避ける（30秒以内）
3. **説明を明確に**: description はツール選択の判断材料
4. **inputSchema 必須**: パラメータの型を明示
5. **10個以下**: プロジェクトあたりのMCP数を制限
