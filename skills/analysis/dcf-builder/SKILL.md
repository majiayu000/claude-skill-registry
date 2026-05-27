---
name: "dcf-builder"
version: "1.0.0"
owner: "Platform AI Team"
description: "Build defensible DCF models with cited sources, Excel export, and sensitivity analysis"
dependencies:
  - mcp: "edgar"          # SEC EDGAR connector
  - mcp: "postgres"       # pgvector for historical data
  - mcp: "python"         # DCF calculations
  - mcp: "filesystem"     # Excel export
capabilities:
  - citations_required: true
  - code_execution: python
  - produce_files: [".xlsx", ".csv", ".md"]
guardrails:
  - "Do not invent values. Every numeric must trace to cited source (EDGAR, company filings)"
  - "If inputs missing, ask for them or return needs_inputs block"
  - "No personal investment advice; educational modeling only"
  - "Include disclaimer: 'Educational analysis, not investment advice'"
inputs:
  - ticker_or_cik: "Ticker symbol or CIK"
  - currency: "USD, EUR, PHP, etc"
  - scenario: "base | bull | bear"
  - forecast_years: "5-10 years (default: 5)"
workflow:
  - step: "Fetch latest 10-K/10-Q from EDGAR; extract financials from XBRL"
  - step: "Extract historical: revenue, EBITDA, D&A, capex, working capital, tax rate"
  - step: "Compute WACC: risk-free rate, equity risk premium, beta, cost of debt"
  - step: "Forecast FCF (forecast_years) using growth assumptions"
  - step: "Calculate terminal value (perpetuity growth or exit multiple)"
  - step: "Discount to present value; sum to enterprise value"
  - step: "Subtract net debt to get equity value; divide by shares for price target"
  - step: "Run sensitivity analysis (WACC ±200 bps, terminal growth ±100 bps)"
  - step: "Export Excel with formulas, Markdown summary with sources"
success_criteria:
  - "All numbers link to sources (accession ID/XBRL fact)"
  - "Excel workbook opens with working formulas"
  - "Sensitivity table shows range of valuations"
  - "Markdown summary includes 'Sources' section with URLs"
---

# DCF Builder Skill

## Purpose

Build discounted cash flow (DCF) models from SEC filings with full source attribution. Outputs Excel workbook with formulas and Markdown summary.

## Usage

```python
# Build DCF for Omnicom Group
dcf = build_dcf(
    ticker_or_cik="OMC",
    currency="USD",
    scenario="base",
    forecast_years=5
)
```

## Workflow

### 1. Fetch Historical Financials

```python
def fetch_historical_financials(cik):
    """Fetch historical financials from SEC EDGAR"""
    # Get company facts (XBRL aggregated data)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik.zfill(10)}.json"
    response = requests.get(url, headers=EDGAR_HEADERS, timeout=30)
    response.raise_for_status()

    facts = response.json()

    # Extract key metrics
    financials = {
        'revenue': extract_fact(facts, 'Revenues'),
        'cogs': extract_fact(facts, 'CostOfRevenue'),
        'operating_expenses': extract_fact(facts, 'OperatingExpenses'),
        'depreciation': extract_fact(facts, 'DepreciationAndAmortization'),
        'capex': extract_fact(facts, 'PaymentsToAcquirePropertyPlantAndEquipment'),
        'tax_rate': extract_fact(facts, 'EffectiveIncomeTaxRateContinuingOperations'),
        'cash': extract_fact(facts, 'Cash'),
        'debt': extract_fact(facts, 'LongTermDebt'),
        'shares_outstanding': extract_fact(facts, 'CommonStockSharesOutstanding'),
    }

    return financials

def extract_fact(facts, concept_name):
    """Extract XBRL fact by concept name"""
    try:
        # Navigate nested structure: facts -> concept -> units -> values
        concept = facts['facts']['us-gaap'][concept_name]
        # Get USD annual values
        usd_values = concept['units']['USD']
        # Filter for 10-K filings (FY = full year)
        annual_values = [v for v in usd_values if v['form'] == '10-K']
        # Sort by date
        annual_values.sort(key=lambda x: x['end'], reverse=True)
        # Return most recent 5 years
        return [{
            'date': v['end'],
            'value': v['val'],
            'accession': v['accn'],
            'source': f"https://www.sec.gov/cgi-bin/viewer?action=view&cik={cik}&accession_number={v['accn']}"
        } for v in annual_values[:5]]
    except KeyError:
        return []
```

### 2. Compute WACC

