---
name: dask
description: Dask parallel computing library. Use for scaling pandas.
---

# Dask

Dask scales Python. It looks like Pandas/NumPy but runs on clusters. 2025 updates focus on **High Performance Shuffle** and GPU integration.

## When to Use

- **Big Data**: When data > RAM but < BigQuery scale.
- **Cluster Computing**: Utilizing a Kubernetes cluster for Python functions.
- **Xarray**: Backend for geospatial data.

## Core Concepts

### Collections

`dask.dataframe`, `dask.array`, `dask.bag`.

### Scheduler

Decides where to run tasks (Local Threads, Processes, or Distributed Cluster).

### Dashboard

Real-time visualization of task progress (port 8787).

## Best Practices (2025)

**Do**:

- **Use `dask-expr`**: The new query optimization engine for Dask DataFrames.
- **Use Parquet**: CSVs are distinctively slow in distributed settings.

**Don't**:

- **Don't use for small data**: The overhead of the scheduler makes it slower than Pandas for <1GB.

## References

- [Dask Documentation](https://graph.dask.org/)
