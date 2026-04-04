---
name: server-actions-and-routes
description: Next.js App Router における Server Actions と Route Handlers の使い分け、セキュリティ、および実装規約。
metadata:
  short-description: Server Actions & API Route 実装規約
---

# Server Actions & Routes 技術規約

Next.js のサーバーサイド通信において、一貫性・セキュリティ・開発効率を担保するためのルールです。

## 1. 使い分けの基準

基本的には **Server Actions を第一選択** とし、Route Handlers は特殊なケースに限定します。

| 通信方式           | 推奨される用途                                                                                   | 配置パス / 命名                   |
| :----------------- | :----------------------------------------------------------------------------------------------- | :-------------------------------- |
| **Server Actions** | **CRUD操作、フォーム送信、状態変更**。クライアントからの一般的なリクエストに優先使用。           | `src/server/actions/*.actions.ts` |
| **Route Handlers** | **SSE (ストリーミング)**、外部 Webhook、Cron ジョブ、特定の HTTP メソッド/ヘッダーが必要な場合。 | `app/api/**/route.ts`             |

## 2. Server Actions 実装ルール

- **ファイルレベルの宣言**: ファイルの先頭に必ず `'use server';` を記述します。関数レベルでの宣言は避け、`.actions.ts` ファイルに集約してください。
- **命名規則**: ファイル名は必ず `[feature].actions.ts` とします。
- **バリデーション**: 入力引数は `zod` スキーマを使用して `parse` または `safeParse` し、型安全を保証します。
- **クライアント用インポート**: 既存の一部実装（例: `chat.actions.ts`）では、名前衝突回避や明示性のために `export const MyActionSA = MyAction;` のようなエイリアスを定義している場合がありますが、新規実装において必須ではありません。

## 3. セキュリティ & 認証

- **認証の必須化**: 認証が必要な全てのアクション/ルートにおいて、処理の先頭で認証チェックを実施します。
  - **Server Actions**: 引数の `liffAccessToken` を `authMiddleware` に渡して検証。
  - **Route Handlers**: ヘッダー（Bearer）または Cookie からトークンを取得し、`ensureAuthenticated` 等の共通ロジックで検証。
- **特権操作の制限**: `viewMode` (閲覧モード) が有効な場合、データの「書き込み」や「管理者操作」を拒否し、`VIEW_MODE_ERROR_MESSAGE` を返却する必要があります。
- **エラーハンドリング**:
  - Server Actions では、ユーザーフレンドリーなエラーメッセージを含むオブジェクトを返却します。
  - Route Handlers では、適切な HTTP ステータスコード（401, 403, 429 等）と JSON データを返却します。
- **情報のカプセル化**: 内部 ID や不必要な機密情報（API キー等）をクライアントに返さないよう、専用のレスポンス型（例: `ChatResponse`）を定義して返却データをフィルタリングします。

## 4. 実装のアンチパターン

- [ ] `app/api/` 内の `route.ts` に `'use server';` を記述する（不要かつ誤解を招く）。
- [ ] クライアントから直接 `prisma` や `supabase` (Service Role) を呼び出すコードを Server Actions 外に書く。
- [ ] 認証チェックなしで `Service Role` による DB 操作を行う（重大なセキュリティリスク）。

## セルフレビュー項目

- [ ] その機能は Server Action で実装可能か？（SSE 等が必要ないなら Action を選択）
- [ ] 経路に応じた適切な共通認証ロジックで検証を行っているか？
- [ ] `viewMode` の際に破壊的操作が制限されているか？
- [ ] `zod` で入力値を検証しているか？
