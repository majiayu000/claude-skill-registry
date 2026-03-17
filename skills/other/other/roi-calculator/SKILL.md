---
name: roi-calculator
description: Calculate ROI for marketing campaigns, investments, and business decisions. Includes break-even analysis, payback period, and comparative ROI.
---

# ROI Calculator

Comprehensive ROI calculations for marketing, investments, and business decisions.

## Features

- **Simple ROI**: Basic return on investment calculation
- **Marketing ROI**: Campaign performance with attribution
- **Investment ROI**: Time-adjusted returns with CAGR
- **Break-Even Analysis**: Find profit threshold
- **Payback Period**: Time to recover investment
- **Comparative Analysis**: Compare multiple options
- **What-If Scenarios**: Sensitivity analysis

## Quick Start

```python
from roi_calculator import ROICalculator

calc = ROICalculator()

# Simple ROI
roi = calc.simple_roi(investment=10000, return_value=15000)
print(f"ROI: {roi['roi_percent']}%")

# Marketing ROI
marketing = calc.marketing_roi(
    ad_spend=5000,
    revenue_generated=25000,
    cost_of_goods=10000
)
print(f"Marketing ROI: {marketing['roi_percent']}%")

# Break-even analysis
breakeven = calc.break_even(
    fixed_costs=50000,
    price_per_unit=100,
    variable_cost_per_unit=60
)
print(f"Break-even units: {breakeven['units']}")
```

## CLI Usage

```bash
# Simple ROI
python roi_calculator.py --investment 10000 --return 15000

# Marketing campaign ROI
python roi_calculator.py --marketing --spend 5000 --revenue 25000 --cogs 10000

# Break-even analysis
python roi_calculator.py --breakeven --fixed 50000 --price 100 --variable 60

# Investment with time (CAGR)
python roi_calculator.py --investment 10000 --return 20000 --years 5

# Payback period
python roi_calculator.py --payback --investment 100000 --annual-return 25000

# Compare multiple investments
python roi_calculator.py --compare investments.csv
```

## API Reference

### ROICalculator Class

```python
class ROICalculator:
    def __init__(self)

    # Basic ROI
    def simple_roi(self, investment: float, return_value: float) -> Dict
    def net_roi(self, investment: float, gain: float, costs: float = 0) -> Dict

    # Marketing ROI
    def marketing_roi(self, ad_spend: float, revenue_generated: float,
                      cost_of_goods: float = 0) -> Dict
    def campaign_roi(self, campaigns: List[Dict]) -> pd.DataFrame
    def roas(self, ad_spend: float, revenue: float) -> Dict  # Return on Ad Spend

    # Investment ROI
    def investment_roi(self, initial: float, final: float, years: float) -> Dict
    def cagr(self, initial: float, final: float, years: float) -> float
    def total_return(self, initial: float, final: float, dividends: float = 0) -> Dict

    # Break-Even Analysis
    def break_even(self, fixed_costs: float, price_per_unit: float,
                   variable_cost_per_unit: float) -> Dict
    def break_even_revenue(self, fixed_costs: float, contribution_margin_ratio: float) -> Dict

    # Payback Period
    def payback_period(self, investment: float, annual_cash_flow: float) -> Dict
    def payback_period_uneven(self, investment: float, cash_flows: List[float]) -> Dict

    # Comparative Analysis
    def compare_investments(self, investments: List[Dict]) -> pd.DataFrame
    def rank_by_roi(self, investments: List[Dict]) -> List[Dict]

    # Sensitivity Analysis
    def sensitivity_analysis(self, base_case: Dict, variables: Dict) -> pd.DataFrame
    def scenario_analysis(self, scenarios: List[Dict]) -> pd.DataFrame

    # Reporting
    def generate_report(self, analysis: Dict, output: str) -> str
```

## ROI Calculations

### Simple ROI
```python
result = calc.simple_roi(investment=10000, return_value=15000)
# Returns:
# {
#     "investment": 10000,
#     "return_value": 15000,
#     "gain": 5000,
#     "roi_percent": 50.0,
#     "roi_ratio": 0.5
# }
```

### Net ROI (with additional costs)
```python
result = calc.net_roi(
    investment=10000,
    gain=8000,
    costs=2000  # Additional costs
)
# Returns:
# {
#     "investment": 10000,
#     "gross_gain": 8000,
#     "costs": 2000,
#     "net_gain": 6000,
#     "roi_percent": 60.0
# }
```

## Marketing ROI

### Campaign ROI
```python
result = calc.marketing_roi(
    ad_spend=5000,
    revenue_generated=25000,
    cost_of_goods=10000
)
# Returns:
# {
#     "ad_spend": 5000,
#     "revenue": 25000,
#     "cost_of_goods": 10000,
#     "gross_profit": 15000,
#     "net_profit": 10000,  # After ad spend
#     "roi_percent": 200.0,
#     "roas": 5.0  # $5 revenue per $1 ad spend
# }
```

### Return on Ad Spend (ROAS)
```python
result = calc.roas(ad_spend=1000, revenue=4000)
# Returns:
# {
#     "ad_spend": 1000,
#     "revenue": 4000,
#     "roas": 4.0,
#     "roas_percent": 400.0
# }
```

### Multi-Campaign Comparison
```python
campaigns = [
    {"name": "Facebook", "spend": 2000, "revenue": 8000, "cogs": 3000},
    {"name": "Google", "spend": 3000, "revenue": 15000, "cogs": 6000},
    {"name": "Email", "spend": 500, "revenue": 3000, "cogs": 1000}
]
results = calc.campaign_roi(campaigns)
# Returns DataFrame with ROI for each campaign
```

## Investment ROI

