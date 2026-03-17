---
name: gcs-husdyr-data
description: |
  Activates when querying livestock and animal data from GCS.
  Use this skill for: CHR registry, pig movements, animal welfare, antibiotics,
  animal density, mortality rates, herd tracking, svineflytning.
  Keywords: husdyr, livestock, animal, dyr, CHR, svin, pig, ko, cattle, antibiotika, dyrevelfærd, flytning, movement
---

# GCS Husdyr (Livestock) Data Catalog

Livestock data including animal movements, welfare inspections, and herd tracking.

## Frontend Metrics Supported

| Metric Key | Danish Name | Description |
|------------|-------------|-------------|
| `antibiotic_usage` | Antibiotikaforbrug | Antibiotic consumption per animal |
| `animal_density` | Husdyrtæthed | Livestock units per hectare |
| `animal_welfare_violations` | Dyrevelfærdsovertrædelser | Welfare inspection violations |
| `livestock_units` | Dyreenheder | Total livestock units (DE) |
| `pig_movements` | Svinetransporter | Pig transport movements |
| `mortality_rate` | Dødelighed | Animal mortality rate |

## Key Identifier: CHR Number

**CHR (Central Husbandry Register)** is the primary identifier for livestock operations.
- **Format**: 6 digits (e.g., `123456`)
- **Validation**: `^\d{6}$`
- **Note**: One CVR can have multiple CHR numbers (multiple herds/locations)

## Available Datasets

### Silver Layer

#### Svineflytning Movements (1.27M rows)
**Path**: `gs://$GCS_BUCKET/silver/svineflytning/*/movements.parquet`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| movement_id | string | Unique movement ID | MVT-2024-123456 |
| movement_date | date | Date of transport | 2024-05-15 |
| sender_chr_number | int64 | Sender herd CHR | 123456 |
| sender_herd_number | string | Sender herd sub-ID | 1 |
| sender_address | string | Sender address | Gårdvej 1, 1234 By |
| sender_municipality_code | string | Sender municipality | 0101 |
| receiver_chr_number | int64 | Receiver herd CHR | 654321 |
| receiver_herd_number | string | Receiver herd sub-ID | 2 |
| receiver_address | string | Receiver address | Markstien 5, 5678 By |
| receiver_municipality_code | string | Receiver municipality | 0201 |
| total_animals | int | Total animals moved | 250 |
| sow_count | int | Number of sows | 0 |
| slaughter_pig_count | int | Slaughter pigs | 250 |
| piglet_count | int | Number of piglets | 0 |
| boar_count | int | Number of boars | 0 |
| vehicle_registration | string | Transport vehicle | AB12345 |
| transport_duration_hours | float | Transport duration | 2.5 |
| distance_km | float | Transport distance | 45.2 |

**Schema (introspected)**:
```
movement_id: string
movement_date: date32
sender_chr_number: int64
sender_herd_number: string
sender_address: string
sender_municipality_code: string
receiver_chr_number: int64
receiver_herd_number: string
receiver_address: string
receiver_municipality_code: string
total_animals: int64
sow_count: int64
slaughter_pig_count: int64
piglet_count: int64
boar_count: int64
vehicle_registration: string
[51 columns total]
```

#### Animal Welfare Inspections
**Path**: `gs://$GCS_BUCKET/silver/animal welfare/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| chr_number | int64 | Herd CHR number |
| inspection_date | date | Date of inspection |
| inspection_type | string | Type of inspection |
| violations_found | int | Number of violations |
| violation_categories | list | Categories of violations |
| compliance_status | string | Overall compliance |
| follow_up_required | bool | Follow-up needed |

#### Animal Mortality
**Path**: `gs://$GCS_BUCKET/silver/animal mortality/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| chr_number | int64 | Herd CHR number |
| report_date | date | Mortality report date |
| animal_type | string | Type of animal |
| mortality_count | int | Number of deaths |
| mortality_rate_pct | float | Mortality percentage |
| cause_category | string | Cause of death category |

