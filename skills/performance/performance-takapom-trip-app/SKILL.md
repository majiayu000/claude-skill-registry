---
name: performance
description: React Nativeアプリのパフォーマンスを最適化する。FlatList化、メモ化、画像最適化などを実施する。「パフォーマンス改善して」「リスト重い」「描画を速くして」などのリクエストで使用する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [対象画面名 or 省略で全画面]
---

# パフォーマンス最適化スキル

iPhoneでの滑らかな60fps描画を目指し、React Nativeアプリのパフォーマンスを最適化する。

## デザイン前提: Liquid Glass

本プロジェクトは `@callstack/liquid-glass` による Liquid Glass デザインを前提とする。
ガラスエフェクトはGPU負荷が高いため、以下のパフォーマンス指針を守る:

- **リストアイテム内のガラス要素は最小限に:** FlatList の `renderItem` 内に `LiquidGlassView` を配置する場合、`removeClippedSubviews={true}` で画面外要素をアンマウントする
- **ガラス要素のネストを避ける:** `LiquidGlassView` の中に別の `LiquidGlassView` を入れない
- **`effect` の動的切り替えを頻繁に行わない:** マテリアライズ/デマテリアライズのアニメーションはコストが高い
- **`LiquidGlassContainerView` の `spacing` を適切に設定:** 不要なマージ計算を避ける
- **スクロール中のガラス要素数を制限:** 大量のガラスカードが同時に表示される場合、`windowSize` を小さめ（3-5）に設定する
- **フォールバック時は単純な `View` + `backgroundColor`:** ガラス非対応デバイスではブラー計算が不要なため、パフォーマンスが向上する

## 対象ファイル

- `src/screens/**/*.tsx` — 画面コンポーネント
- `src/components/**/*.tsx` — UIコンポーネント
- `src/hooks/**/*.ts` — カスタムフック

## 手順

### 1. リスト表示の最適化（最優先）

#### ScrollView + .map() → FlatList への変換

**問題:** `.map()` はすべての要素を一度にレンダリングするため、リストが長くなるとパフォーマンスが低下する。

**変換パターン:**
```tsx
// Before: ScrollView + .map()
<ScrollView>
  {items.map((item) => (
    <ItemCard key={item.id} item={item} />
  ))}
</ScrollView>

// After: FlatList
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <ItemCard item={item} />}
  contentContainerStyle={{ paddingBottom: spacing.xxl }}
  showsVerticalScrollIndicator={false}
/>
```

**グリッドレイアウト（2列）:**
```tsx
<FlatList
  data={posts}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <PostCard post={item} />}
  numColumns={2}
  columnWrapperStyle={{ gap: spacing.sm }}
  contentContainerStyle={{ gap: spacing.sm, paddingBottom: spacing.xxl }}
  showsVerticalScrollIndicator={false}
/>
```

**FlatList に追加すべきプロパティ:**
```tsx
<FlatList
  // 基本
  data={data}
  keyExtractor={(item) => item.id}
  renderItem={renderItem}
  // パフォーマンス
  removeClippedSubviews={true}        // 画面外の要素をアンマウント
  maxToRenderPerBatch={10}            // バッチあたりの最大レンダリング数
  windowSize={5}                       // レンダリングウィンドウサイズ
  initialNumToRender={10}             // 初期レンダリング数
  // UX
  ListEmptyComponent={<EmptyState />}  // 空状態
  ListHeaderComponent={<Header />}     // ヘッダー
/>
```

### 2. プルトゥリフレッシュの追加

FlatList 化と同時に RefreshControl を追加する:

```tsx
import { RefreshControl } from 'react-native';

const { refetch, isRefetching } = useMyQuery();

<FlatList
  refreshControl={
    <RefreshControl
      refreshing={isRefetching}
      onRefresh={refetch}
      tintColor={color.accent}
    />
  }
/>
```

### 3. コンポーネントのメモ化

頻繁に再レンダリングされるコンポーネントを `React.memo` で最適化:

```tsx
// リストアイテムコンポーネント
export const PostCard = React.memo<Props>(({ post, onPress }) => {
  return (
    // ...
  );
});
```

**メモ化すべきコンポーネント:**
- リストのアイテムコンポーネント（`renderItem` で使用）
- `AppTabBar`（親の状態変更で不要に再レンダリングされる）
- `GradientPillButton`, `OutlinePillButton`（props が変わらない限り再描画不要）

**メモ化が不要なコンポーネント:**
- 画面トップレベルコンポーネント（Screen系）
- 常にpropsが変わるコンポーネント

### 4. コールバックのメモ化

`renderItem` や `onPress` など、子コンポーネントに渡すコールバックを `useCallback` で安定させる:

```tsx
const renderItem = useCallback(({ item }: { item: Post }) => (
  <PostCard post={item} onPress={() => handlePostPress(item.id)} />
), [handlePostPress]);

const handlePostPress = useCallback((postId: string) => {
  // ...
}, []);
```

### 5. 画像の最適化

```tsx
import { Image } from 'react-native';

<Image
  source={{ uri: imageUrl }}
  style={styles.postImage}
  resizeMode="cover"
  // 画像サイズの事前指定（レイアウトシフト防止）
  fadeDuration={200}
/>
```

**推奨: expo-image への移行（大量の画像がある場合）:**
```bash
npx expo install expo-image
```
```tsx
import { Image } from 'expo-image';

<Image
  source={{ uri: imageUrl }}
  style={styles.postImage}
  contentFit="cover"
  placeholder={blurhash}       // ブラーハッシュプレースホルダー
  transition={200}             // フェードイン
  cachePolicy="memory-disk"   // メモリ+ディスクキャッシュ
/>
```

### 6. 計算値のメモ化

重い計算やフィルタリングには `useMemo` を使用:

```tsx
const sortedPosts = useMemo(
  () => posts?.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()),
  [posts]
);
```

### 7. TanStack Query の最適化

既存の設定 (`src/lib/queryClient.ts`) を確認し、必要に応じて調整:

```tsx
// 画面フォーカス時の自動再取得
import { useIsFocused } from '@react-navigation/native'; // or equivalent

const { data } = useMyQuery({
  // 画面フォーカス時のみ再取得
  refetchOnWindowFocus: true,
  // バックグラウンド復帰時の再取得
  refetchOnReconnect: true,
});
```

## チェックリスト

変更後に以下を確認:

- [ ] `.map()` によるリスト描画が `FlatList` に置き換わっているか
- [ ] `FlatList` に `keyExtractor` が設定されているか
- [ ] リストアイテムコンポーネントが `React.memo` で包まれているか
- [ ] `renderItem` が `useCallback` で安定しているか
- [ ] 大量の画像にキャッシュ戦略があるか
- [ ] 不要なインラインオブジェクト/関数の生成がないか

## ルール

- 既存の UI/レイアウトを変更しない（パフォーマンスのみ改善）
- `React.memo` は props が頻繁に変わるコンポーネントには使わない（逆効果）
- 過度な最適化は避ける（measurable な問題がある箇所を優先）
- TanStack Query のキャッシュ戦略（`staleTime`, `gcTime`）は既存設定を尊重する
- 新規パッケージは `expo-image` のみ必要に応じて追加可（それ以外は既存APIで対応）
