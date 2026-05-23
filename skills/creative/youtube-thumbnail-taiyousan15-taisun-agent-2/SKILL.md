---
name: youtube-thumbnail
description: YouTube thumbnail creation guide
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
disable-model-invocation: true
---

# YouTubeサムネイル作成ガイド - NanoBanana Pro完全マニュアル

## 概要

| 項目 | 値 |
|------|-----|
| ツール | NanoBanana Pro (Gemini) + Canva |
| サイズ | 1280x720px（16:9） |
| 形式 | JPG/PNG |
| 目的 | クリック率（CTR）向上 |

---

## サムネイルの基本原則

### クリックされるサムネイルの要素

```
1. 視認性 - 小さくても内容がわかる
2. 感情 - 見た人の感情を動かす
3. 好奇心 - 「見たい」と思わせる
4. 一貫性 - チャンネルブランドの統一
5. 差別化 - 競合との違いを出す
```

### 避けるべきNG要素

```
❌ 文字が多すぎる（読めない）
❌ 色が地味（目立たない）
❌ 顔が小さい（感情が伝わらない）
❌ ごちゃごちゃしている（何の動画かわからない）
❌ クリックベイト（内容と違う）
```

---

## サムネイルのパターン

### パターン1: 人物フォーカス型

```
┌─────────────────────────────────┐
│                                 │
│  ┌─────┐                        │
│  │ 顔  │    【テキスト】         │
│  │表情 │     キャッチコピー      │
│  └─────┘                        │
│                                 │
└─────────────────────────────────┘

特徴:
- 人の顔が大きく入る
- 強い表情（驚き、喜び、困惑）
- テキストは右側または上部
```

### パターン2: Before/After型

```
┌─────────────────────────────────┐
│                                 │
│  Before    →    After          │
│  ┌────┐        ┌────┐          │
│  │ 😢 │        │ 😄 │          │
│  └────┘        └────┘          │
│                                 │
└─────────────────────────────────┘

特徴:
- 変化が一目でわかる
- 矢印や対比で視線誘導
- 数字を入れると効果的
```

### パターン3: テキスト主体型

```
┌─────────────────────────────────┐
│                                 │
│     【衝撃】                    │
│   これを知らないと              │
│     損します                    │
│                                 │
└─────────────────────────────────┘

特徴:
- 大きな文字
- 3行以内
- 背景はシンプルまたはグラデーション
```

### パターン4: 数字インパクト型

```
┌─────────────────────────────────┐
│                                 │
│        月収                     │
│      100万円                    │
│     達成した方法                │
│                                 │
└─────────────────────────────────┘

特徴:
- 数字を大きく
- 単位も明記
- 具体性を出す
```

---

## NanoBanana Pro プロンプト集

### 人物サムネイル生成

```
Create a YouTube thumbnail image.

Subject: Japanese [male/female] in [age]s
Expression: [Surprised/Shocked/Happy/Confused/Determined]
- Large, expressive face taking up 40-50% of frame
- Direct eye contact with camera
- [Specific expression details]

Background:
- [Solid color gradient / Blurred office / Abstract]
- High contrast with subject

Composition:
- Subject on [left/right] third
- Space for text on [opposite side]
- Clean, uncluttered

Style:
- High contrast, saturated colors
- Professional quality
- Eye-catching for small display

Technical:
- Size: 1280x720px
- No text in image
- Leave space for text overlay
```

**具体例（驚き表情）:**

```
Create a YouTube thumbnail image.

Subject: Japanese woman in her 30s, entrepreneur look
Expression: Extremely surprised/shocked
- Eyes wide open, eyebrows raised high
- Mouth slightly open in amazement
- Hand near face (optional)
- Taking up 50% of left side

Background:
- Gradient from dark blue (#1E3A5F) to lighter blue
- Subtle glow effect behind subject
- Professional, modern feel

Composition:
- Subject on left third
- Large empty space on right for text
- High contrast lighting on face

Style:
- Vibrant, eye-catching colors
- Japanese YouTube style
- Premium quality

Size: 1280x720px
No text - leave right side empty for text overlay.
```

