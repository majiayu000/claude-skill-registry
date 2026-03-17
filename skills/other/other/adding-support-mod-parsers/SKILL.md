---
name: adding-support-mod-parsers
description: Use when adding support mod parsers to convert support skill affix strings to typed SupportMod objects - guides the template-based parsing pattern (project)
---

# Adding Support Mod Parsers

## Overview

Support mod parsers convert raw support skill affix strings (e.g., `"+15% additional damage for the supported skill"`) into typed `SupportMod` objects at runtime. Unlike active/passive skills which use level-scaling factories, support skills parse their affixes directly using templates.

## When to Use

- Adding support for new support skill affix patterns
- Extending support mod parsing to handle new variants

## Project File Locations

| Purpose | File Path |
|---------|-----------|
| Support mod templates | `src/tli/skills/support-mod-templates.ts` |
| Mod type definitions | `src/tli/mod.ts` |
| SupportMod type | `src/tli/core.ts` |
| Template/spec helpers | `src/tli/mod-parser/` |
| Calculation handlers | `src/tli/calcs/offense.ts` |

## Implementation Checklist

### 1. Check if Mod Type Exists

Look in `src/tli/mod.ts` under `ModDefinitions`. If the mod type doesn't exist, add it first (see `adding-mod-parsers` skill).

### 2. Add Template in `support-mod-templates.ts`

Templates use the same DSL as the main mod parser:

```typescript
// In allSupportParsers array
t("{value:dec%} additional damage for the supported skill").output(
  "DmgPct",
  (c) => ({
    value: c.value,
    dmgModType: "global" as const,
    addn: true,
  }),
),
```

**Template capture types:**

| Type | Matches | Example Input → Output |
|------|---------|------------------------|
| `{name:int}` | Unsigned integer | `"5"` → `5` |
| `{name:dec}` | Unsigned decimal | `"21.5"` → `21.5` |
| `{name:int%}` | Unsigned integer percent | `"30%"` → `30` |
| `{name:dec%}` | Unsigned decimal percent | `"96%"` → `96` |
| `{name:+int}` | **Signed** integer (requires `+` or `-`) | `"+5"` → `5`, `"-3"` → `-3` |
| `{name:+dec}` | **Signed** decimal (requires `+` or `-`) | `"+21.5"` → `21.5` |
| `{name:+int%}` | **Signed** integer percent | `"+30%"` → `30`, `"-15%"` → `-15` |
| `{name:+dec%}` | **Signed** decimal percent | `"+96%"` → `96` |

**Signed vs Unsigned Types:**
- Use **unsigned** (`dec%`, `int`) when input does NOT start with `+` or `-` (e.g., `"0.8% additional damage"`)
- Use **signed** (`+dec%`, `+int`) when input STARTS with `+` or `-` (e.g., `"+19.8% additional damage"`)
- Signed types will NOT match unsigned inputs, and vice versa
- **IMPORTANT:** Some support skills have signed inputs, others have unsigned - you may need BOTH templates (see examples below)

**Optional syntax:**
- `[additional]` - Optional literal, sets `c.additional?: true`
- `(effect|damage)` - Alternation (regex-style)
- `\\(` and `\\)` - Escaped parentheses for literal matching

### 3. SupportMod Structure

Each parsed mod is wrapped in `SupportMod`:
```typescript
interface SupportMod {
  mod: Mod;
}
```

The `parseSupportAffix` function handles this wrapping:
```typescript
return mods.map((mod) => ({ mod }));
```

### 4. Multi-Output Parsers

For affixes that produce multiple mods:
```typescript
t("{value:dec%} additional attack and cast speed for the supported skill")
  .outputMany([
    spec("AspdPct", (c) => ({ value: c.value, addn: true })),
    spec("CspdPct", (c) => ({ value: c.value, addn: true })),
  ]),
```

### 5. Add a Test

Add a test case to `src/tli/skills/support-mod-templates.test.ts` using the example input string given to you:

```typescript
test("parse <skill name> <description of what it parses>", () => {
  const result = parseSupportAffixes([
    "<exact input string from the skill data>",
  ]);
  expect(result).toEqual([
    [
      {
        mod: {
          type: "<ModType>",
          // ... expected mod properties
        },
      },
    ],
  ]);
});
```

### 6. Verify

Run tests to ensure parsing works:
```bash
pnpm test
pnpm typecheck
pnpm check
```

## Examples

### Damage Mod with BOTH Signed and Unsigned Variants

Some support skills use `+{value}%` templates (e.g., Increased Area) while others use `{value}%` (e.g., Haunt). You need BOTH templates:

**Inputs:**
- `"+19.8% additional damage for the supported skill"` (Increased Area - signed)
- `"0.8% additional damage for the supported skill"` (Haunt - unsigned)

