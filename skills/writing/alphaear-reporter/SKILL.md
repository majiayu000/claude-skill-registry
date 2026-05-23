---
name: alphaear-reporter
description: Plan, write, and edit professional financial reports; generate chart configurations. Use when condensing analysis into a structured output.
---

# AlphaEar Reporter Skill

## Overview

This skill provides a structured workflow for generating professional financial reports. It includes planning, writing, editing, and creating visual aids (charts).

## Capabilities

### 1. Generate Structured Reports

Use `scripts/report_agent.py` logic (referencing `build_structured_report` method logic) to create reports.

**Key Components:**

-   **Plan**: Outline report structure based on input signals/data.
-   **Write**: Generate content for each section.
-   **Edit**: Refine content for clarity and tone.
-   **Charts**: Generate ECharts configurations via `AlphaEarVisualizer` (in `scripts/visualizer.py`).

**Example Usage (Visualizer):**

```python
from scripts.visualizer import AlphaEarVisualizer

# Generate Chart Config
viz = AlphaEarVisualizer()
chart_config = viz.generate_chart_config(
    chart_type="line",
    title="Stock Price Trend",
    data={"x": ["2023-01", "2023-02"], "y": [100, 120]}
)
print(chart_config)
```

## Dependencies

-   `agno` (Agent framework)
-   `sqlite3` (built-in)

Ensure `DatabaseManager` is initialized correctly.
