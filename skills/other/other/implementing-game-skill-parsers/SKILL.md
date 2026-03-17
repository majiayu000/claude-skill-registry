---
name: implementing-game-skill-parsers
description: Use when implementing skill data generation from HTML sources for game build planners - guides the parser-factory-generation pattern for extracting level-scaling values for active and passive skills (project)
---

# Implementing Game Skill Parsers

## Overview

Skill data generation follows a **parser-factory-generation** pattern:
1. **Parser** extracts numeric values from HTML/data sources with **named keys**
2. **Factory** defines how to build Mod objects using those named values
3. **Generation script** combines parsed values into `levelValues` output

**Critical:** Parser keys MUST match factory key usage exactly.

**Note:** This skill covers active and passive skills only. For support skills, see the `adding-support-mod-parsers` skill.

## When to Use

- Adding new active or passive skills with level-scaling properties
- Extracting values from game data HTML pages

## Project File Locations

| Purpose | File Path |
|---------|-----------|
| Active factories | `src/tli/skills/active-factories.ts` |
| Passive factories | `src/tli/skills/passive-factories.ts` |
| Factory types & helpers | `src/tli/skills/types.ts` |
| Active parsers | `src/scripts/skills/active-parsers.ts` |
| Passive parsers | `src/scripts/skills/passive-parsers.ts` |
| Parser registry | `src/scripts/skills/index.ts` |
| Generation script | `src/scripts/generate-skill-data.ts` |
| HTML data sources | `.garbage/tlidb/skill/{category}/{Skill_Name}.html` |

**Categories:** `active`, `passive`, `activation_medium`

## Implementation Checklist

### 1. Identify Data Source
- HTML file at `.garbage/tlidb/skill/{category}/{Skill_Name}.html`
- Find Progression /40 table - columns are: level, col0, col1, col2 (Descript)
- **Column indexing:** `values[0]` = first column after level, `values[2]` = Descript
- Input is clean text (HTML already stripped by `buildProgressionTableInput`)

### 2. Define Factory (structure + key names)
```typescript
// In active-factories.ts or passive-factories.ts
import { v } from "./types";

"Ice Bond": (l, vals) => ({
  buffMods: [
    {
      type: "DmgPct",
      value: v(vals.coldDmgPctVsFrostbitten, l),  // Define key name here
      addn: true,
      dmgModType: "cold",
      cond: "enemy_frostbitten",
    },
  ],
}),
```

**Factory return types:**
- **Active skills:** `{ offense?: SkillOffense; mods?: Mod[]; buffMods?: Mod[] }`
- **Passive skills:** `{ mods?: Mod[]; buffMods?: Mod[] }`

**SkillOffense is a structured interface, NOT an array:**
```typescript
interface SkillOffense {
  weaponAtkDmgPct?: { value: number };
  addedDmgEffPct?: { value: number };
  persistentDmg?: { value: number; dmgType: DmgChunkType; duration: number };
  spellDmg?: { value: DmgRange; dmgType: DmgChunkType; castTime: number };
  // Multi-phase attack skills (e.g., Berserking Blade)
  sweepWeaponAtkDmgPct?: { value: number };
  sweepAddedDmgEffPct?: { value: number };
  steepWeaponAtkDmgPct?: { value: number };
  steepAddedDmgEffPct?: { value: number };
}
```

The `v(arr, level)` helper safely accesses `arr[level - 1]` with bounds checking.

**Key naming conventions:**
- Use descriptive camelCase names
- Include context: `dmgPctPerProjectile` not just `dmgPct`

