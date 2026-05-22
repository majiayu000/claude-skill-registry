---
name: feature-scaffolding
description: BoxLogの新しいFeatureモジュールを作成。stores, hooks, components, types の統一構造を生成。
---

# Feature Scaffolding Skill

BoxLogプロジェクトの新しいFeatureモジュールを規約に沿って作成するスキルです。

## このスキルを使用するタイミング

以下のキーワードが含まれる場合に自動的に起動：

- 「新しい機能を作成」「feature作成」
- 「〇〇機能を追加」
- 「モジュールを作成」
- 「src/features/xxx を作って」

## Feature構造

```
src/features/{feature-name}/
├── index.ts              # Public API（バレルファイル）
├── types/
│   └── index.ts          # 型定義
├── stores/
│   └── index.ts          # Zustand stores
├── hooks/
│   └── index.ts          # カスタムフック
├── components/
│   └── index.ts          # UIコンポーネント
├── constants/            # (optional)
│   └── index.ts
└── contexts/             # (optional)
    └── {Feature}Context.tsx
```

## 作成手順

### 1. ディレクトリ作成

```bash
FEATURE_NAME="your-feature"
mkdir -p src/features/${FEATURE_NAME}/{types,stores,hooks,components}
```

### 2. types/index.ts

```typescript
// {Feature}の型定義

export interface {Entity} {
  id: string
  user_id: string
  // entity fields
  created_at: Date
  updated_at: Date
}

export interface Create{Entity}Input {
  // required fields for creation
}

export interface Update{Entity}Input {
  // optional fields for update
}
```

### 3. stores/index.ts

```typescript
export { use{Feature}Store } from './use{Feature}Store'
```

### 4. stores/use{Feature}Store.ts

```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface {Feature}State {
  // state
  items: {Entity}[]

  // actions
  addItem: (item: Create{Entity}Input) => Promise<boolean>
  updateItem: (id: string, updates: Update{Entity}Input) => Promise<boolean>
  deleteItem: (id: string) => Promise<boolean>
  getItemById: (id: string) => {Entity} | undefined
}

export const use{Feature}Store = create<{Feature}State>()(
  devtools(
    persist(
      (set, get) => ({
        items: [],

        addItem: async (data) => {
          // implementation
        },

        updateItem: async (id, updates) => {
          // implementation
        },

        deleteItem: async (id) => {
          // implementation
        },

        getItemById: (id) => {
          return get().items.find((item) => item.id === id)
        },
      }),
      {
        name: '{feature}-storage',
        partialize: (state) => ({ items: state.items }),
      }
    ),
    { name: '{feature}-store' }
  )
)
```

### 5. hooks/index.ts

```typescript
export { use{Feature}s } from './use-{feature}s'
export { use{Feature}Operations } from './use-{feature}-operations'
```

### 6. components/index.ts

```typescript
export { {Feature}List } from './{Feature}List'
export { {Feature}Item } from './{Feature}Item'
```

### 7. index.ts（Public API）

```typescript
/**
 * {Feature} Feature - Public API
 *
 * @example
 * ```tsx
 * // ✅ 推奨: バレルファイル経由
 * import { {Feature}List, use{Feature}s, use{Feature}Store } from '@/features/{feature}'
 *
 * // ❌ 非推奨: 深いパス指定
 * import { {Feature}List } from '@/features/{feature}/components/{Feature}List'
 * ```
 */

// Components
export { } from './components'

// Hooks
export { } from './hooks'

// Stores
export { use{Feature}Store } from './stores'

// Types
export type { } from './types'
```

## 命名規則

| 種類 | 命名規則 | 例 |
|------|----------|-----|
| ディレクトリ | kebab-case | `user-settings` |
| コンポーネント | PascalCase | `UserSettingsList` |
| フック | camelCase (use prefix) | `useUserSettings` |
| ストア | camelCase (use prefix) | `useUserSettingsStore` |
| 型 | PascalCase | `UserSettings` |

## チェックリスト

- [ ] 全てのexportは `index.ts` 経由
- [ ] 型は `types/index.ts` に集約
- [ ] ストアは devtools + persist ミドルウェア使用
- [ ] コンポーネントは `export function` 形式（`export default` 禁止）
- [ ] セマンティックトークン使用（`bg-card`, `text-foreground` 等）

## 参考: 既存Feature

```
src/features/
├── tags/        # 参考実装（最も完成度が高い）
├── plans/       # 複雑なFeatureの例
├── calendar/    # 大規模Featureの例
├── settings/    # シンプルなFeatureの例
└── auth/        # 認証関連
```
