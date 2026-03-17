---
name: tautulli-analytics
description: Work with Tautulli analytics integration for Plex streaming metrics. Use when building analytics features, adding charts, fetching streaming data, working with watch history, or analyzing user activity patterns. Covers both the Tautulli client (API communication) and analytics module (data collection and storage).
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Tautulli Analytics Integration

This skill helps with Tautulli analytics features in homescreen-hero. Tautulli provides streaming metrics and watch history from Plex servers.

## Key Files

- [tautulli_client.py](homescreen_hero/core/integrations/tautulli_client.py) - Tautulli API client
- [tautulli_analytics.py](homescreen_hero/core/integrations/tautulli_analytics.py) - Analytics collection logic
- [analytics.py](homescreen_hero/core/db/analytics.py) - Database operations for analytics
- [analytics.py](homescreen_hero/web/routers/analytics.py) - API endpoints

## Tautulli Client Overview

The `TautulliClient` wraps the Tautulli API v2. It handles:
- API authentication via API key in URL params
- Response parsing (Tautulli wraps responses in `{"response": {"result": "success", "data": ...}}`)
- Error handling for timeouts, auth failures, HTTP errors

### Key Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `ping()` | Health check | `(bool, Optional[str])` - success status and error message |
| `get_libraries()` | Get Plex libraries | List of library dicts with `section_id` |
| `get_collection_stats(rating_key, query_days)` | Watch stats for a collection | Dict with `total_plays`, `total_duration` |
| `get_history(length, start)` | Watch history entries | List of history dicts with timestamps |
| `get_user_watch_time_stats(query_days)` | User watch stats | List of user stats |
| `get_plays_by_date(time_range, y_axis)` | Play counts by date | Dict with `categories` (dates) and `series` (play data) |
| `get_plays_by_hourofday(time_range, y_axis)` | Play counts by hour | Dict with `categories` (hours) and `series` |
| `get_plays_by_stream_type(time_range, y_axis)` | Plays by stream type with concurrent streams | Dict with stream type data including max concurrent |

### Configuration

Tautulli requires:
- `HSH_TAUTULLI_API_KEY` environment variable (or in config.yaml)
- `HSH_TAUTULLI_BASE_URL` environment variable (default: `http://localhost:8181`)
- `enabled: true` in config.yaml under `tautulli` section

## Analytics Module

The `tautulli_analytics.py` module collects watch statistics and stores them in SQLite:

### Main Functions

**`collect_analytics_for_collections(config, collection_names, rotation_id)`**
- Collects watch stats for specified collections
- Finds collections in Plex libraries using rating_key
- Aggregates stats from all items in each collection
- Stores snapshots in the database via `record_collection_analytics()`
- Returns summary dict with `collected`, `failed`, and `total_collections`

**`collect_analytics_for_all_active(config)`**
- Collects analytics for all currently promoted collections
- Queries Plex for collections with visibility > 0
- Uses `collect_analytics_for_collections()` internally

### Data Flow

1. **Find collection in Plex** - Search enabled libraries for collection by name
2. **Get rating_key** - Extract Plex's internal ID for the collection
3. **Query Tautulli** - Use rating_key to get watch stats from Tautulli API
4. **Aggregate** - Sum stats across all items in the collection
5. **Store** - Save snapshot to `collection_analytics` table in SQLite

## Common Tasks

### Adding a New Chart

When adding a new chart to the frontend:
1. Check if the Tautulli API endpoint exists in `tautulli_client.py`
2. Add method to client if needed (follow pattern of existing methods)
3. Create API endpoint in `homescreen_hero/web/routers/analytics.py`
4. Fetch data in React component using the new endpoint
5. Use Recharts components to visualize

### Testing Tautulli Connection

```python
from homescreen_hero.core.integrations.tautulli_client import get_tautulli_client
from homescreen_hero.core.config.loader import load_config

config = load_config()
client = get_tautulli_client(config)
if client:
    success, error = client.ping()
    print(f"Tautulli connection: {'OK' if success else f'Failed - {error}'}")
```

### Fetching Watch Stats

```python
# Get stats for a specific collection (by rating_key)
stats = client.get_collection_stats(rating_key=12345, query_days=30)
print(f"Total plays: {stats['total_plays']}")

# Get play history
history = client.get_history(length=100)
for entry in history:
    print(f"{entry['user']}: {entry['title']} at {entry['date']}")
```

## API Response Formats

### get_collection_stats
```json
{
  "total_plays": 42,
  "total_duration": 7200,
  "total_time": "2h 0m"
}
```

### get_plays_by_date
```json
{
  "categories": ["2024-01-01", "2024-01-02", ...],
  "series": {
    "Movies": [5, 8, 3, ...],
    "TV": [12, 15, 10, ...]
  }
}
```

### get_plays_by_stream_type
```json
{
  "categories": ["2024-01-01", "2024-01-02", ...],
  "series": {
    "Direct Play": [5, 8, ...],
    "Direct Stream": [3, 2, ...],
    "Transcode": [1, 4, ...],
    "Concurrent Streams": [8, 12, ...]  // Max concurrent per day
  }
}
```

## Database Schema

Analytics are stored in `collection_analytics` table:
- `collection_name` - Name of the collection
- `plex_library` - Library name (Movies, TV Shows, etc.)
- `rating_key` - Plex rating key
- `total_plays` - Total play count
- `total_duration_seconds` - Total watch time in seconds
- `unique_users` - Count of unique users (nullable)
- `rotation_id` - FK to rotation that triggered collection (nullable)
- `collected_at` - Timestamp of collection
- `extra_data` - JSON field for additional metadata

## Notes

- Tautulli tracks stats per-item, not per-collection
- Analytics module aggregates item-level stats to collection-level
- Concurrent streams calculation requires analyzing overlapping watch history timestamps
- All API methods include error handling and logging
- Use `logger.debug()` for API requests, `logger.info()` for successful operations, `logger.error()` for failures
