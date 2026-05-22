---
name: "data-analysis"
description: "Executive-grade data analysis with pandas/polars and McKinsey-quality visualizations. Use when: analyze data, build dashboard, create charts, investor presentation, SaaS metrics, cohort analysis, visualize, pandas, streamlit, executive summary."
---

# Data Analysis Skill

Executive-grade data analysis for VC, PE, C-suite presentations using pandas, polars, Plotly, Altair, and Streamlit.

## Quick Reference

| Task | Tools | Output |
|------|-------|--------|
| Data ingestion | pandas, polars, pdfplumber, python-pptx | DataFrame |
| Wrangling | pandas/polars transforms | Clean dataset |
| Analysis | numpy, scipy, statsmodels | Insights |
| Visualization | Plotly, Altair, Seaborn | Charts |
| Dashboards | Streamlit, DuckDB | Interactive apps |
| Presentations | Plotly export, PDF generation | Investor-ready |

## Data Ingestion Patterns

### Universal Data Loader

```python
import pandas as pd
import polars as pl
from pathlib import Path

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from any common format."""
    path = Path(file_path)
    suffix = path.suffix.lower()

    loaders = {
        '.csv': lambda p: pd.read_csv(p),
        '.xlsx': lambda p: pd.read_excel(p, engine='openpyxl'),
        '.xls': lambda p: pd.read_excel(p, engine='xlrd'),
        '.json': lambda p: pd.read_json(p),
        '.parquet': lambda p: pd.read_parquet(p),
        '.sql': lambda p: pd.read_sql(open(p).read(), conn),
        '.md': lambda p: parse_markdown_tables(p),
        '.pdf': lambda p: extract_pdf_tables(p),
        '.pptx': lambda p: extract_pptx_tables(p),
    }

    if suffix not in loaders:
        raise ValueError(f"Unsupported format: {suffix}")

    return loaders[suffix](path)
```

### PDF Table Extraction

```python
import pdfplumber

def extract_pdf_tables(pdf_path: str) -> pd.DataFrame:
    """Extract tables from PDF using pdfplumber."""
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table and len(table) > 1:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)

    return pd.concat(all_tables, ignore_index=True) if all_tables else pd.DataFrame()
```

### PowerPoint Data Extraction

```python
from pptx import Presentation
from pptx.util import Inches

def extract_pptx_tables(pptx_path: str) -> list[pd.DataFrame]:
    """Extract all tables from PowerPoint."""
    prs = Presentation(pptx_path)
    tables = []

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_table:
                table = shape.table
                data = []
                for row in table.rows:
                    data.append([cell.text for cell in row.cells])
                df = pd.DataFrame(data[1:], columns=data[0])
                tables.append(df)

    return tables
```

## Data Wrangling Patterns

### Polars for Performance (30x faster than pandas)

```python
import polars as pl

# Lazy evaluation for large datasets
df = (
    pl.scan_csv("large_file.csv")
    .filter(pl.col("revenue") > 0)
    .with_columns([
        (pl.col("revenue") / pl.col("customers")).alias("arpu"),
        pl.col("date").str.to_date().alias("date_parsed"),
    ])
    .group_by("segment")
    .agg([
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("customers").mean().alias("avg_customers"),
    ])
    .collect()
)
```

### Common Transformations

```python
def prepare_for_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Standard data prep pipeline."""
    return (df
        .dropna(subset=['key_column'])
        .drop_duplicates()
        .assign(
            date=lambda x: pd.to_datetime(x['date']),
            revenue=lambda x: pd.to_numeric(x['revenue'], errors='coerce'),
            month=lambda x: x['date'].dt.to_period('M'),
        )
        .sort_values('date')
        .reset_index(drop=True)
    )
```

## SaaS Metrics Calculations

### Core Metrics

