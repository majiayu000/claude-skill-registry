---
name: mcp-builder
description: |
  Guide for creating MCP (Model Context Protocol) servers that enable LLMs to interact with
  external services through well-designed tools.
  Triggers: 「MCPサーバーを作成」「外部API連携」「ツール統合」「MCP開発」
  Use when: Building MCP servers to integrate external APIs or services.
  Recommended stack: TypeScript + MCP SDK
---

# MCP Server Development Guide

MCPサーバーの設計・実装ガイド。LLMが外部サービスとやり取りするためのツールを提供する。

## High-Level Workflow

### Phase 1: Deep Research and Planning

1. **MCP仕様の確認**: `https://modelcontextprotocol.io/sitemap.xml` から関連ページを確認
20. 2. **SDK確認**: TypeScript SDK (`https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v0.6.0/README.md`) <!-- Pinned to v0.6.0 -->
21. 3. **API理解**: 対象サービスのAPIドキュメントを調査
22. 4. **ツール設計**: 実装するエンドポイントをリストアップ

### Phase 2: Implementation

#### プロジェクト構造（TypeScript推奨）

```text
mcp-server-xxx/
├── src/
│   ├── index.ts        # サーバーエントリーポイント
│   ├── tools/          # ツール定義
│   ├── types/          # 型定義
│   └── utils/          # ユーティリティ
├── package.json
└── tsconfig.json
```

#### ツール実装のポイント

- **Input Schema**: Zodでバリデーション、制約と説明を含める
- **Output Schema**: `outputSchema` で構造化データを定義
- **Description**: 機能の簡潔なサマリー + パラメータ説明
- **Error Handling**: アクション可能なエラーメッセージ（次のステップを提案）

#### Annotations

```typescript
{
  annotations: {
    title: 'List all users',           // 人間が読めるツールの表示名
    readOnlyHint: true,                // データを変更しない（読み取り専用）
    destructiveHint: false,            // リソースを破壊しない
    idempotentHint: true,              // 同じ入力で同じ結果を返す
    openWorldHint: true,               // 外部サービスとやり取りする
  },
}
```

### Phase 3: Review and Test

1. `npm run build` でコンパイル確認
2. MCP Inspectorでテスト: `npx @modelcontextprotocol/inspector@0.19.0`
3. コード品質チェック: DRY、一貫したエラーハンドリング、型カバレッジ

### Phase 4: VS Code統合

`.vscode/mcp.json` に設定を追加:

```json
{
  "servers": {
    "your-server": {
      "command": "npx",
      "args": ["-y", "your-mcp-server-package"]
    }
  }
}
```

## Design Principles

- **Tool Naming**: 一貫したプレフィックス（例: `github_create_issue`）
- **Context Management**: 簡潔なツール説明、フィルタ/ページネーション対応
- **Error Messages**: エージェントを解決に導く具体的な提案
- **API Coverage**: ワークフローツールよりも包括的なAPI網羅を優先

## Resources

- [Best Practices](resources/mcp_best_practices.md): セキュリティ、エラーハンドリング、開発のベストプラクティス
- [Node.js Implementation](resources/node_mcp_server.md): TypeScript SDKを使用した実装ガイド
- [Python Implementation](resources/python_mcp_server.md): Python SDKを使用した実装ガイド
- [Evaluation Guide](resources/evaluation.md): サーバーのテストと評価方法
