---
name: regional-doc
description: Generate regional analysis document templates for paleoseismic research. Use when starting analysis of a new cave or event, creating standardized documentation. Triggers on "new regional doc", "create analysis", "template for", "document cave".
---

# /regional-doc - Regional Analysis Template Generator

## Purpose

Generate standardized markdown templates for regional paleoseismic analyses. Ensures consistent documentation structure across all regions and events.

## Usage

```
/regional-doc <type> <region> <subject> [--date DATE] [--cave CAVE]
```

**Types:**
- `cave-analysis` - Full cave analysis document
- `event-analysis` - Single event/anomaly analysis
- `validation` - Cross-validation with paleoseismic records
- `blind-test` - Modern earthquake validation test
- `fault-verification` - Fault database verification

**Examples:**
```
/regional-doc cave-analysis italy "Corchia Cave"
/regional-doc event-analysis belize "620 CE" --cave "Yok Balum"
/regional-doc validation california "1741" --cave "Crystal Cave"
/regional-doc fault-verification caribbean "Dos Anas" --date 1400
```

## Template Types

### 1. Cave Analysis (`cave-analysis`)

**Filename**: `[CAVE_NAME]_CAVE_ANALYSIS.md`
**Location**: `regions/[region]/`

```markdown
# [Cave Name] Cave Analysis

**Location**: [lat]°N/S, [lon]°E/W
**Region**: [Country/Region]
**Entity ID**: [SISAL entity_id]
**Data Source**: SISAL v3

---

## Cave Overview

### Geography & Geology
- **Elevation**: [X] m asl
- **Cave type**: [limestone/dolomite/etc.]
- **Speleothem type**: [stalagmite/flowstone/etc.]
- **Climate zone**: [tropical/temperate/etc.]

### Tectonic Setting
- **Nearest major fault**: [Fault name] ([distance] km)
- **Seismic hazard**: [high/moderate/low]
- **Known historical earthquakes**: [list major events]

---

## Data Coverage

| Proxy | Time Span | Measurements | Resolution |
|-------|-----------|--------------|------------|
| δ18O | [start] - [end] CE | [N] | [X] yr/sample |
| δ13C | [start] - [end] CE | [N] | [X] yr/sample |
| Mg/Ca | [start] - [end] CE | [N] | [X] yr/sample |

### Baseline Statistics

| Proxy | Mean (μ) | Std Dev (σ) | Range |
|-------|----------|-------------|-------|
| δ18O | [X]‰ | [X]‰ | [min] to [max] |
| δ13C | [X]‰ | [X]‰ | [min] to [max] |

---

## Anomaly Inventory

### Significant Anomalies (|z| ≥ 2.0)

| Date (CE) | δ18O z | δ13C z | Classification | Notes |
|-----------|--------|--------|----------------|-------|
| ~[year] | [z]σ | [z]σ | [SEISMIC/CLIMATIC/etc.] | [notes] |

### Top 5 Most Extreme

1. **[Date]**: [description]
2. ...

---

## Seismic Candidates

### Event 1: ~[Date] CE

**Evidence summary:**
| Metric | Value | Significance |
|--------|-------|--------------|
| δ18O z | [X]σ | [interpretation] |
| δ13C z | [X]σ | [interpretation] |
| Recovery | [X] years | [interpretation] |

**Classification**: [SEISMIC CANDIDATE / CLIMATIC / etc.]

**Cross-validation**: [list independent evidence]

---

## Modern Earthquake Validation

| Date | Magnitude | Distance | Detection? | Notes |
|------|-----------|----------|------------|-------|
| [date] | M[X] | [X] km | [YES/NO] | [notes] |

**Detection rate**: [X]/[Y] ([Z]%)

---

## References

1. [Primary publication for this cave]
2. [SISAL database entry]
3. [Relevant seismic catalogs]
```

### 2. Event Analysis (`event-analysis`)

**Filename**: `[CAVE]_[DATE]CE_ANALYSIS.md`

