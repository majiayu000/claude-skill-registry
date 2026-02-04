---
name: media-generator
description: |
  バナー/図表/スライド/画像の生成・編集を行うサブエージェント。
  Gemini Image Generation APIを使用して各種メディアを生成する。
  「バナーを作って」「図表を生成」「スライドを作成」「画像を生成」等のリクエストで発動。
triggers:
  - バナーを作って
  - バナー生成
  - 図表を作成
  - インフォグラフィック
  - ダイアグラム
  - スライドを生成
  - 画像を生成
  - 画像を編集
  - X用の画像
  - Instagram用
  - Facebook用
---

# Media Generator サブエージェント

バナー/図表/スライド/画像の生成・編集を専用コンテキストで実行するサブエージェント。

## 目的

メディア生成処理をメインエージェントのコンテキストから分離し：
- 複数の参照画像を含む処理を効率化
- プラットフォーム別プリセットの適用
- 生成結果のパス情報のみを返却

## 機能一覧

| 機能 | スクリプト | 説明 |
|-----|----------|------|
| バナー生成 | `banner_creator.py` | SNS/広告向けバナー生成 |
| 図表生成 | `generate_diagram.py` | インフォグラフィック/図表生成 |
| スライド生成 | `generate_slide.py` | 講義用スライド画像生成 |
| 汎用画像生成 | `nanobanana.py` | テキスト→画像、画像編集 |

## 1. バナー生成 (`cursor_tools/banner_creator.py`)

### プラットフォーム別プリセット

| プリセット | サイズ | アスペクト比 | 用途 |
|-----------|-------|-------------|------|
| `x_post` | 1200x675 | 16:9 | X タイムライン投稿 |
| `x_card` | 800x418 | 16:9 | X リンクカード |
| `facebook` | 1200x630 | 16:9 | Facebook リンク投稿 |
| `facebook_story` | 1080x1920 | 9:16 | Facebook ストーリーズ |
| `instagram_feed` | 1080x1080 | 1:1 | Instagram フィード |
| `instagram_story` | 1080x1920 | 9:16 | Instagram ストーリーズ |
| `prtimes` | 1200x630 | 16:9 | PRTimes プレスリリース |
| `youtube_thumbnail` | 1280x720 | 16:9 | YouTube サムネイル |
| `line` | 1200x628 | 16:9 | LINE 公式アカウント |
| `web_banner` | 1200x628 | 16:9 | Web広告バナー |

### 使用方法

```bash
# X用バナー生成
python cursor_tools/banner_creator.py \
  --platform x_post \
  --topic "新サービスリリース告知" \
  --tone professional \
  --output-dir docs/generated/banners

# 参照画像を使用
python cursor_tools/banner_creator.py \
  --platform instagram_feed \
  --topic "夏のキャンペーン" \
  --reference-images image1.png image2.png \
  --output-dir docs/generated/banners

# コピーテキスト同時生成
python cursor_tools/banner_creator.py \
  --platform prtimes \
  --topic "プレスリリース用" \
  --with-copy \
  --output-dir docs/generated/banners
```

## 2. 図表/インフォグラフィック生成 (`cursor_tools/generate_diagram.py`)

### スタイル

| スタイル | 説明 |
|---------|------|
| `colorful_infographic` | 明るい色、アイコン、読みやすいレイアウト |
| `sketch` | 手描き風、鉛筆/チャコールテクスチャ |
| `photorealistic` | 写真のようなリアルな質感 |
| `minimalist` | シンプル、余白重視、限定カラー |
| `claymation` | 3Dクレイ風、柔らかい照明 |
| `pixel_art` | レトロゲーム風、ブロック調 |

### 使用方法

```bash
# トピックから図表生成
python cursor_tools/generate_diagram.py \
  --topic "マーケティングファネル" \
  --style colorful_infographic \
  --aspect-ratio 16:9 \
  --output-dir reports/visualizations

# 長文テキストからインフォグラフィック
python cursor_tools/generate_diagram.py \
  --topic "$(cat article.txt)" \
  --style minimalist \
  --output-dir reports/visualizations
```

## 3. 汎用画像生成/編集 (`cursor_tools/nanobanana.py`)

### 使用方法

```bash
# テキストから画像生成
python cursor_tools/nanobanana.py \
  --prompt "A futuristic city at sunset" \
  --aspect-ratio 16:9 \
  --output-dir docs/generated

# 画像編集（参照画像+指示）
python cursor_tools/nanobanana.py \
  --prompt "Make the background blue" \
  --reference reference.png \
  --output-dir docs/generated

# 複数参照画像を使用
python cursor_tools/nanobanana.py \
  --prompt "Combine these styles" \
  --reference image1.png image2.png \
  --output-dir docs/generated
```

### アスペクト比

| アスペクト比 | 用途 |
|-------------|------|
| `1:1` | Instagram、プロフィール画像 |
| `4:3` | 汎用横長 |
| `3:4` | 汎用縦長 |
| `16:9` | YouTube、プレゼン |
| `9:16` | ストーリーズ、リール |
| `21:9` | ウルトラワイド |

## サブエージェント呼び出しパターン

メインエージェントは以下のパターンでこのサブエージェントを呼び出す：

```python
Task(
    subagent_type="generalPurpose",
    model="fast",
    description="Banner generation",
    prompt="""
    このスキルを読んで実行してください: .claude/skills/media-generator/SKILL.md
    
    タスク: {ユーザーの指示}
    プラットフォーム: {x_post / instagram_feed / etc.}
    トピック: {生成内容}
    
    生成した画像のパスを返却してください。
    """
)
```

## 返却フォーマット

処理結果は以下の形式で返却：

```yaml
status: success
generated_files:
  - path: docs/generated/banners/x_post_20260127_143022.png
    platform: x_post
    size: 1200x675
    aspect_ratio: 16:9
copy_text: |
  【新サービスリリース】
  AIを活用した業務効率化ツールが登場！
  #AI #業務効率化
```

## 依存関係

```txt
google-generativeai>=0.3.0
Pillow>=9.0.0
python-dotenv>=1.0.0
```

## 環境変数

```bash
# 必須
GEMINI_API_KEY=your_api_key
# または
GOOGLE_API_KEY=your_api_key
```

## 注意事項

- 生成画像は`docs/generated/`配下に自動保存
- セッション名を指定するとサブフォルダに整理
- 日本語テキストを含める場合は明示的に指示
- 参照画像は最大5枚まで
