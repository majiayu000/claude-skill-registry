---
name: web-utilities-date-fns
description: date-fns patterns for TypeScript - formatting, parsing, manipulation, comparison, timezone handling, and internationalization
---

# date-fns Date Utility Patterns

> **Quick Guide:** Use date-fns for modular, tree-shakeable date operations. Import only what you need. Use `parseISO` for ISO strings, `format` with Unicode tokens for display, and pure functions that return new Date objects. For timezones, use `@date-fns/tz` with `TZDate` (v4+) or `date-fns-tz` with `formatInTimeZone` (v3.x). Never mutate dates.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `parseISO()` for ISO 8601 strings - NEVER use `new Date(string)` which has browser inconsistencies)**

**(You MUST import only needed functions - NEVER use `import * as dateFns` which defeats tree-shaking)**

**(You MUST use pure functions that return new dates - NEVER mutate dates with `setDate()` or similar)**

**(You MUST use named constants for format strings and durations - NO magic strings like 'yyyy-MM-dd' scattered in code)**

</critical_requirements>

---

**Auto-detection:** date-fns, format, parseISO, addDays, subMonths, differenceInDays, formatDistance, isAfter, isBefore, eachDayOfInterval, date-fns-tz, @date-fns/tz, @date-fns/utc, TZDate, TZDateMini, UTCDate, UTCDateMini, tz(), transpose, tzName, tzScan, withTimeZone, locale

**When to use:**

- Formatting dates for display with locale support
- Parsing date strings into Date objects
- Date arithmetic (add/subtract days, months, years)
- Comparing dates and checking intervals
- Calculating differences between dates
- Generating date ranges for calendars
- Relative time formatting ("2 hours ago")

**When NOT to use:**

- Simple date display - use `Intl.DateTimeFormat` (zero bundle cost)
- Very simple operations - native `Date` may suffice
- Complex recurring dates - use `rrule.js` alongside
- Future projects with Temporal API browser support

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

date-fns is a **modular, functional** date utility library. Each function is independent, enabling tree-shaking to include only what you use. All functions are **pure** - they return new Date objects rather than mutating inputs. This makes date operations predictable and testable.

**Key principle:** Import what you need, let bundlers remove the rest. A simple `format` import adds ~2KB, not the entire 80KB library.

```typescript
// Tree-shakeable - only includes format and parseISO
import { format, parseISO } from "date-fns";

// Format constant at module level
const DATE_DISPLAY_FORMAT = "MMMM d, yyyy";

const date = parseISO("2026-01-15");
const display = format(date, DATE_DISPLAY_FORMAT); // "January 15, 2026"
```

**v3+ is 100% TypeScript** with built-in type definitions. No `@types/date-fns` needed.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Format Tokens (Unicode TR35)

date-fns uses Unicode Technical Standard #35 format tokens. These differ from Moment.js.

#### Format Token Reference

```typescript
import { format } from "date-fns";

// Format string constants
const ISO_DATE_FORMAT = "yyyy-MM-dd";
const ISO_DATETIME_FORMAT = "yyyy-MM-dd'T'HH:mm:ss'Z'";
const DISPLAY_DATE_FORMAT = "MMMM d, yyyy";
const DISPLAY_TIME_FORMAT = "h:mm a";
const DISPLAY_DATETIME_FORMAT = "MMMM d, yyyy 'at' h:mm a";

const date = new Date(2026, 0, 15, 14, 30, 0);

// Year
format(date, "yyyy"); // "2026" (4-digit)
format(date, "yy"); // "26" (2-digit)

// Month
format(date, "MMMM"); // "January" (full name)
format(date, "MMM"); // "Jan" (abbreviated)
format(date, "MM"); // "01" (2-digit)
format(date, "M"); // "1" (1 or 2 digit)

// Day
format(date, "dd"); // "15" (2-digit)
format(date, "d"); // "15" (1 or 2 digit)
format(date, "do"); // "15th" (ordinal)

// Day of week
format(date, "EEEE"); // "Thursday" (full)
format(date, "EEE"); // "Thu" (abbreviated)
format(date, "EEEEE"); // "T" (narrow)

// Hour
format(date, "HH"); // "14" (24-hour, 2-digit)
format(date, "H"); // "14" (24-hour)
format(date, "hh"); // "02" (12-hour, 2-digit)
format(date, "h"); // "2" (12-hour)

// Minute and Second
format(date, "mm"); // "30" (minutes)
format(date, "ss"); // "00" (seconds)

// AM/PM
format(date, "a"); // "PM"
format(date, "aaaa"); // "p.m."

// Timezone
format(date, "z"); // "EST" (short)
format(date, "zzzz"); // "Eastern Standard Time" (full)
```

**Why good:** named constants make format strings reusable and discoverable, Unicode tokens are standard across date libraries

---

### Pattern 2: Locale-Aware Format Shortcuts

Use `P`, `PP`, `PPP`, `PPPP` for locale-aware date formatting without specifying exact format.

