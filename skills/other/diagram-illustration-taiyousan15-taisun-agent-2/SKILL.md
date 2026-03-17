---
name: diagram-illustration
description: |
  図解・インフォグラフィック・解説イラスト制作ガイド。NanoBanana Pro使用。
  Use when: (1) user says「図解を作って」「インフォグラフィック」「解説画像」,
  (2) user wants visual explanations for content,
  (3) user mentions「フロー図」「比較図」「構造図」.
  Do NOT use for: 人物画像生成（nanobanana-proを使用）、
  サムネイル作成（youtube-thumbnailを使用）。
---

# 図解・解説画像制作ガイド - NanoBanana Pro完全マニュアル

## 概要

| 項目 | 値 |
|------|-----|
| ツール | NanoBanana Pro (Gemini) |
| 用途 | Kindle本・note記事・ブログ・SNS |
| 形式 | 図解・インフォグラフィック・解説イラスト |

---

## 図解の種類

### 1. フロー図（プロセス説明）

```
┌────┐    ┌────┐    ┌────┐    ┌────┐
│ A  │ → │ B  │ → │ C  │ → │ D  │
└────┘    └────┘    └────┘    └────┘
  ↓         ↓         ↓         ↓
説明1     説明2     説明3     説明4
```

**用途**: 手順、プロセス、時系列の説明

### 2. 比較図（Before/After、対比）

```
┌─────────────┬─────────────┐
│   Before    │    After    │
├─────────────┼─────────────┤
│  ❌ 悪い例  │  ✅ 良い例  │
│  ・項目1   │  ・項目1    │
│  ・項目2   │  ・項目2    │
└─────────────┴─────────────┘
```

**用途**: 変化、改善、選択肢の比較

### 3. 構造図（階層・関係性）

```
        ┌─────────┐
        │  中心   │
        └────┬────┘
    ┌────────┼────────┐
    ↓        ↓        ↓
┌─────┐  ┌─────┐  ┌─────┐
│要素1│  │要素2│  │要素3│
└─────┘  └─────┘  └─────┘
```

**用途**: 組織、概念の構造、関係性

### 4. リスト図（ポイント列挙）

```
┌─────────────────────────────┐
│    【タイトル】              │
├─────────────────────────────┤
│ ① ポイント1                 │
│ ② ポイント2                 │
│ ③ ポイント3                 │
│ ④ ポイント4                 │
│ ⑤ ポイント5                 │
└─────────────────────────────┘
```

**用途**: 重要ポイント、チェックリスト、まとめ

### 5. サイクル図（循環プロセス）

```
      ┌─────┐
      │  A  │
      └──┬──┘
    ↗    │    ↘
┌─────┐  ↓  ┌─────┐
│  D  │←───→│  B  │
└─────┘     └─────┘
    ↖    ↓    ↙
      ┌─────┐
      │  C  │
      └─────┘
```

**用途**: PDCAサイクル、継続的プロセス

### 6. ファネル図（段階的絞り込み）

```
┌─────────────────────────┐
│        認知 1000人       │
└───────────┬─────────────┘
    ┌───────┴───────┐
    │   興味 500人   │
    └───────┬───────┘
        ┌───┴───┐
        │検討200│
        └───┬───┘
          ┌─┴─┐
          │50人│
          └───┘
```

**用途**: マーケティングファネル、コンバージョン

---

## NanoBanana Pro プロンプト集

### 基本プロンプト構造

```
Create an infographic illustration for [Kindle book / blog article].

Topic: [トピック]
Type: [Flow chart / Comparison / Structure / List / Cycle / Funnel]

Content to visualize:
1. [要素1]
2. [要素2]
3. [要素3]
...

Style:
- Clean, modern flat design
- Color scheme: [カラー]
- Japanese business/educational style
- Simple icons and shapes
- Easy to understand at a glance

Technical:
- Size: [1200x800px / 800x1200px / 1080x1080px]
- Background: [White / Light gray / Color]
- No text in image (leave label spaces empty)
```

### フロー図プロンプト

```
Create a flow chart infographic.

Process: [プロセス名]

Steps (left to right):
Step 1: [内容] - Icon: [アイコン説明]
Step 2: [内容] - Icon: [アイコン説明]
Step 3: [内容] - Icon: [アイコン説明]
Step 4: [内容] - Icon: [アイコン説明]

Connecting elements:
- Arrows between steps
- Progress indication

Style:
- Horizontal flow (left to right)
- Each step in rounded rectangle
- Consistent icon style
- Color scheme: Blue (#1E3A5F) + Green (#22C55E) accent

Size: 1200x600px
Background: White
Leave text labels empty for later addition.
```

**具体例（マーケティングファネル）:**

```
Create a flow chart infographic.

Process: Marketing automation funnel

Steps (left to right):
Step 1: Content creation - Icon: Document/video
Step 2: Lead capture - Icon: Magnet/form
Step 3: Email nurturing - Icon: Email sequence
Step 4: Sales conversion - Icon: Shopping cart/money

Connecting elements:
- Curved arrows between steps
- Funnel visualization

Style:
- Modern, clean design
- Color gradient from blue to green
- Simple, recognizable icons
- Professional Japanese style

Size: 1200x600px
Background: Light gray (#F8FAFC)
No text - leave label areas empty.
```

