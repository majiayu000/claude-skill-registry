---
name: gemini-caption-translate
description: Translate subtitles to target language using Gemini API with context-aware translation
---

# Gemini Subtitle Translation Skill

Use this skill to translate subtitle files while preserving timestamps and formatting.

## Installation

```bash
# Using uv (recommended)
uv pip install gemini-caption-skills

# Or using pip
pip install gemini-caption-skills
```

## Prerequisites

### Get Your API Key

1. Visit: https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key

### Configure API Key (choose one)

**Option 1: Save to config (recommended)**
```python
from gemini_caption import set_api_key
set_api_key("your-api-key-here")
```
Config location: `~/.config/gemini-caption/config.json`

**Option 2: Environment variable**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Usage

### Translate Subtitle File

```python
from gemini_caption.translation import GeminiTranslator

translator = GeminiTranslator(verbose=True)

# Translate SRT to Chinese
translator.translate(
    input_file="video.srt",
    output_file="video.zh.srt",
    target_language="zh",
)

# Translate VTT to Japanese
translator.translate(
    input_file="video.vtt",
    output_file="video.ja.vtt",
    target_language="ja",
)
```

### Generate Bilingual Subtitles

```python
from gemini_caption.translation import BilingualGenerator

generator = BilingualGenerator(verbose=True)

# Create bilingual SRT (English + Chinese)
generator.generate(
    input_file="video.srt",
    output_file="video.bilingual.srt",
    target_language="zh",
)
```

Output format:
```srt
1
00:00:00,000 --> 00:00:02,500
Welcome to the show.
欢迎来到节目。

2
00:00:02,500 --> 00:00:05,000
Thank you for having me.
感谢邀请我。
```

### Transcribe and Translate in One Step

```python
from gemini_caption import GeminiTranscriber

transcriber = GeminiTranscriber(verbose=True)

# Transcribe and translate to target language
transcript = transcriber.transcribe_translate(
    source="https://www.youtube.com/watch?v=VIDEO_ID",
    target_language="zh",
    output_file="video.zh.md",
)
```

## Configuration

```python
from gemini_caption.translation import TranslationConfig, GeminiTranslator

config = TranslationConfig(
    model_name="gemini-2.5-flash",
    batch_size=50,           # Lines per API call
    context_window=3,        # Context lines before/after
    preserve_formatting=True,
    verbose=True,
)

translator = GeminiTranslator(config=config)
```

## Supported Languages

All languages supported by Gemini API:

| Code | Language |
|------|----------|
| `zh` | Chinese (Simplified) |
| `zh-TW` | Chinese (Traditional) |
| `ja` | Japanese |
| `ko` | Korean |
| `en` | English |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `pt` | Portuguese |
| `ru` | Russian |
| `ar` | Arabic |
| `hi` | Hindi |
| ... | And 100+ more |

## Input/Output Formats

Supports all formats from `lattifai-captions`:

- **SRT** (.srt)
- **VTT** (.vtt)
- **ASS/SSA** (.ass, .ssa)
- **TTML** (.ttml)
- **JSON** (.json)
- **Gemini Markdown** (.md)

## Translation Quality Tips

1. **Use context window**: Helps maintain consistency across segments
2. **Batch appropriately**: 30-50 lines per batch balances speed and quality
3. **Review terminology**: Add custom terminology hints in config if needed

## Error Handling

```python
from gemini_caption.translation import GeminiTranslator, TranslationError

translator = GeminiTranslator()

try:
    translator.translate("input.srt", "output.srt", "zh")
except TranslationError as e:
    print(f"Translation failed: {e}")
    # Check e.failed_segments for partial results
```

## CLI Usage (Coming Soon)

```bash
# Translate subtitle
gemini-translate input.srt output.zh.srt --lang zh

# Generate bilingual
gemini-translate input.srt output.srt --lang zh --bilingual

# Transcribe and translate
gemini-transcribe video.mp4 --translate zh -o output.zh.srt
```
