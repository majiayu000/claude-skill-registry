---
name: afferent-reactive-universe-levels
description: |
  Fix universe level mismatch errors when defining Lean 4 structures containing Reactive.Event
  or Reactive.Dynamic types in Afferent/Canopy widgets. Use when: (1) compiler error "Type 1
  of sort Type 2 but expected Type of sort Type 1", (2) WidgetM won't accept your result
  structure, (3) structure contains Reactive.Event Spider or Reactive.Dynamic Spider fields.
  The fix is to place `open Reactive Reactive.Host` BEFORE structure definitions.
author: Claude Code
version: 1.0.0
date: 2026-01-24
---

# Afferent Reactive Universe Levels

## Problem
When creating Canopy widgets that return structures containing `Reactive.Event Spider α` or
`Reactive.Dynamic Spider α` fields, the compiler reports universe level mismatches like:

```
Application type mismatch: The argument MyResult has type Type 1 of sort Type 2
but is expected to have type Type of sort Type 1 in the application WidgetM MyResult
```

## Context / Trigger Conditions
- Defining a new Canopy widget in `Afferent/Canopy/Widget/`
- Widget returns a result structure containing `Reactive.Event` or `Reactive.Dynamic`
- Error occurs at function signature like `def myWidget (...) : WidgetM MyResult`
- Identical pattern works in other widget files (e.g., ListBox.lean)

## Solution

The `open` statements must appear BEFORE any structure definitions that use reactive types.

**Broken pattern:**
```lean
namespace Afferent.Canopy

open Afferent.Arbor hiding Event

/-- This structure ends up in Type 1 -/
structure MyResult where
  onClick : Reactive.Event Spider Unit

/-! ## Reactive Section -/
open Reactive Reactive.Host  -- Too late!
open Afferent.Canopy.Reactive

def myWidget : WidgetM MyResult := ...  -- Error: Type 1 vs Type
```

**Fixed pattern:**
```lean
namespace Afferent.Canopy

open Afferent.Arbor hiding Event
open Reactive Reactive.Host           -- Before structure!
open Afferent.Canopy.Reactive

/-- Now correctly in Type 0 -/
structure MyResult where
  onClick : Reactive.Event Spider Unit

def myWidget : WidgetM MyResult := ...  -- Works
```

## Verification
After reordering, rebuild with `./build.sh`. The universe error should disappear and
the widget should compile successfully.

## Example
From Toolbar.lean - the working structure:

```lean
namespace Afferent.Canopy

open Afferent.Arbor hiding Event
open Reactive Reactive.Host
open Afferent.Canopy.Reactive

structure ToolbarResult where
  onAction : Reactive.Event Spider String

def toolbar (actions : Array ToolbarAction) (theme : Theme)
    (variant : ToolbarVariant := .filled) : WidgetM ToolbarResult := do
  ...
```

## Notes
- This affects the `Spider` timeline type resolution
- The `hiding Event` on `Afferent.Arbor` is necessary because Arbor has its own Event type
- Compare with working files like `ListBox.lean` or `Dropdown.lean` which have opens at the top
- Pure WidgetBuilder functions (not WidgetM) don't have this issue since they don't return reactive types

## References
- Afferent/Canopy/Widget/Data/ListBox.lean - working example pattern
- Afferent/Canopy/Widget/Input/Dropdown.lean - working example pattern
