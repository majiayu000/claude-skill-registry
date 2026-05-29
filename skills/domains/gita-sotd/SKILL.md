---
name: gita-sotd
description: >
  Get the Bhagavad Gita Slok of the Day (SOTD) or fetch specific verses.
  Use when the user asks for a Gita verse, slok, daily wisdom from the Gita,
  Hindu scripture quotes, or anything related to the Bhagavad Gita text.
  Supports Sanskrit text, transliteration, and translations from multiple scholars.
---

# Bhagavad Gita Slok of the Day

Fetch verses from the Bhagavad Gita using the free [vedicscriptures API](https://vedicscriptures.github.io/).

## Usage

Run the script to get a slok:

```bash
# Daily slok (deterministic, changes each day)
python3 scripts/fetch_slok.py

# Specific verse
python3 scripts/fetch_slok.py --chapter 2 --verse 47

# Random verse
python3 scripts/fetch_slok.py --random

# Different translator (prabhu, siva, purohit, gambir, chinmay, etc.)
python3 scripts/fetch_slok.py --translator siva

# Raw JSON output
python3 scripts/fetch_slok.py --json
```

## Available Translators

- `prabhu` - A.C. Bhaktivedanta Swami Prabhupada (default)
- `siva` - Swami Sivananda
- `purohit` - Shri Purohit Swami
- `gambir` - Swami Gambirananda
- `chinmay` - Swami Chinmayananda
- `tej` - Swami Tejomayananda (Hindi)
- `rams` - Swami Ramsukhdas (Hindi)
- `raman` - Sri Ramanuja

## Output Format

The script outputs formatted markdown with:

- Chapter and verse reference
- Sanskrit text (optional)
- Transliteration
- English/Hindi translation with author attribution

## API Reference

Base URL: `https://vedicscriptures.github.io`

- `GET /slok/:chapter/:verse` - Get specific verse
- `GET /chapter/:ch` - Get chapter info
- `GET /chapters` - List all chapters

The Bhagavad Gita has 18 chapters with 700 total verses.
