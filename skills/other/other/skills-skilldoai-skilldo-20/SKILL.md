---
name: arrow
description: Date, time, and timezone handling with an Arrow datetime type plus parsing/formatting helpers.
version: 1.4.0
ecosystem: python
license: MIT
generated_with: gpt-5.2
---

## Imports

```python
import arrow
from arrow import Arrow, ArrowFactory, get, now, utcnow
from arrow.formatter import FORMAT_RFC3339, FORMAT_RFC3339_STRICT, FORMAT_RFC2822
from arrow.parser import DateTimeParser, ParserError, ParserMatchError
```

## Core Patterns

### Create Arrow instances (now/utcnow/get) ✅ Current
```python
import arrow

# Current time in UTC (timezone-aware)
a_utc = arrow.utcnow()

# Current time in a specific timezone (IANA tz name or "local"/"utc")
a_local = arrow.now("local")
a_pacific = arrow.now("US/Pacific")

# Parse ISO-8601-like strings (Arrow will infer many common formats)
a_iso = arrow.get("2024-01-15T10:30:00+02:00")

# Avoid asserting exact offsets for zones with DST; instead, assert tzinfo exists.
# Also avoid relying on tzinfo.key being present across tzinfo implementations.
assert a_utc.tzinfo is not None
assert a_pacific.tzinfo is not None

print(a_utc)
print(a_local)
print(a_pacific)
print(a_iso)
```
* Prefer `arrow.utcnow()` / `arrow.now()` / `arrow.get(...)` as the primary constructors.

### Parse non-ISO strings with Arrow tokens ✅ Current
```python
import arrow

# Arrow tokens (NOT datetime.strptime tokens)
a = arrow.get("2013-05-05 12:30:45", "YYYY-MM-DD HH:mm:ss")

# Formatting with Arrow tokens
s1 = a.format("YYYY-MM-DD")
s2 = a.format("YYYY-MM-DD HH:mm:ss")

print(s1)
print(s2)
```
* When parsing/formatting custom strings, use Arrow token strings (e.g., `YYYY-MM-DD`), not `%Y-%m-%d`.

### Parse with multiple format fallbacks ✅ Current
```python
import arrow

# Try multiple formats until one succeeds
date_str = "15/01/19"
a = arrow.get(date_str, ["DD/MM/YY", "DD/MM/YYYY"])

print(a)
```
* Pass a list of format strings to try parsing with multiple formats in order.

### Shift/replace/to for time arithmetic and timezone handling ✅ Current
```python
import arrow

a = arrow.get("2024-02-01T12:00:00Z")

# Relative offsets (returns a new Arrow)
b = a.shift(days=+7, hours=-3)

# Set specific components (returns a new Arrow)
c = a.replace(hour=9, minute=15, second=0, microsecond=0)

# Convert the same instant to another timezone
d = a.to("Europe/Paris")

print("a:", a)
print("b:", b)
print("c:", c)
print("d:", d)
```
* Use `.shift(...)` for relative offsets and `.replace(...)` for setting components.
* Use `.to("Zone/Name")` to convert the same instant into another timezone.

### Humanize with a stable reference time (especially in tests) ✅ Current
```python
import arrow

present = arrow.utcnow()
past = present.shift(hours=-1, minutes=-5)

# Stable output: compare against an explicit reference time
print(past.humanize(present))
print(past.humanize(present, only_distance=True))
```
* Pass a reference time to `humanize(...)` to avoid time-sensitive test failures.
* `only_distance=True` omits "ago"/"in".

### Use ArrowFactory for Arrow subclasses ✅ Current
```python
from __future__ import annotations

import arrow
from arrow import Arrow

class CustomArrow(Arrow):
    """Arrow subclass for project-specific helpers."""
    def iso_date(self) -> str:
        return self.format("YYYY-MM-DD")

custom = arrow.ArrowFactory(CustomArrow)

a = custom.utcnow()
print(type(a).__name__)
print(a.iso_date())
```
* For custom behavior, subclass `arrow.Arrow` and build a `arrow.ArrowFactory(CustomArrow)`.

### Parse timestamps with Arrow tokens ✅ Current
```python
import arrow

# Parse Unix timestamp (seconds since epoch)
a = arrow.get("1569982581", "X")
print(a)

# Parse expanded timestamp (milliseconds since epoch)
b = arrow.get("1569982581413", "x")
print(b)
```
* Use `"X"` token for Unix timestamps (seconds).
* Use `"x"` token for expanded timestamps (milliseconds/microseconds).

### Parse month and day names ✅ Current
```python
import arrow

# Full month names
a = arrow.get("January 1, 2012", "MMMM D, YYYY")
print(a)

# Short month names
b = arrow.get("Jan 1, 2012", "MMM D, YYYY")
print(b)

# Day of week (validated if date also specified)
c = arrow.get("Tue 2019-10-17", "ddd YYYY-MM-DD")
print(c)
```
* Use `MMMM` for full month names, `MMM` for short month names.
* Use `dddd` for full day names, `ddd` for short day names.