### 比較図プロンプト

```
Create a comparison infographic.

Comparison: [比較タイトル]

LEFT SIDE (Before/Option A):
- Header: [ヘッダー]
- Items:
  1. [項目1] - negative indicator
  2. [項目2] - negative indicator
  3. [項目3] - negative indicator
- Mood: [Negative/Neutral]
- Color: [Gray/Red tones]

RIGHT SIDE (After/Option B):
- Header: [ヘッダー]
- Items:
  1. [項目1] - positive indicator
  2. [項目2] - positive indicator
  3. [項目3] - positive indicator
- Mood: [Positive]
- Color: [Green/Blue tones]

Divider: Clear vertical line or VS symbol
Arrow or transformation indicator in center (optional)

Style:
- Clear visual contrast between sides
- Check marks (✓) and X marks (✗) for items
- Clean, modern design

Size: 1200x800px
Background: White
No text - leave all label areas empty.
```

**具体例（労働集約 vs 自動化）:**

```
Create a comparison infographic.

Comparison: Working style comparison

LEFT SIDE (Traditional):
- Person looking tired at desk
- Clock showing long hours
- Scattered papers, chaos
- Red/gray color tone
- Downward trend arrow

RIGHT SIDE (Automated):
- Relaxed person with laptop
- Clock showing short hours
- Organized, clean workspace
- Green/blue color tone
- Upward trend arrow

Center: Clear transformation arrow

Style:
- Dramatic contrast
- Simple icon-based illustrations
- Japanese business style
- Clean, professional

Size: 1200x800px
Background: White
No text.
```

### 構造図プロンプト

```
Create a structure/hierarchy infographic.

Topic: [トピック]

Structure:
CENTER: [中心要素]

BRANCHES (surrounding center):
1. [要素1] - [簡単な説明]
2. [要素2] - [簡単な説明]
3. [要素3] - [簡単な説明]
4. [要素4] - [簡単な説明]
(Add more as needed)

Layout: [Radial / Tree / Mind map]
Connections: Lines or arrows from center to branches

Style:
- Clean, organized layout
- Consistent shape for each element
- Color coding for different categories
- Simple icons for each branch

Size: 1080x1080px
Background: White
No text - leave label areas empty.
```

### リスト図プロンプト

```
Create a numbered list infographic.

Title area: [タイトル用スペース]

List items (5 items):
1. [項目1] - Icon: [アイコン]
2. [項目2] - Icon: [アイコン]
3. [項目3] - Icon: [アイコン]
4. [項目4] - Icon: [アイコン]
5. [項目5] - Icon: [アイコン]

Layout:
- Vertical list
- Number prominently displayed
- Icon to the left of each item
- Space for text on right

Style:
- Clean, scannable design
- Alternating background for rows (optional)
- Consistent icon style
- Color scheme: [指定色]

Size: 800x1200px (vertical)
Background: [White / Gradient]
No text - leave description areas empty.
```

### サイクル図プロンプト

```
Create a cycle diagram infographic.

Cycle: [サイクル名]

Stages (clockwise):
1. [ステージ1] - Icon: [アイコン] - Color: [色1]
2. [ステージ2] - Icon: [アイコン] - Color: [色2]
3. [ステージ3] - Icon: [アイコン] - Color: [色3]
4. [ステージ4] - Icon: [アイコン] - Color: [色4]

Center element: [中心のテキスト/アイコン用スペース]

Connecting arrows: Curved arrows between stages (clockwise)

Style:
- Circular layout
- Each stage in pie slice or node
- Smooth arrow transitions
- Gradient or distinct colors per stage

Size: 1080x1080px
Background: White
No text - leave labels empty.
```

### ファネル図プロンプト

```
Create a funnel infographic.

Funnel stages (top to bottom):
1. [最上部] - Width: 100% - Color: [色1]
2. [第2層] - Width: 70% - Color: [色2]
3. [第3層] - Width: 50% - Color: [色3]
4. [第4層] - Width: 30% - Color: [色4]
5. [最下部] - Width: 15% - Color: [色5]

Side annotations: Space for percentages and labels

Style:
- 3D funnel effect (optional)
- Gradient from wide to narrow
- Clear separation between stages
- Numbers/stats area on sides

Size: 800x1000px
Background: White or light gradient
No text - leave label areas empty.
```

---

## Kindle本用図解

### 章の導入図解

```
Create a chapter introduction infographic for Kindle book.

Chapter topic: [章のトピック]

Elements:
- Chapter number indicator (large)
- Topic icon (central)
- 3-4 key points to be covered (surrounding)
- Visual hierarchy showing chapter structure

Style:
- Book-appropriate design
- Readable on e-reader (high contrast)
- Simple, not too detailed
- Monochrome-friendly (for e-ink displays)

Size: 1400x800px
Background: White
No text - leave all labels empty.
```

### 概念説明図解

