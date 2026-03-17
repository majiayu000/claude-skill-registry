---
name: news-feeds
description: Fetch latest news headlines from major RSS feeds (BBC, Reuters, AP, Al Jazeera, NPR, The Guardian, DW). No API keys required.
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---

# News Feeds Skill

Fetch current news headlines and summaries from major international RSS feeds. Zero API keys, zero dependencies — uses only Python stdlib and HTTP.

## Available Commands

### Command: news
**What it does:** Fetch latest headlines from all configured feeds (or a specific source).
**How to execute:**
```bash
python3 {baseDir}/scripts/news.py
```

### Command: news from a specific source
**What it does:** Fetch headlines from one source only.
**How to execute:**
```bash
python3 {baseDir}/scripts/news.py --source bbc
python3 {baseDir}/scripts/news.py --source reuters
python3 {baseDir}/scripts/news.py --source ap
python3 {baseDir}/scripts/news.py --source guardian
python3 {baseDir}/scripts/news.py --source aljazeera
python3 {baseDir}/scripts/news.py --source npr
python3 {baseDir}/scripts/news.py --source dw
```

### Command: news by topic
**What it does:** Fetch headlines filtered to a specific topic/keyword.
```bash
python3 {baseDir}/scripts/news.py --topic "climate"
python3 {baseDir}/scripts/news.py --source bbc --topic "ukraine"
```

### Command: news with more items
**What it does:** Control how many items per feed (default 8).
```bash
python3 {baseDir}/scripts/news.py --limit 20
```

### Command: list sources
**What it does:** Show all available feed sources and their categories.
```bash
python3 {baseDir}/scripts/news.py --list-sources
```

## Available Sources

| Source       | Categories                                      |
|-------------|------------------------------------------------|
| bbc         | top, world, business, tech, science, health     |
| reuters      | top, world, business, tech, science, health     |
| ap          | top                                             |
| guardian    | top, world, business, tech, science             |
| aljazeera   | top                                             |
| npr         | top                                             |
| dw          | top                                             |

## When to Use

- User asks for latest news, current events, headlines
- User wants a news briefing or daily digest
- User asks "what's happening in the world"
- User asks about news on a specific topic
- User asks for a morning briefing

## Output Format

Returns markdown with headlines, short descriptions, publication times, and links. Grouped by source.
