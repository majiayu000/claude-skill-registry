---
name: monitoring-implementation
description: Implement comprehensive monitoring and observability features for Vibe Piper pipelines
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T11:00:04.774Z"
  updated_at: "2026-01-29T11:00:04.774Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Implement metrics collection, logging, error tracking, health checks, and profiling for pipeline observability.

# When To Use
- Adding monitoring/observability to a data pipeline framework
- Tracking pipeline execution metrics
- Implementing structured logging
- Setting up health checks
- Adding performance profiling

# Preconditions
- Existing `src/vibe_piper/` package structure
- Python 3.12+ environment
- UV package manager

# Steps

## 1. Create monitoring module structure
```bash
mkdir -p src/vibe_piper/monitoring
```

## 2. Implement metrics collection (metrics.py)
- Create `MetricType` enum (COUNTER, GAUGE, HISTOGRAM, TIMER, SUMMARY)
- Create `Metric` dataclass (name, value, type, timestamp, labels, unit)
- Create `MetricsSnapshot` dataclass with filtering methods
- Create `MetricsCollector` class with:
  - `start_execution()` / `end_execution()` for pipeline-level metrics
  - `record_metric()` for custom metrics
  - `record_asset_execution()` for AssetResult integration
  - `record_execution_result()` for ExecutionResult integration
  - `get_snapshot()` / `to_dict()` for export
  - Thread-safe implementation with `_lock`

## 3. Implement structured logging (logging.py)
- Create `LogLevel` enum (TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Create `JSONFormatter` for machine-parsable logs
- Create `ColoredFormatter` for console output
- Create `StructuredLogger` wrapper with context support
- Create `log_execution()` context manager for pipeline tracing
- Create `configure_logging()` for setup

## 4. Implement health checks (health.py)
- Create `HealthStatus` enum (HEALTHY, DEGRADED, UNHEALTHY, UNKNOWN)
- Create `HealthCheckResult` dataclass
- Create `HealthChecker` class with:
  - `register_check()` / `unregister_check()` for dynamic checks
  - `run_check()` / `run_all_checks()` for execution
  - `get_overall_health()` for aggregate status
- Create factory functions: `create_disk_space_check()`, `create_memory_check()`

## 5. Implement error aggregation (errors.py)
- Create `ErrorSeverity` enum (LOW, MEDIUM, HIGH, CRITICAL)
- Create `ErrorCategory` enum (VALIDATION, CONNECTION, TRANSFORMATION, IO, TIMEOUT, SYSTEM, UNKNOWN)
- Create `ErrorRecord` dataclass with aggregation support
- Create `ErrorAggregator` class with:
  - `add_error()` for recording errors
  - Aggregation window for similar errors
  - Filtering methods (by severity, category, asset)
  - `get_summary()` for analytics

## 6. Implement profiling (profiling.py)
- Create `ProfileData` dataclass
- Create `Profiler` class with:
  - `@profile` decorator
  - `get_stats()` / `get_history()` for analysis
  - Optional psutil integration for memory tracking
- Create `profile_execution()` context manager

## 7. Update package exports
```bash
# Edit src/vibe_piper/__init__.py
# Add monitoring imports to __all__
```

## 8. Type checking and linting
```bash
uv run mypy src/vibe_piper/monitoring/
uv run ruff check src/vibe_piper/monitoring/ --fix
uv run ruff format src/vibe_piper/monitoring/
```

## 9. Create test suite
```bash
mkdir -p tests/monitoring
```

Create tests for:
- `test_metrics.py`: MetricsCollector, MetricsSnapshot, Metric
- `test_logging.py`: LogLevel, formatters, StructuredLogger, log_execution
- `test_health.py`: HealthChecker, health check functions
- `test_errors.py`: ErrorAggregator, ErrorRecord
- `test_profiling.py`: Profiler, ProfileData

## 10. Integration points
- MetricsCollector integrates with ExecutionEngine via `record_execution_result()`
- StructuredLogger can be used throughout codebase via `get_logger()`
- HealthChecker for system/resource health monitoring
- ErrorAggregator for tracking and alerting on errors

# Examples
```python
from vibe_piper.monitoring import (
    MetricsCollector,
    StructuredLogger,
    HealthChecker,
    ErrorAggregator,
    configure_logging,
)

# Configure logging
configure_logging(level=LogLevel.INFO, format_type="json")

# Collect metrics
metrics = MetricsCollector()
metrics.start_execution("my_pipeline", "run_123")
metrics.record_metric("custom_metric", 42)
metrics.end_execution()

# Health checks
health_checker = HealthChecker()
health_checker.register_check("disk", create_disk_space_check("/tmp"))
results = health_checker.run_all_checks()
```

# Gotchas
- Optional psutil dependency: handle ImportError gracefully
- Thread-safety: use threading.Lock for shared state
- Type safety: use Optional[T] with proper None handling
- MyPy errors: use `type: ignore[import-untyped]` for untyped deps
- Formatter type mismatch: use separate variables for each formatter type
- Datetime arithmetic: coalesce None with `datetime.utcnow()`

# Verification
```bash
uv run pytest tests/monitoring/ -v
uv run mypy src/vibe_piper/monitoring/ strict
```
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
