---
name: inspect-nextjs-runtime
description: MCPを使用してNext.jsランタイムを検査し、エラー診断、ログ、メタデータ、Server Actionsを確認します。エラーのデバッグ、ルートのチェック、コンポーネントの検査、プロジェクト構造の理解に使用します。
---

# Next.jsランタイムの検査

2つの補完的なMCPサーバーでNext.jsランタイム情報にアクセス。

## クイックスタート

```typescript
// 現在のエラーを取得
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  toolName: "get_errors"
})

// 開発ログを取得
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  toolName: "get_logs"
})

// ページメタデータを取得
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  toolName: "get_page_metadata",
  args: { path: "/users" }
})
```

## 2つのMCPサーバー

### 1. 組み込みMCPサーバー（低レベル）

Next.js内部への直接アクセス。**Next.js 16+でデフォルト有効。**

**公式の5つのツール:**

#### `get_errors`
現在のビルドエラー、ランタイムエラー、型エラーを取得。

```typescript
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  toolName: "get_errors"
})
```

**使用する場合:**
- ビルド失敗のデバッグ
- ランタイムエラーの調査
- 型エラーのチェック
- ハイドレーションエラーの診断

---

#### `get_logs`
開発サーバーのログとコンソール出力にアクセス。

```typescript
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  toolName: "get_logs"
})
```

**使用する場合:**
- サーバーサイドのコンソール出力確認
- リクエストログのレビュー
- 開発サーバーの活動監視

---

#### `get_page_metadata`
ルート、コンポーネント、レンダリング情報を含む特定ページのメタデータを取得。

```typescript
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  toolName: "get_page_metadata",
  args: { path: "/users/[id]" }
})
```

**使用する場合:**
- ページ構造の理解
- ルートに対してどのlayout/pageがレンダリングされるか確認
- コンポーネント階層の検査
- レンダリング戦略の決定（静的/動的）

---

#### `get_project_metadata`
プロジェクト構造、設定、全体的なメタデータを取得。

```typescript
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  toolName: "get_project_metadata"
})
```

**使用する場合:**
- プロジェクトアーキテクチャの理解
- Next.js設定の確認
- ルート構造のレビュー
- ミドルウェア設定の分析

---

#### `get_server_action_by_id`
デバッグと検査のためにIDでServer Actionsを検索。

```typescript
mcp__next-devtools__nextjs_runtime({
  action: "call_tool",
  toolName: "get_server_action_by_id",
  args: { id: "abc123" }
})
```

**使用する場合:**
- Server Actionエラーのデバッグ
- Server Action実行のトレース
- Server Action実装の検査

---

### 2. next-devtools-mcp（高レベル）

開発ガイダンスとドキュメント。**別パッケージが必要。**

**機能:**
- ドキュメント検索（`nextjs_docs`）
- ランタイム調査の概要
- ベストプラクティスの推奨

```typescript
// ドキュメント検索
mcp__next-devtools__nextjs_docs({
  query: "async params searchParams",
  category: "api-reference"
})

// サーバー検出
mcp__next-devtools__nextjs_runtime({
  action: "discover_servers"
})

// 利用可能なツールをリスト
mcp__next-devtools__nextjs_runtime({
  action: "list_tools"
})
```

## 一般的なユースケース

公式ドキュメントに基づく

### 1. エラー診断
ハイドレーションエラー、ビルド失敗、ランタイム問題の特定と修正。

```typescript
// すべての現在のエラーを取得
const errors = await call_tool("get_errors")
// 分析と修正を提供
```

### 2. コンテキストを考慮した提案
既存構造に基づいて新機能の最適な場所を推奨。

```typescript
// プロジェクトメタデータを取得
const metadata = await call_tool("get_project_metadata")
// 新機能の最適な場所を提案
```

### 3. ライブ状態クエリ
開発中の現在の設定、ルート、ミドルウェアを確認。

```typescript
// 特定ルートのページメタデータを取得
const pageInfo = await call_tool("get_page_metadata", { path: "/dashboard" })
```

### 4. アプリアーキテクチャの理解
どのページとレイアウトが任意の時点でレンダリングされるかを判断。

```typescript
// ルート構造を検査
const metadata = await call_tool("get_project_metadata")
// page/layout階層を理解
```

### 5. ガイド付きアップグレード
ステップバイステップの指示でバージョン移行を支援。

```typescript
// アップグレードドキュメントを検索
mcp__next-devtools__nextjs_docs({
  query: "migrate to Next.js 16",
  category: "guides"
})
```

## どちらを使うか

### 組み込みMCPサーバー
**特定のランタイムクエリ**に使用
- 現在のエラー取得
- ログチェック
- ページ/プロジェクトメタデータの検査
- Server Actionsのデバッグ

### next-devtools-mcp
**ドキュメントとガイダンス**に使用
- Next.jsドキュメント検索
- パターンとベストプラクティスの学習
- 高レベルランタイム概要の取得

### 両方を併用（推奨）
包括的な開発サポートのために組み合わせる
1. 学習とドキュメントにはnext-devtools-mcpを使用
2. 特定のランタイム検査には組み込みMCPを使用

## 要件

- **Next.js 16+**（組み込みMCPがデフォルトで有効）
- **開発サーバーが起動中**（`npm run dev`）
- **next-devtools-mcpパッケージ**（オプション、高レベル機能用）

## ベストプラクティス

1. **最初に開発サーバーを起動**: MCPには実行中のサーバーが必要
2. **両方のMCPサーバーを使用**: 補完的な機能
3. **定期的にエラーをチェック**: プロアクティブなデバッグのために `get_errors`
4. **実装前に検査**: 最初にプロジェクト構造を確認
5. **ドキュメントと組み合わせる**: ドキュメント検索 + ランタイム検査

## 重要な注意事項

- 組み込みMCPはNext.js 16+で**デフォルト有効**
- MCPツールは開発中の**ライブ状態**を提供
- 両方のMCPサーバーは**補完的に**動作（低レベル + 高レベル）
- **開発モード**が必要（本番環境にはMCPサーバーなし）
