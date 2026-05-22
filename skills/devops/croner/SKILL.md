---
name: croner
description: Cron expression parsing and scheduling
---

# croner

A fully-featured, lightweight Rust library for parsing and evaluating cron patterns. Used in script-kit-gpui for scheduled script execution.

## Key Types

### `Cron`

The main struct for working with cron expressions. Parse from string and query for occurrences.

```rust
use croner::Cron;
use std::str::FromStr;
use chrono::Utc;

// Parse cron expression
let cron = Cron::from_str("0 9 * * *")?;  // Every day at 9 AM

// Access the pattern
let pattern_str = cron.pattern.to_string();
```

### `CronPattern`

Accessible via `cron.pattern`, contains the parsed representation of each field.

### `CronError`

Error type returned when parsing fails or time operations fail.

### `CronIterator`

Iterator for traversing scheduled times forward or backward.

## Usage in script-kit-gpui

Scripts can specify schedules using metadata comments:

```typescript
// Cron: */5 * * * *
// Raw cron pattern - runs every 5 minutes

// Schedule: every tuesday at 2pm
// Natural language - converted to cron via english-to-cron
```

The `Scheduler` in `src/scheduler.rs` manages script execution:

```rust
use croner::Cron;
use std::str::FromStr;
use chrono::Utc;

// Parse and validate cron expression
pub fn parse_cron(expr: &str) -> Result<Cron> {
    Cron::from_str(expr)
        .map_err(|e| anyhow::anyhow!("Invalid cron expression '{}': {}", expr, e))
}

// Find next scheduled run time
fn find_next_occurrence(cron: &Cron, after: &DateTime<Utc>) -> Result<DateTime<Utc>> {
    cron.find_next_occurrence(after, false)  // false = exclusive (not including current time)
        .map_err(|e| anyhow::anyhow!("Failed to find next occurrence: {:?}", e))
}
```

## Cron Syntax

Standard 5-field cron (optional 6th field for seconds):

```
// Standard 5-field (minute precision)
// ┌────────────── minute (0 - 59)
// │ ┌──────────── hour (0 - 23)
// │ │ ┌────────── day of month (1 - 31)
// │ │ │ ┌──────── month (1 - 12, JAN-DEC)
// │ │ │ │ ┌────── day of week (0 - 6, SUN-SAT, 7 = SUN)
// │ │ │ │ │
// * * * * *

// Optional 6-field (second precision)
// ┌──────────────── second (0 - 59)
// │ ┌────────────── minute (0 - 59)
// │ │ ┌──────────── hour (0 - 23)
// │ │ │ ┌────────── day of month (1 - 31)
// │ │ │ │ ┌──────── month (1 - 12)
// │ │ │ │ │ ┌────── day of week (0 - 6)
// │ │ │ │ │ │
// * * * * * *
```

### Special Characters

| Char | Meaning | Example |
|------|---------|---------|
| `*` | Any value | `* * * * *` (every minute) |
| `,` | List of values | `1,15 * * * *` (minute 1 and 15) |
| `-` | Range | `0 9-17 * * *` (9am to 5pm hourly) |
| `/` | Step values | `*/5 * * * *` (every 5 minutes) |
| `?` | No specific value | `0 0 ? * MON` (any day of month) |
| `L` | Last | `0 0 L * *` (last day of month) |
| `W` | Weekday | `0 0 15W * *` (nearest weekday to 15th) |
| `#` | Nth weekday | `0 0 * * 1#2` (2nd Monday) |

### Common Patterns

```rust
// Every minute
"* * * * *"

// Every 5 minutes
"*/5 * * * *"

// Every hour at minute 0
"0 * * * *"

// Every day at 9:00 AM
"0 9 * * *"

// Every Monday at 2:30 PM
"30 14 * * 1"

// Every weekday at 9 AM
"0 9 * * 1-5"

// First day of month at midnight
"0 0 1 * *"

// Every 15 minutes during business hours
"*/15 9-17 * * 1-5"
```

## Next Occurrence

Finding when a cron pattern will next match:

```rust
use croner::Cron;
use chrono::Utc;
use std::str::FromStr;

let cron = Cron::from_str("0 9 * * *")?;
let now = Utc::now();

// Next occurrence after now (exclusive)
let next = cron.find_next_occurrence(&now, false)?;

// Next occurrence including now if it matches (inclusive)
let next_inclusive = cron.find_next_occurrence(&now, true)?;

// Previous occurrence before now
let previous = cron.find_previous_occurrence(&now, false)?;

// Check if current time matches pattern
let matches = cron.is_time_matching(&now)?;
```

