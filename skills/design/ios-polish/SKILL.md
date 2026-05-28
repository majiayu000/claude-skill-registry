---
name: ios-polish
description: iOSネイティブの操作感に近づけるUI仕上げを行う。ジェスチャー、アニメーション、ブラーエフェクト、ダークモード対応などを実装する。「iOSっぽくして」「操作感を良くして」「アニメーション追加」「ダークモード対応」などのリクエストで使用する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [対象画面名 or 機能名]
---

# iOS 仕上げスキル

iPhoneユーザーが「ネイティブアプリのように感じる」操作感を実現するための仕上げを行う。

## デザイン前提: Liquid Glass

本プロジェクトは Apple iOS 26 の **Liquid Glass** デザインを前提とする。
`@callstack/liquid-glass` ライブラリを使用し、ガラス質感のUIを実現する。

### ライブラリ要件
- `@callstack/liquid-glass` — Liquid Glass コンポーネント
- Xcode >= 26, React Native 0.80+
- **Expo Go では動作しない**（Development Build が必要）

### コアコンポーネント

**LiquidGlassView** — ガラスエフェクトを持つ View:
```tsx
import { LiquidGlassView, isLiquidGlassSupported } from '@callstack/liquid-glass';

<LiquidGlassView
  style={{ borderRadius: 20, padding: 16 }}
  effect="regular"       // 'clear' | 'regular' | 'none'
  interactive={true}     // タッチ時のガラスアニメーション
  tintColor="#FF7AA2"    // ガラスの色味（ブランドカラー）
  colorScheme="system"   // 'light' | 'dark' | 'system'
>
  <Text style={{ color: PlatformColor('labelColor') }}>コンテンツ</Text>
</LiquidGlassView>
```

**LiquidGlassContainerView** — 複数ガラス要素のマージ:
```tsx
import { LiquidGlassContainerView, LiquidGlassView } from '@callstack/liquid-glass';

// タブバーのように近接するガラス要素をグループ化
<LiquidGlassContainerView spacing={12}>
  <LiquidGlassView style={{ borderRadius: 20, padding: 12 }}>
    <Ionicons name="home" size={24} />
  </LiquidGlassView>
  <LiquidGlassView style={{ borderRadius: 20, padding: 12 }}>
    <Ionicons name="notifications" size={24} />
  </LiquidGlassView>
</LiquidGlassContainerView>
```

### 適用箇所ガイド

| UI要素 | effect | interactive | 備考 |
|--------|--------|-------------|------|
| カード（広場カード、投稿カード） | `regular` | `true` | タップ可能なカードに最適 |
| ツールバー / ナビゲーションバー | `regular` | `false` | 背景ブラーのみ |
| タブバー | `regular` | `true` | `LiquidGlassContainerView` でグループ化 |
| モーダル / ボトムシート | `clear` | `false` | より透明なガラスで背景を透過 |
| ボタン（プライマリ） | `regular` | `true` | `tintColor` でブランドカラーを適用 |
| フローティングアクションボタン | `regular` | `true` | 丸いガラスボタン |
| 装飾・背景 | — | — | **ガラスを使わない**（全画面ガラスはNG） |

### フォールバックパターン

```tsx
import { LiquidGlassView, isLiquidGlassSupported } from '@callstack/liquid-glass';

const GlassCard: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  if (isLiquidGlassSupported) {
    return (
      <LiquidGlassView
        style={styles.card}
        effect="regular"
        interactive
      >
        {children}
      </LiquidGlassView>
    );
  }

  // iOS 26未満 / Android フォールバック
  return (
    <View style={[styles.card, styles.cardFallback]}>
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    borderRadius: 20,
    padding: 16,
  },
  cardFallback: {
    backgroundColor: 'rgba(255, 255, 255, 0.85)',
    // 既存デザイントークンの shadow.soft を適用
  },
});
```

### テキスト色のガイドライン

```tsx
import { PlatformColor } from 'react-native';

// ガラス上のテキスト（iOS 26で自動適応）
const glassTextStyle = {
  color: PlatformColor('labelColor'),          // メインテキスト
  // or
  color: PlatformColor('secondaryLabelColor'), // サブテキスト
};

// フォールバック（PlatformColor非対応環境）
const fallbackTextStyle = {
  color: '#1B1B1D', // color.ink from tokens.ts
};
```

## 対象ファイル

- `src/screens/**/*.tsx` — 画面コンポーネント
- `src/components/**/*.tsx` — UIコンポーネント
- `src/theme/tokens.ts` — デザイントークン
- `src/App.tsx` — ナビゲーション

## カテゴリ別 実装手順

---

### 1. プレスフィードバック（ボタンのアニメーション）

すべてのインタラクティブ要素にプレス時の視覚的フィードバックを追加する。

**Pressable の style 関数パターン:**
```tsx
<Pressable
  onPress={handlePress}
  style={({ pressed }) => [
    styles.button,
    {
      opacity: pressed ? 0.7 : 1,
      transform: [{ scale: pressed ? 0.97 : 1 }],
    },
  ]}
>
```

**カードのプレスフィードバック:**
```tsx
<Pressable
  onPress={handlePress}
  style={({ pressed }) => [
    styles.card,
    {
      opacity: pressed ? 0.85 : 1,
      transform: [{ scale: pressed ? 0.98 : 1 }],
    },
  ]}
>
```

---

### 2. iOS標準アイコンへの置き換え

絵文字アイコンを `@expo/vector-icons` の Ionicons（iOS標準に最も近い）に置き換える。