### Bronze Layer

#### CHR Movement Summaries (124K rows)
**Path**: `gs://$GCS_BUCKET/bronze/chr/*/chr_dyr_movement_summaries.parquet`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| reporting_herd_number | int64 | CHR number | 123456 |
| animal_type | string | Type of animal | Svin |
| period_start | date | Period start | 2024-01-01 |
| period_end | date | Period end | 2024-03-31 |
| animals_in | int | Animals received | 500 |
| animals_out | int | Animals sent | 450 |
| births | int | Animals born | 200 |
| deaths | int | Animals died | 30 |
| animal_count | int | End-of-period count | 720 |

**Schema (introspected)**:
```
reporting_herd_number: int64
animal_type: string
period_start: date32
period_end: date32
animals_in: int64
animals_out: int64
births: int64
deaths: int64
animal_count: int64
[11 columns total]
```

#### Antibiotic Usage
**Path**: `gs://$GCS_BUCKET/bronze/vetstat/*/antibiotic_usage.parquet`

| Column | Type | Description |
|--------|------|-------------|
| chr_number | int64 | Herd CHR number |
| prescription_date | date | Date of prescription |
| antibiotic_type | string | Type of antibiotic |
| dosage_amount | float | Amount prescribed |
| dosage_unit | string | Unit of measure |
| treatment_reason | string | Reason for treatment |

## Common Queries

### Track Pig Movements for a CHR
```python
import pyarrow.parquet as pq
from google.cloud import storage
import io

client = storage.Client()
bucket = client.bucket('$GCS_BUCKET')

# Read svineflytning movements
blob = bucket.blob('silver/svineflytning/2025-01-10/movements.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
df = pq.read_table(buffer).to_pandas()

chr_number = 123456

# Find all movements involving this CHR (as sender or receiver)
outgoing = df[df['sender_chr_number'] == chr_number]
incoming = df[df['receiver_chr_number'] == chr_number]

print(f"Outgoing movements: {len(outgoing)}, Animals sent: {outgoing['total_animals'].sum()}")
print(f"Incoming movements: {len(incoming)}, Animals received: {incoming['total_animals'].sum()}")
```

### Calculate Animal Density by Municipality
```python
# Get movement data to estimate animal counts
movements = df.groupby('receiver_municipality_code').agg({
    'total_animals': 'sum'
}).reset_index()

# Join with land area data (from landbrugsareal skill)
# to calculate animals per hectare
```

### Network Analysis: Farm-to-Farm Connections
```python
# Create network of farm connections
import networkx as nx

G = nx.DiGraph()

for _, row in df.iterrows():
    sender = row['sender_chr_number']
    receiver = row['receiver_chr_number']
    animals = row['total_animals']

    if G.has_edge(sender, receiver):
        G[sender][receiver]['weight'] += animals
    else:
        G.add_edge(sender, receiver, weight=animals)

# Find most connected farms
centrality = nx.degree_centrality(G)
top_farms = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
```

### Movement Patterns Over Time
```python
import pandas as pd

# Convert to datetime and aggregate by month
df['movement_month'] = pd.to_datetime(df['movement_date']).dt.to_period('M')

monthly_movements = df.groupby('movement_month').agg({
    'movement_id': 'count',
    'total_animals': 'sum'
}).reset_index()
monthly_movements.columns = ['month', 'movement_count', 'total_animals']
```

### Find High-Volume Transport Routes
```python
# Aggregate by sender-receiver municipality pairs
routes = df.groupby(['sender_municipality_code', 'receiver_municipality_code']).agg({
    'total_animals': 'sum',
    'movement_id': 'count'
}).reset_index()
routes.columns = ['from_muni', 'to_muni', 'total_animals', 'trips']

# Top routes
top_routes = routes.nlargest(10, 'total_animals')
```

