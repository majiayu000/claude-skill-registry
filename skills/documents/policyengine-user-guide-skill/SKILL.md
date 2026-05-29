---
name: policyengine-user-guide
description: Using PolicyEngine web apps to analyze tax and benefit policy impacts - for users of policyengine.org
---

# PolicyEngine User Guide

This skill helps you use PolicyEngine to analyze how tax and benefit policies affect households and populations.

## For Users: Getting Started

### What is PolicyEngine?

PolicyEngine computes the impact of public policy on households and society. You can:
- Calculate how policies affect your household
- Analyze population-wide impacts of reforms
- Create and share custom policy proposals
- Compare different policy options

### Web App: policyengine.org

**Main features:**
1. **Your household** - Calculate your taxes and benefits
2. **Policy** - Design custom reforms and see impacts
3. **Research** - Read policy analysis and blog posts

### Available Countries

- **United States** - policyengine.org/us
- **United Kingdom** - policyengine.org/uk
- **Canada** - policyengine.org/ca (beta)

## Using the Household Calculator

### Step 1: Navigate to Household Page

**US:** https://policyengine.org/us/household
**UK:** https://policyengine.org/uk/household

### Step 2: Enter Your Information

**Income:**
- Employment income (W-2 wages)
- Self-employment income
- Capital gains and dividends
- Social Security, pensions, etc.

**Household composition:**
- Adults and dependents
- Ages
- Marital status

**Location:**
- State (US) or region (UK)
- NYC checkbox for New York City residents

**Deductions (US):**
- Charitable donations
- Mortgage interest
- State and local taxes (SALT)
- Medical expenses

### Step 3: View Results

**Net income** - Your income after taxes and benefits

**Breakdown:**
- Total taxes (federal + state + local)
- Total benefits (EITC, CTC, SNAP, etc.)
- Effective tax rate
- Marginal tax rate

**Charts:**
- Net income by earnings
- Marginal tax rate by earnings

## Creating a Policy Reform

### Step 1: Navigate to Policy Page

**US:** https://policyengine.org/us/policy
**UK:** https://policyengine.org/uk/policy

### Step 2: Select Parameters to Change

**Browse parameters by:**
- Government department (IRS, SSA, etc.)
- Program (EITC, CTC, SNAP)
- Type (tax rates, benefit amounts, thresholds)

**Example: Increase Child Tax Credit**
1. Navigate to gov.irs.credits.ctc.amount.base_amount
2. Change from $2,000 to $5,000
3. Click "Calculate economic impact"

### Step 3: View Population Impacts

**Budgetary impact:**
- Total cost or revenue raised
- Breakdown by program

**Poverty impact:**
- Change in poverty rates
- By age group (children, adults, seniors)
- Deep poverty (income < 50% of threshold)

**Distributional impact:**
- Average impact by income decile
- Winners and losers by decile
- Relative vs absolute changes

**Inequality impact:**
- Gini index change
- Top 10% and top 1% income share

### Step 4: Share Your Reform

**Share URL:**
Every reform has a unique URL you can share:
```
policyengine.org/us/policy?reform=12345&region=enhanced_us&timePeriod=2025
```

**Parameters in URL:**
- `reform=12345` - Your custom reform ID
- `region=enhanced_us` - Geography (US, state, or congressional district)
- `timePeriod=2025` - Year of analysis

## Understanding Results

### Metrics Explained

**Supplemental Poverty Measure (SPM):**
- Accounts for taxes, benefits, and living costs
- US Census Bureau's official alternative poverty measure
- More comprehensive than Official Poverty Measure

**Gini coefficient:**
- Measures income inequality (0 = perfect equality, 1 = perfect inequality)
- US Gini is typically around 0.48
- Lower values = more equal income distribution

**Income deciles:**
- Population divided into 10 equal groups by income
- Decile 1 = bottom 10% of earners
- Decile 10 = top 10% of earners

**Winners and losers:**
- Winners: Net income increases by 5% or more
- Losers: Net income decreases by 5% or more
- Neutral: Net income change less than 5%

### Reading Charts

**Household impact charts:**
- X-axis: Usually income or earnings
- Y-axis: Net income, taxes, or benefits
- Hover to see exact values

