---
name: stat-data-fetcher
description: Access reliable statistical data from the World Bank. Avoids hallucinated numbers by fetching direct time-series data from the official API.
---

# Statistical Data Fetcher Skill

This skill allows you to retrieve grounded economic and social data, ensuring specific numbers in your reports are accurate and traced to an official source.

## Capabilities

1.  **Search Indicators**: Find the correct ID for a metric (e.g., "GDP per capita" -> `NY.GDP.PCAP.CD`).
2.  **Fetch Data**: Get time-series data for specific countries.

## Usage

Run the python script `fetch_worldbank.py`.

### Arguments

*   `--search` (optional): search term to find indicator IDs.
*   `--indicator` (optional): The content indicator ID (e.g., `NY.GDP.MKTP.CD`).
*   `--country` (optional): Country code (ISO 2-letter, e.g., US, CN, JP) or "all". Default "US".
*   `--date` (optional): Date range (e.g., "2020:2025").

### Example

```bash
# 1. Find the indicator for "population"
python3 fetch_worldbank.py --search "total population"

# 2. Get US and China population for last 5 years
# (Assuming found ID is SP.POP.TOTL)
python3 fetch_worldbank.py --indicator SP.POP.TOTL --country US;CN --date 2020:2025
```

## Output Format

The script outputs a JSON object (or list):
```json
[
  {
    "indicator": {"id": "SP.POP.TOTL", "value": "Population, total"},
    "country": {"id": "CN", "value": "China"},
    "countryiso3code": "CHN",
    "date": "2023",
    "value": 1411750000,
    ...
  }
]
```

## Tips for the Agent

*   **Always Search First**: Indicator IDs are specific. Don't guess `GDP`. Search for "GDP" and pick `NY.GDP.MKTP.CD` (current US$).
*   **Nulls**: Real data often has gaps. Check for `null` values.
