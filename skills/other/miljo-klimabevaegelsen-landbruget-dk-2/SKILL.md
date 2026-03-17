---
name: gcs-miljo-data
description: |
  Activates when querying environmental data from GCS.
  Use this skill for: pesticides, nitrogen leaching, BNBO drinking water protection,
  wetlands, soil types, environmental compliance, biodiversity.
  Keywords: miljø, environment, pesticide, pesticid, nitrogen, kvælstof, BNBO, wetlands, vådomr, soil, jord, biodiversity
---

# GCS Miljø (Environment) Data Catalog

Environmental data including pesticides, nitrogen leaching, protected areas, and soil.

## Frontend Metrics Supported

| Metric Key | Danish Name | Description |
|------------|-------------|-------------|
| `pesticide_burden` | Pesticidbelastning | Total pesticide load |
| `pesticide_pfas` | PFAS i pesticider | PFAS-containing pesticides |
| `pesticide_glyphosate` | Glyphosat | Glyphosate usage |
| `nitrogen_leaching` | Kvælstofudvaskning | Nitrogen leaching estimates |
| `bnbo_overlap` | BNBO-overlap | Fields overlapping drinking water areas |
| `protected_nature` | Beskyttet natur | Protected nature areas |
| `environmental_compliance` | Miljøoverholdelse | Environmental compliance rate |
| `biodiversity_score` | Biodiversitet | Biodiversity indicators |

## Available Datasets

### Silver Layer

#### Pesticides (316K rows)
**Path**: `gs://$GCS_BUCKET/silver/pesticides/*/data.parquet`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| cvr_number | string | Company CVR | 31373077 |
| pesticide_name | string | Pesticide product name | Roundup |
| active_ingredient | string | Active chemical | Glyphosate |
| dosage_quantity | float | Amount applied | 2.5 |
| dosage_unit | string | Unit of measure | L/ha |
| application_date | date | Date applied | 2024-05-15 |
| crop_type | string | Target crop | Hvede |

#### BNBO Status (5.4K rows)
**Path**: `gs://$GCS_BUCKET/silver/bnbo_status/*/data.parquet`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| geometry | binary | Protection zone polygon (WKB) | - |
| area_ha | float | Zone area in hectares | 45.2 |
| temanavn | string | Theme name | BNBO |
| status_bnbo | string | BNBO status | Indsatsplan vedtaget |
| kommunenav | string | Municipality name | København |
| anlaegsnav | string | Water facility name | Vandværk Nord |
| dgunr | string | DGU number (well ID) | 123.456 |

**Schema (introspected)**:
```
geometry: binary (WKB)
area_ha: double
temanavn: string
status_bnbo: string
kommunenav: string
anlaegsnav: string
dgunr: string
[30 columns total]
```

#### Wetlands (1.7M rows)
**Path**: `gs://$GCS_BUCKET/silver/wetlands/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| id | int64 | Wetland polygon ID |
| gridcode | int | Grid classification code |
| toerv_pct | float | Peat percentage |
| geometry | binary | Wetland polygon (WKB) |

#### Soil Types
**Path**: `gs://$GCS_BUCKET/silver/soil_types/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| geometry | binary | Soil type polygon (WKB) |
| soil_code | string | Soil classification code |
| soil_description | string | Soil type description |
| clay_content | float | Clay percentage |

#### Slurry Leaks (Incidents)
**Path**: `gs://$GCS_BUCKET/silver/slurry leaks/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| incident_date | date | Date of leak |
| location | binary | Incident location (WKB) |
| volume_m3 | float | Volume of spill |
| cvr_number | string | Responsible company |

### Gold Layer

#### Pesticide Disaggregation (1.52M rows)
**Path**: `gs://$GCS_BUCKET/gold/pesticide_disaggregation_{year}/*/data.parquet`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| DisaggregatedID | int64 | Unique record ID | 12345678 |
| cvr_number | string | Company CVR | 31373077 |
| PesticideName | string | Pesticide name | Roundup Bio |
| PesticideRegistrationNumber | string | Registration number | 1-234 |
| DosageQuantity | float | Dosage amount | 2.5 |
| DosageUnit | string | Dosage unit | L/ha |
| MatchedFieldID | string | Matched field ID | 610341-27-1-0 |
| MatchedBlockID | string | Matched block ID | 610341-27 |
| AllocatedArea | float | Area allocated (ha) | 5.2 |
| field_uuid | string | Field UUID | - |
| municipality | string | Municipality code | 0101 |