```typescript
// Signed version (e.g., "+19.8% additional damage...")
t("{value:+dec%} additional damage for the supported skill").output(
  "DmgPct",
  (c) => ({
    value: c.value,
    dmgModType: "global" as const,
    addn: true,
  }),
),
// Unsigned version (e.g., "0.8% additional damage...")
t("{value:dec%} additional damage for the supported skill").output(
  "DmgPct",
  (c) => ({
    value: c.value,
    dmgModType: "global" as const,
    addn: true,
  }),
),
```

### Typed Damage Mod (Signed)
**Input:** `"+20% additional melee damage for the supported skill"`
```typescript
t("{value:+dec%} additional melee damage for the supported skill").output(
  "DmgPct",
  (c) => ({
    value: c.value,
    dmgModType: "melee" as const,
    addn: true,
  }),
),
```

### Attack Speed (Signed - can be negative)
**Input:** `"-15% Attack Speed for the supported skill"` (Steamroll)
```typescript
t("{value:+dec%} attack speed for the supported skill").output(
  "AspdPct",
  (c) => ({
    value: c.value,
    addn: false,
  }),
),
```

Note: `+dec%` matches both `+` and `-` signs.

### Conditional Mod
**Input:** `"The supported skill deals +30% additional damage to cursed enemies"`
```typescript
t("the supported skill deals {value:dec%} additional damage to cursed enemies")
  .output("DmgPct", (c) => ({
    value: c.value,
    dmgModType: "global" as const,
    addn: true,
    cond: "enemy_is_cursed" as const,
  })),
```

### Per-Stackable Mod
**Input:** `"+5% additional damage for the supported skill for every stack of buffs while standing still"`
```typescript
t("{value:dec%} additional damage for the supported skill for every stack of buffs while standing still")
  .output("DmgPct", (c) => ({
    value: c.value,
    dmgModType: "global" as const,
    addn: false,
    per: { stackable: "willpower" as const },
  })),
```

### Mod with No Value
**Input:** `"The supported skill cannot inflict wilt"`
```typescript
t("the supported skill cannot inflict wilt").output("CannotInflictWilt"),
```

### Escaped Parentheses
**Input:** `"Stacks up to 5 time(s)"`
```typescript
t("stacks up to {value:int} time(s)").output("MaxWillpowerStacks", (c) => ({
  value: c.value,
})),
```

Note: Literal `(` and `)` don't need escaping when they don't contain alternations.

### Complex Pattern with Ignored Values
**Input:** `"When the supported skill deals damage over time, it inflicts 10 affliction on the enemy. Effect cooldown: 3 s"`
```typescript
t("when the supported skill deals damage over time, it inflicts {value:int} affliction on the enemy. effect cooldown: {_:int} s")
  .output("AfflictionInflictedPerSec", (c) => ({
    value: c.value,
  })),
```

Use `{_:type}` to capture but ignore values.

### Shadow Quantity (Signed Flat Integer)
**Input:** `"+2 Shadow Quantity for the supported skill"`
```typescript
t("{value:+int} shadow quantity for the supported skill").output(
  "ShadowQuant",
  (c) => ({
    value: c.value,
  }),
),
```

## Template Ordering

**IMPORTANT:** More specific patterns must come before generic ones in `allSupportParsers` array.

```typescript
// Good: specific before generic
t("{value:dec%} additional melee damage for the supported skill").output(...),
t("{value:dec%} additional damage for the supported skill").output(...),

// Bad: generic would match first
t("{value:dec%} additional damage for the supported skill").output(...),
t("{value:dec%} additional melee damage for the supported skill").output(...),  // never matches
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `dec%` for input with `+` prefix | Use `+dec%` for inputs like `"+25% damage"` |
| Using `+dec%` for input without sign | Use `dec%` for inputs like `"0.8% damage"` |
| Only one template when inputs vary | Add BOTH signed and unsigned templates (see examples) |
| Generic template before specific | Move specific templates earlier in array |
| Missing `as const` on string literals | Add `as const` for type narrowing |
| Handler doesn't account for new mod type | Update `offense.ts` to handle new mod types |
| Forgot the wrapper structure | `parseSupportAffix` already wraps in `{ mod }` |

## Data Flow

```
Support skill affix: "+15% additional damage for the supported skill"
    ↓ parseSupportAffixes()
    ↓ normalize (lowercase, trim)
"15% additional damage for the supported skill"
    ↓ template matching (allSupportParsers)
[{ mod: { type: "DmgPct", value: 15, dmgModType: "global", addn: true } }]
    ↓ resolveSelectedSkillSupportMods() in offense.ts
Applied to skill calculations
```

## Difference from Main Mod Parser

| Aspect | Main Mod Parser | Support Mod Parser |
|--------|-----------------|-------------------|
| File | `src/tli/mod-parser/templates.ts` | `src/tli/skills/support-mod-templates.ts` |
| Source | Gear affixes, talents, etc. | Support skill affixes only |
| Output | `Mod[]` | `SupportMod[]` (wrapped in `{ mod }`) |
| Usage | `parseMod()` | `parseSupportAffixes()` |

Both use the same template DSL (`t()`, `spec()`, `outputMany()`).