### Time-Adjusted ROI with CAGR
```python
result = calc.investment_roi(
    initial=10000,
    final=20000,
    years=5
)
# Returns:
# {
#     "initial": 10000,
#     "final": 20000,
#     "total_gain": 10000,
#     "total_roi_percent": 100.0,
#     "cagr_percent": 14.87,  # Compound Annual Growth Rate
#     "years": 5
# }
```

### Total Return with Dividends
```python
result = calc.total_return(
    initial=10000,
    final=12000,
    dividends=1500
)
# Returns:
# {
#     "initial": 10000,
#     "final": 12000,
#     "capital_gain": 2000,
#     "dividends": 1500,
#     "total_return": 3500,
#     "total_return_percent": 35.0
# }
```

## Break-Even Analysis

### Unit Break-Even
```python
result = calc.break_even(
    fixed_costs=50000,
    price_per_unit=100,
    variable_cost_per_unit=60
)
# Returns:
# {
#     "fixed_costs": 50000,
#     "price_per_unit": 100,
#     "variable_cost_per_unit": 60,
#     "contribution_margin": 40,
#     "contribution_margin_ratio": 0.4,
#     "break_even_units": 1250,
#     "break_even_revenue": 125000
# }
```

### Revenue Break-Even
```python
result = calc.break_even_revenue(
    fixed_costs=50000,
    contribution_margin_ratio=0.4  # 40% margin
)
# Returns:
# {
#     "fixed_costs": 50000,
#     "contribution_margin_ratio": 0.4,
#     "break_even_revenue": 125000
# }
```

## Payback Period

### Simple Payback
```python
result = calc.payback_period(
    investment=100000,
    annual_cash_flow=25000
)
# Returns:
# {
#     "investment": 100000,
#     "annual_cash_flow": 25000,
#     "payback_years": 4.0,
#     "payback_months": 48
# }
```

### Uneven Cash Flows
```python
result = calc.payback_period_uneven(
    investment=100000,
    cash_flows=[20000, 30000, 40000, 35000, 25000]  # Per year
)
# Returns:
# {
#     "investment": 100000,
#     "payback_years": 2.75,  # Recovered in year 3
#     "cumulative_flows": [20000, 50000, 90000, 125000, 150000]
# }
```

## Comparative Analysis

### Compare Multiple Investments
```python
investments = [
    {"name": "Project A", "investment": 50000, "return": 75000, "years": 2},
    {"name": "Project B", "investment": 30000, "return": 48000, "years": 3},
    {"name": "Project C", "investment": 100000, "return": 180000, "years": 5}
]
comparison = calc.compare_investments(investments)
# Returns DataFrame:
#   name      | investment | return  | roi%   | cagr%  | payback
#   Project A | 50000      | 75000   | 50.0   | 22.5   | 1.33
#   Project B | 30000      | 48000   | 60.0   | 17.0   | 1.88
#   Project C | 100000     | 180000  | 80.0   | 12.5   | 2.78
```

### Rank by ROI
```python
ranked = calc.rank_by_roi(investments)
# Returns investments sorted by ROI percentage
```

## Sensitivity Analysis

### Variable Sensitivity
```python
base_case = {
    "fixed_costs": 50000,
    "price_per_unit": 100,
    "variable_cost_per_unit": 60,
    "units_sold": 2000
}

# Test impact of price changes
sensitivity = calc.sensitivity_analysis(
    base_case=base_case,
    variables={
        "price_per_unit": [80, 90, 100, 110, 120],
        "units_sold": [1500, 1750, 2000, 2250, 2500]
    }
)
# Returns DataFrame showing profit at each combination
```

### Scenario Analysis
```python
scenarios = [
    {"name": "Pessimistic", "units": 1500, "price": 90},
    {"name": "Base", "units": 2000, "price": 100},
    {"name": "Optimistic", "units": 2500, "price": 110}
]
results = calc.scenario_analysis(scenarios)
```

## Example Workflows

### Marketing Campaign Analysis
```python
calc = ROICalculator()

# Analyze Q4 campaigns
campaigns = [
    {"name": "Black Friday Email", "spend": 2000, "revenue": 45000, "cogs": 20000},
    {"name": "Holiday Facebook", "spend": 8000, "revenue": 35000, "cogs": 14000},
    {"name": "Google Shopping", "spend": 5000, "revenue": 28000, "cogs": 12000}
]

results = calc.campaign_roi(campaigns)
print(results.sort_values("roi_percent", ascending=False))

# Find best performing campaign
best = results.loc[results["roi_percent"].idxmax()]
print(f"Best ROI: {best['name']} at {best['roi_percent']:.1f}%")
```

### Business Investment Decision
```python
calc = ROICalculator()

# Compare expansion options
options = [
    {"name": "New Location", "investment": 200000, "annual_return": 45000},
    {"name": "Equipment Upgrade", "investment": 75000, "annual_return": 20000},
    {"name": "Digital Marketing", "investment": 30000, "annual_return": 12000}
]

for opt in options:
    payback = calc.payback_period(opt["investment"], opt["annual_return"])
    roi = calc.simple_roi(opt["investment"], opt["investment"] + opt["annual_return"] * 5)
    print(f"{opt['name']}: Payback={payback['payback_years']:.1f}yr, 5yr ROI={roi['roi_percent']:.1f}%")
```

### Pricing Strategy Analysis
```python
calc = ROICalculator()

# Break-even at different price points
fixed_costs = 100000
variable_cost = 25

for price in [40, 50, 60, 75, 100]:
    be = calc.break_even(fixed_costs, price, variable_cost)
    print(f"Price ${price}: Break-even at {be['break_even_units']:,} units (${be['break_even_revenue']:,.0f})")
```

## Dependencies

- pandas>=2.0.0
- numpy>=1.24.0
