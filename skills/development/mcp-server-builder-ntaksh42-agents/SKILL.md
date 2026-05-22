---
name: mcp-server-builder
description: Build Model Context Protocol (MCP) servers with best practices. Generate production-ready MCP servers in Python or TypeScript with tools, resources, and prompts.
---

# MCP Server Builder Skill

Model Context Protocol (MCP) サーバーを簡単に構築するスキルです。

## 概要

このスキルは、Anthropicの**Model Context Protocol (MCP)**に準拠したサーバーを自動生成します。MCPは、LLM（大規模言語モデル）が外部ツール、データベース、APIと標準化されたインターフェースで動的に対話できるオープンスタンダードです。

## 主な機能

- **フル機能のMCPサーバー生成**: Python、TypeScript、C#、Goに対応
- **3つのMCP機能実装**: Tools、Resources、Prompts
- **ベストプラクティス適用**: ログ、エラーハンドリング、スキーマ検証
- **本番環境対応**: セキュリティ、パフォーマンス、保守性を考慮
- **Claude Desktop統合**: 設定ファイル自動生成
- **テストコード付属**: 包括的なテストスイート
- **デバッグサポート**: ログとエラートレース機能
- **ドキュメント自動生成**: README、API仕様書、使い方ガイド

## MCPとは？

**Model Context Protocol (MCP)**は、LLMアプリケーションとデータソース間の標準化された接続方法です。

### MCPの3つの主要機能

1. **Tools（ツール）**: LLMが呼び出せる関数
   - API呼び出し、データベースクエリ、計算処理など

2. **Resources（リソース）**: ファイル的なデータ
   - ドキュメント、設定ファイル、データベース内容など

3. **Prompts（プロンプト）**: 事前定義されたテンプレート
   - 再利用可能なプロンプト、ワークフローテンプレート

## サポート言語

### TypeScript
- **推奨**: 最新機能が最初に実装される
- **SDK**: `@modelcontextprotocol/sdk`
- **バリデーション**: Zod（組み込み）
- **ロギング**: pino、winston

### Python
- **SDK**: `mcp`
- **バリデーション**: Pydantic
- **ロギング**: logging（標準ライブラリ）
- **非同期**: asyncio

### その他
- **C#**: 公式SDKあり（2025年4月リリース）
- **Go**: 公式SDKあり（機能は後追い）

## 使用方法

### 基本的なMCPサーバー生成

```
MCPサーバーを作成してください：

名前: weather-server
言語: TypeScript
機能:
- 天気予報を取得するツール
- 天気アラートを取得するツール
```

### Pythonサーバーの生成

```
Python MCPサーバーを作成：

名前: github-analyzer
機能:
- GitHubリポジトリを分析するツール
- コミット履歴を取得するリソース
- PR レビューテンプレートのプロンプト
依存関係: requests, PyGithub
```

### フル機能サーバー

```
本番環境向けMCPサーバーを生成：

名前: database-manager
言語: TypeScript
Tools:
- データベースクエリ実行
- スキーマ情報取得
Resources:
- テーブル一覧
- インデックス情報
Prompts:
- SQLクエリ最適化
- スキーマ設計レビュー
認証: API Key
ロギング: 詳細
エラーハンドリング: 包括的
テスト: 含む
```

## 生成パターン

### 1. TypeScript サーバー（基本）

**入力**:
```
TypeScript MCPサーバーを作成：
名前: calculator
ツール: add, subtract, multiply, divide
```

**生成されるファイル構成**:
```
calculator-mcp/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts          # メインサーバー
│   ├── tools.ts          # ツール実装
│   └── types.ts          # 型定義
├── tests/
│   └── tools.test.ts     # テスト
├── README.md
└── .env.example
```

**src/index.ts**:
```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

// ツールスキーマ定義
const AddArgsSchema = z.object({
  a: z.number().describe("First number"),
  b: z.number().describe("Second number"),
});

const server = new Server(
  {
    name: "calculator-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// ツール一覧を返す
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "add",
        description: "Add two numbers together",
        inputSchema: {
          type: "object",
          properties: {
            a: { type: "number", description: "First number" },
            b: { type: "number", description: "Second number" },
          },
          required: ["a", "b"],
        },
      },
      {
        name: "subtract",
        description: "Subtract second number from first",
        inputSchema: {
          type: "object",
          properties: {
            a: { type: "number" },
            b: { type: "number" },
          },
          required: ["a", "b"],
        },
      },
    ],
  };
});

// ツール実行ハンドラー
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "add": {
      const validated = AddArgsSchema.parse(args);
      const result = validated.a + validated.b;
      return {
        content: [
          {
            type: "text",
            text: `Result: ${validated.a} + ${validated.b} = ${result}`,
          },
        ],
      };
    }

    case "subtract": {
      const validated = AddArgsSchema.parse(args);
      const result = validated.a - validated.b;
      return {
        content: [
          {
            type: "text",
            text: `Result: ${validated.a} - ${validated.b} = ${result}`,
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// サーバー起動
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // CRITICAL: stderr にログ出力（stdout はプロトコル通信用）
  console.error("Calculator MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
```