**具体例（成功・達成表情）:**

```
Create a YouTube thumbnail image.

Subject: Confident Japanese businessman in 30s
Expression: Successful, proud smile
- Confident smirk/smile
- Arms crossed or thumbs up
- Professional attire (shirt, no tie)
- Looking directly at camera

Background:
- Modern office with growth chart visible
- Warm lighting suggesting success
- Blurred background (depth of field)

Composition:
- Subject on right third
- Space for big numbers on left
- Power pose framing

Style:
- Warm, inviting colors
- Success/wealth aesthetic
- Clean, professional

Size: 1280x720px
No text in image.
```

### Before/After サムネイル

```
Create a YouTube thumbnail showing transformation.

Split composition:
LEFT SIDE (Before):
- [Negative state description]
- Darker, desaturated colors
- Tired/frustrated expression

RIGHT SIDE (After):
- [Positive state description]
- Bright, vibrant colors
- Happy/successful expression

Divider:
- Clear visual separation (line or gradient)
- Arrow or transformation indicator space

Same person in both sides for authenticity.

Style:
- High contrast between before/after
- Dramatic lighting difference
- Japanese YouTube style

Size: 1280x720px
No text - leave space for "Before/After" labels.
```

### 背景のみ生成

```
Create a YouTube thumbnail background (no people).

Style: [選択]
□ Gradient - Blue to purple, modern tech feel
□ Office - Blurred modern workspace
□ Abstract - Geometric shapes, vibrant colors
□ Money/Success - Coins, graphs, luxury items
□ Problem - Dark, concerning atmosphere

Requirements:
- Space for subject on [left/right]
- Space for text on [opposite side]
- High contrast, eye-catching
- Not too busy or distracting

Size: 1280x720px
No text or people.
```

### アイコン・要素生成

```
Create a simple icon for YouTube thumbnail.

Icon type: [選択]
□ Arrow (pointing up/right)
□ Checkmark (success)
□ X mark (wrong/avoid)
□ Question mark (curiosity)
□ Exclamation mark (important)
□ Money symbol (yen/dollar)
□ Graph (growth)

Style:
- Bold, simple design
- Single color: [#22C55E green / #EF4444 red / #FBBF24 yellow]
- Clean edges
- Works at small size

Size: 500x500px
Transparent background (PNG).
```

---

## カラーパレット

### 高CTRカラー組み合わせ

| 組み合わせ | 背景 | テキスト | アクセント | 印象 |
|-----------|------|---------|----------|------|
| 信頼・ビジネス | #1E3A5F (紺) | #FFFFFF (白) | #22C55E (緑) | プロフェッショナル |
| 緊急・重要 | #DC2626 (赤) | #FFFFFF (白) | #FBBF24 (黄) | 注目・警告 |
| 成功・お金 | #065F46 (深緑) | #FBBF24 (金) | #FFFFFF (白) | 富・成功 |
| エネルギー | #F97316 (オレンジ) | #FFFFFF (白) | #1E3A5F (紺) | 活力・行動 |
| クール・テック | #7C3AED (紫) | #FFFFFF (白) | #22D3EE (シアン) | 革新・未来 |

### 避けるべき色

```
❌ パステルカラー（目立たない）
❌ 似た色の組み合わせ（コントラスト不足）
❌ 茶色系（古臭い印象）
❌ グレー単色（地味）
```

---

## テキスト追加ガイド

### フォント選定

| 用途 | 推奨フォント | 特徴 |
|------|-------------|------|
| メインコピー | ヒラギノ角ゴ StdN W8 | 太く視認性高い |
| インパクト | 源ノ角ゴシック Heavy | モダンで力強い |
| 数字 | Impact / Bebas Neue | 数字が目立つ |
| 補足 | Noto Sans JP Medium | 読みやすい |

### テキスト配置ルール

