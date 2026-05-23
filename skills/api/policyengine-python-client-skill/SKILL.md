---
name: policyengine-python-client
description: Using PolicyEngine programmatically via Python client or REST API
---

# PolicyEngine Python Client

This skill covers programmatic access to PolicyEngine for analysts and researchers.

## Installation

```bash
# Install the Python client
pip install policyengine

# Or for local development
pip install policyengine-us  # Just the US model (offline)
```

## Quick Start: Python Client

```python
from policyengine import Simulation

# Create a household
household = {
    "people": {
        "you": {
            "age": {"2024": 30},
            "employment_income": {"2024": 50000}
        }
    },
    "households": {
        "your household": {
            "members": ["you"],
            "state_name": {"2024": "CA"}
        }
    }
}

# Run simulation
sim = Simulation(situation=household, country_id="us")
income_tax = sim.calculate("income_tax", "2024")
```

## For Users: Why Use Python?

**Web app limitations:**
- ✅ Great for exploring policies interactively
- ❌ Can't analyze many households at once
- ❌ Can't automate repetitive analyses
- ❌ Limited customization of charts

**Python benefits:**
- ✅ Analyze thousands of households in batch
- ✅ Automate regular policy analysis
- ✅ Create custom visualizations
- ✅ Integrate with other data sources
- ✅ Reproducible research

## For Analysts: Common Workflows

### Workflow 1: Calculate Your Own Taxes

```python
from policyengine import Simulation

# Your household (more complex than web app)
household = {
    "people": {
        "you": {
            "age": {"2024": 35},
            "employment_income": {"2024": 75000},
            "qualified_dividend_income": {"2024": 5000},
            "charitable_cash_donations": {"2024": 3000}
        },
        "spouse": {
            "age": {"2024": 33},
            "employment_income": {"2024": 60000}
        },
        "child1": {"age": {"2024": 8}},
        "child2": {"age": {"2024": 5}}
    },
    # ... entities setup (see policyengine-us-skill)
}

sim = Simulation(situation=household, country_id="us")

# Calculate specific values
federal_income_tax = sim.calculate("income_tax", "2024")
state_income_tax = sim.calculate("state_income_tax", "2024")
ctc = sim.calculate("ctc", "2024")
eitc = sim.calculate("eitc", "2024")

print(f"Federal income tax: ${federal_income_tax:,.0f}")
print(f"State income tax: ${state_income_tax:,.0f}")
print(f"Child Tax Credit: ${ctc:,.0f}")
print(f"EITC: ${eitc:,.0f}")
```

### Workflow 2: Analyze a Policy Reform

```python
from policyengine import Simulation

# Define reform (increase CTC to $5,000)
reform = {
    "gov.irs.credits.ctc.amount.base_amount": {
        "2024-01-01.2100-12-31": 5000
    }
}

# Compare baseline vs reform
household = create_household()  # Your household definition

sim_baseline = Simulation(situation=household, country_id="us")
sim_reform = Simulation(situation=household, country_id="us", reform=reform)

ctc_baseline = sim_baseline.calculate("ctc", "2024")
ctc_reform = sim_reform.calculate("ctc", "2024")

print(f"CTC baseline: ${ctc_baseline:,.0f}")
print(f"CTC reform: ${ctc_reform:,.0f}")
print(f"Increase: ${ctc_reform - ctc_baseline:,.0f}")
```

### Workflow 3: Batch Analysis

```python
import pandas as pd
from policyengine import Simulation

# Analyze multiple households
households = [
    {"income": 30000, "children": 0},
    {"income": 50000, "children": 2},
    {"income": 100000, "children": 3},
]

results = []
for h in households:
    situation = create_household(income=h["income"], num_children=h["children"])
    sim = Simulation(situation=situation, country_id="us")

    results.append({
        "income": h["income"],
        "children": h["children"],
        "income_tax": sim.calculate("income_tax", "2024"),
        "ctc": sim.calculate("ctc", "2024"),
        "eitc": sim.calculate("eitc", "2024")
    })

df = pd.DataFrame(results)
print(df)
```

## Using the REST API Directly

### Authentication

