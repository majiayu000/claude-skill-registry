---
name: youtube-metadata
description: Generate YouTube title, description, and tags for bilingual audiobook videos. Use when user asks to upload video, generate youtube metadata, or prepare video for upload.
trigger_phrases:
  - youtube metadata
  - youtube description
  - название для ютуба
  - описание для ютуба
  - generate youtube
  - upload video
  - залить видео
  - загрузить на ютуб
---

# YouTube Metadata Generator for Bilingual Audiobooks

Generate optimized YouTube metadata for bilingual audiobook videos.

## Input Required

User MUST provide:
- **Author** (in English)
- **Title** (in English)
- **Source language** (default: RU)
- **Target language** (default: ES LATAM)

## Output: Upload Command

Generate the full command for `scripts/youtube_upload.py`:

```bash
python3 scripts/youtube_upload.py "PROJECT_NAME" --title "[Bilingual][SOURCE→TARGET] Author - Title"
```

## Title Format

```
[Bilingual][{SOURCE}→{TARGET}] {Author} - {Title}
```

**⚠️ CRITICAL: Author and Title MUST be in ENGLISH!**

Examples:
- `[Bilingual][RU→ES LATAM] Sheckley - Ticket to Tranai`
- `[Bilingual][RU→ES LATAM] Asimov - Profession`
- `[Bilingual][RU→EN] Bulgakov - The Master and Margarita`
- `[Bilingual][EN→ES LATAM] Bradbury - The Veldt`

## Description Templates by Language Pair

### RU → ES LATAM (Russian to Latin American Spanish)
```
🎧 AI-generated bilingual audio for passive language learning.
Each sentence: first Russian, then Latin American Spanish.

⚠️ Neural TTS - minor errors possible. Premium voices coming soon.

📩 Want other languages or texts? Drop a comment!

#LearnSpanish #Bilingual #LanguageLearning #испанский
```

### RU → EN (Russian to English)
```
🎧 AI-generated bilingual audio for passive language learning.
Each sentence: first Russian, then English.

⚠️ Neural TTS - minor errors possible. Premium voices coming soon.

📩 Want other languages or texts? Drop a comment!

#LearnEnglish #Bilingual #LanguageLearning #английский
```

### EN → ES LATAM (English to Latin American Spanish)
```
🎧 AI-generated bilingual audio for passive language learning.
Each sentence: first English, then Latin American Spanish.

⚠️ Neural TTS - minor errors possible. Premium voices coming soon.

📩 Want other languages or texts? Drop a comment!

#LearnSpanish #Bilingual #LanguageLearning #AprendeEspañol
```

### EN → RU (English to Russian)
```
🎧 AI-generated bilingual audio for passive language learning.
Each sentence: first English, then Russian.

⚠️ Neural TTS - minor errors possible. Premium voices coming soon.

📩 Want other languages or texts? Drop a comment!

#LearnRussian #Bilingual #LanguageLearning #русскийязык
```

### RU → DE (Russian to German)
```
🎧 AI-generated bilingual audio for passive language learning.
Each sentence: first Russian, then German.

⚠️ Neural TTS - minor errors possible. Premium voices coming soon.

📩 Want other languages or texts? Drop a comment!

#LearnGerman #Bilingual #LanguageLearning #немецкий
```

### RU → FR (Russian to French)
```
🎧 AI-generated bilingual audio for passive language learning.
Each sentence: first Russian, then French.

⚠️ Neural TTS - minor errors possible. Premium voices coming soon.

📩 Want other languages or texts? Drop a comment!

#LearnFrench #Bilingual #LanguageLearning #французский
```

## Tags by Language Pair (NO # symbols)

### RU → ES LATAM
```
learn Spanish, Spanish for Russians, bilingual, language learning, passive learning, español latino, испанский язык, учу испанский, español argentino, Russian Spanish, изучение языков, {Author}, {Title}
```

### RU → EN
```
learn English, English for Russians, bilingual, language learning, passive learning, английский язык, учу английский, Russian English, изучение языков, {Author}, {Title}
```

### EN → ES LATAM
```
learn Spanish, Spanish for English speakers, bilingual, language learning, passive learning, español latino, español argentino, English Spanish, aprender español, {Author}, {Title}
```

### EN → RU
```
learn Russian, Russian for English speakers, bilingual, language learning, passive learning, русский язык, Russian language, English Russian, изучение русского, {Author}, {Title}
```

### RU → DE
```
learn German, German for Russians, bilingual, language learning, passive learning, немецкий язык, учу немецкий, Russian German, Deutsch lernen, изучение языков, {Author}, {Title}
```

### RU → FR
```
learn French, French for Russians, bilingual, language learning, passive learning, французский язык, учу французский, Russian French, apprendre français, изучение языков, {Author}, {Title}
```

## Language Codes Reference

| Code | Full Name | For Title |
|------|-----------|-----------|
| RU | Russian | RU |
| ES LATAM | Latin American Spanish | ES LATAM |
| ES | European Spanish | ES |
| EN | English | EN |
| DE | German | DE |
| FR | French | FR |
| PT-BR | Brazilian Portuguese | PT-BR |

## Important Rules

1. **Title**: Always `[Bilingual][SOURCE→TARGET] Author - Title` format
2. **Author/Title**: MUST be in English (for international reach)
3. **Description**: Always in English
4. **Tags**: NO hashtag symbols (YouTube adds them)
5. **Avoid**: Words "audiobook", "book", "read" (copyright risk)
6. **Focus**: Language learning angle

## Example Interaction

**User:** залей видео Билет на планету Транай на ютуб

**Claude:**
```
📺 YouTube Upload Command:

python3 scripts/youtube_upload.py "Билет на планету Транай_ru_es-latam" --title "[Bilingual][RU→ES LATAM] Sheckley - Ticket to Tranai"

The script will:
1. Show channel name for confirmation
2. Let you select a playlist
3. Ask for final confirmation before upload
```

**User:** upload The Veldt by Bradbury, English to Spanish

**Claude:**
```
📺 YouTube Upload Command:

python3 scripts/youtube_upload.py "The Veldt_en_es-latam" --title "[Bilingual][EN→ES LATAM] Bradbury - The Veldt"
```
