---
name: plotly
description: Plotly interactive visualization library. Use for interactive charts.
---

# Plotly

Plotly creates **interactive** (zoomable, hoverable) charts in the browser. v6.0 (2025) drops big dependencies (Pandas is optional) and improves performance.

## When to Use

- **Dashboards**: Streamlit, Dash.
- **3D Plots**: Rotating 3D scatter plots.
- **Interactivity**: Users need to drill down into data.

## Core Concepts

### Plotly Express (`px`)

High-level API. `px.scatter(df, x="a", y="b", color="c")`.

### Graph Objects (`go`)

Low-level API. `go.Figure(data=[go.Scatter(...)])`.

### Dash

The framework for building web apps with Plotly charts.

## Best Practices (2025)

**Do**:

- **Use Plotly Express**: It covers 90% of use cases.
- **Use WebGL**: `render_mode='webgl'` for large datasets (>10k points).

**Don't**:

- **Don't use it for static papers**: Use Matplotlib for print.

## References

- [Plotly Python](https://plotly.com/python/)
