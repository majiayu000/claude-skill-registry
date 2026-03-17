---
name: k-fencore
description: >
  Context for FenCore - the pure logic library for WoW addons. Covers
  utility functions, math helpers, table operations, and environment
  detection. Load this when working with FenCore or needing utility functions.
  Triggers: fencore, utility, math, table, logic, pure functions.
---

# FenCore Library

FenCore is a pure logic library for WoW addons - no UI dependencies, just utility functions.

## Design Philosophy

- **Pure Functions**: No side effects, predictable outputs
- **No UI Dependencies**: Works in any layer of your addon
- **Testable**: All functions can be unit tested without WoW
- **Documented**: Every function has clear input/output contracts

## MCP Tools

| Task | MCP Tool |
|------|----------|
| List All Functions | `fencore.catalog()` |
| Search Functions | `fencore.search(query="clamp")` |
| Get Function Details | `fencore.info(domain="Math", function="Clamp")` |

## Domains

FenCore organizes functions by domain:

| Domain | Purpose | Examples |
|--------|---------|----------|
| **Math** | Numeric operations | `Clamp`, `Round`, `Lerp`, `InRange` |
| **Table** | Table manipulation | `Copy`, `Merge`, `Filter`, `Map` |
| **String** | String utilities | `Split`, `Trim`, `StartsWith`, `Format` |
| **Color** | Color manipulation | `HexToRGB`, `RGBToHex`, `Lighten`, `Darken` |
| **Time** | Time formatting | `FormatDuration`, `FormatTime`, `ParseDuration` |
| **Environment** | WoW detection | `IsRetail`, `IsClassic`, `GetExpansion` |

## Usage Pattern

```lua
local FenCore = LibStub("FenCore")

-- Access by domain
local Math = FenCore.Math
local result = Math.Clamp(value, 0, 100)

-- Or direct access
local clamped = FenCore.Math.Clamp(value, 0, 100)
```

## Common Functions

### Math

```lua
FenCore.Math.Clamp(value, min, max)     -- Constrain value to range
FenCore.Math.Round(value, decimals)      -- Round to decimal places
FenCore.Math.Lerp(a, b, t)              -- Linear interpolation
FenCore.Math.InRange(value, min, max)   -- Check if value in range
```

### Table

```lua
FenCore.Table.Copy(tbl)                 -- Shallow copy
FenCore.Table.DeepCopy(tbl)             -- Deep copy
FenCore.Table.Merge(base, override)     -- Merge tables
FenCore.Table.Filter(tbl, predicate)    -- Filter by function
FenCore.Table.Map(tbl, transform)       -- Transform values
```

### Environment

```lua
FenCore.Environment.IsRetail()          -- true if retail client
FenCore.Environment.IsClassic()         -- true if classic client
FenCore.Environment.GetExpansion()      -- "TWW", "Classic", etc.
FenCore.Environment.GetBuildInfo()      -- version, build, date
```

## Best Practices

1. **Use for Core layer** - FenCore belongs in your addon's pure logic layer
2. **Don't wrap unnecessarily** - Call FenCore directly, don't create wrappers
3. **Check domain first** - Use `fencore.search` to find existing functions before writing your own
4. **Prefer pure functions** - If you need state, that belongs in Bridge layer
