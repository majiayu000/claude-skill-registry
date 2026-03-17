---
name: nodatime
description: >
  Guidance for NodaTime date and time library for .NET.
  USE FOR: precise date/time handling, time zone conversions, period and duration calculations, calendar-aware date arithmetic, replacing ambiguous DateTime usage, scheduling across time zones.
  DO NOT USE FOR: simple timestamp logging (use DateTimeOffset), timer-based scheduling (use PeriodicTimer), date formatting only (use standard .NET formatting), legacy .NET Framework DateTime interop without conversion.
license: MIT
metadata:
  displayName: NodaTime
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "NodaTime Documentation"
    url: "https://nodatime.org/"
  - title: "NodaTime GitHub Repository"
    url: "https://github.com/nodatime/nodatime"
  - title: "NodaTime NuGet Package"
    url: "https://www.nuget.org/packages/NodaTime"
---

# NodaTime

## Overview

NodaTime is an alternative date and time library for .NET that replaces the ambiguous `DateTime` type with a set of distinct types, each representing a specific concept: an instant in time, a local date, a local time, a zoned date/time, and more. By making these distinctions explicit in the type system, NodaTime prevents common bugs caused by confusing UTC times with local times or ignoring time zone transitions.

NodaTime uses the IANA time zone database (TZDB) for accurate historical and future time zone data, making it more reliable than the Windows time zone database for cross-platform applications.

Install via NuGet:
```
dotnet add package NodaTime
dotnet add package NodaTime.Serialization.SystemTextJson
```

## Core Type System

NodaTime separates date/time concepts into distinct types to prevent misuse.

```csharp
using NodaTime;

// Instant: a point on the global timeline (like UTC)
Instant now = SystemClock.Instance.GetCurrentInstant();
Console.WriteLine($"Now (instant): {now}");

// LocalDate: a date without time or zone (e.g., a birthday)
LocalDate birthday = new LocalDate(1990, 6, 15);
Console.WriteLine($"Birthday: {birthday}");

// LocalTime: a time without date or zone (e.g., store opening)
LocalTime opening = new LocalTime(9, 30, 0);
Console.WriteLine($"Opens at: {opening}");

// LocalDateTime: date + time, no zone (e.g., "meeting at 3 PM")
LocalDateTime meeting = new LocalDateTime(2025, 3, 15, 15, 0, 0);
Console.WriteLine($"Meeting: {meeting}");

// ZonedDateTime: date + time + zone (fully resolved)
DateTimeZone newYork = DateTimeZoneProviders.Tzdb["America/New_York"];
ZonedDateTime zonedMeeting = meeting.InZoneLeniently(newYork);
Console.WriteLine($"Meeting (NYC): {zonedMeeting}");

// OffsetDateTime: date + time + fixed UTC offset (no DST rules)
OffsetDateTime offset = now.WithOffset(Offset.FromHours(-5));
Console.WriteLine($"Offset: {offset}");
```

## Time Zone Conversions

Convert between time zones using `DateTimeZone` and `ZonedDateTime`.

```csharp
using NodaTime;

var clock = SystemClock.Instance;
Instant now = clock.GetCurrentInstant();

// Get time zones
DateTimeZone eastern = DateTimeZoneProviders.Tzdb["America/New_York"];
DateTimeZone pacific = DateTimeZoneProviders.Tzdb["America/Los_Angeles"];
DateTimeZone tokyo = DateTimeZoneProviders.Tzdb["Asia/Tokyo"];
DateTimeZone london = DateTimeZoneProviders.Tzdb["Europe/London"];

// Convert instant to various zones
ZonedDateTime easternTime = now.InZone(eastern);
ZonedDateTime pacificTime = now.InZone(pacific);
ZonedDateTime tokyoTime = now.InZone(tokyo);
ZonedDateTime londonTime = now.InZone(london);

Console.WriteLine($"New York:   {easternTime:uuuu-MM-dd HH:mm:ss z}");
Console.WriteLine($"Los Angeles: {pacificTime:uuuu-MM-dd HH:mm:ss z}");
Console.WriteLine($"Tokyo:      {tokyoTime:uuuu-MM-dd HH:mm:ss z}");
Console.WriteLine($"London:     {londonTime:uuuu-MM-dd HH:mm:ss z}");

// Convert between zones
ZonedDateTime nycMeeting = new LocalDateTime(2025, 7, 15, 14, 0, 0)
    .InZoneLeniently(eastern);
ZonedDateTime tokyoEquivalent = nycMeeting.WithZone(tokyo);
Console.WriteLine($"NYC 2 PM = Tokyo {tokyoEquivalent:HH:mm} (next day: {tokyoEquivalent.Date})");
```

## Periods and Durations

`Period` represents a human calendar-based difference (years, months, days). `Duration` represents an exact elapsed time.

