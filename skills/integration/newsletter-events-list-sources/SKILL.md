---
name: newsletter-events-list-sources
description: List all configured event sources (Instagram, web aggregators)
---

<essential_principles>
## Configuration Location

All sources are stored in `~/.config/local-media-tools/sources.yaml`.

## Source Types

| Type | Filter Keyword | Description |
|------|----------------|-------------|
| Instagram | `instagram`, `ig` | @handle accounts |
| Web | `web` | Event aggregator websites |

**Note:** Facebook events are not configured sources. Pass event URLs directly to `/research`.

## Output Format

Sources are displayed in grouped tables with relevant metadata for each type.
</essential_principles>

<intake>
What sources do you want to list?

**Options:**
- `all` or blank - Show all configured sources
- `instagram` - Only Instagram accounts
- `web` - Only web aggregators

Provide filter (or press Enter for all):
</intake>

<process>
## Step 1: Parse Filter

Check if user provided a filter keyword:

```python
filter_input = user_input.strip().lower()

# Normalize filter aliases
filter_map = {
    "": "all",
    "all": "all",
    "instagram": "instagram",
    "ig": "instagram",
    "web": "web",
}

selected_filter = filter_map.get(filter_input, "all")
```

## Step 2: Load Config

```python
from pathlib import Path
import yaml

config_path = Path.home() / ".config" / "local-media-tools" / "sources.yaml"

if not config_path.exists():
    print("ERROR: sources.yaml not found. Run /newsletter-events:setup first.")
    # STOP HERE

with open(config_path) as f:
    config = yaml.safe_load(f)
```

## Step 3: Extract Sources

```python
sources = config.get("sources", {})

instagram_accounts = sources.get("instagram", {}).get("accounts", [])
web_sources = sources.get("web_aggregators", {}).get("sources", [])
```

## Step 4: Check for Empty State

```python
total_sources = len(instagram_accounts) + len(web_sources)

if total_sources == 0:
    print("No sources configured.")
    print("")
    print("To add sources: /newsletter-events:add-source @handle")
    # STOP HERE
```

## Step 5: Format and Display Tables

Display each category with appropriate columns:

**Instagram Accounts:**

| Handle | Name | Type | Location |
|--------|------|------|----------|
| @localvenue | Local Venue | music_venue | Kingston, NY |
| @themusicbar | The Music Bar | bar | - |

**Web Aggregators:**

| URL | Name | Type | Max Pages |
|-----|------|------|-----------|
| https://hvmag.com/events | HV Magazine | listing | 50 |

## Step 6: Show Summary

```
Total: N sources configured
- Instagram: X accounts
- Web: Y aggregators

To add sources: /newsletter-events:add-source @handle
To remove sources: /newsletter-events:remove-source @handle

Note: For Facebook events, pass URLs directly to /research
```

## Handling Filtered Views

If a filter was applied but that category is empty:

```
No instagram sources found.

You have:
- 1 web aggregator

To add Instagram accounts: /newsletter-events:add-source @handle
```

</process>

<success_criteria>
- [ ] Config loaded successfully
- [ ] Filter applied correctly (if provided)
- [ ] Output formatted as readable tables
- [ ] Empty states handled with helpful messages
- [ ] Summary shows totals
- [ ] Next actions suggested
</success_criteria>
