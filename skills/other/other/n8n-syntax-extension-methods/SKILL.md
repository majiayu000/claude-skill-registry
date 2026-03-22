---
name: n8n-syntax-extension-methods
description: >
  Use when transforming data in expressions, formatting dates, manipulating
  arrays/objects, or working with binary file metadata. Prevents using
  unavailable methods and incorrect method signatures. Covers 17 string methods
  (.extractEmail, .hash, .toDateTime, .urlEncode), 21 array methods (.pluck,
  .removeDuplicates, .chunk, .smartJoin), 13 number methods, 12 object methods
  (.compact, .keepFieldsContaining), 3 boolean methods, 25+ DateTime/Luxon
  methods (.plus, .minus, .format, .diffTo), and 7 BinaryFile properties.
  Keywords: n8n, extension methods, string, array, DateTime, Luxon, pluck,
  extractEmail, removeDuplicates, binary file.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Extension Methods

> Complete reference for all n8n v1.x expression extension methods.
> ALWAYS use extension methods over raw JavaScript equivalents — they are null-safe and optimized for n8n's expression engine.

## Quick Reference — Method Categories

| Category | Count | Common Use Cases |
|----------|-------|-----------------|
| **String** | 19 methods | Extract emails/URLs, encode/decode, hash, case conversion |
| **Array** | 21 methods | Pluck fields, deduplicate, chunk, set operations |
| **Number** | 11 methods | Round, format, type checks, convert to DateTime |
| **Object** | 12 methods | Filter fields, merge, compact, serialize |
| **Boolean** | 3 methods | Convert to number/string, null check |
| **DateTime** | 25+ methods | Arithmetic, comparison, formatting, timezone |
| **BinaryFile** | 7 properties | File metadata access |

> Full method signatures and parameters: [references/methods.md](references/methods.md)
> Practical examples: [references/examples.md](references/examples.md)
> Common mistakes: [references/anti-patterns.md](references/anti-patterns.md)

## Decision Tree — Which Method Category?

```
What data type are you working with?
|
+-- String value?
|   +-- Need to extract structured data? --> .extractEmail(), .extractUrl(), .extractDomain()
|   +-- Need to validate? --> .isEmail(), .isUrl(), .isEmpty()
|   +-- Need encoding/hashing? --> .urlEncode(), .base64Encode(), .hash()
|   +-- Need case conversion? --> .toTitleCase(), .toSnakeCase(), .toSentenceCase()
|   +-- Need type conversion? --> .toDateTime(), .toBoolean()
|
+-- Array value?
|   +-- Need specific fields from objects? --> .pluck("field1", "field2")
|   +-- Need deduplication? --> .removeDuplicates() or .unique()
|   +-- Need set operations? --> .union(), .intersection(), .difference()
|   +-- Need aggregation? --> .sum(), .average(), .min(), .max()
|   +-- Need restructuring? --> .chunk(), .smartJoin(), .renameKeys()
|
+-- Number value?
|   +-- Need rounding? --> .round(), .ceil(), .floor()
|   +-- Need formatting? --> .format(locale)
|   +-- Need type check? --> .isEven(), .isOdd(), .isInteger()
|   +-- Need conversion? --> .toDateTime(), .toBoolean()
|
+-- Object value?
|   +-- Need to filter fields? --> .keepFieldsContaining(), .removeFieldsContaining()
|   +-- Need to clean nulls? --> .compact()
|   +-- Need to check structure? --> .hasField(), .keys(), .values()
|   +-- Need to combine? --> .merge()
|   +-- Need serialization? --> .toJsonString(), .urlEncode()
|
+-- DateTime value?
|   +-- Need arithmetic? --> .plus(), .minus()
|   +-- Need comparison? --> .equals(), .isBetween(), .diffTo()
|   +-- Need formatting? --> .format(), .toISO(), .toRelative()
|   +-- Need extraction? --> .year, .month, .day, .hour, .weekday
|   +-- Need timezone? --> .setZone(), .toUTC(), .toLocal()
|
+-- Boolean value?
|   +-- Need number? --> .toNumber()
|   +-- Need string? --> .toString()
|
+-- Binary file?
    +-- Need file info? --> .fileName, .fileSize, .mimeType, .fileExtension
```