```markdown
# [Cave Name] ~[Date] CE Analysis

**Dating uncertainty**: [uncertainty description]
**Classification**: [SEISMIC CANDIDATE / DARK EARTHQUAKE / etc.]

---

## Executive Summary

[2-3 paragraph summary of findings]

---

## Primary Evidence

### Geochemical Anomaly

| Proxy | Anomaly Period | Peak Z-score | Notes |
|-------|---------------|--------------|-------|
| δ18O | [start]-[end] CE | [z]σ | [notes] |
| δ13C | [start]-[end] CE | [z]σ | [notes] |
| Mg/Ca | [start]-[end] CE | [z]σ | [notes] |

### Temporal Structure

[Description of anomaly shape - sudden onset, recovery pattern, etc.]

### Coupling Analysis

- Coupling ratio: [X]
- Classification: [COUPLED/DECOUPLED]
- Interpretation: [SEISMIC/CLIMATIC/VOLCANIC]

---

## Alternative Explanations

### Volcanic Forcing
- Eruptions checked: [list]
- Result: [RULED OUT / POSSIBLE / CONFIRMED]

### Climatic Forcing
- Drought indicators: [present/absent]
- Regional climate: [notes]
- Result: [RULED OUT / POSSIBLE]

---

## Cross-Validation

| Source | Finding | Overlap? |
|--------|---------|----------|
| [Paleoseismic trench] | [finding] | [YES/NO] |
| [Archaeological record] | [finding] | [YES/NO] |
| [Historical catalog] | [finding] | [YES/NO] |

---

## Classification Rationale

| Evidence | Status | Weight |
|----------|--------|--------|
| Multi-proxy | [✓/✗] | [HIGH/MOD/LOW] |
| Cross-validation | [✓/✗] | [HIGH/MOD/LOW] |
| Alternative ruled out | [✓/✗] | [HIGH/MOD/LOW] |

**Final classification**: [TIER 1/2/3] [CLASSIFICATION]

---

## Files Updated

| File | Change |
|------|--------|
| `PAPER_2_DARK_EARTHQUAKES.md` | [section] |
| `ANOMALY_CATALOG.md` | [entry added] |
```

### 3. Validation Document (`validation`)

**Filename**: `[CAVE]_[EVENT]_VALIDATION.md`

```markdown
# [Cave Name] [Event] Validation

**Purpose**: Cross-validate speleothem detection against independent paleoseismic records

---

## Speleothem Signal

| Proxy | Date | Z-score | Notes |
|-------|------|---------|-------|
| δ18O | [date] | [z]σ | [notes] |

---

## Independent Paleoseismic Evidence

### Source 1: [Trench/Lake/Tree Ring Name]

**Reference**: [citation]
**Method**: [trenching/turbidites/dendro/etc.]
**Date range**: [date ± uncertainty]
**Distance from cave**: [X] km

### Source 2: ...

---

## Temporal Overlap Analysis

| Source | Date Range | Speleothem Date | Overlap? |
|--------|------------|-----------------|----------|
| [source] | [range] | [date] | [YES/NO] |

---

## Validation Assessment

**Match quality**: [STRONG / MODERATE / WEAK / NO MATCH]

**Interpretation**: [1-2 paragraphs]
```

### 4. Fault Verification (`fault-verification`)

**Filename**: `[CAVE]_FAULT_DATABASE_VERIFICATION.md`

```markdown
# [Cave/Region] Fault Database Verification

**Date verified**: [date]
**Candidate event**: [event description]
**Classification**: [TRUE DARK / PRE-HISTORICAL / etc.]

---

## Databases Checked

| Database | Checked | Faults within 50km | Faults within 100km |
|----------|---------|-------------------|---------------------|
| [DISS/SCEC/GEM/etc.] | [✅/❌] | [list] | [list] |

---

## Key Findings

[Summary of what was found]

---

## Classification Rationale

| Criterion | Status | Notes |
|-----------|--------|-------|
| Fault mapped in databases | [YES/NO] | [details] |
| Historical record exists | [YES/NO] | [details] |
| Pre-dates written records | [YES/NO] | [details] |

**Final classification**: [TRUE DARK / PRE-HISTORICAL / etc.]
```

## Output

The skill generates:
1. **Template file** with all sections pre-structured
2. **Suggested filename** following naming convention
3. **Location** in correct `regions/` subdirectory

Then asks for approval to create the file.

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Cave analysis | `[CAVE]_CAVE_ANALYSIS.md` | `SOFULAR_CAVE_ANALYSIS.md` |
| Event analysis | `[CAVE]_[DATE]CE_ANALYSIS.md` | `YOK_BALUM_620CE_ANALYSIS.md` |
| Validation | `[CAVE]_[EVENT]_VALIDATION.md` | `MINNETONKA_WASATCH_VALIDATION.md` |
| Fault check | `[CAVE]_FAULT_DATABASE_VERIFICATION.md` | `DOS_ANAS_FAULT_DATABASE_VERIFICATION.md` |

## Directory Structure

```
regions/
├── brazil/
├── caribbean/
├── central_america/
├── india/
├── italy/
├── north_america/
├── peru/
├── romania/
└── turkey/
```

## Auto-Population

When possible, the skill will pre-populate:
- Cave coordinates from SISAL
- Baseline statistics from `/zscore` output
- Anomaly inventory from z-score analysis
- Fault distances using `calc_distance` MCP tool
