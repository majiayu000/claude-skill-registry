---
name: newsletter-events-update-event
description: Manually refresh specific event pages to update event data
---

<essential_principles>
## Purpose

Re-scrape specific event page URLs to update event data in the database. Use this
when event details have changed (date, time, venue, etc.) or to verify event
information.

## When to Use

- Event details have changed and need updating
- You want to verify/refresh event data from the source
- A page was scraped but events weren't extracted correctly

## URL Handling

- URLs are normalized before lookup (trailing slashes, tracking params stripped)
- The normalized URL must match what's in the `scraped_pages` table
- If URL not found in database, it will be scraped as new

## Multi-Event Pages

Some pages contain multiple events (e.g., weekly schedules). When updating:
- ALL events with matching `source_url` are updated
- New events on the page are created
- Events no longer on the page are NOT deleted (they may have passed)
</essential_principles>

<intake>
Which event page(s) do you want to refresh?

**Examples:**
- `https://hvmag.com/events/jazz-night-jan-20`
- `https://example.com/event/123 https://example.com/event/456`

Provide the URL(s):
</intake>

<process>
## Step 1: Parse URLs

Extract all URLs from user input.

```python
import re

url_pattern = r'https?://[^\s<>"\']+'
urls = re.findall(url_pattern, user_input)

if not urls:
    print("ERROR: No valid URLs found in input")
    # STOP HERE
```

## Step 2: Normalize and Lookup

```python
from scripts.url_utils import normalize_url
from schemas.sqlite_storage import SqliteStorage
from pathlib import Path

db_path = Path.home() / ".config" / "local-media-tools" / "data" / "events.db"
storage = SqliteStorage(db_path)

# Normalize URLs
url_map = {normalize_url(url): url for url in urls}

# Check which URLs exist in scraped_pages
for normalized_url, original_url in url_map.items():
    # Find the source_name for this URL (query scraped_pages)
    page_record = None
    with storage._connection() as conn:
        row = conn.execute(
            "SELECT source_name, url, scraped_at FROM scraped_pages WHERE url = ?",
            (normalized_url,),
        ).fetchone()
        if row:
            page_record = dict(row)

    if page_record:
        print(f"ℹ Found: {original_url}")
        print(f"  Source: {page_record['source_name']}")
        print(f"  Last scraped: {page_record['scraped_at']}")
    else:
        print(f"⚠ Not found in database: {original_url}")
        print(f"  Will be scraped as new URL")
```

## Step 3: Re-scrape Pages

```python
from scripts.scrape_firecrawl import FirecrawlClient, FirecrawlError

client = FirecrawlClient()
scraped_pages = []

for normalized_url, original_url in url_map.items():
    try:
        page = client.scrape_url(original_url)
        scraped_pages.append({
            "normalized_url": normalized_url,
            "original_url": original_url,
            "markdown": page.get("markdown", ""),
            "title": page.get("title", ""),
        })
        print(f"✓ Scraped: {original_url}")
    except FirecrawlError as e:
        print(f"✗ Failed to scrape {original_url}: {e}")
```

## Step 4: Extract Events (Claude)

For each scraped page, analyze the markdown and extract events.

**For each page:**
1. Read the markdown content
2. Extract event details (title, date, time, venue, description, price, etc.)
3. Create Event objects with `source_url` set to the original URL

```python
from schemas.event import Event, Venue, EventSource

event = Event(
    title=extracted_title,
    venue=Venue(name=venue_name, address=venue_address),
    event_date=parsed_date,
    start_time=parsed_time,
    source=EventSource.WEB_AGGREGATOR,
    source_url=page["original_url"],
    description=description,
    price=price,
    ticket_url=ticket_url,
    confidence=0.9,  # Higher confidence for manual refresh
    needs_review=False,  # User explicitly requested this update
)
```

## Step 5: Update Database

For each page, update or create events, then update the scraped_pages record.

```python
from schemas.event import EventCollection

for page in scraped_pages:
    events_from_page = events_by_url.get(page["original_url"], [])

    # 1. Save/update events
    if events_from_page:
        collection = EventCollection(events=events_from_page)
        result = storage.save(collection)
        print(f"  → {len(events_from_page)} events: {result.saved} new, {result.updated} updated")
    else:
        print(f"  → No events extracted from page")

    # 2. Update scraped_pages record
    # Determine source_name (from existing record or ask user)
    if page_record:
        source_name = page_record["source_name"]
    else:
        # For new URLs, try to infer source from config or use domain
        from urllib.parse import urlparse
        source_name = urlparse(page["original_url"]).netloc

    storage.save_scraped_page(
        source_name=source_name,
        url=page["normalized_url"],
        events_count=len(events_from_page),
    )

print(f"\n✓ Update complete")
```

## Step 6: Report Results

Display summary of what was updated:

| URL | Events Found | New | Updated |
|-----|--------------|-----|---------|
| hvmag.com/events/jazz | 1 | 0 | 1 |
| example.com/schedule | 5 | 2 | 3 |

</process>

<success_criteria>
- [ ] All URLs parsed from input
- [ ] URLs normalized for consistent lookup
- [ ] Pages re-scraped via Firecrawl
- [ ] Events extracted from markdown
- [ ] Events saved BEFORE URL marked as scraped
- [ ] scraped_pages records updated with new timestamp
- [ ] Summary shown to user
</success_criteria>
