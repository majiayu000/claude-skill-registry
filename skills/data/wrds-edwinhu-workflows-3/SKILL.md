---
name: wrds
version: 1.0
description: This skill should be used when the user asks to "query WRDS", "access Compustat", "get CRSP data", "pull Form 4 insider data", "query ISS compensation", "download SEC EDGAR filings", "get ExecuComp data", "access Capital IQ", "write SAS code for WRDS", "SAS ETL", "SAS hash merge", "SGE array job", "qsas", "qsub SAS", or needs WRDS PostgreSQL query patterns or SAS ETL performance patterns.
user-invocable: false
---

## Contents

- [Query Enforcement](#query-enforcement)
- [SAS ETL Enforcement](#sas-etl-enforcement)
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

This is not negotiable. Skipping sample inspection is NOT HELPFUL — the user builds analysis on data with undetected quality problems.

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

## SAS ETL Enforcement

### IRON LAW: NO SAS CODE WITHOUT PERFORMANCE VALIDATION FIRST

<EXTREMELY-IMPORTANT>
Before writing or executing ANY SAS code on WRDS, you MUST validate performance patterns. This is not negotiable.

1. **MERGE STRATEGY** — Is hash or sort-merge appropriate? Justify the choice.
2. **WHERE CLAUSES** — Are all date/string filters index-friendly? No functions on indexed columns.
3. **PARALLELISM** — Can this job run as an SGE array? Year-by-year is always parallelizable.
4. **SQL OPTIMIZATION** — For PROC SQL: pass-through opportunity? Indexed join columns?

Writing SAS code that forces full table scans when indexes exist is NOT HELPFUL — the user's job runs 100x slower than necessary and may timeout.
</EXTREMELY-IMPORTANT>

### SAS Code Validation Checklist

Before EVERY SAS program execution:

**For merges/joins:**
- [ ] Small lookup + large fact table → hash object (not `PROC SORT` + `DATA` merge)
- [ ] Hash uses `defineKey`/`defineData`/`defineDone` pattern correctly
- [ ] `h.output()` uses double quotes for macro resolution (not single quotes)
- [ ] `call missing()` initializes hash data variables for non-matches
- [ ] Both tables >50M rows → sort-merge is justified (document why)

**For WHERE clauses (CRITICAL):**
- [ ] **NO** `year(date)`, `month(date)`, `datepart(dt)` wrapping indexed columns
- [ ] Date filters use `BETWEEN "01jan&year."d AND "31dec&year."d` range pattern
- [ ] String filters avoid `upcase()`, `substr()` on indexed columns
- [ ] Compound date filters collapsed to single range (not `year() = X AND quarter() = Y`)

**For batch processing:**
- [ ] Multi-year jobs use SGE array (`#$ -t start-end`) not sequential loop
- [ ] Year passed via `-sysparm` (not `-set` or `%sysget`)
- [ ] Per-year log files (not single shared log)
- [ ] Memory allocation appropriate for workload (`#$ -l m_mem_free=4G` minimum)
- [ ] Single-year benchmark run completed before full array submission

**For PROC SQL:**
- [ ] Join columns are not wrapped in functions
- [ ] `calculated` keyword used for computed column references in HAVING
- [ ] Pass-through SQL considered for direct WRDS PostgreSQL queries
- [ ] No redundant subqueries that could be hash lookups

**For macros:**
- [ ] Macro variables terminated with period (`&year.` not `&year`)
- [ ] Double quotes used where macro resolution is needed
- [ ] `options mprint mlogic symbolgen` used during development

### SAS Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "Sort-merge is simpler to write" | Hash is 10x faster for lookup joins and requires no sorting | Write the hash — it's 5 extra lines |
| "year(date) is readable" | Readable but prevents index usage — full table scan on millions of rows | Use BETWEEN with date literals |
| "I'll parallelize later" | Later never comes and the job runs 18x slower sequentially | Write the SGE array job NOW |
| "Single quotes work fine in hash" | Single quotes block macro resolution — your output dataset name is wrong | ALWAYS double quotes in h.output() |
| "PROC SQL is easier than hash" | PROC SQL still sorts for joins — hash avoids all sorting | Hash for lookups, SQL only for complex aggregations |
| "The job only takes a few minutes per year" | 18 years × 3 minutes = 54 minutes sequential vs 3 minutes parallel | SGE array for ANY multi-year job |
| "%sysget works for getting the year" | Unreliable in SGE context — may return blank silently | Use -sysparm + &sysparm. |

### SAS Red Flags - STOP Immediately If You're About To:

- Write `where year(date) = ` anything → STOP. Use `BETWEEN` with date literals.
- Write `proc sort; data; merge` for a lookup join → STOP. Use hash object.
- Write a `%do year = start %to end` loop → STOP. Use SGE array job.
- Use single quotes in `h.output(dataset: '...')` → STOP. Use double quotes.
- Submit a full array job without testing one year first → STOP. Benchmark first.
- Use `-set` or `%sysget` for SGE task parameters → STOP. Use `-sysparm`.

### SAS Reference

See **`references/sas-etl.md`** for complete patterns:
- Hash object merge (basic, multidata, accumulator)
- Index-friendly WHERE clause quick reference table
- SGE array job templates with memory and logging
- PROC SQL pass-through and optimization
- Macro quoting and debugging

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
- **`references/sas-etl.md`** - SAS hash objects, index-friendly WHERE, SGE array jobs, PROC SQL optimization

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