**Population impact charts:**
- Bar charts: Compare across groups (deciles, states)
- Line charts: Show relationships (income vs impact)
- Waterfall charts: Show components of budgetary impact

## Common Use Cases

### Use Case 1: How Does Policy X Affect My Household?

1. Go to household calculator
2. Enter your information
3. Select "Reform" and choose the policy
4. Compare baseline vs reform results

### Use Case 2: How Much Would Policy X Cost?

1. Go to policy page
2. Create or select the reform
3. View "Budgetary impact" section
4. See total cost and breakdown

### Use Case 3: Would Policy X Reduce Poverty?

1. Go to policy page
2. Create or select the reform
3. View "Poverty impact" section
4. See change in poverty rate by age group

### Use Case 4: Who Benefits from Policy X?

1. Go to policy page
2. Create or select the reform
3. View "Distributional impact" section
4. See winners and losers by income decile

### Use Case 5: Compare Two Policy Proposals

1. Create Reform A (e.g., expand EITC)
2. Note the URL or reform ID
3. Create Reform B (e.g., expand CTC)
4. Compare budgetary, poverty, and distributional impacts

## For Analysts: Moving Beyond the Web App

Once you understand the web app, you can:

**Use the Python client:**
- See `policyengine-python-client-skill` for programmatic access
- See `policyengine-us-skill` for detailed simulation patterns

**Create custom analyses:**
- See `policyengine-analysis-skill` for analysis patterns
- See `microdf-skill` for data analysis utilities

**Access the API directly:**
- See `policyengine-api-skill` for API documentation
- REST endpoints for integration

## For Contributors: Building PolicyEngine

To contribute to PolicyEngine development:

**Understanding the stack:**
- See `policyengine-core-skill` for engine architecture
- See `policyengine-us-skill` for country model patterns
- See `policyengine-api-skill` for API development
- See `policyengine-app-skill` for app development

**Development standards:**
- See `policyengine-standards-skill` for code quality requirements
- See `policyengine-writing-skill` for documentation style

## Frequently Asked Questions

### How accurate is PolicyEngine?

PolicyEngine uses official tax and benefit rules from legislation and regulations. Calculations match official calculators (IRS, SSA, etc.) for individual households.

Population-level estimates use microsimulation with survey data (Current Population Survey for US, Family Resources Survey for UK).

### Can I use PolicyEngine for my taxes?

PolicyEngine is for policy analysis, not tax filing. Results are estimates based on the information you provide. For filing taxes, use IRS.gov or professional tax software.

### How is PolicyEngine funded?

PolicyEngine is a nonprofit funded by grants and donations. The platform is free to use.

### Can I export results?

Yes! Charts can be downloaded as PNG or HTML. You can also share reform URLs with others.

### What programs does PolicyEngine model?

**US (federal):**
- Income tax, payroll tax, capital gains tax
- EITC, CTC, ACTC
- SNAP, WIC, ACA premium tax credits
- Social Security, SSI, TANF
- State income taxes (varies by state)

**UK:**
- Income tax, National Insurance
- Universal Credit, Child Benefit
- State Pension, Pension Credit
- Council Tax, Council Tax Support

For complete lists, see:
- US: https://policyengine.org/us/parameters
- UK: https://policyengine.org/uk/parameters

### How do I report a bug?

**If you find incorrect calculations:**
1. Go to the household calculator
2. Note your inputs and the incorrect result
3. File an issue: https://github.com/PolicyEngine/policyengine-us/issues (or appropriate country repo)
4. Include the household URL

**If you find app bugs:**
1. Note what you were doing
2. File an issue: https://github.com/PolicyEngine/policyengine-app/issues

## Resources

- **Website:** https://policyengine.org
- **Documentation:** https://policyengine.org/us/docs
- **Blog:** https://policyengine.org/us/research
- **GitHub:** https://github.com/PolicyEngine
- **Contact:** hello@policyengine.org

## Related Skills

- **policyengine-python-client-skill** - Using PolicyEngine programmatically
- **policyengine-us-skill** - Understanding US tax/benefit calculations
- **policyengine-analysis-skill** - Creating custom policy analyses
