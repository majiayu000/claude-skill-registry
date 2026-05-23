---
name: ieasyhydro-sdk
description: |
  Expert guide for the ieasyhydro-python-sdk library for connecting to iEasyHydro High Frequency (HF) database.
  Use when: (1) Making API requests to iEasyHydro HF, (2) Retrieving discharge/meteorological data,
  (3) Debugging 422 or other API errors, (4) Formatting filters for get_data_values_for_site(),
  (5) Working with code in preprocessing_runoff that fetches from iEasyHydro HF,
  (6) Understanding response structure from the SDK.
  Triggers: ieasyhydro, iEasyHydro, SDK, HF database, WDDA, WDD, discharge data retrieval, site_codes filter.
---

# iEasyHydro Python SDK Guide

SDK repository: https://github.com/hydrosolutions/ieasyhydro-python-sdk

## Installation

```bash
pip install git+https://github.com/hydrosolutions/ieasyhydro-python-sdk
```

## Configuration & Initialization

**Environment variables:**
```dotenv
IEASYHYDROHF_HOST=https://hf.ieasyhydro.org/api/v1/
IEASYHYDROHF_USERNAME=username
IEASYHYDROHF_PASSWORD=password
```

**Initialization options:**
```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK

# Option 1: From environment variables
sdk = IEasyHydroHFSDK()

# Option 2: Explicit configuration
sdk = IEasyHydroHFSDK(
    host='https://hf.ieasyhydro.org/api/v1/',
    username='username',
    password='password',
)
```

## Key Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_discharge_sites()` | List[dict] | Discharge stations (manual measurement sites) |
| `get_virtual_sites()` | List[dict] | Virtual/calculated stations |
| `get_meteo_sites()` | List[dict] | Meteorological stations |
| `get_data_values_for_site(filters)` | dict | Time-series data matching filters |
| `get_norm_for_site(site_code, norm_type, norm_period, automatic)` | List[float] | Historical norm values |

---

## Fetching Sites

### Discharge Sites

```python
discharge_sites = sdk.get_discharge_sites()
```

### Virtual Sites (calculated from associations)

```python
virtual_sites = sdk.get_virtual_sites()
```

### Meteorological Sites

```python
meteo_sites = sdk.get_meteo_sites()
```

### Site Response Structure

```python
{
    'id': 96,                           # Unique internal ID
    'site_code': '15054',               # Station code (use this for queries)
    'official_name': 'Ак-Сай - с.Көк-Сай',
    'national_name': '',
    'site_type': 'manual',              # 'manual' or 'automatic'
    'latitude': 42.8746,
    'longitude': 74.5698,
    'elevation': 0.0,
    'country': 'Кыргызстан',
    'basin': {
        'official_name': 'Иссык-Куль',
        'national_name': ''
    },
    'region': {
        'official_name': 'ИССЫК-КУЛЬСКАЯ ОБЛАСТЬ',
        'national_name': ''
    },
    'dangerous_discharge': 100.0,
    'historical_discharge_maximum': None,
    'historical_discharge_minimum': None,
    'bulletin_order': 0,
    'enabled_forecasts': {
        'daily_forecast': False,
        'decadal_forecast': False,
        'monthly_forecast': False,
        'pentad_forecast': False,
        'seasonal_forecast': False
    },
    # Associations: for virtual/calculated stations only
    # Formula: discharge = sum(weight_i * discharge_i) for each association
    'associations': [
        {
            'name': 'Ак-Терек - с.Ак-Терек',
            'id': 9,
            'uuid': '110e8400-e29b-41d4-a716-446655440000',
            'weight': 0.9,
            'station_code': '12346'
        }
    ]
}
```

**Note:** Meteo sites have `enabled_forecasts: None`.

---

## Fetching Data Values

### Basic Usage

