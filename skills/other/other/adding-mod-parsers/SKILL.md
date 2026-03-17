---
name: adding-mod-parsers
description: Use when adding new mod parsers to convert game mod strings to typed Mod objects - guides the template-based parsing pattern (project)
---

# Adding Mod Parsers

## Overview

The mod parser converts raw mod strings (e.g., `"+10% all stats"`) into typed `Mod` objects used by the calculation engine. It uses a **template-based** system for pattern matching.

## When to Use

- Adding support for new mod string patterns
- Extending existing mod types to handle new variants
- Adding new mod types to the engine

## Project File Locations

| Purpose | File Path |
|---------|-----------|
| Mod type definitions | `src/tli/mod.ts` |
| Parser templates | `src/tli/mod-parser/templates.ts` |
| Enum registrations | `src/tli/mod-parser/enums.ts` |
| Calculation handlers | `src/tli/calcs/offense.ts` |
| Tests | `src/tli/mod-parser.test.ts` |

## Implementation Checklist

### 1. Check if Mod Type Exists

Look in `src/tli/mod.ts` under `ModDefinitions`. If the mod type doesn't exist, add it:

```typescript
interface ModDefinitions {
  // ... existing types ...
  NewModType: { value: number; someField: string };
}
```

### 2. Add Template in `templates.ts`

Templates use a DSL for pattern matching. **Do not add comments to templates.ts** - the template string itself is self-documenting.

```typescript
t("{value:dec%} all stats").output("StatPct", (c) => ({
  value: c.value,
  statModType: "all" as const,
})),
t("{value:dec%} {statModType:StatWord}")
  .enum("StatWord", StatWordMapping)
  .output("StatPct", (c) => ({ value: c.value, statModType: c.statModType })),
t("{value:dec%} [additional] [{modType:DmgModType}] damage").output("DmgPct", (c) => ({
  value: c.value,
  dmgModType: c.modType ?? "global",
  addn: c.additional !== undefined,
})),
t("{value:dec%} attack and cast speed").outputMany([
  spec("AspdPct", (c) => ({ value: c.value, addn: false })),
  spec("CspdPct", (c) => ({ value: c.value, addn: false })),
]),
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
| `{name:?int}` | **Optional-sign** integer (matches with or without `+`/`-`) | `"5"` → `5`, `"+5"` → `5`, `"-3"` → `-3` |
| `{name:?dec}` | **Optional-sign** decimal | `"21.5"` → `21.5`, `"+21.5"` → `21.5` |
| `{name:?int%}` | **Optional-sign** integer percent | `"30%"` → `30`, `"+30%"` → `30` |
| `{name:?dec%}` | **Optional-sign** decimal percent | `"96%"` → `96`, `"+96%"` → `96` |
| `{name:EnumType}` | Enum lookup | `{dmgType:DmgChunkType}` |

**Signed vs Unsigned vs Optional-sign Types:**
- Use **unsigned** (`dec%`, `int`) when input NEVER has `+` or `-` (e.g., `"8% additional damage applied to Life"`)
- Use **signed** (`+dec%`, `+int`) when input ALWAYS has `+` or `-` (e.g., `"+25% additional damage"`)
- Use **optional-sign** (`?dec%`, `?int`) when input MAY OR MAY NOT have a sign — this avoids needing two separate templates for signed/unsigned variants
- Signed types will NOT match unsigned inputs, and unsigned will NOT match signed inputs
- Prefer `?dec%` over two separate `dec%`/`+dec%` templates when the same mod can appear with or without a sign

**Optional syntax:**
- `[additional]` - Optional literal, sets `c.additional?: true`
- `[{modType:DmgModType}]` - Optional capture, sets `c.modType?: DmgModType`
- `{(effect|damage)}` - Alternation (regex-style)

### 3. Add Enum Mapping (if needed)

If you need custom word → value mapping, add to `enums.ts`:

```typescript
export const StatWordMapping: Record<string, string> = {
  strength: "str",
  dexterity: "dex",
  intelligence: "int",
};

