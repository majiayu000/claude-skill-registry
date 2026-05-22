---
name: nextjs-firestore
description: Next.js + Firebase/Firestore統合開発パターン。型定義、データ操作(CRUD)、リアルタイム同期、認証、セキュリティルールに使用。Firestore、Firebase、データベース操作、リアルタイムリスナー、Firebase Auth時に使用。
---

# Next.js + Firestore 開発スキル

Next.jsアプリケーションでFirestoreを効率的に使用するためのパターンとベストプラクティス。

## クイックスタート

### 基本的なドキュメント型定義

```typescript
import { Timestamp } from 'firebase/firestore';

interface BaseDocument {
  id: string;
  createdAt: Timestamp;
  updatedAt: Timestamp;
}

export interface User extends BaseDocument {
  email: string;
  displayName: string;
  photoURL?: string;
}
```

### ドキュメント取得

```typescript
import { doc, getDoc } from 'firebase/firestore';
import { db } from '@/lib/firebase';

export async function getUser(userId: string): Promise<User | null> {
  const docRef = doc(db, 'users', userId);
  const docSnap = await getDoc(docRef);
  return docSnap.exists() ? docSnap.data() as User : null;
}
```

### リアルタイムリスナー（カスタムフック）

```typescript
import { doc, onSnapshot } from 'firebase/firestore';
import { useEffect, useState } from 'react';

export function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onSnapshot(
      doc(db, 'users', userId),
      (snapshot) => {
        setUser(snapshot.exists() ? snapshot.data() as User : null);
        setLoading(false);
      }
    );
    return () => unsubscribe();
  }, [userId]);

  return { user, loading };
}
```

### 認証状態管理

```typescript
import { createContext, useContext, useEffect, useState } from 'react';
import { onAuthStateChanged, User } from 'firebase/auth';
import { auth } from '@/lib/firebase';

const AuthContext = createContext<{ user: User | null; loading: boolean }>({
  user: null,
  loading: true
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

---

## 詳細パターン

より詳細な実装パターンと例は以下のリファレンスを参照:

- **[data-operations.md](references/data-operations.md)** - CRUD操作、クエリ、トランザクション、Converterパターン
- **[realtime-listeners.md](references/realtime-listeners.md)** - リアルタイムリスナーの詳細パターン、エラーハンドリング
- **[auth-patterns.md](references/auth-patterns.md)** - 認証フロー、サインイン/アウト、ユーザー管理
- **[security-rules.md](references/security-rules.md)** - Firestoreセキュリティルールのベストプラクティス

---

## ベストプラクティス

### 型定義
- `BaseDocument`を継承して一貫性を保つ
- Converterパターンで型安全性を確保

### データ操作
- `serverTimestamp()`で一貫性を保つ
- エラーハンドリングを必ず実装

### リアルタイムリスナー
- `useEffect`のreturnでunsubscribeを呼ぶ
- ローディング状態とエラー状態を管理

### セキュリティ
- クライアントサイドでのセキュリティ依存は避ける
- セキュリティルールを必ず設定

---

## エラーハンドリング

```typescript
import { FirebaseError } from 'firebase/app';

export function handleFirestoreError(error: unknown): string {
  if (error instanceof FirebaseError) {
    switch (error.code) {
      case 'permission-denied': return 'アクセス権限がありません';
      case 'not-found': return 'データが見つかりません';
      case 'already-exists': return 'データが既に存在します';
      case 'unavailable': return 'サービスが一時的に利用できません';
      default: return `エラーが発生しました: ${error.message}`;
    }
  }
  return '予期しないエラーが発生しました';
}
```