**インストール確認:**
```bash
# @expo/vector-icons は Expo に同梱済み。追加インストール不要
```

**置き換えマッピング:**

| 現在（絵文字） | 置き換え先 | Ionicons名 |
|---------------|-----------|------------|
| ← （戻る） | `<Ionicons name="chevron-back" />` | `chevron-back` |
| ••• （設定） | `<Ionicons name="ellipsis-horizontal" />` | `ellipsis-horizontal` |
| ＋ （追加） | `<Ionicons name="add" />` | `add` |
| 🏠 （ホーム） | `<Ionicons name="home" />` / `home-outline` | `home` / `home-outline` |
| 🔔 （通知） | `<Ionicons name="notifications" />` / `notifications-outline` | `notifications` |
| ⚙️ （設定） | `<Ionicons name="settings" />` / `settings-outline` | `settings` |
| 📷 （カメラ） | `<Ionicons name="camera" />` / `camera-outline` | `camera` |
| 👍 （いいね） | `<Ionicons name="heart" />` / `heart-outline` | `heart` |

**使用パターン:**
```tsx
import { Ionicons } from '@expo/vector-icons';

<Ionicons
  name="chevron-back"
  size={24}
  color={color.ink}
/>
```

**タブバーでの使い分け（選択/非選択）:**
```tsx
<Ionicons
  name={isActive ? "home" : "home-outline"}
  size={24}
  color={isActive ? color.accent : color.textMuted}
/>
```

---

### 3. ナビゲーションのジェスチャー対応

#### スワイプバック（推奨: react-native-gesture-handler）

現在の状態ベースルーターでスワイプバックを実装する場合:

```tsx
import { GestureDetector, Gesture } from 'react-native-gesture-handler';

// 画面コンポーネントのルートに追加
const swipeBack = Gesture.Pan()
  .activeOffsetX(20)       // 右方向20px以上で発動
  .onEnd((event) => {
    if (event.translationX > 80) {
      // 前の画面に戻る
      onBack();
    }
  });

<GestureDetector gesture={swipeBack}>
  <View style={{ flex: 1 }}>
    {/* 画面コンテンツ */}
  </View>
</GestureDetector>
```

#### プルトゥリフレッシュ

```tsx
import { RefreshControl } from 'react-native';

<FlatList
  refreshControl={
    <RefreshControl
      refreshing={isRefreshing}
      onRefresh={handleRefresh}
      tintColor={color.accent}
    />
  }
/>
```

---

### 4. 画面遷移アニメーション

Animated API を使った画面のフェードイン:

```tsx
import { useEffect, useRef } from 'react';
import { Animated } from 'react-native';

const fadeAnim = useRef(new Animated.Value(0)).current;
const slideAnim = useRef(new Animated.Value(20)).current;

useEffect(() => {
  Animated.parallel([
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 300,
      useNativeDriver: true,
    }),
    Animated.timing(slideAnim, {
      toValue: 0,
      duration: 300,
      useNativeDriver: true,
    }),
  ]).start();
}, []);

<Animated.View style={{ opacity: fadeAnim, transform: [{ translateY: slideAnim }] }}>
  {/* コンテンツ */}
</Animated.View>
```

---

### 5. ロングプレスメニュー

投稿カードやリストアイテムにロングプレスアクションを追加:

```tsx
<Pressable
  onPress={handlePress}
  onLongPress={() => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    showActionSheet();  // or setMenuVisible(true)
  }}
  delayLongPress={500}
>
```

---

### 6. StatusBar の適切な管理

各画面の背景色に応じた StatusBar スタイル:

```tsx
import { StatusBar } from 'expo-status-bar';

// 明るい背景の画面
<StatusBar style="dark" />

// 暗い/グラデーション背景の画面
<StatusBar style="light" />

// 自動判定（推奨）
<StatusBar style="auto" />
```

---

### 7. タッチターゲットの最適化

iOS Human Interface Guidelines: 最低44x44ptのタッチ領域:

```tsx
<Pressable
  onPress={handlePress}
  hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}  // タッチ領域を拡大
  style={styles.smallButton}
>
```

---

### 8. ダークモード対応（オプション）

`useColorScheme` でシステムのダークモード設定を取得:

```tsx
import { useColorScheme } from 'react-native';

const colorScheme = useColorScheme();  // 'light' | 'dark'

const themeColors = {
  background: colorScheme === 'dark' ? '#1B1B1D' : '#F7F7FB',
  text: colorScheme === 'dark' ? '#F7F7FB' : '#1B1B1D',
  card: colorScheme === 'dark' ? '#2C2C2E' : '#FFFFFF',
  // ...
};
```

**注意:** ダークモード対応は `src/theme/tokens.ts` のデザイントークンと連携して行うこと。

## 適用優先度

1. **必須**: プレスフィードバック（全ボタン）、アイコン置き換え（絵文字→Ionicons）
2. **推奨**: StatusBar管理、タッチターゲット最適化、プルトゥリフレッシュ
3. **任意**: 画面遷移アニメーション、スワイプバック、ダークモード

## ルール

- React Native の `Animated` API を優先する（`react-native-reanimated` は必要な場合のみ）
- `useNativeDriver: true` を必ず設定する（JS スレッドをブロックしない）
- 既存のデザイントークン (`src/theme/tokens.ts`) の値を使う
- アニメーションの duration は 200-400ms の範囲（iOS標準に合わせる）
- 新規パッケージの追加は最小限にする
- 変更はUIの見た目を壊さない範囲で行う
