---
name: mcp-builder-jp
description: Simplified Japanese MCP (Model Context Protocol) server builder skill covering project setup, Japanese API integrations (Chatwork, Backlog, freee, kintone), and development guidelines. Triggers on requests for MCPサーバー構築, MCP開発, MCPツール作成.
---

# MCPサーバー構築支援スキル

## 概要

MCP（Model Context Protocol）サーバーの設計・構築を支援するスキルです。日本で広く使われるビジネスAPIとの連携を中心に、プロジェクト構成からツール定義までをカバーします。

## MCPサーバーの基本構成

MCPサーバーは、LLMが外部ツール・データソースにアクセスするための標準プロトコルです。

```
クライアント (Claude等) ←→ MCPサーバー ←→ 外部API / データベース
```

### 主要な構成要素

| 要素 | 説明 |
|------|------|
| **Tools** | LLMが呼び出せる関数（API操作、データ取得など） |
| **Resources** | LLMが読み取れるデータソース（ファイル、DB） |
| **Prompts** | 再利用可能なプロンプトテンプレート |

## 日本のAPI連携例

### Chatwork API

```typescript
// チャットワークへのメッセージ送信ツール
server.tool("chatwork_send_message", {
  room_id: z.string().describe("ルームID"),
  body: z.string().describe("メッセージ本文"),
}, async ({ room_id, body }) => {
  const res = await fetch(
    `https://api.chatwork.com/v2/rooms/${room_id}/messages`,
    { method: "POST", headers: { "X-ChatWorkToken": TOKEN },
      body: new URLSearchParams({ body }) }
  );
  return { content: [{ type: "text", text: `送信完了: ${res.status}` }] };
});
```

### Backlog API

- 課題の作成・更新・検索
- Wiki ページの取得・編集
- プロジェクト情報の参照

### freee会計 API

- 取引の登録・検索
- 勘定科目の取得
- 請求書の作成

### kintone API

- レコードの取得・登録・更新
- アプリ情報の参照
- フィールド定義の取得

## プロジェクト構成テンプレート

```
my-mcp-server/
├── src/
│   ├── index.ts          # エントリポイント（サーバー起動）
│   ├── tools/            # ツール定義
│   │   ├── chatwork.ts   # Chatwork 連携ツール
│   │   └── backlog.ts    # Backlog 連携ツール
│   ├── resources/        # リソース定義
│   └── utils/            # ユーティリティ関数
├── package.json
├── tsconfig.json
└── README.md             # 日本語ドキュメント
```

### 基本的なサーバー初期化

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

// ツールの登録
// server.tool(...) でツールを追加

const transport = new StdioServerTransport();
await server.connect(transport);
```

## 開発ルール

### コメント・ドキュメントは日本語で記述

```typescript
/**
 * Chatworkの指定ルームにメッセージを送信する
 * @param roomId - 送信先のルームID
 * @param message - 送信するメッセージ本文
 * @returns 送信結果のステータス
 */
```

### ツール説明文の日本語化

- `describe()` の引数は日本語で記述する
- LLMがツールの用途を正しく理解できるよう、具体的に記述する

### エラーメッセージの日本語化

- API エラーは日本語で分かりやすく返す
- 例: `"Chatworkへの送信に失敗しました（ステータス: 401 認証エラー）"`

## 参考リンク

- [MCP仕様書](https://spec.modelcontextprotocol.io/)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCPサーバー一覧](https://github.com/modelcontextprotocol/servers)