### Slaughter Pig vs Breeding Stock Analysis
```python
# Calculate proportion of different animal types
df['pct_slaughter'] = df['slaughter_pig_count'] / df['total_animals'] * 100
df['pct_sows'] = df['sow_count'] / df['total_animals'] * 100
df['pct_piglets'] = df['piglet_count'] / df['total_animals'] * 100

# Movements by type
slaughter_movements = df[df['slaughter_pig_count'] > 0]
breeding_movements = df[df['sow_count'] > 0]
```

## Join Keys

| This Dataset | Join Column | Target Dataset | Target Column |
|--------------|-------------|----------------|---------------|
| svineflytning | sender_chr_number | chr_movements | reporting_herd_number |
| svineflytning | receiver_chr_number | chr_movements | reporting_herd_number |
| svineflytning | sender_municipality_code | dagi_kommuner | code |
| svineflytning | receiver_municipality_code | dagi_kommuner | code |
| animal_welfare | chr_number | chr_movements | reporting_herd_number |
| antibiotic_usage | chr_number | chr_movements | reporting_herd_number |

### Linking CHR to CVR

CHR numbers link to CVR through the CHR registry (separate lookup):
```python
# CHR to CVR mapping typically comes from:
# - bronze/chr/*/chr_bedrifter.parquet
# - Contains chr_number -> cvr_number mapping
```

## Data Quality Notes

### Svineflytning
- **Update frequency**: Daily/Weekly from Danish Veterinary Authority
- **Coverage**: All registered pig movements in Denmark
- **Lag**: ~1 week from actual movement to data availability
- **Completeness**: Mandatory reporting, high coverage

### CHR Movements
- **Update frequency**: Quarterly summaries
- **Coverage**: All registered herds
- **Note**: Summary data, not individual movements

### Animal Welfare
- **Update frequency**: After inspection completion
- **Coverage**: Risk-based inspection regime
- **Caveat**: Not all farms inspected every year

## Disease Tracing

The svineflytning data is critical for disease outbreak tracing:
```python
def trace_contacts(chr_number, df, days_back=21):
    """Find all farms that had contact with a CHR within time window."""
    # Get movement dates for this CHR
    outgoing = df[df['sender_chr_number'] == chr_number]
    incoming = df[df['receiver_chr_number'] == chr_number]

    if len(outgoing) == 0 and len(incoming) == 0:
        return []

    # Get date range
    all_dates = pd.concat([outgoing['movement_date'], incoming['movement_date']])
    max_date = all_dates.max()
    min_date = max_date - pd.Timedelta(days=days_back)

    # Filter to time window
    recent_out = outgoing[outgoing['movement_date'] >= min_date]
    recent_in = incoming[incoming['movement_date'] >= min_date]

    # Get contact CHRs
    contacts = set(recent_out['receiver_chr_number'].tolist())
    contacts.update(recent_in['sender_chr_number'].tolist())
    contacts.discard(chr_number)

    return list(contacts)
```

## Related Skills

- **landbrugsareal/** - Land area for animal density calculations
- **miljo/** - Environmental impact of livestock operations
- **okonomi/** - Subsidies related to animal production
- **medarbejdere/** - Agricultural worker data for livestock operations

## GCS Paths Reference

```bash
# List svineflytning snapshots
gsutil ls gs://$GCS_BUCKET/silver/svineflytning/

# List CHR data
gsutil ls gs://$GCS_BUCKET/bronze/chr/

# List animal welfare data
gsutil ls gs://$GCS_BUCKET/silver/animal\ welfare/

# List animal mortality data
gsutil ls gs://$GCS_BUCKET/silver/animal\ mortality/
```

## Note on CHR vs CVR

- **CHR** identifies a physical location/herd
- **CVR** identifies a legal entity (company)
- One CVR can own multiple CHR (multiple farms/herds)
- One CHR belongs to exactly one CVR
- Join using CHR registry lookup tables
