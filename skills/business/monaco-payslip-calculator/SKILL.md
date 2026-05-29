---
name: monaco-payslip-calculator
description: Calculate Monaco payslips (bulletin de salaire) with social security contributions, taxes, and net salary. Use when user requests Monaco payslip calculations, salary breakdowns for Monaco employees, or needs to compute Monegasque employer/employee contributions.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Monaco Payslip Calculator

## Overview

Calculate accurate Monaco payslips (bulletin de salaire) including gross salary, employer and employee social security contributions, and net salary. This skill handles calculations for the Monaco social security system (Caisses Sociales de Monaco) with proper contribution rates and thresholds.

## When to Use This Skill

Use this skill when the user:
- Requests to calculate a Monaco payslip or bulletin de salaire
- Needs to compute social security contributions for Monaco employees
- Asks about Monaco employer costs or employee net salary
- Wants to understand the breakdown of Monaco salary calculations
- Mentions "Caisses Sociales" or Monaco employment calculations

## Workflow

### 1. Gather Required Information

Ask the user for the following information if not provided:

**Required:**
- **Gross monthly salary** (salaire brut mensuel)
- **Employee type**: Standard employee, household employee (gens de maison), or other
- **Employment status**: Full-time or part-time

**Optional but recommended:**
- Number of hours worked (for part-time)
- Special allowances or bonuses
- Previous YTD (year-to-date) amounts if calculating mid-year
- Any specific deductions or benefits

### 2. Determine Contribution Rates

Use the reference data in `references/contribution_rates.md` to determine:
- Employer social security contribution rates
- Employee social security contribution rates
- Any applicable ceilings or thresholds
- Tax rates if applicable

The main contribution categories in Monaco include:
- **Maladie** (Health insurance)
- **Vieillesse** (Pension/Retirement)
- **Chômage** (Unemployment)
- **Accidents du travail** (Work accidents)
- **Allocations familiales** (Family allowances)

### 3. Calculate the Payslip

Execute the calculation script to compute:

```bash
python3 scripts/payslip_calculator.py \
  --gross-salary <amount> \
  --employee-type <type> \
  --output-format <json|pdf|txt>
```

Or use the Python module directly in the response for interactive calculations:

```python
# Read and execute the calculator script
exec(open('scripts/payslip_calculator.py').read())

# Create calculator instance
calculator = MonacoPayslipCalculator(
    gross_salary=3500.00,
    employee_type='standard'
)

# Calculate contributions
result = calculator.calculate()

# Display results
print(f"Gross Salary: €{result['gross_salary']:.2f}")
print(f"Employee Contributions: €{result['employee_total']:.2f}")
print(f"Net Salary: €{result['net_salary']:.2f}")
print(f"Employer Contributions: €{result['employer_total']:.2f}")
print(f"Total Employer Cost: €{result['total_cost']:.2f}")
```

### 4. Present Results

Format the results as a complete payslip showing:

**Employee Section:**
- Gross salary (Salaire brut)
- Itemized employee contributions by category
- Net salary before tax (Salaire net avant impôt)
- Net salary to pay (Salaire net à payer)

**Employer Section:**
- Itemized employer contributions by category
- Total employer contributions
- Total employer cost (gross salary + employer contributions)

**Summary:**
- Total social security contributions (employee + employer)
- Effective rate percentages

### 5. Provide Explanation

Include a brief explanation of:
- Which contribution categories apply
- Any thresholds or special calculations used
- Links to official Monaco social security resources
- How the user can verify calculations on the official calculator

## Calculation Details

### Standard Contribution Structure

Monaco payslip calculations follow this structure:

```
GROSS SALARY (Salaire Brut)
├─ Employee Contributions (Cotisations Salariales)
│  ├─ Health Insurance (Maladie)
│  ├─ Pension (Vieillesse)
│  ├─ Unemployment (Chômage)
│  └─ Other applicable contributions
└─ NET SALARY (Salaire Net)

Separately calculated:
EMPLOYER CONTRIBUTIONS (Cotisations Patronales)
├─ Health Insurance
├─ Pension
├─ Unemployment
├─ Work Accidents
├─ Family Allowances
└─ Other applicable contributions

TOTAL EMPLOYER COST = Gross Salary + Employer Contributions
```

### Important Notes

1. **Contribution Rates**: Rates are subject to change. Always verify with the latest rates from Caisses Sociales de Monaco.

2. **Ceilings**: Some contributions have maximum salary ceilings (plafonds) - the contribution only applies up to a certain amount.

3. **Household Employees**: Different rates apply for "gens de maison" (household employees).

4. **Official Calculator**: Users can verify calculations at:
   https://employeur.caisses-sociales.mc/ (if accessible)

5. **Currency**: All amounts are in Euros (€).

## Example Usage

**User Request:** "Calculate a Monaco payslip for a gross salary of €3,500 per month"

**Response Process:**
1. Confirm employee type (standard/household employee)
2. Load contribution rates from references
3. Calculate using the script:
   - Employee contributions: ~€280-350 (8-10%)
   - Net salary: ~€3,150-3,220
   - Employer contributions: ~€1,050-1,400 (30-40%)
   - Total cost: ~€4,550-4,900
4. Present formatted payslip with itemized breakdown
5. Explain the calculation methodology

## Resources

### scripts/
- `payslip_calculator.py` - Main calculation engine for Monaco payslips
  - Handles standard and household employee calculations
  - Supports multiple output formats (JSON, text, PDF-ready)
  - Includes validation and error handling

### references/
- `contribution_rates.md` - Current Monaco social security contribution rates
  - Employer rates by category
  - Employee rates by category
  - Thresholds and ceilings
  - Special cases and exemptions
  - Last updated date and official sources

### assets/
- `payslip_template.txt` - Text template for formatted payslip output
- `example_payslips/` - Sample payslip calculations for reference

## Data Sources

The contribution rates and calculation rules should be verified against:
1. Official Caisses Sociales de Monaco website: https://www.caisses-sociales.mc/
2. Monaco employer portal: https://employeur.caisses-sociales.mc/
3. Official Monaco legislation and decrees

**Note**: Since the official calculator URLs returned access errors, the user should manually verify the current contribution rates and update `references/contribution_rates.md` with the accurate data.

## Limitations

- This skill calculates standard payslip elements. Complex situations (expatriate status, special regimes, etc.) may require additional verification
- Tax calculations are not included as Monaco has specific tax rules based on nationality and residency
- Always verify critical calculations with official Monaco authorities or qualified accountants
- Contribution rates must be kept up-to-date in the reference files
