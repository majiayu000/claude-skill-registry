---
name: vaex
description: Vaex out-of-core DataFrames. Use for big data exploration.
---

# Vaex

Vaex is a hidden gem. It uses **Memory Mapping** to open 100GB files instantly on a laptop and visualize them.

## When to Use

- **Visualization**: Plotting 1 billion points via heatmaps.
- **Instant Opening**: No "loading" time for HDF5/Arrow files.
- **String Processing**: Very fast string operations.

## Core Concepts

### Out-of-Core

Data stays on disk. Virtual columns are computed on the fly.

### Binning

Aggregating data into a grid for visualization (heatmap) rather than plotting individual points.

## Best Practices (2025)

**Do**:

- **Convert to HDF5/Arrow**: Vaex shines with these formats.
- **Use it for EDA**: Rapidly exploring massive datasets locally.

**Don't**:

- **Don't use for complex unrelated logic**: It's specialized for columnar aggregation.

## References

- [Vaex Documentation](https://vaex.io/docs/index.html)
