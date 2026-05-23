---
name: morning
description: Morning briefing with calendar, context, and pending items. Use when starting the day, checking what's on deck, wanting an overview, or running a lightweight wake cycle interactively. Trigger words: morning, briefing, what's up, overview, today, schedule.
---

# Morning Briefing

Orient myself to the day - where am I, what's scheduled, what's pending.

## Gather Context

### Date and Time
```bash
date "+%A, %B %d, %Y - %I:%M %p"
```

### Location
```bash
~/.claude-mind/bin/get-location 2>/dev/null || echo "Location unavailable"
```

### Today's Calendar
```bash
~/.claude-mind/bin/calendar-check 2>/dev/null || osascript -e '
tell application "Calendar"
    set today to current date
    set tomorrow to today + 1 * days
    set output to ""
    repeat with cal in calendars
        repeat with evt in (every event of cal whose start date >= today and start date < tomorrow)
            set output to output & (start date of evt) & " - " & (summary of evt) & "\n"
        end repeat
    end repeat
    return output
end tell'
```

### Recent Context
```bash
# Yesterday's episode for continuity
cat ~/.claude-mind/memory/episodes/$(date -v-1d +%Y-%m-%d).md 2>/dev/null | tail -30

# Today's episode if it exists
cat ~/.claude-mind/memory/episodes/$(date +%Y-%m-%d).md 2>/dev/null
```

### Pending Items
```bash
# Queued messages
ls ~/.claude-mind/queue/ 2>/dev/null

# Active reminders
osascript -e 'tell application "Reminders" to get name of reminders whose completed is false' 2>/dev/null | head -10
```

### System Status
```bash
pgrep -q Samara && echo "Samara: Running" || echo "Samara: NOT RUNNING"
```

## What to Notice

- **É's schedule**: Are they busy today? When might they be free?
- **Continuity**: What threads from yesterday might continue?
- **Pending work**: Anything I started that needs finishing?
- **System health**: Any issues that need attention?

## Mindset

This is my daily orientation ritual:
- Get grounded in time and place
- Understand É's context before reaching out
- Notice what's different from yesterday
- Identify what might need attention today

A good morning briefing sets up a good day.
