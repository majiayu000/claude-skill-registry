---
name: store-creating
description: BoxLogのZustand storeを作成。devtools, persist, 型安全なパターンを適用。
---

# Store Creating Skill

BoxLogプロジェクトのZustand storeを規約に沿って作成するスキルです。

## このスキルを使用するタイミング

以下のキーワードが含まれる場合に自動的に起動：

- 「ストアを作成」「store作成」
- 「状態管理を追加」
- 「Zustandストア」
- 「useXxxStore を作って」

## ストアのパターン

### 1. 基本ストア（CRUD操作）

```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface EntityState {
  // State
  items: Entity[]
  isLoading: boolean
  error: string | null

  // Actions
  addItem: (item: CreateEntityInput) => Promise<boolean>
  updateItem: (id: string, updates: UpdateEntityInput) => Promise<boolean>
  deleteItem: (id: string) => Promise<boolean>
  getItemById: (id: string) => Entity | undefined

  // Helpers
  reset: () => void
}

export const useEntityStore = create<EntityState>()(
  devtools(
    persist(
      (set, get) => ({
        items: [],
        isLoading: false,
        error: null,

        addItem: async (data) => {
          try {
            set({ isLoading: true, error: null })
            // API call or local update
            const newItem: Entity = {
              id: generateId(),
              ...data,
              created_at: new Date(),
              updated_at: new Date(),
            }
            set((state) => ({
              items: [...state.items, newItem],
              isLoading: false,
            }))
            return true
          } catch (error) {
            set({ error: (error as Error).message, isLoading: false })
            return false
          }
        },

        updateItem: async (id, updates) => {
          try {
            set((state) => ({
              items: state.items.map((item) =>
                item.id === id
                  ? { ...item, ...updates, updated_at: new Date() }
                  : item
              ),
            }))
            return true
          } catch (error) {
            console.error('Failed to update:', error)
            return false
          }
        },

        deleteItem: async (id) => {
          set((state) => ({
            items: state.items.filter((item) => item.id !== id),
          }))
          return true
        },

        getItemById: (id) => get().items.find((item) => item.id === id),

        reset: () => set({ items: [], isLoading: false, error: null }),
      }),
      {
        name: 'entity-storage',
        partialize: (state) => ({ items: state.items }),
      }
    ),
    { name: 'entity-store' }
  )
)
```

### 2. UIステートストア（persist なし）

```typescript
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

interface UIState {
  isOpen: boolean
  selectedId: string | null

  open: () => void
  close: () => void
  setSelectedId: (id: string | null) => void
}

export const useDialogStore = create<UIState>()(
  devtools(
    (set) => ({
      isOpen: false,
      selectedId: null,

      open: () => set({ isOpen: true }),
      close: () => set({ isOpen: false, selectedId: null }),
      setSelectedId: (id) => set({ selectedId: id }),
    }),
    { name: 'dialog-store' }
  )
)
```

### 3. 選択ストア（ファクトリーパターン）

```typescript
import { createTableSelectionStore } from '@/features/table'

// 既存のファクトリーを使用
export const useEntitySelectionStore = createTableSelectionStore({
  storeName: 'entity-selection-store',
})
```

### 4. フィルター/ソートストア

```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

type SortField = 'name' | 'created_at' | 'updated_at'
type SortOrder = 'asc' | 'desc'

interface FilterState {
  search: string
  sortField: SortField
  sortOrder: SortOrder
  filters: Record<string, unknown>

  setSearch: (search: string) => void
  setSort: (field: SortField, order: SortOrder) => void
  setFilter: (key: string, value: unknown) => void
  clearFilters: () => void
}

export const useEntityFilterStore = create<FilterState>()(
  devtools(
    persist(
      (set) => ({
        search: '',
        sortField: 'created_at',
        sortOrder: 'desc',
        filters: {},

        setSearch: (search) => set({ search }),
        setSort: (field, order) => set({ sortField: field, sortOrder: order }),
        setFilter: (key, value) =>
          set((state) => ({
            filters: { ...state.filters, [key]: value },
          })),
        clearFilters: () => set({ search: '', filters: {} }),
      }),
      { name: 'entity-filter-storage' }
    ),
    { name: 'entity-filter-store' }
  )
)
```

## 命名規則

| パターン | ファイル名 | export名 |
|----------|-----------|----------|
| メインストア | `use{Entity}Store.ts` | `use{Entity}Store` |
| 選択ストア | `use{Entity}SelectionStore.ts` | `use{Entity}SelectionStore` |
| フィルター | `use{Entity}FilterStore.ts` | `use{Entity}FilterStore` |
| ソート | `use{Entity}SortStore.ts` | `use{Entity}SortStore` |
| ダイアログ | `use{Entity}DialogStore.ts` | `use{Entity}DialogStore` |

## チェックリスト

- [ ] `devtools` ミドルウェア使用（開発時デバッグ用）
- [ ] 永続化が必要なら `persist` ミドルウェア使用
- [ ] `partialize` で永続化対象を明示
- [ ] store名は一意（devtools識別用）
- [ ] インターフェース定義は State と Actions を分離
- [ ] エラーハンドリング実装
- [ ] テストファイル作成（`use{Entity}Store.test.ts`）

## 既存ストア参考

```
src/features/tags/stores/
├── useTagStore.ts           # CRUD操作
├── useTagSelectionStore.ts  # 選択（ファクトリー使用）
├── useTagSortStore.ts       # ソート
├── useTagSearchStore.ts     # 検索
├── useTagPaginationStore.ts # ページネーション
└── index.ts                 # バレル
```
