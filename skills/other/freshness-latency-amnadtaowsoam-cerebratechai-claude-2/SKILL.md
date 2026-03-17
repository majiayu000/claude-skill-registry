---
name: Data Freshness and Latency
description: Monitoring and optimizing how quickly data flows through pipelines and ensuring it meets timeliness requirements.
---

# Data Freshness and Latency

## Overview

Data Freshness measures how current the data is (age), while Latency measures how long it takes for data to flow through the pipeline (processing time). Both are critical for real-time analytics, operational dashboards, and time-sensitive decision-making.

**Core Principle**: "Stale data leads to stale decisions. Monitor freshness, optimize latency."

---

## 1. Freshness vs. Latency

| Metric | Definition | Example | Measurement |
|--------|------------|---------|-------------|
| **Freshness** | How old is the data? | Data is 5 minutes old | `NOW() - MAX(event_timestamp)` |
| **Latency** | How long does processing take? | Pipeline takes 2 minutes | `processing_end_time - event_timestamp` |

### Example
```
Event occurs: 10:00:00
Event arrives in pipeline: 10:00:05 (5 sec ingestion latency)
Processing completes: 10:02:00 (2 min processing latency)
Data queried by user: 10:05:00

Freshness at query time: 5 minutes (10:05 - 10:00)
Total latency: 2 minutes 5 seconds
```

---

## 2. Freshness Requirements by Use Case

| Use Case | Freshness SLO | Acceptable Latency | Example |
|----------|---------------|-------------------|---------|
| **Real-time fraud detection** | < 1 second | < 100ms | Credit card transaction scoring |
| **Live dashboards** | < 1 minute | < 10 seconds | Website analytics |
| **Operational metrics** | < 5 minutes | < 1 minute | Server health monitoring |
| **Business intelligence** | < 1 hour | < 15 minutes | Sales reports |
| **Data warehouse** | < 24 hours | < 4 hours | Historical analysis |
| **Compliance reporting** | < 7 days | Days | Annual audits |

---

## 3. Measuring Data Freshness

### SQL Freshness Check
```sql
-- Check freshness of latest record
SELECT 
    MAX(created_at) as latest_record,
    NOW() as current_time,
    EXTRACT(EPOCH FROM (NOW() - MAX(created_at))) / 60 as age_minutes
FROM events;

-- Alert if data is stale (> 10 minutes old)
SELECT 
    CASE 
        WHEN MAX(created_at) < NOW() - INTERVAL '10 minutes' 
        THEN 'STALE'
        ELSE 'FRESH'
    END as freshness_status
FROM events;
```

### Python Freshness Monitoring
```python
from datetime import datetime, timedelta
import pandas as pd

def check_freshness(df: pd.DataFrame, timestamp_col: str, max_age_minutes: int = 10):
    """Check if data is fresh enough"""
    latest_timestamp = df[timestamp_col].max()
    age = datetime.now() - latest_timestamp
    age_minutes = age.total_seconds() / 60
    
    is_fresh = age_minutes <= max_age_minutes
    
    return {
        'is_fresh': is_fresh,
        'latest_timestamp': latest_timestamp,
        'age_minutes': age_minutes,
        'threshold_minutes': max_age_minutes
    }

# Usage
result = check_freshness(df, 'event_time', max_age_minutes=10)
if not result['is_fresh']:
    alert(f"Data is stale: {result['age_minutes']} minutes old")
```

### dbt Freshness Tests
```yaml
# models/sources.yml
version: 2

sources:
  - name: production
    database: analytics
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    
    tables:
      - name: events
        loaded_at_field: created_at
        freshness:
          warn_after: {count: 10, period: minute}
          error_after: {count: 30, period: minute}
```

---

## 4. Latency Measurement

### End-to-End Pipeline Latency
```python
def measure_pipeline_latency(event_id: str):
    """Measure latency from event to availability"""
    
    # Get event timestamp from source
    event_time = get_event_timestamp(event_id)
    
    # Get processing completion time
    processed_time = get_processed_timestamp(event_id)
    
    # Calculate latency
    latency = (processed_time - event_time).total_seconds()
    
    # Track percentiles
    latency_metrics.observe(latency)
    
    return {
        'event_id': event_id,
        'event_time': event_time,
        'processed_time': processed_time,
        'latency_seconds': latency
    }
```

### Per-Stage Latency Tracking
```python
class PipelineStage:
    def __init__(self, name: str):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, *args):
        self.end_time = datetime.now()
        latency = (self.end_time - self.start_time).total_seconds()
        
        # Log to monitoring
        log_metric(f'pipeline.{self.name}.latency', latency)

# Usage
with PipelineStage('ingestion'):
    ingest_data()

with PipelineStage('transformation'):
    transform_data()

with PipelineStage('loading'):
    load_data()
```

