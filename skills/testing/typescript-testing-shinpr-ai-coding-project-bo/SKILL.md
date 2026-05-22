---
name: frontend/typescript-testing
description: React Testing LibraryとMSWでテストを設計。コンポーネントテストパターンを適用。
---

# TypeScript テストルール（フロントエンド）

## テストフレームワーク
- **Vitest**: このプロジェクトではVitestを使用
- **React Testing Library**: コンポーネントテスト用
- **MSW (Mock Service Worker)**: APIモック用
- テストのインポート: `import { describe, it, expect, beforeEach, vi } from 'vitest'`
- コンポーネントテストのインポート: `import { render, screen, fireEvent } from '@testing-library/react'`
- モックの作成: `vi.mock()` を使用

## テストの基本方針

### 品質要件
- **カバレッジ**: 単体テストのカバレッジは60%以上を必須（フロントエンド標準 2025）
- **独立性**: 各テストは他のテストに依存せず実行可能
- **再現性**: テストは環境に依存せず、常に同じ結果を返す
- **可読性**: テストコードも製品コードと同様の品質を維持

### カバレッジ要件
**必須**: 単体テストのカバレッジは60%以上
**コンポーネント別目標**:
- Atoms（Button、Text等）: 70%以上
- Molecules（FormField等）: 65%以上
- Organisms（Header、Footer等）: 60%以上
- Custom Hooks: 65%以上
- Utils: 70%以上

**指標**: Statements（文）、Branches（分岐）、Functions（関数）、Lines（行）

### テストの種類と範囲
1. **単体テスト（React Testing Library）**
   - 個々のコンポーネントや関数の動作を検証
   - 外部依存はすべてモック化
   - 最も数が多く、細かい粒度で実施
   - ユーザーから観測可能な振る舞いに焦点を当てる

2. **統合テスト（React Testing Library + MSW）**
   - 複数のコンポーネントの連携を検証
   - MSW（Mock Service Worker）でAPIをモック
   - 実際のDB接続なし（DBはバックエンドが管理）
   - 主要な機能フローの検証

3. **E2Eテストでの機能横断検証**
   - 新機能追加時、既存機能への影響を必ず検証
   - Design Docの「統合ポイントマップ」で影響度「高」「中」の箇所をカバー
   - 検証パターン: 既存機能動作 → 新機能有効化 → 既存機能の継続性確認
   - 判定基準: 表示内容の変化なし、レンダリング時間5秒以内
   - CI/CDでの自動実行を前提とした設計

## テストの実装規約

### ディレクトリ構造（Co-location原則）
```
src/
└── components/
    └── Button/
        ├── Button.tsx
        ├── Button.test.tsx  # コンポーネントと同じ場所に配置
        └── index.ts
```

**理由**:
- React Testing Libraryのベストプラクティス
- ADR-0002 Co-location原則
- 実装と一緒にテストを見つけやすく、保守しやすい

### 命名規則
- テストファイル: `{ComponentName}.test.tsx`
- 統合テストファイル: `{FeatureName}.integration.test.tsx`
- テストスイート: 対象のコンポーネントや機能を説明する名前
- テストケース: ユーザー視点から期待される動作を説明する名前

### テストコードの品質ルール

**推奨: すべてのテストを常に有効に保つ**
- メリット: テストスイートの完全性を保証
- 実践: 問題があるテストは修正して有効化

**避けるべき: test.skip()やコメントアウト**
- 理由: テストの穴が生まれ、品質チェックが不完全になる
- 対処: 不要なテストは完全に削除する

## モックの型安全性の徹底

### MSW（Mock Service Worker）セットアップ
```typescript
// 型安全なMSWハンドラー
import { rest } from 'msw'

const handlers = [
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(ctx.json({ id: '1', name: 'John' } satisfies User))
  })
]
```

### コンポーネントモックの型安全性
```typescript
// 必要な部分のみ
type TestProps = Pick<ButtonProps, 'label' | 'onClick'>
const mockProps: TestProps = { label: 'Click', onClick: vi.fn() }

// やむを得ない場合のみ、理由明記
const mockRouter = {
  push: vi.fn()
} as unknown as Router // 複雑なRouter型構造のため
```

## React Testing Libraryの基本例

```typescript
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button', () => {
  it('should call onClick when clicked', () => {
    const onClick = vi.fn()
    render(<Button label="Click me" onClick={onClick} />)
    fireEvent.click(screen.getByRole('button', { name: 'Click me' }))
    expect(onClick).toHaveBeenCalledOnce()
  })
})
```

## テスト品質基準

### 境界値・異常系の網羅
正常系に加え、境界値と異常系を含める。
```typescript
it('renders empty state for empty array', () => {
  render(<UserList users={[]} />)
  expect(screen.getByText('ユーザーがいません')).toBeInTheDocument()
})

it('displays error message on API failure', async () => {
  server.use(rest.get('/api/users', (req, res, ctx) => res(ctx.status(500))))
  render(<UserList />)
  expect(await screen.findByText('エラーが発生しました')).toBeInTheDocument()
})
```

### ユーザー中心のクエリ

```typescript
// 良い: アクセシブルなクエリ
screen.getByRole('button', { name: 'Submit' })
screen.getByLabelText('Email')
screen.getByText('Welcome')

// 悪い: 実装詳細への依存
screen.getByTestId('submit-btn')
container.querySelector('.btn-primary')
```

### 非同期処理のテスト

```typescript
it('loads and displays user data', async () => {
  render(<UserProfile userId="1" />)

  // ローディング状態を確認
  expect(screen.getByText('Loading...')).toBeInTheDocument()

  // データ表示を待機
  expect(await screen.findByText('John Doe')).toBeInTheDocument()

  // ローディングが消えていることを確認
  expect(screen.queryByText('Loading...')).not.toBeInTheDocument()
})
```

### フォームテスト

```typescript
it('submits form with valid data', async () => {
  const onSubmit = vi.fn()
  render(<LoginForm onSubmit={onSubmit} />)

  await userEvent.type(screen.getByLabelText('Email'), 'test@example.com')
  await userEvent.type(screen.getByLabelText('Password'), 'password123')
  await userEvent.click(screen.getByRole('button', { name: 'Login' }))

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'password123'
  })
})
```

## アンチパターン

```typescript
// 悪い: 実装詳細のテスト
it('calls setState', () => {
  const setState = vi.spyOn(React, 'useState')
  render(<Counter />)
  // ...
})

// 良い: ユーザーが見る結果をテスト
it('increments count when clicked', () => {
  render(<Counter />)
  fireEvent.click(screen.getByRole('button', { name: '+' }))
  expect(screen.getByText('Count: 1')).toBeInTheDocument()
})
```
