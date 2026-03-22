---
name: managing-dei-metrics
description: Structures diversity, equity, and inclusion data collection with benchmarking and disclosure requirements. Use when analyzing DEI metrics, benchmarking diversity, or preparing DEI disclosures.
tags:
  - management
  - sustainable-finance
metadata:
  author: casemark
  practice_areas:
    - ESG
    - Impact Investing
    - Sustainable Finance
  document_types:
    - Management Report
  skill_modes:
    - Management
    - Coordination
---
# Managing DEI Metrics

Structures diversity, equity, and inclusion data collection, benchmarking against peer and industry standards, and preparation of disclosure-ready DEI reports for ESG frameworks and investor communications.

## When To Use

- Building or auditing a portfolio company's DEI data collection infrastructure
- Benchmarking workforce composition against industry peers or index constituents
- Preparing DEI disclosures for annual reports, sustainability reports, or LP questionnaires
- Responding to ESG rating agency questionnaires (MSCI, Sustainalytics, ISS) that include diversity dimensions
- Evaluating fund-level or GP-level diversity commitments (e.g., ILPA diversity metrics template)
- Supporting regulatory disclosure under Nasdaq board diversity rules, EU CSRD, or UK FCA diversity requirements [VERIFY]

## Inputs To Gather

- **Entity scope**: Fund-level, GP-level, or portfolio company-level; single entity or aggregated
- **Reporting framework(s)**: SASB, GRI 405/406, TCFD-adjacent social metrics, ILPA template, UNPRI, proprietary LP templates
- **Metric categories**: Board composition, senior leadership, overall workforce, new hires, promotions, attrition, pay equity
- **Demographic dimensions**: Gender, race/ethnicity, age, disability status, veteran status; confirm which are legally collectible in relevant jurisdictions [VERIFY]
- **Benchmark sources**: Industry peer set, index composition data, national labor force statistics (e.g., BLS EEO-1 categories for US)
- **Reporting period**: Fiscal year, calendar year, or point-in-time snapshot date
- **Prior period data**: At least one prior period for trend analysis; ideally two or more for trajectory assessment
- **Data collection method**: Self-identification surveys, HRIS exports, board questionnaires, third-party data providers

## Workflow

1. **Define metric taxonomy**
   - Map requested metrics to reporting framework definitions (e.g., GRI 405-1 distinguishes governance bodies vs. employees by category)
   - Standardize demographic category labels across entities if aggregating multiple portfolio companies
   - Confirm legal permissibility of collecting each demographic dimension per jurisdiction [VERIFY]

2. **Collect and validate raw data**
   - Ingest HRIS or survey data; flag response rates below 70% as potentially non-representative
   - Cross-check headcount totals against payroll or financial records
   - Identify missing data points and mark with [VERIFY] rather than imputing values
   - Note self-identification opt-out rates separately — do not merge "declined to state" with any demographic category

3. **Calculate core metrics**
   - Representation percentages by level (board, C-suite, VP+, manager, individual contributor)
   - Year-over-year change in representation at each level
   - Hiring and promotion rates by demographic group relative to applicant/eligible pool
   - Attrition rates by demographic group (voluntary vs. involuntary where available)
   - Pay equity ratios (median and mean) by gender and race/ethnicity, controlling for role level and geography where data permits

4. **Benchmark against peers**
   - Source industry benchmarks from relevant datasets (e.g., McKinsey Diversity Wins, Equileap, Bloomberg Gender-Equality Index)
   - Present entity metrics alongside 25th, 50th, and 75th percentile benchmarks
   - Flag metrics where entity falls below 25th percentile as areas of concern
   - Note benchmark vintage — stale benchmarks (>2 years old) should be flagged

5. **Assess disclosure readiness**
   - Map completed metrics to each target framework's required and recommended fields
   - Identify gaps: missing metrics, insufficient granularity, or data quality issues
   - For regulated disclosures (Nasdaq, CSRD, FCA), confirm all mandatory fields are populated [VERIFY]
   - Draft narrative context for quantitative metrics — explain material changes, initiatives underway, and targets

6. **Compile output report**
   - Structure by audience: investor-facing summary, internal management detail, regulatory submission
   - Include methodology notes covering data sources, response rates, category definitions, and benchmark sources
   - Attach data tables in appendix format suitable for LP due diligence or rating agency submission

## Output

A DEI metrics management report containing:

- **Executive summary**: Key representation figures, notable trends, and peer positioning
- **Detailed metrics tables**: Broken out by level, demographic dimension, and reporting period
- **Benchmark comparison**: Entity vs. peer/industry percentiles with visual indicators (above/below median)
- **Gap analysis**: Missing data points, framework compliance gaps, and recommended remediation steps
- **Methodology appendix**: Data sources, collection dates, response rates, category definitions, benchmark vintage
- **Disclosure crosswalk**: Matrix mapping available metrics to each target framework's line items

## Quality Checks

- Confirm all percentages within a category sum to 100% (accounting for rounding)
- Verify headcount figures reconcile to a known source of truth (payroll, board roster)
- Ensure no personally identifiable information appears in output — all data must be aggregated
- Check that small-group thresholds are applied (suppress demographic breakdowns where group size < 5 to prevent re-identification)
- Validate that benchmark comparisons use matching scope (e.g., same industry classification, comparable entity size)
- Confirm disclosure crosswalk covers all mandatory fields for each specified framework [VERIFY]
- Flag any metric where data quality or coverage is insufficient with [VERIFY] and a brief explanation
