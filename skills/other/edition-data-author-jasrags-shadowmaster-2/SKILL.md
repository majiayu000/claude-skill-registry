---
name: edition-data-author
description: Creates and validates catalog items for edition JSON files including spells, qualities, gear, augmentations, weapons, armor, adept powers, foci, and complex forms. Use when adding new items to core-rulebook.json or sourcebook files, or when validating existing catalog entries.
allowed-tools: Read, Grep, Glob
---

# Edition Data Author

This skill guides the creation of catalog items for Shadowrun edition data files. All items live in `/data/editions/{editionCode}/` JSON files.

## Key Files

- **Type definitions**: `/lib/types/edition.ts`
- **SR5 core data**: `/data/editions/sr5/core-rulebook.json`
- **Rating spec types**: `/lib/types/ratings.ts`
- **Quality types**: `/lib/types/qualities.ts`

## Naming Conventions

All `id`, `category`, and `subcategory` values must use **kebab-case** (lowercase letters, numbers, and hyphens).

**Validation regex:** `/^[a-z0-9]+(-[a-z0-9]+)*$/`

**Run `pnpm verify-naming` to validate all data files.**

### ID Examples

```
combat-sense
ares-predator-v
wired-reflexes
muscle-replacement
control-thoughts
push-the-limit
```

### Category Examples

```
armor-modification    (NOT armorModification)
rfid-tags             (NOT rfidTags)
nervous-system
eyeware
```

### Subcategory Examples

```
throwing-weapons      (NOT throwingWeapons)
heavy-pistols
light-pistol
assault-rifles
```

### Special Rules

For items with ratings, include the base name only (not the rating):

```
wired-reflexes     (NOT wired-reflexes-1, wired-reflexes-2)
```

For items requiring a selection (attribute, skill, limit):

```
improved-physical-attribute  (with requiresAttribute: true)
improved-ability             (with requiresSkill: true)
```

## Common Patterns

### Availability Format

```typescript
availability: number;           // Base availability value (0-20+)
legality?: "restricted" | "forbidden";  // R or F suffix in books
```

### Cost Patterns

```typescript
// Fixed cost
cost: 5000;

// Cost with rating (use ratingSpec)
cost: 1000;
ratingSpec: {
  rating: { hasRating: true, maxRating: 6 },
  costScaling: { perRating: true }
}
```

### Page References

```typescript
page?: number;      // Page number in source book
source?: string;    // "SR5" or book abbreviation
```

---

## Catalog Item Types

### 1. Spells

Location: `modules.magic.payload.spells.{category}[]`

Categories: `combat`, `detection`, `health`, `illusion`, `manipulation`

```typescript
interface SpellCatalogItem {
  id: string; // kebab-case
  name: string; // Display name
  category: "combat" | "detection" | "health" | "illusion" | "manipulation";
  type: "mana" | "physical";
  range: "touch" | "LOS" | "LOS(A)" | "self";
  duration: "instant" | "sustained" | "permanent";
  drain: string; // "F-2", "F", "F+1", etc.
  damage?: string; // For combat spells: "(F-3)P", "(F)S", etc.
  description: string;
  page?: number;
  source?: string;
}
```

Example:

```json
{
  "id": "fireball",
  "name": "Fireball",
  "category": "combat",
  "type": "physical",
  "range": "LOS(A)",
  "duration": "instant",
  "drain": "F",
  "damage": "(F)P",
  "description": "Deals Fire damage in an area."
}
```

### 2. Qualities

Location: `modules.qualities.payload.qualities[]`

```typescript
interface Quality {
  id: string;
  name: string;
  type: "positive" | "negative";
  category: "physical" | "mental" | "social" | "magical" | "mundane" | "metatype";
  cost: number; // Karma cost (positive for positive qualities)
  maxRating?: number; // If quality has levels (1-4 typically)
  costPerRating?: boolean;
  metatypeRestrictions?: string[]; // ["human", "elf"]
  prerequisites?: QualityPrerequisites;
  incompatible?: string[]; // IDs of incompatible qualities
  description: string;
  effects?: QualityEffect[];
  source?: SourceReference;
}
```

Example:

```json
{
  "id": "toughness",
  "name": "Toughness",
  "type": "positive",
  "category": "physical",
  "cost": 9,
  "description": "+1 to Physical damage resistance tests.",
  "effects": [
    {
      "type": "dicePoolModifier",
      "target": "damageResistance",
      "modifier": 1
    }
  ]
}
```

### 3. Cyberware

Location: `modules.cyberware.payload.cyberware[]`

Categories: `headware`, `eyeware`, `earware`, `bodyware`, `cyberlimbs`, `nervous-system`, `biomonitors`