### 2. Python サーバー（リソース付き）

**入力**:
```
Python MCPサーバーを作成：
名前: file-manager
機能:
- ファイル一覧取得（リソース）
- ファイル読み込み（ツール）
- ファイル書き込み（ツール）
```

**生成されるファイル構成**:
```
file-manager-mcp/
├── pyproject.toml
├── src/
│   └── file_manager/
│       ├── __init__.py
│       ├── server.py       # メインサーバー
│       ├── tools.py        # ツール実装
│       └── resources.py    # リソース実装
├── tests/
│   └── test_server.py
└── README.md
```

**src/file_manager/server.py**:
```python
import asyncio
import logging
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    Resource,
    TextContent,
    CallToolRequest,
    ListResourcesRequest,
    ListToolsRequest,
    ReadResourceRequest,
)
from pydantic import BaseModel, Field

# CRITICAL: stderr にログ出力（stdout はプロトコル通信用）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # デフォルトで stderr
)
logger = logging.getLogger("file-manager")


class ReadFileArgs(BaseModel):
    """ファイル読み込み引数"""
    path: str = Field(description="Path to the file to read")


class WriteFileArgs(BaseModel):
    """ファイル書き込み引数"""
    path: str = Field(description="Path to the file to write")
    content: str = Field(description="Content to write to the file")


class FileManagerServer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.server = Server("file-manager")
        self._setup_handlers()

    def _setup_handlers(self):
        """ハンドラー登録"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="read_file",
                    description="Read contents of a file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "File path to read",
                            }
                        },
                        "required": ["path"],
                    },
                ),
                Tool(
                    name="write_file",
                    description="Write content to a file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"},
                        },
                        "required": ["path", "content"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            if name == "read_file":
                args = ReadFileArgs(**arguments)
                file_path = self.base_path / args.path

                if not file_path.exists():
                    raise ValueError(f"File not found: {args.path}")

                content = file_path.read_text()
                return [TextContent(type="text", text=content)]

            elif name == "write_file":
                args = WriteFileArgs(**arguments)
                file_path = self.base_path / args.path

                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(args.content)

                return [
                    TextContent(
                        type="text",
                        text=f"Successfully wrote {len(args.content)} bytes to {args.path}",
                    )
                ]

            raise ValueError(f"Unknown tool: {name}")

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """ディレクトリ内のファイル一覧"""
            resources = []
            for file_path in self.base_path.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(self.base_path)
                    resources.append(
                        Resource(
                            uri=f"file://{relative_path}",
                            name=str(relative_path),
                            mimeType="text/plain",
                            description=f"File: {relative_path}",
                        )
                    )
            return resources

        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """リソース読み込み"""
            if not uri.startswith("file://"):
                raise ValueError(f"Invalid URI: {uri}")

            path = uri.replace("file://", "")
            file_path = self.base_path / path

            if not file_path.exists():
                raise ValueError(f"Resource not found: {uri}")

            return file_path.read_text()

    async def run(self):
        """サーバー起動"""
        async with stdio_server() as (read_stream, write_stream):
            logger.info("File Manager MCP server running")
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


async def main():
    server = FileManagerServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
```

### 3. プロンプト機能付きサーバー

**入力**:
```
MCPサーバーにプロンプト機能を追加：
名前: code-review-assistant
プロンプト:
- セキュリティレビュー
- パフォーマンスレビュー
- コード品質レビュー
```

