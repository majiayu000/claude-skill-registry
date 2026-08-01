---
name: crop-data
description: 'Crop planning data model and architecture. Use when working with crops.json,
  bed-plan.json, TimelineCrop, or plan data structures for: (1) Understanding entity
  relationships (Crop → PlantingConfig → P'
---

---
name: crop-data
description: Crop planning data model and architecture. Use when working with crops.json, bed-plan.json, TimelineCrop, or plan data structures for: (1) Understanding entity relationships (Crop → PlantingConfig → Planting → Product), (2) Determining which fields are static inputs vs calculated, (3) Identifying which entity a field belongs to (crop, product, planting, or config-level), (4) Planning data migrations or implementing the slim data architecture, (5) Modifying timeline or explorer components that consume crop data. (project)
---

# Crop Data Context

This skill provides essential context for working with the crop planning data model.

## CRITICAL: Data Analysis Caveats

**The extracted analysis files have known gaps:**

| File | Issue |
|------|-------|
| `column-analysis.json` | Misclassifies array formulas as "static" or "mixed" |
| `formula-analysis.json` | Missing ~20+ formulas using SWITCH, complex XLOOKUP |

**Always verify against the actual workbook** using:
```bash
python scripts/inspect-column.py "STH"           # Inspect specific column
python scripts/inspect-column.py --list          # List all columns
python scripts/inspect-column.py "DTM" --sheet "Bed Plan"
```

**Authoritative reference**: `vba/workbook-structure.md` has table schemas extracted directly from Excel.

## Key Timing Formulas (FROM WORKBOOK)

**STH (Seed To Harvest)** - NOT static, despite what analysis files say:
```
SWITCH(Normal Method,
  "DS": Days to Germination + DTM + IF(Days in Cells > 0, 15, 0)
  "TP": DTM + Days in Cells + IF(Days in Cells <= 0, 20, 0)
  "X":  DTM
)
```

**DTM** - Calculated from range:
```
=FLOOR.MATH(AVERAGE(DTM Lower, DTM Upper))
```

**Days in Cells** - Sum of tray stages:
```
=SUM(Tray 1 Days, Tray 2 Days, Tray 3 Days)
```

**Target dates**:
- `Target Sewing Date = LastFrostDate - 5 * Sewing Rel Last Frost`
- `Target Field Date = Target Sewing Date + Days in Cells`
- `Target Harvest Data = Target Sewing Date + STH`
- `Target End of Harvest = Target Harvest Data + Harvest window`

## Entity Model

```
GLOBAL CONSTANTS (farm settings: LastFrostDate, BedLength, LaborRate)
       │
       ▼
CROP (~100 unique) ─────────────────────────────────────────────────┐
│ name, category, deprecated                                        │
│ Same for all configurations of a crop                             │
       │                                                            │
       │ one crop → many configurations                             │
       ▼                                                            │
PLANTING CONFIGURATION (340 total)                                  │
│ structure (Field/Hoop/Greenhouse)                                 │
│ method (DS/TP), season (Sp/Su/Fa/Wi/Ow)                          │
│ product type, DTM, spacing, rows                                  │
│ Identifier: "Arugula - Baby Leaf | Field DS Sp"                  │
       │                                    │                       │
       │ one config → many plantings        │ references            │
       ▼                                    ▼                       │
PLANTING (per-plan instance)          PRODUCT (processing info) ◄──┘
│ bed, bedsCount, startDate           │ Unit, Price, Yield
│ per-planting overrides              │ Wash type, labor times
│ actual vs planned dates (future)    │ Holding period
```

## Data Source Files

| File | Size | Contents | Notes |
|------|------|----------|-------|
| `src/data/crops.json` | 1.7 MB | 340 configs × ~155 fields | Fat export, includes calculated |
| `src/data/bed-plan.json` | 170 KB | ~138 plantings | Current plan assignments |
| `src/data/products.json` | 213 KB | Product processing data | Labor times, packaging |
| `column-analysis.json` | 46 KB | Field classification | **Has gaps - verify!** |
| `formula-analysis.json` | 29 KB | Formula DAG | **Missing array formulas!** |
| `vba/workbook-structure.md` | - | Table schemas | **Authoritative reference** |

## Planting Override Fields

These bed-plan fields modify catalog values per-planting:

| Override Field | Modifies | Purpose |
|----------------|----------|---------|
| `additionalDaysInField` | STH/DTM | Weather, conditions adjustment |
| `additionalDaysOfHarvest` | Harvest window | Extended/shortened season |
| `additionalDaysInCells` | Days in Cells | Greenhouse timing adjustment |

**Computation pattern**:
```typescript
const effectiveDTM = catalog.STH + planting.additionalDaysInField;
const effectiveHarvestWindow = catalog.harvestWindow + planting.additionalDaysOfHarvest;
```

## Timeline Date Computation

The timeline uses these inputs to compute dates:

**From Catalog (crops.json)**:
- `STH` - Total days from seeding to first harvest
- `Harvest window` - Days of harvest period
- `Days in Cells` - Greenhouse time (0 = direct seed)

**From Planting (bed-plan.json)**:
- `fixedFieldStartDate` - The target transplant/direct-seed date
- `additionalDays*` - Per-planting adjustments

**Computed**:
```
startDate = fixedFieldStartDate (the TP/DS date)
harvestStartDate = startDate + (STH - daysInCells) = startDate + DTM
endDate = harvestStartDate + harvestWindow
```

## Finding Things

Run from `crop-api/` directory. Use patterns (not file paths) to locate code:

```bash
# Entity types (new canonical location)
node scripts/ast-query.js "Plan"           # What does Plan contain?
node scripts/ast-query.js "Planting"       # What does Planting contain?
node scripts/ast-query.js "CropConfig"     # What does CropConfig contain?

# Find type definitions
grep -r "^export interface" src/lib/entities/

# Find calculation functions
grep -r "^export function calculate" src/lib

# Find what uses entities
grep -r "from.*entities" src/lib --include="*.ts"

# Find bed length logic
grep -r "lengthFt\|ROW_LENGTHS" src/lib

# Find plan store actions
grep -r "^  [a-z]*:" src/lib/plan-store.ts | head -30
```

## Data Extraction

Re-extract from Excel when workbook changes (run from `crop-api/`):

```bash
python scripts/extract-products.py
```

## Testing & Verification

Run from `crop-api/`:

```bash
npx tsx scripts/test-entities.ts        # Entity validation
npx tsx scripts/test-slim-planting.ts   # Date computation parity
npx tsx scripts/test-catalog-parity.ts  # Catalog lookup parity
npx tsx scripts/test-crop-calculations.ts  # Crop calc vs Excel

# Inspect actual Excel formulas
python scripts/inspect-column.py "STH"
python scripts/inspect-column.py --list
```

## Architecture

**New canonical types** live in `lib/entities/`:
- `Bed` - bed with `lengthFt` (F/J=20, A-E/G-I/U=50, X=80)
- `Planting` - one per planting, references `configId`
- `CropConfig` - planting configuration with calculations
- `Plan` - self-contained: owns `beds`, `cropCatalog`, `plantings`

**Key principle**: Plans own their data. No external references.

```typescript
// What we store
interface Plan {
  beds: Record<string, Bed>;           // Plan's bed layout
  cropCatalog: Record<string, CropConfig>;  // Plan's crop configs
  plantings: Planting[];               // One per planting decision
}

// Computed at render time
const timing = calculateCropTiming(planting, config);
const bedSpan = calculateBedSpan(planting.bedFeet, planting.startBed, plan.beds);
```

See `.claude/plans/state-migration.md` for full migration plan.