### Parse 12-hour format with AM/PM ✅ Current
```python
import arrow

# Lowercase am/pm
a = arrow.get("1 pm", "h a")
print(a)

# Uppercase AM/PM
b = arrow.get("1 PM", "h A")
print(b)
```
* Use `"a"` for lowercase am/pm, `"A"` for uppercase AM/PM.
* Use with `"h"` (12-hour) or `"hh"` (zero-padded 12-hour) tokens.

### Parse with timezone information ✅ Current
```python
import arrow

# Timezone offset (±HH:MM)
a = arrow.get("2013-01-01 -07:00", "YYYY-MM-DD ZZ")
print(a)

# Timezone name (IANA)
b = arrow.get("2013-01-01 America/New_York", "YYYY-MM-DD ZZZ")
print(b)
```
* Use `ZZ` for timezone offset like `+05:30` or `-07:00`.
* Use `ZZZ` for IANA timezone names like `America/New_York`.

### Parse subseconds with precision control ✅ Current
```python
import arrow

# Parse microseconds (up to 6 digits)
a = arrow.get("2013-01-01 12:30:45.987654", "YYYY-MM-DD HH:mm:ss.SSSSSS")
print(a)

# Automatic rounding for longer subsecond values
b = arrow.get("2013-01-01 12:30:45.9876539", "YYYY-MM-DD HH:mm:ss.S")
print(b)  # Rounds to microseconds
```
* Use 1-6 `S` tokens for subseconds.
* Values beyond 6 digits are automatically rounded to microseconds.

### Parse ordinal day of year ✅ Current
```python
import arrow

# Day 136 of 1998 (May 16)
a = arrow.get("1998-136", "YYYY-DDDD")
print(a)
```
* Use `DDD` or `DDDD` for ordinal day of year (001-366).

### Parse ISO week dates ✅ Current
```python
import arrow

# ISO week date: Year-Week-Day
a = arrow.get("2011-W05-4", "W")
print(a)
```
* Use `"W"` token for ISO week date format (`YYYY-Www-D` or `YYYYWwwD`).

### Handle 24:00:00 (midnight of next day) ✅ Current
```python
import arrow

# 24:00:00 is interpreted as 00:00:00 of the next day
a = arrow.get("2019-10-30T24:00:00", "YYYY-MM-DDTHH:mm:ss")
print(a)  # 2019-10-31 00:00:00
```
* `HH` token accepts `24` as midnight of the next day.

### Parse from natural language text ✅ Current
```python
import arrow

# Extract datetime from text with surrounding words
text = "Meet me at 2016-05-16T04:05:06.789120 at the restaurant."
a = arrow.get(text, "YYYY-MM-DDThh:mm:ss.S")
print(a)
```
* Arrow can extract datetime patterns from natural language text.

### Use DateTimeParser directly with caching ✅ Current
```python
from arrow.parser import DateTimeParser

# Create parser with LRU cache for compiled regex patterns
parser = DateTimeParser(cache_size=128)

# Parse with caching enabled
dt = parser.parse("2012-01-01 12:05:10", "YYYY-MM-DD HH:mm:ss")
print(dt)
```
* Use `cache_size` parameter to enable LRU caching of compiled patterns.
* Useful when parsing many strings with the same format.

### Parse with locale support ✅ Current
```python
from arrow.parser import DateTimeParser

# Create parser for French locale
fr_parser = DateTimeParser("fr")

# Parse localized day/month names
dt = fr_parser.parse("mar 2019-10-17", "ddd YYYY-MM-DD")
print(dt)
```
* Pass locale string to `DateTimeParser` for localized parsing.

## Configuration

- **Timezones**
  - `arrow.utcnow()` returns a timezone-aware Arrow in UTC.
  - `arrow.now(tz)` accepts common timezone expressions such as `"utc"`, `"local"`, or IANA names like `"Europe/Paris"`, `"US/Pacific"`.
  - Convert instants with `Arrow.to(tz)`. Reinterpret wall time (change tz metadata without converting the instant) with `Arrow.replace(tzinfo=...)` when that is explicitly desired.
- **DST ambiguity (fold)**
  - For ambiguous local times during DST fall-back, pass `fold=0` or `fold=1` when constructing/replacing an `Arrow` (e.g., `Arrow(..., fold=0)` then `.replace(fold=1)`).
- **Formatting constants**
  - Common formatter constants are available (e.g., `arrow.formatter.FORMAT_RFC3339`, `FORMAT_RFC2822`, `FORMAT_ATOM`, `FORMAT_RSS`, `FORMAT_W3C`, `FORMAT_COOKIE`, `FORMAT_RFC822`, `FORMAT_RFC850`, `FORMAT_RFC1036`, `FORMAT_RFC1123`) for consistent output formats.