**プロンプト実装例（TypeScript）**:
```typescript
import { ListPromptsRequestSchema, GetPromptRequestSchema } from "@modelcontextprotocol/sdk/types.js";

// プロンプト一覧
server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: "security-review",
        description: "Comprehensive security code review",
        arguments: [
          {
            name: "code",
            description: "Code to review",
            required: true,
          },
          {
            name: "language",
            description: "Programming language",
            required: false,
          },
        ],
      },
      {
        name: "performance-review",
        description: "Performance analysis and optimization suggestions",
        arguments: [
          {
            name: "code",
            description: "Code to analyze",
            required: true,
          },
        ],
      },
    ],
  };
});

// プロンプト取得
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "security-review") {
    const code = args?.code as string;
    const language = (args?.language as string) || "unknown";

    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Please perform a comprehensive security review of the following ${language} code:

\`\`\`${language}
${code}
\`\`\`

Check for:
1. SQL Injection vulnerabilities
2. XSS (Cross-Site Scripting) risks
3. Authentication and authorization issues
4. Data validation and sanitization
5. Encryption and hashing
6. Hardcoded secrets
7. CSRF protection
8. Input validation

Provide specific recommendations with code examples.`,
          },
        },
      ],
    };
  }

  if (name === "performance-review") {
    const code = args?.code as string;

    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Analyze the following code for performance issues:

\`\`\`
${code}
\`\`\`

Focus on:
1. Time complexity (Big O)
2. Unnecessary loops or nesting
3. Database query optimization (N+1 problems)
4. Memory leaks
5. Inefficient data structures
6. Caching opportunities
7. Async/await usage

Provide optimization suggestions with improved code examples.`,
          },
        },
      ],
    };
  }

  throw new Error(`Unknown prompt: ${name}`);
});
```

## ベストプラクティス

### 1. ロギング（CRITICAL）

**TypeScript**:
```typescript
// ❌ 絶対にNG: stdout はプロトコル通信用
console.log("Server started");

// ✅ 正しい: stderr にログ出力
console.error("Server started");

// ✅ ロガーライブラリ使用（推奨）
import pino from "pino";
const logger = pino({ level: "info" });
logger.info("Server started");
```

**Python**:
```python
# ✅ 標準loggingライブラリ（デフォルトで stderr）
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Server started")
```

### 2. スキーマ検証

**TypeScript (Zod)**:
```typescript
import { z } from "zod";

const UserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

// 検証
const validated = UserSchema.parse(args);
```

**Python (Pydantic)**:
```python
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int | None = Field(None, gt=0)

# 検証
user = User(**args)
```

### 3. エラーハンドリング

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const { name, arguments: args } = request.params;

    // 入力検証
    if (!name) {
      throw new Error("Tool name is required");
    }

    // ツール実行
    const result = await executeTool(name, args);

    return {
      content: [{ type: "text", text: JSON.stringify(result) }],
    };
  } catch (error) {
    // エラーログ（stderr）
    console.error("Tool execution failed:", error);

    // ユーザーフレンドリーなエラーメッセージ
    if (error instanceof z.ZodError) {
      throw new Error(`Validation failed: ${error.message}`);
    }

    throw error;
  }
});
```

### 4. ツール登録タイミング

```typescript
// ✅ 正しい: トランスポート接続前にツール登録
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: [...] };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // ツール実行
});

// この後で接続
await server.connect(transport);
```

### 5. 非同期処理

**Python**:
```python
# ✅ async/await を適切に使用
async def call_tool(name: str, arguments: dict):
    if name == "fetch_data":
        # 非同期API呼び出し
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return [TextContent(type="text", text=str(data))]
```

## Claude Desktop 統合

### 設定ファイル生成

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "calculator": {
      "command": "node",
      "args": ["/path/to/calculator-mcp/dist/index.js"]
    },
    "file-manager": {
      "command": "python",
      "args": ["-m", "file_manager.server"],
      "env": {
        "BASE_PATH": "/Users/username/documents"
      }
    }
  }
}
```

### 起動と確認

1. Claude Desktop を再起動
2. チャットで `/mcp` と入力してサーバー確認
3. ツールを使用: "Use the calculator to add 5 and 3"

## デバッグ方法

### TypeScript

```typescript
// 詳細ログ有効化
const logger = pino({ level: "debug" });

// リクエスト/レスポンスのログ
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  logger.debug({ request }, "Received tool call");

  const result = await executeTool(request.params.name, request.params.arguments);

  logger.debug({ result }, "Tool call completed");
  return result;
});
```

### Python

```python
# デバッグレベルのログ
logging.basicConfig(level=logging.DEBUG)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.debug(f"Tool call: {name} with args {arguments}")
    result = await execute_tool(name, arguments)
    logger.debug(f"Tool result: {result}")
    return result
