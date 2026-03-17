---
name: srt-translator
description: Translate video subtitles (SRT, VTT, TXT) between languages. Supports batch translation and maintains timing synchronization. Use when creating multilingual subtitles, expanding to international audiences, or translating video transcripts.
---

# SRT Translator

Translate subtitles while preserving timing and formatting.

## Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| SubRip | .srt | Most common, numbered entries |
| WebVTT | .vtt | Web standard, supports styling |
| Plain Text | .txt | Transcript without timing |

## SRT Format Reference

```
1
00:00:01,000 --> 00:00:04,000
This is the first subtitle line.

2
00:00:04,500 --> 00:00:08,000
This is the second subtitle line.
It can have multiple lines.

3
00:00:08,500 --> 00:00:12,000
And so on...
```

## Translation Guidelines

### Preserve Structure
```
ORIGINAL (English):
1
00:00:05,000 --> 00:00:08,500
Welcome to my channel!

TRANSLATED (Spanish):
1
00:00:05,000 --> 00:00:08,500
¡Bienvenidos a mi canal!

✅ Same timing, same number
✅ Natural translation (not word-for-word)
✅ Appropriate punctuation for target language
```

### Handle Line Length
```
PROBLEM: Translation is longer than original
SOLUTION: Split or abbreviate while keeping meaning

ORIGINAL:
1
00:00:10,000 --> 00:00:13,000
Click the subscribe button

GERMAN (longer):
1
00:00:10,000 --> 00:00:13,000
Klickt auf den
Abonnieren-Button

✅ Split into two lines if needed
✅ Keep within ~42 characters per line
✅ Maintain readability
```

### Cultural Adaptation
```
DON'T just translate - LOCALIZE:

Original: "That costs about 20 bucks"
Spanish (Latin America): "Eso cuesta unos 20 dólares"
Spanish (Spain): "Eso cuesta unos 20 euros"

Original: "Super Bowl Sunday"
French: "Le dimanche du Super Bowl" (keep cultural reference)
Chinese: "超级碗周日" (may need explanation)
```

## Translation Output Format

```
═══════════════════════════════════════════════════════════════
SUBTITLE TRANSLATION
Source Language: [Language]
Target Language: [Language]
Total Entries: [X]
═══════════════════════════════════════════════════════════════

TRANSLATION NOTES:
─────────────────────────────────────────────────────────────
• [Any cultural adaptations made]
• [Technical terms kept/translated]
• [Idioms adapted]

TRANSLATED SRT:
─────────────────────────────────────────────────────────────
1
00:00:00,000 --> 00:00:03,500
[Translated text]

2
00:00:04,000 --> 00:00:07,500
[Translated text]

[Continue for all entries...]

═══════════════════════════════════════════════════════════════
COPY-PASTE READY FILE:
═══════════════════════════════════════════════════════════════
[Clean SRT output without notes]
```

## How to Use

### Full SRT Translation
```
Translate this SRT file to [Language]:

[Paste SRT content]
```

### Batch Translation Request
```
Translate to multiple languages:
Languages: Spanish, French, German, Japanese, Chinese

[Paste SRT content]
```

### With Context
```
Translate this gaming video subtitle to Korean:
- Game: [Game name]
- Tone: [Casual/Professional]
- Technical terms: [Keep English / Translate]

[Paste SRT content]
```

### From Transcript to SRT
```
Convert this transcript to SRT format, then translate to [Language]:

[00:00] Hello everyone, welcome to the video.
[00:05] Today we're going to talk about...
```

## Translation Tips by Language

### Spanish (ES/LATAM)
```
• Use ustedes (LATAM) vs vosotros (Spain)
• "Click" = "Haz clic" / "Da clic"
• Keep brand names in English
• Informal tone often preferred for YouTube
```

### French (FR/CA)
```
• Tu (informal) vs Vous (formal) - YouTube usually tu
• "Subscribe" = "Abonnez-vous" / "Abonne-toi"
• Quebec French has unique expressions
• Keep anglicisms when commonly used
```

### German (DE)
```
• Du (informal) vs Sie (formal) - Du common on YouTube
• Compound words can be very long - may need line breaks
• "Daumen hoch" = Thumbs up
• Technical terms often kept in English
```

### Japanese (JA)
```
• Casual (だ/である) vs Polite (です/ます)
• YouTube content usually casual-polite mix
• Keep brand names in katakana or English
• Consider vertical text for some contexts
```

### Chinese (ZH-CN/ZH-TW)
```
• Simplified (CN) vs Traditional (TW)
• No spaces between words
• "Subscribe" = 订阅 (CN) / 訂閱 (TW)
• May need shorter text (faster reading)
```

### Korean (KO)
```
• Honorific levels matter (해요체 common for YouTube)
• "Subscribe" = 구독
• Mixing English is common and accepted
• Konglish terms often preferred
```

### Portuguese (PT-BR/PT-PT)
```
• Brazilian vs European Portuguese differ significantly
• "Você" vs "Tu" usage varies
• "Subscribe" = "Se inscreva" (BR) / "Subscreva" (PT)
• Brazilian audience is larger on YouTube
```

### Arabic (AR)
```
• Right-to-left text
• Modern Standard vs Colloquial
• Numbers may need adjustment
• Consider dialect for specific regions
```

### Hindi (HI)
```
• Devanagari script
• English mixing (Hinglish) is common
• Formal vs informal forms
• Regional language considerations
```

## Quality Checklist

Before finalizing translation:

- [ ] Timing unchanged from original
- [ ] Line numbers sequential and correct
- [ ] No missing entries
- [ ] Line length readable (≤42 chars)
- [ ] Natural language (not robotic)
- [ ] Cultural references adapted
- [ ] Technical terms consistent
- [ ] Punctuation correct for target language
- [ ] Character encoding correct (UTF-8)
- [ ] Format valid (SRT/VTT structure)

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Text overflow | Translation longer than original | Split lines, use abbreviations |
| Timing mismatch | Reading speed different | Adjust text length, not timing |
| Encoding errors | Wrong character set | Save as UTF-8 with BOM |
| Broken format | Extra line breaks | Validate SRT structure |
| Awkward phrasing | Literal translation | Localize for natural speech |

## Multi-Language Workflow

```
EFFICIENT BATCH PROCESS:

1. Get original transcript/SRT
2. Identify top languages for your audience:
   - Check YouTube Analytics for viewer locations
   - Common targets: ES, PT-BR, FR, DE, JA, KO, ZH

3. Translation priority order:
   Tier 1: Spanish, Portuguese (largest non-EN audiences)
   Tier 2: French, German (strong markets)
   Tier 3: Japanese, Korean (dedicated fandoms)
   Tier 4: Chinese, Hindi (massive populations)

4. Upload workflow:
   - YouTube: Add via Studio > Subtitles
   - Filename: videoname.[lang].srt (e.g., video.es.srt)
```

## Integration with YouTube

### Upload Subtitles
```
YouTube Studio > Video > Subtitles > Add Language

File types accepted:
- .srt (SubRip)
- .sbv (YouTube format)
- .vtt (WebVTT)
- .sub (SubViewer)

Naming convention:
videoname.en.srt (English)
videoname.es.srt (Spanish)
videoname.ja.srt (Japanese)
```

### Auto-Translate Warning
```
⚠️ YouTube's auto-translate is poor quality.
   Always provide human-quality translations for top languages.

Priority: Upload translated subtitles for your top 3-5 viewer countries.
```