```python
def compute_wacc(cik, financials):
    """Compute Weighted Average Cost of Capital"""

    # Cost of Equity (CAPM): Rf + Beta * (Rm - Rf)
    risk_free_rate = 0.045  # 10-year Treasury yield
    market_risk_premium = 0.08  # Historical equity risk premium
    beta = fetch_beta(cik)  # From financial data providers or regression

    cost_of_equity = risk_free_rate + beta * market_risk_premium

    # Cost of Debt: Interest Expense / Total Debt
    interest_expense = extract_latest_value(financials, 'InterestExpense')
    total_debt = extract_latest_value(financials, 'LongTermDebt')
    cost_of_debt = interest_expense / total_debt if total_debt > 0 else 0.05

    # After-tax cost of debt
    tax_rate = extract_latest_value(financials, 'EffectiveIncomeTaxRateContinuingOperations') / 100
    cost_of_debt_after_tax = cost_of_debt * (1 - tax_rate)

    # Market values
    equity_value = extract_latest_value(financials, 'CommonStockSharesOutstanding') * fetch_stock_price(cik)
    debt_value = total_debt

    # WACC = (E/V) * Re + (D/V) * Rd * (1 - Tc)
    total_value = equity_value + debt_value
    wacc = (equity_value / total_value) * cost_of_equity + (debt_value / total_value) * cost_of_debt_after_tax

    return {
        'wacc': wacc,
        'cost_of_equity': cost_of_equity,
        'cost_of_debt': cost_of_debt_after_tax,
        'weights': {
            'equity': equity_value / total_value,
            'debt': debt_value / total_value,
        },
        'sources': {
            'risk_free_rate': '10-Year Treasury Yield',
            'beta': 'Computed from historical returns',
            'debt': financials['debt'][0]['source'],
        }
    }
```

### 3. Forecast Free Cash Flow

```python
def forecast_fcf(financials, scenario='base', forecast_years=5):
    """Forecast Free Cash Flow"""

    # Historical revenue growth
    revenues = [f['value'] for f in financials['revenue']]
    historical_growth = [(revenues[i] / revenues[i+1]) - 1 for i in range(len(revenues)-1)]
    avg_growth = sum(historical_growth) / len(historical_growth)

    # Scenario assumptions
    growth_assumptions = {
        'base': avg_growth,
        'bull': avg_growth * 1.2,  # 20% higher
        'bear': avg_growth * 0.8,  # 20% lower
    }

    revenue_growth = growth_assumptions[scenario]

    # Forecast revenues
    latest_revenue = revenues[0]
    forecasted_revenues = []
    for year in range(1, forecast_years + 1):
        forecasted_revenue = latest_revenue * ((1 + revenue_growth) ** year)
        forecasted_revenues.append(forecasted_revenue)

    # Forecast FCF components
    fcf_projections = []
    for year, revenue in enumerate(forecasted_revenues, start=1):
        # Operating margin assumption (use historical average)
        ebitda_margin = compute_avg_margin(financials, 'EBITDA')
        ebitda = revenue * ebitda_margin

        # D&A as % of revenue
        da_pct = compute_avg_pct(financials, 'depreciation')
        depreciation = revenue * da_pct

        # EBIT = EBITDA - D&A
        ebit = ebitda - depreciation

        # Taxes
        tax_rate = extract_latest_value(financials, 'EffectiveIncomeTaxRateContinuingOperations') / 100
        taxes = ebit * tax_rate

        # NOPAT (Net Operating Profit After Tax)
        nopat = ebit - taxes

        # Add back D&A
        # Subtract Capex
        capex_pct = compute_avg_pct(financials, 'capex')
        capex = revenue * capex_pct

        # Change in NWC (working capital)
        nwc_change = revenue * 0.02  # Assume 2% of revenue growth

        # FCF = NOPAT + D&A - Capex - ΔNW C
        fcf = nopat + depreciation - capex - nwc_change

        fcf_projections.append({
            'year': year,
            'revenue': revenue,
            'ebitda': ebitda,
            'depreciation': depreciation,
            'ebit': ebit,
            'taxes': taxes,
            'nopat': nopat,
            'capex': capex,
            'nwc_change': nwc_change,
            'fcf': fcf,
        })

    return fcf_projections
```

### 4. Calculate Terminal Value and Valuation

```python
def calculate_valuation(fcf_projections, wacc, terminal_growth=0.025):
    """Calculate enterprise and equity value"""

    # Discount FCF to present value
    pv_fcf = []
    for projection in fcf_projections:
        year = projection['year']
        fcf = projection['fcf']
        discount_factor = (1 + wacc) ** year
        pv = fcf / discount_factor
        pv_fcf.append(pv)

    sum_pv_fcf = sum(pv_fcf)

    # Terminal value (perpetuity growth method)
    final_fcf = fcf_projections[-1]['fcf']
    terminal_value = (final_fcf * (1 + terminal_growth)) / (wacc - terminal_growth)

    # Discount terminal value to present
    terminal_year = len(fcf_projections)
    pv_terminal_value = terminal_value / ((1 + wacc) ** terminal_year)

    # Enterprise value
    enterprise_value = sum_pv_fcf + pv_terminal_value

    # Equity value = EV - Net Debt
    net_debt = extract_latest_value(financials, 'LongTermDebt') - extract_latest_value(financials, 'Cash')
    equity_value = enterprise_value - net_debt

    # Price per share
    shares_outstanding = extract_latest_value(financials, 'CommonStockSharesOutstanding')
    price_target = equity_value / shares_outstanding

    return {
        'sum_pv_fcf': sum_pv_fcf,
        'terminal_value': terminal_value,
        'pv_terminal_value': pv_terminal_value,
        'enterprise_value': enterprise_value,
        'net_debt': net_debt,
        'equity_value': equity_value,
        'shares_outstanding': shares_outstanding,
        'price_target': price_target,
    }
```

