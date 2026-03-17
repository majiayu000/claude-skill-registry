---
name: underwriting-analysis
description: Credit underwriting analysis patterns for alternative lending. Covers borrower analysis, financial spreading, and risk assessment methodologies.
---

# Underwriting Analysis Skill

Comprehensive credit underwriting methodologies for alternative lending and investment.

## Borrower Analysis Framework

### Entity Structure Review

```markdown
Key Questions:
1. What is the legal entity type?
   - LLC, Corporation, Partnership, Other
2. Where is it organized?
   - State of formation, foreign qualifications
3. Who are the owners?
   - Beneficial ownership down to 25%+ holders
4. What is the management structure?
   - Officers, managers, board composition
5. Are there related entities?
   - Affiliates, subsidiaries, parents
```

### Management Evaluation

```markdown
Scoring Criteria (1-5 scale):

Experience in Industry:
5 = 15+ years, multiple successful ventures
4 = 10-15 years, proven track record
3 = 5-10 years, some success
2 = 2-5 years, limited track record
1 = <2 years, unproven

Financial Management:
5 = Excellent controls, timely reporting
4 = Good controls, minor issues
3 = Adequate controls, some gaps
2 = Weak controls, reporting issues
1 = Poor controls, unreliable data

Personal Credit:
5 = 750+ FICO, clean history
4 = 700-749 FICO, minor issues
3 = 650-699 FICO, some derogatory
2 = 600-649 FICO, significant issues
1 = <600 FICO, recent bankruptcy/foreclosure
```

## Financial Statement Analysis

### Spreading Standards

```markdown
Income Statement Adjustments:

Revenue Recognition:
- Verify timing of revenue recognition
- Identify non-recurring revenue
- Adjust for related-party transactions

Expense Normalization:
+ Add back owner compensation above market
+ Add back one-time expenses
+ Add back non-cash expenses (if appropriate)
- Subtract understated expenses
- Subtract non-recurring income
= Adjusted EBITDA

Balance Sheet Adjustments:
- Mark assets to fair market value
- Identify related-party receivables/payables
- Verify inventory valuation method
- Assess intangible asset values
- Identify off-balance-sheet liabilities
```

### Key Ratio Analysis

```markdown
Liquidity Ratios:
Current Ratio = Current Assets / Current Liabilities
   Benchmark: >1.5x
Quick Ratio = (Current Assets - Inventory) / Current Liabilities
   Benchmark: >1.0x
Cash Ratio = Cash / Current Liabilities
   Benchmark: >0.2x

Leverage Ratios:
Debt/Equity = Total Debt / Total Equity
   Benchmark: <2.0x
Debt/EBITDA = Total Debt / Adjusted EBITDA
   Benchmark: <4.0x
Senior Debt/EBITDA = Senior Debt / Adjusted EBITDA
   Benchmark: <3.0x

Coverage Ratios:
DSCR = EBITDA / Total Debt Service
   Benchmark: >1.25x
Interest Coverage = EBIT / Interest Expense
   Benchmark: >3.0x
Fixed Charge Coverage = (EBITDA - CapEx) / Fixed Charges
   Benchmark: >1.15x

Profitability Ratios:
Gross Margin = Gross Profit / Revenue
   Industry dependent
EBITDA Margin = EBITDA / Revenue
   Cannabis: 15-35%
Net Margin = Net Income / Revenue
   Cannabis (post-280E): 5-15%
```

### Cash Flow Analysis

```markdown
Quality of Cash Flow Assessment:

Cash Flow from Operations (CFO):
- Compare to net income (CFO should approximate NI)
- Identify working capital manipulation
- Assess sustainability of cash generation

Free Cash Flow Quality:
- CFO - CapEx = FCF
- Recurring vs. one-time CapEx
- Maintenance vs. growth CapEx distinction

Cash Burn Analysis (for growth companies):
Monthly Cash Burn = (Beginning Cash - Ending Cash) / Months
Runway = Current Cash / Monthly Burn
   Minimum: 12 months runway for new loans
```

## Risk Assessment Methodology

### Credit Risk Matrix

```markdown
|              | Low Impact | Medium Impact | High Impact |
|--------------|------------|---------------|-------------|
| High Prob    | Monitor    | Mitigate      | DECLINE     |
| Medium Prob  | Accept     | Monitor       | Mitigate    |
| Low Prob     | Accept     | Accept        | Monitor     |

Risk Categories to Assess:
1. Credit/Financial Risk
2. Industry/Market Risk
3. Operational Risk
4. Regulatory Risk
5. Key Person Risk
6. Collateral Risk
7. Legal/Documentation Risk
```

### Industry Risk Assessment

