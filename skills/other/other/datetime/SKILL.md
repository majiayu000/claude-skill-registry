---
name: datetime
description: Get current date and time in various formats. Use whenever you need the current date, time, timestamps, or formatted datetime values for any purpose (logging, file naming, scheduling, comparisons, etc.)
---

# datetime - Current Date & Time

Get the current date and time in various formats.

## Quick Reference

```bash
# Date only
date +%Y-%m-%d                    # 2025-01-15
date +%Y/%m/%d                    # 2025/01/15
date +%d-%m-%Y                    # 15-01-2025

# Date with time
date +"%Y-%m-%d %H:%M:%S"         # 2025-01-15 14:30:45
date +"%Y-%m-%dT%H:%M:%S"         # 2025-01-15T14:30:45 (ISO 8601)
date -u +"%Y-%m-%dT%H:%M:%SZ"     # 2025-01-15T14:30:45Z (UTC ISO 8601)

# Time only
date +%H:%M:%S                    # 14:30:45
date +%H:%M                       # 14:30
date +%I:%M%p                     # 02:30PM (12-hour)

# Timestamps
date +%s                          # 1705329045 (Unix epoch)
date +%s%3N                       # 1705329045123 (milliseconds)

# Human readable
date "+%B %d, %Y"                 # January 15, 2025
date "+%A, %B %d, %Y"             # Wednesday, January 15, 2025
date "+%b %d %Y"                  # Jan 15 2025

# File-safe formats (no colons/spaces)
date +%Y%m%d                      # 20250115
date +%Y%m%d_%H%M%S               # 20250115_143045
date +%Y%m%d-%H%M%S               # 20250115-143045
```

## When to Use

Use this skill whenever you need:
- Current date for logging or timestamps
- Date strings for file naming
- ISO 8601 formatted dates for APIs
- Unix timestamps for calculations
- Human-readable date displays
- UTC time for cross-timezone consistency

## Format Codes

| Code | Output | Example |
|------|--------|---------|
| `%Y` | Year (4-digit) | 2025 |
| `%m` | Month (01-12) | 01 |
| `%d` | Day (01-31) | 15 |
| `%H` | Hour 24h (00-23) | 14 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%I` | Hour 12h (01-12) | 02 |
| `%p` | AM/PM | PM |
| `%s` | Unix timestamp | 1705329045 |
| `%A` | Weekday name | Wednesday |
| `%B` | Month name | January |
| `%b` | Month abbrev | Jan |
| `%Z` | Timezone | PST |

## Common Patterns

**Log timestamp:**
```bash
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Event occurred"
```

**Backup file naming:**
```bash
cp file.txt "file_$(date +%Y%m%d_%H%M%S).txt"
```

**API timestamp (UTC):**
```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```