```typescript
interface CyberwareCatalogItem {
  id: string;
  name: string;
  category: CyberwareCategory;
  essenceCost: number; // Base essence cost
  cost: number; // Base nuyen cost
  availability: number;
  legality?: "restricted" | "forbidden";

  // For rated items, use ratingSpec (preferred)
  ratingSpec?: CatalogItemRatingSpec;

  // Or legacy properties (deprecated but still work)
  hasRating?: boolean;
  maxRating?: number;
  essencePerRating?: boolean;
  costPerRating?: boolean;

  // Capacity (for cyberlimbs that hold enhancements)
  capacity?: number; // Capacity this provides
  capacityCost?: number; // Capacity this consumes (for enhancements)

  // Bonuses
  attributeBonuses?: Record<string, number>;
  initiativeDiceBonus?: number;

  // Descriptions
  description?: string;
  wirelessBonus?: string;

  page?: number;
  source?: string;
}
```

Example:

```json
{
  "id": "wired-reflexes",
  "name": "Wired Reflexes",
  "category": "nervous-system",
  "essenceCost": 2,
  "cost": 39000,
  "availability": 8,
  "legality": "restricted",
  "ratingSpec": {
    "rating": { "hasRating": true, "minRating": 1, "maxRating": 3 },
    "essenceScaling": { "perRating": true },
    "costScaling": { "values": [39000, 149000, 217000] }
  },
  "initiativeDiceBonus": 1,
  "description": "Hardwired reflexes for faster reaction time.",
  "wirelessBonus": "+1 Initiative Die while wireless enabled."
}
```

### 4. Bioware

Location: `modules.bioware.payload.bioware[]`

Categories: `standard`, `cultured`, `cosmetic`, `biosculpting`

```typescript
interface BiowareCatalogItem {
  id: string;
  name: string;
  category: BiowareCategory;
  essenceCost: number;
  cost: number;
  availability: number;
  legality?: "restricted" | "forbidden";

  ratingSpec?: CatalogItemRatingSpec;
  hasRating?: boolean;
  maxRating?: number;

  attributeBonuses?: Record<string, number>;
  description?: string;
  wirelessBonus?: string;

  page?: number;
  source?: string;
}
```

### 5. Weapons

Location: `modules.gear.payload.weapons.{subcategory}[]`

Subcategories: `holdout-pistols`, `light-pistols`, `heavy-pistols`, `machine-pistols`, `smgs`, `assault-rifles`, `sniper-rifles`, `shotguns`, `lmgs`, `hmgs`, `assault-cannons`, `blades`, `clubs`, `exotic-weapons`, `throwing-weapons`, `bows`, `crossbows`

```typescript
interface WeaponCatalogItem {
  id: string;
  name: string;
  subcategory: string;
  damage: string; // "5P", "8P(f)", "(STR+2)P"
  accuracy: number;
  ap: number; // Armor Penetration (usually negative)
  mode?: string; // "SA", "SA/BF", "SA/BF/FA"
  rc?: number; // Recoil compensation
  ammo?: string; // "12(c)", "30(c)", "belt"
  cost: number;
  availability: number;
  legality?: "restricted" | "forbidden";
  reach?: number; // For melee weapons
  concealability?: number; // Modifier for concealment
  description?: string;
  page?: number;
  source?: string;
}
```

Example:

```json
{
  "id": "ares-predator-v",
  "name": "Ares Predator V",
  "subcategory": "heavy-pistols",
  "damage": "8P",
  "accuracy": 5,
  "ap": -1,
  "mode": "SA",
  "rc": 0,
  "ammo": "15(c)",
  "cost": 725,
  "availability": 5,
  "legality": "restricted",
  "description": "The iconic sidearm of shadowrunners everywhere."
}
```

### 6. Armor

Location: `modules.gear.payload.armor[]`

```typescript
interface ArmorCatalogItem {
  id: string;
  name: string;
  armorRating: number;
  capacity: number; // For armor modifications
  cost: number;
  availability: number;
  legality?: "restricted" | "forbidden";
  encumbrance?: number; // Modifier to physical tests
  concealability?: number;
  description?: string;
  page?: number;
  source?: string;
}
```

### 7. Weapon Modifications

Location: `modules.modifications.payload.weaponMods[]`