- **Parser caching**
  - `DateTimeParser` supports LRU caching via the `cache_size` parameter to improve performance when parsing many strings with repeated formats.

## Pitfalls

### Wrong: Using `strptime`-style tokens with `arrow.get()` / `Arrow.format()`
```python
import arrow

# Looks reasonable but uses datetime.strptime tokens, not Arrow tokens
a = arrow.get("2013-05-05 12:30:45", "%Y-%m-%d %H:%M:%S")
print(a.format("%Y-%m-%d"))
```

### Right: Use Arrow tokens (YYYY, MM, DD, etc.)
```python
import arrow

a = arrow.get("2013-05-05 12:30:45", "YYYY-MM-DD HH:mm:ss")
print(a.format("YYYY-MM-DD"))
```

### Wrong: Using `replace(tzinfo=...)` when you mean "convert the instant"
```python
import arrow

arw = arrow.utcnow()

# This reinterprets wall time in US/Pacific (changes the instant)
pacific_wrong = arw.replace(tzinfo="US/Pacific")
print(arw)
print(pacific_wrong)
```

### Right: Use `.to(...)` to convert the same instant to another timezone
```python
import arrow

arw = arrow.utcnow()

pacific = arw.to("US/Pacific")
print(arw)
print(pacific)
```

### Wrong: Ignoring DST ambiguity for an ambiguous local time
```python
import arrow

# Ambiguous time during fall-back; fold not specified
paris = arrow.Arrow(2019, 10, 27, 2, 0, 0, tzinfo="Europe/Paris")
print(paris)
```

### Right: Specify `fold` and switch with `.replace(fold=...)`
```python
import arrow

paris_early = arrow.Arrow(2019, 10, 27, 2, 0, 0, tzinfo="Europe/Paris", fold=0)
paris_late = paris_early.replace(fold=1)

print(paris_early)
print(paris_late)
```

### Wrong: Unstable `humanize()` assertions that depend on "now"
```python
import arrow

present = arrow.utcnow()
past = arrow.utcnow().shift(hours=-1)

# Output can vary depending on runtime timing/rounding
print(past.humanize())
```

### Right: Provide an explicit reference time
```python
import arrow

present = arrow.utcnow()
past = present.shift(hours=-1)

print(past.humanize(present))
```

### Wrong: Not handling parsing errors
```python
import arrow

# Will raise ParserError if format doesn't match
a = arrow.get("01-01", "YYYY-MM-DD")
```

### Right: Catch parsing exceptions
```python
import arrow
from arrow.parser import ParserError, ParserMatchError

try:
    a = arrow.get("01-01", "YYYY-MM-DD")
except (ParserError, ParserMatchError) as e:
    print(f"Failed to parse: {e}")
```

## References

