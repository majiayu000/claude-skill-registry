---
name: manage-swr-data
description: useSWR/useSWRMutationでサーバーデータを管理します。データ取得、変更、SWRキー管理を含む、カスタムフックパターンを実装します。
---

# SWRデータ管理スキル

**重要**: useSWR/useSWRMutation/hcをコンポーネント内で直接使用せず、必ずカスタムフック経由で使用します。

## いつ使うか

このスキルは以下の場合に使用してください：

- サーバーからデータを取得する
- サーバーのデータを作成・更新・削除する
- データ取得・変更のロジックをコンポーネントから分離したい
- キャッシュ管理を統一したい

**注意**: クライアント内で完結する UI 状態（サイドバー、テーマ、URL 同期）には manage-client-state スキルを使用してください。

## クイックスタート

### 1. SWRキー定義

```typescript
// apps/admin/src/swr/users/user-swr-keys.ts
import type { SearchUsersParams } from '@/features/users/lib/search-params'

export const userSwrKeys = {
  list: (params: SearchUsersParams) => ['admin', 'users', params] as const,
  detail: (id: string) => ['admin', 'users', id] as const,
} as const
```

### 2. データ取得フック

```typescript
// apps/admin/src/swr/users/use-user.ts
import useSWR from 'swr'
import { parseResponse } from 'hono/client'
import { hc } from '@/utils/hc'
import { userSwrKeys } from './user-swr-keys'

export function useUser(id: string) {
  return useSWR(userSwrKeys.detail(id), async () => {
    const data = await parseResponse(
      hc.admin.users[':id'].$get({ param: { id } })
    )
    return data.user
  })
}
```

### 3. データ変更フック

```typescript
// apps/admin/src/swr/users/use-mutate-user.ts
import { useRouter } from 'next/navigation'
import type { CreateUserBody } from '@repo/schemas/request/admin/users.dto'
import { parseResponse } from 'hono/client'
import { toast } from 'sonner'
import useSWRMutation from 'swr/mutation'
import { hc } from '@/utils/hc'

export function useCreateUser() {
  const router = useRouter()

  const { trigger, isMutating: isCreating } = useSWRMutation(
    ['/admin/users', 'create'],
    async (_key, { arg }: { arg: CreateUserBody }) => {
      return await parseResponse(hc.admin.users.$post({ json: arg }))
    },
    {
      onSuccess: () => {
        toast.success('ユーザーを作成しました')
        router.push('/users')
      },
      onError: (e) => {
        toast.error(e instanceof Error ? e.message : 'ユーザーの作成に失敗しました')
      },
    }
  )

  return { createUser: trigger, isCreating }
}
```

## 重要ルール

### データ取得

- **カスタムフック経由**: `useSWR/hc` を直接使用しない
- **配置**: `apps/admin/src/swr/[entity]/use-[entity].ts`（単一）、`use-[entities].ts`（一覧）
- **SWRキー**: `[entity]-swr-keys.ts` で一元管理
- **parseResponse**: Hono RPCの型安全なエラーハンドリング

### データ変更

- **配置**: `apps/admin/src/swr/[entity]/use-mutate-[entity].ts`（同一ファイル内で複数export function）
- **フックの使用場所**: カスタムボタンコンポーネント内、またはConfirmation Dialog内
- **状態管理**: `useState`不要、`isMutating`を直接使用
- **ナビゲーション**: `router.push()`のみ（`router.refresh()`は不要）
- **キャッシュ無効化**: `mutate()`は使用しない（Background Revalidationに任せる）

### Mutation パターン

2つのパターンがあり、エンティティの特性に応じて使い分けます：

**パターンA（一般的）**: 詳細ページ（`/[entity]/[id]`）がある
- Mutation key: `entityKeys.detail(id)`
- Hook定義: `useUpdateEntity(id: string)` - 初期化時にidを受け取る

**パターンB（例外）**: 一覧で直接CRUD操作
- Mutation key: `entityKeys.list()`
- Hook定義: `useUpdateEntity()` - 実行時にidを受け取る

詳細は [mutation-patterns.md](references/mutation-patterns.md) を参照してください。

## ディレクトリ構造

```
apps/admin/src/swr/
└── [entity]/
    ├── [entity]-swr-keys.ts      # SWRキー定義
    ├── use-[entity].ts            # 単一データ取得
    ├── use-[entities].ts          # 一覧データ取得
    └── use-mutate-[entity].ts     # データ変更（複数フック定義）
```

## 詳細パターン

詳細な実装パターンについては references を参照してください：

- [fetch-data.md](references/fetch-data.md) - データ取得、エラーハンドリング、条件付きフェッチ
- [mutate-data.md](references/mutate-data.md) - データ変更、カスタムボタン、Confirmation Dialog
- [mutation-patterns.md](references/mutation-patterns.md) - パターンA/B、楽観的更新、キャッシュ戦略

## 関連スキル

- build-api-hono: Hono RPC統合、型安全なAPI呼び出し
- handle-forms-rhf-zod: フォームとの統合
- optimize-conditional-rendering-activity: データ取得状態の表示
- manage-client-state: UI状態管理との使い分け
