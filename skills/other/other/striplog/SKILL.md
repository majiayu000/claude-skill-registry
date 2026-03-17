---
name: striplog
description: |
  Create, visualize, and analyze lithological and stratigraphic logs for well
  data. Use when Claude needs to: (1) Create lithology columns from depth intervals,
  (2) Parse geological descriptions into structured logs, (3) Visualize stratigraphic
  columns with patterns and colors, (4) Perform well-to-well correlations, (5) Extract
  statistics like net-to-gross ratios, (6) Define rock type lexicons and legends,
  (7) Export lithology data to CSV/LAS/JSON.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Lithology, Stratigraphy, Well Correlation, Visualization, Well Logs, Striplog, Net-to-Gross, Sedimentology]
dependencies: [striplog>=0.9.0, matplotlib]
complements: [lasio, welly, petropy]
workflow_role: visualization
---

# striplog - Lithological Logs

## Quick Reference

```python
from striplog import Striplog, Interval, Component

# Create from intervals
intervals = [
    Interval(top=0, base=10, components=[Component({'lithology': 'sandstone'})]),
    Interval(top=10, base=25, components=[Component({'lithology': 'shale'})]),
    Interval(top=25, base=40, components=[Component({'lithology': 'limestone'})]),
]
strip = Striplog(intervals)

# Load from file
strip = Striplog.from_csv('lithology.csv')  # Columns: top, base, lithology

# Access and display
print(strip)
strip.plot()
df = strip.to_dataframe()
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `Striplog` | Main log container - holds intervals |
| `Interval` | Depth interval with top, base, and components |
| `Component` | Rock type definition with properties |
| `Lexicon` | Rock type dictionary with synonyms |
| `Legend` | Visualization styles (colors, patterns) |

## Essential Operations

### Create from CSV
```python
# CSV format: top,base,lithology
strip = Striplog.from_csv('lithology.csv')
strip.plot()
```

### Create from Description Text
```python
from striplog import Striplog, Lexicon

description = """
0.0 - 5.5 m: Fine to medium sandstone
5.5 - 12.0 m: Grey shale with silt laminations
12.0 - 18.5 m: Massive limestone, fossiliferous
"""
strip = Striplog.from_description(description, lexicon=lexicon)
```

### Query and Extract
```python
# Get interval at depth
interval = strip.read_at(z=15)
print(interval.primary.lithology)

# Crop to depth range
subset = strip.crop((10, 30))

# Unique lithologies
lithologies = strip.unique('lithology')
```

### Statistics
```python
# Net-to-gross for specific lithology
ntg = strip.net_to_gross(pattern={'lithology': 'sandstone'})
print(f"Sandstone: {ntg * 100:.1f}%")

# Merge adjacent same-lithology intervals
merged = strip.merge_neighbours()
```

### Well Correlation
```python
import matplotlib.pyplot as plt

wells = [Striplog.from_csv(f'well{i}.csv') for i in range(1, 4)]
fig, axes = plt.subplots(1, 3, figsize=(10, 8), sharey=True)

for ax, well, name in zip(axes, wells, ['Well 1', 'Well 2', 'Well 3']):
    well.plot(ax=ax, legend=legend)
    ax.set_title(name)

plt.tight_layout()
plt.savefig('correlation.png')
```

### Export
```python
strip.to_csv('output.csv')
strip.to_las('output.las')
strip.to_json('output.json')
df = strip.to_dataframe()
```

## Hatch Patterns

| Pattern | Code | Typical Use |
|---------|------|-------------|
| Dots | `...` | Sandstone |
| Dashes | `---` | Shale |
| Plus | `+++` | Limestone |
| X | `xxx` | Dolomite |
| V | `vvv` | Volcanic |

## When to Use vs Alternatives

| Tool | Best For |
|------|----------|
| **striplog** | Structured lithology logs, interval-based data, NTG, correlation |
| **welly** | Well log curves (continuous data), multi-well projects |
| **custom matplotlib** | Simple one-off stratigraphic columns without interval logic |

**Use striplog when** you need to represent geological intervals (lithology,
facies) as structured objects with querying, statistics, and correlation.

**Use welly instead** when working with continuous well log curves (GR, RHOB).
Welly and striplog complement each other -- welly for curves, striplog for
lithology intervals.

**Use custom matplotlib instead** for simple, one-off stratigraphic columns
where you don't need interval querying or net-to-gross calculations.

## Common Workflows

### Create lithological log from CSV data
```
- [ ] Prepare CSV with columns: top, base, lithology (optionally color)
- [ ] Load with `Striplog.from_csv('lithology.csv')`
- [ ] Define Legend with colors and hatch patterns for each lithology
- [ ] Verify intervals: check for gaps or overlaps
- [ ] Merge adjacent same-lithology intervals with `merge_neighbours()`
- [ ] Compute statistics: `net_to_gross()`, `unique()`
- [ ] Plot with legend and export to desired format
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Text not parsing | Define a Lexicon with synonyms |
| Wrong colors | Create custom Legend with Decor objects |
| Gaps in log | Check interval top/base values match |
| Plot looks wrong | Verify depth direction (increasing down) |

## References

- **[Lexicon Configuration](references/lexicon.md)** - Rock type dictionaries and synonyms
- **[Component Definitions](references/components.md)** - Properties and multi-attribute intervals

## Scripts

- **[scripts/create_striplog.py](scripts/create_striplog.py)** - Create striplog from CSV or text data
