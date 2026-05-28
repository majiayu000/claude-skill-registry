---
name: optimize-conditional-rendering-activity
description: Activityコンポーネントを使用してすべての条件付きレンダリングを処理します。タブ、モーダル、表示/非表示UI、APIレスポンス状態（loading、error、empty、data）に必須です。
---

# Activity による条件付きレンダリングの最適化

**すべての条件付きレンダリングは Activity コンポーネントを使用してください。**

## ⚠️ 重要ルール

**条件付きレンダリングは必ずActivityを使用してください。**

### 禁止

- `{condition && <Component />}`
- `{condition ? <A /> : <B />}`
- CSS `display: none` による表示/非表示

### 必須

- `<Activity mode={condition ? 'visible' : 'hidden'}><Component /></Activity>`

### 例外

- early returnのみ（型narrowingが必要な場合）

```typescript
// ✅ OK: early returnで型narrowing
function Component() {
  const { data, error, isLoading } = useSWR(...)

  if (isLoading) return <Spinner />
  if (error) return <Alert>エラー</Alert>
  if (!data) return <Empty />

  // ここでdataはData型に確定
  return <div>{data.name}</div>
}

// ❌ NG: 条件付きレンダリング
function Component() {
  const { data } = useSWR(...)
  return (
    <div>
      {data && <UserList data={data} />}
    </div>
  )
}
```

## クイックスタート

### パターン 1: タブUI

```typescript
import { Activity } from 'react'
import { useState } from 'react'

export function TabPanel() {
  const [activeTab, setActiveTab] = useState('profile')

  return (
    <div>
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="profile">プロフィール</TabsTrigger>
          <TabsTrigger value="settings">設定</TabsTrigger>
        </TabsList>

        <div className="mt-4">
          <Activity mode={activeTab === 'profile' ? 'visible' : 'hidden'}>
            <ProfileTab />
          </Activity>
          <Activity mode={activeTab === 'settings' ? 'visible' : 'hidden'}>
            <SettingsTab />
          </Activity>
        </div>
      </Tabs>
    </div>
  )
}
```

### パターン 2: モーダル/ダイアログ

```typescript
import { Activity } from 'react'

export function UserDialog({ open, onOpenChange, userId }) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <Activity mode={open ? 'visible' : 'hidden'}>
          <UserDetail userId={userId} />
        </Activity>
      </DialogContent>
    </Dialog>
  )
}
```

## いつ使うか

**必ず使用する場合：**
- タブの構築（切り替え時にフォーム状態を保持）
- モーダルの構築（スクロール位置を保持）
- APIレスポンス状態の処理（loading、error、empty、data）
- 任意の条件付き表示/非表示UI

**唯一の例外：**
- 型narrowingが必要なearly returnパターン

## 重要ルール

- `react`からインポート: `import { Activity } from 'react'`
- 表示には `<Activity mode="visible">` を使用
- 非表示には `<Activity mode="hidden">` を使用
- 非表示時もコンポーネント状態は保持される
- 条件付きレンダリングよりパフォーマンスが良い
- プリレンダリングと選択的ハイドレーションを可能にする

### ⚠️ Activity 内での型安全性

**Activity は `mode='hidden'` でも DOM を保持するため、non-null assertion (`!`) は使用禁止です。**

```typescript
// ❌ NG: mode='hidden' 時に undefined で実行時エラー
<Activity mode={user ? 'visible' : 'hidden'}>
  <div>{user!.email}</div>
  <Badge>{getRoleLabel(user!.role)}</Badge>
</Activity>

// ✅ OK: optional chaining を使用
<Activity mode={user ? 'visible' : 'hidden'}>
  <div>{user?.email}</div>
  <Badge>{user?.role && getRoleLabel(user.role)}</Badge>
</Activity>

// ❌ OK: 子の中で && を使ってガード（コンポーネント全体を渡す場合。プリレンダリング対象が空のため、Activityの恩恵を得られない。stateも保持されない）
<Activity mode={user ? 'visible' : 'hidden'}>
  {user && <UserProfile user={user} />}
</Activity>
```

### Activity のネスト禁止

**Activity コンポーネントはネストせず、二次的な条件は `&&` 演算子を使用してください。**

## メリット

1. **状態保持**: コンポーネント状態（スクロール位置、フォーム入力、展開状態）が非表示時も保持される
2. **型安全**: ほとんどの場合で型narrowingが不要
3. **パフォーマンス**: コンポーネントのマウント/アンマウントより高速
4. **一貫性**: すべての条件付きレンダリングが同じパターンを使用
5. **可読性**: 並列的な状態記述はネストした条件分岐より理解しやすい

## よくある間違い

### ❌ && 演算子を使わない

```typescript
// ❌ NG
{userName && <UserLink userName={userName} />}
{isLoading && <Spinner />}
```

### ❌ 三項演算子を表示/非表示に使わない

```typescript
// ❌ NG
{isLoading ? <Spinner /> : <UserList />}
```

### ❌ CSS displayを使わない

```typescript
// ❌ NG
<div style={{ display: isLoading ? 'block' : 'none' }}>
  <Spinner />
</div>
```

### ✅ Activityを使う

```typescript
// ✅ OK
<Activity mode={userName ? 'visible' : 'hidden'}>
  <UserLink userName={userName} />
</Activity>

<Activity mode={isLoading ? 'visible' : 'hidden'}>
  <Spinner />
</Activity>
```

## 関連スキル

- handle-edit-pages: 編集ページでloading/errorステート処理にActivityが必要
- handle-forms-rhf-zod: フォームの送信中/成功/エラー状態にActivityが必要
- manage-swr-data: データ取得・変更のloading/success/errorフィードバックにActivityが必要
- convert-enum-labels: Activity 内で enum ラベルを表示する際の optional chaining パターン
- format-dates: Activity 内で日付をフォーマットする際の optional chaining パターン
