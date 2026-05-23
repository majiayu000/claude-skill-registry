---
name: zscore
description: Calculate z-scores for speleothem geochemical data. Use when analyzing cave isotope anomalies, finding significant deviations, or identifying potential earthquake signals. Triggers on "zscore", "calculate z", "anomaly analysis", "find anomalies".
---

# /zscore - Quick Z-Score Analysis Skill

## Purpose

Rapidly calculate z-scores for speleothem δ18O, δ13C, and other proxy data to identify significant anomalies. This is the core analysis workflow used multiple times per session.

## Usage

```
/zscore <cave_name_or_entity_id> [--start YEAR] [--end YEAR] [--proxy PROXY] [--threshold Z]
```

**Examples:**
```
/zscore YOKI                              # All Yok Balum data
/zscore CRC-3 --start 1850 --end 1950     # Crystal Cave 1850-1950
/zscore "Bàsura" --proxy d18O,d13C        # Multiple proxies
/zscore 390 --threshold 2.5               # Higher significance threshold
```

## Workflow

### Step 1: Get Cave Data

Use MCP tools to retrieve data:

```
# Search for cave
sisal_search_caves region="Italy" min_samples=50

# Get samples for specific entity
sisal_get_samples entity_id="123"
```

### Step 2: Extract Proxy Measurements

From the returned data, extract:
- `d18O_measurement` - Oxygen isotope values (‰ VPDB)
- `d13C_measurement` - Carbon isotope values (‰ VPDB)
- `interp_age` - Interpolated age (years BP)
- `year_CE` - Calendar year (1950 - interp_age)

### Step 3: Calculate Baseline Statistics

For the full record (or specified baseline period):

```
δ18O: μ = mean(d18O), σ = std(d18O)
δ13C: μ = mean(d13C), σ = std(d13C)
```

### Step 4: Calculate Z-Scores

For each measurement:
```
z = (measurement - μ) / σ
```

### Step 5: Identify Anomalies

Apply threshold (default |z| ≥ 2.0):

| Z-Score Range | Classification |
|---------------|----------------|
| z ≤ -3.0 | **EXTREME NEGATIVE** |
| -3.0 < z ≤ -2.0 | **SIGNIFICANT NEGATIVE** |
| -2.0 < z < +2.0 | Normal |
| +2.0 ≤ z < +3.0 | **SIGNIFICANT POSITIVE** |
| z ≥ +3.0 | **EXTREME POSITIVE** |

### Step 6: Generate Output Table

```markdown
## Z-Score Analysis: [Cave Name]

**Entity**: [entity_id]
**Data range**: [start] - [end] CE
**Measurements**: [N] δ18O, [N] δ13C

### Baseline Statistics

| Proxy | Mean (μ) | Std Dev (σ) | N |
|-------|----------|-------------|---|
| δ18O | -X.XX‰ | X.XX‰ | N |
| δ13C | -X.XX‰ | X.XX‰ | N |

### Anomalies (|z| ≥ 2.0)

| Year CE | δ18O (‰) | δ18O z | δ13C (‰) | δ13C z | Classification |
|---------|----------|--------|----------|--------|----------------|
| ~1394 | -6.23 | -2.16σ | N/A | N/A | SIGNIFICANT NEG |
| ~1285 | -6.89 | -2.46σ | N/A | N/A | SIGNIFICANT NEG |

### Time Windows of Interest

[Group consecutive anomalies into windows]

| Window | Duration | Peak δ18O z | Peak δ13C z | Notes |
|--------|----------|-------------|-------------|-------|
| 1280-1295 CE | 15 yr | -2.46σ | N/A | Possible seismic |
```

## Interpretation Guidelines

### δ18O Anomalies

| Direction | Typical Cause |
|-----------|---------------|
| **Negative** (z < -2) | Increased deep/old water contribution OR wetter conditions |
| **Positive** (z > +2) | Increased evaporation OR drier conditions |

### δ13C Anomalies

| Direction | Typical Cause |
|-----------|---------------|
| **Negative** (z < -2) | More biogenic CO₂ (soil respiration) |
| **Positive** (z > +2) | More geogenic CO₂ (earthquake/volcanic) OR prior calcite precipitation |

### Coupled vs Decoupled

| Pattern | δ18O | δ13C | Interpretation |
|---------|------|------|----------------|
| **COUPLED** | Anomaly | Anomaly (same direction) | SEISMIC (Chiodini mechanism) |
| **DECOUPLED** | Anomaly | Normal OR opposite | CLIMATIC (drought, volcanic) |

## Output Format

The skill outputs:

1. **Cave metadata** (entity, coordinates, coverage)
2. **Baseline statistics table**
3. **All anomalies table** (sorted by |z|)
4. **Time windows of interest** (grouped anomalies)
5. **Quick interpretation** (coupled/decoupled assessment)

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `sisal_search_caves` | Find cave entity ID |
| `sisal_get_samples` | Download measurements |

## Advanced Options

### Multi-Proxy Analysis
```
/zscore YOKI --proxy d18O,d13C,MgCa
```

### Specific Time Window
```
/zscore CRC-3 --start 1890 --end 1900  # Around 1896 earthquake
```

### Higher Threshold
```
/zscore "Bàsura" --threshold 2.5  # More stringent (fewer false positives)
```

### Baseline Period
```
/zscore YOKI --baseline 1800-1900  # Use specific period for μ/σ
```

## Example Full Output

```
## Z-Score Analysis: Crystal Cave (CRC-3)

**Entity**: 456
**Coordinates**: 36.59°N, 118.82°W
**Data range**: 873 - 2006 CE
**Measurements**: 1,054 δ18O

### Baseline Statistics

| Proxy | Mean (μ) | Std Dev (σ) | N |
|-------|----------|-------------|---|
| δ18O | -8.23‰ | 0.42‰ | 1,054 |

### Anomalies (|z| ≥ 2.0)

| Year CE | δ18O (‰) | δ18O z | Classification |
|---------|----------|--------|----------------|
| ~1741 | -9.72 | -3.54σ | **EXTREME NEG** |
| ~1896 | -9.13 | -2.14σ | SIGNIFICANT NEG |
| ~1910 | -9.72 | -3.54σ | **EXTREME NEG** |
| ... | ... | ... | ... |

**Total anomalies**: 47 (4.5% of record)

### Top 5 Most Extreme

1. ~1741 CE: z = -3.54σ (Pre-Spanish earthquake?)
2. ~1910 CE: z = -3.54σ (Known M6.0 Bishop)
3. ~1929 CE: z = -2.61σ (Known M5.5 Independence)
4. ~1896 CE: z = -2.14σ (Known M6.3 Independence)
5. ~1984 CE: z = -2.71σ (Known M6.1 Round Valley)

### Interpretation

✓ Modern earthquakes (1896, 1910, 1929, 1984) all show z ≤ -2.0
✓ Pre-Spanish ~1741 anomaly consistent with Rose Canyon/Kern Canyon event
✓ Cave shows reliable seismic sensitivity
```

## Important Notes

1. **Z-scores are relative** - Compare within same cave record
2. **Resolution matters** - Annual vs decadal samples affect detection
3. **Missing data** - Note gaps in record around anomalies
4. **Multi-proxy preferred** - Single proxy anomaly is weaker evidence
5. **Follow up with /classify-anomaly** - For full seismic vs climatic discrimination