- [Documentation](https://arrow.readthedocs.io)
- [Source](https://github.com/arrow-py/arrow)
- [Issues](https://github.com/arrow-py/arrow/issues)

## Migration from v0.x

Arrow 1.4.0 requires **Python 3.8+**. If migrating from 0.x versions:

- **Python version**: Upgrade to Python 3.8 or higher.
- **Type hints**: Arrow 1.4.0 includes full PEP 484-style type hints for better IDE support and type checking.
- **Parsing/formatting**: Ensure parsing/formatting uses **Arrow tokens** (e.g., `YYYY-MM-DD`) rather than `strptime` tokens.
- **Timezone conversion**: Prefer `.to(...)` for timezone conversion; reserve `.replace(tzinfo=...)` for explicit reinterpretation.
- **DST handling**: Audit DST fall-back behavior and set `fold` where ambiguous local times matter.

## API Reference

- **arrow.__version__** - Library version string.
- **arrow.get(*args, **kwargs) -> Arrow** - Primary constructor/parser for Arrow instances (supports strings, datetimes, timestamps, formats).
- **arrow.utcnow() -> Arrow** - Current time as a timezone-aware Arrow in UTC.
- **arrow.now(tz: Optional[TZ_EXPR] = None) -> Arrow** - Current time in a specified timezone (`"utc"`, `"local"`, IANA name, etc.).
- **arrow.factory(type: Type[Arrow]) -> ArrowFactory** - Create a factory for producing Arrow objects (alternative to ArrowFactory constructor).
- **arrow.Arrow(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, **kwargs)** - Arrow datetime type (timezone-aware); key params: `year, month, day, hour, minute, second, microsecond, tzinfo`.
- **Arrow.now(tzinfo: Optional[dt_tzinfo] = None) -> Arrow** - Classmethod variant of "now".
- **Arrow.utcnow() -> Arrow** - Classmethod variant of "utcnow".
- **Arrow.fromtimestamp(timestamp: Union[int, float, str], tzinfo: Optional[TZ_EXPR] = None) -> Arrow** - Build from Unix timestamp (int/float/str) with optional timezone.
- **Arrow.utcfromtimestamp(timestamp: Union[int, float, str]) -> Arrow** - Build from Unix timestamp interpreted in UTC.
- **Arrow.fromdatetime(dt: dt_datetime, tzinfo: Optional[TZ_EXPR] = None) -> Arrow** - Build from `datetime.datetime` with optional timezone override.
- **Arrow.fromdate(date: date, tzinfo: Optional[TZ_EXPR] = None) -> Arrow** - Build from `datetime.date` with optional timezone.
- **Arrow.strptime(date_str: str, fmt: str, tzinfo: Optional[TZ_EXPR] = None) -> Arrow** - Parse with a specified format string.
- **Arrow.datetime** - Return the Arrow as a Python `datetime` object.
- **Arrow.naive** - Return a naive (timezone-unaware) `datetime` representation.
- **Arrow.tzinfo** - Return the timezone info object.
- **Arrow.year, Arrow.month, Arrow.day, Arrow.hour, Arrow.minute, Arrow.second, Arrow.microsecond** - Component accessors.
- **Arrow.date() -> date** - Return the date portion as a `datetime.date`.
- **Arrow.time() -> time** - Return the time portion as a `datetime.time`.
- **Arrow.timestamp() -> int** - Return Unix timestamp (seconds since epoch).
- **Arrow.shift(**kwargs) -> Arrow** - Return a new Arrow shifted by relative offsets (weeks, days, hours, minutes, seconds, microseconds).
- **Arrow.replace(**kwargs) -> Arrow** - Return a new Arrow with specific components replaced.
- **Arrow.to(tz: TZ_EXPR) -> Arrow** - Convert to another timezone.
- **Arrow.format(fmt: str) -> str** - Format using Arrow tokens.
- **Arrow.humanize(other: Optional[Arrow] = None, only_distance: bool = False, granularity: Union[str, List[str]] = "auto") -> str** - Human-readable representation relative to another time.
- **Arrow.dehumanize(input_string: str) -> Arrow** - Parse human-readable relative time string.
- **Arrow.span(frame: str, count: int = 1) -> Tuple[Arrow, Arrow]** - Return a tuple of (floor, ceil) for the given time frame.
- **Arrow.floor(frame: str) -> Arrow** - Floor to the start of the given time frame.
- **Arrow.ceil(frame: str) -> Arrow** - Ceil to the end of the given time frame.
- **Arrow.span_range(frame: str, start: Arrow, end: Arrow) -> Iterator[Tuple[Arrow, Arrow]]** - Generate span tuples between start and end.
- **Arrow.range(frame: str, start: Arrow, end: Arrow) -> Iterator[Arrow]** - Generate Arrow instances between start and end.
- **Arrow.ambiguous** - Property indicating whether the time is ambiguous during DST transitions.
- **arrow.ArrowFactory(type: Type[Arrow] = Arrow)** - Factory for producing Arrow objects (useful for Arrow subclasses).
- **arrow.ParserError** - Exception raised for parsing failures.
- **arrow.parser.ParserMatchError** - Exception raised when parsing format doesn't match input.
- **arrow.parser.DateTimeParser(locale: str = DEFAULT_LOCALE, cache_size: int = 0)** - Parser for datetime strings with various formats.
- **DateTimeParser.parse(date_str: str, fmt: Union[str, List[str]]) -> datetime** - Parse a datetime string with given format(s).
- **DateTimeParser.parse_iso(date_str: str) -> datetime** - Parse ISO format datetime strings.
- **arrow.formatter.FORMAT_ATOM, FORMAT_COOKIE, FORMAT_RFC822, FORMAT_RFC850, FORMAT_RFC1036, FORMAT_RFC1123, FORMAT_RFC2822, FORMAT_RFC3339, FORMAT_RFC3339_STRICT, FORMAT_RSS, FORMAT_W3C** - Common predefined format string constants.
- **arrow.constants.MAX_TIMESTAMP, MAX_TIMESTAMP_MS, MAX_TIMESTAMP_US** - Maximum timestamp values.
- **arrow.constants.DEFAULT_LOCALE** - Default locale string constant.

## Current Library State

Arrow 1.4.0 is a mature, fully-implemented, drop-in replacement for Python's `datetime` module with enhanced timezone and parsing capabilities. The library provides:

- Timezone-aware datetime handling by default
- Flexible parsing with Arrow's own token system
- Human-readable time representations
- ISO 8601 compliance
- Full PEP 484 type hint support
- Extensibility via subclassing
- Locale support for internationalized parsing and formatting

The API is stable with broad compatibility across Python datetime, dateutil, pytz, and the standard library's zoneinfo (Python 3.9+).