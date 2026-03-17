---
name: feature-store-design
description: Online/offline feature serving, point-in-time correctness, Feast patterns, and feature computation design.
---

# Feature Store Design

## Architecture Decision Table

| Criteria | Feast (OSS) | Tecton | Vertex Feature Store | Custom (Redis + Warehouse) |
|----------|------------|--------|---------------------|---------------------------|
| Setup cost | Low | High (SaaS) | Medium (GCP-only) | Medium-High |
| Online serving latency | <10ms (Redis) | <5ms | <10ms | Depends on impl |
| Offline store | File/BigQuery/Redshift | Spark/Snowflake | BigQuery | Your warehouse |
| Streaming features | Limited (push-based) | Native Spark/Flink | Dataflow | Build your own |
| Point-in-time joins | Built-in | Built-in | Built-in | Must implement |
| Team size sweet spot | 2-15 | 15-100+ | Any (GCP shops) | 5-20 (eng-heavy) |

**Recommendation**: Feast for most teams. It covers 80% of use cases with minimal operational burden. Go custom only when sub-millisecond latency or complex streaming transformations are hard requirements.

## Feast Feature Definition

### feature_store.yaml

```yaml
project: my_ml_project
registry: gs://my-bucket/feast/registry.pb
provider: gcp
online_store:
  type: redis
  connection_string: redis://10.0.0.5:6379
offline_store:
  type: bigquery
entity_key_serialization_version: 2
```

### Feature Definitions

```python
from datetime import timedelta
from feast import Entity, FeatureView, Field, BatchFeatureView
from feast.types import Float32, Int64, String
from feast.infra.offline_stores.bigquery_source import BigQuerySource

# --- Entities ---
user = Entity(
    name="user_id",
    join_keys=["user_id"],
    description="Unique user identifier",
)

product = Entity(
    name="product_id",
    join_keys=["product_id"],
)

# --- Data Sources ---
user_stats_source = BigQuerySource(
    name="user_stats",
    table="ml_features.user_daily_stats",
    timestamp_field="event_date",
    created_timestamp_column="created_at",
)

# --- Feature Views ---
user_features = BatchFeatureView(
    name="user_features",
    entities=[user],
    ttl=timedelta(days=7),
    schema=[
        Field(name="order_count_30d", dtype=Int64),
        Field(name="avg_order_value_30d", dtype=Float32),
        Field(name="days_since_last_order", dtype=Int64),
        Field(name="lifetime_value", dtype=Float32),
        Field(name="preferred_category", dtype=String),
    ],
    source=user_stats_source,
    online=True,
    tags={"team": "recommendations", "version": "v2"},
)
```

## Point-in-Time Join

The most critical feature store operation. Prevents future data from leaking into training examples.

### How It Works

Given training events with timestamps, join the feature value that was **most recent as of** each event timestamp.

```
Event:   user_id=42, event_time=2024-03-15 10:00:00
Feature: user_id=42, order_count_30d=5, event_date=2024-03-14  <-- correct
Feature: user_id=42, order_count_30d=7, event_date=2024-03-16  <-- FUTURE, must exclude
```

### Feast Point-in-Time Retrieval

```python
from feast import FeatureStore
import pandas as pd

store = FeatureStore(repo_path="feature_repo/")

# Training events with timestamps
entity_df = pd.DataFrame({
    "user_id": [42, 99, 42, 17],
    "event_timestamp": pd.to_datetime([
        "2024-03-15 10:00:00",
        "2024-03-15 14:00:00",
        "2024-03-10 08:00:00",  # same user, earlier time = different features
        "2024-03-12 12:00:00",
    ]),
    "label": [1, 0, 1, 0],
})

# Feast handles point-in-time join automatically
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "user_features:order_count_30d",
        "user_features:avg_order_value_30d",
        "user_features:days_since_last_order",
    ],
).to_df()

# Result: each row gets features AS OF its event_timestamp
```

## Online Serving Setup

### Materialization

```bash
# Materialize features from offline -> online store
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")

# Or in code
store.materialize_incremental(end_date=datetime.utcnow())
```

### Online Retrieval for Inference

```python
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo/")

# Single entity lookup -- low latency for real-time serving
features = store.get_online_features(
    features=[
        "user_features:order_count_30d",
        "user_features:avg_order_value_30d",
        "user_features:lifetime_value",
    ],
    entity_rows=[{"user_id": 42}],
).to_dict()

# Returns: {"user_id": [42], "order_count_30d": [5], ...}
```

### Push-Based Streaming Features

```python
from feast import FeatureStore
from feast.data_source import PushMode
from datetime import datetime
import pandas as pd

store = FeatureStore(repo_path="feature_repo/")

# Push fresh features from a streaming job (Kafka consumer, etc.)
store.push(
    push_source_name="user_realtime_stats",
    df=pd.DataFrame({
        "user_id": [42],
        "session_duration_sec": [340],
        "pages_viewed": [12],
        "event_timestamp": [datetime.utcnow()],
    }),
    to=PushMode.ONLINE,  # or ONLINE_AND_OFFLINE
)
```

## Gotchas and Anti-Patterns

### Training-Serving Skew

**Problem**: Features computed differently at training time (SQL/Spark batch) vs serving time (Python real-time). Model performance degrades in production.

**Fix**: Define feature transformations once. Use Feast on-demand feature views or a shared transformation library. Test by comparing online vs offline retrieval for the same entity+timestamp.

```python
# Detect skew: compare online vs offline for same entities
online = store.get_online_features(
    features=feature_list, entity_rows=entities
).to_df()
offline = store.get_historical_features(
    entity_df=entity_df_now, features=feature_list
).to_df()
# Assert values match within tolerance
```

### Time-Travel Bugs

**Problem**: Using `created_at` instead of `event_date` as the timestamp field. Backfilled data gets `created_at = now()`, making all historical point-in-time joins use the backfilled values.

**Fix**: Always use the business timestamp (when the event occurred), not the ingestion timestamp. Set `timestamp_field` to the event time, use `created_timestamp_column` only for deduplication.

### Feature Freshness

**Problem**: Materialization runs hourly but model expects real-time features. Stale features cause prediction drift.

**Fix**: Monitor feature age. Alert when online store values are older than expected TTL:
```python
# Check feature freshness
metadata = store.get_online_features(
    features=["user_features:order_count_30d"],
    entity_rows=[{"user_id": 42}],
    full_feature_names=True,
)
# Compare event_timestamp against current time
```

### Entity Key Design

**Problem**: Using composite keys like `(user_id, session_id)` when features are really per-user. Creates sparse online store, slow lookups.

**Fix**: One entity per natural grain. Use `user_id` for user features, `(user_id, product_id)` only for interaction features. Keep entity key cardinality manageable for online store memory.

| Entity Pattern | Online Store Size | Lookup Speed | Use Case |
|---------------|------------------|-------------|----------|
| `user_id` | ~N users | Fast | User-level aggregates |
| `product_id` | ~N products | Fast | Product metadata/stats |
| `(user_id, product_id)` | ~N*M | Slow if M is large | Interaction features |
| `session_id` | Unbounded | Degrades over time | Avoid; use TTL aggressively |
