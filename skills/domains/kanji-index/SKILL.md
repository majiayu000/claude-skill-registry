---
name: kanji-index
description: Guidelines for maintaining the kanji index feature. Covers kanji ID assignment, index updates, and troubleshooting.
---

# Kanji Index Maintenance

The kanji index allows users to click on any kanji in a dictionary headword to find all other entries containing that same kanji.

## How It Works

1. **Headword kanji** are linked to kanji index pages
2. **Kanji index pages** list all entries containing that kanji
3. **Entry lists** are sorted by reading (hiragana order)

## Directory Structure

```
kanji/
├── kanji_list.json       # Master list: kanji → kanji_id mapping
├── kanji_extracted.json  # Temporary: extracted kanji needing IDs
├── 00001_jin_hito_person.json  # Entry list for 人
├── 00002_nichi_hi_day.json     # Entry list for 日
└── ...

docs/kanji/
├── 00001_jin_hito_person.html  # HTML page for 人
├── 00002_nichi_hi_day.html     # HTML page for 日
└── ...
```

## Kanji ID Format

Format: `{5-digit}_{onyomi}_{kunyomi}_{gloss}`

- **5-digit**: Sequential number (00001, 00002, ...)
- **onyomi**: Most common on'yomi in romaji (or "none")
- **kunyomi**: Most common kun'yomi in romaji without okurigana (or "none")
- **gloss**: Single English word for primary meaning

### Examples

| Kanji | Kanji ID |
|-------|----------|
| 人 | 00001_jin_hito_person |
| 日 | 00002_nichi_hi_day |
| 大 | 00003_dai_oo_big |
| 畑 | 00004_none_hatake_field |
| 茶 | 00005_cha_none_tea |

### Romaji Rules

- Long vowels: "ou" not "ō" (e.g., 高 → "kou")
- Voiced: "ga", "za", "da", "ba" (e.g., 学 → "gaku")
- No okurigana in kun'yomi (e.g., 高い → "taka", not "takai")

## Assigning New Kanji IDs

When new entries introduce kanji not in `kanji_list.json`:

1. **Detect new kanji**:
   ```bash
   python3 build/update_kanji_index.py --check-new
   ```

2. **Assign readings and gloss** using your knowledge:
   - Most common on'yomi
   - Most common kun'yomi (without okurigana)
   - Single-word English gloss

3. **Update kanji_list.json**:
   ```json
   {
     "新": {
       "kanji_id": "00123_shin_atara_new",
       "onyomi": "shin",
       "kunyomi": "atara",
       "gloss": "new"
     }
   }
   ```

4. **Rebuild**:
   ```bash
   python3 build/build_flat.py
   ```

## Common Tasks

### Check for New Kanji
```bash
python3 build/update_kanji_index.py --check-new
```

### Rebuild All Kanji JSON Files
```bash
python3 build/update_kanji_index.py --rebuild-all
```

### Rebuild Kanji HTML Pages
```bash
python3 build/build_kanji_html.py
```

### Full Site Build (includes kanji)
```bash
python3 build/build_flat.py
```

## Troubleshooting

### "Warning: X kanji need IDs assigned"

New kanji were found in entries. Assign IDs manually:
1. Run `--check-new` to see the full list
2. For each kanji, determine on'yomi, kun'yomi, gloss
3. Add to `kanji/kanji_list.json`
4. Rebuild

### Missing kanji index page

Check that:
1. Kanji is in `kanji/kanji_list.json`
2. JSON file exists: `kanji/{kanji_id}.json`
3. Run `python3 build/build_kanji_html.py`

### Kanji link not appearing in headword

Check that:
1. Kanji is in `kanji/kanji_list.json`
2. Entry HTML was rebuilt after kanji was added

### Entry count wrong on kanji page

Rebuild the kanji JSON file:
```bash
python3 build/update_kanji_index.py --rebuild-all
python3 build/build_kanji_html.py
```

## File Formats

### kanji_list.json
```json
{
  "metadata": {
    "description": "Index mapping kanji characters to their kanji index IDs",
    "generated": "2026-01-22T10:30:00Z",
    "total_kanji": 1500
  },
  "kanji": {
    "人": {
      "kanji_id": "00001_jin_hito_person",
      "onyomi": "jin",
      "kunyomi": "hito",
      "gloss": "person"
    }
  }
}
```

### Individual kanji JSON
```json
{
  "metadata": {
    "kanji": "人",
    "kanji_id": "00001_jin_hito_person",
    "onyomi": "jin",
    "kunyomi": "hito",
    "gloss": "person",
    "entry_count": 245,
    "generated": "2026-01-22T10:30:00Z"
  },
  "entries": [
    {
      "id": "01234_akunin",
      "headword": "{悪|あく}{人|にん}",
      "reading": "あくにん",
      "gloss": "villain, bad person"
    }
  ]
}
```

## Design Decisions

### Why invisible links?
- Preserves clean headword appearance
- Users discover feature through tooltip
- No visual clutter

### Why romaji in kanji IDs?
- ASCII-safe file names
- Human-readable
- Easy to search and sort

### Why sort by reading?
- Natural Japanese ordering (gojuon)
- Consistent with how dictionaries organize entries
- Helps users find related words