## String Methods — Overview

19 methods for extraction, validation, encoding, conversion, and formatting.

**Extraction group**: `.extractEmail()`, `.extractUrl()`, `.extractDomain()`, `.extractUrlPath()`
**Validation group**: `.isEmail()`, `.isUrl()`, `.isEmpty()`, `.isNotEmpty()`
**Encoding group**: `.urlEncode()`, `.urlDecode()`, `.base64Encode()`, `.base64Decode()`, `.hash()`
**Conversion group**: `.toDateTime()`, `.toBoolean()`
**Formatting group**: `.toSentenceCase()`, `.toSnakeCase()`, `.toTitleCase()`, `.quote()`, `.removeMarkdown()`, `.replaceSpecialChars()`

Key behavior:
- `.extractEmail()` returns `undefined` if no email found — ALWAYS check with `.isEmpty()` or use `$ifEmpty()`
- `.hash()` defaults to `md5` — ALWAYS specify algorithm explicitly for clarity: `.hash("sha256")`
- `.toBoolean()` treats `"0"`, `"false"`, `"no"` as false (case-insensitive), everything else as true
- `.urlEncode(true)` encodes ALL characters including URI syntax chars (`/`, `?`, `&`)

## Array Methods — Overview

21 methods for extraction, deduplication, set operations, aggregation, and restructuring.

**Extraction group**: `.first()`, `.last()`, `.randomItem()`, `.pluck()`
**Deduplication group**: `.removeDuplicates()`, `.unique()`, `.union()`
**Set operations**: `.difference()`, `.intersection()`, `.union()`
**Aggregation**: `.sum()`, `.average()`, `.min()`, `.max()`
**Restructuring**: `.chunk()`, `.smartJoin()`, `.renameKeys()`, `.append()`, `.compact()`

Key behavior:
- `.pluck("name")` extracts a single field; `.pluck("name", "email")` extracts multiple fields as sub-objects
- `.removeDuplicates()` works on primitives; `.removeDuplicates("email")` deduplicates objects by key
- `.smartJoin("id", "value")` transforms `[{id: "a", value: 1}, {id: "b", value: 2}]` into `{a: 1, b: 2}`
- `.average()` and `.sum()` throw errors on non-numeric arrays — ALWAYS ensure numeric data first

## Number Methods — Overview

11 methods for rounding, formatting, type checks, and conversion.

Key behavior:
- `.format()` uses `Intl.NumberFormat` — pass locale for regional formatting: `.format("de-DE")`
- `.round(2)` rounds to 2 decimal places; `.round()` rounds to nearest integer
- `.isEven()` and `.isOdd()` throw errors on non-integers — ALWAYS check `.isInteger()` first
- `.toDateTime()` interprets numbers as Unix milliseconds by default; use `.toDateTime("s")` for seconds, `.toDateTime("excel")` for Excel serial dates

## Object Methods — Overview

12 methods for filtering, merging, checking, and serializing.

Key behavior:
- `.compact()` removes fields with `null` or `""` values — does NOT remove `0` or `false`
- `.merge(other)` gives precedence to the BASE object, not the argument
- `.keepFieldsContaining("test")` and `.removeFieldsContaining("test")` match partial string values
- `.hasField("name")` checks top-level keys ONLY — does NOT check nested fields
- `.urlEncode()` produces query string format: `key1=value1&key2=value2`

## DateTime Methods — Overview (Luxon-based)

25+ methods organized as property accessors, transformations, comparisons, and formatters.

**Property accessors**: `.year`, `.month`, `.day`, `.hour`, `.minute`, `.second`, `.weekday`, `.weekNumber`, `.quarter`, `.monthLong`, `.weekdayLong`
**Transformation**: `.plus()`, `.minus()`, `.set()`, `.startOf()`, `.endOf()`, `.setZone()`, `.toUTC()`, `.toLocal()`
**Comparison**: `.equals()`, `.hasSame()`, `.isBetween()`, `.diffTo()`, `.diffToNow()`
**Formatting**: `.format()`, `.toISO()`, `.toRelative()`, `.toLocaleString()`, `.toMillis()`, `.toSeconds()`

