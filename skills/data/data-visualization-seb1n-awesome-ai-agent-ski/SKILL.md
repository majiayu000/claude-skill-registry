---
name: data-visualization
description: Create clear, effective charts and dashboards from structured data using matplotlib, seaborn, and plotly. Use when the user requests data visualization or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Data Visualization

This skill enables an AI agent to transform structured data into meaningful visual representations. The agent selects appropriate chart types based on the data and the question being asked, builds publication-quality static charts with matplotlib and seaborn, and creates interactive visualizations with plotly. It follows established data visualization principles to ensure clarity, accuracy, and visual appeal.

## Workflow

1. **Understand the data and the question.** Examine the dataset's structure — how many variables, what types (numeric, categorical, temporal), and what relationship or comparison the user wants to highlight. The question drives chart selection more than the data alone.

2. **Select the appropriate chart type.** Match the analytical goal to the right visual form. Use bar charts for categorical comparisons, line charts for trends over time, scatter plots for relationships between two continuous variables, histograms for distributions, box plots for spread and outliers, and heatmaps for correlation matrices or dense categorical grids.

3. **Prepare the data for plotting.** Aggregate, pivot, or reshape the data as needed. Sort categorical axes by value for bar charts. Resample time-series to the right granularity. Ensure no NaN values leak into the plot that would create gaps or errors.

4. **Build the visualization with appropriate styling.** Apply consistent color palettes, readable axis labels, descriptive titles, and proper legends. Remove chart junk — unnecessary gridlines, borders, and decorations. Use figure sizes that match the intended output medium (report, slide, dashboard).

5. **Add context and annotations.** Highlight key data points with annotations, reference lines, or shaded regions. Add summary statistics directly on the chart where helpful (e.g., median line on a box plot, trend line on a scatter). Context turns a chart from decoration into analysis.

6. **Export or display.** Save static charts as PNG or SVG for reports, or render interactive HTML for dashboards and exploration. Set DPI to 150+ for print-quality output.

## Supported Technologies

- **matplotlib** — foundational plotting library for full control over every visual element
- **seaborn** — statistical visualization with sensible defaults and built-in themes
- **plotly** — interactive charts with hover tooltips, zoom, and pan
- **plotly.express** — concise API for rapid interactive chart creation

### When to Use Which Chart Type

| Goal | Chart Type | Library |
|------|-----------|---------|
| Compare categories | Bar chart (vertical or horizontal) | matplotlib, seaborn |
| Show trend over time | Line chart | matplotlib, plotly |
| Explore relationship between 2 variables | Scatter plot | seaborn, plotly |
| Show distribution of a variable | Histogram or KDE | seaborn |
| Compare distributions across groups | Box plot or violin plot | seaborn |
| Display correlation matrix | Heatmap | seaborn |
| Show composition / proportions | Stacked bar or pie chart | matplotlib |
| Enable user exploration | Interactive chart | plotly |

## Usage

Provide the agent with a dataset and a description of what you want to visualize. Optionally specify chart type, color preferences, output format, and figure dimensions. The agent will select the best approach if no chart type is specified.

## Examples

### Example 1: Sales dashboard with matplotlib and seaborn

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("quarterly_sales.csv", parse_dates=["date"])
sns.set_theme(style="whitegrid", palette="viridis")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Q4 2024 Sales Dashboard", fontsize=16, fontweight="bold")

# 1. Monthly revenue trend
monthly = df.resample("M", on="date")["revenue"].sum()
axes[0, 0].plot(monthly.index, monthly.values, marker="o", linewidth=2)
axes[0, 0].set_title("Monthly Revenue Trend")
axes[0, 0].set_ylabel("Revenue ($)")
axes[0, 0].tick_params(axis="x", rotation=45)

# 2. Revenue by region (horizontal bar)
region = df.groupby("region")["revenue"].sum().sort_values()
axes[0, 1].barh(region.index, region.values, color=sns.color_palette("viridis", len(region)))
axes[0, 1].set_title("Revenue by Region")
axes[0, 1].set_xlabel("Total Revenue ($)")

# 3. Units sold distribution (histogram)
axes[1, 0].hist(df["units_sold"], bins=30, edgecolor="white", alpha=0.8)
axes[1, 0].axvline(df["units_sold"].median(), color="red", linestyle="--", label="Median")
axes[1, 0].set_title("Units Sold Distribution")
axes[1, 0].legend()

# 4. Revenue vs. discount scatter with regression
sns.regplot(data=df, x="discount", y="revenue", ax=axes[1, 1],
            scatter_kws={"alpha": 0.4, "s": 15}, line_kws={"color": "red"})
axes[1, 1].set_title("Revenue vs. Discount")

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
```

### Example 2: Interactive visualization with plotly

```python
import pandas as pd
import plotly.express as px

df = pd.read_csv("global_sales.csv")

# Interactive scatter with size, color, and hover data
fig = px.scatter(
    df,
    x="marketing_spend",
    y="revenue",
    size="units_sold",
    color="region",
    hover_data=["product_name", "quarter"],
    title="Marketing Spend vs Revenue by Region",
    labels={
        "marketing_spend": "Marketing Spend ($)",
        "revenue": "Revenue ($)",
        "units_sold": "Units Sold"
    },
    template="plotly_white"
)

fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color="DarkSlateGrey")))

# Add a trend line annotation
fig.add_annotation(
    x=45000, y=320000,
    text="Strong ROI cluster:<br>low spend, high revenue",
    showarrow=True, arrowhead=2,
    font=dict(size=12, color="darkblue")
)

fig.write_html("interactive_scatter.html")
fig.show()
# Users can hover over points to see product_name and quarter,
# zoom into clusters, and toggle regions on/off via the legend.
```

## Best Practices

- Choose chart type based on the analytical question, not aesthetics — a scatter plot that reveals no pattern is still the right choice if the question is about correlation.
- Limit color categories to 7 or fewer; beyond that, use faceting or small multiples instead of cramming more colors into a single legend.
- Always label axes with units and use human-readable number formats (e.g., "$1.2M" not "1200000").
- Start bar chart y-axes at zero to avoid exaggerating differences; line charts may use a truncated axis when the focus is on change rather than absolute values.
- Use colorblind-friendly palettes (viridis, cividis, or ColorBrewer qualitative sets) by default.
- Export at 150+ DPI for any chart that will appear in a document or presentation.

## Edge Cases

- **Too many categories for a single chart.** If a bar chart would have more than 15 bars, show the top N and aggregate the rest into an "Other" category, or switch to a treemap.
- **Overlapping points in scatter plots.** Use transparency (`alpha=0.3`), jitter, or hexbin/2D density plots when thousands of points overlap.
- **Long axis labels.** Rotate labels 45 degrees, truncate with ellipsis, or switch to horizontal bar charts to keep text readable.
- **Missing values creating gaps in line charts.** Interpolate small gaps (1-2 points) linearly and mark them with a dashed segment. For larger gaps, break the line to avoid implying continuity.
- **Extremely skewed data.** Apply log-scale axes and note the transformation clearly in the axis label (e.g., "Revenue (log scale)").