```python
filters = {
    "site_codes": ["15013", "16159"],           # Station codes (strings)
    "variable_names": ["WDDA"],                  # Required: at least one metric
    "local_date_time__gte": "2024-01-01T00:00:00Z",  # Required: at least one timestamp
    "local_date_time__lte": "2024-12-31T23:59:59Z",
}

response = sdk.get_data_values_for_site(filters=filters)
```

### All Filter Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_codes` | List[str] | No* | Station codes like `["15013", "16159"]` |
| `site_ids` | List[int] | No* | Station IDs (internal database IDs) |
| `variable_names` | List[str] | **Yes** | Metric codes: `WDDA`, `WDD`, `WLD`, etc. |
| `local_date_time__gte` | str | **Yes**† | Local timestamp >= (ISO format) |
| `local_date_time__gt` | str | No | Local timestamp > |
| `local_date_time__lte` | str | No | Local timestamp <= |
| `local_date_time__lt` | str | No | Local timestamp < |
| `local_date_time` | str | No | Exact local timestamp match |
| `utc_date_time__gte` | str | No | UTC timestamp >= |
| `utc_date_time__gt` | str | No | UTC timestamp > |
| `utc_date_time__lte` | str | No | UTC timestamp <= |
| `utc_date_time__lt` | str | No | UTC timestamp < |
| `utc_date_time` | str | No | Exact UTC timestamp match |
| `page` | int | No | Page number for pagination |
| `page_size` | int | No | Items per page (max 1000, default 10) |

*Either `site_codes` or `site_ids` can be used, but `site_codes` is recommended.
†At least one timestamp filter is required.

### CRITICAL: Timestamp Handling

**`local_date_time` should NOT include local timezone - treat it as UTC:**

```python
import datetime

# To get 8AM local metrics:
local_date_time = datetime.datetime(2025, 9, 25, 8, 0, tzinfo=datetime.timezone.utc).isoformat()
# Result: "2025-09-25T08:00:00+00:00"

# To get 8PM local metrics:
local_date_time = datetime.datetime(2025, 9, 25, 20, 0, tzinfo=datetime.timezone.utc).isoformat()
```

### Response Structure

```python
{
    "count": 42,                    # Total number of results across all pages
    "next": "https://...?page=2",   # URL for next page (None if last page)
    "previous": None,               # URL for previous page
    "results": [
        {
            "station_id": 123,
            "station_uuid": "abc-123-def-456",
            "station_code": "16159",
            "station_name": "Station Name",
            "station_type": "hydro",
            "data": [
                {
                    "variable_code": "WDDA",
                    "unit": "m3/s",
                    "values": [
                        {
                            "value": 156.0,
                            "value_type": "M",
                            "timestamp_local": "2024-03-01T08:00:00",
                            "timestamp_utc": "2024-03-01T02:00:00Z",
                            "value_code": None
                        }
                    ]
                }
            ]
        }
    ]
}
```

**Response notes:**
- Non-existent station codes are silently omitted from results
- Stations with no data for requested variables return empty `values: []`

---

## Variable/Metric Codes

### Hydrological Measurements

| Code | Description | Notes |
|------|-------------|-------|
| `WLD` | Water level daily | 8AM or 8PM values from KN-15 telegram |
| `WLDA` | Water level daily average | Calculated from 8AM and 8PM values |
| `WLDC` | Water level decadal | From KN-15 subgroup 966 |
| `WLDCA` | Water level decade average | Decadal average for a period |
| `WDD` | Water discharge daily | Morning reading, may be estimated from rating curve |
| `WDDA` | Water discharge daily average | From daily avg water level + rating curve |
| `WDFA` | Water discharge fiveday average | Pentadal average |
| `WDDCA` | Water discharge decade average | Decadal average |
| `WTO` | Water temperature observation | Daily from KN-15 telegram section 4 |
| `ATO` | Air temperature observation | Daily from KN-15 telegram section 4 |
| `IPO` | Ice phenomena observation | Complex: intensity + value code |
| `PD` | Precipitation daily | Complex: value + duration code |
| `WTDA` | Water temperature daily average | |
| `ATDA` | Air temperature daily average | |
| `RCSA` | River cross section area | From KN-15 subgroup 966 |

