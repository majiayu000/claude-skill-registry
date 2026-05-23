---
name: research-topic
description: Crawl and collect resources for a financial research topic using Exa with full HTML and chart extraction.
allowed-tools: Bash, Read, Write
argument-hint: "<topic>"
---

# Research Topic Crawler

Collect raw resources (articles, charts, tables) for a financial research topic using the optimized Exa crawler.

**Key Features:**
- Full HTML content with tags preserved
- Automatic chart/image URL extraction and download
- Organized by source domain

## Usage

```bash
/research-topic "seasonality in financial assets"
/research-topic "FX macro correlations commodity currencies"
/research-topic "momentum factor investing"
```

## Workflow

### Phase 1: Initialize Topic Folder

```bash
cd /home/adesola/EpochDev/ClaudeCodeResearch
source .venv/bin/activate
python report_notes/scripts/init_topic.py "$TOPIC"
```

This creates:
```
report_notes/<topic_slug>/
├── manifest.json
├── sources/
│   ├── quantpedia/
│   ├── academic/
│   ├── broker_research/
│   ├── market_data/
│   └── misc/
└── images/
```

### Phase 2: Search and Crawl Sources

Use the optimized Exa crawler script which:
- Preserves HTML tags (`includeHtmlTags: true`)
- Extracts image URLs (`extras.imageLinks: 30`)
- Downloads charts automatically
- Organizes by domain

**General Search (broad coverage):**
```bash
python report_notes/scripts/exa_crawler.py search "$TOPIC" --num 15 -o /tmp/search_results.json
```

**Domain-Specific Search (academic/quantitative):**
```bash
python report_notes/scripts/exa_crawler.py search "$TOPIC academic research" --num 10 -o /tmp/academic_results.json
```

**USDCAD/Oil Example:**
```bash
python report_notes/scripts/exa_crawler.py search "USDCAD crude oil WTI correlation" --num 10 -o /tmp/usdcad_results.json
```

### Phase 3: Save Sources to Topic

Process search results and save with chart downloads:

```python
import json
import sys
sys.path.insert(0, 'report_notes/scripts')
from exa_crawler import save_source_to_topic
from pathlib import Path
from datetime import datetime, timezone

# Load search results
with open('/tmp/search_results.json') as f:
    results = json.load(f)

topic_dir = Path('report_notes/<topic_slug>')

# Save each source with chart downloads
for r in results:
    crawl_result = {
        'url': r['url'],
        'title': r['title'],
        'author': r.get('author'),
        'text': r.get('text', ''),
        'image': r.get('image'),
        'imageLinks': r.get('imageLinks', []),
        'links': r.get('links', []),
        'crawled_at': datetime.now(timezone.utc).isoformat(),
        'source': 'exa_search',
    }
    save_source_to_topic(topic_dir, crawl_result, download_images=True)
```

### Phase 4: Crawl Specific URLs

For individual URLs not in search results:

```bash
# Crawl single URL with full content
python report_notes/scripts/exa_crawler.py crawl "<url>" --json -o /tmp/crawl_result.json

# Then save to topic using Python
```

### Phase 5: Show Status

```bash
python -c "
import json
from pathlib import Path
m = json.load(open('report_notes/<topic_slug>/manifest.json'))
print(f'Sources: {m[\"stats\"][\"total_sources\"]}')
print(f'Charts: {m[\"stats\"][\"total_charts\"]}')
for s in m['sources']:
    print(f'  - [{len(s.get(\"charts\",[]))} charts] {s[\"title\"][:50]}...')
"
```

## Exa Crawler Script Reference

Located at: `report_notes/scripts/exa_crawler.py`

### Commands

| Command | Description |
|---------|-------------|
| `search "<query>" --num N` | Search and crawl N results |
| `crawl "<url>"` | Crawl single URL with full content |
| `topic <slug> <urls...>` | Crawl URLs and save to topic |

### API Parameters Used

The script uses optimal Exa API parameters:

```json
{
  "text": {
    "maxCharacters": 50000,
    "includeHtmlTags": true
  },
  "extras": {
    "imageLinks": 30,
    "links": 20
  },
  "livecrawl": "preferred"
}
```

### What Gets Extracted

| Field | Description |
|-------|-------------|
| `text` | Full content with HTML tags |
| `imageLinks` | All image URLs (charts, figures) |
| `links` | Outbound URLs for follow-up |
| `image` | Main page image |
| `author` | Article author |

## Output Structure

```
report_notes/<topic_slug>/
├── manifest.json
├── sources/
│   ├── quantpedia/
│   │   ├── 001_strategy_name.md
│   │   └── 001_strategy_name/
│   │       └── charts/
│   │           ├── chart_01.png
│   │           └── chart_02.jpg
│   ├── academic/
│   ├── broker_research/
│   ├── market_data/
│   └── misc/
└── images/
    └── chart_index.json
```

## Manifest Format

```json
{
  "topic": "FX macro correlations",
  "slug": "fx_macro_correlations",
  "sources": [
    {
      "url": "https://...",
      "domain": "broker_research",
      "title": "USDCAD Oil Correlation",
      "file": "sources/broker_research/001_usdcad_oil.md",
      "charts": ["sources/.../charts/chart_01.png"],
      "tables": 0
    }
  ],
  "stats": {
    "total_sources": 15,
    "total_charts": 62
  }
}
```

## Source Markdown Format

Each source is saved with frontmatter:

```yaml
---
url: https://...
title: Article Title
domain: broker_research
crawled_at: 2026-02-04T01:00:00+00:00
chart_count: 5
image_links:
  - https://example.com/chart1.png
  - https://example.com/chart2.jpg
outbound_links:
  - https://related-article.com
---

<h2>Article Content</h2>
<p>Full HTML preserved...</p>
```

## Domain Categories

| Domain | Folder | Sources |
|--------|--------|---------|
| quantpedia.com | `quantpedia/` | Strategy research |
| ssrn.com, nber.org, arxiv.org | `academic/` | Academic papers |
| forex.com, oanda.com | `broker_research/` | Broker analysis |
| barchart.com, tradingview.com | `market_data/` | Charts, data |
| investopedia.com, babypips.com | `educational/` | Tutorials |
| Other | `misc/` | Everything else |

## Tips

1. **Start with broad search** - Then narrow with domain-specific queries
2. **Charts download automatically** - Script filters logos/icons from real charts
3. **Check manifest.json** - Track progress and chart counts
4. **HTML is preserved** - Tables, links, formatting all retained
5. **Image URLs in frontmatter** - Even if download fails, URLs are saved