```python
def calculate_saas_metrics(df: pd.DataFrame) -> dict:
    """Calculate key SaaS metrics for investor reporting."""

    # MRR / ARR
    mrr = df.groupby('month')['mrr'].sum()
    arr = mrr.iloc[-1] * 12

    # Growth rates
    mrr_growth = mrr.pct_change().iloc[-1]

    # Churn
    churned = df[df['status'] == 'churned']['mrr'].sum()
    total_mrr = df['mrr'].sum()
    churn_rate = churned / total_mrr if total_mrr > 0 else 0

    # CAC & LTV
    total_sales_marketing = df['sales_cost'].sum() + df['marketing_cost'].sum()
    new_customers = df[df['is_new']]['customer_id'].nunique()
    cac = total_sales_marketing / new_customers if new_customers > 0 else 0

    avg_revenue_per_customer = df.groupby('customer_id')['mrr'].mean().mean()
    avg_lifespan_months = 1 / churn_rate if churn_rate > 0 else 36
    ltv = avg_revenue_per_customer * avg_lifespan_months

    ltv_cac_ratio = ltv / cac if cac > 0 else 0
    cac_payback_months = cac / avg_revenue_per_customer if avg_revenue_per_customer > 0 else 0

    return {
        'mrr': mrr.iloc[-1],
        'arr': arr,
        'mrr_growth': mrr_growth,
        'churn_rate': churn_rate,
        'cac': cac,
        'ltv': ltv,
        'ltv_cac_ratio': ltv_cac_ratio,
        'cac_payback_months': cac_payback_months,
    }
```

### Cohort Analysis

```python
def cohort_retention_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Build cohort retention matrix for investor reporting."""

    # Assign cohort (first purchase month)
    df['cohort'] = df.groupby('customer_id')['date'].transform('min').dt.to_period('M')
    df['period'] = df['date'].dt.to_period('M')
    df['cohort_age'] = (df['period'] - df['cohort']).apply(lambda x: x.n)

    # Build retention matrix
    cohort_data = df.groupby(['cohort', 'cohort_age']).agg({
        'customer_id': 'nunique',
        'revenue': 'sum'
    }).reset_index()

    # Pivot for visualization
    cohort_counts = cohort_data.pivot(
        index='cohort',
        columns='cohort_age',
        values='customer_id'
    )

    # Calculate retention percentages
    cohort_sizes = cohort_counts.iloc[:, 0]
    retention = cohort_counts.divide(cohort_sizes, axis=0) * 100

    return retention
```

## Executive Visualization

### McKinsey/BCG Chart Principles

```yaml
mckinsey_style:
  colors:
    primary: "#003366"      # Deep blue
    accent: "#0066CC"       # Bright blue
    positive: "#2E7D32"     # Green
    negative: "#C62828"     # Red
    neutral: "#757575"      # Gray

  typography:
    title: "Georgia, serif"
    body: "Arial, sans-serif"
    size_title: 18
    size_body: 12

  principles:
    - "One message per chart"
    - "Action title (not descriptive)"
    - "Data-ink ratio > 80%"
    - "Remove chartjunk"
    - "Label directly on chart"
```

### Plotly Executive Charts

```python
import plotly.express as px
import plotly.graph_objects as go

EXEC_COLORS = {
    'primary': '#003366',
    'secondary': '#0066CC',
    'positive': '#2E7D32',
    'negative': '#C62828',
    'neutral': '#757575',
}

def exec_line_chart(df, x, y, title):
    """McKinsey-style line chart."""
    fig = px.line(df, x=x, y=y)

    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=18, family="Georgia"),
            x=0,
        ),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, showline=True, linecolor='black'),
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0', showline=True, linecolor='black'),
        margin=dict(l=60, r=40, t=60, b=40),
    )

    fig.update_traces(line=dict(color=EXEC_COLORS['primary'], width=3))

    return fig

def exec_waterfall(values, labels, title):
    """Waterfall chart for revenue/cost breakdown."""
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative"] * (len(values) - 1) + ["total"],
        x=labels,
        y=values,
        connector=dict(line=dict(color="rgb(63, 63, 63)")),
        increasing=dict(marker=dict(color=EXEC_COLORS['positive'])),
        decreasing=dict(marker=dict(color=EXEC_COLORS['negative'])),
        totals=dict(marker=dict(color=EXEC_COLORS['primary'])),
    ))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=18, family="Georgia")),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        showlegend=False,
    )

    return fig
```

### Cohort Heatmap