```csharp
using NodaTime;

// Period: calendar-based (accounts for varying month lengths)
LocalDate start = new LocalDate(2024, 1, 31);
LocalDate end = new LocalDate(2025, 3, 15);
Period period = Period.Between(start, end);
Console.WriteLine($"Between: {period.Years} years, {period.Months} months, {period.Days} days");

// Age calculation
LocalDate birthDate = new LocalDate(1990, 6, 15);
LocalDate today = LocalDate.FromDateTime(DateTime.Today);
Period age = Period.Between(birthDate, today, PeriodUnits.Years);
Console.WriteLine($"Age: {age.Years} years");

// Duration: exact elapsed time
Instant start2 = SystemClock.Instance.GetCurrentInstant();
// ... work happens ...
Instant end2 = SystemClock.Instance.GetCurrentInstant();
Duration elapsed = end2 - start2;
Console.WriteLine($"Elapsed: {elapsed.TotalMilliseconds:F0}ms");

// Date arithmetic
LocalDate nextBirthday = birthDate.PlusYears(today.Year - birthDate.Year);
if (nextBirthday <= today) nextBirthday = nextBirthday.PlusYears(1);
Period untilBirthday = Period.Between(today, nextBirthday, PeriodUnits.Days);
Console.WriteLine($"Days until birthday: {untilBirthday.Days}");
```

## Handling DST Transitions

NodaTime makes DST transitions explicit rather than silently adjusting times.

```csharp
using NodaTime;

DateTimeZone eastern = DateTimeZoneProviders.Tzdb["America/New_York"];

// Spring forward: 2:00 AM -> 3:00 AM (2:30 AM does not exist)
LocalDateTime springForward = new LocalDateTime(2025, 3, 9, 2, 30, 0);

// InZoneLeniently returns 3:30 AM (moved forward)
ZonedDateTime lenient = springForward.InZoneLeniently(eastern);
Console.WriteLine($"Lenient (spring): {lenient}");

// InZoneStrictly throws AmbiguousTimeException or SkippedTimeException
try
{
    ZonedDateTime strict = springForward.InZoneStrictly(eastern);
}
catch (SkippedTimeException ex)
{
    Console.WriteLine($"Skipped time: {ex.Message}");
}

// Fall back: 1:00 AM occurs twice
LocalDateTime fallBack = new LocalDateTime(2025, 11, 2, 1, 30, 0);
try
{
    ZonedDateTime strictFall = fallBack.InZoneStrictly(eastern);
}
catch (AmbiguousTimeException ex)
{
    Console.WriteLine($"Ambiguous time: {ex.Message}");
    // Resolve explicitly
    ZonedDateTime earlier = ex.EarlierMapping.Map(fallBack);
    ZonedDateTime later = ex.LaterMapping.Map(fallBack);
    Console.WriteLine($"Earlier (EDT): {earlier}");
    Console.WriteLine($"Later (EST):   {later}");
}
```

## JSON Serialization

Integrate NodaTime types with System.Text.Json for API serialization.

```csharp
using System.Text.Json;
using NodaTime;
using NodaTime.Serialization.SystemTextJson;

var options = new JsonSerializerOptions
{
    WriteIndented = true
};
options.ConfigureForNodaTime(DateTimeZoneProviders.Tzdb);

var appointment = new
{
    Title = "Team Standup",
    ScheduledAt = SystemClock.Instance.GetCurrentInstant(),
    Date = new LocalDate(2025, 3, 15),
    Time = new LocalTime(9, 0, 0),
    Duration = Duration.FromMinutes(30)
};

string json = JsonSerializer.Serialize(appointment, options);
Console.WriteLine(json);
// { "Title": "Team Standup", "ScheduledAt": "2025-01-15T10:30:00Z", ... }
```

## NodaTime vs System DateTime Types

| Concept | NodaTime | System | Ambiguity Risk |
|---------|----------|--------|---------------|
| Point in time | `Instant` | `DateTimeOffset` | Low |
| Local date only | `LocalDate` | `DateOnly` (.NET 6+) | Low |
| Local time only | `LocalTime` | `TimeOnly` (.NET 6+) | Low |
| Date + time, no zone | `LocalDateTime` | `DateTime` (Unspecified) | Medium |
| Date + time + zone | `ZonedDateTime` | None (no equivalent) | N/A |
| Date + time + offset | `OffsetDateTime` | `DateTimeOffset` | Low |
| Calendar difference | `Period` | None | N/A |
| Exact elapsed time | `Duration` | `TimeSpan` | Low |
| Time zone | `DateTimeZone` | `TimeZoneInfo` | Medium |

## Best Practices

1. **Use `Instant` for timestamps** stored in databases, logs, and APIs -- it represents an unambiguous point in time equivalent to UTC.
2. **Use `LocalDate` for dates that have no time component** (birthdays, holidays, business dates) instead of `DateTime` with time set to midnight.
3. **Use `ZonedDateTime` when you need to display or reason about time in a specific zone** -- it carries both the instant and the zone rules.
4. **Prefer IANA time zone IDs** (`America/New_York`) over Windows IDs (`Eastern Standard Time`) for cross-platform compatibility and accuracy.
5. **Use `InZoneStrictly` during development** to catch DST ambiguities as exceptions, and switch to `InZoneLeniently` or custom resolvers in production with logging.
6. **Store `Instant` in databases and convert to `ZonedDateTime` at the presentation layer** to keep stored data unambiguous and let the UI handle user-local display.
7. **Use `Period` for human-calendar calculations** (age, months until expiry) and `Duration` for machine-elapsed time (timeouts, benchmarks).
8. **Configure NodaTime JSON serialization** with `ConfigureForNodaTime` on `JsonSerializerOptions` so API models can use NodaTime types directly.
9. **Inject `IClock` instead of using `SystemClock.Instance` directly** so tests can use `FakeClock` to control time without modifying system state.
10. **Update the TZDB data regularly** by updating the `NodaTime.Tzdb` NuGet package, since time zone rules change frequently (governments modify DST dates).
