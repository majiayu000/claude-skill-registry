---
name: Schema Drift Detection
description: Detecting and managing schema changes that can break data pipelines and downstream consumers.
---

# Schema Drift Detection

## Overview

Schema Drift occurs when the structure of data changes unexpectedly—columns are added, removed, or renamed; data types change; or constraints are modified. These changes can silently break pipelines, queries, and ML models if not detected and managed proactively.

**Core Principle**: "Schema changes are inevitable. Detect them early, manage them gracefully."

---

## 1. What is Schema Drift?

Schema drift is any unplanned or untracked change to the structure of data. Unlike intentional schema evolution (migrations), drift is often accidental and undocumented.

### Common Causes
- Developer adds a column without updating data contracts
- Upstream API changes response structure
- Database migration runs without notification
- Source system vendor updates their schema
- Manual database changes bypass version control

---

## 2. Types of Schema Changes

| Change Type | Example | Impact Level | Breaking? |
|-------------|---------|--------------|-----------|
| **Column Added** | New `middle_name` field | Low | Usually No |
| **Column Removed** | Deleted `fax_number` | High | Yes |
| **Column Renamed** | `user_id` → `customer_id` | Critical | Yes |
| **Data Type Changed** | `price` INT → DECIMAL | High | Maybe |
| **Constraint Added** | `email` now NOT NULL | Medium | Maybe |
| **Constraint Removed** | `age` CHECK removed | Low | No |
| **Table Renamed** | `users` → `customers` | Critical | Yes |
| **Table Dropped** | `temp_table` deleted | Critical | Yes |

---

## 3. Why Schema Drift Matters

### Breaking Data Pipelines
```python
# Pipeline expects 'user_id' column
df = spark.read.parquet("s3://data/users/")
df.select("user_id", "email")  # ❌ Fails if column renamed to 'customer_id'
```

### Breaking Queries
```sql
-- Dashboard query
SELECT user_id, COUNT(*) 
FROM users 
GROUP BY user_id;  -- ❌ Fails if 'user_id' column removed
```

### Breaking ML Models
```python
# Model trained on specific features
model.predict(df[['age', 'income', 'credit_score']])  
# ❌ Fails if 'credit_score' column removed
```

---

## 4. Schema Drift Detection

### Method 1: Automated Schema Monitoring
```python
import pandas as pd
from datetime import datetime

class SchemaMonitor:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.schema_history = []
    
    def capture_schema(self, df: pd.DataFrame) -> dict:
        """Capture current schema"""
        schema = {
            'timestamp': datetime.now(),
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'row_count': len(df)
        }
        return schema
    
    def detect_drift(self, current_df: pd.DataFrame) -> dict:
        """Detect schema changes"""
        current_schema = self.capture_schema(current_df)
        
        if not self.schema_history:
            self.schema_history.append(current_schema)
            return {'drift_detected': False}
        
        previous_schema = self.schema_history[-1]
        
        # Detect changes
        added_columns = set(current_schema['columns']) - set(previous_schema['columns'])
        removed_columns = set(previous_schema['columns']) - set(current_schema['columns'])
        
        dtype_changes = {}
        for col in set(current_schema['columns']) & set(previous_schema['columns']):
            if current_schema['dtypes'][col] != previous_schema['dtypes'][col]:
                dtype_changes[col] = {
                    'old': previous_schema['dtypes'][col],
                    'new': current_schema['dtypes'][col]
                }
        
        drift = {
            'drift_detected': bool(added_columns or removed_columns or dtype_changes),
            'added_columns': list(added_columns),
            'removed_columns': list(removed_columns),
            'dtype_changes': dtype_changes,
            'timestamp': current_schema['timestamp']
        }
        
        if drift['drift_detected']:
            self.alert_drift(drift)
        
        self.schema_history.append(current_schema)
        return drift
    
    def alert_drift(self, drift: dict):
        """Send alert on schema drift"""
        message = f"⚠️ Schema drift detected in {self.table_name}:\n"
        if drift['added_columns']:
            message += f"  Added: {drift['added_columns']}\n"
        if drift['removed_columns']:
            message += f"  Removed: {drift['removed_columns']}\n"
        if drift['dtype_changes']:
            message += f"  Type changes: {drift['dtype_changes']}\n"
        
        # Send to Slack/PagerDuty
        send_alert(message)

# Usage
monitor = SchemaMonitor("users")
drift = monitor.detect_drift(new_data)
```