### Meteorological Measurements

| Code | Description | Notes |
|------|-------------|-------|
| `ATDCA` | Air temperature decade average | Manual entry or KN-15 subgroup 988 |
| `PDCA` | Precipitation decade average | Manual entry or KN-15 subgroup 988 |
| `ATMA` | Air temperature monthly average | Manual entry or KN-15 subgroup 988 |
| `PMA` | Precipitation monthly average | Manual entry or KN-15 subgroup 988 |

### Value Type Codes

| Code | Description |
|------|-------------|
| `M` | Manual measurement |
| `A` | Automatic measurement |
| `E` | Estimated value |
| `I` | Imported value |
| `U` | Unknown source |
| `O` | Override (manually entered by hydrologist) |

---

## Pagination

### Page Size Limit

**The API supports `page_size` up to 1000 (updated January 2026).**

- Default page size is 10
- Using `page_size=1000` significantly improves performance (reduced maintenance run from 800s to 364s)
- You may still need pagination for very large result sets

### Pagination Pattern

```python
def fetch_all_with_pagination(sdk, filters):
    """Fetch all results with pagination."""
    all_results = []
    page = 1

    while True:
        paginated_filters = {**filters, "page": page, "page_size": 1000}
        response = sdk.get_data_values_for_site(filters=paginated_filters)

        # Check for API error
        if isinstance(response, dict) and 'status_code' in response:
            print(f"Error: {response}")
            break

        results = response.get('results', [])
        all_results.extend(results)

        # Check if there are more pages
        if not response.get('next'):
            break
        page += 1

    return all_results
```

### Optimized Parallel Pagination

For better performance, fetch pages in parallel after getting the count from page 1:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_all_parallel(sdk, filters, max_workers=10):
    """Fetch all results using parallel page requests."""
    PAGE_SIZE = 1000

    # Step 1: Get first page to learn total count
    first_response = sdk.get_data_values_for_site(
        filters={**filters, "page": 1, "page_size": PAGE_SIZE}
    )

    if isinstance(first_response, dict) and 'status_code' in first_response:
        return []  # Error

    total_count = first_response.get('count', 0)
    all_results = first_response.get('results', [])

    total_pages = (total_count + PAGE_SIZE - 1) // PAGE_SIZE
    if total_pages <= 1:
        return all_results

    # Step 2: Fetch remaining pages in parallel
    def fetch_page(page_num):
        resp = sdk.get_data_values_for_site(
            filters={**filters, "page": page_num, "page_size": PAGE_SIZE}
        )
        if isinstance(resp, dict) and 'status_code' not in resp:
            return resp.get('results', [])
        return []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_page, p) for p in range(2, total_pages + 1)]
        for future in as_completed(futures):
            all_results.extend(future.result())

    return all_results
```

---

## Fetching Norms

Historical norm values for stations:

```python
# Get decadal discharge norm (default)
norm = sdk.get_norm_for_site("11194", "discharge")

# Get monthly discharge norm
norm = sdk.get_norm_for_site("11194", "discharge", norm_period="m")

# Get pentad norms for automatic station
norm = sdk.get_norm_for_site("11194", "discharge", norm_period="p", automatic=True)

