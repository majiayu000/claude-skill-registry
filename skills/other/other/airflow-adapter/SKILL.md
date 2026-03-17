---
description: Airflow adapter pattern for v2/v3 API compatibility
globs:
  - src/astro_airflow_mcp/adapters/**
  - src/astro_airflow_mcp/server.py
---

# Airflow Adapter Pattern

Enables compatibility with both Airflow 2.x (`/api/v1`) and 3.x (`/api/v2`).

## Architecture

```
MCP Tool → _get_adapter() → AirflowV2Adapter or AirflowV3Adapter → Airflow API
```

Version is auto-detected at startup.

## Key Files

- `adapters/base.py` - Abstract interface
- `adapters/airflow_v2.py` - Airflow 2.x (`/api/v1`)
- `adapters/airflow_v3.py` - Airflow 3.x (`/api/v2`)

## Related Files

- @api-differences.md - V2 vs V3 field/endpoint differences
- @patterns.md - Implementation patterns

## Quick Reference

```python
adapter = _get_adapter()
dags = adapter.list_dags(limit=100)
run = adapter.trigger_dag_run("my_dag", conf={"key": "value"})
```
