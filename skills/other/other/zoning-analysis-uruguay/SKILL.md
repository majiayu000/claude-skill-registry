---
name: zoning-analysis-uruguay
description: Analyze zoning envelope rules for lots in Maldonado, Uruguay using GIS data and TONE regulations
allowed-tools:
  - Read
  - Write
  - Edit
  - WebFetch
  - AskUserQuestion
  - Bash
  - Glob
  - Grep
user-invocable: true
---

# /zoning-analysis-uruguay — Zoning Envelope Analysis (Maldonado, Uruguay)

Analyze building envelope rules for one or more lots in Maldonado using GIS data from the ArcGIS cadastral portal and the TONE (Volume V of the Digesto Departamental). When multiple adjoining lots are provided, compares individual, apareada (party wall), and unified (englobamiento) development scenarios.

## Workflow

### Step 1: Parse GIS Input

Accept pasted JSON from the Maldonado ArcGIS cadastral portal. The input is an array — it may contain one or multiple lot features.

**Detect urban vs rural:** Check the attribute keys to determine the parcel type:
- **Urban lots** have: `nomloccat`, `nummancat`, `valaream2`, `tiporegime`
- **Rural lots** have: `areaha`, `areamc`, `seccat` (and lack `nomloccat`)

**If RURAL → immediately flag as non-viable for multi-unit development:**

Rural lots in Maldonado are governed by Resolución 3103/2014 and Decreto 3866/2010, not the urban TONE. The constraints make starter home development impractical:
- **50,000 m²/dwelling** minimum → an 8 ha lot supports only 1-2 houses
- **FOS 5%, FOT 8%** — extremely low density
- **90% must remain natural/unpaved**
- **Only isolated units** — no blocks, no paired, no apartments
- **No subdivision** for housing without soil category transformation (Decreto 3866/2010)
- Soil transformation requires Executive approval and existing luxury dwellings on site

Present this as a short verdict:
```
## Rural Lot — Not Viable for Starter Home Development

| Parameter | Value |
|-----------|-------|
| Padrón | [number] |
| Area | [X] ha ([Y] m²) |
| Sección catastral | [N] |
| Coordinates | lat, lon |

### Why This Doesn't Work
- Min 50,000 m²/dwelling → only [N] unit(s) possible
- FOS 5% / FOT 8% — rural density limits
- 90% must remain natural
- No blocks, paired units, or apartments — isolated viviendas only
- Rural → suburban conversion requires Executive approval (Dto. 3866/2010)

### Path to Viability
Soil category transformation (rural → suburban) under Decreto 3866/2010, but requires:
1. Executive (Intendencia) approval
2. Existing luxury dwellings (Cat. D/E) on site
3. 25m buffer from public domain
4. 15m service roads
5. SRN land is excluded entirely

**Recommendation:** Skip this lot for the starter home program. Focus on urban/suburban parcels where density is permitted by right.
```

Do NOT proceed to Steps 2-7 for rural lots. Do NOT run the pro forma.

**If URBAN → continue with normal workflow:**

Extract key attributes:
- `nomloccat` — locality name (e.g., "LA BARRA")
- `padron` — lot number
- `nummancat` — block (manzana) number
- `valaream2` — lot area in m²
- `tiporegime` — property regime (PC = Propiedad Común, PH = Propiedad Horizontal)
- `geometry.rings` — polygon coordinates in Web Mercator (EPSG:3857)

**Multiple lots:** If the input contains more than one feature, proceed to Step 1b.

### Step 1b: Detect Adjoining Lots (multi-lot input only)

When multiple lots are provided:
1. Check if they share the same `nomloccat` and `nummancat` (same locality and block)
2. Test adjacency by checking if any polygon edges are shared or nearly coincident (within 1m tolerance). Two lots are adjoining if they share a common edge (not just a corner point).
3. Compute the **combined polygon** by merging the rings — remove the shared internal edge to get the outer boundary of the unified parcel.
4. Calculate the combined area (sum of `valaream2` values) and combined dimensions from the merged polygon.
5. Determine the combined frente (front) by measuring the merged polygon's frontage.

If lots are NOT adjoining, analyze each lot independently (run the full workflow per lot).

If lots ARE adjoining, continue with **both** tracks:
- **Individual analysis** — each lot on its own (Steps 2–7)
- **Combined analysis** — the unified parcel (Steps 2–7 using combined area/geometry)
- **Comparison** — side-by-side comparison at the end (Step 7)

### Step 2: Convert Coordinates

