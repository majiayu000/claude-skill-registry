---
name: Data Quality Checks and Validation
description: Implementing comprehensive data quality checks across the data pipeline to ensure accuracy, completeness, and reliability.
---

# Data Quality Checks and Validation

## Overview

Data Quality Checks are automated tests that validate data against predefined rules and expectations. They act as the "unit tests" for data, catching issues before they propagate downstream to analytics, ML models, or business decisions.

**Core Principle**: "Trust but verify. Every data pipeline should have quality gates."

---

## 1. The Six Dimensions of Data Quality

| Dimension | Definition | Example Check |
|-----------|------------|---------------|
| **Accuracy** | Data correctly represents reality | `price` matches source system |
| **Completeness** | All required data is present | `email` field is not null for 100% of users |
| **Consistency** | Data is consistent across systems | `user_id` exists in both `users` and `orders` tables |
| **Timeliness** | Data is up-to-date | Latest record timestamp < 1 hour old |
| **Validity** | Data conforms to format/rules | `email` matches regex pattern |
| **Uniqueness** | No duplicate records | `order_id` has no duplicates |

---

## 2. Data Quality Rules

### Database Constraints
```sql
-- PostgreSQL example
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INT CHECK (age >= 0 AND age <= 150),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    country_code CHAR(2) CHECK (country_code ~ '^[A-Z]{2}$')
);

-- Referential integrity
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id),
    total_amount DECIMAL(10,2) CHECK (total_amount > 0)
);
```

### Application-Level Validation (Pydantic)
```python
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime

class User(BaseModel):
    user_id: str
    email: EmailStr
    age: int = Field(ge=0, le=150)
    country_code: str = Field(regex=r'^[A-Z]{2}$')
    created_at: datetime
    
    @validator('user_id')
    def validate_uuid(cls, v):
        import uuid
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError('Invalid UUID format')
        return v

# Usage
try:
    user = User(
        user_id="550e8400-e29b-41d4-a716-446655440000",
        email="user@example.com",
        age=25,
        country_code="US",
        created_at=datetime.now()
    )
except ValidationError as e:
    print(f"Validation failed: {e}")
```

---

## 3. Great Expectations Framework

Great Expectations is the industry standard for data validation in Python pipelines.

### Installation and Setup
```bash
pip install great_expectations
great_expectations init
```

### Creating Expectations
```python
import great_expectations as ge
import pandas as pd

# Load data
df = ge.read_csv("users.csv")

# Define expectations
df.expect_column_values_to_not_be_null("email")
df.expect_column_values_to_be_unique("user_id")
df.expect_column_values_to_be_between("age", 0, 150)
df.expect_column_values_to_match_regex("email", r"^[\w\.-]+@[\w\.-]+\.\w+$")
df.expect_column_values_to_be_in_set("country_code", ["US", "CA", "GB", "DE"])

# Validate
validation_result = df.validate()

if not validation_result["success"]:
    print("Data quality check failed!")
    for result in validation_result["results"]:
        if not result["success"]:
            print(f"Failed: {result['expectation_config']['expectation_type']}")
```

### Great Expectations Suite Configuration
```yaml
# great_expectations/expectations/users_suite.json
{
  "expectation_suite_name": "users_suite",
  "expectations": [
    {
      "expectation_type": "expect_column_to_exist",
      "kwargs": {"column": "user_id"}
    },
    {
      "expectation_type": "expect_column_values_to_not_be_null",
      "kwargs": {"column": "email"}
    },
    {
      "expectation_type": "expect_column_values_to_be_between",
      "kwargs": {
        "column": "age",
        "min_value": 0,
        "max_value": 150
      }
    }
  ]
}
```

---

## 4. dbt Data Quality Tests

### Built-in Tests
```yaml
# models/schema.yml
version: 2

models:
  - name: users
    columns:
      - name: user_id
        tests:
          - unique
          - not_null
      
      - name: email
        tests:
          - unique
          - not_null
          - dbt_utils.email_format
      
      - name: age
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 150
      
      - name: created_at
        tests:
          - not_null
          - dbt_utils.recency:
              datepart: hour
              interval: 24
```

