---
name: lseg-data
version: 1.0
description: This skill should be used when the user asks to "access LSEG data", "query Refinitiv", "get market data from Refinitiv", "download fundamentals from LSEG", "access ESG scores", "convert RIC to ISIN", or needs the LSEG Data Library Python API.
---

## Contents

- [Query Enforcement](#query-enforcement)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Core APIs](#core-apis)
- [Key Field Prefixes](#key-field-prefixes)
- [RIC Symbology](#ric-symbology)
- [Rate Limits](#rate-limits)
- [Additional Resources](#additional-resources)

# LSEG Data Library

Access financial data from LSEG (London Stock Exchange Group), formerly Refinitiv, via the `lseg.data` Python library.

## Query Enforcement

### IRON LAW: NO DATA CLAIM WITHOUT SAMPLE INSPECTION

Before claiming ANY LSEG query succeeded, follow these steps:
1. **VALIDATE** field names exist (check prefixes: TR., CF_)
2. **VALIDATE** RIC symbology is correct (.O, .N, .L, .T)
3. **EXECUTE** the query
4. **INSPECT** sample rows with `.head()` or `.sample()`
5. **VERIFY** critical columns are not NULL
6. **VERIFY** date range matches expectations
7. **CLAIM** success only after all checks pass

This is not negotiable. Claiming data retrieval without inspecting results is LYING to the user about data quality.

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The query returned data, so it worked" | Returned data ≠ correct data | INSPECT for NULLs, wrong dates, invalid values |
| "User gave me the RIC" | Users often use wrong suffixes | VERIFY symbology against RIC Symbology section |
| "I'll let pandas handle missing data" | You'll propagate bad data downstream | CHECK for NULLs BEFORE returning |
| "Field names look right" | Typos are common (TR.EPS vs TR.Eps) | VALIDATE field names in documentation first |
| "Just a quick test" | Test queries teach bad habits | Full validation even for tests |
| "I can check the data later" | You won't | Inspection is MANDATORY before claiming success |
| "Rate limits don't matter for small queries" | Small queries add up | CHECK rate limits section, use batching |

### Red Flags - STOP Immediately If You Think:

- "Let me run this and see what happens" → NO. Validate field names and RICs FIRST.
- "The API will error if something is wrong" → NO. API returns empty results, not errors.
- "I'll just return the dataframe to the user" → NO. Inspect sample BEFORE returning.
- "Market data is always up-to-date" → NO. Check Date Awareness section (T-1 lag).

### Data Validation Checklist

Before EVERY data retrieval claim, verify the following:

**For `ld.get_data()` (fundamentals/ESG):**
- [ ] Field names use correct prefix (TR. for Refinitiv)
- [ ] RIC symbology verified (correct exchange suffix)
- [ ] Result inspection: `.head()` or `.sample()` executed
- [ ] NULL check on critical fields (e.g., revenue, EPS)
- [ ] Row count verification (is result size reasonable?)
- [ ] Date context verified (fiscal periods, as-of dates)

**For `ld.get_history()` (time series):**
- [ ] Field names are valid (OPEN, HIGH, LOW, CLOSE, VOLUME, or CF_ prefixes)
- [ ] Start/end dates specified explicitly
- [ ] Date range adjusted for T-1 availability (market data lag)
- [ ] Result inspection: check first and last rows
- [ ] NULL check on OHLCV fields
- [ ] Date continuity check (gaps in trading days expected, but not in date sequence)

**For `symbol_conversion.Definition()` (mapping):**
- [ ] Input identifier type specified correctly
- [ ] Result inspection: verify mapped values exist
- [ ] NULL check (some securities may not have all identifiers)

**For ALL queries:**
- [ ] Rate limits considered (batch if >10k data points)
- [ ] Session management: `open_session()` at start, `close_session()` at end
- [ ] Error handling: try/except for network failures
- [ ] Sample inspection BEFORE claiming data is ready

## Quick Start

To get started with LSEG Data Library, initialize a session and execute queries:

```python
import lseg.data as ld

# Initialize session
ld.open_session()

# Get fundamentals
df = ld.get_data(
    universe=['AAPL.O', 'MSFT.O'],
    fields=['TR.CompanyName', 'TR.Revenue', 'TR.EPS']
)
print(df.head())  # Inspect sample data

# Get historical prices
prices = ld.get_history(
    universe='AAPL.O',
    fields=['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'],
    start='2023-01-01',
    end='2023-12-31'
)
print(prices.head())  # Inspect sample data

# Close session
ld.close_session()
```

## Authentication

Configure LSEG authentication using either a config file or environment variables.

### Config File Method

Create `lseg-data.config.json`:
```json
{
  "sessions": {
    "default": "platform.ldp",
    "platform": {
      "ldp": {
        "app-key": "YOUR_APP_KEY",
        "username": "YOUR_MACHINE_ID",
        "password": "YOUR_PASSWORD"
      }
    }
  }
}
```

### Environment Variables Method

Set the following environment variables for LSEG authentication:

```bash
# Configure LSEG credentials via environment variables
export RDP_USERNAME="YOUR_MACHINE_ID"
export RDP_PASSWORD="YOUR_PASSWORD"
export RDP_APP_KEY="YOUR_APP_KEY"
```

## Core APIs

| API | Use Case | Example |
|-----|----------|---------|
| `ld.get_data()` | Point-in-time data | Fundamentals, ESG scores |
| `ld.get_history()` | Time series | Historical prices, OHLCV |
| `symbol_conversion.Definition()` | ID mapping | RIC ↔ ISIN ↔ CUSIP |

## Key Field Prefixes

| Prefix | Type | Example |
|--------|------|---------|
| `TR.` | Refinitiv fields | `TR.Revenue`, `TR.EPS` |
| `CF_` | Composite (real-time) | `CF_LAST`, `CF_BID` |

## RIC Symbology

| Suffix | Exchange | Example |
|--------|----------|---------|
| `.O` | NASDAQ | `AAPL.O` |
| `.N` | NYSE | `IBM.N` |
| `.L` | London | `VOD.L` |
| `.T` | Tokyo | `7203.T` |

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `get_data()` | 10,000 data points/request |
| `get_history()` | 3,000 rows/request |
| Session | 500 requests/minute |

## Additional Resources

### Reference Files

- **`references/fundamentals.md`** - Financial statement fields, ratios, estimates
- **`references/esg.md`** - ESG scores, pillars, controversies
- **`references/symbology.md`** - RIC/ISIN/CUSIP conversion
- **`references/pricing.md`** - Historical prices, real-time data
- **`references/screening.md`** - Stock screening with Screener object
- **`references/troubleshooting.md`** - Common issues and solutions
- **`references/wrds-comparison.md`** - LSEG vs WRDS data mapping

### Example Files

- **`examples/historical_pricing.ipynb`** - Historical price retrieval
- **`examples/fundamentals_query.py`** - Fundamental data patterns
- **`examples/stock_screener.ipynb`** - Dynamic stock screening

### Scripts

- **`scripts/test_connection.py`** - Validate LSEG connectivity

### Local Sample Repositories

LSEG API samples at `~/resources/lseg-samples/`:
- `Example.RDPLibrary.Python/` - Core API examples
- `Examples.DataLibrary.Python.AdvancedUsecases/` - Advanced patterns
- `Article.DataLibrary.Python.Screener/` - Stock screening

## Date Awareness

When querying market data, account for current date context and market data lag.

### Market Data Lag

Market data typically has T-1 availability, meaning today's data becomes available tomorrow. Adjust date ranges accordingly.

### Date Range Example

Use current date context when querying historical prices:

```python
from datetime import datetime, timedelta

# Get recent market data
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# Adjust to exclude recent data (T-1 for market data availability)
end_date = end_date - timedelta(days=1)

df = ld.get_history(
    universe="AAPL.O",
    fields=['CLOSE'],
    start=start_date.strftime('%Y-%m-%d'),
    end=end_date.strftime('%Y-%m-%d')
)
```

Remember: Always account for the T-1 lag in market data availability.
