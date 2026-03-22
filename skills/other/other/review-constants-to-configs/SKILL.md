---
name: review-constants-to-configs
description: Find hardcoded constants that should be user-configurable via config registry
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Inventory all hardcoded constants and evaluate which should be promoted to the config registry. Use parallelism where possible.

## Tools

| Command | Purpose |
|---------|---------|
| `query_config.ps1` | Browse config registry — sections, groups, existing entries |
| `query_config.ps1 -Usage <key>` | Which files consume a config value |

## Step 1 — Inventory constants NOT in the config registry

Scan all `src/` files (excluding `src/lib/`) for hardcoded constants:
- Named constants at file scope (e.g., `TIMEOUT_MS := 5000`)
- Magic numbers in function bodies that control behavior (timeouts, thresholds, sizes, intervals)
- Hardcoded pixel values, colors, dimensions
- Timer intervals passed to `SetTimer`
- Sleep durations that control timing behavior
- Buffer sizes, retry counts, polling intervals

Cross-reference each against `query_config.ps1` to confirm it's not already in the registry.

**Exclude from inventory:**
- Windows API constants (WM_ messages, GDI flags, DllCall numeric args) — these are protocol, not tunables
- Array indices, loop bounds tied to data structure size
- Boolean flags (`true`/`false`)
- Values in `src/lib/` (third-party)
- Constants that are already config-driven via `cfg.*`

## Step 2 — Evaluate which should become config entries

Not every constant belongs in config. The bar is: **would an end user reasonably want to change this?**

**Promote to config when:**
- The value controls user-visible behavior (timing, appearance, thresholds)
- Different users/environments may need different values (e.g., slow machines need longer timeouts)
- The value was already asked about in issues or feedback
- Changing it requires editing source code today

**Keep as hardcoded constant when:**
- It's an implementation detail users shouldn't need to think about (internal buffer sizes, protocol constants)
- Changing it would likely break things (carefully tuned race condition windows, critical section timeouts)
- It's tightly coupled to other values that would also need to change (better to keep them together in code)
- It only makes sense in the context of the surrounding code (not meaningful as a standalone setting)

**Keep as hardcoded but name it when:**
- It's a magic number in a function body that should be a named constant for readability, but doesn't need to be user-configurable

## Config Registry Requirements

For any constant promoted to config, specify:
- **Section** and **Group** — where it fits in the existing registry organization
- **Key name** — following existing naming conventions (check `query_config.ps1` for patterns)
- **Type** — `int`, `float`, `bool`, `string`, `color`
- **Default** — the current hardcoded value
- **Min/max** — reasonable bounds to prevent broken configs
- **Description** — one-line explanation for the config editor

Use `query_config.ps1` to understand the existing section/group structure before proposing new entries. New entries should fit naturally into existing sections where possible.

## Plan Format

**Section 1 — Full inventory** (all constants found, categorized):

| File | Lines | Constant | Current Value | Category |
|------|-------|----------|--------------|----------|
| `gui_paint.ahk` | 42 | `BORDER_WIDTH` | `2` | Appearance |
| `gui_state.ahk` | 15 | `GRACE_PERIOD_MS` | `150` | Timing |

**Section 2 — Recommended promotions** (constants → config entries):

| Constant | File | Value | Config Key | Section | Type | Min/Max | Why Configurable |
|----------|------|-------|-----------|---------|------|---------|-----------------|
| `GRACE_PERIOD_MS` | `gui_state.ahk:15` | `150` | `GracePeriodMs` | `[Behavior]` | `int` | `50/500` | Users report quick Alt-Tab too sensitive |

**Section 3 — Recommended naming only** (magic number → named constant, not config):

| File | Lines | Current | Proposed Name | Why Not Config |
|------|-------|---------|--------------|---------------|
| `foo.ahk` | 88 | `Sleep(50)` | `POLL_INTERVAL_MS := 50` | Internal polling detail |

Order promotions by user impact: settings users are likely to want first.

Ignore any existing plans — create a fresh one.
