---
name: web-search
description: This skill should be used when users need to search the web for information, find current content, look up news articles, search for images, or find videos. It uses duckse (DDGS-based CLI) to return clean results in pretty text or JSON.
---

# Web Search (duckse)

## Overview

Gunakan `duckse` untuk metasearch web berbasis DDGS. Skill ini mendukung:
- `text`, `news`, `images`, `videos`, `books`
- filter waktu, region, safe search, backend
- output rapi (default) atau JSON (`--json`)
- URL final via redirect (`--expand-url`)

## When to Use This Skill

Gunakan skill ini saat user meminta:
- pencarian web umum
- berita terbaru/topik tertentu
- pencarian gambar/video
- riset cepat dengan sumber URL
- fact-checking berbasis hasil web

## Prerequisites

Pastikan `duckse` tersedia:

```bash
duckse --help
```

Jika belum ada, install:

```bash
curl -sSL https://raw.githubusercontent.com/dwirx/duckse/main/scripts/install.sh | bash
```

## Core Commands

### 1. Basic Web Search

```bash
duckse "<query>"
```

Contoh:

```bash
duckse "python asyncio tutorial"
```

### 2. Limit Results

```bash
duckse "<query>" --max-results <N>
```

Contoh:

```bash
duckse "machine learning frameworks" --max-results 20
```

### 3. Time Filter

```bash
duckse "<query>" --timelimit <d|w|m|y>
```

Contoh:

```bash
duckse "artificial intelligence news" --type news --timelimit w
```

### 4. News Search

```bash
duckse "<query>" --type news
```

Contoh:

```bash
duckse "climate change" --type news --timelimit w --max-results 15
```

### 5. Image Search

```bash
duckse "<query>" --type images
```

Contoh:

```bash
duckse "sunset over mountains" --type images --max-results 20
```

Filter image:

```bash
duckse "landscape photos" --type images --size Large
duckse "abstract art" --type images --color Blue
duckse "icons" --type images --type-image transparent
duckse "wallpapers" --type images --layout Wide
```

### 6. Video Search

```bash
duckse "<query>" --type videos
```

Contoh:

```bash
duckse "python tutorial" --type videos --max-results 15
```

Filter video:

```bash
duckse "cooking recipes" --type videos --duration short
duckse "documentary" --type videos --resolution high
```

### 7. Books Search

```bash
duckse "<query>" --type books --backend annasarchive
```

Contoh:

```bash
duckse "sea wolf jack london" --type books --max-results 10
```

### 8. Region and SafeSearch

```bash
duckse "<query>" --region us-en --safesearch moderate
```

Contoh:

```bash
duckse "local news" --type news --region us-en --safesearch on
```

### 9. JSON and Final URL

JSON output:

```bash
duckse "quantum computing" --json
```

Resolve final URL:

```bash
duckse "beritakan di indonesia hari ini" --expand-url --max-results 5
```

## Valid Backends by Type

- `text`: `bing, brave, duckduckgo, google, grokipedia, mojeek, yandex, yahoo, wikipedia, auto`
- `images`: `duckduckgo, auto`
- `videos`: `duckduckgo, auto`
- `news`: `bing, duckduckgo, yahoo, auto`
- `books`: `annasarchive, auto`

## Common Usage Patterns

### Research Topic

```bash
duckse "machine learning basics" --max-results 15
duckse "machine learning" --type news --timelimit m --max-results 15
duckse "machine learning tutorial" --type videos --max-results 10
```

### Current Events Monitoring

```bash
duckse "climate summit" --type news --timelimit d --max-results 20
```

### Fact-Checking

```bash
duckse "specific claim to verify" --type news --timelimit w --max-results 20 --expand-url
```

## Quick Reference

Command format:

```bash
duckse "<query>" [options]
```

Essential options:
- `--type` (`text|images|videos|news|books`)
- `--max-results`
- `--timelimit` (`d|w|m|y`)
- `--region`
- `--safesearch` (`on|moderate|off`)
- `--backend`
- `--json`
- `--expand-url`
- `--proxy`, `--timeout`, `--verify`

## Best Practices

1. Gunakan query spesifik
2. Pakai `--timelimit` untuk informasi terbaru
3. Pakai `--expand-url` jika butuh URL final
4. Gunakan `--json` untuk otomasi/pipeline
5. Sesuaikan `--max-results` (mulai 10-20)

## Troubleshooting

- `duckse: command not found`
  - tambahkan PATH: `export PATH="$HOME/.local/bin:$PATH"`
- backend tidak valid
  - sesuaikan dengan daftar backend per type
- hasil kosong
  - longgarkan query atau hapus filter waktu
- timeout/network
  - ulangi, tambah `--timeout`, atau gunakan `--proxy`

## Development Fallback

Jika sedang develop lokal tanpa binary terpasang global:

```bash
uv run python main.py "<query>" [opsi yang sama]
```