```
Create a concept explanation infographic for Kindle book.

Concept: [概念名]

Visual explanation:
- Main concept in center
- Related elements around it
- Arrows showing relationships
- Simple metaphor/analogy visualization

Style:
- Educational, clear
- Works in grayscale (for e-ink)
- High contrast elements
- Simple icons and shapes

Size: 1200x900px
Background: White
No text.
```

### まとめ図解

```
Create a chapter summary infographic for Kindle book.

Summary of: [章/セクション名]

Key takeaways (3-5 points):
1. [ポイント1] - Icon
2. [ポイント2] - Icon
3. [ポイント3] - Icon
4. [ポイント4] - Icon
5. [ポイント5] - Icon

Layout: Clean list or grid format
Visual: Checkmarks or numbered badges

Style:
- Summary/recap feel
- Quick reference design
- High contrast for e-readers
- Clean, minimal

Size: 1200x800px
Background: White
No text - leave point descriptions empty.
```

---

## note記事用図解

### アイキャッチ図解

```
Create an eye-catching header infographic for blog article.

Article topic: [記事トピック]

Elements:
- Main visual metaphor for topic
- Engaging, curiosity-inducing design
- Space for title overlay
- Professional, modern aesthetic

Style:
- Blog/social media ready
- Vibrant colors
- Clean composition
- Japanese web design style

Size: 1200x630px (OGP size)
Background: Gradient or solid color
No text.
```

### 本文中の説明図解

```
Create an explanatory infographic for blog article.

Explaining: [説明内容]

Type: [Flow / Comparison / List / Structure]

Content:
[具体的な内容をリスト]

Style:
- Web-optimized design
- Mobile-friendly (readable on small screens)
- Colorful but professional
- Matches article tone

Size: 1080x1080px (square for versatility)
Background: White or light
No text - leave labels empty.
```

### SNS共有用図解

```
Create a shareable infographic for social media.

Topic: [トピック]

Key message: [伝えたいこと]

Design:
- Instantly understandable
- Share-worthy visual
- Brand colors: [カラー]
- Clean, impactful

Formats needed:
- Instagram/note: 1080x1080px
- Twitter: 1200x675px
- Story: 1080x1920px

Style:
- Bold, eye-catching
- Minimal text areas
- Strong visual hierarchy
- Japanese SNS style

Background: [指定色]
No text in image.
```

---

## カラーパレット

### ビジネス・教育系

| 用途 | プライマリ | セカンダリ | アクセント |
|------|-----------|-----------|----------|
| 信頼・専門性 | #1E3A5F | #64748B | #22C55E |
| 成長・成功 | #065F46 | #10B981 | #FBBF24 |
| 革新・テック | #4F46E5 | #818CF8 | #22D3EE |
| 温かみ・親しみ | #9A3412 | #FB923C | #FDE047 |

### 状態表現

| 状態 | 色 | Hex |
|------|-----|-----|
| ポジティブ/成功 | 緑 | #22C55E |
| ネガティブ/問題 | 赤 | #EF4444 |
| 注意/重要 | 黄 | #FBBF24 |
| 中立/情報 | 青 | #3B82F6 |
| 無効/過去 | グレー | #9CA3AF |

---

## テキスト追加ガイド

### Canvaでのテキスト追加

```
1. 生成した画像をCanvaにアップロード
2. テキストツールで各ラベルエリアにテキスト追加
3. フォント設定:
   - 日本語: Noto Sans JP / ヒラギノ角ゴ
   - 数字: Montserrat / Roboto
4. サイズ: 読みやすさを確認（最小16px）
5. 色: 背景とのコントラストを確保
6. 書き出し: PNG形式
```

### フォント推奨

| 用途 | フォント | サイズ目安 |
|------|---------|----------|
| タイトル | Noto Sans JP Bold | 24-32px |
| 見出し | Noto Sans JP Medium | 18-24px |
| 本文 | Noto Sans JP Regular | 14-18px |
| 数字 | Montserrat Bold | 各種サイズ |
| 補足 | Noto Sans JP Light | 12-14px |

---

## ワークフロー

### 1枚の図解制作（15-20分）

```
1. 図解の種類を決定（2分）
2. 内容を整理・箇条書き（3分）
3. プロンプト作成（3分）
4. NanoBanana Proで生成（3分）
5. 必要に応じて再生成（3分）
6. Canvaでテキスト追加（5分）
7. 確認・書き出し（2分）
```

### Kindle本全体の図解制作

```
章数: 10章と仮定
1章あたり図解: 2-3枚
合計: 20-30枚

制作時間目安:
- 企画・構成: 1時間
- 図解生成: 5-7時間
- テキスト追加: 3-5時間
- 確認・調整: 2時間
合計: 約12-15時間（2-3日）
```

---

## 品質チェックリスト

```
□ 一目で内容がわかる
□ 情報の階層が明確
□ 色のコントラストが十分
□ アイコン/シェイプが統一されている
□ テキストが読みやすい
□ 余白が適切
□ Kindle/スマホで見ても読める
□ 本文との整合性がある
□ ブランドカラーと合っている
□ ファイルサイズが適切
```