**Public access:**
- 100 requests per minute (unauthenticated)
- No API key needed for basic use

**Authenticated access:**
- 1,000 requests per minute
- Contact hello@policyengine.org for API key

### Key Endpoints

**Calculate household impact:**
```python
import requests

url = "https://api.policyengine.org/us/calculate"
payload = {
    "household": household_dict,
    "policy_id": reform_id  # or None for baseline
}

response = requests.post(url, json=payload)
result = response.json()
```

**Get policy details:**
```python
# Get policy metadata
response = requests.get("https://api.policyengine.org/us/policy/12345")
policy = response.json()
```

**Get parameter values:**
```python
# Get current parameter value
response = requests.get(
    "https://api.policyengine.org/us/parameter/gov.irs.credits.ctc.amount.base_amount"
)
parameter = response.json()
```

### For Full API Documentation

**OpenAPI spec:** https://api.policyengine.org/docs

**To explore:**
```bash
# View all endpoints
curl https://api.policyengine.org/docs

# Test calculate endpoint
curl -X POST https://api.policyengine.org/us/calculate \
  -H "Content-Type: application/json" \
  -d '{"household": {...}}'
```

## Limitations and Considerations

### Rate Limits

**Unauthenticated:**
- 100 requests/minute
- Good for exploratory analysis

**Authenticated:**
- 1,000 requests/minute
- Required for production use

### Data Privacy

- PolicyEngine does not store household data
- All calculations happen server-side and are not logged
- Reform URLs are public (don't include personal info in reforms)

### Performance

**API calls:**
- Simple household: ~200-500ms
- Population impact: ~5-30 seconds (varies by reform)
- Use caching for repeated calculations

**Local simulation (policyengine-us):**
- Faster for batch analysis
- No rate limits
- No network dependency
- Limited to one country per package

## Choosing Local vs API

### Use Local (policyengine-us package)

**When:**
- Batch analysis of many households
- Need offline capability
- Analyzing parameter sweeps (axes)
- Development/testing

**Install:**
```bash
pip install policyengine-us  # US only
pip install policyengine-uk  # UK only
```

**Example:**
```python
from policyengine_us import Simulation

# Works offline
sim = Simulation(situation=household)
```

### Use API (policyengine or requests)

**When:**
- Multi-country analysis
- Using latest model version
- Don't want to manage dependencies
- Integration with web services

**Example:**
```python
import requests

# Requires internet
response = requests.post("https://api.policyengine.org/us/calculate", ...)
```

## For Contributors: Understanding the Client

**Repository:** PolicyEngine/policyengine.py

**To see implementation:**
```bash
# Clone the client
git clone https://github.com/PolicyEngine/policyengine.py

# See the Simulation class
cat policyengine/simulation.py

# See API integration
cat policyengine/api.py
```

**Architecture:**
- `Simulation` class wraps API calls
- `calculate()` method handles caching
- Transparent fallback between API and local

## Advanced: Direct Country Package Usage

For maximum control and performance, use country packages directly:

```python
from policyengine_us import Simulation

# Full control over situation structure
situation = {
    # Complete situation dictionary
    # See policyengine-us-skill for patterns
}

sim = Simulation(situation=situation)
result = sim.calculate("variable_name", 2024)
```

**Benefits:**
- No API dependency
- Faster (no network)
- Full access to all variables
- Use axes for parameter sweeps

**See policyengine-us-skill for detailed patterns.**

## Examples and Tutorials

**PolicyEngine documentation:**
- US: https://policyengine.org/us/docs
- UK: https://policyengine.org/uk/docs

**Example notebooks:**
- Repository: PolicyEngine/analysis-notebooks
- See policyengine-analysis-skill for analysis patterns

**Community examples:**
- Blog posts: policyengine.org/us/research
- GitHub discussions: github.com/PolicyEngine discussions

## Getting Help

**For usage questions:**
- GitHub Discussions: https://github.com/PolicyEngine/policyengine-us/discussions

**For bugs:**
- File issues in appropriate repo (policyengine-us, policyengine.py, etc.)

**For collaboration:**
- Email: hello@policyengine.org
