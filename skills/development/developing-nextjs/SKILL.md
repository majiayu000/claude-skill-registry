---
name: developing-nextjs
description: Guides Next.js 16 / React 19 development. Use when package.json contains 'next' or next.config.* is detected. Supports App Router, Server Components, Cache Components, strict TypeScript, Tailwind CSS v4, Prisma ORM, and Vitest.
---

# Next.js 16 / React 19 Modern Web Development Skill

## 概要

このスキルは、Next.js 16.0.0 + React 19.2.0を使用した最新のWebアプリケーション開発のベストプラクティスを提供します。

## 使用タイミング

以下のような場面でこのスキルを参照してください：

- **新規プロジェクト作成**: Next.js 16でプロジェクトを開始する前に全体像を把握
- **実装前の確認**: 特定機能（Server Components、Actions、Cache等）の実装方法を確認
- **設定ファイル作成**: mise.toml、tsconfig.json、eslint.config.mjs等の設定例が必要なとき
- **トラブルシューティング**: ビルドエラー、型エラー、Docker問題の解決方法を確認
- **コード品質向上**: TypeScript厳格設定、ESLint、テスト戦略を学ぶ

## 対象技術スタック

- **Next.js**: 16.0.0（App Router、Server Components、Cache Components）
- **React**: 19.2.0（Actions、useActionState、ref as prop等の新機能）
- **TypeScript**: 5.9.3（strict mode、厳格な型チェック）
- **Tailwind CSS**: 4.1.15 + shadcn/ui 3.4.2
- **Prisma ORM**: 6.18.0（PostgreSQL）
- **Vitest + MSW**: テスト環境
- **Docker**: マルチステージビルド、GCPデプロイ対応
- **mise**: ツールバージョン管理

## ドキュメント構成（Progressive Disclosure）

このスキルは、必要な情報に素早くアクセスできるよう、以下のファイルに分割されています：

### 🏗️ プロジェクト構成とセットアップ
- **[PROJECT-STRUCTURE.md](./PROJECT-STRUCTURE.md)**: プロジェクト全体のフォルダ構成、命名規則、推奨構造
- **[TOOLING.md](./TOOLING.md)**: mise.toml、pnpm、ESLint、TypeScript、Prettier等の開発ツール設定

### ⚛️ フレームワーク固有ガイド
- **[NEXTJS-GUIDE.md](./NEXTJS-GUIDE.md)**: App Router、Server Components、Cache Components、動的ルーティング等
- **[REACT-GUIDE.md](./REACT-GUIDE.md)**: React 19新機能（Actions、useActionState、ref as prop等）

### 🎨 UI・スタイリング
- **[STYLING.md](./STYLING.md)**: Tailwind CSS v4設定、shadcn/ui使用方法、カスタムコンポーネント作成

### 🗄️ データ管理とテスト
- **[DATABASE.md](./DATABASE.md)**: Prisma ORM設定、マイグレーション、型安全なクエリ
- **[TESTING.md](./TESTING.md)**: Vitest設定、MSWモック、テスト戦略、カバレッジ

### 🐳 デプロイと運用
- **[DOCKER.md](./DOCKER.md)**: マルチステージビルド、Next.js standalone出力、GCP Cloud Run対応

### 📖 実装例
- **[EXAMPLES.md](./EXAMPLES.md)**: page.tsx、layout.tsx、Server Actions、API routes等の実装サンプル

## 他のスキルとの連携

このスキルは、以下の既存スキルと組み合わせて使用してください：

### 必須スキル（実装時に必ず参照）
- **`applying-solid-principles`**: SOLID原則、クリーンコード、単一責任原則等
- **`enforcing-type-safety`**: any/Any型禁止、型ガード、厳格な型チェック
- **`testing`**: TDD、AAA パターン、テストカバレッジ100%目標
- **`securing-code`**: セキュアコーディング、CodeGuard実行（実装完了後必須）
- **`writing-technical-docs`**: 7つのC原則（Clear, Concise, Correct, Coherent, Concrete, Complete, Courteous）

