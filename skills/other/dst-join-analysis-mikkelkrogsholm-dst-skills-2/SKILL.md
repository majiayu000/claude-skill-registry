---
name: dst-join-analysis
description: |
  Perform SQL joins and multi-table analysis on DST data in DuckDB. Use when
  research requires combining multiple tables on common dimensions (time, region).
  Provides patterns for common DST dimension joins and multi-table comparisons.
---

# DST Multi-Table Join Analysis

Combine and analyze multiple Danmarks Statistik tables stored in DuckDB.

## Common DST Dimensions

DST tables often share these dimensions:

### 1. Time Dimensions
- `tid` - Time period (year, quarter, month)
- Common formats: '2023', '2023K1', '2023M01'
- All tables with time series can join on this

### 2. Regional Dimensions
- `område` - Geographic area (hele landet, regions, municipalities)
- `region` - Region codes
- `kommune` - Municipality codes

### 3. Demographic Dimensions
- `køn` - Gender (M/K/Total)
- `alder` - Age groups
- `herkomst` - Origin/ethnicity

## Join Patterns

### Pattern 1: Time-Series Join

When both tables have time dimension:

```sql
-- Example: Join population (FOLK1A) with births (FOD)
SELECT
  f.tid AS year,
  f.indhold AS population,
  b.indhold AS births,
  ROUND(b.indhold::FLOAT / f.indhold * 1000, 2) AS birth_rate_per_1000
FROM dst_folk1a f
INNER JOIN dst_fod b ON f.tid = b.tid
WHERE f.område = 'Hele landet'
  AND b.område = 'Hele landet'
ORDER BY f.tid;
```

**Use when**: Comparing two time-series indicators

### Pattern 2: Regional Comparison

When both tables have regional breakdown:

```sql
-- Example: Compare population (FOLK1A) across regions
SELECT
  t1.område AS region,
  t1.tid AS year,
  t1.indhold AS population_2020,
  t2.indhold AS population_2023,
  ROUND((t2.indhold::FLOAT - t1.indhold) / t1.indhold * 100, 2) AS growth_pct
FROM dst_folk1a t1
INNER JOIN dst_folk1a t2
  ON t1.område = t2.område
WHERE t1.tid = '2020'
  AND t2.tid = '2023'
  AND t1.område != 'Hele landet'
ORDER BY growth_pct DESC;
```

**Use when**: Comparing regions across same indicator

### Pattern 3: Multi-Indicator Analysis

When joining different indicators by time and region:

```sql
-- Example: Correlate unemployment with business bankruptcies
SELECT
  u.tid AS year,
  u.indhold AS unemployment_rate,
  b.indhold AS bankruptcies,
  ROUND(b.indhold::FLOAT / u.indhold, 2) AS bankruptcies_per_unemployed
FROM dst_unemployment u
INNER JOIN dst_bankruptcies b
  ON u.tid = b.tid
  AND u.område = b.område
WHERE u.område = 'Hele landet'
ORDER BY u.tid;
```

**Use when**: Exploring relationships between different indicators

### Pattern 4: Aggregate Join

When one table is at higher granularity:

```sql
-- Example: Join total population with regional breakdown
SELECT
  total.tid AS year,
  total.indhold AS total_population,
  region.område AS region,
  region.indhold AS region_population,
  ROUND(region.indhold::FLOAT / total.indhold * 100, 2) AS pct_of_total
FROM dst_folk1a total
INNER JOIN dst_folk1a region
  ON total.tid = region.tid
WHERE total.område = 'Hele landet'
  AND region.område != 'Hele landet'
  AND region.område LIKE 'Region%'
ORDER BY total.tid, pct_of_total DESC;
```

**Use when**: Comparing parts to whole

## Data Type Handling

DST data stored as TEXT, convert for calculations:

```sql
-- Convert to numeric for math
SELECT
  tid,
  CAST(indhold AS INTEGER) AS value_int,
  CAST(indhold AS FLOAT) AS value_float,
  CAST(indhold AS DECIMAL(15,2)) AS value_decimal
FROM dst_table;
```

## Common Calculations

### Growth Rate
```sql
ROUND((new_value::FLOAT - old_value) / old_value * 100, 2) AS growth_pct
```

### Year-over-Year Change
```sql
SELECT
  t1.tid AS year,
  t1.indhold AS current_value,
  LAG(t1.indhold) OVER (ORDER BY t1.tid) AS previous_value,
  t1.indhold::FLOAT - LAG(t1.indhold) OVER (ORDER BY t1.tid) AS yoy_change
FROM dst_table t1;
```

### Moving Average
```sql
SELECT
  tid,
  indhold,
  AVG(indhold::FLOAT) OVER (
    ORDER BY tid
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS moving_avg_3y
FROM dst_table;
```

### Correlation (Pearson)
```sql
-- DuckDB has built-in correlation
SELECT
  CORR(t1.indhold::FLOAT, t2.indhold::FLOAT) AS correlation_coefficient
FROM dst_table1 t1
INNER JOIN dst_table2 t2 ON t1.tid = t2.tid;
```

## Handling Missing Data

DST tables may have:
- `NULL` values
- `".."` for unavailable data
- `"-"` for zero/not applicable

```sql
-- Filter out missing data
WHERE indhold IS NOT NULL
  AND indhold NOT IN ('..', '-', '')
  AND TRY_CAST(indhold AS INTEGER) IS NOT NULL
```

## Query Optimization Tips

1. **Filter early**: Apply WHERE before JOIN when possible
2. **Use indexes**: DuckDB auto-indexes, but column order matters
3. **Limit rows**: Add LIMIT for exploration, remove for final analysis
4. **Aggregate wisely**: Use GROUP BY only when necessary

## Example Multi-Table Research Query

```sql
-- Research question: "How does population growth correlate with housing starts?"

WITH pop_growth AS (
  SELECT
    t1.tid AS year,
    (t2.indhold::FLOAT - t1.indhold) / t1.indhold * 100 AS pop_growth_pct
  FROM dst_folk1a t1
  INNER JOIN dst_folk1a t2 ON t1.tid = CAST(CAST(t2.tid AS INTEGER) - 1 AS VARCHAR)
  WHERE t1.område = 'Hele landet' AND t2.område = 'Hele landet'
),
housing AS (
  SELECT
    tid AS year,
    indhold::INTEGER AS housing_starts
  FROM dst_housing_table
  WHERE område = 'Hele landet'
)
SELECT
  p.year,
  p.pop_growth_pct,
  h.housing_starts,
  CORR(p.pop_growth_pct, h.housing_starts) OVER () AS correlation
FROM pop_growth p
INNER JOIN housing h ON p.year = h.year
ORDER BY p.year;
```

## Usage Guidelines

When dst-research-analyst invokes you:

1. **Identify join keys**: What dimensions do tables share?
2. **Choose pattern**: Which pattern fits the analysis?
3. **Handle data types**: Convert TEXT to numeric
4. **Filter missing data**: Remove NULL/".."/"-"
5. **Add calculations**: Growth rates, percentages, correlations
6. **Order results**: By time or magnitude
7. **Return SQL**: Provide query for dst-query skill to execute

Remember: You provide the SQL patterns, dst-query executes them.
