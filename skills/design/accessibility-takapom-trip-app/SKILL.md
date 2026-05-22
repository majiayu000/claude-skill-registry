---
name: accessibility
description: iPhoneのVoiceOver対応を中心にアクセシビリティを改善する。「アクセシビリティ対応して」「VoiceOver対応」「a11y改善」などのリクエストで使用する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [対象画面名 or 省略で全画面]
---

# アクセシビリティ改善スキル

iPhoneの VoiceOver を中心に、アクセシビリティ対応を実装する。

## デザイン前提: Liquid Glass

本プロジェクトは `@callstack/liquid-glass` による Liquid Glass デザインを前提とする。
Liquid Glass はアクセシビリティ上の注意点が多い:

### ガラス上テキストのコントラスト確保
- ガラスの背景ブラーにより、テキストの可読性が低下しやすい
- `LiquidGlassView` の高さが **65px超** の場合、テキスト色の自動適応が効かない。`PlatformColor('labelColor')` を明示的に使用する
- WCAG AA 基準（コントラスト比 4.5:1 以上）を満たすよう、必要に応じてテキストに影 (`textShadowColor`) やフォントウェイトの増加で補完する

### 「透明度を下げる」設定への対応
```tsx
import { AccessibilityInfo } from 'react-native';
import { isLiquidGlassSupported } from '@callstack/liquid-glass';

const [reduceTransparency, setReduceTransparency] = useState(false);

useEffect(() => {
  AccessibilityInfo.isReduceTransparencyEnabled().then(setReduceTransparency);
  const sub = AccessibilityInfo.addEventListener(
    'reduceTransparencyChanged',
    setReduceTransparency,
  );
  return () => sub.remove();
}, []);

// reduceTransparency が true の場合、ガラスエフェクトを無効化し不透明背景にする
```

### フォールバック
- `isLiquidGlassSupported === false` または `reduceTransparency === true` の場合は、ガラスを使わず十分なコントラストを持つ不透明背景を提供する

## 対象ファイル

- `src/screens/**/*.tsx` — 画面コンポーネント
- `src/components/**/*.tsx` — UIコンポーネント

引数が指定された場合はその画面のみ、省略時は全ファイルを対象とする。

## 手順

### 1. 対象要素の特定

以下の要素を検索し、アクセシビリティ属性の有無を確認する:
- `Pressable`, `TouchableOpacity`, `TouchableHighlight` — ボタン系
- `Image` — 画像
- `TextInput` — 入力フィールド
- `Switch` — トグル
- `Text`（見出し相当） — ヘッダー

### 2. アクセシビリティ属性の適用ルール

#### ボタン / Pressable

```tsx
<Pressable
  accessibilityRole="button"
  accessibilityLabel="戻る"           // VoiceOverが読み上げるテキスト
  accessibilityHint="前の画面に戻ります"  // 操作の結果を説明（任意）
  onPress={handleBack}
>
  <ChevronIcon />
</Pressable>
```

| 要素の種類 | accessibilityRole | accessibilityLabel の指針 |
|-----------|-------------------|--------------------------|
| 通常ボタン | `button` | アクションを示す動詞（「保存する」「送信する」） |
| リンクボタン | `link` | 遷移先を示す（「設定を開く」） |
| 戻るボタン | `button` | 「戻る」 |
| アイコンボタン | `button` | アイコンの意味（「設定」「メニュー」） |
| いいねボタン | `button` | 状態を含む（「いいね、現在5件」） |
| タブバー項目 | `tab` | タブ名（「ホーム」「通知」「設定」） |
| 画像 | `image` | 画像の内容を説明する簡潔なテキスト |
| 装飾的画像 | — | `accessible={false}` を設定 |
| 入力フィールド | — | `accessibilityLabel` でフィールド名 |
| トグル | `switch` | 設定名と現在の状態 |
| 見出しテキスト | `header` | — （Text内容が自動で読まれる） |

#### 画像

```tsx
// 意味のある画像
<Image
  source={{ uri: postImageUrl }}
  accessibilityRole="image"
  accessibilityLabel="投稿画像: カフェの外観写真"
/>

// 装飾的な画像（VoiceOverでスキップ）
<Image
  source={decorativeBlob}
  accessible={false}
/>
```

#### TextInput

```tsx
<TextInput
  accessibilityLabel="メールアドレス"
  accessibilityHint="ログイン用のメールアドレスを入力してください"
  placeholder="example@mail.com"
/>
```

#### 見出し

```tsx
<Text
  accessibilityRole="header"
  style={styles.sectionTitle}
>
  基本情報
</Text>
```

#### 状態を持つ要素

```tsx
// いいねボタンの例
<Pressable
  accessibilityRole="button"
  accessibilityLabel={`いいね、現在${likesCount}件`}
  accessibilityState={{ selected: isLiked }}
  onPress={handleLike}
>
```

### 3. グループ化

関連する要素をまとめて1つの VoiceOver 項目にする:

```tsx
// カードをグループ化
<View
  accessible={true}
  accessibilityRole="button"
  accessibilityLabel={`${hirobaTitle}、メンバー${memberCount}人、投稿${postCount}件`}
>
  <Text>{hirobaTitle}</Text>
  <Text>{memberCount}人</Text>
  <Text>{postCount}件</Text>
</View>
```

### 4. 読み上げ順序

重要な情報が先に読まれるよう、必要に応じて `accessibilityElementsHidden` や `importantForAccessibility` を使用:

```tsx
// 装飾要素をVoiceOverから除外
<View accessibilityElementsHidden={true}>
  <DecorativeBackground />
</View>
```

### 5. 絵文字アイコンの対応

絵文字をアイコンとして使用している箇所に `accessibilityLabel` を追加:

```tsx
// Before
<Text>🏠</Text>

// After
<Text accessible={false}>🏠</Text>
// 親要素に accessibilityLabel を設定
```

## ルール

- `accessibilityLabel` は簡潔に、スクリーンリーダーで自然に聞こえる日本語にする
- 装飾的な要素（背景画像、区切り線等）は `accessible={false}` で除外する
- 動的な値（カウント、状態）を含むラベルは変数で構築する
- `accessibilityHint` は必須ではない。操作結果が自明でない場合のみ追加する
- 既存の `accessibilityRole="button"` は維持し、`accessibilityLabel` が未設定の場合のみ追加する
- テスト: 変更後「VoiceOverで全画面を操作できるか」を基準とする
