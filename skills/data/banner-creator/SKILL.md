---
name: banner-creator
description: Generate advertising banners and creatives for various platforms (X, Facebook, Instagram, PRTimes, YouTube, LINE, Web ads). Supports platform-specific presets, reference image search, and copy text generation. Use when creating social media posts, ads, or promotional materials.
---

# Banner Creator - 広告バナー/クリエイティブ生成

各種SNS・広告プラットフォーム向けのバナー/クリエイティブを生成します。

## 機能

1. **プラットフォーム別プリセット**: X, Facebook, Instagram, PRタイムズ, YouTube, LINE, Web広告
2. **トーン・スタイル設定**: プロフェッショナル、ポップ、エレガントなど
3. **参考画像検索**: キーワードからWeb検索で参考画像を取得
4. **コピーテキスト生成**: 投稿文・ハッシュタグ・CTAを同時生成

## プラットフォーム別サイズ

| Platform | Size | Aspect Ratio |
|----------|------|--------------|
| x_post | 1200x675 | 16:9 |
| x_card | 800x418 | 1.91:1 |
| facebook | 1200x630 | 1.91:1 |
| facebook_story | 1080x1920 | 9:16 |
| instagram_feed | 1080x1080 | 1:1 |
| instagram_story | 1080x1920 | 9:16 |
| prtimes | 1200x630 | 1.91:1 |
| youtube | 1280x720 | 16:9 |
| line | 1040x1040 | 1:1 |
| web_horizontal | 1200x628 | 1.91:1 |
| web_vertical | 300x600 | 1:2 |

## Usage

```bash
# Basic usage
python scripts/banner_creator.py --platform x_post --message "キャッチコピー"

# With copy text generation
python scripts/banner_creator.py --platform instagram_feed --message "新商品発売" --with-copy

# With reference image search
python scripts/banner_creator.py --platform facebook --message "セール" --search-ref "EC セール バナー"

# Full options
python scripts/banner_creator.py \
  --platform x_post \
  --message "メインメッセージ" \
  --sub-copy "サブコピー" \
  --cta "今すぐ登録" \
  --tone professional \
  --color-scheme cool \
  --font-style bold \
  --priority ctr \
  --brand-name "会社名" \
  --session "campaign_name" \
  --with-copy \
  --variants 3
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --platform | Yes | - | Target platform (see table above) |
| --message | Yes | - | Main headline/catchphrase |
| --sub-copy | No | - | Sub-headline or details |
| --cta | No | - | Call-to-action text |
| --tone | No | professional | Tone: professional, casual, pop, elegant, urgent, minimal, tech, natural |
| --color-scheme | No | auto | Color: warm, cool, mono, pastel, vivid, dark, or HEX code |
| --font-style | No | auto | Font: gothic, mincho, handwritten, bold, script, geometric |
| --priority | No | ctr | Focus: ctr, brand, info, emotion, product, event |
| --brand-name | No | - | Brand/company name to display |
| --reference | No | - | Local path or URL to reference image |
| --search-ref | No | - | Keywords to search for reference images |
| --session | No | - | Session name for organizing output |
| --with-copy | No | false | Generate copy text along with image |
| --variants | No | 1 | Number of variations to generate |
| --output | No | auto | Output file path |

## Output

- **Image**: `docs/generated/banners/{date}_{session}/{filename}.png`
- **Copy text** (when --with-copy): Saved as `{filename}_copy.md`
  - 3 post text variations
  - Hashtag suggestions
  - CTA phrases

## Examples

### X Post Banner
```bash
python scripts/banner_creator.py \
  --platform x_post \
  --message "AI時代の働き方改革" \
  --sub-copy "無料ウェビナー開催" \
  --cta "今すぐ登録" \
  --tone professional \
  --with-copy
```

### Instagram Feed with Reference Search
```bash
python scripts/banner_creator.py \
  --platform instagram_feed \
  --message "Summer Collection" \
  --tone pop \
  --color-scheme vivid \
  --search-ref "fashion summer sale instagram"
```

### PRTimes Press Release Image
```bash
python scripts/banner_creator.py \
  --platform prtimes \
  --message "新サービスリリースのお知らせ" \
  --brand-name "株式会社〇〇" \
  --tone professional \
  --priority info
```

## Requirements

- GEMINI_API_KEY or GOOGLE_API_KEY in environment
- Python packages: google-genai, Pillow, python-dotenv, requests
