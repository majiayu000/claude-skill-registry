---
name: time-helper
description: Get current time, convert timezones, and perform time calculations using native PHP (Windows/Mac/Linux compatible)
version: 1.0.0
author: SubsHero Team
tags: [time, timezone, datetime, utility, cross-platform, token-efficient]
---

# Time & Timezone Helper Skill

Ultra-efficient, cross-platform time operations using native PHP. Replaces timezone MCP servers with 67% token savings.

## Overview

This skill provides timezone and time operations WITHOUT requiring MCP servers, saving 60-75% tokens per query.

**Cross-Platform:** Works on Windows, Mac, and Linux (uses PHP, not bash scripts).

**Token Savings:**
- MCP call: ~400 tokens
- This skill: ~130 tokens
- **Savings: 270 tokens per query (67.5%)**

## 🔧 **BASH COMMAND ATTRIBUTION PATTERN**

**CRITICAL: Before executing EACH php/bash command, MUST output:**
```
🔧 [time-helper] Running: <command>
```

**Examples:**
```
🔧 [time-helper] Running: php -r "echo (new DateTime('now', new DateTimeZone('Asia/Tokyo')))->format('Y-m-d H:i:s T');"
🔧 [time-helper] Running: php -r "date_default_timezone_set('America/New_York'); echo date('Y-m-d H:i:s T');"
🔧 [time-helper] Running: bash .claude/skills/colored-output/color.sh skill-header "time-helper" "Getting time..."
```

**Why:** This pattern helps users identify which skill is executing which command, improving transparency and debugging.

---

## 🎨 **VISUAL OUTPUT FORMATTING**

**CRITICAL: All time-helper output MUST use the colored-output formatter skill!**

### Use Colored-Output Skill

**Instead of writing ANSI codes manually, use the centralized formatter:**

```bash
bash .claude/skills/colored-output/color.sh [type] "time-helper" [message]
```

### Required Output Format

**IMPORTANT: Use MINIMAL colored output (2-3 calls max) to prevent screen flickering!**

**Example formatted output (MINIMAL PATTERN):**
```bash
# START: Header only
bash .claude/skills/colored-output/color.sh skill-header "time-helper" "Getting current time for Tokyo..."

# MIDDLE: Regular text (no colored calls)
Querying timezone database...
Current time: 2025-10-22 14:30:00 JST
UTC offset: +09:00

# END: Result only
bash .claude/skills/colored-output/color.sh success "" "Time retrieved successfully"
```

### When to Use Colored Output

**DO Use:**
- Initial header: `bash .claude/skills/colored-output/color.sh skill-header "time-helper" "Processing..."`
- Final result: `bash .claude/skills/colored-output/color.sh success "" "Complete"`
- Errors only: `bash .claude/skills/colored-output/color.sh error "" "Invalid timezone"`

**DON'T Use:**
- ❌ Progress updates - use regular text
- ❌ Info messages - use regular text
- ❌ Intermediate steps - use regular text

**WHY:** Each bash call creates a task in Claude CLI, causing screen flickering. Keep it minimal!

---

## Usage Examples

### Get Current Time
- `/time-helper "current time"`
- `/time-helper "what time is it in Tokyo"`
- `/time-helper "time in America/New_York"`

### Convert Between Timezones
- `/time-helper "convert 3pm EST to Tokyo"`
- `/time-helper "what's 14:00 UTC in PST"`
- `/time-helper "3:00 PM New York time in London"`

### Time Calculations
- `/time-helper "5 hours from now"`
- `/time-helper "30 days from today"`
- `/time-helper "what date is 2 weeks from now"`

### List Timezones
- `/time-helper "list timezones America"`
- `/time-helper "find timezone for London"`
- `/time-helper "show all Europe timezones"`

### DST Information
- `/time-helper "is EST in daylight saving"`
- `/time-helper "DST status for Europe/Paris"`

---

## How It Works

When user asks about time/timezone:

1. **Determine Command Type**: Analyze user request (current time, conversion, calculation, list, DST)
2. **Extract Parameters**: Timezone names, times, offsets
3. **Execute PHP Script**: Run cross-platform time-helper.php
4. **Return Formatted Output**: Human-readable response

---

## Commands for PHP Script

The skill uses `~/.claude/skills/time-helper/time-helper.php` script:

### Get Current Time
```bash
php ~/.claude/skills/time-helper/time-helper.php now "Asia/Tokyo"
php ~/.claude/skills/time-helper/time-helper.php now "America/New_York"
php ~/.claude/skills/time-helper/time-helper.php now "Europe/London"
```