```markdown
Cannabis Industry Risk Factors:

Regulatory Risk (HIGH):
- Federal illegality
- State licensing requirements
- Banking access limitations
- Tax implications (280E)

Market Risk (MEDIUM-HIGH):
- Price compression
- Oversupply in mature markets
- Competition from unlicensed operators
- Consumer preference shifts

Operational Risk (MEDIUM):
- Product recalls
- Crop failures
- Employee theft
- Compliance violations

Mitigation Strategies:
- Diversified state exposure
- License renewal monitoring
- Enhanced reporting requirements
- Cash management controls
- Third-party compliance audits
```

### Collateral Risk Analysis

```markdown
Collateral Quality Assessment:

Accounts Receivable:
Quality Factors:
- Age of receivables (% current vs. aged)
- Debtor credit quality
- Concentration risk
- Historical collection rates
- Dispute/offset exposure

Inventory:
Quality Factors:
- Turnover rate
- Obsolescence risk
- Storage conditions
- Market price volatility
- Regulatory compliance

Equipment:
Quality Factors:
- Age and condition
- Useful life remaining
- Specialized vs. general purpose
- Secondary market liquidity
- Maintenance history

Advance Rate Adjustment:
Base Rate: X%
- Concentration adjustment: (X%)
- Age adjustment: (X%)
- Quality adjustment: +/- X%
= Adjusted Advance Rate: X%
```

## Underwriting Decision Framework

### Credit Score Calculation

```python
def calculate_credit_score(factors: dict) -> float:
    """
    Calculate weighted credit score.

    Weights should sum to 100.
    """
    weights = {
        'management': 15,
        'industry': 15,
        'financial_performance': 25,
        'cash_flow': 20,
        'collateral': 15,
        'guarantor': 10
    }

    score = sum(
        factors[factor] * weights[factor] / 100
        for factor in weights
    )

    return score  # Range: 1.0 - 5.0
```

### Decision Matrix

```markdown
Score Range | Decision | Conditions
------------|----------|------------
4.5 - 5.0   | Approve  | Standard terms
4.0 - 4.4   | Approve  | Enhanced monitoring
3.5 - 3.9   | Conditional | Structure enhancements required
3.0 - 3.4   | Committee | Requires credit committee approval
2.5 - 2.9   | Decline  | Unless significant mitigants
< 2.5       | Decline  | Hard decline
```

### Structure Enhancement Options

```markdown
For Borderline Credits (Score 3.0-4.0):

Pricing Enhancements:
- Higher interest rate (+200-500 bps)
- Larger origination fee (+0.5-2.0%)
- Minimum interest provisions

Structural Enhancements:
- Lower advance rates (-10-20%)
- Additional collateral requirements
- Stronger guarantor requirements
- More restrictive covenants
- Shorter loan term
- Faster amortization

Monitoring Enhancements:
- More frequent reporting
- Field exams/audits
- Lockbox arrangements
- Reserve requirements
```

## Due Diligence Checklist

### Complete Package Requirements

```markdown
Borrower Information:
- [ ] Application and summary
- [ ] Organizational documents
- [ ] Good standing certificates
- [ ] Ownership/beneficial ownership
- [ ] Management bios/resumes
- [ ] Business plan (if applicable)

Financial Information:
- [ ] 3 years financial statements
- [ ] 3 years tax returns
- [ ] Current year-to-date financials
- [ ] Projections (3-5 years)
- [ ] Accounts receivable aging
- [ ] Accounts payable aging
- [ ] Inventory reports
- [ ] Bank statements (12 months)

Collateral Information:
- [ ] Asset schedules
- [ ] Appraisals/valuations
- [ ] Title reports
- [ ] Environmental reports
- [ ] UCC search results
- [ ] Insurance certificates

Third-Party Reports:
- [ ] Background checks
- [ ] Credit reports (business and personal)
- [ ] Reference checks
- [ ] Site visit report
- [ ] Independent market analysis
```

### Red Flags Checklist

```markdown
Immediate Concerns (Require Explanation):
- [ ] Declining revenue trend
- [ ] Negative or declining EBITDA
- [ ] DSCR below 1.0x
- [ ] Recent management changes
- [ ] Legal or regulatory issues
- [ ] Tax liens or judgments
- [ ] Related-party transactions
- [ ] Guarantor credit issues
- [ ] Inconsistencies in financials
- [ ] Resistance to providing information

Deal Breakers (Likely Decline):
- [ ] Fraud indicators
- [ ] Active litigation (material)
- [ ] License suspension/revocation
- [ ] Recent bankruptcy
- [ ] Federal violations (cannabis)
- [ ] Criminal background (principals)
- [ ] Negative net worth
- [ ] Cash flow insufficient for debt service
```
