---
name: figma
description: Figmaからデザインデータを取得し、React Nativeコンポーネントやデザイントークンに変換する。「Figmaからデザインを取って」「Figmaのカラーを抽出して」「Figmaのコンポーネントをコードにして」などのリクエストで使用する。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
argument-hint: [FigmaファイルURL または操作内容]
---

# Figma デザイン取得・変換スキル

Figma からデザインデータを取得し、React Native のコードやデザイントークンに変換する。

## 連携方法

### 方法 1: Figma REST API

Figma Personal Access Token を使って REST API 経由でデザインデータを取得する。

**必要な環境変数:**
- `FIGMA_ACCESS_TOKEN` — Figma の Personal Access Token（Settings → Account → Personal access tokens で発行）

**API エンドポイント:**

```bash
# ファイル全体の情報を取得
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/{file_key}"

# 特定ノードの情報を取得
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}"

# 画像をエクスポート
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=png&scale=2"

# コンポーネント一覧を取得
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/{file_key}/components"

# スタイル一覧を取得
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/{file_key}/styles"

# ローカル変数（デザイントークン）を取得
curl -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  "https://api.figma.com/v1/files/{file_key}/variables/local"
```

**Figma URL からのキー抽出:**
- ファイル URL: `https://www.figma.com/design/{file_key}/{file_name}` → `{file_key}` を取得
- ノード URL: `?node-id={node_id}` クエリパラメータから取得（`-` を `:` に変換）

### 方法 2: Figma MCP Server

Claude の MCP 設定に Figma MCP Server が追加されている場合、MCP ツール経由で直接 Figma にアクセスする。

MCP が利用可能な場合は API より MCP を優先して使う。

## 操作モード

### モード A: デザイントークン抽出

Figma のスタイルや変数からデザイントークン（カラー、タイポグラフィ、スペーシング）を抽出し、TypeScript の定数ファイルに変換する。

**出力先:** `src/constants/`

**カラートークンの例:**
```typescript
// src/constants/colors.ts
export const Colors = {
  primary: '#6366F1',
  primaryLight: '#A5B4FC',
  primaryDark: '#4338CA',
  secondary: '#EC4899',
  background: '#FFFFFF',
  surface: '#F9FAFB',
  text: '#111827',
  textSecondary: '#6B7280',
  border: '#E5E7EB',
  error: '#EF4444',
  success: '#22C55E',
  warning: '#F59E0B',
} as const;

export type ColorKey = keyof typeof Colors;
```

**タイポグラフィトークンの例:**
```typescript
// src/constants/typography.ts
import { TextStyle } from 'react-native';

export const Typography: Record<string, TextStyle> = {
  h1: { fontSize: 32, fontWeight: '700', lineHeight: 40 },
  h2: { fontSize: 24, fontWeight: '700', lineHeight: 32 },
  h3: { fontSize: 20, fontWeight: '600', lineHeight: 28 },
  body: { fontSize: 16, fontWeight: '400', lineHeight: 24 },
  bodySmall: { fontSize: 14, fontWeight: '400', lineHeight: 20 },
  caption: { fontSize: 12, fontWeight: '400', lineHeight: 16 },
} as const;
```

**スペーシングトークンの例:**
```typescript
// src/constants/spacing.ts
export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
} as const;

export const BorderRadius = {
  sm: 4,
  md: 8,
  lg: 16,
  full: 9999,
} as const;
```

### モード B: コンポーネント変換

Figma のフレームやコンポーネントを React Native コンポーネントコードに変換する。

**手順:**

1. Figma API / MCP でノードのデザインデータ（レイアウト、色、フォント、サイズ等）を取得する
2. Figma の Auto Layout を React Native の `flexDirection`, `gap`, `padding` にマッピングする
3. デザイントークンが `src/constants/` に存在すればそれを参照する
4. `src/components/` にコンポーネントファイルを生成する

**Figma → React Native マッピング:**

| Figma プロパティ | React Native スタイル |
|---|---|
| Auto Layout (horizontal) | `flexDirection: 'row'` |
| Auto Layout (vertical) | `flexDirection: 'column'` |
| Spacing between items | `gap: number` |
| Padding | `padding`, `paddingHorizontal`, `paddingVertical` |
| Fill container | `flex: 1` |
| Fixed size | `width` / `height` |
| Corner radius | `borderRadius` |
| Fill (solid color) | `backgroundColor` |
| Stroke | `borderWidth`, `borderColor` |
| Drop shadow | `shadowColor`, `shadowOffset`, `shadowOpacity`, `shadowRadius`, `elevation` |
| Text properties | `fontSize`, `fontWeight`, `lineHeight`, `color`, `textAlign` |
| Opacity | `opacity` |

## 手順（共通）

1. ユーザーから Figma URL またはファイルキーを受け取る
2. URL から `file_key` と `node_id` を抽出する
3. 環境変数 `FIGMA_ACCESS_TOKEN` の存在を確認する（なければ設定方法を案内する）
4. MCP が利用可能か確認し、可能なら MCP を使う
5. 指定されたモード（トークン抽出 / コンポーネント変換）を実行する
6. 生成したファイルの内容をユーザーに報告する

## ルール

- Figma の色は RGBA → HEX に変換する（Figma API は 0〜1 の float で返す）
- フォントファミリーは Expo で利用可能なものに置き換える（`expo-font` で読み込み前提）
- `px` 値はそのまま React Native の数値として使う（React Native は dp ベース）
- 画像アセットは `assets/` ディレクトリにエクスポートする
- 既存のデザイントークンファイルがあれば上書きではなくマージする
- `FIGMA_ACCESS_TOKEN` をコードやログに直接記載しない
