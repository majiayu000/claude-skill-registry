---
name: custom-character
description: |
  既存キャラクター画像を使用した一貫性のあるマーケティング素材制作ガイド。
  Use when: (1) user says「キャラクター設定」「同じキャラで」「キャラ一貫性」,
  (2) user wants consistent character across multiple images,
  (3) user mentions「表情バリエーション」「ポーズ違い」.
  Do NOT use for: ゼロからのキャラ生成（nanobanana-proを使用）、
  アニメ動画制作（anime-productionを使用）。
---

# カスタムキャラクターガイド

## 概要
既存のキャラクター画像を使用して、一貫性のあるマーケティング素材を制作する方法。

---

## カスタムキャラクター対応機能

### できること
- 既存キャラ画像をベースに新規シーン生成
- 表情バリエーションの追加
- 異なるポーズ・背景での展開
- アニメ/漫画スタイルへの変換

### 制限事項
- 完全な再現は困難（類似度80%程度）
- 複雑なデザインは簡略化される場合あり
- 著作権のある画像は使用不可

---

## 使用方法

### Step 1: 参照画像の準備

**推奨画像条件**:
- 解像度: 512x512px以上
- 背景: 単色または透過
- 構図: 正面または斜め45度
- 照明: 均一、影少なめ

### Step 2: キャラクター分析プロンプト

まず、キャラクターの特徴を言語化:

```
このキャラクターの特徴を教えてください:
- 性別・年齢層
- 髪型・髪色
- 服装
- 特徴的なアクセサリー
- 全体の雰囲気
```

### Step 3: 再現プロンプト作成

分析結果をプロンプトに変換:

```
[Style] style character,
[Gender] in their [age]s,
[hair description],
[clothing description],
[accessories],
[overall vibe/atmosphere]
```

---

## キャラクタープロンプト例

### ビジネスパーソン（男性）
```
Manga style Japanese businessman,
male in his 30s,
short black hair, neat side part,
wearing navy suit, white shirt, red tie,
confident expression,
professional appearance
```

### ビジネスパーソン（女性）
```
Manga style Japanese businesswoman,
female in her late 20s,
shoulder length brown hair,
wearing gray blazer, white blouse,
friendly smile,
modern professional look
```

### 講師キャラクター
```
Anime style Japanese instructor,
male in his 40s,
slightly graying hair, glasses,
wearing casual blazer, open collar shirt,
wise and approachable expression,
mentor figure appearance
```

---

## 表情バリエーション

同じキャラクターで異なる表情を生成:

### ベースプロンプト + 表情指定

| 表情 | 追加プロンプト |
|------|---------------|
| 通常 | neutral expression, calm face |
| 笑顔 | happy smile, bright eyes, cheerful |
| 驚き | shocked expression, wide eyes, open mouth |
| 悲しみ | sad expression, downcast eyes, teary |
| 怒り | angry expression, furrowed brows |
| 決意 | determined look, confident eyes |
| 困惑 | confused expression, tilted head |
| 照れ | embarrassed, blushing cheeks |

---

## ポーズバリエーション

### 説明ポーズ
```
[character base prompt],
explaining gesture,
one hand raised, pointing finger,
standing pose, slight lean forward
```

### 喜びポーズ
```
[character base prompt],
celebration pose,
both arms raised, jumping,
dynamic pose, motion blur
```

### 思考ポーズ
```
[character base prompt],
thinking pose,
hand on chin, looking up,
thoughtful expression
```

### プレゼンポーズ
```
[character base prompt],
presentation pose,
standing next to whiteboard,
gesturing to content
```

---

## 背景設定

### オフィス
```
modern Japanese office background,
desk with computer, plants,
large windows, city view,
clean professional environment
```

### 自宅
```
cozy Japanese home interior,
living room setting,
warm lighting, comfortable furniture,
relaxed atmosphere
```

### セミナー会場
```
seminar room background,
rows of chairs, projector screen,
professional conference setting
```

### 抽象背景
```
abstract gradient background,
[color scheme] colors,
subtle geometric patterns,
no distracting elements
```

---

## キャラクターシート作成

新キャラクター使用時は、まずシートを作成:

```
Character reference sheet,
[full character description],
multiple views: front, side, 3/4 view,
expression chart: happy, sad, angry, surprised,
clean white background,
anime/manga style
```

---

## 一貫性維持のコツ

### 1. シードの固定
同じシードを使用することで類似性向上。

### 2. 詳細な特徴記述
曖昧な表現を避け、具体的に記述:
- ❌ 「髪が長い」
- ✅ 「肩まで届く黒いストレートヘア、前髪は眉上」

### 3. 参照画像の併用
Image-to-Image機能がある場合は積極的に活用。

### 4. 同一セッション内生成
可能な限り、同じセッションで連続生成。

---

## トラブルシューティング

### キャラが別人になる
→ 特徴をより具体的に記述
→ 参照画像を追加で説明

### 服装が変わる
→ 服装の詳細を毎回記述
→ 「same outfit as reference」追加

### 年齢が変わる
→ 年齢を数値で指定
→ 肌や顔の特徴を追加

---

## 著作権注意事項

### 使用可能
- 自分で作成したオリジナルキャラ
- 商用利用可能な素材
- 著作権フリーの画像

### 使用不可
- 他者の著作物（漫画、アニメキャラ等）
- 有名人の肖像
- ライセンス不明の画像

---

## 実践ワークフロー

1. **キャラクター設計**
   - ペルソナに合わせた特徴決定
   - 基本プロンプト作成

2. **シート生成**
   - 参照用キャラクターシート生成
   - 特徴の微調整

3. **シーン展開**
   - 必要なシーン用画像を生成
   - 表情・ポーズを適宜変更

4. **確認・調整**
   - 一貫性の確認
   - 必要に応じて再生成