### Prometheus Metrics
```python
from prometheus_client import Histogram

# Define latency histogram
pipeline_latency = Histogram(
    'pipeline_latency_seconds',
    'Time taken for data to flow through pipeline',
    ['stage', 'source'],
    buckets=[0.1, 0.5, 1, 5, 10, 30, 60, 300]  # seconds
)

# Record latency
with pipeline_latency.labels(stage='transform', source='kafka').time():
    transform_data()
```

---

## 5. Freshness Monitoring and Alerting

### Automated Freshness Checks
```python
import schedule
import time

def monitor_freshness():
    """Continuously monitor data freshness"""
    tables = ['events', 'users', 'orders']
    
    for table in tables:
        freshness = check_table_freshness(table)
        
        if not freshness['is_fresh']:
            alert(
                severity='warning',
                message=f"Table {table} is stale: {freshness['age_minutes']} minutes old",
                threshold=freshness['threshold_minutes']
            )

# Run every 5 minutes
schedule.every(5).minutes.do(monitor_freshness)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Watermark Tracking
```python
class WatermarkTracker:
    """Track high-water mark for streaming data"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.watermark = self.load_watermark()
    
    def load_watermark(self) -> datetime:
        """Load last processed timestamp"""
        result = db.execute(
            f"SELECT MAX(processed_at) FROM {self.table_name}_watermark"
        ).fetchone()
        return result[0] if result[0] else datetime.min
    
    def update_watermark(self, timestamp: datetime):
        """Update watermark after processing"""
        db.execute(
            f"INSERT INTO {self.table_name}_watermark (processed_at) VALUES (%s)",
            (timestamp,)
        )
        self.watermark = timestamp
    
    def get_lag(self) -> timedelta:
        """Get lag between watermark and current time"""
        return datetime.now() - self.watermark
    
    def is_lagging(self, threshold_minutes: int = 10) -> bool:
        """Check if processing is lagging"""
        lag_minutes = self.get_lag().total_seconds() / 60
        return lag_minutes > threshold_minutes
```

---

## 6. Improving Freshness

### Change Data Capture (CDC)
```python
# Debezium CDC example
# Instead of batch ETL every hour, stream changes in real-time

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'dbserver1.inventory.customers',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    change_event = message.value
    
    if change_event['op'] == 'c':  # Create
        insert_to_warehouse(change_event['after'])
    elif change_event['op'] == 'u':  # Update
        update_warehouse(change_event['after'])
    elif change_event['op'] == 'd':  # Delete
        delete_from_warehouse(change_event['before'])
```

### Incremental Updates
```sql
-- Instead of full table refresh
-- DELETE FROM target_table;
-- INSERT INTO target_table SELECT * FROM source_table;

-- Use incremental update
INSERT INTO target_table
SELECT * FROM source_table
WHERE updated_at > (SELECT MAX(updated_at) FROM target_table)
ON CONFLICT (id) DO UPDATE SET
    column1 = EXCLUDED.column1,
    updated_at = EXCLUDED.updated_at;
```

### Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

def process_partition(partition_df: pd.DataFrame):
    """Process a partition of data"""
    # Transform and load
    transformed = transform(partition_df)
    load_to_warehouse(transformed)

# Split data into partitions
partitions = np.array_split(large_df, 10)

# Process in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(process_partition, partitions)
```

---

## 7. Trade-offs

### Freshness vs. Cost
```
Real-time streaming (< 1 min freshness):
- Cost: $$$$ (Kafka, Flink, dedicated infrastructure)
- Use when: Fraud detection, live dashboards

Micro-batch (5-15 min freshness):
- Cost: $$ (Spark Streaming, scheduled jobs)
- Use when: Operational metrics, near-real-time analytics

Batch (hourly/daily freshness):
- Cost: $ (Airflow, cron jobs)
- Use when: Reporting, historical analysis
```

### Freshness vs. Completeness
```python
# Trade-off: Wait for all data vs. process what we have

def process_with_timeout(timeout_seconds: int = 300):
    """Process data with timeout to ensure freshness"""
    start_time = time.time()
    data_buffer = []
    
    while time.time() - start_time < timeout_seconds:
        new_data = fetch_data()
        data_buffer.extend(new_data)
        
        if is_complete(data_buffer):
            break  # Got all data
    
    # Process what we have, even if incomplete
    if len(data_buffer) > 0:
        process(data_buffer)
    else:
        alert("No data received within timeout")
```

---

## 8. Freshness SLAs and SLOs

### Defining SLOs
```yaml
# data_freshness_slos.yml
services:
  - name: user_events
    freshness_slo:
      target: 95  # 95% of data should be fresh
      threshold: 5  # within 5 minutes
      measurement_window: 1h
    
  - name: order_analytics
    freshness_slo:
      target: 99
      threshold: 15  # within 15 minutes
      measurement_window: 24h
```

### Measuring SLO Compliance
```python
def calculate_freshness_slo(table_name: str, threshold_minutes: int, window_hours: int = 1):
    """Calculate % of data meeting freshness SLO"""
    
    query = f"""
    SELECT 
        COUNT(*) FILTER (
            WHERE created_at > NOW() - INTERVAL '{threshold_minutes} minutes'
        )::FLOAT / COUNT(*) * 100 as freshness_percent
    FROM {table_name}
    WHERE created_at > NOW() - INTERVAL '{window_hours} hours'
    """
    
    result = db.execute(query).fetchone()
    freshness_percent = result[0]
    
    return {
        'table': table_name,
        'freshness_percent': freshness_percent,
        'threshold_minutes': threshold_minutes,
        'meets_slo': freshness_percent >= 95  # 95% target
    }
```

---

## 9. Tools for Freshness Monitoring

### Monte Carlo Freshness Checks
```yaml
# Monte Carlo automatically monitors freshness
monitors:
  - type: freshness
    table: production.events
    field: created_at
    threshold: 10 minutes
    alert:
      - slack: #data-alerts
      - pagerduty: data-team
```

### Custom Grafana Dashboard
```promql
# Prometheus query for freshness
time() - max(event_timestamp) by (table)

# Alert rule
ALERT DataStale
IF (time() - max(event_timestamp)) > 600  # 10 minutes
FOR 5m
LABELS { severity="warning" }
ANNOTATIONS {
  summary="Data is stale in {{ $labels.table }}",
  description="Latest data is {{ $value }}s old"
}
```

---

## 10. Handling Stale Data

### Fallback to Cached Data
```python
def get_data_with_fallback(cache_ttl_minutes: int = 60):
    """Get fresh data or fall back to cache"""
    
    # Try to get fresh data
    fresh_data = fetch_from_warehouse()
    freshness = check_freshness(fresh_data, 'updated_at', max_age_minutes=10)
    
    if freshness['is_fresh']:
        # Update cache
        cache.set('latest_data', fresh_data, ttl=cache_ttl_minutes * 60)
        return fresh_data
    else:
        # Fall back to cache
        cached_data = cache.get('latest_data')
        if cached_data:
            logger.warning(f"Using cached data (warehouse data is stale)")
            return cached_data
        else:
            raise DataUnavailableError("No fresh or cached data available")
```

### Display Staleness to Users
```python
def get_dashboard_data():
    """Get data with freshness indicator"""
    data = fetch_data()
    freshness = check_freshness(data, 'event_time')
    
    return {
        'data': data,
        'metadata': {
            'last_updated': freshness['latest_timestamp'],
            'age_minutes': freshness['age_minutes'],
            'is_fresh': freshness['is_fresh'],
            'warning': f"Data is {freshness['age_minutes']:.0f} minutes old" if not freshness['is_fresh'] else None
        }
    }
```

---

## 11. Real Freshness Issues

### Case Study: The Stale Dashboard
- **Problem**: Executive dashboard showing yesterday's revenue
- **Root Cause**: ETL job failed at 2 AM, no alerting on freshness
- **Impact**: Wrong business decisions made based on stale data
- **Solution**: Added freshness monitoring with PagerDuty alerts
- **Prevention**: Implemented SLO tracking and automated freshness tests

### Case Study: The Slow Pipeline
- **Problem**: Real-time fraud detection taking 5 minutes (SLO: < 1 second)
- **Root Cause**: Single-threaded processing, no partitioning
- **Solution**: Implemented Kafka partitioning and parallel consumers
- **Result**: Latency reduced from 5 minutes to 200ms

---

## 12. Data Freshness Checklist

- [ ] **SLOs Defined**: Do we have freshness SLOs for each critical table?
- [ ] **Monitoring**: Are we continuously monitoring freshness?
- [ ] **Alerting**: Do we get alerted when data goes stale?
- [ ] **Latency Tracking**: Are we measuring P50/P95/P99 latencies?
- [ ] **Optimization**: Have we optimized for our freshness requirements?
- [ ] **Fallbacks**: Do we have fallback strategies for stale data?
- [ ] **User Communication**: Do we show data age to end users?
- [ ] **SLO Compliance**: Are we meeting our freshness SLOs > 95% of the time?

---

## Related Skills
- `43-data-reliability/data-quality-monitoring`
- `43-data-reliability/data-contracts`
- `42-cost-engineering/infra-sizing`
