---
name: stat-data-fetcher
description: Access reliable statistical data from the World Bank. Avoids hallucinated numbers by fetching direct time-series data from the official API.
---

# Statistical Data Fetcher Skill

This skill allows you to retrieve grounded economic and social data, ensuring specific numbers in your reports are accurate and traced to an official source.

## Capabilities

1.  **Search Indicators**: Find the correct ID for a metric (e.g., "GDP per capita" -> `NY.GDP.PCAP.CD`).
2.  **Fetch Data**: Get time-series data for specific countries.
3.  **Fuzzy Scanning**: Handles country names like "France" or "USA" without needing ISO codes.
4.  **CSV Export**: Outputs data in CSV format for Excel/Pandas integration.

## Usage

Run the python script [fetch_worldbank.py](file:///C:/Users/Joshua/.gemini/antigravity/brain/126df87b-03b8-439b-8a30-d59c16e53143/skills/stat-data-fetcher/fetch_worldbank.py).

### Arguments

*   `--search` (optional): search term to find indicator IDs.
*   `--indicator` (optional): The content indicator ID (e.g., `NY.GDP.MKTP.CD`).
*   `--country` (optional): Country code OR Name (e.g. US;France;China) or "all". Default "US".
*   `--date` (optional): Date range (e.g., "2020:2025").
*   `--format` (optional): "json" (default) or "csv".

### Example

```bash
# 1. Get GDP for France and Germany in CSV format
python3 fetch_worldbank.py --indicator NY.GDP.MKTP.CD --country "France;Germany" --format csv

# 2. Search for "inflation"
python3 fetch_worldbank.py --search "inflation"
```

## Output Format

The script outputs a JSON list (default) or raw CSV text containing:
*   Country, ISO3, Year, Value, Indicator, Unit.

## Tips for the Agent

*   **Units Matter**: Check the unit field. World Bank often uses current US$ or % growth.
*   **Use CSV**: When the user wants "a table" or "data file", always use `--format csv`.