### Method 2: dbt Schema Tests
```yaml
# models/schema.yml
version: 2

models:
  - name: users
    columns:
      - name: user_id
        tests:
          - not_null
          - unique
      
      - name: email
        tests:
          - not_null
      
      # Test that expected columns exist
      - name: created_at
        tests:
          - not_null

# Custom test for schema stability
tests:
  - name: assert_schema_unchanged
    description: "Fail if schema has changed unexpectedly"
```

### Method 3: Great Expectations Schema Validation
```python
import great_expectations as ge

def validate_schema(df, expected_columns):
    """Validate schema matches expectations"""
    gdf = ge.from_pandas(df)
    
    # Check all expected columns exist
    for col in expected_columns:
        result = gdf.expect_column_to_exist(col)
        if not result['success']:
            raise SchemaError(f"Expected column '{col}' not found")
    
    # Check no unexpected columns
    actual_columns = set(df.columns)
    expected_set = set(expected_columns)
    unexpected = actual_columns - expected_set
    
    if unexpected:
        raise SchemaError(f"Unexpected columns found: {unexpected}")
    
    return True

# Usage
expected_schema = ['user_id', 'email', 'created_at', 'updated_at']
validate_schema(df, expected_schema)
```

---

## 5. Schema Evolution Strategies

### Backward Compatible Changes
```python
# ✅ Safe: Adding optional column
ALTER TABLE users ADD COLUMN middle_name VARCHAR(100);

# ✅ Safe: Making constraint less strict
ALTER TABLE users ALTER COLUMN age DROP NOT NULL;
```

### Forward Compatible Changes
```python
# ✅ Safe: Old code ignores new column
# New schema has 'phone_number', old code doesn't use it
SELECT user_id, email FROM users;  # Still works
```

### Breaking Changes (Require Migration)
```python
# ❌ Breaking: Renaming column
# Solution: Multi-step migration
# Step 1: Add new column
ALTER TABLE users ADD COLUMN customer_id UUID;

# Step 2: Backfill data
UPDATE users SET customer_id = user_id;

# Step 3: Update application to use customer_id

# Step 4: Drop old column (after all consumers migrated)
ALTER TABLE users DROP COLUMN user_id;
```

---

## 6. Handling Schema Changes

### Graceful Degradation
```python
def read_with_fallback(df: pd.DataFrame):
    """Handle schema changes gracefully"""
    # Try new column name first
    if 'customer_id' in df.columns:
        return df['customer_id']
    # Fall back to old column name
    elif 'user_id' in df.columns:
        return df['user_id']
    else:
        raise ValueError("Neither customer_id nor user_id found")
```

### Dynamic Schema Adaptation
```python
def adapt_to_schema(df: pd.DataFrame, required_columns: list):
    """Add missing columns with default values"""
    for col in required_columns:
        if col not in df.columns:
            logger.warning(f"Column '{col}' missing, adding with NULL")
            df[col] = None
    
    return df[required_columns]
```

---

## 7. Tools and Techniques

### Kafka Schema Registry
```python
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# Define schema
value_schema_str = """
{
   "namespace": "my.namespace",
   "name": "User",
   "type": "record",
   "fields" : [
     {"name": "user_id", "type": "string"},
     {"name": "email", "type": "string"}
   ]
}
"""

# Producer enforces schema
avroProducer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
}, default_value_schema=avro.loads(value_schema_str))

# ❌ Fails if data doesn't match schema
avroProducer.produce(topic='users', value={"user_id": "123"})  # Missing email
```

### Monte Carlo Schema Monitoring
```yaml
# Monte Carlo monitors schema automatically
monitors:
  - type: schema_change
    table: production.users
    alert_on:
      - column_added
      - column_removed
      - type_changed
    notification:
      - slack: #data-alerts
      - pagerduty: data-team
```

---

