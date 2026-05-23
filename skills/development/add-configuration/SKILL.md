---
name: add-configuration
description: Use when adding new configuration fields to the Configuration interface for combat conditions, buff stacks, or other build parameters used in damage calculations (project)
---

# Adding Configuration Fields

## Overview

Configuration fields control combat conditions, buff stacks, and other build parameters that affect damage calculations. They are persisted in SaveData and editable via the Configuration tab UI.

## When to Use

- Adding a new toggle (boolean) or numeric parameter for damage calculations
- Adding conditional combat states (e.g., "has X recently", "enemy has Y")
- Adding stack counts for buffs/debuffs
- Adding enemy stat overrides

## Project File Locations

| Purpose | File Path |
|---------|-----------|
| Configuration interface & defaults | `src/tli/core.ts` |
| Zod validation schema | `src/lib/schemas/config.schema.ts` |
| Configuration tab UI | `src/components/configuration/ConfigurationTab.tsx` |
| Calculation usage | `src/tli/calcs/offense.ts` (and other calcs files) |

## Implementation Checklist

### 1. Add Field to Configuration Interface (`src/tli/core.ts`)

Add the field to the `Configuration` interface with a default comment:

**Boolean field (default false):**
```typescript
// default to false
newFieldEnabled: boolean;
```

**Required number field (has a sensible non-undefined default):**
```typescript
// default to 1
numThings: number;
```

**Optional number field (undefined means "use calculated default/max"):**
```typescript
// default to max
someStacks?: number;
```

### 2. Add Default Value to `DEFAULT_CONFIGURATION` (`src/tli/core.ts`)

Add the matching default in `DEFAULT_CONFIGURATION`:

```typescript
// Boolean → false, Required number → the default, Optional number → undefined
newFieldEnabled: false,
numThings: 1,
someStacks: undefined,
```

### 3. Add Schema Validation (`src/lib/schemas/config.schema.ts`)

Add to `ConfigurationPageSchema` using the `d` alias for defaults. The pattern depends on the field type:

**Boolean:**
```typescript
newFieldEnabled: z.boolean().catch(d.newFieldEnabled),
```

**Required number:**
```typescript
numThings: z.number().catch(d.numThings),
```

**Optional number:**
```typescript
someStacks: z.number().optional().catch(d.someStacks),
```

The `satisfies z.ZodType<Configuration>` at the end of the schema ensures the schema stays in sync with the interface — a type error will occur if you miss a field or get the type wrong.

### 4. Add UI Controls (`src/components/configuration/ConfigurationTab.tsx`)

The configuration tab uses a 2-column grid: `grid-cols-[auto_auto]` with label on the left, control on the right.

**NumberInput field (required number):**
```tsx
<label className="text-right text-zinc-50">
  Field Label
  <InfoTooltip text="Description of what this does. Defaults to X." />
</label>
<NumberInput
  value={config.numThings}
  onChange={(v) => onUpdate({ numThings: v ?? 1 })}
  min={1}
/>
```

**NumberInput field (optional number, undefined = max/default):**
```tsx
<label className="text-right text-zinc-50">
  Stack Count
  <InfoTooltip text="Defaults to max" />
</label>
<NumberInput
  value={config.someStacks}
  onChange={(v) => onUpdate({ someStacks: v })}
  min={0}
/>
```

**Checkbox field (boolean):**
```tsx
<label className="text-right text-zinc-50">Field Label</label>
<input
  type="checkbox"
  checked={config.newFieldEnabled}
  onChange={(e) => onUpdate({ newFieldEnabled: e.target.checked })}
  className="h-4 w-4 rounded border-zinc-600 bg-zinc-800 accent-amber-500"
/>
```

**Checkbox with conditional child NumberInput (boolean toggle + optional stacks):**
```tsx
<label className="text-right text-zinc-50">Has Effect</label>
<input
  type="checkbox"
  checked={config.hasEffect}
  onChange={(e) => onUpdate({ hasEffect: e.target.checked })}
  className="h-4 w-4 rounded border-zinc-600 bg-zinc-800 accent-amber-500"
/>

{config.hasEffect && (
  <>
    <label className="text-right text-zinc-50">
      Effect Stacks
      <InfoTooltip text="Defaults to max" />
    </label>
    <NumberInput
      value={config.effectStacks}
      onChange={(v) => onUpdate({ effectStacks: v })}
      min={0}
    />
  </>
)}
```

**Conditionally rendered field (only show when loadout has something):**
```tsx
{hasPactspirit("Some Pactspirit", loadout) && (
  <>
    <label className="text-right text-zinc-50">
      Some Stacks
      <InfoTooltip text="Defaults to max" />
    </label>
    <NumberInput
      value={config.someStacks}
      onChange={(v) => onUpdate({ someStacks: v })}
      min={0}
      max={6}
    />
  </>
)}
```

### 5. Use in Calculations (if applicable)

Access the field via the `config` parameter in calculation functions:

```typescript
// In src/tli/calcs/offense.ts or related files
const numActiveTangles = config.numActiveTangles;
```

### 6. Verify

```bash
pnpm typecheck
pnpm check
pnpm test
```

## Field Type Decision Guide

| Scenario | Interface Type | Default | Schema |
|----------|---------------|---------|--------|
| On/off toggle | `boolean` | `false` | `z.boolean().catch(d.x)` |
| Count with known default | `number` | the value | `z.number().catch(d.x)` |
| Count where undefined = "use max" | `number?` | `undefined` | `z.number().optional().catch(d.x)` |
| Override where undefined = "use calculated" | `number?` | `undefined` | `z.number().optional().catch(d.x)` |

## onChange Patterns for NumberInput

- **Required number:** `onChange={(v) => onUpdate({ field: v ?? defaultValue })}` — fallback to default when cleared
- **Optional number:** `onChange={(v) => onUpdate({ field: v })}` — allow undefined (cleared = use default/max)

## Where to Place in the UI

Place new fields in the grid inside `ConfigurationTab` near related fields. General grouping:
- Top: Level, Fervor, Frostbite, hero-specific
- Middle: Player conditions (blessings, mana, movement, aggression)
- Middle: Enemy conditions (resistances, armor, debuffs, ailments)
- Bottom: Buff stacks, skill-specific counts

## Automatic Persistence

No additional work is needed for persistence. The field flows through:
```
Configuration interface → DEFAULT_CONFIGURATION → ConfigurationPageSchema → SaveData → Zustand store → localStorage
```

The store's `updateConfiguration` action handles partial updates via spread, and the schema's `.catch()` ensures old saves without the new field get the default value.
