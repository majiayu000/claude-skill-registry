---
name: wrds
version: 1.0
description: This skill should be used when the user asks to "query WRDS", "access Compustat", "get CRSP data", "pull Form 4 insider data", "query ISS compensation", "download SEC EDGAR filings", "get ExecuComp data", "access Capital IQ", or needs WRDS PostgreSQL query patterns.
---

## Contents

- [Query Enforcement](#query-enforcement)
- [Quick Reference: Table Names](#quick-reference-table-names)
- [Connection](#connection)
- [Critical Filters](#critical-filters)
- [Parameterized Queries](#parameterized-queries)
- [Additional Resources](#additional-resources)

# WRDS Data Access

WRDS (Wharton Research Data Services) provides academic research data via PostgreSQL at `wrds-pgdata.wharton.upenn.edu:9737`.

## Query Enforcement

### IRON LAW: NO QUERY WITHOUT FILTER VALIDATION FIRST

Before executing ANY WRDS query, you MUST:
1. **IDENTIFY** what filters are required for this dataset
2. **VALIDATE** the query includes those filters
3. **VERIFY** parameterized queries (never string formatting)
4. **EXECUTE** the query
5. **INSPECT** a sample of results before claiming success

This is not negotiable. Claiming query success without sample inspection is LYING to the user about data quality.

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I'll add filters later" | You'll forget and pull bad data | Add filters NOW, before execution |
| "User didn't specify filters" | Standard filters are ALWAYS required | Apply Critical Filters section defaults |
| "Just a quick test query" | Test queries with bad filters teach bad patterns | Use production filters even for tests |
| "I'll let the user filter in pandas" | Pulling millions of unnecessary rows wastes time/memory | Filter at database level FIRST |
| "The query worked, so it's correct" | Query success ≠ data quality | INSPECT sample for invalid records |
| "I can use f-strings for simple queries" | SQL injection risk + wrong type handling | ALWAYS use parameterized queries |

### Red Flags - STOP Immediately If You Think:

- "Let me run this query quickly to see what's there" → NO. Check Critical Filters section first.
- "I'll just pull everything and filter later" → NO. Database-level filtering is mandatory.
- "The table name is obvious from the request" → NO. Check Quick Reference section for exact names.
- "I can inspect the data after the user sees it" → NO. Sample inspection BEFORE claiming success.

### Query Validation Checklist

Before EVERY query execution:

**For Compustat queries (comp.funda, comp.fundq):**
- [ ] Includes `indfmt = 'INDL'`
- [ ] Includes `datafmt = 'STD'`
- [ ] Includes `popsrc = 'D'`
- [ ] Includes `consol = 'C'`
- [ ] Uses parameterized queries for variables
- [ ] Date range is explicitly specified

**For CRSP v2 queries (crsp.dsf_v2, crsp.msf_v2):**
- [ ] Post-query filter: `sharetype == 'NS'`
- [ ] Post-query filter: `securitytype == 'EQTY'`
- [ ] Post-query filter: `securitysubtype == 'COM'`
- [ ] Post-query filter: `usincflg == 'Y'`
- [ ] Post-query filter: `issuertype.isin(['ACOR', 'CORP'])`
- [ ] Uses parameterized queries

**For Form 4 queries (tr_insiders.table1):**
- [ ] Transaction type filter specified (acqdisp)
- [ ] Transaction codes specified (trancode)
- [ ] Date range is explicitly specified
- [ ] Uses parameterized queries

**For ALL queries:**
- [ ] Sample inspection with `.head()` or `.sample()` BEFORE claiming success
- [ ] Row count verification (is result size reasonable?)
- [ ] NULL value check on critical columns
- [ ] Date range validation (does min/max match expectations?)

## Quick Reference: Table Names

| Dataset | Schema | Key Tables |
|---------|--------|------------|
| Compustat | `comp` | `company`, `funda`, `fundq`, `secd` |
| ExecuComp | `comp_execucomp` | `anncomp` |
| CRSP | `crsp` | `dsf`, `msf`, `stocknames`, `ccmxpf_linkhist` |
| CRSP v2 | `crsp` | `dsf_v2`, `msf_v2`, `stocknames_v2` |
| Form 4 Insiders | `tr_insiders` | `table1`, `header`, `company` |
| ISS Incentive Lab | `iss_incentive_lab` | `comppeer`, `sumcomp`, `participantfy` |
| Capital IQ | `ciq` | `wrds_compensation` |
| IBES | `tr_ibes` | `det_epsus`, `statsum_epsus` |
| SEC EDGAR | `wrdssec` | `wrds_forms`, `wciklink_cusip` |
| SEC Search | `wrds_sec_search` | `filing_view`, `registrant` |
| EDGAR | `edgar` | `filings`, `filing_docs` |
| Fama-French | `ff` | `factors_monthly`, `factors_daily` |
| LSEG/Datastream | `tr_ds` | `ds2constmth`, `ds2indexlist` |

## Connection

Initialize PostgreSQL connection to WRDS:

```python
import psycopg2

conn = psycopg2.connect(
    host='wrds-pgdata.wharton.upenn.edu',
    port=9737,
    database='wrds',
    sslmode='require'
    # Credentials from ~/.pgpass
)
```

Configure authentication via `~/.pgpass` with `chmod 600`:
```
wrds-pgdata.wharton.upenn.edu:9737:wrds:USERNAME:PASSWORD
```

Connect via SSH tunnel:
```bash
ssh wrds
```

This uses `~/.ssh/wrds_rsa` for authentication.

## Critical Filters

### Compustat Standard Filters
Always include for clean fundamental data:
```sql
WHERE indfmt = 'INDL'
  AND datafmt = 'STD'
  AND popsrc = 'D'
  AND consol = 'C'
```

### CRSP v2 Common Stock Filter
Equivalent to legacy `shrcd IN (10, 11)`:
```python
df = df.loc[
    (df.sharetype == 'NS') &
    (df.securitytype == 'EQTY') &
    (df.securitysubtype == 'COM') &
    (df.usincflg == 'Y') &
    (df.issuertype.isin(['ACOR', 'CORP']))
]
```

### Form 4 Transaction Types
```sql
WHERE acqdisp = 'D'  -- Dispositions
  AND trancode IN ('S', 'D', 'G', 'F')  -- Sales, Dispositions, Gifts, Tax
```

## Parameterized Queries

Always use parameterized queries (never string formatting):

Use scalar parameter binding for single values:
```python
cursor.execute("""
    SELECT gvkey, conm FROM comp.company WHERE gvkey = %s
""", (gvkey,))
```

Use ANY() for list parameters:
```python
cursor.execute("""
    SELECT * FROM comp.funda WHERE gvkey = ANY(%s)
""", (gvkey_list,))
```

## Additional Resources

### Reference Files

Detailed query patterns and table documentation:

- **`references/compustat.md`** - Compustat tables, ExecuComp, financial variables
- **`references/crsp.md`** - CRSP stock data, CCM linking, v2 format
- **`references/insider-form4.md`** - Thomson Reuters Form 4, rolecodes, insider types
- **`references/iss-compensation.md`** - ISS Incentive Lab, peer companies, compensation
- **`references/edgar.md`** - SEC EDGAR filings, URL construction, DCN vs accession numbers
- **`references/connection.md`** - Connection pooling, caching, error handling

### Example Files

Working code from real projects:

- **`examples/form4_disposals.py`** - Insider trading analysis (from SVB project)
- **`examples/wrds_connector.py`** - Connection pooling pattern

### Scripts

- **`scripts/test_connection.py`** - Validate WRDS connectivity

### Local Sample Notebooks

WRDS-provided samples at `~/resources/wrds-code-samples/`:
- `ResearchApps/CCM2025.ipynb` - Modern CRSP-Compustat merge
- `ResearchApps/ff3_crspCIZ.ipynb` - Fama-French factor construction
- `comp/sas/execcomp_ceo_screen.sas` - ExecuComp patterns

## Date Awareness

When querying historical data, leverage current date context for dynamic range calculations.

Current date is automatically available via `datetime.now()`. Apply this to:
- Data range validation (e.g., "get data for last 5 years")
- Fiscal year calculations
- Event study windows

Implement dynamic date ranges in queries:
```python
from datetime import datetime, timedelta

# Query last 5 years of data
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)

query = """
SELECT * FROM comp.funda
WHERE datadate BETWEEN %s AND %s
"""
df = pd.read_sql(query, conn, params=(start_date, end_date))
```

Always incorporate current date awareness in date-dependent queries to ensure results remain fresh across time.