```typescript
import { format } from "date-fns";
import { enUS, de, ja, fr } from "date-fns/locale";

const date = new Date(2026, 0, 15);

// ✅ Good Example - Locale-aware formatting
// Short date
format(date, "P", { locale: enUS }); // "01/15/2026"
format(date, "P", { locale: de }); // "15.01.2026"
format(date, "P", { locale: ja }); // "2026/01/15"

// Medium date
format(date, "PP", { locale: enUS }); // "Jan 15, 2026"
format(date, "PP", { locale: de }); // "15. Jan. 2026"

// Long date
format(date, "PPP", { locale: enUS }); // "January 15th, 2026"
format(date, "PPP", { locale: fr }); // "15 janvier 2026"

// Full date
format(date, "PPPP", { locale: enUS }); // "Thursday, January 15th, 2026"
format(date, "PPPP", { locale: ja }); // "2026年1月15日木曜日"

// Time shortcuts
format(date, "p", { locale: enUS }); // "12:00 AM"
format(date, "pp", { locale: enUS }); // "12:00:00 AM"

// Combined date and time
format(date, "PPpp", { locale: enUS }); // "Jan 15, 2026, 12:00:00 AM"
```

**Why good:** `P`/`PP`/`PPP` adapt to locale conventions automatically, users see dates in familiar format for their region

```typescript
// ❌ Bad Example - Hardcoded format ignores locale
format(date, "MM/dd/yyyy"); // "01/15/2026" - wrong for most of world!
```

**Why bad:** hardcoded MM/dd/yyyy format is US-specific, confusing for European and Asian users who expect different order

---

### Pattern 3: Safe Parsing with parseISO

Use `parseISO` for ISO 8601 strings. Use `parse` for custom formats.

```typescript
import { parseISO, parse, isValid } from "date-fns";

// ✅ Good Example - parseISO for ISO strings
const isoDate = parseISO("2026-01-15");
const isoDateTime = parseISO("2026-01-15T14:30:00Z");
const isoWithOffset = parseISO("2026-01-15T14:30:00+05:30");

// Custom format parsing
const CUSTOM_DATE_FORMAT = "dd/MM/yyyy";
const customDate = parse("15/01/2026", CUSTOM_DATE_FORMAT, new Date());

// Always validate parsed dates
function safeParseDateString(
  dateString: string,
  formatString: string,
): Date | null {
  const parsed = parse(dateString, formatString, new Date());
  return isValid(parsed) ? parsed : null;
}

// Strict parsing - verify round-trip
function strictParseDateString(
  dateString: string,
  formatString: string,
): Date | null {
  const parsed = parse(dateString, formatString, new Date());
  if (!isValid(parsed)) return null;

  // Verify the date matches input (catches invalid dates like Feb 30)
  if (format(parsed, formatString) !== dateString) return null;

  return parsed;
}
```

**Why good:** parseISO handles all ISO 8601 variants correctly, isValid catches invalid dates, round-trip verification prevents Feb 30 becoming March 2

```typescript
// ❌ Bad Example - Using Date constructor
const date1 = new Date("2026-01-15"); // Browser-inconsistent!
const date2 = new Date("01/15/2026"); // May fail in non-US browsers
```

**Why bad:** `new Date(string)` parsing varies by browser and locale, can produce unexpected results or Invalid Date

---

### Pattern 4: Date Arithmetic

Use pure functions for date manipulation. All return new Date objects.

```typescript
import {
  addDays,
  addMonths,
  addYears,
  subDays,
  subMonths,
  subYears,
  addHours,
  addMinutes,
} from "date-fns";

// Duration constants
const WEEK_IN_DAYS = 7;
const BILLING_CYCLE_MONTHS = 1;
const TRIAL_PERIOD_DAYS = 14;

const date = new Date(2026, 0, 15);

// ✅ Good Example - Pure functions return new dates
const nextWeek = addDays(date, WEEK_IN_DAYS); // Jan 22, 2026
const nextMonth = addMonths(date, BILLING_CYCLE_MONTHS); // Feb 15, 2026
const nextYear = addYears(date, 1); // Jan 15, 2027

const lastWeek = subDays(date, WEEK_IN_DAYS); // Jan 8, 2026
const trialEnd = addDays(date, TRIAL_PERIOD_DAYS); // Jan 29, 2026

// Chain operations
const twoWeeksFromNextMonth = addDays(addMonths(date, 1), WEEK_IN_DAYS * 2);

// Original date is unchanged
console.log(date); // Still Jan 15, 2026
```

**Why good:** pure functions are predictable and testable, original date unchanged, constants document business logic

```typescript
// ❌ Bad Example - Mutating dates
const date = new Date(2026, 0, 15);
date.setDate(date.getDate() + 7); // Mutates original!
// Original date is now changed - causes bugs in shared references
```

**Why bad:** mutation creates side effects, especially problematic when date is passed as prop or stored in state

---

### Pattern 5: Date Boundaries

Use boundary functions for consistent start/end of periods.

