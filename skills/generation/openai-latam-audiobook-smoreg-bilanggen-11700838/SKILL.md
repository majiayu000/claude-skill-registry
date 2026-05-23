---
name: openai-latam-audiobook
description: Create complete audiobook with OpenAI GPT-4o-mini translation to Argentine Spanish. Full pipeline - translate, TTS, video with background image. Auto-scales parallelism based on file size. Use when user wants to create audiobook from Russian text to LATAM Spanish.
---

# OpenAI LATAM Audiobook Generator

## Overview

Полный пайплайн создания аудиокниги:
1. Перевод на аргентинский испанский (GPT-4o-mini)
2. Озвучка (Google Cloud TTS)
3. Поиск и скачивание фоновой картинки
4. Генерация видео

**Скорости озвучки:** RU 1.5x / ES-LATAM 0.8x

---

## Quick Start

Когда пользователь просит создать аудиокнигу:

```bash
# 1. Определить размер файла
FILE_SIZE=$(wc -c < "txt_source/BOOK.txt")

# 2. Выбрать параллелизм
if [ $FILE_SIZE -gt 51200 ]; then
    PARALLEL=16
else
    PARALLEL=4
fi

# 3. Запустить пайплайн
python3 main.py run \
    -i txt_source/BOOK.txt \
    -s ru -t es \
    --translator openai \
    --translator-parallel $PARALLEL \
    --tts google_cloud \
    --tts-parallel $PARALLEL \
    --tts-target-locale es-latam \
    --combine-workers $PARALLEL \
    --video-workers 8 \
    --speed-source 1.5 \
    --speed-target 0.8
```

---

## Full Workflow

### Step 1: Check File Size & Set Parallelism

```bash
# Get file size in bytes
FILE_SIZE=$(wc -c < "txt_source/BOOK.txt")
echo "File size: $FILE_SIZE bytes"

# Set parallelism
if [ $FILE_SIZE -gt 51200 ]; then
    echo "Large file (>50KB) - using 16 parallel workers"
    PARALLEL=16
else
    echo "Small file (<50KB) - using 4 parallel workers"
    PARALLEL=4
fi
```

### Step 2: Use Existing Background Image

**ВАЖНО: Для каждого текста уже есть сгенерированная картинка!**

```
txt_source/
├── book_name.txt      # Исходный текст
└── book_name.png      # Сгенерированная обложка (уже есть!)
```

**Процесс:**
1. Проверить что картинка существует: `txt_source/{BOOK_NAME}.png`
2. Скопировать в проект:
```bash
# После создания проекта - скопировать картинку
cp txt_source/BOOK_NAME.png projects/BOOK_NAME_ru_es/video/background.png
```

**Если картинки НЕТ** (для новых текстов) - использовать WebSearch:

```python
# Search for book-related neutral background image
WebSearch("BOOK_TITLE background wallpaper neutral abstract 1920x1080")
# Download image:
WebFetch(url="IMAGE_URL", save_as="projects/PROJECT/video/background.jpg")
```

**Image search queries by genre:**

| Genre | Search Query |
|-------|-------------|
| Sci-Fi | `space nebula abstract wallpaper 4k` |
| Fantasy | `fantasy landscape castle mountains wallpaper` |
| Horror | `dark forest fog atmospheric wallpaper` |
| Classic | `vintage library books wallpaper aesthetic` |
| Adventure | `ocean sunset adventure wallpaper` |

### Step 3: Run Translation Pipeline

```bash
python3 main.py run \
    -i txt_source/BOOK.txt \
    -s ru -t es \
    --translator openai \
    --translator-parallel $PARALLEL \
    --tts google_cloud \
    --tts-parallel $PARALLEL \
    --tts-target-locale es-latam \
    --combine-workers $PARALLEL \
    --video-workers 8 \
    --speed-source 1.5 \
    --speed-target 0.8
```

### Step 4: Copy Background Image Before Video Generation

**ПЕРЕД генерацией видео** - скопировать картинку:

```bash
# Путь к проекту
PROJECT_DIR="projects/BOOK_NAME_ru_es"

# Создать папку video если её нет
mkdir -p "$PROJECT_DIR/video"

# Скопировать картинку из txt_source (если есть)
if [ -f "txt_source/BOOK_NAME.png" ]; then
    cp "txt_source/BOOK_NAME.png" "$PROJECT_DIR/video/background.png"
    echo "✅ Background image copied"
fi
```

**Важно:** Картинка должна быть в `projects/*/video/background.{png,jpg}` ДО запуска видео-генерации!

---

## Settings Reference

| Parameter | Value | Description |
|-----------|-------|-------------|
| `--translator` | `openai` | GPT-4o-mini для LATAM |
| `--tts-target-locale` | `es-latam` | Латиноамериканский акцент TTS |
| `--speed-source` | `1.5` | Русский 1.5x быстрее |
| `--speed-target` | `0.8` | Испанский 0.8x медленнее |
| `--translator-parallel` | `4` or `16` | По размеру файла |
| `--tts-parallel` | `4` or `16` | По размеру файла |
| `--combine-workers` | `4` or `16` | По размеру файла |
| `--video-workers` | `8` | Всегда 8 |

---

## Parallelism Rules

| File Size | Parallel Workers | Estimated Time |
|-----------|-----------------|----------------|
| < 50 KB | 4 | ~2-5 min |
| 50-200 KB | 8 | ~5-10 min |
| 200-500 KB | 12 | ~10-20 min |
| > 500 KB | 16 | ~20-60 min |

---

## Background Image Guidelines

**DO:**
- Abstract, atmospheric images
- Landscapes without people
- Space/nebula for sci-fi
- Nature scenes for classics
- Dark/moody for horror

**DON'T:**
- Images with text
- Copyrighted characters
- Faces or people
- Low resolution
- Busy/distracting patterns

---

## Cost Estimation (OpenAI GPT-4o-mini)

| Book Size | Characters | Est. Cost |
|-----------|------------|-----------|
| Short story (50KB) | ~50K | ~$0.01 |
| Novella (200KB) | ~200K | ~$0.05 |
| Novel (500KB) | ~500K | ~$0.10 |
| Long novel (1MB) | ~1M | ~$0.20 |

---

## Example: Full Pipeline

```bash
# Example for "The Time Machine" by H.G. Wells

# 1. Check size
wc -c txt_source/wells_time_machine.txt
# 319094 bytes = ~312 KB (use PARALLEL=12)

# 2. Start translation pipeline
python3 main.py run \
    -i txt_source/wells_time_machine.txt \
    -s ru -t es \
    --translator openai \
    --translator-parallel 12 \
    --tts google_cloud \
    --tts-parallel 12 \
    --tts-target-locale es-latam \
    --combine-workers 12 \
    --video-workers 8 \
    --speed-source 1.5 \
    --speed-target 0.8

# 3. PARALLEL: Search background image
# "time machine steampunk victorian wallpaper abstract 4k"
# Download to: projects/wells_time_machine_ru_es/video/background.jpg

# 4. Output: projects/wells_time_machine_ru_es/video/output.mp4
```

---

## Troubleshooting

### SSL Certificate Error (NLTK)
Fixed in code. If still occurs:
```bash
pip3 install certifi
```

### OpenAI Rate Limit (429)
- Reduce `--translator-parallel` to 2-4
- Wait 1 minute and retry

### SQLite Thread Error
Fixed in code with `check_same_thread=False`

### TTS Quota Exceeded
- Check quota: `python3 main.py quota`
- Wait until next month or use `--tts gtts`

---

## Files Created

```
projects/BOOK_ru_es/
├── project.db           # All data
├── text/original.txt    # Source text
├── audio/
│   ├── source/*.mp3     # Russian TTS
│   ├── target/*.mp3     # Spanish TTS
│   └── combined.mp3     # Final audio
└── video/
    ├── background.jpg   # Downloaded image (optional)
    ├── subtitles.ass    # Karaoke subtitles
    └── output.mp4       # Final video
```
