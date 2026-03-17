---
name: etl-incremental-patterns
description: Incremental data loading patterns including backfill strategies, CDC, timestamp-based loads, and pipeline orchestration.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# ETL Incremental Patterns

Patterns for incremental data loading and backfill operations.

## Backfill Strategy

```python
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

def backfill_date_range(
    start: date,
    end: date,
    process_fn: callable,
    parallel: int = 4
) -> None:
    """Backfill data for a date range."""
    dates = []
    current = start
    while current <= end:
        dates.append(current)
        current += timedelta(days=1)

    # Process in parallel with controlled concurrency
    with ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = {executor.submit(process_fn, d): d for d in dates}
        for future in as_completed(futures):
            d = futures[future]
            try:
                future.result()
                print(f"Completed: {d}")
            except Exception as e:
                print(f"Failed: {d} - {e}")

# Usage
backfill_date_range(
    start=date(2024, 1, 1),
    end=date(2024, 3, 31),
    process_fn=process_daily_data,
    parallel=4
)
```

## Incremental Load Patterns

### Timestamp-Based Incremental

```python
def incremental_by_timestamp(table: str, timestamp_col: str) -> pd.DataFrame:
    last_run = get_last_run_timestamp(table)
    query = f"""
        SELECT * FROM {table}
        WHERE {timestamp_col} > :last_run
        ORDER BY {timestamp_col}
    """
    df = pd.read_sql(query, engine, params={'last_run': last_run})
    if not df.empty:
        set_last_run_timestamp(table, df[timestamp_col].max())
    return df
```

### Change Data Capture (CDC)

```python
def process_cdc_events(events: list[dict]) -> None:
    for event in events:
        op = event['operation']  # INSERT, UPDATE, DELETE
        data = event['data']

        if op == 'DELETE':
            soft_delete(data['id'])
        else:
            upsert(data)
```

### Full Refresh with Swap

```python
def full_refresh_with_swap(df: pd.DataFrame, table: str) -> None:
    temp_table = f"{table}_temp"
    df.to_sql(temp_table, engine, if_exists='replace', index=False)

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {table}_old"))
        conn.execute(text(f"ALTER TABLE {table} RENAME TO {table}_old"))
        conn.execute(text(f"ALTER TABLE {temp_table} RENAME TO {table}"))
        conn.execute(text(f"DROP TABLE {table}_old"))
```

## Pipeline Orchestration

```python
from enum import Enum
from dataclasses import dataclass, field

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class PipelineStep:
    name: str
    func: callable
    dependencies: list[str] = field(default_factory=list)
    status: StepStatus = StepStatus.PENDING
    error: str | None = None

class Pipeline:
    def __init__(self, name: str):
        self.name = name
        self.steps: dict[str, PipelineStep] = {}

    def add_step(self, name: str, func: callable, depends_on: list[str] = None):
        self.steps[name] = PipelineStep(name, func, depends_on or [])

    def run(self) -> bool:
        for step in self._topological_sort():
            # Skip if dependencies failed
            if any(self.steps[d].status == StepStatus.FAILED for d in step.dependencies):
                step.status = StepStatus.SKIPPED
                continue

            step.status = StepStatus.RUNNING
            try:
                step.func()
                step.status = StepStatus.SUCCESS
            except Exception as e:
                step.status = StepStatus.FAILED
                step.error = str(e)

        return all(s.status == StepStatus.SUCCESS for s in self.steps.values())

    def _topological_sort(self) -> list[PipelineStep]:
        # Implementation of topological sort for dependency ordering
        ...
```

## Load Strategy Decision Matrix

| Scenario | Pattern | When to Use |
|----------|---------|-------------|
| Small tables (<100K rows) | Full refresh | Daily/hourly loads |
| Large tables with timestamps | Timestamp incremental | Continuous sync |
| Source supports CDC | CDC events | Real-time updates |
| One-time historical load | Parallel backfill | Initial migration |
| Critical tables | Swap pattern | Zero-downtime refresh |
