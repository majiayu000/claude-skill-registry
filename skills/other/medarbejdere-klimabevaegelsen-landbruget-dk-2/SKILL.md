---
name: gcs-medarbejdere-data
description: |
  Activates when querying employee and workplace safety data from GCS.
  Use this skill for: Arbejdstilsynet inspections, work permits, safety violations,
  workplace accidents, compliance rates, foreign workers, incident tracking.
  Keywords: medarbejdere, employees, worker, arbejdstilsynet, inspection, tilsyn, safety, arbejdsmiljø, accident, ulykke, compliance
---

# GCS Medarbejdere (Employees) Data Catalog

Employee and workplace safety data from regulatory inspections and incident reports.

## Frontend Metrics Supported

| Metric Key | Danish Name | Description |
|------------|-------------|-------------|
| `worker_safety_violations` | Arbejdsmiljøovertrædelser | Workplace safety violations |
| `foreign_workers` | Udenlandske arbejdere | Foreign worker registrations |
| `work_accidents` | Arbejdsulykker | Workplace accident count |
| `inspection_frequency` | Tilsynsfrekvens | Inspection frequency rate |
| `compliance_rate` | Overholdelsesrate | Overall compliance rate |

## Available Datasets

### Gold Layer

#### Arbejdstilsynet Inspections (536 rows)
**Path**: `gs://$GCS_BUCKET/gold/arbejdstilsynet_inspections/*/data.parquet`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| date | date | Inspection date | 2024-05-15 |
| case_count | int | Number of cases | 3 |
| decision | string | Inspection decision | Påbud |
| work_env_issue | string | Work environment issue | Ergonomi |
| cvr_number | string | Company CVR | 31373077 |
| company_name | string | Company name | Landbrugsbedrift A/S |
| industry | string | Industry classification | Landbrug |
| severity_score | float | Severity (0-10) | 7.5 |
| company_compliance_rate | float | Historical compliance (0-1) | 0.85 |
| is_repeat_offender | bool | Previous violations | false |
| inspector_id | string | Inspector identifier | AT-123 |
| follow_up_date | date | Follow-up scheduled | 2024-08-15 |
| fine_amount_dkk | float | Fine if applicable | 25000.0 |
| corrective_deadline | date | Deadline for correction | 2024-06-30 |

**Schema (introspected)**:
```
date: date32
case_count: int64
decision: string
work_env_issue: string
cvr_number: string
company_name: string
industry: string
severity_score: double
company_compliance_rate: double
is_repeat_offender: bool
inspector_id: string
follow_up_date: date32
fine_amount_dkk: double
corrective_deadline: date32
[29 columns total]
```

### Silver Layer

#### Work Permits
**Path**: `gs://$GCS_BUCKET/silver/work permits/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| cvr_number | string | Company CVR |
| permit_type | string | Type of permit |
| nationality | string | Worker nationality |
| issue_date | date | Permit issue date |
| expiry_date | date | Permit expiry date |
| worker_count | int | Number of workers |

#### Worker Safety Reports
**Path**: `gs://$GCS_BUCKET/silver/worker safety/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| cvr_number | string | Company CVR |
| report_date | date | Report date |
| incident_type | string | Type of incident |
| injury_severity | string | Severity level |
| days_lost | int | Workdays lost |
| body_part_affected | string | Injured body part |
| activity_during | string | Activity at time |

#### Stable Fires (Incidents)
**Path**: `gs://$GCS_BUCKET/silver/stable fires/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| incident_date | date | Date of fire |
| location | binary | Location (WKB) |
| farm_type | string | Type of farm |
| animals_affected | int | Animals impacted |
| cause | string | Fire cause |
| damage_estimate_dkk | float | Estimated damage |

#### Transport Accidents
**Path**: `gs://$GCS_BUCKET/silver/transportation accidents/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| incident_date | date | Accident date |
| location | binary | Location (WKB) |
| vehicle_type | string | Type of vehicle |
| cargo_type | string | Cargo description |
| injuries | int | Number injured |
| fatalities | int | Number of fatalities |