registerEnum("StatWord", ["strength", "dexterity", "intelligence"]);
```

### 4. Add Handler in `offense.ts` (if new mod type)

If you added a new mod type, add handling in `calculateOffense()` or relevant helper:

```typescript
case "NewModType": {
  break;
}
```

For existing mod types with new variants (like adding `statModType: "all"`), update existing handlers to also filter for the new variant:

```typescript
const flat = sumByValue(
  statMods.filter((m) => m.statModType === statType || m.statModType === "all"),
);
```

### 5. Add Tests

Add test cases in `src/tli/mod_parser.test.ts`:

```typescript
test("parse percentage all stats", () => {
  const result = parseMod("+10% all stats");
  expect(result).toEqual([
    {
      type: "StatPct",
      statModType: "all",
      value: 10,
    },
  ]);
});
```

### 6. Verify

```bash
pnpm test src/tli/mod_parser.test.ts
pnpm typecheck
pnpm check
```

## Template Ordering

**IMPORTANT:** More specific patterns must come before generic ones in `allParsers` array.

```typescript
// Good: specific before generic
t("{value:dec%} all stats").output(...),           // Specific
t("{value:dec%} {statModType:StatWord}").output(...), // Generic

// Bad: generic would match first and fail on "all stats"
```

## Examples

### Simple Value Parser (Signed)

**Input:** `"+10% all stats"` (starts with `+`)

```typescript
t("{value:+dec%} all stats").output("StatPct", (c) => ({
  value: c.value,
  statModType: "all" as const,
})),
```

### Simple Value Parser (Unsigned)

**Input:** `"8% additional damage applied to Life"` (no sign)

```typescript
t("{value:dec%} additional damage applied to life").output("DmgPct", (c) => ({
  value: c.value,
  dmgModType: "global" as const,
  addn: true,
})),
```

### Parser with Condition (Signed)

**Input:** `"+40% damage if you have Blocked recently"`

```typescript
t("{value:+dec%} damage if you have blocked recently").output("DmgPct", (c) => ({
  value: c.value,
  dmgModType: "global" as const,
  addn: false,
  cond: "has_blocked_recently" as const,
})),
```

### Parser with Per-Stackable (Signed in "deals" position)

**Input:** `"Deals +1% additional damage to an enemy for every 2 points of Frostbite Rating the enemy has"`

Note: The `+` appears AFTER "deals", so use `{value:+dec%}`:

```typescript
t("deals {value:+dec%} additional damage to an enemy for every {amt:int} points of frostbite rating the enemy has")
  .output("DmgPct", (c) => ({
    value: c.value,
    dmgModType: "global" as const,
    addn: true,
    per: { stackable: "frostbite_rating" as const, amt: c.amt },
  })),
```

### Multi-Output Parser (Signed)

**Input:** `"+6% attack and cast speed"`

```typescript
t("{value:+dec%} [additional] attack and cast speed").outputMany([
  spec("AspdPct", (c) => ({ value: c.value, addn: c.additional !== undefined })),
  spec("CspdPct", (c) => ({ value: c.value, addn: c.additional !== undefined })),
]),
```

### Flat Stat Parser (Signed)

**Input:** `"+166 Max Mana"`

```typescript
t("{value:+dec} max mana").output("MaxMana", (c) => ({ value: c.value })),
```

### Optional-Sign Parser

**Input:** `"12.5% Sealed Mana Compensation for Spirit Magus Skills"` OR `"+12.5% Sealed Mana Compensation for Spirit Magus Skills"`

Use `?dec%` when the same mod string can appear with or without a `+`/`-` sign, avoiding the need for two separate templates:

```typescript
t("{value:?dec%} sealed mana compensation for spirit magus skills").output(
  "SealedManaCompPct",
  (c) => ({ value: c.value, addn: false, skillType: "spirit_magus" as const }),
),
```

### No-Op Parser (Recognized but produces no mods)

**Input:** `"Energy Shield starts to Charge when Blocking"`

Use `outputNone()` when a mod string should be recognized (not flagged as unparsed) but has no effect on calculations:

```typescript
t("energy shield starts to charge when blocking").outputNone(),
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `dec%` for input with `+` prefix | Use `+dec%` for inputs like `"+25% damage"`, or `?dec%` if sign is optional |
| Using `+dec%` for input without sign | Use `dec%` for inputs like `"8% damage applied to life"`, or `?dec%` if sign is optional |
| Two templates for signed/unsigned variants of the same mod | Use `?dec%` to match both in a single template |
| Template doesn't match input case | Templates are matched case-insensitively; input is normalized to lowercase |
| Missing `as const` on string literals | Add `as const` for type narrowing: `statModType: "all" as const` |
| Handler doesn't account for new variant | Update `offense.ts` to handle new values (e.g., `statModType === "all"`) |
| Generic template before specific | Move specific templates earlier in `allParsers` array |

## Data Flow

```
Raw string: "+10% all stats"
    ↓ normalize (lowercase, trim)
"10% all stats"
    ↓ template matching (allParsers)
{ type: "StatPct", value: 10, statModType: "all" }
    ↓ calculateStats() in offense.ts
Applied to str, dex, int calculations
```