```python
def cohort_heatmap(retention_df, title="Customer Retention by Cohort"):
    """Publication-quality cohort retention heatmap."""
    import plotly.figure_factory as ff

    fig = px.imshow(
        retention_df.values,
        labels=dict(x="Months Since Acquisition", y="Cohort", color="Retention %"),
        x=list(retention_df.columns),
        y=[str(c) for c in retention_df.index],
        color_continuous_scale='Blues',
        aspect='auto',
    )

    # Add text annotations
    for i, row in enumerate(retention_df.values):
        for j, val in enumerate(row):
            if not pd.isna(val):
                fig.add_annotation(
                    x=j, y=i,
                    text=f"{val:.0f}%",
                    showarrow=False,
                    font=dict(color='white' if val > 50 else 'black', size=10)
                )

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=18, family="Georgia")),
        font=dict(family="Arial", size=12),
    )

    return fig
```

## Streamlit Dashboard Template

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Executive Dashboard", layout="wide")

# Custom CSS for executive styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #003366, #0066CC);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .stMetric label { font-family: Georgia, serif; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("Executive Dashboard")
st.markdown("---")

# KPI Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("MRR", f"${mrr:,.0f}", f"{mrr_growth:+.1%}")
with col2:
    st.metric("ARR", f"${arr:,.0f}", f"{arr_growth:+.1%}")
with col3:
    st.metric("LTV:CAC", f"{ltv_cac:.1f}x", delta_color="normal")
with col4:
    st.metric("Churn", f"{churn:.1%}", f"{churn_delta:+.1%}", delta_color="inverse")

# Charts Row
st.markdown("## Revenue Trend")
st.plotly_chart(exec_line_chart(df, 'month', 'revenue', 'MRR Growth Exceeds Target'), use_container_width=True)

# Cohort Analysis
st.markdown("## Cohort Retention")
st.plotly_chart(cohort_heatmap(retention_df), use_container_width=True)
```

## Investor Presentation Patterns

### Pitch Deck Metrics Sequence

```yaml
investor_metrics_flow:
  1_unit_economics:
    charts: ["CAC vs LTV bar", "LTV:CAC trend line"]
    key_message: "3x+ LTV:CAC proves efficient growth"

  2_mrr_waterfall:
    charts: ["MRR waterfall (new, expansion, churn, contraction)"]
    key_message: "Net revenue retention > 100%"

  3_cohort_retention:
    charts: ["Cohort heatmap", "Revenue retention curve"]
    key_message: "Strong retention = compounding value"

  4_growth_efficiency:
    charts: ["Magic Number", "CAC payback period"]
    key_message: "Efficient growth engine"

  5_projections:
    charts: ["ARR projection with scenarios"]
    key_message: "Clear path to $X ARR"
```

### Action Titles (McKinsey Style)

```markdown
## Bad (Descriptive) → Good (Action)

❌ "Revenue by Quarter"
✅ "Q4 Revenue Exceeded Target by 23%"

❌ "Customer Acquisition Cost"
✅ "CAC Decreased 40% While Maintaining Quality"

❌ "Cohort Analysis"
✅ "90-Day Retention Improved to 85%, Up From 72%"

❌ "Market Size"
✅ "TAM of $4.2B with Clear Path to $500M SAM"
```

## Quick Commands

```python
# Load and analyze any file
df = load_data("data.csv")
metrics = calculate_saas_metrics(df)
retention = cohort_retention_analysis(df)

# Generate executive charts
fig = exec_line_chart(df, 'month', 'mrr', 'MRR Growth Accelerating')
fig.write_html("mrr_chart.html")
fig.write_image("mrr_chart.png", scale=2)

# Run Streamlit dashboard
# streamlit run dashboard.py
```

## Integration Notes

- **Pairs with**: revenue-ops-skill (metrics), pricing-strategy-skill (modeling)
- **Stack**: Python 3.11+, pandas, polars, plotly, altair, streamlit
- **Projects**: coperniq-forge (ROI calculators), thetaroom (trading analysis)
- **NO OPENAI**: Use Claude for narrative generation

## Reference Files

- `reference/chart-gallery.md` - 20+ chart templates with code
- `reference/saas-metrics.md` - Complete SaaS KPI definitions
- `reference/streamlit-patterns.md` - Production dashboard patterns
- `reference/data-wrangling.md` - Format-specific extraction guides
