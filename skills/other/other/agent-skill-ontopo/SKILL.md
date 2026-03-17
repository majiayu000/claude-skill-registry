---
name: ontopo
version: 1.0.0
description: Search Israeli restaurants, check table availability, view menus, and get booking links on Ontopo. Use for "restaurant reservation", "table booking", "ontopo", "where to eat in Israel", "מסעדה", "הזמנת שולחן", "תפריט", "ארוחת ערב", "אונטופו", "איפה לאכול".
author: Alex Polonsky (https://github.com/alexpolonsky)
homepage: https://github.com/alexpolonsky/agent-skill-ontopo
metadata: {"openclaw": {"emoji": "🍽️", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}, "install": [{"kind": "uv", "package": "httpx", "label": "Install httpx via pip/uv"}]}}
---

# Ontopo Restaurant Search

Search Israeli restaurants, check table availability, view menus, and get direct booking links on the Ontopo platform.

> **Disclaimer**: This is an unofficial tool, not affiliated with or endorsed by Ontopo. Availability data queries APIs that power the website and may not reflect actual availability. This tool does NOT place reservations - it generates booking links for manual confirmation on Ontopo's website. Provided "as is" without warranty of any kind.

## Quick Start

```bash
# Search for a restaurant
python3 {baseDir}/scripts/ontopo-cli.py search "taizu"

# Find available restaurants for tonight
python3 {baseDir}/scripts/ontopo-cli.py available tomorrow 19:00 --city tel-aviv
```

## Commands

### cities
List supported cities.
```bash
python3 {baseDir}/scripts/ontopo-cli.py cities
python3 {baseDir}/scripts/ontopo-cli.py cities --json
```

### categories
List venue categories.
```bash
python3 {baseDir}/scripts/ontopo-cli.py categories
```

### search
Find restaurants by name.
```bash
python3 {baseDir}/scripts/ontopo-cli.py search "taizu"
python3 {baseDir}/scripts/ontopo-cli.py search "sushi" --city tel-aviv
python3 {baseDir}/scripts/ontopo-cli.py search "taizu" --json
```

### available
Find venues with availability for date and time. Date and time are POSITIONAL arguments.
```bash
python3 {baseDir}/scripts/ontopo-cli.py available tomorrow 19:00
python3 {baseDir}/scripts/ontopo-cli.py available tomorrow 20:00 --city tel-aviv
python3 {baseDir}/scripts/ontopo-cli.py available +3 19:00 --party-size 4
```

### check
Check availability at specific venue. Supports venue name or ID.
```bash
python3 {baseDir}/scripts/ontopo-cli.py check taizu tomorrow 19:00
python3 {baseDir}/scripts/ontopo-cli.py check taizu +2 20:00
python3 {baseDir}/scripts/ontopo-cli.py check 36960535 tomorrow 19:00 --party-size 4
```

### range
Check availability across date range. Times is OPTIONAL (defaults to 19:00,20:00).
```bash
python3 {baseDir}/scripts/ontopo-cli.py range taizu tomorrow +3
python3 {baseDir}/scripts/ontopo-cli.py range 36960535 tomorrow +5 --times "18:00,19:00,20:00"
python3 {baseDir}/scripts/ontopo-cli.py range taizu +1 +7 --party-size 4
```

### menu
View venue menu with optional filters.
```bash
python3 {baseDir}/scripts/ontopo-cli.py menu 66915792
python3 {baseDir}/scripts/ontopo-cli.py menu 66915792 --section drinks
python3 {baseDir}/scripts/ontopo-cli.py menu 66915792 --search "pasta" --max-price 100
```

### info
Get venue details.
```bash
python3 {baseDir}/scripts/ontopo-cli.py info 36960535
python3 {baseDir}/scripts/ontopo-cli.py info 66915792 --json
```

### url
Get booking URL for venue.
```bash
python3 {baseDir}/scripts/ontopo-cli.py url 36960535
python3 {baseDir}/scripts/ontopo-cli.py url 66915792 --locale he
```

## Options Reference

| Option | Commands | Description |
|--------|----------|-------------|
| `--json` | all | Output in JSON format |
| `--locale` | search, info, url | Language: en or he |
| `--city` | available, search | City filter (tel-aviv, jerusalem, etc.) |
| `--party-size` | available, check, range | Number of guests (default: 2) |
| `--times` | range | Comma-separated times (default: 19:00,20:00) |
| `--section` | menu | Filter by menu section |
| `--search` | menu | Search menu items by name |
| `--min-price` | menu | Minimum price filter |
| `--max-price` | menu | Maximum price filter |

## Date/Time Formats

**Dates**: `YYYY-MM-DD`, `today`, `tomorrow`, `+N` (days from now)
**Times**: `HH:MM`, `HHMM`, `7pm`, `19:30`

## Supported Cities

tel-aviv, jerusalem, haifa, herzliya, raanana, ramat-gan, netanya, ashdod, ashkelon, beer-sheva, eilat, modiin, rehovot, rishon-lezion, petah-tikva, holon, kfar-saba, hod-hasharon, caesarea

## Workflow Example

```bash
# 1. Search for restaurant
python3 {baseDir}/scripts/ontopo-cli.py search "taizu"
# Note the venue ID from results (e.g., 36960535)

# 2. Check availability
python3 {baseDir}/scripts/ontopo-cli.py check 36960535 tomorrow --time 19:00

# 3. View menu
python3 {baseDir}/scripts/ontopo-cli.py menu 36960535

# 4. Get booking link
python3 {baseDir}/scripts/ontopo-cli.py url 36960535
```

## Notes

- **Manual booking**: Generates links - complete reservation on Ontopo website
- **No API key**: Queries APIs that power the website
- **Bilingual**: Supports Hebrew and English
- **Real-time data**: Availability fetched live from Ontopo