**Schema (introspected)**:
```
DisaggregatedID: int64
cvr_number: string
PesticideName: string
PesticideRegistrationNumber: string
DosageQuantity: double
DosageUnit: string
MatchedFieldID: string
MatchedBlockID: string
AllocatedArea: double
field_uuid: string
municipality: string
[17 columns total]
```

#### NLES5 Nitrogen Estimates (500K rows)
**Path**: `gs://$GCS_BUCKET/gold/nles5_nitrogen_{year}/*/data.parquet`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| field_id | string | Field identifier | 610341-27-1-0 |
| field_uuid | string | Field UUID | - |
| block_id | string | Block identifier | 610341-27 |
| cvr_number | string | Company CVR | 31373077 |
| year | int | Estimate year | 2024 |
| area_ha | float | Field area | 12.45 |
| crop_type | string | Crop grown | Vårbyg |
| soil_code | string | Soil classification | JB3 |
| soil_description | string | Soil type name | Lerblandet sandjord |
| clay_content | float | Clay percentage | 15.2 |
| nitrogen_washout_kg_ha | float | N leaching kg/ha | 42.5 |
| percolation_mm | float | Water percolation mm | 285.0 |
| data_quality_score | float | Quality indicator | 0.85 |

**Schema (introspected)**:
```
field_id: string
field_uuid: string
block_id: string
cvr_number: string
year: int64
area_ha: double
crop_type: string
soil_code: string
soil_description: string
clay_content: double
nitrogen_washout_kg_ha: double
percolation_mm: double
data_quality_score: double
[20 columns total]
```

#### Field Intersections (Environmental Overlaps)
**Path**: `gs://$GCS_BUCKET/gold/field_analysis_{year}_intersections_*/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| field_id | string | Field identifier |
| bnbo_overlap_ha | float | Area overlapping BNBO |
| wetland_overlap_ha | float | Area overlapping wetlands |
| natura2000_overlap_ha | float | Area overlapping Natura 2000 |

## Common Queries

### Get Pesticide Usage by CVR
```python
import pyarrow.parquet as pq
from google.cloud import storage
import io

client = storage.Client()
bucket = client.bucket('$GCS_BUCKET')

