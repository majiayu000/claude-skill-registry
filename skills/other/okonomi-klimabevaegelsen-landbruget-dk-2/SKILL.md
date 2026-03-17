---
name: gcs-okonomi-data
description: |
  Activates when querying financial/economic data from GCS.
  Use this skill for: subsidies, farm financials, property values, CVR enrichment,
  ownership data, støtte per hektar, samlet støtte, grundværdi.
  Keywords: økonomi, finance, subsidies, støtte, tilskud, CVR, property, ejendom, grundværdi
---

# GCS Økonomi (Finance) Data Catalog

Financial and economic data for Danish agricultural businesses.

## Frontend Metrics Supported

| Metric Key | Danish Name | Description |
|------------|-------------|-------------|
| `subsidy_per_ha` | Støtte per hektar | Subsidy amount per hectare |
| `total_subsidies` | Samlet støtte | Total subsidy amount |
| `land_value` | Grundværdi | Property/land value |

## Available Datasets

### Silver Layer

#### Subsidies (554K rows)
**Path**: `gs://$GCS_BUCKET/silver/subsidies/*/data.parquet`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| cvr_number | string | Company CVR (8 digits) | 31373077 |
| markbloknummer | string | Field block number | 610341-27 |
| marknummer | string | Field number | 1-0 |
| afg_kode_navn | string | Crop code and name | 1 - Vårbyg |
| imkareal | float | Declared area (ha) | 12.45 |
| ansoegtha_grundbet | float | Applied area basic | 12.45 |
| tilskudsberetha_grundbet | float | Eligible area basic | 12.45 |
| grundbetaling_dkk | float | Basic payment DKK | 2500.00 |
| oeko_tilskud_dkk | float | Organic subsidy DKK | 1500.00 |
| pleje_af_graes_dkk | float | Grassland care DKK | 500.00 |

**Schema (introspected)**:
```
cvr_number: string
markbloknummer: string
marknummer: string
afg_kode_navn: string
imkareal: double
ansoegtha_grundbet: double
tilskudsberetha_grundbet: double
[28 columns total - multiple subsidy types]
```

#### Property Owners (8.2M rows)
**Path**: `gs://$GCS_BUCKET/silver/property_owners/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| bestemtFastEjendomBFENr | int64 | BFE number (cadastral ID) |
| ejendePerson | struct | Person owner info (nested) |
| ejendeVirksomhed | struct | Company owner info (nested) |
| ejendeVirksomhed.CVRNummer | string | Owner's CVR number |

**Nested Structure**:
```
bestemtFastEjendomBFENr: int64
ejendePerson:
  - Beskyttelser: list
  - Navn: struct
  - Standardadresse: struct
ejendeVirksomhed:
  - CVRNummer: string
  - beliggenhedsadresse: struct
```

### Gold Layer

#### CVR Enrichment
**Path**: `gs://$GCS_BUCKET/gold/cvr_enrichment/*/`

Contains multiple enrichment files:
- `address_geocoding.parquet` - Geocoded company addresses
- `company_summary.parquet` - Aggregated company data

| Column | Type | Description |
|--------|------|-------------|
| cvr_number | string | Company CVR |
| latitude | float | Company location lat |
| longitude | float | Company location lon |
| total_area_ha | float | Total farmed area |
| employee_count | int | Number of employees |

## Common Queries

### Get Total Subsidies by CVR
```python
import pyarrow.parquet as pq
from google.cloud import storage
import io

client = storage.Client()
bucket = client.bucket('$GCS_BUCKET')

# Read subsidies
blob = bucket.blob('silver/subsidies/2025-01-10T00:00:26.377177/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
df = pq.read_table(buffer).to_pandas()

# Calculate total subsidies per CVR
totals = df.groupby('cvr_number').agg({
    'grundbetaling_dkk': 'sum',
    'oeko_tilskud_dkk': 'sum',
    'imkareal': 'sum'
}).reset_index()

# Add subsidy per hectare
totals['subsidy_per_ha'] = (
    totals['grundbetaling_dkk'] + totals['oeko_tilskud_dkk']
) / totals['imkareal']
```

### Find Property Owner by CVR
```python
# Read property owners
blob = bucket.blob('silver/property_owners/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
df = pq.read_table(buffer).to_pandas()

# Filter by CVR (need to handle nested structure)
import pandas as pd

# Extract CVR from nested structure
df['owner_cvr'] = df['ejendeVirksomhed'].apply(
    lambda x: x.get('CVRNummer') if x else None
)
company_properties = df[df['owner_cvr'] == '31373077']
```

### Subsidies for Specific Field Block
```python
# Get all subsidies for a markblok
field_block_subsidies = df[df['markbloknummer'] == '610341-27']
print(f"Total area: {field_block_subsidies['imkareal'].sum():.2f} ha")
print(f"Total basic payment: {field_block_subsidies['grundbetaling_dkk'].sum():.2f} DKK")
```

### Calculate Municipal Subsidy Statistics
```python
# Join with municipality data for geographic aggregation
# Requires joining with field data that has municipality info
from gcs_data_catalog.landbrugsareal import read_field_data

fields = read_field_data(year=2024)
subsidies_with_geo = df.merge(
    fields[['markbloknummer', 'municipality']],
    on='markbloknummer',
    how='left'
)

municipal_stats = subsidies_with_geo.groupby('municipality').agg({
    'grundbetaling_dkk': 'sum',
    'imkareal': 'sum'
}).reset_index()
```

## Join Keys

| This Dataset | Join Column | Target Dataset | Target Column |
|--------------|-------------|----------------|---------------|
| subsidies | cvr_number | field_production | cvr_number |
| subsidies | markbloknummer | fvm_marker | block_id |
| property_owners | bestemtFastEjendomBFENr | cadastral | bfe_number |
| property_owners | ejendeVirksomhed.CVRNummer | subsidies | cvr_number |

## Data Quality Notes

### Subsidies
- **Update frequency**: Annual (after payment year closes)
- **Coverage**: All EU agricultural subsidy recipients in Denmark
- **Caveat**: Some CVR numbers may be inactive/closed companies

### Property Owners
- **Update frequency**: Weekly
- **Coverage**: All registered property owners in Denmark
- **Caveat**: Nested JSON structure requires careful handling
- **Privacy**: Personal owner data (ejendePerson) may have restrictions

## Related Skills

- **landbrugsareal/** - Field boundaries for geographic context
- **miljo/** - Environmental compliance affecting subsidies
- **husdyr/** - Livestock data for animal-based subsidies
- **medarbejdere/** - Employee data for labor cost analysis

## GCS Paths Reference

```bash
# List available subsidy snapshots
gsutil ls gs://$GCS_BUCKET/silver/subsidies/

# List CVR enrichment data
gsutil ls gs://$GCS_BUCKET/gold/cvr_enrichment/

# List property owner snapshots
gsutil ls gs://$GCS_BUCKET/silver/property_owners/
```