```
【3行以内】
- 1行目: フック（最も大きく）
- 2行目: サブコピー
- 3行目: 補足（小さめ）

【文字サイズ目安】
- メインコピー: 72-120pt
- サブコピー: 48-72pt
- 補足: 36-48pt

【装飾】
- 縁取り: 黒4-6px（白文字の場合）
- 影: ドロップシャドウ（控えめに）
- 背景: 半透明の帯（必要に応じて）
```

### 効果的なコピー例

```
【数字系】
「月収100万円」「たった3日で」「5つの方法」

【疑問系】
「なぜ○○は失敗するのか」「知ってた？」

【否定系】
「やってはいけない」「実は間違い」「損してます」

【煽り系】
「衝撃」「驚愕」「まだ○○してるの？」

【具体系】
「完全解説」「徹底比較」「プロが教える」
```

---

## 制作ワークフロー

### Step 1: 企画（5分）

```
1. 動画の内容を一言で表現
2. ターゲット視聴者を明確に
3. サムネイルのパターンを選択
4. キーワード/数字を決定
```

### Step 2: 画像生成（10分）

```
1. NanoBanana Proでベース画像を生成
2. 必要に応じて複数パターン生成
3. 最も良いものを選択
4. 背景や要素を追加生成（必要に応じて）
```

### Step 3: テキスト追加（10分）

```
1. Canvaにベース画像をアップロード
2. テキストを配置
3. フォント・色・サイズを調整
4. 縁取り・影を追加
5. バランスを確認
```

### Step 4: 確認・書き出し（5分）

```
1. 小さいサイズでプレビュー（実際の表示確認）
2. スマホでの見え方を確認
3. 競合のサムネイルと並べて比較
4. 1280x720px、JPG/PNGで書き出し
```

---

## A/Bテスト

### テスト要素

```
□ 表情の違い（驚き vs 笑顔）
□ 色の違い（暖色 vs 寒色）
□ テキストの違い（疑問形 vs 断定形）
□ レイアウトの違い（人物左 vs 人物右）
□ 数字の有無
```

### 評価指標

```
CTR（クリック率）目標:
- 新規チャンネル: 4-6%
- 成長チャンネル: 6-10%
- 人気チャンネル: 10%以上

改善サイクル:
1. 2パターン作成
2. 48時間後にCTR確認
3. 高い方を残す
4. 新しいパターンで再テスト
```

---

## ジャンル別テンプレート

### ビジネス・副業系

```
Create a YouTube thumbnail for business/side-hustle content.

Subject: Successful Japanese entrepreneur, 30s
- Confident expression
- Business casual attire
- Arms crossed or pointing gesture

Background:
- Modern office or home office
- Laptop and money/charts visible
- Professional lighting

Elements to include space for:
- Large yen amount (¥100万)
- "方法" or "秘密" text

Color scheme: Navy blue + Gold/Green accents
Size: 1280x720px
No text.
```

### ノウハウ・解説系

```
Create a YouTube thumbnail for tutorial/how-to content.

Subject: Friendly Japanese instructor, 30s
- Explaining gesture (pointing or open hands)
- Approachable smile
- Casual professional look

Background:
- Clean, minimal
- Whiteboard or screen visible
- Soft, even lighting

Elements:
- Space for numbered list (①②③)
- Space for topic keyword

Color scheme: Blue + White + Orange accent
Size: 1280x720px
No text.
```

### 比較・レビュー系

```
Create a YouTube thumbnail for comparison/review content.

Layout: Split screen or VS style

Elements:
- Two products/options visible
- Clear visual separation
- Space for VS or comparison text
- Reaction face (thinking or surprised)

Style:
- High contrast
- Clear product visibility
- Professional review aesthetic

Size: 1280x720px
No text.
```

---

## 品質チェックリスト

```
□ 小さいサイズ（120x68px）でも内容がわかる
□ 3秒で何の動画かわかる
□ 顔の表情がはっきり見える
□ テキストが読める
□ 背景がごちゃごちゃしていない
□ 色のコントラストが十分
□ チャンネルの他の動画と統一感がある
□ クリックベイトになっていない
□ 競合と差別化できている
□ スマホでの見え方を確認した
```