### Bronze Layer

#### DMA Permits
**Path**: `gs://$GCS_BUCKET/bronze/dma/*/data.parquet`

| Column | Type | Description |
|--------|------|-------------|
| cvr_number | string | Company CVR |
| permit_number | string | Permit ID |
| permit_type | string | Permit category |
| valid_from | date | Start date |
| valid_until | date | End date |
| conditions | string | Permit conditions |

## Common Queries

### Get Inspection History for CVR
```python
import pyarrow.parquet as pq
from google.cloud import storage
import io

client = storage.Client()
bucket = client.bucket('$GCS_BUCKET')

# Read arbejdstilsynet inspections
blob = bucket.blob('gold/arbejdstilsynet_inspections/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
df = pq.read_table(buffer).to_pandas()

# Filter by CVR
cvr = '31373077'
company_inspections = df[df['cvr_number'] == cvr]

print(f"Total inspections: {len(company_inspections)}")
print(f"Total cases: {company_inspections['case_count'].sum()}")
print(f"Average severity: {company_inspections['severity_score'].mean():.2f}")
print(f"Compliance rate: {company_inspections['company_compliance_rate'].iloc[-1]:.2%}")
```

### Calculate Industry Compliance Rates
```python
# Aggregate by industry
industry_stats = df.groupby('industry').agg({
    'cvr_number': 'nunique',
    'case_count': 'sum',
    'severity_score': 'mean',
    'company_compliance_rate': 'mean',
    'is_repeat_offender': 'sum'
}).reset_index()

industry_stats.columns = ['industry', 'companies', 'total_cases',
                          'avg_severity', 'avg_compliance', 'repeat_offenders']
industry_stats = industry_stats.sort_values('avg_compliance', ascending=True)
```

### Find Repeat Offenders
```python
# Companies with multiple violations
repeat_offenders = df[df['is_repeat_offender'] == True]

# Group by company
offender_summary = repeat_offenders.groupby(['cvr_number', 'company_name']).agg({
    'case_count': 'sum',
    'severity_score': 'mean',
    'fine_amount_dkk': 'sum'
}).reset_index()
offender_summary = offender_summary.sort_values('case_count', ascending=False)
```

### Severity Analysis by Issue Type
```python
# Analyze by work environment issue category
issue_analysis = df.groupby('work_env_issue').agg({
    'case_count': 'sum',
    'severity_score': 'mean',
    'fine_amount_dkk': 'sum'
}).reset_index()
issue_analysis = issue_analysis.sort_values('severity_score', ascending=False)
```

### Monthly Inspection Trends
```python
import pandas as pd

# Convert to datetime
df['inspection_month'] = pd.to_datetime(df['date']).dt.to_period('M')

monthly_stats = df.groupby('inspection_month').agg({
    'cvr_number': 'nunique',
    'case_count': 'sum',
    'severity_score': 'mean'
}).reset_index()
monthly_stats.columns = ['month', 'companies_inspected', 'total_cases', 'avg_severity']
```

### Calculate Fines by Municipality
```python
# Join with CVR address data for geographic analysis
# (requires joining with okonomi/cvr_enrichment data)
from gcs_data_catalog.okonomi import read_cvr_data

cvr_geo = read_cvr_data()
inspections_with_geo = df.merge(
    cvr_geo[['cvr_number', 'municipality']],
    on='cvr_number',
    how='left'
)

municipal_fines = inspections_with_geo.groupby('municipality').agg({
    'fine_amount_dkk': 'sum',
    'case_count': 'sum'
}).reset_index()
```

