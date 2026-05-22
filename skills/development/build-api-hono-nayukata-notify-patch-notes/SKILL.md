---
name: build-api-hono
description: Hono + Zod で型安全な CRUD API を構築し、クライアント通信とテストを統合します。API実装、リクエスト検証、RPC通信、ローカルテストが必要な場合に使用します。
---

# Hono API 構築スキル

HonoとZodによる型安全なAPI開発の全ワークフローを提供します。

## いつ使うか

このスキルは以下の場合に使用してください：

- 新しいCRUD APIエンドポイントの作成
- リクエストバリデーションの追加
- 型安全なクライアント-サーバー通信の構築
- APIのテストと最適化
- Honoドキュメントの検索

## ワークフロー

### 1. API エンドポイントの作成

```typescript
// apps/server/src/routes/admin/users.ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { CreateUserSchema } from '@repo/schemas/request/admin/users'
import { db } from '@repo/database'

const app = new Hono()

// POST /users - 作成
app.post('/', zValidator('json', CreateUserSchema), async (c) => {
  const data = c.req.valid('json')  // 型安全
  const user = await db.user.create({ data })
  return c.json({ user }, 201)
})

// GET /users/:id - 取得
app.get('/:id', async (c) => {
  const id = c.req.param('id')
  const user = await db.user.findUnique({ where: { id } })
  if (!user) return c.json({ error: 'Not found' }, 404)
  return c.json({ user })
})

// RPCのために型をエクスポート
export type AppType = typeof app
```

詳細パターン（エラーハンドリング、ページネーション、複雑なクエリ）は [crud-operations.md](references/crud-operations.md) を参照してください。

### 2. バリデーションの追加

```typescript
// packages/schemas/src/request/admin/users.ts
import { z } from 'zod'
import type { Prisma } from '@repo/database'

export const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
}) satisfies z.ZodType<Prisma.UserCreateInput>  // Prisma型と同期

export type CreateUserInput = z.infer<typeof CreateUserSchema>
```

詳細パターン（カスタムバリデーション、複雑な変換、エラーメッセージ）は [validation.md](references/validation.md) を参照してください。

### 3. RPC クライアントのセットアップ

```typescript
// apps/admin/src/utils/hc.ts
import { hc } from 'hono/client'
import type { AppType } from '@repo/server'

export const client = hc<AppType>('/api')

// apps/admin/src/swr/users/use-user.ts
export function useUser(id: string) {
  return useSWR(['user', id], async () => {
    return await parseResponse(client.admin.users[':id'].$get({ param: { id } })) // 完全に型付けされている
  })
}
```

詳細パターン（型推論、エラーハンドリング、複数API統合）は [rpc-client.md](references/rpc-client.md) を参照してください。

### 4. Hono CLI でテスト・最適化

```bash
# ドキュメントを検索
hono search "middleware"

# ドキュメントを表示
hono docs /docs/guides/middleware

# サーバー起動なしでテスト
hono request -P /api/users apps/server/src/index.ts
hono request -P /api/users -X POST -d '{"name":"Alice"}' apps/server/src/index.ts

# 本番デプロイ前に最適化（ファイルサイズ38%削減、初期化16.5倍高速化）
hono optimize apps/server/src/index.ts -o dist/server.js
```

詳細ワークフロー（CLIコマンド、最適化、自動化パターン）は [hono-cli.md](references/hono-cli.md) を参照してください。

## 重要ルール

### API 作成

- `c.notFound()` は使用しない（RPC型を壊す）
- 常にステータスコードを明示的に指定
- クライアント用に `AppType` をエクスポート
- response スキーマは visibility + deriveDto で構築（`.pick()` は使わない）

### バリデーション

- スキーマ名は **PascalCase**（`CreateUserSchema`）
- スキーマは `packages/schemas/` に定義
- バリデート済みデータ取得には `c.req.valid()` を使用
- クエリパラメータには `z.coerce` を使用（文字列→数値の変換）

### RPC クライアント

- サーバーから `AppType` をエクスポート
- クライアントで型をインポート（値ではない: `import type`）
- 型安全性のために `hc<AppType>()` を使用
- レスポンス型には `InferResponseType` を使用

### Hono CLI

- **開発サーバー不要**: `hono request` は内部で `app.request()` を使用
- 環境の競合とサーバーの乱立を防ぐ
- テストには常に `hono request` を優先
- `hono optimize` は本番デプロイ前に実行（開発中は不要）

## 詳細パターン

詳細な実装パターンについては references を参照してください：

- [crud-operations.md](references/crud-operations.md) - CRUD操作、エラーハンドリング、ページネーション
- [validation.md](references/validation.md) - カスタムバリデーション、複雑な変換、エラーメッセージ
- [rpc-client.md](references/rpc-client.md) - 型推論、エラーハンドリング、複数API
- [hono-cli.md](references/hono-cli.md) - CLIワークフロー、最適化、自動化
