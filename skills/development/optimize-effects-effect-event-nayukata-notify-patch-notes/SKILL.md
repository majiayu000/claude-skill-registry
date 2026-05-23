---
name: optimize-effects-effect-event
description: useEffectEventを使用して非リアクティブなロジックを抽出し、Effectを最適化します。特定の値が変更されたときにEffectを再実行すべきでない場合（ログ、分析、タイマー）に使用します。
---

# useEffectEventによるEffectの最適化

Effect内のリアクティブなロジックと非リアクティブなロジックを分離します。

## クイックスタート

```typescript
import { useEffect, useEffectEvent } from 'react'

export function PageView({ pageUrl }) {
  const userId = useAuthContext()

  // 非リアクティブなロジックを抽出
  const onLog = useEffectEvent((url) => {
    logAnalytics(url, userId) // userIdは常に最新の値
  })

  useEffect(() => {
    onLog(pageUrl)
  }, [pageUrl]) // userIdは依存配列に含めない
}
```

## いつ使うか

このスキルを使用する場合
- ログや分析（すべての状態変更で再ログしたくない場合）
- 最新の状態を使用するタイマー
- Effect内のイベントハンドラ
- 不要なEffectの再実行を避けたい場合

## 重要ルール

- 非リアクティブなロジックを `useEffectEvent` に抽出
- **Effect EventはEffect内から直接呼ばれる関数のみ**（孫関数は通常の関数）
- 他のコンポーネントに渡さない
- Effect外で呼び出さない

## アンチパターン

❌ **間違い**: すべての関数をuseEffectEventにする
```typescript
// 孫関数もuseEffectEvent（不要）
const saveToken = useEffectEvent(async (user) => {...})
const syncUser = useEffectEvent(async () => {...})
const processLogin = useEffectEvent(async (user) => {
  await saveToken(user)  // Effectから直接呼ばれていない
  await syncUser()
})
const handleAuthChange = useEffectEvent(async (user) => {
  await processLogin(user)  // ✅ Effectから直接呼ばれる
})
```

✅ **正解**: Effectから直接呼ばれる関数のみuseEffectEvent
```typescript
// 孫関数は通常の関数
const saveToken = async (user) => {...}
const syncUser = async () => {...}
const processLogin = async (user) => {
  await saveToken(user)
  await syncUser()
}
// Effectから直接呼ばれる関数のみuseEffectEvent
const handleAuthChange = useEffectEvent(async (user) => {
  await processLogin(user)
})
```

**理由**: useEffectEventはEffect内の依存配列を最適化するためのもの。
孫関数は既にEffect Eventの中にあるため、追加のuseEffectEventは不要。

## メリット

- 依存配列がクリーンになる
- Effectの再実行が減る
- 常に最新の値にアクセスできる
- パフォーマンスが向上

## 詳細パターン

[effect-event.md](references/effect-event.md)を参照
- ログパターン
- タイマーパターン
- イベントハンドラパターン
- 移行ガイド