```

### トラブルシューティング

**問題**: サーバーが起動しない
- **原因**: stdout にログ出力している
- **解決**: console.error または stderr 使用

**問題**: ツールが見つからない
- **原因**: ツール名の不一致
- **解決**: ListToolsRequestSchema で返す名前と CallToolRequestSchema で使う名前を一致させる

**問題**: スキーマ検証エラー
- **原因**: 引数の型が合わない
- **解決**: Zod/Pydantic スキーマを確認

## テンプレート

### Minimal TypeScript Server

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({ name: "my-server", version: "1.0.0" }, { capabilities: { tools: {} } });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{ name: "hello", description: "Say hello", inputSchema: { type: "object", properties: {} } }],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "hello") {
    return { content: [{ type: "text", text: "Hello, World!" }] };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Server running");
```

### Minimal Python Server

```python
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("my-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name="hello", description="Say hello", inputSchema={"type": "object", "properties": {}})]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "hello":
        return [TextContent(type="text", text="Hello, World!")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

asyncio.run(main())
```

## 高度な機能

### 認証

```typescript
// API Key 認証
const API_KEY = process.env.API_KEY;

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // ヘッダーから認証情報取得（実装依存）
  const authHeader = request.params._meta?.auth;

  if (authHeader !== API_KEY) {
    throw new Error("Unauthorized");
  }

  // ツール実行
});
```

### レート制限

```typescript
import rateLimit from "express-rate-limit";

const limiter = new Map<string, { count: number; resetAt: number }>();

async function checkRateLimit(clientId: string): Promise<void> {
  const now = Date.now();
  const limit = limiter.get(clientId);

  if (!limit || now > limit.resetAt) {
    limiter.set(clientId, { count: 1, resetAt: now + 60000 });
    return;
  }

  if (limit.count >= 100) {
    throw new Error("Rate limit exceeded");
  }

  limit.count++;
}
```

### キャッシング

```python
from functools import lru_cache
import asyncio

# シンプルなメモリキャッシュ
@lru_cache(maxsize=100)
def get_cached_data(key: str) -> str:
    # 重い処理
    return expensive_operation(key)

# 非同期キャッシュ
cache = {}

async def get_cached_async(key: str) -> str:
    if key in cache:
        return cache[key]

    result = await expensive_async_operation(key)
    cache[key] = result
    return result
```

## 実装例

### 例1: GitHub 統合

```
GitHub統合MCPサーバーを作成：
- リポジトリ情報取得ツール
- PR作成ツール
- Issue検索ツール
- コミット履歴リソース
- PR レビュープロンプト
```

### 例2: データベース管理

```
PostgreSQL MCP サーバー：
- クエリ実行ツール
- スキーマ情報リソース
- クエリ最適化プロンプト
認証: 接続文字列
エラーハンドリング: トランザクションロールバック
```

### 例3: ファイルシステム

```
ファイル操作MCPサーバー：
- ファイル読み書きツール
- ディレクトリ一覧リソース
- ファイル検索ツール
セキュリティ: パストラバーサル対策
```

## ドキュメント生成

自動生成されるドキュメント：

### README.md
- サーバー概要
- インストール手順
- 使用方法
- ツール一覧
- 設定例

### API.md
- 全ツールのAPI仕様
- 入力スキーマ
- 出力例
- エラーコード

### CONTRIBUTING.md
- 開発環境構築
- テスト実行方法
- コントリビューションガイドライン

## 制限事項

- **ネットワーク**: stdio ベースは同一マシン内のみ
- **セキュリティ**: 入力検証は必須（ユーザー入力を信頼しない）
- **パフォーマンス**: 長時間実行タスクはタイムアウト考慮
- **バージョン**: 最新SDK機能はTypeScript/Pythonが先行

## 参考リソース

- **公式ドキュメント**: https://modelcontextprotocol.io/
- **GitHub**: https://github.com/modelcontextprotocol
- **サーバー例**: https://github.com/modelcontextprotocol/servers
- **TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk

## バージョン情報

- スキルバージョン: 1.0.0
- 対応MCP仕様: 2025-01-01
- 最終更新: 2025-11-22

---

**使用例**:

```
TypeScript MCPサーバーを作成してください：

名前: slack-integration
機能:
- メッセージ送信ツール
- チャンネル一覧リソース
- 定型メッセージプロンプト

設定:
- Slack API Token 使用
- エラーハンドリング完備
- レート制限対応
- Claude Desktop設定含む
```

このプロンプトで、本番環境対応のMCPサーバーが生成されます！
