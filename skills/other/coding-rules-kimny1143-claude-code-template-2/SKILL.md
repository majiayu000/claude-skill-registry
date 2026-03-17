---
name: coding-rules
description: >
  プロジェクト共通のコーディング規約。TypeScript、命名規則、関数設計、React/Next.js等。
  使用タイミング: (1) コードレビュー時 (2) 新規ファイル作成時 (3) リファクタリング時
  (4) コーディングスタイルの確認時 (5) チーム開発のルール確認時。
  トリガー例: 「コーディング規約」「命名規則は？」「TypeScriptのルール」
  「インポート順序」「コミットメッセージの書き方」
---

# coding-rules - コーディング規約

プロジェクト共通のコーディングルール。

---

## 1. TypeScript

### 型定義

```typescript
// ✅ 明示的な型定義
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

// ✅ 型推論が明確な場合は省略OK
const users = await repository.findAll(); // 戻り値の型は関数から推論

// ❌ any は使わない
const data: any = response.json();

// ✅ unknown を使って安全に処理
const data: unknown = await response.json();
if (isUser(data)) {
  console.log(data.email);
}
```

### Null/Undefined

```typescript
// ✅ Optional chaining
const email = user?.profile?.email;

// ✅ Nullish coalescing
const name = user.name ?? 'Anonymous';

// ❌ 非推奨
const name = user.name || 'Anonymous'; // 空文字もfalsy
```

---

## 2. インポート順序

```typescript
// 1. 外部ライブラリ
import { useState } from 'react';
import { z } from 'zod';

// 2. 内部モジュール（エイリアス）
import { db } from '@/db';
import { User } from '@/types';

// 3. 相対インポート
import { helper } from './utils';
import styles from './styles.module.css';
```

---

## 3. 命名規則

| 種類 | 規則 | 例 |
|------|------|-----|
| 変数・関数 | camelCase | `getUserById`, `isActive` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| クラス・型 | PascalCase | `UserService`, `CreateUserInput` |
| ファイル | kebab-case | `user-service.ts` |
| Reactコンポーネント | PascalCase | `UserCard.tsx` |
| 環境変数 | UPPER_SNAKE_CASE | `DATABASE_URL` |

### Boolean命名

```typescript
// ✅ is/has/can/should プレフィックス
const isActive = true;
const hasPermission = user.role === 'admin';
const canEdit = isOwner || isAdmin;
const shouldRefetch = isStale && !isLoading;
```

---

## 4. 関数

### 単一責任

```typescript
// ❌ 複数の責任
async function processUser(userId: string) {
  const user = await db.select().from(users).where(eq(users.id, userId));
  await sendEmail(user.email);
  await updateLastLogin(userId);
  return user;
}

// ✅ 分割
async function getUser(userId: string) {
  return db.select().from(users).where(eq(users.id, userId));
}

async function notifyUser(email: string) {
  await sendEmail(email);
}

async function recordLogin(userId: string) {
  await updateLastLogin(userId);
}
```

### 早期リターン

```typescript
// ❌ ネスト深い
function processData(data: Data | null) {
  if (data) {
    if (data.isValid) {
      if (data.items.length > 0) {
        return data.items.map(process);
      }
    }
  }
  return [];
}

// ✅ 早期リターン
function processData(data: Data | null) {
  if (!data) return [];
  if (!data.isValid) return [];
  if (data.items.length === 0) return [];

  return data.items.map(process);
}
```

---

## 5. エラーハンドリング

```typescript
// ✅ カスタムエラークラス
class ValidationError extends Error {
  constructor(
    message: string,
    public field: string
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}

// ✅ 適切なエラー処理
try {
  await riskyOperation();
} catch (error) {
  if (error instanceof ValidationError) {
    return apiError(error.message, { status: 400 });
  }
  console.error('Unexpected error:', error);
  return apiError('Internal error', { status: 500 });
}
```

---

## 6. コメント

```typescript
// ✅ WHYを説明
// Stripe APIの制限により、100件ずつバッチ処理する必要がある
const BATCH_SIZE = 100;

// ❌ WHATを説明（コードを読めばわかる）
// ユーザーを取得する
const user = await getUser(id);

// ✅ TODO/FIXME は issue番号付き
// TODO(#123): キャッシュ実装後に削除
// FIXME(#456): 競合状態の対応が必要
```

---

## 7. React/Next.js

### Server vs Client Components

```typescript
// Server Component (デフォルト)
// - データフェッチ
// - 機密情報アクセス
// - バンドルサイズ削減

// Client Component ('use client')
// - useState, useEffect
// - イベントハンドラ
// - ブラウザAPI

// ✅ 最小限のクライアントコンポーネント
'use client';
export function LikeButton({ postId }: { postId: string }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>Like</button>;
}
```

### Props

```typescript
// ✅ 型定義
interface UserCardProps {
  user: User;
  onEdit?: (id: string) => void;
  className?: string;
}

export function UserCard({ user, onEdit, className }: UserCardProps) {
  // ...
}
```

---

## 8. Git コミット

### Conventional Commits

```
feat: 新機能追加
fix: バグ修正
docs: ドキュメント
refactor: リファクタリング
test: テスト
chore: その他
```

### 例

```
feat: add user authentication
fix: resolve login redirect loop
docs: update API documentation
refactor: extract validation logic to separate module
test: add unit tests for UserService
chore: update dependencies
```