### Foreign Worker Analysis
```python
# Read work permits
blob = bucket.blob('silver/work permits/2025-01-10/data.parquet')
buffer = io.BytesIO()
blob.download_to_file(buffer)
buffer.seek(0)
permits = pq.read_table(buffer).to_pandas()

# Count by nationality
nationality_counts = permits.groupby('nationality').agg({
    'worker_count': 'sum'
}).reset_index()
nationality_counts = nationality_counts.sort_values('worker_count', ascending=False)

# Companies with most foreign workers
company_workers = permits.groupby('cvr_number').agg({
    'worker_count': 'sum'
}).reset_index()
company_workers = company_workers.sort_values('worker_count', ascending=False)
```

## Decision Types

| Decision (Danish) | English | Severity |
|-------------------|---------|----------|
| Påbud | Order/Requirement | Medium |
| Forbud | Prohibition | High |
| Vejledning | Guidance | Low |
| Afgørelse | Decision | Varies |
| Strakspåbud | Immediate Order | High |
| Rådgivningspåbud | Advisory Order | Medium |

## Work Environment Issues

Common categories in `work_env_issue`:
- **Ergonomi** - Ergonomic issues (lifting, posture)
- **Kemisk arbejdsmiljø** - Chemical hazards
- **Psykisk arbejdsmiljø** - Psychological work environment
- **Ulykker** - Accident prevention
- **Støj** - Noise exposure
- **Maskinsikkerhed** - Machine safety
- **Bygge og anlæg** - Construction safety

## Join Keys

| This Dataset | Join Column | Target Dataset | Target Column |
|--------------|-------------|----------------|---------------|
| arbejdstilsynet | cvr_number | subsidies | cvr_number |
| arbejdstilsynet | cvr_number | field_production | cvr_number |
| arbejdstilsynet | cvr_number | pesticide_disaggregation | cvr_number |
| work_permits | cvr_number | arbejdstilsynet | cvr_number |
| worker_safety | cvr_number | arbejdstilsynet | cvr_number |

## Data Quality Notes

### Arbejdstilsynet Inspections
- **Update frequency**: After inspection completion
- **Coverage**: All inspected agricultural businesses
- **Source**: Danish Working Environment Authority
- **Caveat**: Not all farms inspected - risk-based selection

### Work Permits
- **Update frequency**: Monthly
- **Coverage**: All registered foreign worker permits
- **Source**: SIRI (Danish Immigration Service)

### Incidents (Fires, Accidents)
- **Update frequency**: After incident reporting
- **Coverage**: Reported incidents only
- **Caveat**: Underreporting possible

## Compliance Score Interpretation

The `company_compliance_rate` field (0-1 scale):
- **0.90-1.00**: Excellent compliance history
- **0.75-0.89**: Good compliance, minor issues
- **0.50-0.74**: Moderate compliance, attention needed
- **0.00-0.49**: Poor compliance, likely repeat offender

## Related Skills

- **okonomi/** - Company financial data for CVR context
- **landbrugsareal/** - Land area and farm size context
- **miljo/** - Environmental compliance (related violations)
- **husdyr/** - Livestock operations (animal handling safety)

## GCS Paths Reference

```bash
# List arbejdstilsynet inspection data
gsutil ls gs://$GCS_BUCKET/gold/arbejdstilsynet_inspections/

# List work permit data
gsutil ls gs://$GCS_BUCKET/silver/work\ permits/

# List worker safety data
gsutil ls gs://$GCS_BUCKET/silver/worker\ safety/

# List incident data
gsutil ls gs://$GCS_BUCKET/silver/stable\ fires/
gsutil ls gs://$GCS_BUCKET/silver/transportation\ accidents/

# List DMA permit data
gsutil ls gs://$GCS_BUCKET/bronze/dma/
```

## Agricultural-Specific Safety Concerns

Common issues in agricultural workplace inspections:
1. **Machine safety** - Tractors, harvesters, feed machinery
2. **Chemical exposure** - Pesticides, fertilizers, cleaning agents
3. **Animal handling** - Large animal injuries, zoonotic diseases
4. **Ergonomics** - Repetitive lifting, awkward postures
5. **Confined spaces** - Silos, manure pits, grain bins
6. **Environmental** - Heat stress, cold exposure, UV radiation
