---
name: get-calendar
description: Fetch calendar events from macOS Calendar using ekctl for a specified timeframe. Returns structured event data for planning rituals.
disable-model-invocation: true
allowed-tools: Read, Bash(*)
argument-hint: "[scope: today|tomorrow|week|month] [--format json|markdown]"
---

# Get Calendar Sub-Skill

Fetches calendar events from macOS Calendar using the `ekctl` CLI tool. Returns structured data suitable for consumption by planning rituals.

## Prerequisites

This sub-skill requires:
1. **ekctl** installed (typically at `/opt/homebrew/bin/ekctl`)
2. Calendar access granted to Terminal/Claude
3. Aliases configured for calendars to fetch (see Setup in CLAUDE.md)

## Arguments

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| scope | `today`, `tomorrow`, `week`, `month`, `monday`-`sunday`, `YYYY-MM-DD` | `today` | Time range to fetch |
| format | `json`, `markdown` | `json` | Output format |

Parse arguments from `$ARGUMENTS` if provided.

**Scope Resolution:**
- `today`, `tomorrow`, `week`, `month` - Relative to current date
- `monday`, `tuesday`, etc. - Next occurrence of that weekday (including today if it matches)
- `YYYY-MM-DD` - Specific date (e.g., `2026-02-14`)

## Execution Steps

### 1. Read Configuration

Read the skill's configuration file:

```bash
cat .claude/skills/_sub/fetch/get-calendar/calendars.json
```

Extract:
- `calendars`: Array of ekctl alias names to fetch from
- `settings.work_hours`: For focus time calculation
- `settings.one_on_one_patterns`: Patterns to identify 1:1s

If the config file doesn't exist or has no calendars configured, return an error with setup instructions.

### 2. Calculate Date Range

Based on the scope argument (default: `today`), calculate ISO8601 date range using macOS `date` command:

**For `today`:**
```bash
FROM=$(date -v0H -v0M -v0S +"%Y-%m-%dT%H:%M:%S%z")
TO=$(date -v23H -v59M -v59S +"%Y-%m-%dT%H:%M:%S%z")
```

**For `tomorrow`:**
```bash
FROM=$(date -v+1d -v0H -v0M -v0S +"%Y-%m-%dT%H:%M:%S%z")
TO=$(date -v+1d -v23H -v59M -v59S +"%Y-%m-%dT%H:%M:%S%z")
```

**For `week`:**
```bash
FROM=$(date -v0H -v0M -v0S +"%Y-%m-%dT%H:%M:%S%z")
TO=$(date -v+7d -v23H -v59M -v59S +"%Y-%m-%dT%H:%M:%S%z")
```

**For `month`:**
```bash
FROM=$(date -v1d -v0H -v0M -v0S +"%Y-%m-%dT%H:%M:%S%z")
TO=$(date -v1d -v+1m -v-1d -v23H -v59M -v59S +"%Y-%m-%dT%H:%M:%S%z")
```

**For weekday (`monday`, `tuesday`, etc.):**

Calculate the next occurrence of that weekday (including today if it matches). Use the weekday name to determine the target date, then calculate FROM/TO for that single day:
```bash
# Example for "monday" - find next Monday's date, then use single-day range
FROM=$(date -v+Xd -v0H -v0M -v0S +"%Y-%m-%dT%H:%M:%S%z")  # where X = days until target weekday
TO=$(date -v+Xd -v23H -v59M -v59S +"%Y-%m-%dT%H:%M:%S%z")
```

**For specific date (`YYYY-MM-DD`):**

Parse the provided date and calculate the range for that single day:
```bash
# Example for "2026-02-14"
FROM=$(date -j -f "%Y-%m-%d" "2026-02-14" +"%Y-%m-%dT00:00:00%z")
TO=$(date -j -f "%Y-%m-%d" "2026-02-14" +"%Y-%m-%dT23:59:59%z")
```

### 3. Fetch Events from Each Calendar

For each calendar alias in the config, run:

```bash
ekctl list events --calendar "$ALIAS" --from "$FROM" --to "$TO"
```

Example:
```bash
ekctl list events --calendar "work" --from "2026-02-08T00:00:00+0100" --to "2026-02-08T23:59:59+0100"
```

Collect the JSON responses from each calendar.

### 4. Process and Transform

1. **Merge all events** from different calendars into a single array
2. **Sort by start time** (earliest first)
3. **Tag each event** with its source calendar alias
4. **Identify 1:1 meetings** by checking:
   - Title contains patterns from `one_on_one_patterns` (e.g., "1:1", "1-1")
   - Single external attendee
5. **Calculate focus blocks** (gaps between meetings of 30+ minutes within work hours)
6. **Generate summary** with counts and focus time

### 5. Return Output

**JSON format** (default):

```json
{
  "scope": "today",
  "date_range": {
    "from": "2026-02-08T00:00:00+0100",
    "to": "2026-02-08T23:59:59+0100"
  },
  "events": [
    {
      "calendar": "work",
      "title": "Engineering Roadmap Review",
      "start": "2026-02-08T10:00:00+0100",
      "end": "2026-02-08T11:00:00+0100",
      "location": "Conference Room A",
      "is_all_day": false,
      "is_one_on_one": false
    },
    {
      "calendar": "work",
      "title": "1:1: Sarah",
      "start": "2026-02-08T14:00:00+0100",
      "end": "2026-02-08T14:30:00+0100",
      "location": null,
      "is_all_day": false,
      "is_one_on_one": true
    }
  ],
  "summary": {
    "total_events": 2,
    "meetings": 2,
    "one_on_ones": 1,
    "all_day_events": 0,
    "focus_hours": 5.5
  }
}
```

**Markdown format** (when `--format markdown` or `format: markdown`):

```markdown
## Calendar: 2026-02-08 (Saturday)

### Meetings (2)
- **10:00-11:00** Engineering Roadmap Review (Conference Room A)
- **14:00-14:30** 1:1: Sarah *(1:1)*

### All-Day Events
(none)

### Focus Time Available
- 09:00-10:00 (1h)
- 11:00-14:00 (3h)
- 14:30-18:00 (3.5h)

**Summary:** 2 meetings, 1 one-on-one, 0 all-day events, 7.5h focus time
```

## Error Handling

| Error | Response |
|-------|----------|
| ekctl not installed | Return error with: "ekctl not found. Install with: brew install ekctl" |
| Calendar alias not found | Skip calendar, include warning in output |
| No calendars configured | Return error with setup instructions pointing to CLAUDE.md |
| Calendar access denied | Return error with: "Calendar access denied. Grant permission in System Settings > Privacy & Security > Calendars" |
| No events in range | Return empty events array with summary showing 0 counts |

## Usage by Other Skills

Other skills (e.g., daily-planning) reference this sub-skill like:

```markdown
**Use sub-skill: `_sub/fetch/get-calendar`**
- Scope: today
- Format: json

Use the calendar events to:
1. Pre-populate the Meetings section with scheduled meetings
2. Identify 1:1s and use the 1:1 template format from today.md
3. Calculate focus blocks for deep work planning
4. Set the `meetings` count in frontmatter
```
