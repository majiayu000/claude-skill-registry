---
name: pyrolite
description: |
  Geochemistry data analysis and visualization for igneous, metamorphic, and
  sedimentary rocks. Use when Claude needs to: (1) Create ternary diagrams for
  compositional data, (2) Plot REE spider diagrams with normalization, (3) Build
  TAS or other classification diagrams, (4) Apply log-ratio transforms to
  compositional data, (5) Calculate CIPW norms, (6) Generate Harker variation
  diagrams, (7) Compute element ratios and anomalies.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Geochemistry, REE, Spider Diagram, TAS, Compositional Data]
dependencies: [pyrolite>=0.3.0, pandas, matplotlib]
complements: []
workflow_role: visualization
---

# pyrolite - Geochemistry Analysis

## Quick Reference

```python
import pandas as pd
import matplotlib.pyplot as plt
from pyrolite.geochem.norm import get_reference_composition

df = pd.read_csv('samples.csv')
df.pyrochem   # Geochemistry methods
df.pyrocomp   # Compositional methods

# Normalize and plot REE
chondrite = get_reference_composition('Chondrite_McDonough1995')
ax = df.pyrochem.normalize_to(chondrite, units='ppm').pyroplot.REE(unity_line=True)
```

## Key Modules

| Module | Purpose |
|--------|---------|
| `pyrolite.plot` | Ternary, spider diagrams |
| `pyrolite.geochem.norm` | Normalization references |
| `pyrolite.comp` | CLR, ALR, ILR transforms |
| `pyrolite.plot.templates` | TAS, Pearce diagrams |
| `pyrolite.mineral.normative` | CIPW norm |

## Essential Operations

### Ternary Diagram
```python
ax = df[['SiO2', 'CaO', 'Na2O']].pyroplot.scatter(c='k', s=50)
```

### TAS Diagram
```python
from pyrolite.plot.templates import TAS
df['Na2O_K2O'] = df['Na2O'] + df['K2O']
ax = TAS()
ax.scatter(df['SiO2'], df['Na2O_K2O'], c='red', s=50)
```

### REE Pattern
```python
chondrite = get_reference_composition('Chondrite_McDonough1995')
ax = df.pyrochem.normalize_to(chondrite, units='ppm').pyroplot.REE(unity_line=True)
```

### Trace Element Spider
```python
pm = get_reference_composition('PM_McDonough1995')
ax = df.pyrochem.normalize_to(pm).pyroplot.spider(unity_line=True)
```

### Compositional Transforms
```python
df_closed = df.pyrocomp.renormalise(scale=100)  # Closure
df_clr = df.pyrocomp.CLR()   # Centered log-ratio
df_alr = df.pyrocomp.ALR()   # Additive log-ratio
df_ilr = df.pyrocomp.ILR()   # Isometric log-ratio
```

### Element Ratios and Anomalies
```python
df['La_Yb'] = df['La'] / df['Yb']                        # LREE/HREE
df['Eu_Eu*'] = df['Eu'] / (df['Sm'] * df['Gd']) ** 0.5   # Eu anomaly
lambdas = df.pyrochem.lambda_lnREE()                      # REE shape
```

### CIPW Norm
```python
from pyrolite.mineral.normative import CIPW_norm
norm = CIPW_norm(df)  # df must have major oxides in wt%
```

### Harker Diagrams
```python
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
for ax, elem in zip(axes.flatten(), ['TiO2', 'Al2O3', 'FeO', 'MgO', 'CaO', 'Na2O']):
    ax.scatter(df['SiO2'], df[elem], c='blue', s=50)
    ax.set_xlabel('SiO2 (wt%)'); ax.set_ylabel(f'{elem} (wt%)')
```

### Pearce Discrimination
```python
from pyrolite.plot.templates import pearce_templates
ax = pearce_templates.YNb()
ax.scatter(df['Nb'], df['Y'], c='red', s=50)
```

## Common Normalization References

| Reference | Code | Use For |
|-----------|------|---------|
| Chondrite | `Chondrite_McDonough1995` | REE patterns |
| Primitive Mantle | `PM_McDonough1995` | Trace elements |
| N-MORB | `NMORB_SunMcDonough1989` | Ocean basalts |
| Upper Crust | `UCC_RudnickGao2003` | Crustal rocks |

## When to Use vs Alternatives

| Tool | Best For | Limitations |
|------|----------|-------------|
| **pyrolite** | Python-native geochemistry, pandas integration, compositional transforms | Fewer built-in classification templates than GCDkit |
| **GCDkit** | Comprehensive classification diagrams, R ecosystem | R-based, not Python |
| **PetroGraph** | Quick GUI-based classification and plotting | Not scriptable, limited customization |
| **Custom matplotlib** | Full control over plot appearance | No built-in normalization or templates |

**Use pyrolite when** you need geochemistry analysis integrated with pandas workflows,
compositional log-ratio transforms, or REE normalization in Python.

**Consider alternatives when** you need extensive petrographic classification templates
(use GCDkit), a quick GUI for classification (use PetroGraph), or only need simple
scatter plots without normalization (use matplotlib directly).

## Common Workflows

### Geochemical classification and REE pattern analysis
- [ ] Load sample data into pandas DataFrame
- [ ] Close compositions with `df.pyrocomp.renormalise(scale=100)`
- [ ] Plot TAS diagram with `TAS()` and overlay sample data
- [ ] Normalize REE to chondrite with `df.pyrochem.normalize_to()`
- [ ] Plot REE spider diagram with `df.pyroplot.REE()`
- [ ] Calculate Eu anomaly and La/Yb ratio
- [ ] Generate Harker variation diagrams for major elements
- [ ] Export figures for publication

## Tips

1. **Close compositions** before analysis (ensure sum to 100%)
2. **Use log-ratios** (CLR/ALR/ILR) for statistical analysis
3. **Choose appropriate normalization** for spider diagrams
4. **Check for Eu anomaly** (positive = cumulate, negative = fractionation)

## References

- **[Normalization References](references/normalization.md)** - Reference compositions and values
- **[Classification Schemes](references/classification.md)** - TAS, Pearce, AFM diagrams

## Scripts

- **[scripts/geochemistry_plots.py](scripts/geochemistry_plots.py)** - Generate common plots
