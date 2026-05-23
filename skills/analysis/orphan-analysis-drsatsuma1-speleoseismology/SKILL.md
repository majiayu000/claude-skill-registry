---
name: orphan-analysis
description: Identify orphan earthquakes far from mapped faults that indicate unmapped active structures. Use when analyzing microseismicity, finding dark earthquake source faults, or validating fault database gaps. Triggers on "orphan analysis", "unmapped fault", "microseismicity", "fault gap".
---

# /orphan-analysis - Orphan Earthquake Detection Skill

## Purpose

Identify "orphan earthquakes" - seismic events far from any mapped fault - that indicate unmapped active structures. These structures may be sources of historical "dark earthquakes" detectable in speleothem records.

## Usage

```
/orphan-analysis <lat> <lon> [--name NAME] [--radius KM] [--orphan-threshold KM]
```

**Examples:**
```
/orphan-analysis 44.13 8.11 --name "Bàsura Cave"
/orphan-analysis 41.42 31.93 --name "Sofular Cave" --radius 150
/orphan-analysis 16.2 -89.1 --name "Yok Balum" --orphan-threshold 30
```

## Methodology

### Validated in Italy

The orphan analysis methodology was validated in the Ligurian Alps:
- **80% orphan rate** revealed unmapped NNW-trending fault
- **193+ earthquakes** on structure not in ANY database
- **25+ km lineament** identified via DEM + microseismicity
- Now primary candidate for 1285/1394 dark earthquakes

## Workflow

### Step 1: Search Earthquake Catalog

Use `earthquake_search` MCP tool:

```
earthquake_search lat=44.13 lon=8.11 radius_km=100 min_magnitude=2.0
```

**Parameters:**
- Default radius: 100 km
- Default min_magnitude: 2.0 (for microseismicity)
- Date range: 1900-present (or available)

### Step 2: Load Fault Database

Query regional fault database:

| Region | Primary Database | File/URL |
|--------|-----------------|----------|
| Italy | DISS v3.3.1 | `data/fault_databases/diss331_*.geojson` |
| California | SCEC CFM v7.0 | `data/fault_databases/scec_cfm_*.geojson` |
| Turkey | AFAD | Web query |
| Global | GEM Global | `data/gem_active_faults.geojson` |

### Step 3: Calculate Distances

For each earthquake, calculate distance to nearest mapped fault:

```
For each earthquake:
    min_distance = infinity
    for each fault_segment:
        d = calc_distance(eq.lat, eq.lon, fault.lat, fault.lon)
        if d < min_distance:
            min_distance = d
            nearest_fault = fault.name

    earthquake.dist_to_fault = min_distance
    earthquake.nearest_fault = nearest_fault
```

### Step 4: Classify Orphans

Apply orphan threshold (default: 50 km):

```
if dist_to_fault > orphan_threshold:
    earthquake.is_orphan = True
else:
    earthquake.is_orphan = False
```

### Step 5: Cluster Orphans by Azimuth

Group orphan earthquakes by direction from reference point:

```
Azimuth bins:
- N (337.5-22.5°)
- NE (22.5-67.5°)
- E (67.5-112.5°)
- SE (112.5-157.5°)
- S (157.5-202.5°)
- SW (202.5-247.5°)
- W (247.5-292.5°)
- NW (292.5-337.5°)
```

### Step 6: Generate Report

```markdown
## Orphan Earthquake Analysis: [Location Name]

**Reference point**: [lat]°N, [lon]°E
**Search radius**: [X] km
**Orphan threshold**: [X] km
**Analysis date**: [date]

---

### Summary Statistics

| Metric | Value |
|--------|-------|
| Total earthquakes | [N] |
| Orphan earthquakes | [N] ([X]%) |
| M4+ orphans | [N] |
| M5+ orphans | [N] |

---

### Orphan Rate Assessment

| Rate | Interpretation |
|------|----------------|
| > 50% | **CRITICAL** - Major unmapped structure likely |
| 30-50% | **HIGH** - Significant database gap |
| 10-30% | **MODERATE** - Some unmapped faults |
| < 10% | **LOW** - Database reasonably complete |

**This region**: [X]% → [INTERPRETATION]

---

### Orphan Clusters by Azimuth

| Direction | Count | Avg Distance | M4+ | M5+ | Structure? |
|-----------|-------|--------------|-----|-----|------------|
| NNW | [N] | [X] km | [N] | [N] | [YES/NO] |
| SW | [N] | [X] km | [N] | [N] | [YES/NO] |
| ... | ... | ... | ... | ... | ... |

---

### Candidate Unmapped Structures

#### Structure 1: [Direction] Lineament

- **Azimuth**: [X]° ([direction])
- **Orphan count**: [N] earthquakes
- **Distance range**: [min]-[max] km from reference
- **Magnitude range**: M[min]-M[max]
- **Largest event**: M[X] on [date]

**Interpretation**: [Description of possible fault]

---

### Mapped Faults in Region

| Fault Name | Strike | Distance | Type |
|------------|--------|----------|------|
| [name] | [X]° | [X] km | [normal/strike-slip/etc.] |

---

### Visualization

[Description of recommended figure showing:]
- Reference point (cave location)
- Mapped faults (from database)
- All earthquakes (color by orphan status)
- Azimuth bins with orphan clusters
```

## Output Files

The skill can generate:

1. **Analysis report** (`[REGION]_ORPHAN_ANALYSIS.md`)
2. **Earthquake CSV** (`[region]_earthquakes.csv`)
3. **Orphan subset CSV** (`[region]_orphans.csv`)
4. **Cluster definitions** (`[region]_clusters.json`)

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `earthquake_search` | Search USGS catalog |
| `calc_distance` | Calculate earthquake-fault distances |
| `calc_pga` | Estimate ground motion (optional) |

## Example: Italy Bàsura Results

```
## Orphan Analysis: Bàsura Cave (Italy)

Reference: 44.1275°N, 8.1108°E
Radius: 100 km
Orphan threshold: 50 km

### Summary
- Total earthquakes: 241
- Orphan earthquakes: 193 (80%)
- M4+ orphans: 12
- M5+ orphans: 2

### Orphan Rate: 80% → CRITICAL

### Key Finding: NNW Lineament

- Azimuth: 340° (NNW-SSE)
- 85 orphan earthquakes
- Not in DISS, ITHACA, or EFSM20
- 25+ km linear structure identified
- Primary candidate for 1285/1394 dark earthquakes
```

## Integration with DEM Analysis

After orphan analysis, recommend DEM lineament check:

```
If orphan_rate > 30%:
    Recommend: /dem-pipeline for visual confirmation

    Look for:
    - Linear drainage patterns aligned with orphan clusters
    - Edge detection features at orphan azimuths
    - Topographic breaks matching cluster directions
```

## Regional Catalogs

| Region | Catalog | Coverage | Notes |
|--------|---------|----------|-------|
| Italy | INGV ISIDe | 1900-present | Excellent |
| California | USGS ANSS | 1900-present | Excellent |
| Turkey | AFAD | 1900-present | Good |
| Belize | USGS | Limited | Sparse coverage |
| Brazil | USGS + IAG | Limited | Intraplate, sparse |

## Important Notes

1. **Orphan threshold varies by region** - Use 50 km for plate boundaries, 30 km for intraplate
2. **Catalog completeness matters** - Low magnitude threshold may include noise
3. **Fault database gaps exist** - USGS has 9-27 year lag
4. **Offshore coverage poor** - Many faults unmapped submarine
5. **Follow up with DEM** - Visual confirmation strengthens case