### Custom dbt Tests
```sql
-- tests/assert_positive_revenue.sql
SELECT
    order_id,
    total_amount
FROM {{ ref('orders') }}
WHERE total_amount <= 0
```

---

## 5. Data Validation in Pipelines

### Pre-Processing Validation
```python
def validate_input_data(df: pd.DataFrame) -> bool:
    """Validate data before processing"""
    checks = {
        'row_count': len(df) > 0,
        'no_nulls_in_id': df['user_id'].notna().all(),
        'valid_emails': df['email'].str.match(r'^[\w\.-]+@[\w\.-]+\.\w+$').all(),
        'age_range': df['age'].between(0, 150).all()
    }
    
    failed_checks = [k for k, v in checks.items() if not v]
    
    if failed_checks:
        raise ValueError(f"Validation failed: {failed_checks}")
    
    return True

# Usage in pipeline
try:
    validate_input_data(raw_data)
    processed_data = transform(raw_data)
except ValueError as e:
    logger.error(f"Data validation failed: {e}")
    # Quarantine bad data
    raw_data.to_csv(f"quarantine/bad_data_{datetime.now()}.csv")
    raise
```

### Post-Load Validation
```python
def validate_loaded_data(table_name: str, db_connection):
    """Validate data after loading to database"""
    
    # Check row count
    expected_count = get_source_count()
    actual_count = db_connection.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()[0]
    
    assert actual_count == expected_count, \
        f"Row count mismatch: expected {expected_count}, got {actual_count}"
    
    # Check for nulls in critical columns
    null_check = db_connection.execute(f"""
        SELECT COUNT(*) 
        FROM {table_name} 
        WHERE user_id IS NULL OR email IS NULL
    """).fetchone()[0]
    
    assert null_check == 0, f"Found {null_check} rows with null critical fields"
    
    # Check data freshness
    latest_timestamp = db_connection.execute(f"""
        SELECT MAX(created_at) FROM {table_name}
    """).fetchone()[0]
    
    age_hours = (datetime.now() - latest_timestamp).total_seconds() / 3600
    assert age_hours < 2, f"Data is {age_hours} hours old (threshold: 2 hours)"
```

---

## 6. Anomaly Detection

### Statistical Methods
```python
import numpy as np
from scipy import stats

def detect_anomalies_zscore(data: pd.Series, threshold: float = 3.0):
    """Detect anomalies using Z-score method"""
    z_scores = np.abs(stats.zscore(data))
    anomalies = data[z_scores > threshold]
    return anomalies

def detect_anomalies_iqr(data: pd.Series):
    """Detect anomalies using Interquartile Range"""
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    anomalies = data[(data < lower_bound) | (data > upper_bound)]
    return anomalies

# Usage
daily_revenue = df.groupby('date')['revenue'].sum()
revenue_anomalies = detect_anomalies_zscore(daily_revenue)

if len(revenue_anomalies) > 0:
    alert(f"Revenue anomalies detected: {revenue_anomalies}")
```

### ML-Based Anomaly Detection
```python
from sklearn.ensemble import IsolationForest

def detect_anomalies_ml(df: pd.DataFrame, features: list):
    """Detect anomalies using Isolation Forest"""
    model = IsolationForest(contamination=0.01, random_state=42)
    
    # Fit and predict
    predictions = model.fit_predict(df[features])
    
    # -1 indicates anomaly
    anomalies = df[predictions == -1]
    return anomalies

# Usage
anomalies = detect_anomalies_ml(
    df, 
    features=['order_count', 'total_revenue', 'avg_order_value']
)
```

---

## 7. Data Profiling