### 推奨MCP（効率的開発）
- **`using-serena`**: コード編集・分析（最優先）
- **`using-next-devtools`**: Next.js専用ツール（診断、アップグレード、Cache Components最適化）
- **`using-shadcn`**: UIコンポーネント管理（shadcn/ui検索・追加）
- **`mcp-search`**: 最新仕様確認（context7、kagi等）

## 学習パス

### 初心者向け
1. **[PROJECT-STRUCTURE.md](./PROJECT-STRUCTURE.md)** - プロジェクト全体像を把握
2. **[NEXTJS-GUIDE.md](./NEXTJS-GUIDE.md)** - Next.js基本概念（App Router、Server Components）
3. **[EXAMPLES.md](./EXAMPLES.md)** - 実装例で学ぶ

### 中級者向け
1. **[REACT-GUIDE.md](./REACT-GUIDE.md)** - React 19新機能を活用
2. **[DATABASE.md](./DATABASE.md)** - Prisma ORMでデータ層を構築
3. **[TESTING.md](./TESTING.md)** - テスト戦略を学ぶ

### 上級者向け
1. **[TOOLING.md](./TOOLING.md)** - 開発ツールの最適化
2. **[DOCKER.md](./DOCKER.md)** - 本番環境デプロイ
3. `applying-solid-principles`、`enforcing-type-safety`、`securing-code` - コード品質向上

## クイックスタート

### 新規プロジェクト作成
```bash
# 1. Next.js 16プロジェクト作成
npx create-next-app@latest my-app

# 2. mise初期化（推奨）
mise use node@24.5.0 pnpm@10.14.0 pre-commit@latest

# 3. shadcn/ui初期化
pnpm dlx shadcn@latest init

# 4. Prisma初期化
pnpm add -D prisma
pnpm dlx prisma init

# 5. Vitest初期化
pnpm add -D vitest @vitejs/plugin-react vite-tsconfig-paths jsdom
```

詳細な設定は各ドキュメントを参照してください。

## 重要な原則

### 1. 型安全性（必須）
- **any/Any型禁止**: TypeScript/Python共通（`enforcing-type-safety`スキル参照）
- **厳格な型チェック**: tsconfig.jsonで`strict: true`を必ず有効化
- **型推論の活用**: 可能な限り明示的な型注釈より型推論を使用

### 2. Server-First設計
- **デフォルトはServer Components**: クライアント機能が必要な場合のみ`"use client"`
- **データフェッチはサーバーサイド**: `async/await`で直接データベースアクセス
- **Server Actions活用**: フォーム送信、データ更新はServer Actionsで処理

### 3. コード品質
- **SOLID原則遵守**: `applying-solid-principles`スキル参照
- **テストファースト**: `testing`スキル参照
- **セキュアコーディング**: `securing-code`スキル参照（実装完了後にCodeGuard必須実行）

### 4. パフォーマンス最適化
- **キャッシング戦略**: Cache Components、Partial Prerendering活用
- **動的インポート**: 大きなコンポーネントは`dynamic()`で遅延ロード
- **画像最適化**: `next/image`コンポーネント使用

## サポートとフィードバック

このスキルは、実際のプロダクションプロジェクト（信州大学教育プラットフォーム）から抽出されたベストプラクティスに基づいています。

不明点や改善提案があれば、関連ドキュメントを参照するか、最新の公式ドキュメントを確認してください：
- **Next.js公式**: https://nextjs.org/docs
- **React公式**: https://react.dev
- **Tailwind CSS v4**: https://tailwindcss.com
- **shadcn/ui**: https://ui.shadcn.com

---

**対象バージョン**: Next.js 16.x / React 19.x（詳細なバージョンは上記「対象技術スタック」を参照）