Use the geometry rings to calculate approximate lot dimensions:
1. Rings are in Web Mercator (EPSG:3857) — units are meters but distorted by projection
2. For x-axis (east-west): multiply distances by `cos(latitude)` where latitude ≈ -34.8° → cos factor ≈ 0.821
3. For y-axis (north-south): distances are approximately correct
4. Convert first ring to pairs, calculate edge lengths, estimate front × depth
5. Verify calculated area against `valaream2`

To convert EPSG:3857 to lat/lon for reference:
- `lon = x / 20037508.34 × 180`
- `lat = (atan(exp(y / 20037508.34 × π)) × 360 / π) - 90`

### Step 3: Look Up Location

Read `~/.claude/skills/zoning-analysis-uruguay/normativa/location-map.md` to match `nomloccat` to a TONE sector/region.

If no match is found, search the digesto website at `https://digesto.maldonado.gub.uy/` for the location.

### Step 4: Load Normativa

Read the corresponding normativa file from `~/.claude/skills/zoning-analysis-uruguay/normativa/`.

If the file doesn't exist yet:
1. Fetch the relevant articles from the digesto using WebFetch
2. The section index pages are at `https://digesto.maldonado.gub.uy/index.php/armado-seccion/{id}`
3. Individual articles are at `https://digesto.maldonado.gub.uy/index.php/detalle-articulo/{id}`
4. Present the raw content to the user
5. Offer to save it as a new normativa reference file for future use

### Step 5: Determine Zone/Subzone

1. **First**, read `~/.claude/skills/zoning-analysis-uruguay/normativa/tone-zones.json` — a structured index of all 9 localities, 33 zones, 70 subzones with manzana descriptions, FOS/FOT/retiros/altura values, and special rules. Use it to narrow candidates by matching `nomloccat` to a locality and `nummancat` to manzana descriptions.
2. **Then**, cross-reference against the full normativa text (loaded in Step 4) to verify zone boundaries described by street names and geographic features.
3. Use `nomloccat` and `nummancat` (block number) to match zone boundary descriptions
4. Check position relative to Ruta 10, coastline, and named streets
5. If the zone is ambiguous, present the possible options via AskUserQuestion
6. State your reasoning for the zone determination

### Step 6: Calculate Building Envelope

Apply the normativa rules to the specific lot:

1. **Permitted building types**: Check lot area against minimum lot requirements for each type
2. **Maximum height and floors**: Based on building type and lot area
3. **Setbacks**: Front, lateral, rear — accounting for:
   - Ruta 10 frontage (larger setbacks)
   - Small-lot provisions (frente ≤ 15m)
   - Auxiliary construction allowances in setbacks
4. **Occupation factors**: FOS, FOS SS, FOS V, FOT
   - Interpolate by lot area when between defined ranges
   - Calculate actual m² from percentages
5. **Buildable footprint**: Lot area minus setback areas
6. **Maximum built area**: FOT × lot area
7. **Special conditions**: Galibo (last floor setback), overhangs, piloti requirements

### Step 6b: Development Strategy (Decision Tree)

After calculating the envelope, evaluate the optimal development strategy for the lot. This determines the **recommended unit count and building type** that maximizes affordable housing potential.

#### Decision Tree

```
START
  │
  ├─ What building types are permitted in this zone/subzone?
  │   List all: aislada, apareada, conjunto, bloque bajo, edificación baja, bloque medio
  │
  ├─ For each permitted type, does the lot meet minimum area/frente?
  │   Filter to viable types only
  │
  ├─ For each viable type, calculate max units:
  │
  │   AISLADA (isolated):
  │     - If zone has conjunto rule (1,000 m²/unit): units = floor(lot_area / 1,000)
  │     - If no conjunto rule: 1 unit per lot (Art. D.257 always allows 1 vivienda)
  │     - Minimum 1 unit regardless
  │
  │   APAREADA (paired/duplex):
  │     - Conjunto rule is per PAIR: 1,000 m² per pair = 2 units per 1,000 m²
  │     - So units = floor(lot_area / 1,000) × 2
  │     - Shared party wall = 0 m lateral setback on shared side
  │     - Example: 1,028 m² → 1 pair → 2 units
  │
  │   CONJUNTO (group):
  │     - Aisladas: 1,000 m² per unit, 6 m separation
  │     - Apareadas: 1,000 m² per pair, 6 m between pairs
  │     - Units = (aislada count) or (apareada count × 2)
  │
  │   BLOQUE BAJO:
  │     - Min lot typically 1,200 m² (30 m frente)
  │     - Units = floor(FOT m² × (1 - circulation) / avg_unit_area)
  │     - No per-unit lot area rule — density driven by FOT
  │
  │   EDIFICACIÓN BAJA:
  │     - Min lot typically 2,000 m² (30 m frente)
  │     - Similar to bloque bajo but lower height
  │
  │   BLOQUE MEDIO:
  │     - Min lot typically 1,000 m² (30 m frente)
  │     - Highest density — FOT up to 290%
  │
  ├─ SUBDIVISION option:
  │     - Can the lot be subdivided to unlock more units?
  │     - Smaller lots get HIGHER FOS/FOT (40%/60% under 400 m²)
  │     - Each subdivided lot gets 1 vivienda under Art. D.257
  │     - Trade-off: more units but subdivision requires municipal approval
  │     - Calculate: if split into N lots of lot_area/N m² each:
  │       total_buildable = N × (lot_area/N × FOT_at_that_size)
  │     - Compare to single-lot buildable
  │
  ├─ Rank strategies by:
  │     1. Maximum unit count (more units = lower cost per unit = more affordable)
  │     2. Total buildable m² (more area = more flexibility)
  │     3. Administrative feasibility (apareada > subdivision > englobamiento)
  │
  └─ OUTPUT: Recommended strategy with reasoning
```

