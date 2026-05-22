---
name: Backfill and Reconciliation Playbook
description: Playbook สำหรับ backfill historical data และ reconcile inconsistencies ระหว่าง data sources
---

# Backfill and Reconciliation Playbook

## Overview

Playbook สำหรับ backfill historical data (เติมข้อมูลย้อนหลัง) และ reconcile (จับคู่/แก้ไข) inconsistencies ระหว่าง sources

## Why This Matters

- **Data completeness**: ไม่มีช่องว่าง
- **Consistency**: Data ตรงกันทุก source
- **Trust**: เชื่อถือได้ว่า data ถูกต้อง
- **Recovery**: แก้ไขได้ถ้ามี issues

---

## Backfill Strategy

### 1. Identify Gap
```sql
-- Find missing dates
WITH date_range AS (
  SELECT generate_series(
    '2024-01-01'::date,
    CURRENT_DATE,
    '1 day'::interval
  )::date as date
)
SELECT dr.date
FROM date_range dr
LEFT JOIN analytics.daily_metrics dm ON dr.date = dm.date
WHERE dm.date IS NULL
ORDER BY dr.date;

-- Output: Missing dates that need backfill
```

### 2. Backfill in Batches
```python
def backfill_data(start_date: date, end_date: date, batch_size: int = 7):
    """Backfill data in batches to avoid overwhelming system"""
    
    current = start_date
    while current <= end_date:
        batch_end = min(current + timedelta(days=batch_size), end_date)
        
        print(f"Backfilling {current} to {batch_end}")
        
        # Run backfill for this batch
        run_dbt_model(
            model='daily_metrics',
            vars={'start_date': current, 'end_date': batch_end}
        )
        
        # Verify
        verify_backfill(current, batch_end)
        
        current = batch_end + timedelta(days=1)
        time.sleep(60)  # Rate limit

# Example
backfill_data(date(2024, 1, 1), date(2024, 1, 31))
```

---

## Reconciliation

### Compare Sources
```python
def reconcile_sources(source_a: str, source_b: str, key: str):
    """Compare two data sources and find discrepancies"""
    
    # Get data from both sources
    data_a = db_a.query(f"SELECT * FROM {source_a}")
    data_b = db_b.query(f"SELECT * FROM {source_b}")
    
    # Convert to dataframes
    df_a = pd.DataFrame(data_a)
    df_b = pd.DataFrame(data_b)
    
    # Find differences
    merged = df_a.merge(df_b, on=key, how='outer', indicator=True, suffixes=('_a', '_b'))
    
    # Records only in A
    only_a = merged[merged['_merge'] == 'left_only']
    print(f"Only in {source_a}: {len(only_a)} records")
    
    # Records only in B
    only_b = merged[merged['_merge'] == 'right_only']
    print(f"Only in {source_b}: {len(only_b)} records")
    
    # Records in both but different values
    both = merged[merged['_merge'] == 'both']
    for col in df_a.columns:
        if col == key:
            continue
        col_a = f"{col}_a"
        col_b = f"{col}_b"
        if col_a in both.columns and col_b in both.columns:
            diff = both[both[col_a] != both[col_b]]
            if len(diff) > 0:
                print(f"Column {col}: {len(diff)} mismatches")
    
    return merged

# Example
discrepancies = reconcile_sources('users', 'users_replica', 'user_id')
```

---

## Reconciliation Patterns

### Pattern 1: Count Reconciliation
```sql
-- Compare counts
SELECT
  'source_a' as source,
  COUNT(*) as count
FROM source_a.users
WHERE created_at::date = '2024-01-16'

UNION ALL

SELECT
  'source_b',
  COUNT(*)
FROM source_b.users
WHERE created_at::date = '2024-01-16';

-- Expected: Counts should match
```

### Pattern 2: Sum Reconciliation
```sql
-- Compare aggregates
SELECT
  'orders' as source,
  SUM(amount) as total_amount,
  COUNT(*) as order_count
FROM orders
WHERE order_date = '2024-01-16'

UNION ALL

SELECT
  'billing',
  SUM(charge_amount),
  COUNT(*)
FROM billing_records
WHERE charge_date = '2024-01-16';

-- Expected: Totals should match
```

### Pattern 3: Key Reconciliation
```sql
-- Find missing keys
SELECT user_id
FROM source_a.users
WHERE created_at::date = '2024-01-16'

EXCEPT

SELECT user_id
FROM source_b.users
WHERE created_at::date = '2024-01-16';

-- Output: user_ids in A but not in B
```

---

## Automated Reconciliation

```python
# Daily reconciliation job
def daily_reconciliation():
    """Run daily reconciliation checks"""
    
    checks = [
        {
            'name': 'user_count',
            'query_a': 'SELECT COUNT(*) FROM users',
            'query_b': 'SELECT COUNT(*) FROM users_replica',
            'tolerance': 0  # Must match exactly
        },
        {
            'name': 'order_total',
            'query_a': 'SELECT SUM(amount) FROM orders WHERE date = CURRENT_DATE',
            'query_b': 'SELECT SUM(amount) FROM billing WHERE date = CURRENT_DATE',
            'tolerance': 0.01  # Allow 1% difference
        }
    ]
    
    for check in checks:
        result_a = db_a.query(check['query_a'])[0][0]
        result_b = db_b.query(check['query_b'])[0][0]
        
        diff = abs(result_a - result_b)
        diff_pct = diff / result_a if result_a > 0 else 0
        
        if diff_pct > check['tolerance']:
            alert(f"Reconciliation failed: {check['name']}")
            alert(f"Source A: {result_a}, Source B: {result_b}, Diff: {diff_pct:.2%}")
        else:
            print(f"✓ {check['name']} reconciled")

# Schedule
schedule.every().day.at("06:00").do(daily_reconciliation)
```

---

## Summary

**Backfill:** เติมข้อมูลย้อนหลัง

**Process:**
1. Identify gaps
2. Backfill in batches
3. Verify completeness

**Reconciliation:** ตรวจสอบความสอดคล้อง

**Patterns:**
- Count reconciliation
- Sum reconciliation
- Key reconciliation

**Automation:**
- Daily reconciliation jobs
- Alerts on discrepancies
- Auto-fix (if safe)

**Best Practices:**
- Batch processing
- Rate limiting
- Verification
- Audit logging
