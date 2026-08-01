---
name: nano-banana-pro
description: Use the bundled script to generate or edit images.
---

---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro). RoastPlusでの用途: コーヒー豆の視覚化、焙煎度合いの比較画像、クイズ用の画像生成、設定画面のアイコン作成等。
homepage: https://ai.google.dev/
metadata: {"clawdbot":{"emoji":"🍌","requires":{"bins":["uv"],"env":["GEMINI_API_KEY"]},"primaryEnv":"GEMINI_API_KEY","install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Nano Banana Pro (Gemini 3 Pro Image)

Use the bundled script to generate or edit images.

Generate
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "your image description" --filename "output.png" --resolution 1K
```

Edit
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "edit instructions" --filename "output.png" --input-image "/path/in.png" --resolution 2K
```

API key
- `GEMINI_API_KEY` env var
- Or set `skills."nano-banana-pro".apiKey` / `skills."nano-banana-pro".env.GEMINI_API_KEY` in `~/.clawdbot/clawdbot.json`

Notes
- Resolutions: `1K` (default), `2K`, `4K`.
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.png`.
- The script prints a `MEDIA:` line for Clawdbot to auto-attach on supported chat providers.
- Do not read the image back; report the saved path only.

## RoastPlusでの使用例

### コーヒー豆の視覚化

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "コーヒー豆の焙煎度合い比較画像。左から順に浅煎り、中煎り、深煎りの3つの豆を並べる。写真風、プロフェッショナルな照明" \
  --filename "public/images/roast-levels.png" \
  --resolution 2K
```

### クイズ用の画像生成

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "エチオピア産コーヒー豆のクローズアップ写真。豆の形状と色が明確に見える、プロフェッショナルな撮影" \
  --filename "public/images/quiz/ethiopia-beans.png" \
  --resolution 1K
```

### 既存画像の編集（焙煎度合いの調整）

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "この豆をより深煎りに見えるように暗くする" \
  --input-image "public/images/original-bean.png" \
  --filename "public/images/dark-roast-bean.png" \
  --resolution 2K
```

### クリスマスモード用のアイコン

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "雪の結晶の形をしたコーヒー豆のロゴ。クリスマスの雰囲気、ゴールドとダークグリーンの配色" \
  --filename "public/images/christmas-logo.png" \
  --resolution 1K
```

## プロンプト作成のヒント

- **照明**: "プロフェッショナルな照明", "自然光", "スタジオ照明"
- **スタイル**: "写真風", "イラスト風", "ミニマルデザイン"
- **配色**: RoastPlusのブランドカラー（`#EF8A00`, `#211714`）を指定
- **用途**: "クイズ用", "設定画面用", "ホーム画面用" を明記すると適切な構図に