#### Output: Development Strategy Table

Include this in the report after the Building Envelope section:

```markdown
## Development Strategy

| Strategy | Type | Units | Buildable m² | m²/Unit | Feasibility |
|----------|------|-------|-------------|---------|-------------|
| A: Single vivienda | Aislada | 1 | 514 m² | 514 | Immediate |
| B: Duplex | Apareada | 2 | 514 m² | 257 | Immediate |
| C: Subdivide ×3 | Aislada | 3 | 617 m² | 206 | Requires approval |
| **Recommended: B** | | | | | |

**Reasoning:** Apareada (duplex) doubles units without subdivision, leveraging the 1,000 m²/pair rule. Each unit at 257 m² (PB+PA) is generous for first-time buyers. Strategy C yields more units but requires municipal subdivision approval.
```

#### Envelope Data addition

Add the recommended strategy to the Envelope Data JSON:

```json
{
  "strategy": {
    "recommended": "apareada",
    "max_units": 2,
    "building_type": "Unidades apareadas",
    "reasoning": "1,000 m²/pair rule allows 2 units without subdivision",
    "alternatives": [
      { "type": "aislada", "units": 1, "buildable": 514 },
      { "type": "subdivide_3", "units": 3, "buildable": 617, "requires": "municipal approval" }
    ]
  }
}
```

The `/clt-proforma` skill should read `strategy.max_units` to cap units, and `strategy.recommended` to label the building type.

### Step 7: Present Analysis

Use the output format below to present a structured analysis.

### Step 8: Save Report

Save the report as a markdown file to `~/Documents/Alpaca Labs/Estudio Local/Reports/`:
- Single lot: `padron-{number}-{location}.md`
- Multiple lots: `padrones-{range}-{location}-{count}-lots.md`

Use lowercase, hyphens for spaces, and the locality name (e.g., `buenos-aires`, `la-barra`, `punta-del-este`).

### Step 9: Save Normativa (if fetched)

If new articles were fetched from the digesto during this analysis:
1. Ask the user if they want to save them as a local normativa reference file
2. If yes, write to `~/.claude/skills/zoning-analysis-uruguay/normativa/` with a descriptive filename
3. Update `location-map.md` with the new mapping

## Output Format

### Single Lot