### Iterating Occurrences

```rust
use croner::{Cron, Direction};
use chrono::Utc;

let cron = Cron::from_str("0 * * * *")?;
let now = Utc::now();

// Get next 5 occurrences
let upcoming: Vec<_> = cron.iter_after(now)
    .take(5)
    .collect();

// Get previous 5 occurrences
let past: Vec<_> = cron.iter_before(now)
    .take(5)
    .collect();

// Iterate with direction
let iter = cron.iter_from(now, Direction::Forward);
```

## Human-Readable Descriptions

Generate English descriptions of cron patterns:

```rust
let cron = Cron::from_str("0 12 * * MON-FRI")?;
let description = cron.describe();
// "At on minute 0, at hour 12, on Monday,Tuesday,Wednesday,Thursday,Friday."
```

## english-to-cron

Convert natural language schedules to cron expressions (via separate crate):

```rust
use english_to_cron::str_cron_syntax;

// Basic conversions
str_cron_syntax("every minute")?         // "* * * * *"
str_cron_syntax("every hour")?           // "0 * * * *"
str_cron_syntax("every day at 9am")?     // "0 9 * * *"
str_cron_syntax("every tuesday at 2pm")? // "0 14 * * 2"
str_cron_syntax("every weekday at 8am")? // "0 8 * * 1-5"
```

In script-kit-gpui:

```rust
pub fn natural_to_cron(text: &str) -> Result<String> {
    english_to_cron::str_cron_syntax(text)
        .map_err(|e| anyhow::anyhow!("Failed to convert '{}' to cron: {:?}", text, e))
}
```

## Anti-patterns

### Don't forget error handling

```rust
// BAD: Panics on invalid pattern
let cron = Cron::from_str("invalid").unwrap();

// GOOD: Handle parse errors
let cron = Cron::from_str(expr)
    .map_err(|e| anyhow::anyhow!("Invalid cron: {}", e))?;
```

### Don't use inclusive=true unless needed

```rust
// BAD: May match the current second, causing immediate double-trigger
let next = cron.find_next_occurrence(&now, true)?;

// GOOD: Exclusive search for scheduling
let next = cron.find_next_occurrence(&now, false)?;
```

### Don't ignore timezone considerations

```rust
// BAD: Assuming UTC when user expects local time
let now = Utc::now();
let next = cron.find_next_occurrence(&now, false)?;

// GOOD: Be explicit about timezone handling
// croner uses chrono's DateTime<Tz> which is timezone-aware
// Document whether schedules are UTC or local
```

### Don't parse inside tight loops

```rust
// BAD: Parsing every iteration
for _ in 0..100 {
    let cron = Cron::from_str("*/5 * * * *")?;
    let next = cron.find_next_occurrence(&now, false)?;
}

// GOOD: Parse once, reuse
let cron = Cron::from_str("*/5 * * * *")?;
for _ in 0..100 {
    let next = cron.find_next_occurrence(&now, false)?;
}
```

### Don't mix up field order

```rust
// BAD: Confusing minute and hour (runs at 9:00, not 0:09)
"0 9 * * *"  // This is 9:00 AM, not 12:09 AM

// GOOD: Use comments to clarify intent
"0 9 * * *"  // minute=0, hour=9 -> 9:00 AM daily
```

### Don't forget to validate natural language conversion

```rust
// BAD: Assuming conversion always succeeds
let cron_expr = english_to_cron::str_cron_syntax(user_input)?;

// GOOD: Validate the result and provide feedback
match english_to_cron::str_cron_syntax(user_input) {
    Ok(expr) => {
        // Also validate the generated expression
        Cron::from_str(&expr)?;
        Ok(expr)
    }
    Err(e) => Err(anyhow::anyhow!(
        "Could not understand schedule '{}': {:?}", user_input, e
    ))
}
```

## Dependencies

In `Cargo.toml`:

```toml
croner = "3.0"             # Parse and validate cron expressions
english-to-cron = "0.1"    # Convert natural language schedules to cron
chrono = "0.4"             # Date/time handling (croner's timezone support)
```

## References

- [croner on docs.rs](https://docs.rs/croner/latest/croner/)
- [croner GitHub](https://github.com/hexagon/croner-rust)
- [english-to-cron on crates.io](https://crates.io/crates/english-to-cron)
- script-kit-gpui: `src/scheduler.rs`
