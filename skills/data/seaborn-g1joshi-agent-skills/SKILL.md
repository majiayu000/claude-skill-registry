---
name: seaborn
description: Seaborn statistical data visualization. Use for statistical plots.
---

# Seaborn

Seaborn is a high-level wrapper around Matplotlib. It makes **statistical plots** (violins, heatmaps, pairs) easy.

## When to Use

- **Exploratory Data Analysis (EDA)**: Quickly understanding distributions.
- **Statistical Relationships**: "Show me the regression line with confidence intervals".
- **Pandas Models**: Works natively with DataFrames (long-form).

## Core Concepts

### Objects Interface (`so`)

New in v0.12+. A grammar-of-graphics style API (like ggplot2) : `so.Plot(df, x="time", y="val").add(so.Line())`.

### Themes

`sns.set_theme()`.

## Best Practices (2025)

**Do**:

- **Use the Objects Interface**: For composable, complex plots.
- **Use `relplot`, `displot`, `catplot`**: The figure-level functions are more flexible than `scatterplot`.

**Don't**:

- **Don't iterate**: Seaborn handles "hue" and "col" (faceting) automatically.

## References

- [Seaborn Documentation](https://seaborn.pydata.org/)