```markdown
# Zoning Envelope Analysis — Padrón [number], [location]

## Lot Data
| Parameter | Value |
|-----------|-------|
| Padrón | ... |
| Manzana | ... |
| Location | ... |
| Area | ... m² |
| Regime | ... |
| Approx. dimensions | ... m × ... m |
| Coordinates | lat, lon |

## Applicable Zone
**[Zone name] → [Subzone name]**
Reasoning for zone determination.

## Permitted Building Types
Which types are viable given this lot's area, with minimum area requirements listed.

## Building Envelope

### Height
| Parameter | Value |
|-----------|-------|
| Max height | ... m |
| Floors | ... |
| Notes | ... |

### Occupation Factors
| Factor | % | m² |
|--------|---|-----|
| FOS SS | ... | ... |
| FOS | ... | ... |
| FOS V | ... | ... |
| FOT | ... | ... |

(Interpolated by lot area if between defined ranges)

### Setbacks
| Direction | Distance | Notes |
|-----------|----------|-------|
| Front | ... m | ... |
| Lateral 1 | ... m | ... |
| Lateral 2 | ... m | ... |
| Rear | ... m | ... |

### Auxiliary Constructions in Setbacks
What can be built in setbacks, with limits (area, height).

### Overhangs (Salientes)
Projection allowances over setbacks.

## Buildable Envelope Sketch
ASCII diagram showing the lot with setbacks and buildable zone, oriented with front at bottom.

## Key Constraints
- Bullet list of the most important limiting factors
- Compliance issues (undersized lot, etc.)
- Special conditions that apply

## Envelope Data

Machine-readable data for `/zoning-envelope`. Include the exact lot polygon from the GIS input converted to local meters, plus all computed envelope parameters.

```json
{
  "lot_poly": [[x, y], ...],
  "unit": "m",
  "setbacks": { "front": 6, "rear": 3, "lateral1": 3, "lateral2": 2 },
  "volumes": [
    { "type": "base", "inset": 3.5, "h_bottom": 0, "h_top": 7, "label": "unidad aislada" }
  ],
  "height_cap": 7,
  "info": { "title": "Padrón ..., ...", "zone": "...", "id": "Padrón ...", "area": "... m²" },
  "stats": { "FOS": "25% → ... m²", "FOT": "50% → ... m²", ... }
}
```

For multi-lot analyses, add a `"scenarios"` key:
```json
{
  "scenarios": {
    "A": { "label": "Individual", "volumes": [...], "stats": {...} },
    "B": { "label": "Apareadas", "volumes": [...], "stats": {...} },
    "C1": { "label": "Unified", "volumes": [...], "stats": {...} }
  }
}
```

To generate an interactive 3D viewer from this data, run: `/zoning-envelope path/to/this-report.md`
```

### Multiple Adjoining Lots

When analyzing adjoining lots, present three sections:

```markdown
# Zoning Envelope Analysis — Padrones [A], [B], [...], [location]

## Lot Data
Table listing each lot's attributes side by side.

| Parameter | Padrón A | Padrón B | Combined |
|-----------|----------|----------|----------|
| Area | ... m² | ... m² | ... m² |
| Dimensions | ... | ... | ... |
| ... | | | |

## Applicable Zone
Zone determination (typically the same for adjoining lots in the same manzana).

---

## Scenario A: Individual Lots (separate padrones)

For each lot, present the full envelope analysis (height, occupation factors, setbacks, sketch).
Note which building types are available at each individual lot size.

## Scenario B: Apareadas (party wall, no unification)

If the zone permits unidades apareadas:
- Each lot keeps its own padrón and is calculated independently
- Party-wall side: 0 m setback (shared boundary)
- Free lateral: standard setback
- Show combined sketch with both units and the party wall indicated
- Total built area = sum of individual FOTs

## Scenario C: Unificación (englobamiento into single padrón)

Calculate the envelope for the merged lot:
- Combined area for occupation factor interpolation
- Eliminated internal setbacks (shared boundary disappears)
- New combined dimensions and frontage
- Check if the larger area unlocks new building types (bloque bajo at 1,200 m², edificación baja at 2,000 m², etc.)
- Show unified buildable sketch

## Comparison

| Parameter | Individual (×N) | Apareadas | Unified |
|-----------|-----------------|-----------|---------|
| Total area | ... m² | ... m² | ... m² |
| FOS (m²) | ... | ... | ... |
| FOT (m²) | ... | ... | ... |
| Max height | ... | ... | ... |
| Building types | ... | ... | ... |
| Setback efficiency | ... | ... | ... |

## Recommendation
Which scenario offers the best development potential, considering:
- Total buildable area (FOT)
- Layout flexibility (footprint shape and setback efficiency)
- Building types unlocked
- Administrative complexity (englobamiento requires Catastro procedure)
```

## Notes

- The TONE is Volume V of the Digesto Departamental de Maldonado
- Normativa files are organized by Título/Capítulo/Sector following the digesto structure
- Zone-specific rules override general sector rules
- When in doubt about zone boundaries, always ask the user — zone determination is the most critical step
- Occupation factors between defined area ranges should be linearly interpolated

### Multi-lot notes
- **Apareadas** (party wall): each lot retains its own padrón and is calculated independently; the shared boundary has 0 m setback; the TONE permits this wherever "unidades apareadas" are listed as an allowed building type
- **Unificación / englobamiento**: merging padrones at Catastro creates a single lot; all parameters (FOS, FOT, setbacks, building types) are recalculated on the unified area; the internal shared boundary disappears entirely
- **Key thresholds to flag** when combining lots: 1,000 m² (conjunto), 1,200 m² (bloque bajo 9 m), 2,000 m² (bloque bajo 12 m / edificación baja)
- When lots span different zones (rare for adjoining lots), each portion must comply with its own zone's parameters — flag this as a constraint