Key behavior:
- `.plus(5, "days")` and `.minus({days: 5, hours: 3})` — supports both positional and object syntax
- `.format("yyyy-MM-dd")` uses Luxon tokens, NOT moment.js tokens
- `.diffTo(other, "days")` returns a Duration object — access `.days` property for the number
- `.isBetween(start, end)` is exclusive on both bounds
- ALWAYS use `$now` and `$today` instead of `new Date()` — they respect workflow timezone

### Luxon Format Tokens

| Token | Output | Example |
|-------|--------|---------|
| `yyyy` | 4-digit year | 2026 |
| `MM` | 2-digit month | 03 |
| `dd` | 2-digit day | 19 |
| `HH` | 24-hour hour | 14 |
| `mm` | Minute | 05 |
| `ss` | Second | 09 |
| `SSS` | Millisecond | 123 |
| `EEEE` | Full weekday | Wednesday |
| `EEE` | Short weekday | Wed |
| `MMMM` | Full month | March |
| `MMM` | Short month | Mar |
| `a` | AM/PM | PM |
| `Z` | UTC offset | +01:00 |
| `ZZZZ` | Timezone name | Central European Time |

Common patterns:
- ISO date: `yyyy-MM-dd` → `2026-03-19`
- ISO datetime: `yyyy-MM-dd'T'HH:mm:ss` → `2026-03-19T14:05:09`
- Human-readable: `EEEE, MMMM dd yyyy` → `Wednesday, March 19 2026`
- Time only: `HH:mm:ss` → `14:05:09`
- European date: `dd-MM-yyyy` → `19-03-2026`

## Boolean Methods — Overview

3 methods: `.isEmpty()`, `.toNumber()`, `.toString()`.

- `.isEmpty()` returns `false` for ALL boolean values; only returns `true` for `null`
- `.toNumber()` converts `true` → `1`, `false` → `0`

## BinaryFile Properties — Overview

7 read-only properties for file metadata access via `$binary.data`:

| Property | Example Value |
|----------|--------------|
| `.fileName` | `"report.pdf"` |
| `.fileExtension` | `"pdf"` |
| `.fileSize` | `"125432"` (bytes, as string) |
| `.mimeType` | `"application/pdf"` |
| `.fileType` | `"application"` |
| `.directory` | `"/tmp/uploads"` (empty if DB-stored) |
| `.id` | `"abc123"` (disk/S3 storage ID) |

Key behavior:
- `.fileSize` returns a STRING, not a number — ALWAYS convert with `parseInt()` for math operations
- `.directory` is NOT set when binary data is stored in the database — ALWAYS check before using
- `.fileType` returns only the first part of the MIME type (e.g., `"image"` from `"image/jpeg"`)

## Chaining Methods

Extension methods return typed values that support further chaining:

```js
// String chaining
{{ $json.email.extractDomain().toTitleCase() }}

// Array chaining
{{ $json.items.pluck("price").sum() }}

// DateTime chaining
{{ $now.minus({days: 7}).startOf("day").toISO() }}

// Mixed type chaining
{{ $json.timestamp.toDateTime().format("yyyy-MM-dd") }}
```

NEVER chain methods without understanding the return type — check [references/methods.md](references/methods.md) for return types.

## Reference Links

- [Complete Method Tables](references/methods.md) — All methods with full signatures, parameters, and return types
- [Practical Examples](references/examples.md) — Real-world patterns combining multiple methods
- [Anti-Patterns](references/anti-patterns.md) — Common mistakes and how to avoid them
- [n8n Expression Reference](https://docs.n8n.io/code/expressions/) — Official documentation
- [Luxon DateTime](https://moment.github.io/luxon/) — Underlying DateTime library
