---
name: gcs-data-catalog
description: |
  Activates when querying Danish agricultural data from GCS.
  Use this skill for: data discovery, finding datasets, understanding schemas,
  querying parquet files, joining datasets on CVR/CHR/BFE identifiers.
  Keywords: data, catalog, datasets, GCS, parquet, schema, query, DuckDB, pyarrow
---

# GCS Data Catalog - Master Index

This skill provides immediate access to Landbruget.dk's GCS data lake containing 18+ Danish agricultural datasets.

## Quick Access

**GCS Bucket**: Set via `GCS_BUCKET` environment variable (see `.env`)

**Medallion Architecture**:
- `bronze/` - Raw data exactly as received
- `silver/` - Cleaned, validated, standardized
- `gold/` - Analysis-ready, joined datasets

## Setup Code

```python
import os
import pyarrow.parquet as pq
from google.cloud import storage

# Initialize GCS client
client = storage.Client()
bucket_name = os.environ.get('GCS_BUCKET')  # Set in .env
bucket = client.bucket(bucket_name)

# Read parquet from GCS
def read_gcs_parquet(gcs_path: str):
    """Read parquet file from GCS path like 'silver/subsidies/*/data.parquet'"""
    import io
    blob = bucket.blob(gcs_path)
    buffer = io.BytesIO()
    blob.download_to_file(buffer)
    buffer.seek(0)
    return pq.read_table(buffer).to_pandas()
```

## Data Categories (Frontend-Aligned)

| Category | Danish Name | Skill Path | Key Join | Metrics |
|----------|-------------|------------|----------|---------|
| Finance | Økonomi | `gcs-data-catalog/okonomi/` | cvr_number | 3 |
| Agricultural Land | Landbrugsareal | `gcs-data-catalog/landbrugsareal/` | field_id, cvr_number | 4 |
| Environment | Miljø | `gcs-data-catalog/miljo/` | geometry, field_id | 8 |
| Livestock | Husdyr | `gcs-data-catalog/husdyr/` | chr_number | 6 |
| Employees | Medarbejdere | `gcs-data-catalog/medarbejdere/` | cvr_number | 5 |

## Key Identifiers

| Identifier | Format | Description | Validation |
|------------|--------|-------------|------------|
| **CVR** | 8 digits | Company registration number | `^\d{8}$` |
| **CHR** | 6 digits | Central Husbandry Register (herd ID) | `^\d{6}$` |
| **BFE** | Variable | Cadastral parcel number | varies |
| **field_id** | String | Field identifier from FVM | varies |
| **field_uuid** | UUID | Unique field identifier | UUID format |

## Dataset Quick Reference

### Økonomi (Finance)
| Dataset | Path | Rows | Key Columns |
|---------|------|------|-------------|
| Subsidies | `silver/subsidies/` | 554K | cvr_number, tilskudsberetigt |
| CVR Enrichment | `gold/cvr_enrichment/*/` | varies | cvr_number, company data |
| Property Owners | `silver/property_owners/` | 8.2M | CVRNummer, owner info |

### Landbrugsareal (Agricultural Land)
| Dataset | Path | Rows | Key Columns |
|---------|------|------|-------------|
| FVM Marker (fields) | `silver/fvm_marker_{year}/` | 617K/year | field_id, cvr_number, crop_code, geometry |
| Field Production | `gold/field_production_{year}/` | 617K/year | field_id, yield_estimate, crop_type |
| Agricultural Blocks | `silver/agricultural_blocks_{year}/` | varies | block_id, geometry |
| Cadastral | `silver/cadastral/` | 2.16M | bfe_number, geometry |

### Miljø (Environment)
| Dataset | Path | Rows | Key Columns |
|---------|------|------|-------------|
| Pesticide Disaggregation | `gold/pesticide_disaggregation_{year}/` | 1.52M | cvr_number, PesticideName, DosageQuantity |
| NLES5 Nitrogen | `gold/nles5_nitrogen_*/` | 500K | field_id, nitrogen_washout_kg_ha |
| BNBO Status | `silver/bnbo_status/` | 5.4K | geometry, status_bnbo |
| Wetlands | `silver/wetlands/` | 1.7M | geometry, toerv_pct |

