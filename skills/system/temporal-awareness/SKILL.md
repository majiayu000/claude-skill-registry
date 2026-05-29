---
name: temporal-awareness
description: Ensures temporal accuracy by using Unix date commands. Use this skill whenever Claude needs to know today's date, the current day of the week, what day a future/past date falls on, or perform any date/time calculations. Triggers on questions like "what day is it", "what's today's date", "what day of the week is [date]", scheduling tasks, deadline calculations, or any temporal reasoning.
license: MIT
allowed-tools: Bash(date:*)
metadata:
  author: Matt Hodges
  version: "0.0.1"
---

# Temporal Awareness

Claude's system prompt date may be stale or unavailable. Always verify temporal information using Unix commands before responding to date-sensitive queries.

## Example Commands

GNU date (Linux) and BSD date (macOS, FreeBSD) have different syntax. You can check which is installed:

```bash
if date --version >/dev/null 2>&1 ; then
    echo GNU date
else
    echo BSD date
fi

```

### Get current date/time
```bash
# Works on both GNU date and BSD date
date                          # Full date and time
date +%Y-%m-%d                # ISO format: 2025-01-15
date +%A                      # Day of week: Wednesday
date "+%B %d, %Y"             # January 15, 2025
```

### Find day of week for any date
```bash
# GNU date
date -d "2025-03-15" +%A              # From ISO date: Saturday
date -d "March 15, 2025" +%A          # From natural language: Saturday
date -d "next Friday" +%A             # Relative: Friday
date -d "last Monday" +%A             # Relative: Monday

# BSD date
date -j -f "%Y-%m-%d" "2025-03-15" +%A       # From ISO date: Saturday
date -j -f "%B %d, %Y" "March 15, 2025" +%A  # From natural language: Saturday
date -v +fri +%A                             # Next Friday: Friday
date -v -mon +%A                             # Last Monday: Monday
```

### Date arithmetic
```bash
# GNU date
date -d "+7 days" +%Y-%m-%d           # 7 days from now
date -d "-2 weeks" +%A                # Day of week 2 weeks ago
date -d "2025-06-01 +30 days" +%Y-%m-%d   # 30 days after June 1

# BSD date
date -v +7d +%Y-%m-%d                 # 7 days from now (-v: adjust)
date -v -2w +%A                       # Day of week 2 weeks ago
date -j -f "%Y-%m-%d" -v +30d "2025-06-01" +%Y-%m-%d   # 30 days after June 1
```

### Days between dates
```bash
# GNU date
echo $(( ($(date -d "2025-12-31" +%s) - $(date -d "2025-01-01" +%s)) / 86400 ))   # 364

# BSD date
echo $(( ($(date -j -f "%Y-%m-%d" "2025-12-31" +%s) - $(date -j -f "%Y-%m-%d" "2025-01-01" +%s)) / 86400 ))   # 364
```

## When to Use

Run `date` **first** before answering the user or writing date-aware outputs:
- User asks what today's date or day is
- Use asks what day of the week a date falls on
- User needs to calculate deadlines or durations
- User asks about time until/since an event
- Output works with schedules, meetings, deadlines, or events
- Output needs any temporal context for the task

## Example

User: "What day of the week is July 4th, 2026?"

```bash
#GNU Date
date -d "July 4, 2026" +%A

# BSD Date
date -j -f "%B %d, %Y" "July 4, 2026" +%A

# Output: Saturday
```

Then respond: "July 4th, 2026 falls on a Saturday."
