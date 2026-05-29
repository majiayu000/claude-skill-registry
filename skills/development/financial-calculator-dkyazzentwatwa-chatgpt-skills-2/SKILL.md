---
name: financial-calculator
description: "Financial calculations: loans, investments, NPV/IRR, retirement planning, Monte Carlo simulations. Generates tables, charts, and exportable reports."
---

# Financial Calculator Suite

Professional-grade financial calculations with detailed breakdowns, visualizations, and exportable reports. Handles everything from simple loan payments to complex retirement projections with Monte Carlo simulations.

## Core Calculators

- **Loan Calculator**: Amortization schedules, payment breakdowns, prepayment scenarios
- **Investment Calculator**: Future value, compound growth, recurring contributions
- **NPV/IRR Calculator**: Net present value, internal rate of return, payback period
- **Retirement Calculator**: Savings projections, withdrawal strategies, longevity analysis
- **Monte Carlo Simulator**: Risk analysis with probability distributions
- **Mortgage Calculator**: Home affordability, refinance comparison
- **Savings Goal Calculator**: Time to goal, required contributions

## Quick Start

```python
from scripts.financial_calc import FinancialCalculator

# Loan calculation
calc = FinancialCalculator()
loan = calc.loan_payment(principal=250000, rate=6.5, years=30)
print(f"Monthly payment: ${loan['monthly_payment']:,.2f}")

# Investment growth
growth = calc.investment_growth(
    principal=10000,
    rate=7,
    years=20,
    monthly_contribution=500
)
print(f"Final value: ${growth['final_value']:,.2f}")
```

## Loan Calculator

### Basic Loan Payment

```python
from scripts.financial_calc import FinancialCalculator

calc = FinancialCalculator()

# Calculate monthly payment
loan = calc.loan_payment(
    principal=250000,    # Loan amount
    rate=6.5,            # Annual interest rate (%)
    years=30             # Loan term
)

print(f"Monthly Payment: ${loan['monthly_payment']:,.2f}")
print(f"Total Payments: ${loan['total_payments']:,.2f}")
print(f"Total Interest: ${loan['total_interest']:,.2f}")
```

### Amortization Schedule

```python
# Get full amortization schedule
schedule = calc.amortization_schedule(
    principal=250000,
    rate=6.5,
    years=30
)

# Schedule is a list of monthly payments
for payment in schedule[:12]:  # First year
    print(f"Month {payment['month']}: "
          f"Payment ${payment['payment']:,.2f}, "
          f"Principal ${payment['principal']:,.2f}, "
          f"Interest ${payment['interest']:,.2f}, "
          f"Balance ${payment['balance']:,.2f}")

# Export to CSV
calc.export_amortization(schedule, "loan_schedule.csv")
```

### Prepayment Analysis

```python
# Compare with extra payments
comparison = calc.prepayment_comparison(
    principal=250000,
    rate=6.5,
    years=30,
    extra_monthly=200
)

print(f"With extra payments:")
print(f"  Months saved: {comparison['months_saved']}")
print(f"  Interest saved: ${comparison['interest_saved']:,.2f}")
print(f"  New payoff: {comparison['new_term_years']:.1f} years")
```

## Investment Calculator

### Future Value

```python
# Simple compound growth
result = calc.future_value(
    principal=10000,
    rate=7,           # Annual return (%)
    years=20
)
print(f"Future value: ${result['future_value']:,.2f}")

# With monthly contributions
result = calc.investment_growth(
    principal=10000,
    rate=7,
    years=20,
    monthly_contribution=500
)
print(f"Final value: ${result['final_value']:,.2f}")
print(f"Total contributions: ${result['total_contributions']:,.2f}")
print(f"Total growth: ${result['total_growth']:,.2f}")
```

### Investment Comparison

```python
# Compare different scenarios
scenarios = calc.compare_investments([
    {'name': 'Conservative', 'rate': 4, 'principal': 10000, 'monthly': 500},
    {'name': 'Moderate', 'rate': 7, 'principal': 10000, 'monthly': 500},
    {'name': 'Aggressive', 'rate': 10, 'principal': 10000, 'monthly': 500},
], years=20)

for s in scenarios:
    print(f"{s['name']}: ${s['final_value']:,.2f}")
```

## NPV/IRR Calculator

### Net Present Value

```python
# Calculate NPV of cash flows
cash_flows = [-100000, 30000, 35000, 40000, 45000, 50000]  # Initial + 5 years
npv = calc.npv(cash_flows, discount_rate=10)
print(f"NPV: ${npv:,.2f}")
```

### Internal Rate of Return

```python
# Calculate IRR
irr = calc.irr(cash_flows)
print(f"IRR: {irr:.2f}%")
```

### Payback Period

```python
# Simple and discounted payback
payback = calc.payback_period(cash_flows, discount_rate=10)
print(f"Simple payback: {payback['simple']:.2f} years")
print(f"Discounted payback: {payback['discounted']:.2f} years")
```

### Project Comparison

```python
# Compare multiple projects
projects = [
    {'name': 'Project A', 'flows': [-100000, 30000, 40000, 50000, 60000]},
    {'name': 'Project B', 'flows': [-80000, 25000, 30000, 35000, 40000]},
]
comparison = calc.compare_projects(projects, discount_rate=10)
```

## Retirement Calculator

### Basic Retirement Projection

```python
# Project retirement savings
retirement = calc.retirement_projection(
    current_age=35,
    retirement_age=65,
    current_savings=100000,
    monthly_contribution=1000,
    expected_return=7,
    inflation=2.5
)

print(f"Projected savings at retirement: ${retirement['nominal_value']:,.2f}")
print(f"Real value (today's dollars): ${retirement['real_value']:,.2f}")
```

### Withdrawal Strategy

