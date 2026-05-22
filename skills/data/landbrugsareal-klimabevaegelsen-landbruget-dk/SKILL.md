---
name: gcs-landbrugsareal-data
description: |
  Activates when querying agricultural land and field data from GCS.
  Use this skill for: field boundaries, crop data, land use, organic farming,
  production estimates, cadastral data, agricultural blocks, building data.
  Keywords: landbrugsareal, field, mark, marker, crop, afgrøde, organic, økologisk, production, areal, cadastral, matrikel
---

# GCS Landbrugsareal (Agricultural Land) Data Catalog

Field boundaries, crop data, land use, and agricultural production data.

## Frontend Metrics Supported

| Metric Key | Danish Name | Description |
|------------|-------------|-------------|
| `land_use` | Arealanvendelse | Land use categories |
| `organic_farming` | Økologisk areal | Organic farming area |
| `production` | Afgrødeproduktion | Crop production estimates |
| `crop_diversity` | Afgrødediversitet | Diversity of crops grown |

## Available Datasets

### Silver Layer

#### FVM Marker - Field Boundaries (617K rows/year)
**Path**: `gs://$GCS_BUCKET/silver/fvm_marker_{year}/*/data.parquet`
**Years Available**: 2008-2025

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| field_id | string | Unique field identifier | 610341-27-1-0 |
| area_ha | float | Field area in hectares | 12.45 |
| cvr_number | string | Company CVR (8 digits) | 31373077 |
| crop_code | int | Crop type code | 1 |
| crop_name | string | Crop type name | Vårbyg |
| block_id | string | Agricultural block ID | 610341-27 |
| geometry | binary | Field polygon (WKB, EPSG:4326) | - |
| year | int | Data year | 2024 |
| field_uuid | string | UUID for field | - |
| municipality | string | Municipality code | 0101 |
| is_organic | bool | Organic certification | true |
| organic_conversion_date | date | Date of organic conversion | 2020-01-15 |

**Schema (introspected)**:
```
field_id: string
area_ha: double
cvr_number: string
crop_code: int64
crop_name: string
block_id: string
geometry: binary (WKB)
year: int64
field_uuid: string
municipality: string
is_organic: bool
organic_conversion_date: date32
[20 columns total]
```

#### Agricultural Blocks
**Path**: `gs://$GCS_BUCKET/silver/agricultural_blocks_{year}/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| block_id | string | Block identifier |
| geometry | binary | Block polygon (WKB) |
| total_area_ha | float | Total block area |

#### Cadastral (2.16M rows)
**Path**: `gs://$GCS_BUCKET/silver/cadastral/*/data.parquet`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| bfe_number | int64 | Cadastral parcel ID | 1234567 |
| business_event | string | Last registration event | - |
| registration_from | timestamp | Registration date | - |
| is_worker_housing | bool | Worker housing flag | false |
| is_common_lot | bool | Common lot flag | false |
| agricultural_notation | string | Agricultural notation | - |
| geometry | binary | Parcel polygon (WKB) | - |

#### BBR Buildings (579K rows)
**Path**: `gs://$GCS_BUCKET/silver/bbr_buildings/*/joined_buildings.parquet`

| Column | Type | Description |
|--------|------|-------------|
| building_uuid | string | Unique building ID |
| geo_building_polygon | binary | Building footprint (WKB) |
| geo_building_centroid | binary | Building center point |
| building_type | string | Building type code |
| building_floor_area_sqm | float | Floor area in m² |
| building_usage_category | string | Usage category |
| current_use | string | Current use description |
| address | string | Building address |

#### DAGI Kommuner (99 rows)
**Path**: `gs://$GCS_BUCKET/silver/dagi_kommuner/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| code | string | Municipality code |
| name | string | Municipality name |
| region_code | string | Region code |
| geometry | binary | Municipality polygon (WKB) |
| area_m2 | float | Area in m² |
| centroid_x | float | Centroid longitude |
| centroid_y | float | Centroid latitude |

### Gold Layer

#### Field Production (617K rows/year)
**Path**: `gs://$GCS_BUCKET/gold/field_production_{year}/*/data.parquet`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| field_id | string | Field identifier | 610341-27-1-0 |
| block_id | string | Block identifier | 610341-27 |
| cvr_number | string | Company CVR | 31373077 |
| year | int | Production year | 2024 |
| area_ha | float | Field area | 12.45 |
| crop_type | string | Crop type name | Vårbyg |
| organic_farming | bool | Organic flag | true |
| landsdel_code | string | Region code | - |
| landsdel_name | string | Region name | Nordjylland |
| dst_regions | string | DST region classification | - |
| kommune_name | string | Municipality name | København |
| yield_estimate_hkg_ha | float | Yield estimate hkg/ha | 52.3 |
| production_estimate_hkg | float | Total production hkg | 651.14 |
| field_uuid | string | UUID | - |
| primary_field_id | string | Primary field reference | - |

