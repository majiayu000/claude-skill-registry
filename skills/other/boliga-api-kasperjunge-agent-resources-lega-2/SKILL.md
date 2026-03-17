---
name: boliga-api
description: Query Danish real estate data from Boliga.dk as pandas DataFrames. Use when the user asks about Danish property prices, real estate searches, market statistics, or housing analysis in Denmark.
---

# Boliga API

Query Danish real estate data via `scripts/boliga.py`.

## Usage

```python
import sys
sys.path.insert(0, '<skill-path>/scripts')
from boliga import get_properties, Municipality, PropertyType, SortOrder

# Search properties
df = get_properties(
    municipality=Municipality.ROSKILDE,
    property_type=PropertyType.TERRACED,
    price_max=5000000
)

# Analyze with pandas
avg_sqm = df['sqm_price'].mean()
df.groupby('zip_code')['price'].median()
```

## Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `get_properties(...)` | DataFrame | Active listings with filters |
| `get_sold_properties(...)` | DataFrame | Historical sales |
| `get_estate_details(id)` | dict | Property details |
| `get_property_history(id)` | DataFrame | Property sale history |
| `get_market_statistics()` | dict | National price trends |
| `search_location(query)` | DataFrame | Location autocomplete |
| `get_new_construction(...)` | DataFrame | New construction projects |

## Key Parameters

**Municipalities:** `Municipality.COPENHAGEN`, `ROSKILDE`, `AARHUS`, `ODENSE`, `FREDERIKSBERG`, `GENTOFTE`

**Property types:** `PropertyType.VILLA`, `TERRACED`, `APARTMENT`, `HOLIDAY`, `COOPERATIVE`, `FARM`

**Sort:** `SortOrder.PRICE_ASC`, `PRICE_DESC`, `SQM_PRICE_ASC`, `DAYS_FOR_SALE_ASC`

## DataFrame Columns

`get_properties()` returns: `id`, `street`, `city`, `zip_code`, `price`, `sqm_price`, `size`, `rooms`, `build_year`, `property_type`, `days_for_sale`, `lot_size`, `energy_class`, `lat`, `lon`, `views`
