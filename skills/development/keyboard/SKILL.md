---
name: keyboard
description: iPhoneでのキーボード操作を最適化する。TextInputのキーボード回避、閉じる操作、入力補助を実装する。「キーボード対応して」「入力画面を直して」「キーボードが被る」などのリクエストで使用する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [対象画面名 or 省略で全画面]
---

# キーボード最適化スキル

TextInput を含む画面に対して、iPhoneでの快適なキーボード操作を実装する。

## デザイン前提: Liquid Glass

本プロジェクトは `@callstack/liquid-glass` による Liquid Glass デザインを前提とする。
キーボード周りの実装では以下を考慮する:

- `LiquidGlassView` 内の `TextInput` は、ガラスエフェクトのブラーでプレースホルダーが見づらくなる可能性がある。テキストカラーに `PlatformColor('labelColor')` を使用する
- キーボード上部のアクセサリビュー（送信ボタン等）にも `LiquidGlassView` を適用し、ガラス質感を統一する
- フォールバック: `isLiquidGlassSupported` が `false` の場合は半透明背景に切り替える

## 対象ファイル

- `src/screens/**/*.tsx` — 画面コンポーネント
- `src/components/**/*.tsx` — フォーム系コンポーネント

引数が指定された場合はその画面のみ、省略時は TextInput を含む全画面を対象とする。

## 手順

### 1. 対象画面の特定

TextInput を含むファイルを検索する:
```
Grep: "TextInput" in src/screens/ and src/components/
```

### 2. KeyboardAvoidingView の適用

TextInput を含む画面のルートに `KeyboardAvoidingView` を追加する。

**パターン:**
```tsx
import { KeyboardAvoidingView, Platform } from 'react-native';

// 画面コンポーネントのルートに追加
<KeyboardAvoidingView
  style={{ flex: 1 }}
  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
>
  {/* 既存のコンテンツ */}
</KeyboardAvoidingView>
```

### 3. ScrollView の最適化

TextInput を含む ScrollView に以下を追加:
```tsx
<ScrollView
  keyboardShouldPersistTaps="handled"
  keyboardDismissMode="interactive"
  contentContainerStyle={{ flexGrow: 1 }}
>
```

### 4. TextInput の入力補助

各 TextInput に以下のプロパティを適切に設定する:

| 入力の種類 | returnKeyType | autoCapitalize | keyboardType | textContentType |
|-----------|---------------|----------------|--------------|-----------------|
| ユーザー名 | `next` or `done` | `none` | `default` | `username` |
| メール | `next` or `done` | `none` | `email-address` | `emailAddress` |
| パスワード | `done` | `none` | `default` | `password` / `newPassword` |
| 検索 | `search` | `none` | `default` | — |
| 複数行テキスト | `default` | `sentences` | `default` | — |

### 5. キーボード閉じる操作

- 単一フィールド: `onSubmitEditing={() => Keyboard.dismiss()}`
- 複数フィールド: `useRef` で次のフィールドにフォーカス移動
- 画面タップで閉じる: 必要に応じて `TouchableWithoutFeedback` + `Keyboard.dismiss()`

**複数フィールドのフォーカス移動パターン:**
```tsx
import { useRef } from 'react';
import { TextInput, Keyboard } from 'react-native';

const emailRef = useRef<TextInput>(null);
const passwordRef = useRef<TextInput>(null);

<TextInput
  placeholder="ユーザー名"
  returnKeyType="next"
  onSubmitEditing={() => emailRef.current?.focus()}
  blurOnSubmit={false}
/>
<TextInput
  ref={emailRef}
  placeholder="メールアドレス"
  returnKeyType="next"
  onSubmitEditing={() => passwordRef.current?.focus()}
  blurOnSubmit={false}
/>
<TextInput
  ref={passwordRef}
  placeholder="パスワード"
  returnKeyType="done"
  onSubmitEditing={() => Keyboard.dismiss()}
/>
```

### 6. パスワード入力の最適化

```tsx
<TextInput
  secureTextEntry={!showPassword}
  textContentType="password"
  autoComplete="password"
  autoCorrect={false}
/>
```

## ルール

- `Platform.OS` で iOS / Android を分岐し、`behavior` を適切に設定する
- 既存のレイアウト・スタイルを壊さない
- `keyboardVerticalOffset` はヘッダー高さに応じて調整する
- 新規パッケージのインストールは最小限にする（React Native 標準 API を優先）
- 変更後に TextInput のフォーカス・送信が正常に動作することを確認する