**Schema (introspected)**:
```
field_id: string
block_id: string
cvr_number: string
year: int64
area_ha: double
crop_type: string
organic_farming: bool
landsdel_code: string
landsdel_name: string
dst_regions: string
kommune_name: string
yield_estimate_hkg_ha: double
production_estimate_hkg: double
field_uuid: string
primary_field_id: string
[18 columns total]
```

## Common Queries

### Get All Fields for a CVR
```python
import pyarrow.parquet as pq
from google.cloud import storage
import io

client = storage.Client()
bucket = client.bucket('$GCS_BUCKET')

# Read FVM marker data for 2024
blob = bucket.blob('silver/fvm_marker_2024/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
df = pq.read_table(buffer).to_pandas()

# Filter by CVR
company_fields = df[df['cvr_number'] == '31373077']
print(f"Total fields: {len(company_fields)}")
print(f"Total area: {company_fields['area_ha'].sum():.2f} ha")
```

### Calculate Organic Farming Percentage by Municipality
```python
# Group by municipality and organic status
organic_stats = df.groupby(['municipality', 'is_organic']).agg({
    'area_ha': 'sum'
}).unstack(fill_value=0)

organic_stats.columns = ['conventional', 'organic']
organic_stats['organic_pct'] = (
    organic_stats['organic'] /
    (organic_stats['conventional'] + organic_stats['organic']) * 100
)
organic_stats = organic_stats.sort_values('organic_pct', ascending=False)
```

### Get Production Estimates for a Crop
```python
# Read gold production data
blob = bucket.blob('gold/field_production_2024/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
production = pq.read_table(buffer).to_pandas()

# Filter for wheat
wheat = production[production['crop_type'].str.contains('hvede', case=False)]
print(f"Total wheat area: {wheat['area_ha'].sum():.2f} ha")
print(f"Average yield: {wheat['yield_estimate_hkg_ha'].mean():.2f} hkg/ha")
print(f"Total production: {wheat['production_estimate_hkg'].sum():.2f} hkg")
```

### Crop Diversity Analysis
```python
# Count unique crops per CVR
crop_diversity = df.groupby('cvr_number').agg({
    'crop_name': 'nunique',
    'area_ha': 'sum'
}).reset_index()
crop_diversity.columns = ['cvr_number', 'crop_count', 'total_area']
crop_diversity = crop_diversity.sort_values('crop_count', ascending=False)
```

### Read Geometry with GeoPandas
```python
import geopandas as gpd
import io

# Read with geometry
blob = bucket.blob('silver/fvm_marker_2024/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)

# Read as GeoDataFrame
gdf = gpd.read_parquet(buffer)
gdf = gdf.set_crs('EPSG:4326')  # Set CRS if not set

# Plot a sample
gdf[gdf['cvr_number'] == '31373077'].plot()
```

## Join Keys

| This Dataset | Join Column | Target Dataset | Target Column |
|--------------|-------------|----------------|---------------|
| fvm_marker | cvr_number | subsidies | cvr_number |
| fvm_marker | field_id | field_production | field_id |
| fvm_marker | block_id | agricultural_blocks | block_id |
| fvm_marker | field_uuid | pesticide_disaggregation | field_uuid |
| fvm_marker | municipality | dagi_kommuner | code |
| field_production | field_id | nles5_nitrogen | field_id |
| cadastral | bfe_number | property_owners | bestemtFastEjendomBFENr |

## Data Quality Notes

### FVM Marker
- **Update frequency**: Annual (new year data released ~Q2)
- **Coverage**: All registered agricultural fields in Denmark
- **Years available**: 2008-2025 (varies by data source)
- **Geometry**: WKB format, EPSG:4326

### Field Production
- **Update frequency**: Annual after harvest statistics
- **Coverage**: Production estimates for all registered fields
- **Caveat**: Yield estimates are modeled, not measured

### Cadastral
- **Update frequency**: Weekly
- **Coverage**: All cadastral parcels in Denmark
- **Note**: Use for property boundaries, not field boundaries

## Related Skills

- **okonomi/** - Subsidies linked to fields via CVR and markbloknummer
- **miljo/** - Environmental data at field level (pesticides, nitrogen)
- **husdyr/** - Livestock density per land area

## GCS Paths Reference

```bash
# List available FVM marker years
gsutil ls gs://$GCS_BUCKET/silver/ | grep fvm_marker

# List field production years
gsutil ls gs://$GCS_BUCKET/gold/ | grep field_production

# List cadastral snapshots
gsutil ls gs://$GCS_BUCKET/silver/cadastral/

# List DAGI municipality data
gsutil ls gs://$GCS_BUCKET/silver/dagi_kommuner/
```

## Yearly Data Pattern

For datasets with yearly data, use this pattern:
```python
# Query specific year
year = 2024
path = f'silver/fvm_marker_{year}/*/data.parquet'

# Query all years (use with caution - large data)
path = 'silver/fvm_marker_*/*/data.parquet'
```
