---
name: data-pipeline-patterns
description: Follow these patterns when implementing data pipelines, ETL, data ingestion, or data validation in OptAIC. Use for point-in-time (PIT) correctness, Arrow schemas, quality checks, and Prefect orchestration.
---

# Data Pipeline Patterns

Guide for implementing data pipelines that integrate with OptAIC's orchestration and governance.

## When to Use

Apply when:
- Building PipelineDef implementations (ETL, Expression, Training)
- Implementing data ingestion flows
- Creating data quality validation
- Setting up Arrow schemas for datasets
- Integrating with Prefect orchestration

## Pipeline Definition Types

| Type | Purpose | Input | Output |
|------|---------|-------|--------|
| ETL | External data ingestion | API/files | Dataset version |
| Expression | DSL transformation | Datasets | Derived dataset |
| Training | Model training | Datasets | Model artifact |
| Inference | Model prediction | Features + model | Prediction dataset |
| Monitoring | Quality/drift checks | Datasets | Metrics + alerts |

## Point-in-Time (PIT) Correctness

**Critical rule**: Always track `knowledge_date` (when data was known) separately from `as_of_date` (data's effective date).

```python
# WRONG - lookahead bias
df = pd.read_sql("SELECT * FROM prices WHERE date = ?", [target_date])

# CORRECT - PIT query
df = pd.read_sql("""
    SELECT * FROM prices
    WHERE as_of_date <= ?
    AND knowledge_date <= ?
    ORDER BY knowledge_date DESC
""", [target_date, knowledge_cutoff])
```

See [references/pit-patterns.md](references/pit-patterns.md).

## Arrow Schema Pattern

```python
import pyarrow as pa

def price_schema() -> pa.Schema:
    return pa.schema([
        pa.field("date", pa.date32(), nullable=False),
        pa.field("symbol", pa.string(), nullable=False),
        pa.field("close", pa.float64(), nullable=False),
        pa.field("knowledge_date", pa.timestamp("us"), nullable=False),
    ])
```

## Prefect Integration

```python
from prefect import flow, task

@task
async def fetch_data(source: str, date: str) -> dict:
    pass

@task
async def validate_schema(data: dict, schema_ref: str) -> bool:
    pass

@flow
async def daily_refresh(dataset_id: UUID, date: str):
    raw = await fetch_data(...)
    if not await validate_schema(raw, schema_ref):
        raise ValidationError()
    await store_data(raw, dataset_id)
    await emit_activity("dataset.refreshed", ...)
```

See [references/prefect-patterns.md](references/prefect-patterns.md).

## Lineage DAG at Creation Time

**CRITICAL**: Lineage DAG is built when Instances are CREATED, NOT at execution time.

```python
from libs.orchestration import LineageResolver

# At DatasetInstance creation:
async def create_dataset_instance(session, actor, payload):
    resolver = LineageResolver()

    # 1. Build lineage DAG from pipeline config
    dag = await resolver.build_dag_for_instance(session, instance.id, actor.tenant_id)

    # 2. Cache upstream IDs for fast execution checks
    if dag.has_dependencies:
        instance.upstream_resource_ids = dag.upstream_ids
        instance.upstream_status = {str(uid): "unknown" for uid in dag.upstream_ids}

        # 3. Create DatasetLineage + Subscription records
        await resolver.create_lineage_and_subscriptions(session, dag)
```

## Pub/Sub Observer Pattern

Downstream datasets are notified when upstreams complete:

```python
from libs.orchestration import LineageObserver, CentrifugoNotifier

async def on_run_completed(session, run):
    observer = LineageObserver()

    # Notify downstreams, get those now fully ready
    ready_ids = await observer.on_upstream_completed(
        session,
        upstream_id=run.dataset_instance_id,
        run_id=run.resource_id,
    )

    # Publish real-time notifications
    notifier = CentrifugoNotifier()
    for downstream_id in ready_ids:
        await notifier.notify_upstream_ready(downstream_id, upstream_id, True)
```

## Fast Execution Check

Use cached status for execution checks (no lineage query):

```python
from libs.orchestration import LineageResolver

resolver = LineageResolver()
all_ready = await resolver.check_all_upstreams_ready(session, instance_id)

if not all_ready and not force:
    raise UpstreamNotReadyError(...)
```

## UpdateFrequency Configuration

Configure expected update frequency for freshness calculations:

```python
from libs.orchestration import UpdateFrequency

# Daily data, 1 day grace period
frequency = UpdateFrequency(
    frequency="daily",
    grace_period_days=1,
)

# Business days only (skip weekends)
frequency = UpdateFrequency(
    frequency="daily",
    business_days_only=True,
    grace_period_days=1,
)

# Weekly on Monday
frequency = UpdateFrequency(
    frequency="weekly",
    day_of_week=0,  # 0=Monday
)

# Store in Instance config_json
config = {
    "update_frequency": {
        "frequency": "daily",
        "business_days_only": True,
        "grace_period_days": 1,
    }
}
```

See [references/lineage-patterns.md](references/lineage-patterns.md).

## Data Quality Checks

Standard checks to implement:
- `no_future_dates` - Prevent lookahead
- `no_duplicates` - Key uniqueness
- `coverage_check` - Required dates/symbols
- `schema_conformance` - Arrow schema match

See [references/quality-checks.md](references/quality-checks.md).

## Lazy Import Rule

Heavy deps must be lazy-loaded:
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd
    import pyarrow as pa
```

## Reference Files

- [PIT Patterns](references/pit-patterns.md) - Point-in-time correctness
- [Prefect Patterns](references/prefect-patterns.md) - Orchestration integration
- [Quality Checks](references/quality-checks.md) - Data validation
- [Lineage Patterns](references/lineage-patterns.md) - Dependency and freshness tracking
