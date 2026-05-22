---
name: nanobanana-prompts
description: NanoBanana（Google Gemini画像生成）向けの高品質プロンプトを生成。画像生成、編集、フェイススワップ、背景変更、キャラクター一貫性のプロンプト作成を支援。
---

# NanoBanana Pro Prompt Engineer

Google Gemini NanoBanana / NanoBanana Pro 向けの最適化されたプロンプトを生成するスキル。
**100-200語の簡潔で機能的なプロンプト**を生成します。

## When to Use This Skill

以下の場合にこのスキルを使用：
- 「画像プロンプトを作って」「NanoBananaプロンプト」
- 「顔を入れ替えて」「フェイススワップ」
- 「背景を変更して」「人物を別の場所に」
- 「同じキャラクターで別のシーン」
- 「衣装を統一して」「同じ服装で」
- 「スタイルを適用して」

## NanoBanana Pro の特徴

- **32,768トークン** の入力に対応（従来モデルの64倍以上）
- **最大14枚の参照画像** - Identity Locking対応
- **Markdown/JSON** 形式を理解
- **強力なプロンプト遵守** - 指示通りの画像を生成
- **画像編集** - 複数の同時編集が可能
- **テキストレンダリング** - 多言語テキストを画像内に正確に描画
- **4K高解像度出力** - プロフェッショナル品質

---

## 4つの黄金ルール

### 1. 編集を優先する
80%完成した画像には新規生成ではなく、具体的な編集指示を与える
```
❌ "Cool sunset photo"
✅ "Change the lighting to golden hour sunset, add warm orange tones (#FF8C00)"
```

### 2. 自然言語を使用する
キーワード羅列ではなく、完全な文で記述
```
❌ "car, neon, city, rain, night"
✅ "A futuristic sports car speeding through a rainy Tokyo street at night,
   neon signs reflecting on wet asphalt"
```

### 3. 具体的で詳細に
```
❌ "a woman"
✅ "A sophisticated elderly woman in her 60s wearing a vintage Chanel-style
   tweed suit, pearl earrings, silver hair in an elegant updo"
```

### 4. 文脈・目的を提供する
```
❌ "sandwich photo"
✅ "Professional food photography of a gourmet sandwich for a Brazilian
   high-end cookbook, appetizing presentation, natural lighting"
```

---

## プロンプト構造テンプレート

### 基本構造

```
[被写体の詳細説明], [構図・アングル], [照明・雰囲気], [スタイル/カメラ設定], [背景], [追加指示]
```

### 高品質プロンプト例

```
A professional product photograph of a sleek wireless headphone,
shot with Canon EOS 90D DSLR camera,
85mm lens, f/2.8 aperture,
soft studio lighting with rim light,
pure white background,
rule of thirds composition,
Pulitzer Prize winning cover photo quality
```

---

## プロンプトテクニック

### 1. 強調には ALL CAPS を使用

```
The subject MUST be centered.
NEVER include text in the image.
ALL elements should follow the rule of thirds.
```

### 2. Markdown リストで複数指示

```
Make ALL of the following edits:
- Add a red ribbon on the gift box
- Change the background to sunset colors (#FF6B35, #F7931E)
- Remove the watermark in the corner
- Increase the contrast by 20%
```

### 3. 詳細な色指定（HEXコード併用）

```
The dress should be royal purple (#9F2B68),
with gold accents (#FFD700) on the embroidery
```

### 4. カメラ・構図キーワード

| カテゴリ | キーワード例 |
|---------|-------------|
| **カメラ** | Canon EOS 90D, Sony A7III, Hasselblad X2D |
| **レンズ** | 85mm portrait lens, 24mm wide angle, 50mm f/1.4 |
| **構図** | rule of thirds, golden ratio, centered composition |
| **照明** | soft diffused lighting, rim light, golden hour |
| **品質** | Pulitzer Prize winning, award-winning photography |

### 5. JSON形式での詳細指定（上級）

