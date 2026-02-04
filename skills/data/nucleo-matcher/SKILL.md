---
name: nucleo-matcher
description: High-performance fuzzy matching library for filtering choices in prompts
tags: [fuzzy-search, matching, performance, rust]
---

# nucleo-matcher

nucleo-matcher is a high-performance fuzzy matching library from the Helix editor project. It's 10-100x faster than alternatives like `fuzzy-matcher` (skim) or fzf.

## Why It's Fast

1. **Optimized SIMD operations** - Uses CPU-level optimizations for character comparisons
2. **Reusable scratch memory** - Matcher allocates ~135KB once, then reuses it (no allocations during matching)
3. **Automatic algorithm fallback** - Switches from O(mn) to O(n) greedy matching for large inputs
4. **Prefilter acceleration** - Uses memchr for fast substring scanning before full matching
5. **UTF-32 internal representation** - Avoids repeated UTF-8 decoding overhead

## Key Types

### `Matcher`
The core matching engine. **Expensive to create** (~135KB heap allocation), so reuse it.

```rust
use nucleo_matcher::{Matcher, Config};

// Create once, reuse many times
let mut matcher = Matcher::new(Config::DEFAULT);

// For file paths, use path-optimized config
let mut matcher = Matcher::new(Config::DEFAULT.match_paths());
```

### `Pattern`
Parses query strings and handles multi-word matching. Preferred over calling Matcher directly.

```rust
use nucleo_matcher::pattern::{Pattern, CaseMatching, Normalization};

// Parse with fzf-style syntax (^ for prefix, $ for suffix, etc.)
let pattern = Pattern::parse("foo bar", CaseMatching::Ignore, Normalization::Smart);

// Or without special syntax parsing
let pattern = Pattern::new("foo bar", CaseMatching::Ignore, Normalization::Smart, AtomKind::Fuzzy);
```

### `Utf32Str`
Efficient UTF-32 string wrapper. **Requires a buffer** to avoid allocations.

```rust
use nucleo_matcher::Utf32Str;

let mut buf: Vec<char> = Vec::new();
let haystack = Utf32Str::new("hello world", &mut buf);
```

### `Config`
Controls matcher behavior:
- `normalize: bool` - Normalize latin chars to ASCII (default: true)
- `ignore_case: bool` - Case-insensitive matching (default: true)  
- `prefer_prefix: bool` - Bonus for matches near start (default: false)
- `match_paths()` - Preset for file path matching

### `CaseMatching` (enum)
- `Ignore` - Always case-insensitive (`a == A`)
- `Respect` - Always case-sensitive (`a != A`)
- `Smart` - Case-insensitive if query is all lowercase, else sensitive

### `Normalization` (enum)
- `Smart` - Normalize accented characters intelligently
- `Never` - No normalization

## Usage in script-kit-gpui

The codebase uses a `NucleoCtx` wrapper for optimal performance:

```rust
/// Context for nucleo fuzzy matching that reuses allocations across calls.
pub(crate) struct NucleoCtx {
    pattern: Pattern,
    matcher: Matcher,
    buf: Vec<char>,  // Reused buffer for Utf32Str conversion
}

impl NucleoCtx {
    pub fn new(query: &str) -> Self {
        let pattern = Pattern::parse(
            query,
            CaseMatching::Ignore,
            Normalization::Smart,
        );
        Self {
            pattern,
            matcher: Matcher::new(Config::DEFAULT),
            buf: Vec::with_capacity(64), // Pre-allocate for typical strings
        }
    }

    #[inline]
    pub fn score(&mut self, haystack: &str) -> Option<u32> {
        self.buf.clear();  // Clear buffer, keep capacity
        let utf32 = Utf32Str::new(haystack, &mut self.buf);
        self.pattern.score(utf32, &mut self.matcher)
    }
}
```

### Scoring Flow in Search Functions

```rust
pub fn fuzzy_search_scripts(scripts: &[Arc<Script>], query: &str) -> Vec<ScriptMatch> {
    let query_lower = query.to_lowercase();
    
    // Create context ONCE for all items
    let mut nucleo = NucleoCtx::new(&query_lower);
    
    for script in scripts {
        let mut score = 0i32;
        
        // Fuzzy match using nucleo
        if let Some(nucleo_s) = nucleo.score(&script.name) {
            // Scale score (0-1000+) to match other weights
            score += 50 + (nucleo_s / 20) as i32;
        }
        
        // Also check filename, description, etc.
        if let Some(nucleo_s) = nucleo.score(&filename) {
            score += 35 + (nucleo_s / 30) as i32;
        }
    }
}
```

