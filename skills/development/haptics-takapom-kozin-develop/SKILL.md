---
name: haptics
description: iPhoneの触覚フィードバック（ハプティクス）をUIに追加する。「ハプティクス追加して」「触覚フィードバック」「タップ感を出して」などのリクエストで使用する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [対象画面名 or 省略で全画面]
---

# ハプティクス追加スキル

`expo-haptics` を使用して、iPhoneユーザーに適切な触覚フィードバックを提供する。

## デザイン前提: Liquid Glass

本プロジェクトは `@callstack/liquid-glass` による Liquid Glass デザインを前提とする。
ハプティクスとガラスエフェクトの連携:

- `LiquidGlassView` の `interactive` プロパティは、タッチ時にガラスの視覚アニメーションを発生させる。これに **ハプティクス（Light Impact）を同時に発火** させることで、視覚+触覚の統一的なフィードバックを実現する
- ガラスカードのタップ: `interactive={true}` + `Haptics.impactAsync(Light)` をセットで使う
- ガラス要素の `effect` 切り替え時（マテリアライズ/デマテリアライズ アニメーション）にも `Haptics.selectionAsync()` を付与する

## 前提条件

`expo-haptics` がインストールされていること。未インストールの場合は先にインストールする:
```bash
npx expo install expo-haptics
```

## 手順

### 1. 対象の特定

以下のインタラクティブ要素を含むファイルを検索する:
- `Pressable`, `TouchableOpacity`, `TouchableHighlight`
- `Switch`, `Slider`
- カスタムボタンコンポーネント

### 2. ハプティクスの種類と適用ルール

| 操作 | ハプティクスタイプ | 関数 |
|------|-------------------|------|
| 通常のボタンタップ | Light Impact | `Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)` |
| 重要なアクション（送信, 保存） | Medium Impact | `Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)` |
| タブ切り替え / セグメント選択 | Selection | `Haptics.selectionAsync()` |
| トグル（Switch）ON/OFF | Selection | `Haptics.selectionAsync()` |
| 成功（ログイン成功, 投稿完了） | Success Notification | `Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success)` |
| エラー（認証失敗, バリデーション） | Error Notification | `Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error)` |
| 警告（削除確認, 破壊的操作） | Warning Notification | `Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning)` |
| ロングプレス開始 | Heavy Impact | `Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy)` |

### 3. 実装パターン

**パターンA: Pressable のonPressに直接追加**
```tsx
import * as Haptics from 'expo-haptics';

<Pressable
  onPress={() => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    // 既存のonPress処理
    handlePress();
  }}
>
```

**パターンB: カスタムボタンコンポーネントに組み込み**
```tsx
import * as Haptics from 'expo-haptics';

interface Props {
  onPress: () => void;
  hapticStyle?: Haptics.ImpactFeedbackStyle;
  // ... 既存のprops
}

export const HapticButton: React.FC<Props> = ({
  onPress,
  hapticStyle = Haptics.ImpactFeedbackStyle.Light,
  ...rest
}) => {
  const handlePress = () => {
    Haptics.impactAsync(hapticStyle);
    onPress();
  };
  // ...
};
```

**パターンC: 非同期処理の成功/失敗時**
```tsx
const handleSubmit = async () => {
  try {
    await submitForm();
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
  } catch (error) {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
  }
};
```

### 4. 適用優先度

1. **必須**: 削除ボタン（Warning）、認証送信（Success/Error）
2. **推奨**: ナビゲーションボタン（Light）、タブバー（Selection）、いいねボタン（Light）
3. **任意**: 装飾的なプレス（例: カード選択）

## ルール

- ハプティクスは `onPress` の**先頭**で呼び出す（ユーザーが即座にフィードバックを感じるため）
- 非同期処理の結果に応じたフィードバックは処理**完了後**に呼び出す
- 過剰なハプティクスは避ける（スクロールや頻繁なイベントには付けない）
- Android では `expo-haptics` が自動的にフォールバックするため、Platform分岐は不要
- 既存のボタンコンポーネント（`GradientPillButton`, `OutlinePillButton`）がある場合は、そこに一括で組み込むことを優先する
- `import * as Haptics from 'expo-haptics'` の形式でインポートする