```json
{
  "subject": {
    "type": "person",
    "gender": "female",
    "age": "mid-20s",
    "hair": "long black hair with subtle waves",
    "expression": "gentle smile, looking at camera"
  },
  "clothing": {
    "top": "white silk blouse",
    "accessories": "pearl necklace"
  },
  "setting": {
    "location": "modern office with large windows",
    "lighting": "natural daylight from left side",
    "time": "late afternoon, golden hour"
  },
  "style": "professional corporate portrait, magazine quality"
}
```

---

## カテゴリ別プロンプトテンプレート

### ポートレート

```
Professional headshot portrait of [subject description],
shot with 85mm lens at f/1.8,
soft Rembrandt lighting,
shallow depth of field with bokeh background,
neutral expression, direct eye contact,
high-end fashion magazine quality
```

### 商品写真

```
E-commerce product photography of [product],
pure white background (#FFFFFF),
soft diffused lighting from multiple angles,
slight shadow underneath for depth,
centered composition,
ultra high resolution, commercial quality
```

### 風景

```
Breathtaking landscape photograph of [scene],
shot during golden hour,
dramatic clouds in the sky,
foreground interest with [element],
wide angle 16mm lens,
National Geographic cover quality,
vibrant colors with natural saturation
```

### イラスト・アート

```
Digital illustration of [subject],
[art style: anime/watercolor/oil painting/vector],
[color palette description],
detailed line work,
professional concept art quality,
trending on ArtStation
```

### 広告・マーケティング

```
High-impact advertising visual for [product/service],
bold composition with [主要要素],
brand colors: [HEXコード],
clean modern aesthetic,
persuasive visual hierarchy,
award-winning advertising campaign quality
```

---

## 画像編集プロンプト（Pro Engineer機能）

### フェイススワップ（顔の入れ替え）

```
Using Image 1 as the face reference and Image 2 as the body/scene reference:
- PRECISELY preserve the facial features from Image 1 (eyes, nose, mouth shape, skin tone)
- Maintain the exact facial proportions and distinctive characteristics
- Seamlessly blend the face onto the body in Image 2
- Match the lighting direction and color temperature of Image 2
- Preserve natural skin texture and shadows
- ENSURE no distortion or uncanny valley effect
Output: A natural-looking composite where the person from Image 1 appears authentically in the scene from Image 2
```

### 背景変更（人物を別の場所に）

```
Replace the background while preserving the subject with these specifications:
- NEW BACKGROUND: [詳細な背景説明、場所、雰囲気]
- Lighting adjustment: Match subject lighting to new environment
  (light source direction: [方向], color temperature: [warm/cool/neutral])
- Edge blending: Seamless natural transitions, no visible cutout lines
- Shadow preservation: Cast appropriate shadows based on new light source
- Reflection handling: Add/adjust reflections if scene requires (water, glass, etc.)
- Atmospheric integration: Apply consistent haze, color grading to unify scene
CRITICAL: Subject MUST appear naturally present in the new location
```

### 衣装の統一（複数画像で同じ服装）

```
Apply consistent outfit across all provided images:
- REFERENCE OUTFIT from Image [N]: [詳細な服装説明]
- Maintain EXACT: color (#HEX), fabric texture, fit, style details
- Adapt naturally to each pose and lighting condition
- Preserve wrinkles and folds appropriate to body position
- Keep accessories consistent: [アクセサリー詳細]
- Match color saturation and brightness across all outputs
ALL images MUST show the identical outfit with natural variations only for pose/lighting
```

### キャラクター一貫性（Identity Locking）

```
Generate new scene maintaining character identity from reference images:
IDENTITY LOCK - Preserve from reference Image(s) [1-14]:
- Facial structure: exact proportions, distinctive features
- Skin tone and texture
- Hair: color, style, length, texture
- Body type and proportions
- Age appearance
- Any unique characteristics: [特徴]

NEW SCENE:
- Setting: [新しい場所・状況]
- Pose: [ポーズ説明]
- Expression: [表情]
- Lighting: [照明設定]
- Camera angle: [アングル]

The character MUST be instantly recognizable as the same person from references
```

### スタイル適用（アートスタイル変換）

