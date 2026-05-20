---
name: add-hero-trait
description: Use when adding hero trait mod implementations in hero-trait-mods.ts - guides reading trait descriptions, creating mod factories, adding stackables/config, and wiring up the calculation engine (project)
---

# Adding Hero Trait Mods

## Overview

Hero traits are implemented as mod factories in `src/tli/hero/hero-trait-mods.ts`. Each factory takes a level index (0-4) and returns an array of `Mod` objects. The trait's description in `src/data/hero-trait/hero-traits.ts` is the source of truth for what mods and values to produce.

## When to Use

- Implementing a hero trait that isn't yet in `heroTraitModFactories`
- Adding calculation support for a hero trait's mechanics

## Step 0: Read the Trait Description

**Always start here.** Look up the trait in `src/data/hero-trait/hero-traits.ts` and read its `affix` field. This determines:

- What mods to create and their types
- The per-level values (formatted as `(v1/v2/v3/v4/v5)` for levels 1-5)
- Whether it's a player buff or enemy debuff ("damage taken by the enemy" = `isEnemyDebuff: true`)
- Whether it stacks and the max stack count
- Any conditions for activation

## Project File Locations

| Purpose | File Path |
|---------|-----------|
| Trait descriptions (source of truth) | `src/data/hero-trait/hero-traits.ts` |
| Trait mod factories | `src/tli/hero/hero-trait-mods.ts` |
| Mod type definitions | `src/tli/mod.ts` |
| Stackable types | `src/tli/mod.ts` (`StackableValues`) |
| Condition types | `src/tli/mod.ts` (`ConditionValues`) |
| Configuration interface & defaults | `src/tli/core.ts` |
| Configuration schema | `src/lib/schemas/config.schema.ts` |
| Configuration UI | `src/components/configuration/ConfigurationTab.tsx` |
| Calculation engine | `src/tli/calcs/offense.ts` |

## Implementation Checklist

### 1. Add Mod Factory (`src/tli/hero/hero-trait-mods.ts`)

Add an entry to `heroTraitModFactories`. The key must match the trait's `name` field in `hero-traits.ts` exactly (it's typed as `HeroTraitName`).

**Constant mods (no level scaling):**
```typescript
"Trait Name": () => [
  { type: "SomeFlag" },
  { type: "DmgPct", value: 20, dmgModType: "cold", addn: true, cond: "some_condition" },
],
```

**Level-scaled mods:**
```typescript
"Trait Name": (i) => [
  { type: "FrostbiteEffPct", value: [65, 90, 110, 130, 150][i] },
],
```

**Stackable mods (per-stack scaling):**
```typescript
"Trait Name": (i) => [
  {
    type: "DmgPct",
    value: [8, 10, 12, 15, 18][i],
    dmgModType: "cold",
    addn: true,
    isEnemyDebuff: true,
    per: { stackable: "dance_of_frost", limit: 4 },
  },
],
```

Place the factory near other traits for the same hero, using the comment format:
```typescript
// Frostfire Gemma: Frostbitten Heart (#2)
```

### 2. Add New Mod Types (if needed, `src/tli/mod.ts`)

If the trait needs a mod type not in `ModDefinitions`, add it:

```typescript
interface ModDefinitions {
  // ... existing types ...
  NewModType: { value: number };  // or object for flag mods
}
```

### 3. Add New Stackable (if needed, `src/tli/mod.ts`)

If the trait has a per-stack mechanic, add a stackable to `StackableValues`:

```typescript
const StackableValues = [
  // ... existing values ...
  // hero-specific
  "stalker",
  "twisted_spacetime",
  "dance_of_frost",       // Add near other hero-specific stackables
  // ...
] as const;
```

### 4. Add New Condition (if needed, `src/tli/mod.ts`)

If the trait has a conditional activation, add to `ConditionValues`:

```typescript
const ConditionValues = [
  // ... existing values ...
  "frostbitten_heart_is_active",
  "new_condition_name",           // Add here
] as const;
```

Then wire it up in `filterModsByCond` in `src/tli/calcs/offense.ts` (the `.with()` chain).

### 5. Add Configuration Field (if needed)

If the trait introduces a user-configurable value (stack count, toggle, etc.), use the `/add-configuration` skill or follow these steps:

**a. Add to `Configuration` interface (`src/tli/core.ts`):**
```typescript
// hero-specific config section
// default to 0
danceOfFrostStacks?: number;
```

**b. Add default to `DEFAULT_CONFIGURATION` (`src/tli/core.ts`):**
```typescript
danceOfFrostStacks: undefined,
```

**c. Add schema field (`src/lib/schemas/config.schema.ts`):**
```typescript
danceOfFrostStacks: z.number().optional().catch(d.danceOfFrostStacks),
```

**d. Add UI control (`src/components/configuration/ConfigurationTab.tsx`):**
```tsx
<label className="text-right text-zinc-50">
  Dance of Frost Stacks
  <InfoTooltip text="Frostfire Gemma: Dance of Frost trait stacks" />
</label>
<NumberInput
  value={config.danceOfFrostStacks}
  onChange={(v) => onUpdate({ danceOfFrostStacks: v })}
  min={0}
/>
```

Place near other hero-specific config fields (after `frostbittenHeartIsActive`).

### 6. Wire Up in Calculation Engine (`src/tli/calcs/offense.ts`)

**For stackables:** Add a `normalize()` call in `resolveModsForOffenseSkill`:
```typescript
normalize("dance_of_frost", config.danceOfFrostStacks ?? 0);
```

Place near other hero-specific normalizations (near `pushErika1`, `pushYouga2`, etc.).

**For conditions:** Add a `.with()` case in `filterModsByCond`:
```typescript
.with("new_condition_name", () => config.newConditionField)
```

### 7. Verify

```bash
pnpm typecheck
pnpm test
pnpm check
```

## Common Trait Patterns

| Pattern | Example Trait | Implementation |
|---------|--------------|----------------|
| Simple constant buff | Frostbitten Heart | `() => [{ type: "DmgPct", ... }]` |
| Level-scaled value | Deepfreeze | `(i) => [{ ..., value: [v1,v2,v3,v4,v5][i] }]` |
| Per-stack with config | Dance of Frost | `per: { stackable: "x", limit: N }` + config + normalize |
| Conditional activation | Frostbitten Heart | `cond: "condition_name"` + config boolean |
| Flag mod (enables mechanic) | Wind Stalker | `{ type: "WindStalker" }` (object mod) |
| Override limit | Deepfreeze | `{ type: "MaxFrostbiteRatingLimitOverride", value: X }` |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Not reading the trait description first | Always check `src/data/hero-trait/hero-traits.ts` for the `affix` field |
| Guessing values instead of reading description | Values come from the `(v1/v2/v3/v4/v5)` format in the affix |
| Missing `isEnemyDebuff: true` | "damage taken by the enemy" = enemy debuff, not player buff |
| Forgetting `limit` on per-stackable | "stacks up to N times" needs `limit: N` |
| Not adding `normalize()` for new stackables | Per-stackable mods won't resolve without `normalize()` in offense.ts |
| Placing config UI in wrong section | Hero-specific config goes near other hero fields |
| Trait name doesn't match data | Key must exactly match `name` in `hero-traits.ts` (typed as `HeroTraitName`) |