```python
# Calculate sustainable withdrawals
withdrawal = calc.retirement_withdrawal(
    savings=1000000,
    annual_spending=40000,
    expected_return=5,
    inflation=2.5,
    years=30  # Retirement duration
)

print(f"Success probability: {withdrawal['success_rate']:.1f}%")
print(f"Median ending balance: ${withdrawal['median_ending']:,.2f}")
```

### FIRE Calculator

```python
# Financial Independence calculation
fire = calc.fire_calculator(
    annual_expenses=50000,
    current_savings=200000,
    annual_savings=30000,
    expected_return=7,
    safe_withdrawal_rate=4
)

print(f"FIRE number: ${fire['fire_number']:,.2f}")
print(f"Years to FIRE: {fire['years_to_fire']:.1f}")
```

## Monte Carlo Simulation

### Investment Simulation

```python
# Run Monte Carlo simulation
simulation = calc.monte_carlo_investment(
    principal=100000,
    monthly_contribution=1000,
    years=20,
    mean_return=7,
    std_dev=15,       # Volatility
    simulations=1000
)

print(f"Median outcome: ${simulation['median']:,.2f}")
print(f"10th percentile: ${simulation['p10']:,.2f}")
print(f"90th percentile: ${simulation['p90']:,.2f}")
print(f"Probability > $1M: {simulation['prob_above_1m']:.1f}%")
```

### Retirement Simulation

```python
# Monte Carlo retirement analysis
retirement_sim = calc.monte_carlo_retirement(
    savings=1000000,
    annual_withdrawal=40000,
    years=30,
    mean_return=5,
    std_dev=10,
    inflation_mean=2.5,
    inflation_std=1,
    simulations=1000
)

print(f"Success rate: {retirement_sim['success_rate']:.1f}%")
print(f"Median final balance: ${retirement_sim['median_ending']:,.2f}")
```

## Mortgage Calculator

### Affordability

```python
# Calculate affordable home price
affordability = calc.mortgage_affordability(
    annual_income=100000,
    monthly_debt=500,
    down_payment=50000,
    rate=6.5,
    term_years=30,
    dti_limit=43  # Debt-to-income limit (%)
)

print(f"Max home price: ${affordability['max_price']:,.2f}")
print(f"Max loan amount: ${affordability['max_loan']:,.2f}")
print(f"Monthly payment: ${affordability['monthly_payment']:,.2f}")
```

### Refinance Comparison

```python
# Should you refinance?
refinance = calc.refinance_analysis(
    current_balance=200000,
    current_rate=7.0,
    current_payment=1330,
    remaining_months=300,
    new_rate=5.5,
    new_term_years=30,
    closing_costs=5000
)

print(f"New payment: ${refinance['new_payment']:,.2f}")
print(f"Monthly savings: ${refinance['monthly_savings']:,.2f}")
print(f"Break-even: {refinance['break_even_months']} months")
print(f"Lifetime savings: ${refinance['lifetime_savings']:,.2f}")
```

## Savings Goal Calculator

```python
# Time to reach goal
goal = calc.savings_goal(
    target=100000,
    current=10000,
    rate=5,
    monthly_contribution=500
)

print(f"Time to goal: {goal['months']} months ({goal['years']:.1f} years)")

# Required monthly savings
required = calc.required_savings(
    target=100000,
    current=10000,
    rate=5,
    years=10
)

print(f"Required monthly: ${required['monthly_needed']:,.2f}")
```

## Visualization

```python
# Generate charts
calc.plot_amortization(schedule, "amortization.png")
calc.plot_investment_growth(growth_data, "growth.png")
calc.plot_monte_carlo(simulation, "monte_carlo.png")
calc.plot_comparison(scenarios, "comparison.png")
```

## Export Options

```python
# Export to CSV
calc.export_amortization(schedule, "schedule.csv")
calc.export_simulation(simulation, "simulation.csv")

# Export to JSON
calc.export_json(results, "results.json")

# Generate PDF report
calc.generate_report(
    analysis_type='loan',
    data=loan_data,
    output="loan_report.pdf"
)
```

## CLI Usage

```bash
# Loan calculation
python financial_calc.py loan --principal 250000 --rate 6.5 --years 30

# Investment growth
python financial_calc.py invest --principal 10000 --rate 7 --years 20 --monthly 500

# NPV calculation
python financial_calc.py npv --flows "-100000,30000,35000,40000,45000" --rate 10

# Retirement projection
python financial_calc.py retire --age 35 --retire-age 65 --savings 100000 --monthly 1000

# Monte Carlo simulation
python financial_calc.py montecarlo --principal 100000 --years 20 --return 7 --volatility 15
```

## Formulas Reference

### Loan Payment (PMT)
```
PMT = P * [r(1+r)^n] / [(1+r)^n - 1]
where: P = principal, r = monthly rate, n = total payments
```

### Future Value (FV)
```
FV = PV * (1 + r)^n + PMT * [((1 + r)^n - 1) / r]
where: PV = present value, r = rate, n = periods, PMT = periodic payment
```

### Net Present Value (NPV)
```
NPV = Σ [CF_t / (1 + r)^t] for t = 0 to n
where: CF = cash flow, r = discount rate, t = time period
```

### Internal Rate of Return (IRR)
```
0 = Σ [CF_t / (1 + IRR)^t] for t = 0 to n
(Solved iteratively)
```

## Error Handling

```python
from scripts.financial_calc import FinancialCalculator, FinanceError

try:
    result = calc.loan_payment(principal=-1000, rate=5, years=30)
except FinanceError as e:
    print(f"Error: {e}")
```

## Dependencies

```
numpy>=1.24.0
numpy-financial>=1.0.0
pandas>=2.0.0
matplotlib>=3.7.0
scipy>=1.10.0
```