```typescript
interface WeaponModificationCatalogItem {
  id: string;
  name: string;
  mount?: "top" | "under" | "side" | "barrel" | "stock" | "internal";
  occupiedMounts?: WeaponMountType[]; // Additional mounts used
  isBuiltIn?: boolean;
  compatibleWeapons?: string[];
  incompatibleWeapons?: string[];
  minimumWeaponSize?: "holdout" | "light-pistol" | "heavy-pistol" | "smg" | "rifle" | "heavy";

  cost: number;
  costMultiplier?: number;
  availability: number;
  legality?: "restricted" | "forbidden";

  ratingSpec?: CatalogItemRatingSpec;
  hasRating?: boolean;
  maxRating?: number;

  recoilCompensation?: number;
  accuracyModifier?: number;
  concealabilityModifier?: number;

  description?: string;
  wirelessBonus?: string;
  page?: number;
  source?: string;
}
```

### 8. Armor Modifications

Location: `modules.modifications.payload.armorMods[]`

```typescript
interface ArmorModificationCatalogItem {
  id: string;
  name: string;
  capacityCost: number;
  noCapacityCost?: boolean; // If true, doesn't use capacity (bracketed in book)

  ratingSpec?: CatalogItemRatingSpec;
  hasRating?: boolean;
  maxRating?: number;
  capacityPerRating?: boolean;

  cost: number;
  costPerRating?: boolean;
  costMultiplier?: number;
  availability: number;
  availabilityModifier?: number;
  legality?: "restricted" | "forbidden";

  armorBonus?: number;
  requirements?: string[]; // ["full body armor", "helmet"]

  description?: string;
  wirelessBonus?: string;
  page?: number;
  source?: string;
}
```

### 9. Adept Powers

Location: `modules.adeptPowers.payload.powers[]`

```typescript
interface AdeptPowerCatalogItem {
  id: string;
  name: string;
  cost: number | null; // Power point cost (null if table-based)
  costType: "fixed" | "perLevel" | "table";
  maxLevel?: number;
  activation?: "free" | "simple" | "complex" | "interrupt";

  // For powers requiring selection
  requiresAttribute?: boolean;
  validAttributes?: string[];
  requiresSkill?: boolean;
  validSkills?: string[];
  requiresLimit?: boolean;
  validLimits?: string[];

  // For table-based costs (like Improved Reflexes)
  levels?: Array<{
    level: number;
    cost: number;
    bonus: string;
  }>;

  // For powers with variants (like Improved Sense)
  variants?: Array<{
    id: string;
    name: string;
    bonus?: string;
  }>;

  description: string;
  page?: number;
  source?: string;
}
```

### 10. Foci

Location: `modules.foci.payload.foci[]`

```typescript
interface FocusCatalogItem {
  id: string;
  name: string;
  type: "enchanting" | "metamagic" | "power" | "qi" | "spell" | "spirit" | "weapon";
  costMultiplier: number; // Cost = Force × multiplier
  bondingKarmaMultiplier: number; // Karma = Force × multiplier
  availability: number;
  legality?: "restricted" | "forbidden";
  description?: string;
  page?: number;
  source?: string;
}
```

### 11. Complex Forms

Location: `modules.magic.payload.complexForms[]`

```typescript
interface ComplexFormCatalogItem {
  id: string;
  name: string;
  target: "persona" | "device" | "file" | "sprite" | "host" | "self";
  duration: "instant" | "sustained" | "permanent";
  fading: string; // "L+1", "L-1", "L", etc.
  description: string;
  page?: number;
  source?: string;
}
```

---

## Unified Ratings Tables (PREFERRED)

For items with ratings, use **unified ratings tables** - explicit per-rating values that match how source books print data:

```typescript
interface UnifiedRatingConfig {
  hasRating: true; // Must be true to enable ratings
  minRating?: number; // Default: 1
  maxRating: number; // Maximum rating allowed
  ratings: Record<
    number,
    {
      // Explicit values for each rating
      cost?: number; // Nuyen cost at this rating
      availability?: number; // Availability at this rating
      availabilitySuffix?: "R" | "F";
      essenceCost?: number; // Essence cost (cyberware/bioware)
      capacity?: number; // Capacity provided (cyberlimbs, cybereyes)
      capacityCost?: number; // Capacity consumed (enhancements)
      karmaCost?: number; // Karma cost (qualities)
      powerPointCost?: number; // Power point cost (adept powers)
      effects?: {
        // Mechanical effects at this rating
        attributeBonuses?: Record<string, number>;
        initiativeDice?: number;
        initiativeScore?: number;
        limitBonus?: number;
        armorBonus?: number;
      };
    }
  >;
}
```

### Example - Cybereyes (different capacity per rating):

