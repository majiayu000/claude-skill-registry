---
name: trioexplorer
description: Search clinical notes using the Trioexplorer CLI. Use when the user wants to search patient notes, list cohorts, view search history, or explore the clinical notes database.
allowed-tools: Bash
---

# Trioexplorer CLI

Search clinical notes using the `trioexplorer` CLI. The CLI requires `TRIOEXPLORER_API_KEY` to be set.

## Commands

### Search clinical notes
```bash
trioexplorer search "query" [options]
```

Options:
- `-k N` — Number of results (default: 10)
- `-d MODE` — Dedupe mode: `patient`, `encounter`, `note`, or `none` (default: encounter)
- `--type TYPE` — Search type: `keyword`, `semantic`, or `hybrid` (default)
- `--cohort-ids IDS` — Comma-separated cohort IDs to search
- `--patient-id UUID` — Filter to specific patient
- `--encounter-id UUID` — Filter to specific encounter
- `--note-types TYPES` — Comma-separated note types (e.g., "Progress Note,Discharge Summary")
- `--date-from DATE` — Filter notes from date (YYYY-MM-DD)
- `--date-to DATE` — Filter notes to date (YYYY-MM-DD)
- `--format FORMAT` — Output: `table` (default), `json`, or `csv`
- `--full-text` — Show full note text
- `--entity-filters JSON` — Filter by extracted entities (see Filters section)
- `--filters JSON` — Advanced metadata filters (JSON format)
- `--rerank false` — Disable semantic reranking
- `--vector-weight N` — Weight for vector vs keyword (0.0-1.0)

### List resources
```bash
trioexplorer list cohorts [--limit N]
trioexplorer list notetypes [--search TEXT]
trioexplorer list history [--page N] [--user-id ID]
trioexplorer list entities
trioexplorer list filters [--namespace NS] [--field NAME]
```

### Statistics
```bash
trioexplorer stats history [--date-from DATE] [--date-to DATE]
```

### Global options
- `--debug` — Enable request/response logging
- `--help` — Show help for any command

## Deduplication Modes

Use `-d` / `--distinct` to control how results are deduplicated. Each mode returns the highest-scoring result per entity.

| Mode | Description | Use Case |
|------|-------------|----------|
| `patient` | One result per patient | Find unique patients matching criteria |
| `encounter` | One result per encounter (default) | See different visits for same condition |
| `note` | One result per note | Multiple chunks from same note consolidated |
| `none` | No deduplication | See all matching chunks |

### Examples

```bash
# Find unique patients with Dupixent side effects
trioexplorer search "Dupixent side effects" -d patient -k 20

# See all encounters mentioning chest pain (default behavior)
trioexplorer search "chest pain" -d encounter -k 15

# Get all matching chunks without deduplication
trioexplorer search "metformin dosing" -d none -k 50

# Dedupe by note (useful when searching for specific documentation)
trioexplorer search "discharge instructions" -d note -k 10
```

## Basic Examples

Search for diabetes-related notes:
```bash
trioexplorer search "diabetes management" -k 20
```

Semantic search with JSON output:
```bash
trioexplorer search "patient having trouble with blood sugar" --type semantic --format json
```

Search within specific cohorts, dedupe by patient:
```bash
trioexplorer search "chest pain" --cohort-ids abc123 -d patient -k 10
```

## Patient & Encounter Filtering

Filter to a specific patient:
```bash
trioexplorer search "medication history" --patient-id "001EFCDE-62D9-42A0-B184-3E3C732EBDA5"
```

Filter to a specific encounter:
```bash
trioexplorer search "vital signs" --encounter-id "ABC12345-6789-0DEF-GHIJ"
```

Combine patient with date range and note types:
```bash
trioexplorer search "diabetes management" \
  --patient-id "001EFCDE-62D9-42A0-B184-3E3C732EBDA5" \
  --date-from 2025-01-01 \
  --note-types "Progress Note,Discharge Summary"
```

Filter by note type only:
```bash
trioexplorer search "discharge planning" --note-types "Discharge Summary"
```

Filter by date range:
```bash
trioexplorer search "recent visits" --date-from 2025-01-01 --date-to 2025-06-30
```

## Entity Filters

Filter search results by extracted medical entities. Use `--entity-filters` with JSON.

### Available filter fields

| Category | Fields |
|----------|--------|
| Entities | `medications`, `diagnoses`, `symptoms`, `procedures`, `lab_tests`, `vitals`, `allergies` |
| Assertions | `present`, `negated`, `historical`, `hypothetical`, `family` |
| Combined | `medications_present`, `diagnoses_negated`, `lab_tests_present`, etc. |

### Medications filters

```bash
# Notes where metformin is currently prescribed
trioexplorer search "diabetes control" \
  --entity-filters '{"medications_present": ["metformin"]}'

# Multiple medications (OR within field)
trioexplorer search "pain management" \
  --entity-filters '{"medications_present": ["oxycodone", "hydrocodone", "tramadol"]}'

# Biologics for asthma
trioexplorer search "asthma exacerbation" \
  --entity-filters '{"medications_present": ["Dupixent", "Nucala", "Fasenra"]}'
```

### Lab tests filters

```bash
# Notes mentioning A1C
trioexplorer search "glycemic control" \
  --entity-filters '{"lab_tests": ["A1C", "hemoglobin A1c"]}'

# Kidney function labs
trioexplorer search "renal function" \
  --entity-filters '{"lab_tests_present": ["creatinine", "BUN", "GFR"]}'

# Liver function panel
trioexplorer search "hepatotoxicity" \
  --entity-filters '{"lab_tests": ["AST", "ALT", "bilirubin"]}'
```

### Vitals filters

```bash
# Blood pressure mentions
trioexplorer search "hypertension management" \
  --entity-filters '{"vitals": ["blood pressure", "BP", "systolic"]}'

# Respiratory vitals
trioexplorer search "respiratory distress" \
  --entity-filters '{"vitals_present": ["oxygen saturation", "SpO2", "respiratory rate"]}'
```

### Combining filters (AND logic between fields)

```bash
# Medication AND diagnosis
trioexplorer search "treatment efficacy" \
  --entity-filters '{"medications_present": ["metformin"], "diagnoses_present": ["diabetes"]}'

# Medication AND lab monitoring
trioexplorer search "drug monitoring" \
  --entity-filters '{"medications_present": ["warfarin"], "lab_tests": ["INR"]}'
```

## Discovering Filter Values

Check what entities are indexed before filtering:

```bash
# List available filter fields for a cohort
trioexplorer list filters --namespace "v2-cohort-COHORT_ID-arctic"

# List medication values
trioexplorer list filters --namespace "v2-cohort-COHORT_ID-arctic" --field medications --limit 100

# Search for specific medication
trioexplorer list filters --namespace "v2-cohort-COHORT_ID-arctic" --field medications -o csv | grep -i "metformin"
```

## Fallback: Query-based filtering

If an entity isn't indexed, include it in the search query:

```bash
# Instead of entity filter, include medication in query
trioexplorer search "dupixent lack of efficacy" --cohort-ids COHORT_ID -d patient -k 10
```

## Task: $ARGUMENTS
