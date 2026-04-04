---
name: manage-client-state
description: クライアント状態をグローバル/URL状態で型安全に管理します。サイドバーやフィルタはuseSWRImmutable、ページネーションはnuqs。
---

# クライアント状態管理スキル

クライアントサイドの状態管理の全ワークフローを提供します。

## いつ使うか

このスキルは以下の場合に使用してください：

- グローバルUI状態の管理（サイドバー、テーマ）
- URL状態の管理（ページネーション、フィルタ、検索、タブ）
- Contextプロバイダーを避けたい場合
- 状態をURLに永続化したい場合

## manage-swr-data との使い分け

**manage-client-state（このスキル）**: クライアント内で完結する UI 状態

- サイドバー開閉、テーマ、モーダル表示
- URL 同期（ページネーション、検索、フィルタ）
- ブラウザストレージ（localStorage）

**manage-swr-data**: サーバーから取得するデータ

- API レスポンスのキャッシュ
- データ取得・変更（GET/POST/PUT/DELETE）
- バックグラウンド再検証

**判断基準**: サーバーから取得するデータは manage-swr-data、クライアント内で完結する状態は manage-client-state を使用します。

## 状態管理の選択

| 要件 | 手段 | 例 |
|------|------|-----|
| URL復元（戻る/共有） | nuqs | page, query, filter |
| localStorage永続化 | useSWRImmutable + useEffect | theme, settings |
| セッション内のみ | useSWRImmutable | modal, selectedRows |

## ワークフロー

### 1. グローバル状態（useSWRImmutable）

```typescript
'use client'

import useSWRImmutable from 'swr/immutable'

export function useSidebar() {
  const { data, mutate } = useSWRImmutable('sidebar-open', null, {
    fallbackData: true
  })

  return {
    isOpen: data ?? true,
    toggle: () => mutate(!data, false)
  }
}

// コンポーネントでの使用
export function Sidebar() {
  const { isOpen, toggle } = useSidebar()

  return (
    <aside className={isOpen ? 'open' : 'closed'}>
      <button onClick={toggle}>切り替え</button>
    </aside>
  )
}
```

### 2. URL状態（nuqs）

#### Server Component（パース）

```typescript
import { createSearchParamsCache, parseAsInteger } from 'nuqs/server'
import type { PageProps } from 'next/types'

export const searchParamsCache = createSearchParamsCache({
  page: parseAsInteger.withDefault(1),
})

export default async function Page({ searchParams }: PageProps<'/users'>) {
  const { page } = await searchParamsCache.parse(searchParams)

  const users = await fetchUsers({ page })

  return <UserList users={users} page={page} />
}
```

#### Client Component（状態）

```typescript
'use client'

import { useQueryStates, parseAsInteger, parseAsString } from 'nuqs'

export function UserFilters() {
  const [{ page, query }, setFilters] = useQueryStates({
    page: parseAsInteger.withDefault(1),
    query: parseAsString.withDefault(''),
  })

  return (
    <input
      value={query}
      onChange={(e) => setFilters({ query: e.target.value, page: 1 })}
    />
  )
}
```

## 重要ルール

### グローバル状態

- `useSWRImmutable` を使用（`useSWR` ではない）
- デフォルト値に `fallbackData` を設定
- 再検証なしで更新するには `mutate(newValue, false)` を使用
- サーバーデータには使用しない

### URL状態

- Server Componentでは `createSearchParamsCache` を使用
- Client Componentでは `useQueryStates` を使用
- パーサー（`parseAsInteger`、`parseAsString`など）を使用
- 常に `.withDefault()` でデフォルト値を設定

## 詳細パターン

詳細な実装パターンについては references を参照してください：

- [global-state.md](references/global-state.md) - グローバルUI状態、localStorage、型安全
- [url-state.md](references/url-state.md) - URLパラメータ、カスタムパーサー、配列状態
- [integration-pattern.md](references/integration-pattern.md) - Server/Client統合、フィルタ実装、複数状態の併用