```json
{
  "id": "cybereyes",
  "name": "Cybereyes",
  "category": "eyeware",
  "hasRating": true,
  "minRating": 1,
  "maxRating": 4,
  "ratings": {
    "1": { "cost": 4000, "availability": 3, "essenceCost": 0.2, "capacity": 4 },
    "2": { "cost": 6000, "availability": 6, "essenceCost": 0.3, "capacity": 8 },
    "3": { "cost": 10000, "availability": 9, "essenceCost": 0.4, "capacity": 12 },
    "4": { "cost": 14000, "availability": 12, "essenceCost": 0.5, "capacity": 16 }
  },
  "description": "Replacement eyes with customizable enhancements."
}
```

### Example - Wired Reflexes (non-linear essence/cost):

```json
{
  "id": "wired-reflexes",
  "name": "Wired Reflexes",
  "category": "nervous-system",
  "hasRating": true,
  "minRating": 1,
  "maxRating": 3,
  "ratings": {
    "1": {
      "cost": 39000,
      "availability": 8,
      "essenceCost": 2,
      "effects": { "initiativeDice": 1, "initiativeScore": 1 }
    },
    "2": {
      "cost": 149000,
      "availability": 12,
      "essenceCost": 3,
      "effects": { "initiativeDice": 2, "initiativeScore": 2 }
    },
    "3": {
      "cost": 217000,
      "availability": 20,
      "essenceCost": 5,
      "effects": { "initiativeDice": 3, "initiativeScore": 3 }
    }
  },
  "legality": "restricted",
  "description": "Hardwired reflexes for faster reaction time.",
  "wirelessBonus": "+1 Initiative Die while wireless enabled."
}
```

### Example - Quality with Levels (Toughness):

```json
{
  "id": "toughness",
  "name": "Toughness",
  "type": "positive",
  "category": "physical",
  "hasRating": true,
  "minRating": 1,
  "maxRating": 4,
  "ratings": {
    "1": { "karmaCost": 9 },
    "2": { "karmaCost": 18 },
    "3": { "karmaCost": 27 },
    "4": { "karmaCost": 36 }
  },
  "summary": "+1 to Physical damage resistance tests per level."
}
```

### Why Unified Ratings Tables?

1. **Matches source books** - Books print tables, not formulas
2. **Non-linear scaling** - Many items don't follow simple formulas
3. **Easier to audit** - Direct comparison with source material
4. **Single code path** - No special cases for different scaling types
5. **Complete data** - All rating-dependent values in one place

---

## Rating Spec (LEGACY FALLBACK)

The `ratingSpec` format is still supported for backward compatibility, but **unified ratings tables are preferred** for new data:

```typescript
interface CatalogItemRatingSpec {
  rating: {
    hasRating: boolean;
    minRating?: number; // Default: 1
    maxRating: number;
  };
  essenceScaling?: {
    perRating?: boolean;
    values?: number[]; // Specific essence costs per rating
  };
  costScaling?: {
    perRating?: boolean;
    values?: number[]; // Specific costs per rating
  };
  capacityCostScaling?: {
    perRating?: boolean;
    values?: number[];
  };
  attributeBonusScaling?: Record<string, number>; // Bonus per rating
}
```

Legacy Example - Muscle Replacement (linear scaling):

```json
{
  "ratingSpec": {
    "rating": { "hasRating": true, "maxRating": 4 },
    "essenceScaling": { "perRating": true },
    "costScaling": { "perRating": true },
    "attributeBonusScaling": { "strength": 1, "agility": 1 }
  }
}
```

---

## Validation Checklist

When creating new items, verify:

1. **ID is unique** within its category
2. **ID follows kebab-case** convention
3. **Required fields are present** (id, name, category/type-specific fields)
4. **Availability is reasonable** (typically 0-20, rarely higher)
5. **Costs are positive numbers** in appropriate ranges
6. **Legality is only set when restricted/forbidden** (omit for legal items)
7. **Rating specs are consistent**:
   - For rated items, prefer **unified ratings tables** over `ratingSpec`
   - If `hasRating: true`, must have `maxRating` and `ratings` table
   - Each rating in table should have appropriate cost/availability/essence values
8. **Page references are accurate** (if provided)
9. **Descriptions are concise** but informative
10. **Unified ratings tables match source book** values exactly

---

## Adding to JSON Files

Items are added to arrays within the module payloads:

```json
{
  "modules": {
    "magic": {
      "mergeStrategy": "merge",
      "payload": {
        "spells": {
          "combat": [
            {
              /* spell 1 */
            },
            {
              /* spell 2 */
            }
          ]
        }
      }
    }
  }
}
```

For sourcebooks, use appropriate merge strategy:

- `merge` - Combine with existing data (default)
- `append` - Add to arrays without replacing
- `replace` - Completely override module