### 5. Sensitivity Analysis

```python
def sensitivity_analysis(fcf_projections, wacc, terminal_growth, financials):
    """Generate sensitivity table"""

    wacc_range = [wacc - 0.02, wacc - 0.01, wacc, wacc + 0.01, wacc + 0.02]  # ±200 bps
    tg_range = [terminal_growth - 0.01, terminal_growth - 0.005, terminal_growth,
                terminal_growth + 0.005, terminal_growth + 0.01]  # ±100 bps

    sensitivity_table = []
    for w in wacc_range:
        row = []
        for tg in tg_range:
            valuation = calculate_valuation(fcf_projections, w, tg, financials)
            row.append(valuation['price_target'])
        sensitivity_table.append(row)

    return {
        'wacc_range': wacc_range,
        'terminal_growth_range': tg_range,
        'price_targets': sensitivity_table,
    }
```

### 6. Export to Excel

```python
import openpyxl
from openpyxl.styles import Font, Alignment

def export_to_excel(dcf_model, filename='/exports/dcf_model.xlsx'):
    """Export DCF model to Excel with formulas"""

    wb = openpyxl.Workbook()

    # Historical sheet
    ws_hist = wb.active
    ws_hist.title = 'Historical'
    # ... populate historical data ...

    # Projections sheet
    ws_proj = wb.create_sheet('Projections')
    # ... populate projections with formulas ...

    # Valuation sheet
    ws_val = wb.create_sheet('Valuation')
    # ... populate valuation ...

    # Sensitivity sheet
    ws_sens = wb.create_sheet('Sensitivity')
    # ... populate sensitivity table ...

    # Sources sheet
    ws_sources = wb.create_sheet('Sources')
    ws_sources['A1'] = 'Data Sources'
    ws_sources['A1'].font = Font(bold=True, size=14)

    row = 3
    for metric, source in dcf_model['sources'].items():
        ws_sources[f'A{row}'] = metric
        ws_sources[f'B{row}'] = source
        row += 1

    wb.save(filename)
    return filename
```

### 7. Generate Markdown Summary

```python
def generate_markdown_summary(dcf_model):
    """Generate Markdown summary with citations"""

    md = f"""
# DCF Valuation: {dcf_model['ticker']}

**Scenario**: {dcf_model['scenario']}
**Date**: {datetime.now().strftime('%Y-%m-%d')}
**Currency**: {dcf_model['currency']}

## Summary

- **Enterprise Value**: {dcf_model['valuation']['enterprise_value']:,.0f}
- **Equity Value**: {dcf_model['valuation']['equity_value']:,.0f}
- **Price Target**: {dcf_model['valuation']['price_target']:.2f}

## Assumptions

- **WACC**: {dcf_model['wacc']['wacc']:.2%}
- **Terminal Growth**: {dcf_model['terminal_growth']:.2%}
- **Forecast Period**: {dcf_model['forecast_years']} years

## Free Cash Flow Projections

| Year | Revenue | EBITDA | FCF |
|------|---------|--------|-----|
"""

    for proj in dcf_model['fcf_projections']:
        md += f"| {proj['year']} | {proj['revenue']:,.0f} | {proj['ebitda']:,.0f} | {proj['fcf']:,.0f} |\n"

    md += f"""
## Sensitivity Analysis

Price target range: **{min(min(dcf_model['sensitivity']['price_targets']))} - {max(max(dcf_model['sensitivity']['price_targets'])):.2f}**

## Sources

"""

    for metric, source in dcf_model['sources'].items():
        md += f"- **{metric}**: {source}\n"

    md += """

---

**Disclaimer**: This is an educational analysis and not investment advice.
"""

    return md
```

## Evaluation

Test DCF output quality:

```yaml
# tests/finance/dcf-builder.yaml
suite: dcf-builder
thresholds:
  has_excel_export: true
  has_sensitivities: true
  cites_sources: true

cases:
  - id: ev-dcf-omnicom
    prompt: "Build a base-case DCF for Omnicom (OMC) with 5y forecast"
    expects:
      - has_excel_export: true
      - has_formulas: true
      - has_sensitivity_table: true
      - cites_sources: true
      - price_target_reasonable: true  # Within 20% of current price
```

## References

- DCF Methodology: https://www.investopedia.com/terms/d/dcf.asp
- XBRL Facts API: https://www.sec.gov/edgar/sec-api-documentation
- WACC Calculation: https://corporatefinanceinstitute.com/resources/valuation/wacc-formula/