# Get monthly temperature norms
norm = sdk.get_norm_for_site("15194", "temperature", norm_period="m", automatic=False)
```

### Norm Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `norm_type` | `discharge`, `water_level`, `precipitation`, `temperature` | Type of norm |
| `norm_period` | `d` (decadal, default), `p` (pentad), `m` (monthly) | Time period |
| `automatic` | `True`/`False` | Automatic vs manual station |

### Norm Response

Returns a list of float values:
- **Decadal**: 36 values (3 per month)
- **Monthly**: 12 values (1 per month)
- **Pentadal**: 72 values (6 per month)

```python
[11.76, 11.69, 11.64, ...]  # 36 decadal values
```

Missing norms are `None`:
```python
[2.50, None, 3.75, 0.23, None, None, None, 0.45, 0.50, None, None, None]
```

---

## Error Handling

### API Requirements

1. **At least one timestamp filter must be present**
2. **At least one variable name must be specified**
3. **Variable names must be valid** (see metric codes above)

### Error Response Format

```python
{
    'status_code': 422,
    'text': '{"detail": "Some data is invalid or missing", "code": "schema_error"}'
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 422 "Some data is invalid" | Missing timestamp filter | Add `local_date_time__gte` or similar |
| 422 "Some data is invalid" | Missing variable_names | Add `variable_names: ["WDDA"]` |
| 422 "Invalid metric names" | Wrong variable code | Check metric codes table |
| 422 with large requests | Too many sites + large date range | Use batching or individual requests |

### Robust Fetching Strategy

```python
def fetch_robust(sdk, site_codes, base_filters, batch_size=10):
    """Try bulk, then batches, then individual requests."""

    # 1. Try bulk request
    bulk_filters = {**base_filters, "site_codes": site_codes}
    response = sdk.get_data_values_for_site(filters=bulk_filters)

    if isinstance(response, dict) and 'status_code' not in response:
        return fetch_all_with_pagination(sdk, bulk_filters)

    # 2. Try batches
    all_results = []
    for i in range(0, len(site_codes), batch_size):
        batch = site_codes[i:i + batch_size]
        batch_filters = {**base_filters, "site_codes": batch}
        results = fetch_all_with_pagination(sdk, batch_filters)
        all_results.extend(results)

    if all_results:
        return all_results

    # 3. Fall back to individual requests
    for code in site_codes:
        single_filters = {**base_filters, "site_codes": [code]}
        results = fetch_all_with_pagination(sdk, single_filters)
        all_results.extend(results)

    return all_results
```

---

## Complete Working Example

```python
from ieasyhydro_sdk.sdk import IEasyHydroHFSDK
from datetime import datetime, timezone, timedelta

sdk = IEasyHydroHFSDK()

# 1. Get all discharge sites
sites = sdk.get_discharge_sites()
site_codes = list(set(s['site_code'] for s in sites))  # Unique codes
print(f"Found {len(site_codes)} unique discharge sites")

# 2. Define date range
end_date = datetime.now(timezone.utc)
start_date = end_date - timedelta(days=30)

# 3. Build filters
filters = {
    "site_codes": site_codes,
    "variable_names": ["WDDA"],
    "local_date_time__gte": start_date.strftime('%Y-%m-%dT00:00:00Z'),
    "local_date_time__lte": end_date.strftime('%Y-%m-%dT23:59:59Z'),
}

# 4. Fetch with pagination
all_results = []
page = 1
while True:
    filters['page'] = page
    filters['page_size'] = 1000  # Max allowed

    response = sdk.get_data_values_for_site(filters=filters)

    if isinstance(response, dict) and 'status_code' in response:
        print(f"Error: {response}")
        break

    all_results.extend(response.get('results', []))

    if not response.get('next'):
        break
    page += 1

print(f"Fetched {len(all_results)} station records in {page} pages")

# 5. Process results
for station in all_results:
    code = station['station_code']
    name = station['station_name']
    for var in station.get('data', []):
        values = var.get('values', [])
        if values:
            latest = max(v['timestamp_local'][:10] for v in values)
            print(f"{code} ({name}): {len(values)} values, latest: {latest}")
```

---

## Key Gotchas Summary

1. **Page size max is 1000** - use this for better performance
2. **Use `site_codes` (strings) not `site_ids`** - both work but codes are more reliable
3. **`local_date_time` acts as UTC** - don't include local timezone offset
4. **At least one timestamp filter required** - or you get 422 error
5. **At least one variable_name required** - or you get 422 error
6. **Non-existent stations are silently omitted** - no error, just missing from results
7. **Large bulk requests may fail** - use batching for many sites + long date ranges
8. **Associations are for calculation** - they define how virtual station discharge is computed
