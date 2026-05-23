---
name: newsletter-events-write
description: Generate markdown newsletters from stored events. Use when the user wants to create, write, or generate a newsletter from scraped events.
---

<essential_principles>
## How This Skill Works

This skill generates markdown newsletters from events stored in SQLite. The workflow splits responsibility:

1. **CLI tool** handles fragile data operations (paths, types, queries)
2. **Claude** handles creative generation (interpreting preferences, formatting)

### Key Concept: Natural Language Formatting

Users describe how they want newsletters formatted in plain English. You interpret these instructions directly - no templates or structured syntax needed.

Example preference from config:
```yaml
formatting_preferences: |
  Organize by date with each day as a section header.
  Use emojis: 🎵 music, 🎨 art, 🍴 food.
  Format: **Title** @ Venue | Time | Price
```

### Data Source

Events are stored in SQLite at `~/.config/local-media-tools/data/events.db`.
Config is at `~/.config/local-media-tools/sources.yaml`.

### Output

Generated markdown saved to `./newsletter_YYYY-MM-DD.md` in the current working directory.
</essential_principles>

<critical>
## Use CLI for Data Loading - Never Inline Python

**NEVER write inline Python to load events or config.** Use the CLI tool:

```bash
# Get plugin directory first
PLUGIN_DIR=$(cat ~/.claude/plugins/installed_plugins.json | jq -r '.plugins["newsletter-events@local-media-tools"][0].installPath')

# Load events and preferences (default: next 7 days)
cd "$PLUGIN_DIR" && uv run python scripts/cli_newsletter.py load --days 7
```

The CLI tool handles:
- Correct database path resolution
- Proper date type conversions
- Loading formatting preferences from config
- Returning structured JSON

**Do NOT:**
- Write inline Python to query the database
- Hardcode paths to config or database
- Import schema modules directly
</critical>

<workflow>
## Step 0: Get Plugin Directory

```bash
cat ~/.claude/plugins/installed_plugins.json | jq -r '.plugins["newsletter-events@local-media-tools"][0].installPath'
```

Save the output path as `PLUGIN_DIR`.

## Step 1: Load Data with CLI

Run the CLI to get events and formatting preferences:

```bash
cd "$PLUGIN_DIR" && uv run python scripts/cli_newsletter.py load --days 7
```

Or for a specific date range:
```bash
cd "$PLUGIN_DIR" && uv run python scripts/cli_newsletter.py load --from 2025-01-01 --to 2025-01-14
```

**Output:** JSON containing:
- `newsletter_name` - Newsletter title
- `region` - Geographic region
- `formatting_preferences` - User's natural language formatting instructions
- `date_range` - Start and end dates
- `event_count` - Number of events
- `events` - Array of event objects

If no events found, the CLI returns an error with suggestions.

## Step 2: Generate Newsletter (Your Creative Task)

Using the JSON output from Step 1, generate markdown that follows the `formatting_preferences`.

**Your task:** Interpret the natural language preferences and apply them creatively:
- Read the `formatting_preferences` field
- Adapt raw event descriptions to match user's desired style
- Apply emoji rules, formatting patterns, organization
- Generate readable, well-structured markdown

### Available Fields Reference

Each event in the `events` array has:

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Event name | "Jazz Night" |
| `venue` | Venue name | "The Blue Note" |
| `venue_city` | Venue city | "Kingston" |
| `date` | ISO date | "2025-01-20" |
| `day_of_week` | Full day name | "Saturday" |
| `formatted_date` | Human-readable date | "January 20" |
| `time` | Start time | "8:00 PM" or null |
| `description` | Event description | "Live jazz trio..." |
| `category` | Event category | "music", "art", "food_drink" |
| `price` | Price or null | "$15" |
| `is_free` | Boolean | true/false |
| `ticket_url` | Link to buy tickets | URL or null |
| `event_url` | Link to event page | URL or null |
| `source_url` | Where event was found | URL or null |

### Formatting Guidelines

1. **Read preferences carefully** - follow user instructions exactly
2. **Handle nulls gracefully** - skip fields that are null/missing
3. **Sort appropriately** - events come pre-sorted by date then time
4. **Be creative** - adapt descriptions to match user's style

## Step 3: Save Output

Write the generated markdown to the current working directory:

```
./newsletter_YYYY-MM-DD.md
```

Use today's date for the filename.

## Step 4: Display Preview

Show the first ~50 lines of generated markdown so user can review.

Report:
- Output file path
- Number of events included
- Date range covered
</workflow>

<error_handling>
### No Events Found

The CLI will return:
```json
{
  "error": "no_events",
  "message": "No events found from 2025-01-01 to 2025-01-07",
  "suggestion": "Run /newsletter-events:research to scrape new events, or try a wider date range with --days 14"
}
```

Report this to the user with the suggestion.

### No Formatting Preferences

If `formatting_preferences` is null or empty, use sensible defaults:
```
Organize events chronologically by date.
Use section headers for each day (e.g., "## Saturday, January 20").
Include event title, venue, time, and price.
Keep formatting simple and readable.
```

### Database Not Found

The CLI will return:
```json
{
  "error": "database_not_found",
  "message": "Database not found at ~/.config/local-media-tools/data/events.db",
  "suggestion": "Run /newsletter-events:research to scrape events first"
}
```
</error_handling>

<success_criteria>
Newsletter generation is complete when:
- [ ] CLI tool used to load events (not inline Python)
- [ ] Formatting preferences interpreted correctly
- [ ] Markdown generated following user's preferences
- [ ] Output saved to `./newsletter_YYYY-MM-DD.md`
- [ ] Preview displayed to user
</success_criteria>