### Convert Time Between Timezones
```bash
php ~/.claude/skills/time-helper/time-helper.php convert "15:00" "America/New_York" "Asia/Tokyo"
php ~/.claude/skills/time-helper/time-helper.php convert "2025-10-20 14:00" "UTC" "America/Los_Angeles"
```

### Add Time Offset
```bash
php ~/.claude/skills/time-helper/time-helper.php add "5 hours"
php ~/.claude/skills/time-helper/time-helper.php add "30 days"
php ~/.claude/skills/time-helper/time-helper.php add "2 weeks" "2025-10-20"
```

### Subtract Time Offset
```bash
php ~/.claude/skills/time-helper/time-helper.php subtract "3 hours"
php ~/.claude/skills/time-helper/time-helper.php subtract "7 days"
```

### List Available Timezones
```bash
php ~/.claude/skills/time-helper/time-helper.php list
php ~/.claude/skills/time-helper/time-helper.php list "America"
php ~/.claude/skills/time-helper/time-helper.php list "Europe"
php ~/.claude/skills/time-helper/time-helper.php list "Asia"
```

### Check DST Status
```bash
php ~/.claude/skills/time-helper/time-helper.php dst "America/New_York"
php ~/.claude/skills/time-helper/time-helper.php dst "Europe/Paris"
```

---

## Example Interactions

### Example 1: Current Time Query
**User:** "What time is it in Tokyo?"

**Execute:**
```bash
php ~/.claude/skills/time-helper/time-helper.php now "Asia/Tokyo"
```

**Output:**
```
🕐 Sunday, October 20, 2025 - 8:03:51 PM JST
   Timezone: Asia/Tokyo
   UTC Offset: +09:00
```

### Example 2: Timezone Conversion
**User:** "Convert 3pm EST to Tokyo time"

**Execute:**
```bash
php ~/.claude/skills/time-helper/time-helper.php convert "15:00" "America/New_York" "Asia/Tokyo"
```

**Output:**
```
📍 Original:  3:00 PM EST (Sunday, Oct 20, 2025)
📍 Converted: 4:00 AM JST (Monday, Oct 21, 2025)

From: America/New_York
To:   Asia/Tokyo
```

### Example 3: Time Calculation
**User:** "What's the date 30 days from now?"

**Execute:**
```bash
php ~/.claude/skills/time-helper/time-helper.php add "30 days"
```

**Output:**
```
📅 Base time:   2025-10-20 11:03:51 UTC
➕ Adding:      30 days
📅 Result:      2025-11-19 11:03:51 UTC

   (Tuesday, November 19, 2025 at 11:03 AM)
```

### Example 4: List Timezones
**User:** "Show me all America timezones"

**Execute:**
```bash
php ~/.claude/skills/time-helper/time-helper.php list "America"
```

**Output:**
```
🌍 Available Timezones (filtered by 'America'):
═══════════════════════════════════════
   • America/New_York
   • America/Los_Angeles
   • America/Chicago
   • America/Denver
   ... (142 more)

Total: 146 timezone(s)
```

### Example 5: DST Check
**User:** "Is New York in daylight saving time?"

**Execute:**
```bash
php ~/.claude/skills/time-helper/time-helper.php dst "America/New_York"
```

**Output:**
```
🌞 Timezone: America/New_York
   Current time: 2025-10-20 07:03:51 EDT
   DST Active: ✅ Yes
   UTC Offset: -04:00
   Abbreviation: EDT
```

---

## Common Timezone Names

### United States
- `America/New_York` - Eastern Time (ET)
- `America/Chicago` - Central Time (CT)
- `America/Denver` - Mountain Time (MT)
- `America/Los_Angeles` - Pacific Time (PT)
- `America/Anchorage` - Alaska Time (AKT)
- `Pacific/Honolulu` - Hawaii Time (HST)

### Europe
- `Europe/London` - UK (GMT/BST)
- `Europe/Paris` - France (CET/CEST)
- `Europe/Berlin` - Germany (CET/CEST)
- `Europe/Rome` - Italy (CET/CEST)
- `Europe/Madrid` - Spain (CET/CEST)
- `Europe/Moscow` - Russia (MSK)

### Asia
- `Asia/Tokyo` - Japan (JST)
- `Asia/Shanghai` - China (CST)
- `Asia/Hong_Kong` - Hong Kong (HKT)
- `Asia/Singapore` - Singapore (SGT)
- `Asia/Dubai` - UAE (GST)
- `Asia/Kolkata` - India (IST)

