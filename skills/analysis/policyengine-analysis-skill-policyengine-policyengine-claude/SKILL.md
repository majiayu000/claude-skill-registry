---
name: policyengine-analysis
description: Common analysis patterns for PolicyEngine research repositories (CRFB, newsletters, dashboards, impact studies)
---

# PolicyEngine Analysis

Patterns for creating policy impact analyses, dashboards, and research using PolicyEngine.

## For Users 👥

### What are Analysis Repositories?

Analysis repositories produce the research you see on PolicyEngine:

**Blog posts:**
- "How Montana's tax cuts affect poverty"
- "Harris EITC proposal costs and impacts"
- "UK Budget 2024 analysis"

**Dashboards:**
- State tax comparisons
- Policy proposal scorecards
- Interactive calculators (GiveCalc, SALT calculator)

**Research reports:**
- Distributional analyses for organizations
- Policy briefs for legislators
- Impact assessments

### How Analysis Works

1. **Define policy reform** using PolicyEngine parameters
2. **Create household examples** showing specific impacts
3. **Run population simulations** for aggregate effects
4. **Calculate distributional impacts** (who wins, who loses)
5. **Create visualizations** (charts, tables)
6. **Write report** following policyengine-writing-skill style
7. **Publish** to blog or share with stakeholders

### Reading PolicyEngine Analysis

**Key sections in typical analysis:**

**The proposal:**
- What policy changes
- Specific parameter values

**Household impacts:**
- 3-5 example households
- Dollar amounts for each
- Charts showing impact across income range

**Statewide/national impacts:**
- Total cost or revenue
- Winners and losers by income decile
- Poverty and inequality effects

**See policyengine-writing-skill for writing conventions.**

## For Analysts 📊

### When to Use This Skill

- Creating policy impact analyses
- Building interactive dashboards with Streamlit/Plotly
- Writing analysis notebooks
- Calculating distributional impacts
- Comparing policy proposals
- Creating visualizations for research
- Publishing policy research

### Example Analysis Repositories

- `crfb-tob-impacts` - Policy impact analyses
- `newsletters` - Data-driven newsletters
- `2024-election-dashboard` - Policy comparison dashboards
- `marginal-child` - Specialized policy analyses
- `givecalc` - Charitable giving calculator

## Repository Structure

Standard analysis repository structure:

```
analysis-repo/
├── analysis.ipynb           # Main Jupyter notebook
├── app.py                   # Streamlit app (if applicable)
├── requirements.txt         # Python dependencies
├── README.md               # Documentation
├── data/                   # Data files (if needed)
├── outputs/                # Generated charts, tables
└── .streamlit/             # Streamlit config
    └── config.toml
```

## Common Analysis Patterns

### Pattern 1: Impact Analysis Across Income Distribution

```python
import pandas as pd
import numpy as np
from policyengine_us import Simulation

# Define reform
reform = {
    "gov.irs.credits.ctc.amount.base_amount": {
        "2024-01-01.2100-12-31": 5000
    }
}

# Analyze across income distribution
incomes = np.linspace(0, 200000, 101)
results = []

for income in incomes:
    # Baseline
    situation = create_situation(income=income)
    sim_baseline = Simulation(situation=situation)
    tax_baseline = sim_baseline.calculate("income_tax", 2024)[0]

    # Reform
    sim_reform = Simulation(situation=situation, reform=reform)
    tax_reform = sim_reform.calculate("income_tax", 2024)[0]

    results.append({
        "income": income,
        "tax_baseline": tax_baseline,
        "tax_reform": tax_reform,
        "tax_change": tax_reform - tax_baseline
    })

df = pd.DataFrame(results)
```

### Pattern 2: Household-Level Case Studies

```python
# Define representative households
households = {
    "Single, No Children": {
        "income": 40000,
        "num_children": 0,
        "married": False
    },
    "Single Parent, 2 Children": {
        "income": 50000,
        "num_children": 2,
        "married": False
    },
    "Married, 2 Children": {
        "income": 100000,
        "num_children": 2,
        "married": True
    }
}

# Calculate impacts for each
case_studies = {}
for name, params in households.items():
    situation = create_family(**params)

    sim_baseline = Simulation(situation=situation)
    sim_reform = Simulation(situation=situation, reform=reform)

    case_studies[name] = {
        "baseline_tax": sim_baseline.calculate("income_tax", 2024)[0],
        "reform_tax": sim_reform.calculate("income_tax", 2024)[0],
        "ctc_baseline": sim_baseline.calculate("ctc", 2024)[0],
        "ctc_reform": sim_reform.calculate("ctc", 2024)[0]
    }

case_df = pd.DataFrame(case_studies).T
```

### Pattern 3: State-by-State Comparison

