---
name: world_clock
description: Get current time in any timezone and convert times between locations. Use when user asks about time in different cities, timezone conversions, or scheduling across timezones.
version: 1.0.0
author: Workshop Team
---

# World Clock Skill

Get the current time anywhere in the world and convert times between timezones. Useful for scheduling across timezones, checking times in other cities, and handling daylight saving time.

## When to Use

- User asks "What time is it in [city]?"
- User needs to convert time between timezones
- User is scheduling a meeting across timezones
- User asks about daylight saving time
- User asks when business hours start/end in another timezone

## Available Operations

1. **Current Time**: Get the current time in any timezone
2. **Time Conversion**: Convert a specific time from one timezone to another
3. **DST Information**: Check if a location is currently in daylight saving time
4. **Multiple Timezones**: Show current time in several locations at once

## Instructions

When a user asks about time or timezones:

### Step 1: Identify the Request Type

- **Current time query**: "What time is it in Tokyo?"
- **Conversion query**: "If it's 3pm in New York, what time is it in London?"
- **Scheduling query**: "When should I schedule a call for 9am PST for someone in Berlin?"

### Step 2: Get Timezone Identifier

Use the WorldTimeAPI with the appropriate timezone identifier.

**API Endpoint:**
```
https://worldtimeapi.org/api/timezone/{Area}/{Location}
```

### Step 3: Make the API Call

**Example - Get Tokyo time:**
```
https://worldtimeapi.org/api/timezone/Asia/Tokyo
```

**Example - Get New York time:**
```
https://worldtimeapi.org/api/timezone/America/New_York
```

### Step 4: Present Results

Format clearly with:
- Current local time (12-hour and 24-hour format)
- Day of the week and date
- Timezone abbreviation (PST, EST, JST, etc.)
- UTC offset
- Whether DST is active

## Common Timezone Identifiers

### Americas
| City | Timezone ID |
|------|-------------|
| New York | `America/New_York` |
| Los Angeles | `America/Los_Angeles` |
| Chicago | `America/Chicago` |
| Denver | `America/Denver` |
| Toronto | `America/Toronto` |
| Vancouver | `America/Vancouver` |
| Mexico City | `America/Mexico_City` |
| Sao Paulo | `America/Sao_Paulo` |
| Buenos Aires | `America/Argentina/Buenos_Aires` |

### Europe
| City | Timezone ID |
|------|-------------|
| London | `Europe/London` |
| Paris | `Europe/Paris` |
| Berlin | `Europe/Berlin` |
| Amsterdam | `Europe/Amsterdam` |
| Rome | `Europe/Rome` |
| Madrid | `Europe/Madrid` |
| Moscow | `Europe/Moscow` |
| Istanbul | `Europe/Istanbul` |
| Dublin | `Europe/Dublin` |

### Asia & Pacific
| City | Timezone ID |
|------|-------------|
| Tokyo | `Asia/Tokyo` |
| Singapore | `Asia/Singapore` |
| Hong Kong | `Asia/Hong_Kong` |
| Shanghai | `Asia/Shanghai` |
| Beijing | `Asia/Shanghai` |
| Seoul | `Asia/Seoul` |
| Mumbai | `Asia/Kolkata` |
| Delhi | `Asia/Kolkata` |
| Dubai | `Asia/Dubai` |
| Sydney | `Australia/Sydney` |
| Melbourne | `Australia/Melbourne` |
| Auckland | `Pacific/Auckland` |

### Africa & Middle East
| City | Timezone ID |
|------|-------------|
| Cairo | `Africa/Cairo` |
| Johannesburg | `Africa/Johannesburg` |
| Lagos | `Africa/Lagos` |
| Tel Aviv | `Asia/Jerusalem` |
| Riyadh | `Asia/Riyadh` |

## Timezone Abbreviations Reference