# Read pesticide disaggregation data
blob = bucket.blob('gold/pesticide_disaggregation_2024/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
df = pq.read_table(buffer).to_pandas()

# Filter by CVR
company_pesticides = df[df['cvr_number'] == '31373077']
print(f"Total pesticide records: {len(company_pesticides)}")
print(f"Unique pesticides used: {company_pesticides['PesticideName'].nunique()}")

# Summarize by pesticide
usage_summary = company_pesticides.groupby('PesticideName').agg({
    'DosageQuantity': 'sum',
    'AllocatedArea': 'sum'
}).reset_index()
```

### Find Fields in BNBO Protection Zones
```python
import geopandas as gpd

# Read BNBO zones
blob = bucket.blob('silver/bnbo_status/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
bnbo = gpd.read_parquet(buffer)
bnbo = bnbo.set_crs('EPSG:4326')

# Read field boundaries
blob = bucket.blob('silver/fvm_marker_2024/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
fields = gpd.read_parquet(buffer)
fields = fields.set_crs('EPSG:4326')

# Spatial join to find overlapping fields
fields_in_bnbo = gpd.sjoin(fields, bnbo, how='inner', predicate='intersects')
print(f"Fields overlapping BNBO zones: {len(fields_in_bnbo)}")
```

### Calculate Nitrogen Leaching by Municipality
```python
# Read nitrogen data
blob = bucket.blob('gold/nles5_nitrogen_2024/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
nitrogen = pq.read_table(buffer).to_pandas()

# Read field data with municipality
blob = bucket.blob('silver/fvm_marker_2024/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
fields = pq.read_table(buffer).to_pandas()

# Join and aggregate
nitrogen_with_muni = nitrogen.merge(
    fields[['field_id', 'municipality']],
    on='field_id',
    how='left'
)

muni_stats = nitrogen_with_muni.groupby('municipality').agg({
    'nitrogen_washout_kg_ha': 'mean',
    'area_ha': 'sum'
}).reset_index()
muni_stats.columns = ['municipality', 'avg_n_leaching', 'total_area']
```

### Glyphosate Usage Analysis
```python
# Filter for glyphosate products
glyphosate = df[
    df['PesticideName'].str.contains('glyph|roundup', case=False, na=False)
]

# Summarize by municipality
glyph_by_muni = glyphosate.groupby('municipality').agg({
    'DosageQuantity': 'sum',
    'AllocatedArea': 'sum'
}).reset_index()

# Calculate intensity
glyph_by_muni['dose_per_ha'] = glyph_by_muni['DosageQuantity'] / glyph_by_muni['AllocatedArea']
```

### Wetland Overlap Analysis
```python
import geopandas as gpd

# Read wetlands
blob = bucket.blob('silver/wetlands/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
wetlands = gpd.read_parquet(buffer)
wetlands = wetlands.set_crs('EPSG:4326')

# High peat content areas
high_peat = wetlands[wetlands['toerv_pct'] > 50]
print(f"High peat wetland polygons: {len(high_peat)}")
```

## Join Keys

| This Dataset | Join Column | Target Dataset | Target Column |
|--------------|-------------|----------------|---------------|
| pesticide_disaggregation | cvr_number | subsidies | cvr_number |
| pesticide_disaggregation | MatchedFieldID | fvm_marker | field_id |
| pesticide_disaggregation | field_uuid | field_production | field_uuid |
| nles5_nitrogen | field_id | fvm_marker | field_id |
| nles5_nitrogen | cvr_number | subsidies | cvr_number |
| bnbo_status | geometry | fvm_marker | geometry (spatial) |
| wetlands | geometry | fvm_marker | geometry (spatial) |

## Data Quality Notes

### Pesticide Disaggregation
- **Update frequency**: Annual (after reporting deadline)
- **Coverage**: Disaggregated to field level from company-level reports
- **Caveat**: Allocation is modeled based on crop types

### NLES5 Nitrogen
- **Update frequency**: Annual
- **Model**: NLES5 model output from Aarhus University
- **Coverage**: All agricultural fields
- **Quality**: data_quality_score indicates confidence

### BNBO Status
- **Update frequency**: Quarterly
- **Coverage**: All designated drinking water protection zones
- **Source**: Danish EPA (Miljøstyrelsen)

### Wetlands
- **Update frequency**: Annual
- **Source**: Danish Environmental Portal
- **Note**: toerv_pct indicates peat soil percentage

## Related Skills

- **landbrugsareal/** - Field boundaries for spatial joins
- **okonomi/** - Subsidies potentially affected by environmental compliance
- **husdyr/** - Livestock density affecting nitrogen loading
- **medarbejdere/** - Environmental compliance inspections

## GCS Paths Reference

```bash
# List pesticide disaggregation years
gsutil ls gs://$GCS_BUCKET/gold/ | grep pesticide

# List NLES5 nitrogen years
gsutil ls gs://$GCS_BUCKET/gold/ | grep nles5

# List BNBO status snapshots
gsutil ls gs://$GCS_BUCKET/silver/bnbo_status/

# List wetland data
gsutil ls gs://$GCS_BUCKET/silver/wetlands/

# List field intersection analyses
gsutil ls gs://$GCS_BUCKET/gold/ | grep intersections
```

## Spatial Analysis Tips

### CRS Handling
All geometry stored in EPSG:4326 (WGS84). For Danish projections:
```python
# Convert to Danish UTM
gdf = gdf.to_crs('EPSG:25832')

# Calculate areas in meters
gdf['area_m2'] = gdf.geometry.area
```

### Buffer Analysis
```python
# Create 100m buffer around BNBO zones
bnbo_buffered = bnbo.copy()
bnbo_buffered = bnbo_buffered.to_crs('EPSG:25832')  # UTM for meters
bnbo_buffered['geometry'] = bnbo_buffered.buffer(100)
bnbo_buffered = bnbo_buffered.to_crs('EPSG:4326')  # Back to WGS84
```
