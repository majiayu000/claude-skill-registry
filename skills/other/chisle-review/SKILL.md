---
name: chisle-review
description: >
  Review a diff or file through the Chisle lens: flag over-engineering,
  speculative abstractions, reinvented stdlib, and verbose code that a lazier
  approach would shrink. One finding per line, no praise. Use when the user says
  "chisle review", "review this for bloat", or invokes /chisle-review.
---

# Chisle review

Review the diff/file for **what could be deleted or simplified**, not for style nits.

## What to flag

- Abstraction with one implementation (interface/factory/wrapper for a single case)
- Reinvented stdlib (hand-rolled debounce, deep-clone, groupBy, date math)
- New dependency for what a few lines or an installed dep already does
- Config/option that never varies
- Speculative "for later" scaffolding with no current caller
- Verbose code where a native platform feature (CSS, DB constraint, `<input type>`) does it

## What NOT to flag

- Input validation at trust boundaries
- Error handling that prevents data loss
- Security / accessibility code
- Anything the task explicitly required

## Output format

One finding per line. No preamble, no praise.

```
path:line: <what's over-built>. <the lazier replacement>.
```

Example:

```
cache.js:12: ApiCacheManager class for one call site. Replace with lru_cache / a Map.
search.js:40: hand-rolled debounce util. setTimeout+clearTimeout inline is enough.
```

End with a one-line verdict: `N findings. Est. <X> lines removable.`