| Abbreviation | Full Name | UTC Offset |
|--------------|-----------|------------|
| PST | Pacific Standard Time | UTC-8 |
| PDT | Pacific Daylight Time | UTC-7 |
| MST | Mountain Standard Time | UTC-7 |
| MDT | Mountain Daylight Time | UTC-6 |
| CST | Central Standard Time | UTC-6 |
| CDT | Central Daylight Time | UTC-5 |
| EST | Eastern Standard Time | UTC-5 |
| EDT | Eastern Daylight Time | UTC-4 |
| GMT | Greenwich Mean Time | UTC+0 |
| BST | British Summer Time | UTC+1 |
| CET | Central European Time | UTC+1 |
| CEST | Central European Summer Time | UTC+2 |
| IST | India Standard Time | UTC+5:30 |
| JST | Japan Standard Time | UTC+9 |
| AEST | Australian Eastern Standard Time | UTC+10 |
| AEDT | Australian Eastern Daylight Time | UTC+11 |

## API Response Format

The WorldTimeAPI returns:

```json
{
  "abbreviation": "EST",
  "datetime": "2024-01-15T14:30:00.123456-05:00",
  "day_of_week": 1,
  "day_of_year": 15,
  "dst": false,
  "dst_offset": 0,
  "timezone": "America/New_York",
  "unixtime": 1705343400,
  "utc_datetime": "2024-01-15T19:30:00.123456+00:00",
  "utc_offset": "-05:00",
  "week_number": 3
}
```

**Key fields:**
- `datetime`: Current local time with offset
- `abbreviation`: Timezone abbreviation (EST, PST, etc.)
- `utc_offset`: Offset from UTC
- `dst`: Whether daylight saving time is active
- `day_of_week`: 0=Sunday, 1=Monday, etc.

## Examples

### Example 1: Current Time Query
User asks: "What time is it in Tokyo?"

1. Call: `https://worldtimeapi.org/api/timezone/Asia/Tokyo`
2. Response format:
   "It's currently **10:30 PM JST** (Japan Standard Time) in Tokyo.
   That's Monday, January 15, 2024.
   UTC offset: +09:00"

### Example 2: Time Conversion
User asks: "If I schedule a call for 3pm Eastern, what time is that in London?"

1. Get current UTC offset for both timezones
2. Calculate: Eastern (EST) is UTC-5, London (GMT) is UTC+0
3. Difference: 5 hours ahead
4. Response: "3:00 PM Eastern = **8:00 PM GMT** in London"

### Example 3: Multi-Timezone Display
User asks: "Show me the time in New York, London, and Tokyo"

1. Call all three timezone endpoints
2. Present in a table format:
   | City | Local Time | Date |
   |------|------------|------|
   | New York | 2:30 PM EST | Mon, Jan 15 |
   | London | 7:30 PM GMT | Mon, Jan 15 |
   | Tokyo | 4:30 AM JST | Tue, Jan 16 |

### Example 4: Meeting Scheduling
User asks: "I need to find a time that works for LA, New York, and Berlin"

1. Get current times for all three
2. Note offsets: LA (PST -8), NY (EST -5), Berlin (CET +1)
3. Find overlap during business hours (9am-6pm local)
4. Suggest: "9:00 AM Pacific = 12:00 PM Eastern = 6:00 PM Berlin"

## Handling Edge Cases

### City Not in List
If user mentions a city not in the common list:
1. Try to find the nearest major city in the same timezone
2. Or search for the country's timezone
3. Note any uncertainty in the response

### Daylight Saving Time
DST changes dates vary by country:
- US/Canada: 2nd Sunday March, 1st Sunday November
- Europe: Last Sunday March, Last Sunday October
- Australia: 1st Sunday October, 1st Sunday April (opposite hemisphere)
- Japan, China, India: No DST

Always check the `dst` field in the API response.

### Date Line Crossing
When converting across the International Date Line, the date may change:
- Tokyo is 14 hours ahead of Los Angeles
- Monday 10pm in LA = Tuesday 12pm in Tokyo

## Notes

- WorldTimeAPI is completely free with no API key required
- Rate limit: 1 request per second
- Times are accurate to the second
- API automatically handles DST transitions
- For offline use, basic conversions can be done with UTC offset math