## Matching Patterns (fzf-style syntax with Pattern::parse)

| Prefix/Suffix | Meaning | Example |
|---------------|---------|---------|
| (none) | Fuzzy match | `bar` matches "foobar" |
| `^` | Prefix match | `^foo` matches "foobar" |
| `$` | Suffix match | `bar$` matches "foobar" |
| `'` | Exact substring | `'bar` matches "foobar" exactly |
| `!` | Inverse match | `!bar` excludes items with "bar" |

Multiple words are AND-ed together:
```rust
// "foo bar" matches items containing BOTH "foo" AND "bar" (in any order)
Pattern::parse("foo bar", CaseMatching::Ignore, Normalization::Smart)
```

## Performance Tips

### DO: Reuse Matcher and Buffer
```rust
// GOOD: Create once, reuse
let mut ctx = NucleoCtx::new(query);
for item in items {
    ctx.score(&item.name);
}
```

### DON'T: Create Matcher Per Item
```rust
// BAD: 135KB allocation per item!
for item in items {
    let mut matcher = Matcher::new(Config::DEFAULT);
    // ...
}
```

### DO: Pre-allocate Buffer with Capacity
```rust
// GOOD: Pre-allocate for typical string sizes
buf: Vec::with_capacity(64)
```

### DO: Clear Buffer, Not Re-allocate
```rust
// GOOD: Keeps allocated memory
self.buf.clear();

// BAD: Re-allocates
self.buf = Vec::new();
```

### DO: Use ASCII Fast-Path When Possible
```rust
// script-kit-gpui combines ASCII fast-path with nucleo fallback
if query_is_ascii && item.name.is_ascii() {
    // Fast byte-level comparison
    if let Some(pos) = find_ignore_ascii_case(&item.name, &query_lower) {
        score += 100;
    }
}
// Then add nucleo fuzzy score
if let Some(nucleo_s) = nucleo.score(&item.name) {
    score += 50 + (nucleo_s / 20) as i32;
}
```

### DO: Use match_paths() for File Paths
```rust
// Applies bonuses appropriate for path separators
let matcher = Matcher::new(Config::DEFAULT.match_paths());
```

## Anti-patterns

### Creating Matcher in Hot Loop
```rust
// WRONG: ~135KB allocation per iteration
for item in items {
    let mut matcher = Matcher::new(Config::DEFAULT);
}
```

### Not Reusing UTF-32 Buffer
```rust
// WRONG: New allocation per call
fn score(haystack: &str, pattern: &Pattern, matcher: &mut Matcher) -> Option<u32> {
    let mut buf = Vec::new();  // Allocates every time!
    let utf32 = Utf32Str::new(haystack, &mut buf);
    pattern.score(utf32, matcher)
}
```

### Using Direct Matcher Methods Instead of Pattern
```rust
// WRONG for most use cases - Pattern handles multi-word, case folding, etc.
matcher.fuzzy_match(haystack, needle)

// RIGHT: Pattern handles complexity
pattern.score(haystack, &mut matcher)
```

### Not Scaling Nucleo Scores
```rust
// WRONG: Raw nucleo scores (0-1000+) don't mix with other scoring weights
score += nucleo_s as i32;

// RIGHT: Scale to match your scoring system
score += 50 + (nucleo_s / 20) as i32;
```

### Blocking UI Thread with Large Lists
```rust
// WRONG: Blocks UI for large lists
let matches = Pattern::parse(query, ...).match_list(huge_list, &mut matcher);

// RIGHT: Use high-level `nucleo` crate for async/threaded matching
// Or batch process in background
```

## Score Ranges

- **0**: No match
- **100-200**: Weak fuzzy match (scattered characters)
- **200-500**: Good fuzzy match (consecutive characters)
- **500-1000+**: Excellent match (prefix/exact substring)

## References

- [docs.rs/nucleo-matcher](https://docs.rs/nucleo-matcher/latest/nucleo_matcher/)
- [GitHub: helix-editor/nucleo](https://github.com/helix-editor/nucleo)
- Local implementation: `src/scripts/search.rs`