### Others
- `UTC` - Coordinated Universal Time
- `Australia/Sydney` - Australia East (AEST/AEDT)
- `Pacific/Auckland` - New Zealand (NZST/NZDT)

---

## Natural Language Processing

### When User Says... Execute This:

| User Request | Command |
|--------------|---------|
| "What time is it in [city/timezone]?" | `php ... now "[timezone]"` |
| "Current time [timezone]" | `php ... now "[timezone]"` |
| "Convert [time] [from] to [to]" | `php ... convert "[time]" "[from_tz]" "[to_tz]"` |
| "[time] [from_tz] in [to_tz]" | `php ... convert "[time]" "[from_tz]" "[to_tz]"` |
| "[X] hours/days from now" | `php ... add "[X] hours/days"` |
| "[X] hours/days ago" | `php ... subtract "[X] hours/days"` |
| "List timezones [filter]" | `php ... list "[filter]"` |
| "Is [tz] in daylight saving?" | `php ... dst "[timezone]"` |

### Timezone Abbreviation Mapping

Map common abbreviations to full timezone identifiers:

| Abbrev | Full Timezone |
|--------|---------------|
| EST/EDT | America/New_York |
| CST/CDT | America/Chicago |
| MST/MDT | America/Denver |
| PST/PDT | America/Los_Angeles |
| GMT/BST | Europe/London |
| CET/CEST | Europe/Paris |
| JST | Asia/Tokyo |
| CST (China) | Asia/Shanghai |
| IST | Asia/Kolkata |
| AEST/AEDT | Australia/Sydney |

---

## Technical Details

### Features
- ✅ 594+ timezone identifiers supported
- ✅ Automatic DST handling
- ✅ Cross-platform (Windows/Mac/Linux)
- ✅ No external dependencies (native PHP)
- ✅ DateTimeImmutable for thread safety
- ✅ Error handling with helpful messages

### Requirements
- PHP 7.4+ (SubsHero uses PHP 8.3+)
- DateTimeZone class (included in PHP core)

### Token Efficiency
- **Without this skill**: Use MCP (~400 tokens/query)
- **With this skill**: Direct PHP execution (~130 tokens/query)
- **10 time queries**: Save 2,700 tokens per session!

---

## Error Handling

### Invalid Timezone
**Input:** `php ... now "Invalid/Timezone"`

**Output:**
```
❌ Error: Invalid timezone 'Invalid/Timezone'
   Use 'list' command to see available timezones
```

### Invalid Time Format
**Input:** `php ... convert "invalid" "UTC" "EST"`

**Output:**
```
❌ Error: Failed to parse time string 'invalid'
```

### Missing Arguments
**Input:** `php ... now`

**Output:**
```
❌ Error: Missing timezone argument
Usage: php time-helper.php now <timezone>
```

---

## Maintenance

### Adding New Features

To add new commands, edit `time-helper.php`:

1. Add new function (e.g., `function getBusinessHours()`)
2. Add case to switch statement
3. Update skill.md with usage examples

### Testing

Test all commands directly:
```bash
cd ~/.claude/skills/time-helper
php time-helper.php now "UTC"
php time-helper.php convert "12:00" "UTC" "America/New_York"
php time-helper.php add "5 hours"
php time-helper.php list "America"
php time-helper.php dst "Europe/London"
```

---

## Migration from Timezone MCP

If you previously used a timezone MCP server:

1. ✅ **Install this skill** (2 files created)
2. 🧪 **Test all use cases** (verify same functionality)
3. 🗑️ **Remove Timezone MCP** from `.mcp.json`
4. 💾 **Enjoy 67% token savings** on all time queries!

---

## Support

**File Location:** `~/.claude/skills/time-helper/`

**Files:**
- `skill.md` - This documentation
- `time-helper.php` - Cross-platform PHP script

**Timezone List:** Use `php time-helper.php list` to see all 594 timezones

**Common Issues:**
- If PHP not found: Ensure PHP is in PATH
- If timezone invalid: Use `list` command to find correct name
- If DST info unavailable: Some timezones don't observe DST

---

## Version History

### v1.0.0 (2025-10-20)
- Initial release
- Get current time in any timezone
- Convert between timezones
- Time calculations (add/subtract)
- List available timezones with filtering
- DST detection and status
- Cross-platform PHP script (Windows/Mac/Linux)
- 67% token savings vs. MCP servers