## 8. Schema Change Notification

### Automated Alerts
```python
def notify_schema_change(table: str, changes: dict):
    """Send notifications on schema changes"""
    
    severity = determine_severity(changes)
    
    if severity == 'critical':
        # Page on-call
        pagerduty.trigger_incident(
            title=f"Critical schema change in {table}",
            details=changes
        )
    elif severity == 'warning':
        # Slack notification
        slack.post_message(
            channel='#data-alerts',
            text=f"⚠️ Schema change detected in {table}: {changes}"
        )
    
    # Always log to schema changelog
    log_schema_change(table, changes)

def determine_severity(changes: dict) -> str:
    """Determine severity of schema changes"""
    if changes.get('removed_columns') or changes.get('table_dropped'):
        return 'critical'
    elif changes.get('dtype_changes'):
        return 'warning'
    else:
        return 'info'
```

---

## 9. Database Migration Best Practices

### Migrations in Version Control
```
migrations/
├── 001_create_users_table.sql
├── 002_add_email_column.sql
├── 003_rename_user_id_to_customer_id.sql
└── 004_add_phone_number.sql
```

### Zero-Downtime Migration Pattern
```sql
-- Step 1: Add new column (non-blocking)
ALTER TABLE users ADD COLUMN customer_id UUID;

-- Step 2: Backfill in batches (avoid locking)
DO $$
DECLARE
    batch_size INT := 1000;
    offset_val INT := 0;
BEGIN
    LOOP
        UPDATE users
        SET customer_id = user_id
        WHERE customer_id IS NULL
        LIMIT batch_size;
        
        EXIT WHEN NOT FOUND;
        offset_val := offset_val + batch_size;
        
        -- Pause between batches
        PERFORM pg_sleep(0.1);
    END LOOP;
END $$;

-- Step 3: Add NOT NULL constraint (after backfill complete)
ALTER TABLE users ALTER COLUMN customer_id SET NOT NULL;

-- Step 4: Drop old column (after all apps migrated)
ALTER TABLE users DROP COLUMN user_id;
```

---

## 10. Schema Documentation

### Data Dictionary
```markdown
# Users Table Schema

| Column | Type | Nullable | Description | Added |
|--------|------|----------|-------------|-------|
| user_id | UUID | No | Primary key | 2023-01-01 |
| email | VARCHAR(255) | No | User email address | 2023-01-01 |
| phone_number | VARCHAR(20) | Yes | User phone | 2024-01-15 |
| created_at | TIMESTAMP | No | Account creation time | 2023-01-01 |

## Schema Changes
- 2024-01-15: Added `phone_number` column (optional)
- 2023-06-10: Changed `age` from INT to SMALLINT
```

---

## 11. Real Schema Drift Incidents

### Case Study: The Midnight Migration
- **Incident**: ETL pipeline failed at 2 AM
- **Cause**: Upstream team renamed `user_id` to `customer_id` without notice
- **Impact**: 6 hours of missing data in data warehouse
- **Resolution**: Added schema validation before ETL, implemented change notification process
- **Prevention**: Schema registry with breaking change alerts

### Case Study: The Type Mismatch
- **Incident**: ML model predictions became NaN
- **Cause**: `price` column changed from INT to VARCHAR in source
- **Impact**: Revenue prediction model offline for 12 hours
- **Resolution**: Added type validation in feature pipeline
- **Prevention**: Automated schema tests in CI/CD

---

## 12. Schema Drift Checklist

- [ ] **Monitoring**: Do we have automated schema drift detection?
- [ ] **Alerts**: Are we notified immediately of schema changes?
- [ ] **Validation**: Do pipelines validate schema before processing?
- [ ] **Documentation**: Is schema documented and versioned?
- [ ] **Contracts**: Do we have data contracts with upstream systems?
- [ ] **Testing**: Do we test schema compatibility in CI/CD?
- [ ] **Migration**: Do we have a process for safe schema changes?
- [ ] **Rollback**: Can we rollback schema changes if needed?

---

## Related Skills
- `43-data-reliability/data-contracts`
- `43-data-reliability/schema-management`
- `43-data-reliability/data-quality-checks`