```python
states = ["CA", "NY", "TX", "FL", "PA", "OH", "IL", "MI"]

state_results = []
for state in states:
    situation = create_situation(income=75000, state=state)

    sim_baseline = Simulation(situation=situation)
    sim_reform = Simulation(situation=situation, reform=reform)

    state_results.append({
        "state": state,
        "baseline_net_income": sim_baseline.calculate("household_net_income", 2024)[0],
        "reform_net_income": sim_reform.calculate("household_net_income", 2024)[0],
        "change": (sim_reform.calculate("household_net_income", 2024)[0] -
                  sim_baseline.calculate("household_net_income", 2024)[0])
    })

state_df = pd.DataFrame(state_results)
```

### Pattern 4: Marginal Analysis (Winners/Losers)

```python
import plotly.graph_objects as go

# Calculate across income range
situation_with_axes = {
    # ... setup ...
    "axes": [[{
        "name": "employment_income",
        "count": 1001,
        "min": 0,
        "max": 200000,
        "period": 2024
    }]]
}

sim_baseline = Simulation(situation=situation_with_axes)
sim_reform = Simulation(situation=situation_with_axes, reform=reform)

incomes = sim_baseline.calculate("employment_income", 2024)
baseline_net = sim_baseline.calculate("household_net_income", 2024)
reform_net = sim_reform.calculate("household_net_income", 2024)

gains = reform_net - baseline_net

# Identify winners and losers
winners = gains > 0
losers = gains < 0
neutral = gains == 0

print(f"Winners: {winners.sum() / len(gains) * 100:.1f}%")
print(f"Losers: {losers.sum() / len(gains) * 100:.1f}%")
print(f"Neutral: {neutral.sum() / len(gains) * 100:.1f}%")
```

## Visualization Patterns

### Standard Plotly Configuration

```python
import plotly.graph_objects as go

# PolicyEngine brand colors
TEAL = "#39C6C0"
BLUE = "#2C6496"
DARK_GRAY = "#616161"

def create_pe_layout(title, xaxis_title, yaxis_title):
    """Create standard PolicyEngine chart layout."""
    return go.Layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        font=dict(family="Roboto Serif", size=14),
        plot_bgcolor="white",
        hovermode="x unified",
        xaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
            zeroline=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
            zeroline=True
        )
    )

# Use in charts
fig = go.Figure(layout=create_pe_layout(
    "Tax Impact by Income",
    "Income",
    "Tax Change"
))
fig.add_trace(go.Scatter(x=incomes, y=tax_change, line=dict(color=TEAL)))
```

### Common Chart Types

**1. Line Chart (Impact by Income)**
```python
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df.income,
    y=df.tax_change,
    mode='lines',
    name='Tax Change',
    line=dict(color=TEAL, width=3)
))
fig.update_layout(
    title="Tax Impact by Income Level",
    xaxis_title="Income",
    yaxis_title="Tax Change ($)",
    xaxis_tickformat="$,.0f",
    yaxis_tickformat="$,.0f"
)
```

**2. Bar Chart (State Comparison)**
```python
fig = go.Figure()
fig.add_trace(go.Bar(
    x=state_df.state,
    y=state_df.change,
    marker_color=TEAL
))
fig.update_layout(
    title="Net Income Change by State",
    xaxis_title="State",
    yaxis_title="Change ($)",
    yaxis_tickformat="$,.0f"
)
```

**3. Waterfall Chart (Budget Impact)**
```python
fig = go.Figure(go.Waterfall(
    x=["Baseline", "Tax Credit", "Phase-out", "Reform"],
    y=[baseline_revenue, credit_cost, phaseout_revenue, 0],
    measure=["absolute", "relative", "relative", "total"],
    connector={"line": {"color": "gray"}}
))
```

## Streamlit Dashboard Patterns

### Basic Streamlit Setup

```python
import streamlit as st
from policyengine_us import Simulation

st.set_page_config(page_title="Policy Analysis", layout="wide")

st.title("Policy Impact Calculator")

# User inputs
col1, col2, col3 = st.columns(3)
with col1:
    income = st.number_input("Income", value=60000, step=5000)
with col2:
    state = st.selectbox("State", ["CA", "NY", "TX", "FL"])
with col3:
    num_children = st.number_input("Children", value=0, min_value=0, max_value=10)

# Calculate
if st.button("Calculate"):
    situation = create_family(
        parent_income=income,
        num_children=num_children,
        state=state
    )

    sim_baseline = Simulation(situation=situation)
    sim_reform = Simulation(situation=situation, reform=reform)

    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Baseline Tax",
            f"${sim_baseline.calculate('income_tax', 2024)[0]:,.0f}"
        )
    with col2:
        st.metric(
            "Reform Tax",
            f"${sim_reform.calculate('income_tax', 2024)[0]:,.0f}"
        )
    with col3:
        change = (sim_reform.calculate('income_tax', 2024)[0] -
                 sim_baseline.calculate('income_tax', 2024)[0])
        st.metric("Change", f"${change:,.0f}", delta=f"${-change:,.0f}")
```

