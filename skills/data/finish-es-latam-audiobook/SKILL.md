---
name: finish-es_latam-audiobook
description: Финализация аудиокниги ru→es_latam. Проверяет что ВСЕ переводы готовы, генерирует TTS, комбинирует аудио, ищет фоновую картинку, создаёт видео. Использовать ТОЛЬКО после завершения claude-translation-pipeline-es_latam.
---

# Finish es_latam Audiobook

## ⚠️ КРИТИЧЕСКИЕ ТРЕБОВАНИЯ

### 1. ПЕРЕВОДИТЬ НЕЛЬЗЯ!
```
❌ ЗАПРЕЩЕНО: Переводить предложения или слова
❌ ЗАПРЕЩЕНО: Изменять таблицы sentences/rare_words
✅ РАЗРЕШЕНО: Только чтение из БД + генерация audio/video
```

### 2. Предварительная проверка (ОБЯЗАТЕЛЬНО!)

**Перед ЛЮБЫМИ действиями выполни:**
```python
import sqlite3
db = sqlite3.connect('projects/PROJECT_ru_es_latam/project.db')

# Проверить ВСЕ предложения переведены
missing = db.execute('''
    SELECT COUNT(*) FROM sentences WHERE lang="ru"
    AND sentence_idx NOT IN (SELECT sentence_idx FROM sentences WHERE lang="es_latam")
''').fetchone()[0]

# Проверить ВСЕ слова переведены
missing_words = db.execute('''
    SELECT COUNT(*) FROM rare_words WHERE translation IS NULL
''').fetchone()[0]

if missing > 0 or missing_words > 0:
    print(f"❌ СТОП! Переводы не завершены!")
    print(f"   Missing sentences: {missing}")
    print(f"   Missing words: {missing_words}")
    print("   → Сначала завершить claude-translation-pipeline-es_latam")
    # ОСТАНОВИТЬСЯ! НЕ ПРОДОЛЖАТЬ!
else:
    print("✅ Все переводы готовы, можно продолжать")
```

**Если есть missing → ОСТАНОВИТЬСЯ и сообщить пользователю!**

---

## Параметры

| Параметр | Значение |
|----------|----------|
| Source lang | `ru` |
| Target lang | `es_latam` |
| TTS locale | `es-latam` (Latin American Spanish) |
| Source speed | `1.5` |
| Target speed | `0.8` |
| Parallel workers | `16` (все процессы) |

---

## Pipeline

### Step 1: Проверка переводов
См. выше. Если не пройдена → СТОП.

### Step 2: Поиск фоновой картинки

```python
# Получить название книги из проекта
book_name = "asimov_profession"  # из имени проекта или meta

# Поиск в интернете
search_query = f"{book_name} book cover art wallpaper"
# Использовать WebSearch для поиска
# Выбрать подходящую картинку (1920x1080 или больше)
# Скачать в projects/PROJECT/video/background.jpg
```

**Критерии выбора картинки:**
- Разрешение минимум 1920x1080
- Тематически связана с книгой
- Без текста или с минимальным текстом
- Подходит как фон (не слишком яркая/пёстрая)

### Step 3: Генерация Audio + Video

```bash
python3 main.py resume PROJECT_NAME \
    --tts google_cloud \
    --tts-target-locale es-latam \
    --source-speed 1.5 \
    --target-speed 0.8 \
    --tts-parallel 16 \
    --combine-workers 16 \
    --video-workers 16 \
    --background projects/PROJECT/video/background.jpg
```

**Если background не поддерживается CLI:**
```bash
# Сначала audio
python3 main.py resume PROJECT_NAME \
    --tts google_cloud \
    --tts-target-locale es-latam \
    --source-speed 1.5 \
    --target-speed 0.8 \
    --tts-parallel 16 \
    --combine-workers 16

# Потом video с background (проверить CLI опции)
python3 main.py resume PROJECT_NAME \
    --video-workers 16 \
    --background projects/PROJECT/video/background.jpg
```

---

## Workflow Summary

```
1. ✅ Проверить переводы (sentences + rare_words)
   ↓ Если missing → СТОП
2. 🔍 Найти фоновую картинку (WebSearch)
   ↓ Скачать в video/background.jpg
3. 🎙️ TTS генерация (16 параллелей)
   - Source: ru, speed 1.5
   - Target: es-latam, speed 0.8
4. 🔊 Combine audio (16 параллелей)
5. 🎬 Generate video с background (16 параллелей)
6. ✅ Готово!
```

---

## Проверка результата

После завершения:
```bash
ls -la projects/PROJECT/
# Должно быть:
# - audio/combined.mp3
# - video/output.mp4
# - video/subtitles.ass
# - video/background.jpg

# Проверить размер видео
ffprobe projects/PROJECT/video/output.mp4
```

---

## Troubleshooting

### TTS квота исчерпана
```bash
python3 main.py quota
# Если Google Cloud квота закончилась - подождать или использовать другой провайдер
```

### Video генерация падает
```bash
# Уменьшить параллелизм
--video-workers 8
# Или даже
--video-workers 4
```

### Background не подхватывается
Проверить что картинка:
- Существует по пути
- Формат JPG/PNG
- Не битая

---

## Self-Reminder

```
📌 CURRENT STATE:
- Project: {name}
- Translations: ✅ verified
- Background: {found/missing}
- Audio: {pending/in_progress/complete}
- Video: {pending/in_progress/complete}
- Next: {action}
```

---

## Anti-Patterns

❌ **НЕ ДЕЛАТЬ:**
- Запускать без проверки переводов
- Переводить что-либо
- Редактировать sentences/rare_words
- Использовать es вместо es-latam для TTS
- Забывать про background картинку

✅ **ДЕЛАТЬ:**
- Проверка переводов ПЕРВЫМ шагом
- Искать качественный background
- 16 параллелей везде
- Скорости: source 1.5, target 0.8
- TTS locale: es-latam
