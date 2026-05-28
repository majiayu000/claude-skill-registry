---
name: ios-ux-audit
description: iPhoneユーザー向けのUX監査を実行し、問題点と改善案をレポートする。「UX監査して」「iOS UXチェック」「画面を監査」などのリクエストで使用する。
allowed-tools: Read, Glob, Grep
argument-hint: [対象画面名 or 省略で全画面]
---

# iOS UX 監査スキル

指定された画面（または全画面）を走査し、iPhoneユーザーのUX品質を監査する。

## デザイン前提: Liquid Glass

本プロジェクトは Apple iOS 26 の **Liquid Glass** デザインを前提とする。
監査時は `@callstack/liquid-glass` (`LiquidGlassView`, `LiquidGlassContainerView`) の使用状況も確認する。

## 監査対象

対象ファイル:
- `src/screens/**/*.tsx` — 画面コンポーネント
- `src/components/**/*.tsx` — UIコンポーネント
- `src/App.tsx` — ナビゲーション構造

引数が指定された場合はその画面のみ、省略時は全画面を対象とする。

## 監査チェックリスト

以下の7カテゴリを順にチェックし、問題があれば具体的なファイル名・行番号と改善案を報告する。

### 1. Safe Area & デバイス対応

- [ ] `SafeAreaView` がルートで使用されているか
- [ ] ノッチ / Dynamic Island 領域に要素が被っていないか
- [ ] ホームインジケータ領域（画面下部）にボタン等が被っていないか
- [ ] `useSafeAreaInsets()` で動的にパディングを取得しているか
- [ ] ステータスバーのスタイル（`light` / `dark`）が背景色と適切か

### 2. キーボード処理

- [ ] `TextInput` を含む画面に `KeyboardAvoidingView` があるか（iOS: `behavior="padding"`）
- [ ] `ScrollView` に `keyboardShouldPersistTaps="handled"` が設定されているか
- [ ] `returnKeyType` が適切に設定されているか（`done`, `next`, `search` 等）
- [ ] キーボードを閉じる手段があるか（`Keyboard.dismiss()` 等）

### 3. ハプティクス

- [ ] ボタンのプレスに触覚フィードバックがあるか
- [ ] 破壊的アクション（削除等）に `notificationAsync(Warning)` があるか
- [ ] タブ切り替え・トグルに `selectionAsync()` があるか
- [ ] 成功・完了時に `notificationAsync(Success)` があるか

### 4. アクセシビリティ

- [ ] すべての `Pressable` / `TouchableOpacity` に `accessibilityLabel` があるか
- [ ] アイコンのみのボタンに `accessibilityLabel` があるか
- [ ] 画像に `accessibilityLabel` または `accessible={false}`（装飾的）があるか
- [ ] `accessibilityRole` が適切に設定されているか（`button`, `link`, `header` 等）
- [ ] 絵文字アイコンがアクセシビリティラベルで補完されているか

### 5. パフォーマンス

- [ ] リスト表示に `FlatList` / `SectionList` を使っているか（`.map()` ではなく）
- [ ] 画像に適切な `resizeMode` と遅延読み込みがあるか
- [ ] 不要な再レンダリングを防ぐ `React.memo` / `useMemo` / `useCallback` があるか
- [ ] `key` prop に配列のインデックスではなく一意のIDを使っているか

### 6. iOS HIG 準拠

- [ ] 絵文字ではなくアイコンライブラリ（`@expo/vector-icons` 等）を使っているか
- [ ] 戻るボタンがiOS標準のシェブロン（`<`）スタイルか
- [ ] モーダル/シート表示が適切か（設定画面等）
- [ ] タッチターゲットが最低44x44ptあるか
- [ ] フォントサイズがiOSの推奨範囲内か（本文: 17pt, キャプション: 12pt以上）

### 7. Liquid Glass デザイン準拠

- [ ] カード・ツールバー・モーダルに `LiquidGlassView` が適用されているか
- [ ] 近接するガラス要素が `LiquidGlassContainerView` でグループ化されているか
- [ ] `effect` プロパティが適切か（カード: `regular`, オーバーレイ: `clear`）
- [ ] ガラス背景上のテキストが十分なコントラストを持つか（WCAG AA以上）
- [ ] `isLiquidGlassSupported` で非対応デバイスにフォールバックがあるか
- [ ] フォールバック時に半透明背景色（例: `rgba(255,255,255,0.8)`）が設定されているか
- [ ] 全画面ガラス背景を避け、アクセント的に使用しているか
- [ ] ガラス要素に `borderRadius` が設定されているか
- [ ] 「透明度を下げる」設定 (`AccessibilityInfo`) を尊重しているか
- [ ] ガラス要素の高さが65px超の場合、テキストに `PlatformColor('labelColor')` を使用しているか

### 8. ジェスチャー & インタラクション

- [ ] スワイプバック（←方向）でナビゲーション戻りができるか
- [ ] リストにプルトゥリフレッシュ (`RefreshControl`) があるか
- [ ] ロングプレスでコンテキストメニューが出るか（必要な箇所）
- [ ] ボタンにプレス状態のフィードバック（opacity/scale）があるか

## 出力フォーマット

```
## iOS UX 監査レポート

### 対象: [画面名 or 全画面]

#### 🔴 Critical（即座に修正すべき）
- **[カテゴリ]** `ファイル名:行番号` — 問題の説明
  → 改善案: ...

#### 🟡 Warning（改善推奨）
- **[カテゴリ]** `ファイル名:行番号` — 問題の説明
  → 改善案: ...

#### 🟢 Good（問題なし）
- [カテゴリ]: ✓ 適切に実装済み

#### 📊 スコア: X / 8 カテゴリ合格
```

## ルール

- コードの変更は行わない。監査とレポートのみ
- 問題箇所は必ずファイルパスと行番号を含める
- 改善案は具体的なコード例を含める
- プロジェクトの `src/theme/tokens.ts` のデザイントークンを考慮する
- 既存の依存パッケージで対応可能な改善を優先する
