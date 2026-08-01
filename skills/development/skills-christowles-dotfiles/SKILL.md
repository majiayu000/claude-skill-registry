---
name: skills-christowles-dotfiles
description: This skill helps generate Last Epoch stash search filters and lookup
  items.
---

# Last Epoch Item Filter Generator

This skill helps generate Last Epoch stash search filters and lookup items.

## Two Filter Systems

### 1. In-Game Loot Filter (Official)
- GUI-based, accessed via `Shift+F`
- Visual rule builder (no code/regex)
- Conditions: affixes, tiers, LP, rarity, class, level
- 75 rules max, top-to-bottom priority

### 2. Stash Search Syntax (This Guide)
**Community-developed regex-like DSL** for searching stash/databases.
Used by Maxroll, lastepochtools.com, and checkmatez.github.io/eternity

**Not official documentation** - community convention.

## Stash Search Operators

### Core Syntax
- `/pattern/` - regex text match
- `&` - AND operator (outside regex)
- `|` - OR operator (inside regex patterns)

### Affix Modifiers
- `2T7` - exactly two T7 affixes
- `2T6+` - two or more T6+ affixes
- `3T5-` - three or fewer T5 affixes
- `sealed0` - no sealed affixes
- `FP0` / `FP1+` - forging potential
- `prefixes1-` - max 1 prefix
- `suffixes1-` - max 1 suffix

### Item Modifiers
- `LP1+` - legendary potential 1 or higher
- `LP2-` - LP 2 or lower
- `exalted` - rarity filter
- `unique` - unique items

## Range Patterns

Use regex ranges for numeric values:
- `[2-3][0-9]` = 20-39
- `1[5-9]` = 15-19
- `[4-9]` = 4-9

## Complex Boolean Logic (A AND (B OR C))

Use `|` inside regex patterns for OR logic:

```
# Boots with 25-30% movement speed
FP1+&/boots/&/2[5-9]% increased movement|3[0]% increased movement/

# Pattern breakdown:
# A = FP1+&/boots/
# (B OR C) = /2[5-9]% increased movement|3[0]% increased movement/
```

**Key rules:**
- `&` joins conditions (AND)
- `|` inside `/pattern/` creates alternation (OR)
- No parentheses grouping support
- Must repeat full pattern on each side of `|` including `%` and text

## Common Filter Templates

### Unique Items
```
/item name/&/[min-max]% stat/&LP1+
```

### Exalted Craft Bases
```
/base type/&2T6+&sealed0&exalted
```

### Slam Targets (2LP)
```
2T6+&sealed0&exalted&/desired affix/&/base type/
```

## Item Databases

### Maxroll
- Database: https://maxroll.gg/last-epoch/database
- Build planner: https://maxroll.gg/last-epoch/planner/
- Unique farming guide: https://maxroll.gg/last-epoch/resources/unique-and-set-item-farming

### Last Epoch Tools
- Database: https://lastepochtools.com/db/
- Superior tracking of unique chances, LP, and affixes

## Syntax Origins

This DSL is **community-developed**, not official EHG documentation.

**History:**
- Patch 1.2.3: Added regex to in-game stash search
- Community tools extended this to create unified search syntax
- Conventions spread via Maxroll filters, forums, and tools

**Key Tools:**
- https://checkmatez.github.io/eternity/search/ - Filter builder
  - It's got some bugs but good for learning syntax
  - doesn't correctly generate some complex filters like percent greater than 25% logic
-
- lastepochtools.com - Database with search
- Maxroll filters - Popular presets

## Workflow

1. Identify item and key stats
2. Find stat ranges from databases or in-game
3. Create stash search with regex ranges for thresholds
4. Add LP/tier requirements
5. Use in stash search or community tools

## Examples

See `/home/ctowles/code/p/dotfiles/docs/apps/last-epoch.md` for comprehensive examples.