```
Transform the image to [スタイル名] style while preserving:
- Core composition and subject placement
- Recognizable features and identity
- Overall mood and atmosphere

Style specifications:
- Art style: [具体的なスタイル: anime/oil painting/watercolor/pencil sketch/etc.]
- Color palette: [色調指定]
- Line work: [線の特徴: bold/delicate/sketchy/clean]
- Texture: [テクスチャ: smooth/rough/painterly/digital]
- Reference artist/work: [参考アーティスト or 作品]

MAINTAIN subject recognizability while fully embracing the new artistic style
```

### 複数編集の例

```
Edit this image with ALL of the following changes:
- Replace the sky with a dramatic sunset (#FF4500 to #800080 gradient)
- Add lens flare from the sun position
- Enhance the subject's contrast
- Remove all distracting elements in the background
- Add a subtle vignette effect
```

---

## 100-200語プロンプト最適化

### 最適なプロンプト構造（推奨）

```
[主題 30-40語] + [技術仕様 20-30語] + [スタイル/雰囲気 20-30語] + [制約/必須条件 30-50語]
```

### 例：ポートレート（156語）

```
Create a professional corporate headshot of a confident Asian businesswoman
in her early 40s. She has shoulder-length black hair with subtle highlights,
wearing a tailored navy blue blazer over a cream silk blouse. Her expression
is warm yet authoritative, with a slight smile and direct eye contact.

Technical: Shot with Canon EOS R5, 85mm f/1.4 lens, studio lighting setup
with key light at 45 degrees, fill light opposite, and hair light from above.
Shallow depth of field with creamy bokeh background in neutral gray gradient.

Style: Modern executive portrait suitable for LinkedIn and company website.
Clean, polished, Fortune 500 CEO aesthetic.

MUST include: Catch lights in eyes, natural skin texture, professional color
grading. NEVER include: Harsh shadows, overly retouched skin, distracting
background elements. Output in 4K resolution, suitable for print and digital.
```

---

## 品質向上のコツ

1. **具体的に記述** - 「きれいな花」→「鮮やかな赤いバラ、朝露の水滴がついた花びら」
2. **プロ機材を指定** - カメラ、レンズ、照明を具体的に
3. **品質キーワード追加** - "award-winning", "professional", "magazine quality"
4. **否定形も活用** - "NO text", "NEVER include watermarks"
5. **複数指示はリスト形式で**

---

## 使用フロー

```
ユーザー: 「猫の画像のプロンプト作って」

→ スキルが以下を提供:

1. 基本プロンプト（すぐ使える版）
2. 詳細プロンプト（カスタマイズ可能版）
3. JSON形式（高精度版）

ユーザーは目的に応じて選択し、gemini-image-generator で画像生成
```

## 連携スキル

- **gemini-image-generator** - 生成したプロンプトで画像を生成
- **copywriting-helper** - 広告用画像のコンセプト立案

---

## インタラクティブ使用例

```
ユーザー: 「この写真の顔を別の人に入れ替えて」

→ スキルが質問:
  1. 顔の参照画像はどれですか？
  2. 体/シーンの画像はどれですか？
  3. 特に保持したい特徴は？

→ 最適化されたフェイススワッププロンプトを生成（100-200語）
→ gemini-image-generator で実行
```

```
ユーザー: 「同じキャラクターで別のシーンを作って」

→ スキルが質問:
  1. 参照画像は何枚ありますか？（最大14枚）
  2. 新しいシーンの設定は？
  3. ポーズや表情の希望は？

→ Identity Locking プロンプトを生成
→ キャラクターの一貫性を保った新シーンを生成
```

---

## References

- [awesome-nanobanana-pro (GitHub)](https://github.com/ZeroLu/awesome-nanobanana-pro)
- [Max Woolf's NanoBanana Prompt Guide](https://minimaxir.com/2025/11/nano-banana-prompts/)
- [Nano Banana Prompt Library](https://nanobananaprompt.org/)
- [DEV Community - NanoBanana Pro Prompting Guide](https://dev.to/googleai/nano-banana-pro-prompting-guide-strategies-1h9n)
- [AIPRM - Nano Banana Pro Prompt Engineer](https://app.aiprm.com/gpts/g-RBjaM21Jr/nano-banana-prompt-engineer-text-to-image)