### Husdyr (Livestock)
| Dataset | Path | Rows | Key Columns |
|---------|------|------|-------------|
| Svineflytning | `silver/svineflytning/*/movements.parquet` | 1.27M | sender_chr_number, receiver_chr_number, total_animals |
| CHR Movements | `bronze/chr/*/chr_dyr_movement_summaries.parquet` | 124K | reporting_herd_number, animal_count |
| Animal Welfare | `silver/animal welfare/` | varies | chr_number |

### Medarbejdere (Employees)
| Dataset | Path | Rows | Key Columns |
|---------|------|------|-------------|
| Arbejdstilsynet | `gold/arbejdstilsynet_inspections/` | 536 | cvr_number, decision, severity_score |
| Work Permits | `silver/work permits/` | varies | cvr_number |
| Worker Safety | `silver/worker safety/` | varies | cvr_number |

## Common Queries

### List Available Years for a Dataset
```bash
gsutil ls gs://$GCS_BUCKET/silver/fvm_marker_*/
```

### Check Dataset Schema
```python
import os
import pyarrow.parquet as pq
from google.cloud import storage
import io

client = storage.Client()
bucket_name = os.environ.get('GCS_BUCKET')
bucket = client.bucket(bucket_name)

# Get first parquet file and read schema
blob = bucket.blob('silver/subsidies/2025-01-10T00:00:26.377177/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
schema = pq.read_schema(buffer)
print(schema)
```

### Query Specific CVR
```python
df = read_gcs_parquet('silver/subsidies/2025-01-10T00:00:26.377177/data.parquet')
company_data = df[df['cvr_number'] == '31373077']
```

## Cross-Dataset Joins

### CVR-based joins (most common)
```python
# Join subsidies with pesticides on CVR
subsidies = read_gcs_parquet('silver/subsidies/*/data.parquet')
pesticides = read_gcs_parquet('gold/pesticide_disaggregation_2024/*/data.parquet')
merged = subsidies.merge(pesticides, on='cvr_number', how='inner')
```

### Field-based joins
```python
# Join field production with nitrogen estimates
field_prod = read_gcs_parquet('gold/field_production_2024/*/data.parquet')
nitrogen = read_gcs_parquet('gold/nles5_nitrogen_2024/*/data.parquet')
merged = field_prod.merge(nitrogen, on=['field_id', 'cvr_number'], how='inner')
```

### CHR-based joins
```python
# Join movements with animal welfare
movements = read_gcs_parquet('silver/svineflytning/*/movements.parquet')
welfare = read_gcs_parquet('silver/animal welfare/*/data.parquet')
# Join on sender or receiver CHR
```

## Data Update Schedule

| Layer | Frequency | Notes |
|-------|-----------|-------|
| Bronze | Weekly (Mondays 2AM UTC) | Immutable, timestamped |
| Silver | After bronze update | Cleaned, validated |
| Gold | After silver update | Analysis-ready |

## Related Skills

- **okonomi/** - Financial data: subsidies, property values
- **landbrugsareal/** - Field and crop data: FVM marker, production
- **miljo/** - Environmental data: pesticides, nitrogen, BNBO
- **husdyr/** - Livestock data: CHR, movements, welfare
- **medarbejdere/** - Employee data: inspections, safety

## Troubleshooting

### Authentication
```bash
# Check GCS access
gcloud auth application-default login
gsutil ls gs://$GCS_BUCKET/
```

### Large Files
For datasets > 1GB, use DuckDB or chunked reading:
```python
import duckdb
# Query directly without loading into memory
result = duckdb.query("""
    SELECT cvr_number, SUM(area_ha) as total_area
    FROM 'gs://$GCS_BUCKET/gold/field_production_2024/*/data.parquet'
    GROUP BY cvr_number
""").df()
```

### CRS Conversion
All geometry is stored in EPSG:4326 (WGS84). For Danish coordinates (EPSG:25832):
```python
import geopandas as gpd
gdf = gdf.to_crs('EPSG:25832')  # Convert to UTM 32N
```
