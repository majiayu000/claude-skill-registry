---
name: trpc-router-creating
description: BoxLogのtRPC v11ルーターを作成。サービス層分離、Zodバリデーション、エラーハンドリングを適用。
---

# tRPC Router Creating Skill

BoxLogプロジェクトのtRPC v11ルーターを規約に沿って作成するスキルです。

## このスキルを使用するタイミング

以下のキーワードが含まれる場合に自動的に起動：

- 「APIを作成」「エンドポイント追加」
- 「tRPCルーター」「router作成」
- 「バックエンド実装」
- 「CRUD API」

## ルーター構造

```
src/server/api/routers/{entity}/
├── index.ts        # ルーターのマージ・エクスポート
├── crud.ts         # 基本CRUD操作
├── bulk.ts         # バルク操作（optional）
├── statistics.ts   # 統計（optional）
└── __tests__/
    └── crud.test.ts
```

## 作成手順

### 1. スキーマ定義（Zod）

```typescript
// src/schemas/{entity}.ts
import { z } from 'zod'

export const {entity}IdSchema = z.object({
  id: z.string().uuid(),
})

export const create{Entity}Schema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  // other fields
})

export const update{Entity}Schema = create{Entity}Schema.partial()

export const {entity}FilterSchema = z.object({
  search: z.string().optional(),
  limit: z.number().min(1).max(100).default(50),
  offset: z.number().min(0).default(0),
})
```

### 2. サービス層（ビジネスロジック）

```typescript
// src/server/services/{entity}/index.ts
import { SupabaseClient } from '@supabase/supabase-js'

export class {Entity}ServiceError extends Error {
  constructor(
    public code: string,
    message: string
  ) {
    super(message)
    this.name = '{Entity}ServiceError'
  }
}

export function create{Entity}Service(supabase: SupabaseClient) {
  return {
    async list(params: { userId: string; limit?: number; offset?: number }) {
      const { data, error } = await supabase
        .from('{entities}')
        .select('*')
        .eq('user_id', params.userId)
        .range(params.offset ?? 0, (params.offset ?? 0) + (params.limit ?? 50) - 1)

      if (error) {
        throw new {Entity}ServiceError('FETCH_FAILED', error.message)
      }
      return data
    },

    async getById(params: { userId: string; {entity}Id: string }) {
      const { data, error } = await supabase
        .from('{entities}')
        .select('*')
        .eq('id', params.{entity}Id)
        .eq('user_id', params.userId)
        .single()

      if (error) {
        throw new {Entity}ServiceError('NOT_FOUND', error.message)
      }
      return data
    },

    async create(params: { userId: string; input: Create{Entity}Input }) {
      const { data, error } = await supabase
        .from('{entities}')
        .insert({ ...params.input, user_id: params.userId })
        .select()
        .single()

      if (error) {
        throw new {Entity}ServiceError('CREATE_FAILED', error.message)
      }
      return data
    },

    async update(params: { userId: string; {entity}Id: string; input: Update{Entity}Input }) {
      const { data, error } = await supabase
        .from('{entities}')
        .update(params.input)
        .eq('id', params.{entity}Id)
        .eq('user_id', params.userId)
        .select()
        .single()

      if (error) {
        throw new {Entity}ServiceError('UPDATE_FAILED', error.message)
      }
      return data
    },

    async delete(params: { userId: string; {entity}Id: string }) {
      const { error } = await supabase
        .from('{entities}')
        .delete()
        .eq('id', params.{entity}Id)
        .eq('user_id', params.userId)

      if (error) {
        throw new {Entity}ServiceError('DELETE_FAILED', error.message)
      }
      return { success: true }
    },
  }
}
```

### 3. CRUDルーター

```typescript
// src/server/api/routers/{entity}/crud.ts
import { z } from 'zod'

import { create{Entity}Schema, {entity}IdSchema, update{Entity}Schema } from '@/schemas/{entity}'
import { createTRPCRouter, protectedProcedure } from '@/server/api/trpc'
import { handleServiceError } from '@/server/services/errors'
import { create{Entity}Service } from '@/server/services/{entity}'

// handleServiceErrorは共通モジュールを使用
// 新しいエラーコードが必要な場合は src/server/services/errors.ts の ERROR_CODE_MAP に追加

export const {entity}CrudRouter = createTRPCRouter({
  list: protectedProcedure.query(async ({ ctx }) => {
    const service = create{Entity}Service(ctx.supabase)
    try {
      return await service.list({ userId: ctx.userId })
    } catch (error) {
      handleServiceError(error)
    }
  }),

  getById: protectedProcedure.input({entity}IdSchema).query(async ({ ctx, input }) => {
    const service = create{Entity}Service(ctx.supabase)
    try {
      return await service.getById({ userId: ctx.userId, {entity}Id: input.id })
    } catch (error) {
      handleServiceError(error)
    }
  }),

  create: protectedProcedure.input(create{Entity}Schema).mutation(async ({ ctx, input }) => {
    const service = create{Entity}Service(ctx.supabase)
    try {
      return await service.create({ userId: ctx.userId, input })
    } catch (error) {
      handleServiceError(error)
    }
  }),

  update: protectedProcedure
    .input(z.object({ id: z.string().uuid(), data: update{Entity}Schema }))
    .mutation(async ({ ctx, input }) => {
      const service = create{Entity}Service(ctx.supabase)
      try {
        return await service.update({
          userId: ctx.userId,
          {entity}Id: input.id,
          input: input.data,
        })
      } catch (error) {
        handleServiceError(error)
      }
    }),

  delete: protectedProcedure.input({entity}IdSchema).mutation(async ({ ctx, input }) => {
    const service = create{Entity}Service(ctx.supabase)
    try {
      return await service.delete({ userId: ctx.userId, {entity}Id: input.id })
    } catch (error) {
      handleServiceError(error)
    }
  }),
})
```

### 4. ルーターのマージ

```typescript
// src/server/api/routers/{entity}/index.ts
import { mergeRouters } from '@/server/api/trpc'
import { {entity}CrudRouter } from './crud'
// import { {entity}BulkRouter } from './bulk'  // optional

export const {entity}Router = mergeRouters(
  {entity}CrudRouter,
  // {entity}BulkRouter,
)
```

### 5. メインルーターに追加

```typescript
// src/server/api/root.ts
import { {entity}Router } from './routers/{entity}'

export const appRouter = createTRPCRouter({
  // existing routers...
  {entity}: {entity}Router,
})
```

## アーキテクチャ

```
┌─────────────────────┐
│   tRPC Router       │  ← 入力バリデーション + エラーハンドリング
├─────────────────────┤
│   Service Layer     │  ← ビジネスロジック
├─────────────────────┤
│   Supabase Client   │  ← データアクセス
└─────────────────────┘
```

## チェックリスト

- [ ] Zodスキーマを `src/schemas/` に作成
- [ ] サービス層を `src/server/services/` に作成
- [ ] `protectedProcedure` を使用（認証必須）
- [ ] エラーハンドリングで `TRPCError` を使用
- [ ] `user_id` でフィルタリング（マルチテナント）
- [ ] テストファイル作成
- [ ] メインルーターに登録

## 既存ルーター参考

```
src/server/api/routers/
├── plans/           # 最も完成度が高い例
│   ├── index.ts
│   ├── crud.ts
│   ├── bulk.ts
│   ├── statistics.ts
│   └── __tests__/
├── profile.ts       # シンプルな例
└── notifications.ts
```