### 3. Create Parser (extract values for those keys)
```typescript
// In active-parsers.ts or passive-parsers.ts
import { findColumn, validateAllLevels } from "./progression-table";
import { template } from "./template-compiler";
import type { SupportLevelParser } from "./types";
import { createConstantLevels } from "./utils";

export const iceBondParser: SupportLevelParser = (input) => {
  const { skillName, progressionTable } = input;

  // Find column by header (uses substring matching)
  const descriptCol = findColumn(progressionTable, "descript", skillName);
  const coldDmgPctVsFrostbitten: Record<number, number> = {};

  // Iterate over column rows (level → text)
  for (const [levelStr, text] of Object.entries(descriptCol.rows)) {
    const level = Number(levelStr);
    // Use template() for pattern matching - cleaner than regex
    const match = template("{value:dec%} additional cold damage").match(
      text,
      skillName,
    );
    coldDmgPctVsFrostbitten[level] = match.value;
  }

  validateAllLevels(coldDmgPctVsFrostbitten, skillName);

  // Return named keys matching factory expectations
  return { coldDmgPctVsFrostbitten };
};
```

**Template syntax for value extraction:**
- `{name:int}` - Integer (e.g., "5" → 5)
- `{name:dec}` - Decimal (e.g., "21.5" → 21.5)
- `{name:dec%}` - Percentage as decimal (e.g., "96%" → 96, NOT 0.96)
- `{name:int%}` - Percentage as integer (e.g., "-30%" → -30)

For constant values (same across all levels): use `createConstantLevels(value)`

### 4. Register Parser
```typescript
// In index.ts
{ skillName: "Ice Bond", categories: ["active"], parser: iceBondParser }
```

### 5. Regenerate & Verify
```bash
pnpm exec tsx src/scripts/generate_skill_data.ts
pnpm test
```

Check generated output for levels 1, 20, 40 against source HTML.

## Example: Complex Skill (Frost Spike)

**Parser** extracts multiple named values:
```typescript
export const frostSpikeParser: SupportLevelParser = (input) => {
  const weaponAtkDmgPct: Record<number, number> = {};
  const addedDmgEffPct: Record<number, number> = {};
  // ... extract from columns ...

  return {
    weaponAtkDmgPct,
    addedDmgEffPct,
    convertPhysicalToColdPct: createConstantLevels(convertValue),
    maxProjectile: createConstantLevels(maxProjValue),
    projectilePerFrostbiteRating: createConstantLevels(projPerRating),
    baseProjectile: createConstantLevels(baseProj),
    dmgPctPerProjectile: createConstantLevels(dmgPerProj),
  };
};
```

**Factory** uses those keys:
```typescript
"Frost Spike": (l, vals) => ({
  offense: {
    weaponAtkDmgPct: { value: v(vals.weaponAtkDmgPct, l) },
    addedDmgEffPct: { value: v(vals.addedDmgEffPct, l) },
  },
  mods: [
    { type: "ConvertDmgPct", value: v(vals.convertPhysicalToColdPct, l), from: "physical", to: "cold" },
    { type: "MaxProjectile", value: v(vals.maxProjectile, l), override: true },
    { type: "Projectile", value: v(vals.projectilePerFrostbiteRating, l), per: { stackable: "frostbite_rating", amt: 35 } },
    { type: "BaseProjectileQuant", value: v(vals.baseProjectile, l) },
    { type: "DmgPct", value: v(vals.dmgPctPerProjectile, l), dmgModType: "global", addn: true, per: { stackable: "projectile" } },
  ],
}),
```

**Generated output:**
```typescript
levelValues: {
  weaponAtkDmgPct: [1.49, 1.51, 1.54, ...],
  addedDmgEffPct: [1.49, 1.51, 1.54, ...],
  convertPhysicalToColdPct: [1, 1, 1, ...],
  maxProjectile: [5, 5, 5, ...],
  projectilePerFrostbiteRating: [1, 1, 1, ...],
  baseProjectile: [2, 2, 2, ...],
  dmgPctPerProjectile: [0.08, 0.08, 0.08, ...],
}
```

## Example: Multi-Phase Attack Skill (Berserking Blade)

For skills with multiple attack phases, use the dedicated offense properties:

```typescript
"Berserking Blade": (l, vals) => ({
  offense: {
    // Sweep phase stats
    sweepWeaponAtkDmgPct: { value: v(vals.sweepWeaponAtkDmgPct, l) },
    sweepAddedDmgEffPct: { value: v(vals.sweepAddedDmgEffPct, l) },
    // Steep strike phase stats
    steepWeaponAtkDmgPct: { value: v(vals.steepWeaponAtkDmgPct, l) },
    steepAddedDmgEffPct: { value: v(vals.steepAddedDmgEffPct, l) },
  },
  mods: [
    {
      type: "SkillAreaPct",
      skillAreaModType: "global" as const,
      value: v(vals.skillAreaBuffPct, l),
      per: { stackable: "berserking_blade_buff" },
    },
    { type: "MaxBerserkingBladeStacks", value: v(vals.maxBerserkingBladeStacks, l) },
    { type: "SteepStrikeChancePct", value: v(vals.steepStrikeChancePct, l) },
  ],
}),
```

## Example: Spell Skill (Chain Lightning)

Spell skills use `spellDmg` with damage range and cast time:

```typescript
"Chain Lightning": (l, vals) => ({
  offense: {
    addedDmgEffPct: { value: v(vals.addedDmgEffPct, l) },
    spellDmg: {
      value: { min: v(vals.spellDmgMin, l), max: v(vals.spellDmgMax, l) },
      dmgType: "lightning",
      castTime: v(vals.castTime, l),
    },
  },
  mods: [{ type: "Jump", value: v(vals.jump, l) }],
}),
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using array for offense | `offense` is a `SkillOffense` object, NOT an array. Use `offense: { weaponAtkDmgPct: { value: ... } }` |
| Using `modType` in DmgPct mods | Use `dmgModType` instead of `modType` |
| Using HTML regex on clean text | Input is already `.text().trim()` - no HTML tags |
| Parser key doesn't match factory key | Keys must match exactly: `vals.dmgPct` needs parser to return `{ dmgPct: ... }` |
| Forgetting parser registration | Add to SKILL_PARSERS array in `index.ts` |
| Missing factory | Must add factory in `*-factories.ts` for mods to be applied at runtime |
| `findColumn` substring collision | "damage" matches "Effectiveness of added damage" first - use exact matching (see below) |
| Missing levels 21-40 | Many skills only have data for levels 1-20; fill 21-40 with level 20 values |

## findColumn Gotcha: Substring Matching

`findColumn` uses template substring matching. If column headers share substrings, you may get the wrong column:

```typescript
// PROBLEM: "damage" is a substring of "Effectiveness of added damage"
// This returns the WRONG column!
const damageCol = findColumn(progressionTable, "damage", skillName);

// SOLUTION: Use exact header matching when there's a collision
const damageCol = progressionTable.find(
  (col) => col.header.toLowerCase() === "damage",
);
if (!damageCol) {
  throw new Error(`${skillName}: no "damage" column found`);
}
```

## Handling Levels 21-40 with Empty Data

Many skills only have progression data for levels 1-20. Fill levels 21-40 with level 20 values:

```typescript
// Extract levels 1-20
for (const [levelStr, text] of Object.entries(someCol.rows)) {
  const level = Number(levelStr);
  if (level <= 20 && text !== "") {
    values[level] = parseValue(text);
  }
}

// Fill levels 21-40 with level 20 value
const level20Value = values[20];
if (level20Value === undefined) {
  throw new Error(`${skillName}: level 20 value missing`);
}
for (let level = 21; level <= 40; level++) {
  values[level] = level20Value;
}
```

## Data Flow

```
HTML Source → buildProgressionTableInput (strips HTML)
           → Parser (extracts values with named keys)
           → Generation Script (converts to levelValues arrays)
           → Output TypeScript file
           ↓
Runtime: Factory + levelValues → Mod objects
```

## Benefits of Named Keys

1. **Self-documenting:** `vals.projectilePerFrostbiteRating` is clearer than `vals[4]`
2. **Order-independent:** Parser and factory don't need to agree on array order
3. **Extensible:** Adding new values doesn't shift existing indices
4. **Type-safe:** TypeScript can catch typos in key names
