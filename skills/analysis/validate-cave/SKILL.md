---
name: validate-cave
description: Test speleothem earthquake detection against modern earthquake catalogs. Use when validating methodology, checking if cave detects known earthquakes, building validation matrix. Triggers on "validate cave", "test detection", "modern earthquake validation", "blind test".
---

# /validate-cave - Modern Earthquake Validation Skill

## Purpose

Systematically test if a speleothem cave record detects known modern earthquakes. This validates the paleoseismic methodology and builds the 50+ validation matrix.

## Usage

```
/validate-cave <cave_name_or_entity_id> [--start YEAR] [--end YEAR] [--radius KM]
```

**Examples:**
```
/validate-cave CRC-3                     # Crystal Cave (California)
/validate-cave YOKI --start 1970 --end 2010
/validate-cave "Lapa Grande" --radius 50
/validate-cave Ko-1                      # Kocain (Turkey)
```

## Workflow

### Step 1: Identify Cave & Get Coordinates

1. **Search SISAL** using `sisal_search_caves` MCP tool
2. **Get cave metadata**: entity_id, coordinates, site name
3. **Determine data coverage**: earliest/latest sample dates

```
# Example MCP call
sisal_search_caves region="California" min_samples=50
```

### Step 2: Search for Modern Earthquakes

Use `earthquake_search` MCP tool to find earthquakes near cave:

```
# Default: M≥5.0, 100 km radius, 1900-2025
earthquake_search lat=36.59 lon=-118.82 min_magnitude=5.0 radius_km=100
```

**Filter results**:
- Keep only earthquakes within cave data timespan
- Note earthquakes outside timespan (for documentation)

### Step 3: Download Cave Data

Use `sisal_get_samples` MCP tool:

```
sisal_get_samples entity_id="123"
```

**Extract**:
- δ18O measurements with dates
- δ13C measurements (if available)
- Mg/Ca measurements (if available)

### Step 4: Calculate Baseline Statistics

For all cave data:
```
δ18O: μ = mean(d18O_measurement), σ = std(d18O_measurement)
δ13C: μ = mean(d13C_measurement), σ = std(d13C_measurement)
```

### Step 5: Test Each Earthquake

For each earthquake within cave data coverage:

1. **Define test window**: earthquake_year ± 10 years
2. **Extract data in window**: All samples within ±10 years
3. **Calculate z-scores**: z = (measurement - μ) / σ
4. **Find extreme values**: Most negative AND most positive z-score
5. **Apply detection threshold**:
   - |z| ≥ 2.0 → **DETECTED**
   - |z| < 2.0 → **NOT DETECTED**

### Step 6: Generate Results Table

```markdown
| Date | Magnitude | Distance (km) | Cave Data? | δ18O z | Detection | Notes |
|------|-----------|---------------|------------|--------|-----------|-------|
| 1976-02-04 | M7.5 | 30 km | ✓ Yes | +1.32σ | ✗ NO | Below threshold |
| 1896-07-21 | M6.3 | 48 km | ✓ Yes | -3.54σ | **✓ YES** | Strong signal |
```

### Step 7: Calculate Statistics

```
Detection rate = (detections / tests_with_data) × 100%

Example:
- Total earthquakes found: 9
- Earthquakes with cave coverage: 6
- Detections (z ≥ 2.0): 1
- Non-detections: 5
- **Detection rate: 16.7%**
```

### Step 8: Update VALIDATION_MATRIX_50PLUS.md

Add/update cave section in `paleoseismic_caves/VALIDATION_MATRIX_50PLUS.md`:

```markdown
### [Cave Name] ([Country]) - [N] Earthquakes

**Cave coordinates**: [lat]°N, [lon]°W
**Data coverage**: [start] - [end] CE
**Cave entity**: [entity_id] (SISAL)

#### Modern Earthquakes:

[Results table]

**Detection rate**: X/Y (Z%)

**Notes**: [Interpretation, hypotheses for non-detections]
```

## Detection Criteria

| Threshold | Interpretation |
|-----------|----------------|
| z ≥ +2.0 or z ≤ -2.0 | **DETECTED** (significant anomaly) |
| 1.5 ≤ |z| < 2.0 | **MARGINAL** (near threshold) |
| |z| < 1.5 | **NOT DETECTED** |

## Interpreting Results

### High Detection Rate (≥60%)
- Cave is **sensitive** to earthquakes
- Methodology validated for this setting
- Prehistoric detections are credible

### Moderate Detection Rate (30-60%)
- Cave may be **selective** (certain magnitudes/distances)
- Need to identify detection threshold
- Prehistoric detections need scrutiny

### Low Detection Rate (<30%)
- Cave may be **insensitive** after certain date
- Check for cave changes (flowpath, aquifer)
- Prehistoric detections HIGHLY UNCERTAIN

### Zero Detection (0%)
- **Critical concern** (like Yok Balum)
- Investigate: (a) Cave sensitivity, (b) Tectonic setting, (c) Data quality
- Prehistoric "detections" may not be seismic

## Output Format

The skill outputs:

1. **Cave metadata box** (coordinates, coverage, entity_id)
2. **Earthquake search summary** (N earthquakes found, N testable)
3. **Full results table** (all earthquakes with test results)
4. **Statistics summary** (detection rate, range tested)
5. **Interpretation** (what results mean for methodology)
6. **Update to VALIDATION_MATRIX_50PLUS.md** (with approval)

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `sisal_search_caves` | Find cave in SISAL database |
| `sisal_get_samples` | Download δ18O/δ13C/Mg measurements |
| `earthquake_search` | Search USGS catalog near cave |
| `calc_distance` | Verify earthquake-cave distances |
| `calc_pga` | Calculate expected ground acceleration |

## Example Full Workflow

```
User: /validate-cave CRC-3

Claude:
1. Searching SISAL for CRC-3 (Crystal Cave)...
   - Entity ID: 123
   - Coordinates: 36.59°N, 118.82°W
   - Data: 873-2006 CE (1,054 δ18O measurements)

2. Searching USGS catalog (M≥5.0, 100km, 1900-2025)...
   - Found 11 earthquakes
   - 9 within cave data coverage (873-2006 CE)

3. Calculating z-scores...
   - Baseline: μ=-8.23‰, σ=0.42‰

4. Testing each earthquake...
   [Results table]

5. RESULTS:
   - Detections: 9/9
   - Detection rate: **100%** ✓✓✓

6. INTERPRETATION:
   Crystal Cave shows PERFECT detection of modern earthquakes.
   This validates the methodology for California Sierra Nevada setting.

Would you like me to update VALIDATION_MATRIX_50PLUS.md with these results?
```

## Important Notes

1. **Document BOTH detections AND non-detections** - Publication requires honest statistics
2. **Non-detection ≠ failure** - May indicate distance/magnitude thresholds
3. **0% detection is significant** - Yok Balum 0% rate is scientifically valuable
4. **Check data quality** - Missing samples around earthquake = inconclusive, not non-detection
5. **Consider tectonic setting** - Strike-slip vs thrust vs subduction may behave differently