### Interactive Chart with Streamlit

```python
# Create chart based on user inputs
incomes = np.linspace(0, income_max, 1001)
results = []

for income in incomes:
    situation = create_situation(income=income, state=selected_state)
    sim = Simulation(situation=situation, reform=reform)
    results.append(sim.calculate("household_net_income", 2024)[0])

fig = go.Figure()
fig.add_trace(go.Scatter(x=incomes, y=results, line=dict(color=TEAL)))
st.plotly_chart(fig, use_container_width=True)
```

## Jupyter Notebook Best Practices

### Notebook Structure

```python
# Cell 1: Title and Description
"""
# Policy Analysis: [Policy Name]

**Date:** [Date]
**Author:** [Your Name]

## Summary
Brief description of the analysis and key findings.
"""

# Cell 2: Imports
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from policyengine_us import Simulation

# Cell 3: Configuration
YEAR = 2024
STATES = ["CA", "NY", "TX", "FL"]

# Cell 4+: Analysis sections with markdown headers
```

### Export Results

```python
# Save DataFrame
df.to_csv("outputs/impact_analysis.csv", index=False)

# Save Plotly chart
fig.write_html("outputs/chart.html")
fig.write_image("outputs/chart.png", width=1200, height=600)

# Save summary statistics
summary = {
    "total_winners": winners.sum(),
    "total_losers": losers.sum(),
    "avg_gain": gains[winners].mean(),
    "avg_loss": gains[losers].mean()
}
pd.DataFrame([summary]).to_csv("outputs/summary.csv", index=False)
```

## Repository-Specific Examples

This skill includes example templates in the `examples/` directory:

- `impact_analysis_template.ipynb` - Standard impact analysis
- `dashboard_template.py` - Streamlit dashboard
- `state_comparison.py` - State-by-state analysis
- `case_studies.py` - Household case studies
- `reform_definitions.py` - Common reform patterns

## Common Pitfalls

### Pitfall 1: Not Using Consistent Year
**Problem:** Mixing 2024 and 2025 calculations

**Solution:** Define year constant at top:
```python
CURRENT_YEAR = 2024
# Use everywhere
simulation.calculate("income_tax", CURRENT_YEAR)
```

### Pitfall 2: Inefficient Simulations
**Problem:** Creating new simulation for each income level

**Solution:** Use axes for efficiency:
```python
# SLOW
for income in incomes:
    situation = create_situation(income=income)
    sim = Simulation(situation=situation)
    results.append(sim.calculate("income_tax", 2024)[0])

# FAST
situation_with_axes = create_situation_with_axes(incomes)
sim = Simulation(situation=situation_with_axes)
results = sim.calculate("income_tax", 2024)  # Array of all results
```

### Pitfall 3: Forgetting to Compare Baseline and Reform
**Problem:** Only showing reform results

**Solution:** Always show both:
```python
results = {
    "baseline": sim_baseline.calculate("income_tax", 2024),
    "reform": sim_reform.calculate("income_tax", 2024),
    "change": reform - baseline
}
```

## PolicyEngine API Usage

For larger-scale analyses, use the PolicyEngine API:

```python
import requests

def calculate_via_api(situation, reform=None):
    """Calculate using PolicyEngine API."""
    url = "https://api.policyengine.org/us/calculate"

    payload = {
        "household": situation,
        "policy_id": reform_id if reform else baseline_policy_id
    }

    response = requests.post(url, json=payload)
    return response.json()
```

## Testing Analysis Code

```python
import pytest

def test_reform_increases_ctc():
    """Test that reform increases CTC as expected."""
    situation = create_family(income=50000, num_children=2)

    sim_baseline = Simulation(situation=situation)
    sim_reform = Simulation(situation=situation, reform=reform)

    ctc_baseline = sim_baseline.calculate("ctc", 2024)[0]
    ctc_reform = sim_reform.calculate("ctc", 2024)[0]

    assert ctc_reform > ctc_baseline, "Reform should increase CTC"
    assert ctc_reform == 5000 * 2, "CTC should be $5000 per child"
```

## Documentation Standards

### README Template

```markdown
# [Analysis Name]

## Overview
Brief description of the analysis.

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Methodology
Explanation of approach and data sources.

## How to Run

\```bash
pip install -r requirements.txt
python app.py  # or jupyter notebook analysis.ipynb
\```

## Outputs
- `outputs/chart1.png` - Description
- `outputs/results.csv` - Description

## Contact
PolicyEngine Team - hello@policyengine.org
```

## Additional Resources

- **PolicyEngine API Docs:** https://policyengine.org/us/api
- **Analysis Examples:** https://github.com/PolicyEngine/analysis-notebooks
- **Streamlit Docs:** https://docs.streamlit.io
- **Plotly Docs:** https://plotly.com/python/