```typescript
import {
  startOfDay,
  endOfDay,
  startOfWeek,
  endOfWeek,
  startOfMonth,
  endOfMonth,
  startOfQuarter,
  endOfQuarter,
  startOfYear,
  endOfYear,
} from "date-fns";

const date = new Date(2026, 0, 15, 14, 30, 0);

// ✅ Good Example - Boundary functions for consistent ranges
const dayStart = startOfDay(date); // Jan 15, 2026 00:00:00
const dayEnd = endOfDay(date); // Jan 15, 2026 23:59:59.999

// Week boundaries (weekStartsOn: 1 = Monday)
const weekStart = startOfWeek(date, { weekStartsOn: 1 }); // Jan 13, 2026
const weekEnd = endOfWeek(date, { weekStartsOn: 1 }); // Jan 19, 2026

const monthStart = startOfMonth(date); // Jan 1, 2026
const monthEnd = endOfMonth(date); // Jan 31, 2026 23:59:59.999

// Useful for date range queries
interface DateRange {
  start: Date;
  end: Date;
}

function getMonthRange(date: Date): DateRange {
  return {
    start: startOfMonth(date),
    end: endOfMonth(date),
  };
}
```

**Why good:** boundary functions handle edge cases (month lengths, leap years), consistent for database queries and filtering

---

### Pattern 6: Date Comparisons

Use comparison functions instead of manual timestamp comparisons.

```typescript
import {
  isAfter,
  isBefore,
  isEqual,
  isSameDay,
  isSameMonth,
  isSameYear,
  isWithinInterval,
  isToday,
  isPast,
  isFuture,
  isWeekend,
} from "date-fns";

const date1 = new Date(2026, 0, 15);
const date2 = new Date(2026, 0, 20);

// ✅ Good Example - Semantic comparison functions
const isLater = isAfter(date2, date1); // true
const isEarlier = isBefore(date1, date2); // true
const areSame = isEqual(date1, date1); // true

// Same period checks (ignore time)
const sameDay = isSameDay(date1, date1); // true
const sameMonth = isSameMonth(date1, date2); // true (both January)
const sameYear = isSameYear(date1, date2); // true (both 2026)

// Range check
const isInRange = isWithinInterval(new Date(2026, 0, 17), {
  start: date1,
  end: date2,
}); // true

// Convenience checks
const todayCheck = isToday(new Date()); // true
const pastCheck = isPast(date1); // depends on current date
const futureCheck = isFuture(date2); // depends on current date
const weekendCheck = isWeekend(date1); // false (Thursday)
```

**Why good:** semantic function names make code readable, handles edge cases like time zone differences

```typescript
// ❌ Bad Example - Manual timestamp comparison
const isLater = date2.getTime() > date1.getTime();
const sameDay =
  date1.getFullYear() === date2.getFullYear() &&
  date1.getMonth() === date2.getMonth() &&
  date1.getDate() === date2.getDate();
```

**Why bad:** verbose, error-prone, doesn't handle edge cases, hard to read intent

</patterns>

---

<integration>

## Integration Guide

**date-fns integrates with:**

- **React Query**: Format dates in query results, use for cache key generation
- **Zod**: Create date schemas with `z.string().transform()` + date-fns parsing
- **React Hook Form**: Date validation and transformation
- **i18n libraries**: Use with locale imports for internationalized formatting

**Version Notes:**

- **v4+** (current): Uses `@date-fns/tz` for timezone handling with `TZDate` class and `tz()` helper
- **v3.x**: Uses `date-fns-tz` package with `formatInTimeZone`, `toZonedTime`, `fromZonedTime`
- v4 is ESM-first; constants must be imported from `date-fns/constants`
- v4 returns Invalid Date/NaN instead of throwing errors for invalid inputs
- All versions are 100% TypeScript with built-in types

**v4 Bundle Size Reference:**

- Core date-fns function: ~2KB each (tree-shakeable)
- `TZDate`: 1.2 KB | `TZDateMini`: 916 B (use Mini for internal calculations)
- `UTCDate`: 504 B | `UTCDateMini`: 239 B (use Mini for internal calculations)
- Recommendation: Use `TZDateMini`/`UTCDateMini` internally, full classes when exposing from libraries

**v4 Key Functions:**

- `tz()`: Creates timezone context for the `in` option
- `transpose()`: Converts dates between timezones (replaces `toZonedTime`/`fromZonedTime`)
- `tzName()`: Returns human-readable timezone name (short, long, generic formats)
- `tzScan()`: Detects DST transitions within a date range
- `.withTimeZone()`: TZDate method for timezone conversion

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `parseISO()` for ISO 8601 strings - NEVER use `new Date(string)` which has browser inconsistencies)**

**(You MUST import only needed functions - NEVER use `import * as dateFns` which defeats tree-shaking)**

**(You MUST use pure functions that return new dates - NEVER mutate dates with `setDate()` or similar)**

**(You MUST use named constants for format strings and durations - NO magic strings like 'yyyy-MM-dd' scattered in code)**

**Failure to follow these rules will cause browser inconsistencies, bundle bloat, and mutation bugs.**

</critical_reminders>