```python
import pandas as pd

def profile_dataframe(df: pd.DataFrame) -> dict:
    """Generate comprehensive data profile"""
    profile = {
        'row_count': len(df),
        'column_count': len(df.columns),
        'columns': {}
    }
    
    for col in df.columns:
        profile['columns'][col] = {
            'dtype': str(df[col].dtype),
            'null_count': df[col].isna().sum(),
            'null_percentage': df[col].isna().mean() * 100,
            'unique_count': df[col].nunique(),
            'cardinality': df[col].nunique() / len(df) * 100
        }
        
        # Numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):
            profile['columns'][col].update({
                'min': df[col].min(),
                'max': df[col].max(),
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std()
            })
        
        # String columns
        elif pd.api.types.is_string_dtype(df[col]):
            profile['columns'][col].update({
                'min_length': df[col].str.len().min(),
                'max_length': df[col].str.len().max(),
                'avg_length': df[col].str.len().mean()
            })
    
    return profile
```

---

## 8. Handling Data Quality Failures

### Strategy 1: Fail Pipeline
```python
def process_with_strict_validation(data):
    """Fail entire pipeline on any validation error"""
    if not validate_data(data):
        raise DataQualityError("Validation failed - stopping pipeline")
    
    return transform(data)
```

### Strategy 2: Quarantine Bad Data
```python
def process_with_quarantine(data):
    """Separate good and bad data"""
    valid_data = data[validate_rows(data)]
    invalid_data = data[~validate_rows(data)]
    
    if len(invalid_data) > 0:
        invalid_data.to_csv(f"quarantine/{datetime.now()}.csv")
        alert(f"Quarantined {len(invalid_data)} invalid rows")
    
    return transform(valid_data)
```

### Strategy 3: Alert and Continue
```python
def process_with_alerts(data):
    """Log issues but continue processing"""
    validation_results = validate_data(data)
    
    if not validation_results['success']:
        alert(f"Data quality issues: {validation_results['failures']}")
        log_to_monitoring(validation_results)
    
    # Continue processing anyway
    return transform(data)
```

---

## 9. Data Quality Metrics

```python
def calculate_dq_score(validation_results: dict) -> float:
    """Calculate overall data quality score (0-100)"""
    total_checks = len(validation_results)
    passed_checks = sum(1 for r in validation_results.values() if r['passed'])
    
    return (passed_checks / total_checks) * 100

# Track over time
dq_scores = []
for date, data in daily_data.items():
    results = validate_data(data)
    score = calculate_dq_score(results)
    dq_scores.append({'date': date, 'score': score})

# Alert if score drops
if score < 95:
    alert(f"Data quality score dropped to {score}%")
```

---

## 10. Tools Comparison

| Tool | Best For | Pros | Cons |
|------|----------|------|------|
| **Great Expectations** | Python pipelines | Comprehensive, well-documented | Learning curve |
| **dbt tests** | SQL transformations | Integrated with dbt, simple | Limited to SQL |
| **Soda** | Collaboration | Business-friendly, SaaS | Paid for advanced features |
| **Monte Carlo** | Observability | ML-based anomaly detection | Expensive |

---

## 11. Real-World Data Quality Issues

### Case Study: The Missing Orders
- **Problem**: 10% of orders missing from data warehouse
- **Root Cause**: ETL pipeline skipped records with null `shipping_address`
- **Solution**: Added validation to fail pipeline if > 1% of records are skipped
- **Prevention**: Implemented pre-load row count validation

### Case Study: The Duplicate Customers
- **Problem**: Same customer appearing multiple times with different IDs
- **Root Cause**: No uniqueness check on email during ingestion
- **Solution**: Added UNIQUE constraint on email, deduplication logic
- **Prevention**: Implemented fuzzy matching for duplicate detection

---

## 12. Data Quality Checklist

- [ ] **Completeness**: Are all required fields populated?
- [ ] **Uniqueness**: Are primary keys truly unique?
- [ ] **Validity**: Do all fields match expected formats?
- [ ] **Consistency**: Is data consistent across related tables?
- [ ] **Freshness**: Is data updated within SLA?
- [ ] **Accuracy**: Have we validated against source systems?
- [ ] **Monitoring**: Are we tracking DQ metrics over time?
- [ ] **Alerting**: Do we get notified of quality degradation?

---

## Related Skills
- `43-data-reliability/data-contracts`
- `43-data-reliability/schema-management`
- `43-data-reliability/data-lineage`
