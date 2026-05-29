---
name: Support Data Analyzer
description: Analyze customer support data (Excel/CSV with PIT, Support Tickets, CSAT) to categorize issues, prioritize by impact (P0-P3), and generate strategic markdown reports with examples and trends.
version: 1.1.0
dependencies: python>=3.8, openpyxl>=3.0.0, pandas>=1.3.0
allowed-tools: [Bash, Read, Write]
---

## Overview

This Skill analyzes customer support feedback from multiple data sources (PIT/Roadblocks, Support Tickets, CSAT surveys, Ideas Forum) to identify pain points, categorize by theme, prioritize by customer impact, and generate comprehensive strategic reports.

**Supports two analysis modes:**
1. **Comprehensive Analysis**: Full categorization, prioritization, and strategic reporting (initial analysis)
2. **Targeted Deep-Dive**: Timeline analysis, theme investigation, resolution tracking (follow-up queries)

## When to Apply

**Use this skill for analysis of structured support data in the expected format:**

**Initial Analysis:**
- User provides Excel/CSV files with PIT/Roadblocks, Support Tickets, or CSAT data columns
- User asks to "analyze support data", "prioritize customer feedback", or "generate impact report"
- User wants to understand top customer pain points from support channels
- User needs to scope analysis to a specific time period (e.g., "last 60 days")

**Expected data format:** Excel/CSV with columns like frustration level, MRR, ticket categories, CSAT scores

**Follow-up Analysis:**
- User asks about specific findings: "Has X issue dropped off?", "Show timeline for Y"
- User wants to investigate a theme mentioned in existing reports
- User needs to verify if an issue is resolved/declining/active
- User asks for examples or details about a specific category

**In scope:**
- Categorizing issues by product area and sub-category
- Calculating volume, frustration levels, and revenue impact
- Assigning priority levels (P0, P1, P2, P3) based on multiple factors
- Generating markdown reports with executive summaries and customer examples
- **Timeline analysis and trend tracking for specific issues**
- **Deep-dive investigation of specific themes**
- Comparing recent trends vs. historical baselines
- CSAT analysis and correlation

**Out of scope:**
- Sentiment analysis requiring NLP models not available in environment
- Predictive forecasting of future support volumes
- Root cause analysis requiring engineering investigation
- Data collection or export from live systems (only analyzes provided files)

## Inputs

**Required:**
- Excel file(s) or CSV file(s) containing support data with these datasets:
  - **PIT & Roadblocks**: Strategic customer issues with frustration levels (1-5), MRR data, categories, submitted dates
  - **Support Tickets**: Support cases with product areas, roadblock types, created dates, ticket content
  - **Optional but recommended**: CSAT survey responses, Ideas Forum requests

**Optional:**
- Time range filter (e.g., "last 60 days", "Q4 2025")
- Historical baseline data for trend comparison
- Specific focus areas (e.g., "focus on association issues")

**Expected data columns:**
- PIT data: Submitted At Date, Category, Sub Category, Frustration Level (1-5), MRR (CS), MRR (Sales), Use Case Title, Use Case Body
- Support data: Created UTC Date, Support Product Area, Support roadblock, Ticket Name, Content
- CSAT data: Created At Date, Score (1-5), Text, Event Trigger

## Outputs

**Primary artifact:**
- Comprehensive markdown report (`*_Support_Analysis.md`) containing:
  - Executive summary with top 3 critical areas
  - Prioritized themes by P0, P1, P2, P3 with metrics
  - Customer feedback examples (5 per major theme)
  - Strategic recommendations
  - Revenue at risk analysis
  - Frustration heatmap
  - Trend comparison (if historical data provided)

**Optional artifacts:**
- Customer feedback examples document with detailed quotes
- CSV extracts of filtered data for further analysis

**Success criteria:**
- Issues categorized into clear themes (e.g., "Object > Associations")
- Priority levels assigned with clear rationale
- At least 3-5 real customer examples per P0/P1 issue
- Actionable recommendations with impact estimates

## Instructions for Claude

### Step 1: Data Loading and Validation
1. Convert Excel files to CSV if needed using Python openpyxl
2. Read all data sources and display summary:
   - Total records per source
   - Date range coverage
   - Column validation (check for required fields)
3. If time filter specified, parse and apply date filtering
4. Report filtered counts and date ranges

### Step 2: Theme Categorization
1. Combine issues by theme: `{Product Area} > {Sub Category/Roadblock}`
2. For each theme, calculate:
   - Total count (PIT + Support tickets)
   - PIT count and Support count separately
   - Average frustration (from PIT data where available)
   - High frustration count (frustration ≥ 4)
   - Total MRR impact (sum of MRR (CS) + MRR (Sales) from PIT data)
3. Sort themes by total count descending
4. Calculate percentage of total for each theme

### Step 3: Priority Assignment
Apply the prioritization framework from `resources/PRIORITIZATION_FRAMEWORK.md`:

**P0 (Critical):**
- Volume >150 issues (60-day) OR >1,000 issues (historical) OR
- High frustration (avg ≥3.5) + volume >100 OR
- Revenue impact >$75K (60-day) OR >$4M (historical) OR
- Increasing trend (>20% vs baseline)

**P1 (High):**
- Volume 100-150 (60-day) OR 700-1,000 (historical) OR
- Frustration avg 3.0-3.5 with volume >50 OR
- Revenue impact $25K-$75K (60-day) OR $1.5M-$4M (historical)

**P2 (Medium):**
- Volume 30-100 (60-day) OR 200-700 (historical) OR
- High frustration (≥3.5) with lower volume OR
- Specialized use cases affecting specific segments

**P3 (Lower):**
- Volume <30 (60-day) OR <200 (historical)
- Administrative/low-frequency issues
- Lower frustration with low volume

### Step 4: Customer Example Selection
For each P0 and P1 theme:
1. Select 5 diverse customer examples:
   - Mix of PIT issues (strategic feedback with frustration/MRR) and support tickets (tactical issues)
   - Prioritize high frustration examples (≥4) first
   - Include variety: different use cases, customer sizes, specific vs. general
2. For each example, extract:
   - Issue title/ticket name
   - Frustration level (if PIT data)
   - MRR (if available)
   - Full description/content (first 300 chars)
3. Add interpretation: "What this means:" explaining the customer impact

### Step 5: CSAT Analysis (if data provided)
1. Calculate overall metrics:
   - Average score
   - Distribution by score (1-5)
   - Dissatisfaction rate (<4)
2. Identify top event triggers (what actions prompted survey)
3. Correlate CSAT triggers with support themes
4. Extract sample low-score feedback with categories

### Step 6: Trend Analysis (if historical data provided)
1. Compare key metrics between time periods:
   - Average frustration change
   - Volume change by theme (percentage point shifts)
   - New themes emerging in top 10
2. Identify "getting worse" vs "improving" patterns
3. Flag NEW issues (not in historical top 10 but now top 5)

### Step 7: Report Generation
Use the structure from `resources/REPORT_TEMPLATE.md`:

1. **Executive Summary** (must include):
   - Total issues analyzed
   - Top 3 critical areas with one-line description
   - Key changes vs historical (if applicable)
   - Overall frustration trend
   - Total revenue at risk

2. **Detailed Analysis by Priority**:
   - For each P0, P1, P2 theme:
     - Metrics table (volume, frustration, MRR, % of total)
     - Key pain points (bulleted list)
     - 5 customer examples with "What this means"
     - "Why P0/P1/P2" explanation

3. **Strategic Recommendations**:
   - Immediate actions (P0)
   - High priority (P1)
   - Cross-cutting initiatives
   - Impact estimates

4. **Supporting Sections**:
   - Revenue at risk table
   - Frustration heatmap
   - Comparison tables (if trend analysis)
   - Methodology appendix

---

## Follow-up Analysis Workflow (Deep-Dive Queries)

When user asks specific questions about existing reports (e.g., "Has autosave issue been resolved?", "Show timeline for association complaints"), use this targeted analysis approach:

### Step 1: Understand the Context
1. Read existing analysis report (if available) to understand:
   - Source file path from YAML frontmatter
   - Date range of existing analysis
   - What theme/issue the user is asking about
2. Optionally grep or read data.csv to see how issues were categorized

### Step 2: Install Required Dependencies
```bash
pip3 install openpyxl pandas --break-system-packages --quiet
```

**Important:** Use `--break-system-packages` flag on macOS to bypass externally-managed-environment errors.

### Step 3: Load Raw Data with Python
Use Python via Bash tool with heredoc to load and analyze Excel data:

```python
python3 << 'EOF'
import openpyxl
import pandas as pd
from datetime import datetime, timedelta

# Load Excel file
wb = openpyxl.load_workbook('/full/path/to/feedback-data/file.xlsx')

# Process PIT and Roadblocks sheet
pit_sheet = wb['PIT and Roadblocks']
pit_data = []
pit_headers = [cell.value for cell in pit_sheet[1]]

for row in pit_sheet.iter_rows(min_row=2, values_only=True):
    pit_data.append(dict(zip(pit_headers, row)))

pit_df = pd.DataFrame(pit_data)

# Process Support Data sheet
support_sheet = wb['Support Data']
support_data = []
support_headers = [cell.value for cell in support_sheet[1]]

for row in support_sheet.iter_rows(min_row=2, values_only=True):
    support_data.append(dict(zip(support_headers, row)))

support_df = pd.DataFrame(support_data)

# Continue with analysis...
EOF
```

### Step 4: Filter and Analyze
```python
# Filter for specific keyword/theme
pit_filtered = pit_df[
    pit_df['Use Case Title'].fillna('').str.contains('keyword', case=False, na=False) |
    pit_df['Use Case Body'].fillna('').str.contains('keyword', case=False, na=False)
].copy()

support_filtered = support_df[
    support_df['Ticket Name'].fillna('').str.contains('keyword', case=False, na=False) |
    support_df['Content'].fillna('').str.contains('keyword', case=False, na=False)
].copy()

# Timeline analysis
support_filtered['Created UTC Date'] = pd.to_datetime(support_filtered['Created UTC Date'], errors='coerce')
support_filtered['Month'] = support_filtered['Created UTC Date'].dt.to_period('M')
monthly_counts = support_filtered.groupby('Month').size()

print("Monthly breakdown:")
for month, count in monthly_counts.items():
    print(f"  {month}: {count} issues")

# Trend analysis
print(f"\nMost recent: {support_filtered['Created UTC Date'].max()}")
print(f"Oldest in dataset: {support_filtered['Created UTC Date'].min()}")
print(f"Total issues: {len(pit_filtered) + len(support_filtered)}")

# Check recent activity (last 30 days)
recent_cutoff = datetime.now() - timedelta(days=30)
recent = support_filtered[support_filtered['Created UTC Date'] >= recent_cutoff]
print(f"Issues in last 30 days: {len(recent)}")
```

### Step 5: Generate Insights
Based on the Python output, provide:
1. **Total volume** of issues matching the query
2. **Timeline breakdown** (monthly or weekly counts)
3. **Trend analysis**: % change from peak to current, identify drop-offs
4. **Status determination**: Resolved / Declining / Active / Increasing
5. **Specific examples** with dates, frustration scores, MRR values
6. **Recommendation**: Whether issue needs action or can be marked resolved

### Step 6: Update Existing Report (if applicable)
If the deep-dive reveals the issue is resolved/declining, update the existing report.md:
- Add notes to relevant examples marking them as "(RESOLVED)" or "(DECLINING)"
- Add timeline analysis to report appendix
- Update Strategic Recommendations section
- Add update note to YAML frontmatter

### Example: Autosave Timeline Analysis
**User question:** "Has the autosave issue been resolved?"

**Steps taken:**
1. Read report.md to get source file: `feedback-data/2025-11-03_data-platform-code-orange.xlsx`
2. Installed pandas/openpyxl
3. Loaded raw Excel, filtered for "autosave" mentions in both PIT and Support sheets
4. Grouped by month to see trend: April 2025 (9 issues) → Oct 2025 (2 issues)
5. Calculated 89% decline from peak
6. Determined status: **RESOLVED**
7. Updated report.md with timeline analysis and marked examples as resolved

---

### Edge Cases and Tie-Breakers
- **Missing MRR data**: Use volume + frustration only for priority
- **Ties in volume**: Prioritize higher average frustration
- **Low sample PIT data**: Weight support ticket volume more heavily
- **Conflicting signals** (high volume, low frustration): Assign P1 and note in report
- **New themes**: Flag explicitly as "NEW to top X" in report

### Quality Checks
Before finalizing report:
- [ ] Executive summary has specific numbers (not vague)
- [ ] Each P0/P1 has exactly 5 customer examples
- [ ] Examples include "What this means" interpretation
- [ ] Recommendations are actionable with timelines/impact
- [ ] All percentages sum correctly
- [ ] MRR totals are accurate
- [ ] Customer voice quotes are real (not synthesized)

## Examples

### Example Input
```
User: "Can you analyze this support data and prioritize the top issues? Focus on the last 60 days."

Files provided:
- Data Platform data - Code Orange.xlsx (contains sheets: Ideas Forum, CSAT, PIT and Roadblocks, Support Data)
```

### Example Output
```markdown
# Data Platform Support Data - Prioritized Analysis (Last 60 Days)

**Analysis Date:** October 31, 2025
**Time Period:** September 1, 2025 - October 31, 2025 (60 days)
**Total Issues Analyzed:** 2,201

## Executive Summary

Analysis of **2,201 customer issues from the last 60 days** reveals:

### Top 3 Critical Areas (P0):

1. **Object Associations** - 468 issues (27.5%), $141K MRR, 3.38 avg frustration
   - Association labels unavailable in reports (most common complaint)

2. **Property Edit** - 232 issues (13.6%), $96K MRR, 3.06 avg frustration
   - Cannot edit internal values after creation

3. **Property Values & History** - 223 issues (13.1%), $80K MRR
   - NEW to top 3 - sync delays and data integrity issues

**Key Changes vs. Historical:**
- Frustration increased 14% (2.71 → 3.09/5)
- Associations now 27.5% of issues (up from 24%)
- Property Values jumped to #3 (was #4)

**Total Revenue at Risk:** $684K MRR

---

## P0 - CRITICAL IMPACT

### 1. Object Associations (468 issues | $141K MRR)

**Metrics:**
- Volume: 21 PIT + 447 Support
- Average Frustration: 3.38/5
- Percentage of Total: 27.5%

**Key Pain Points:**
- Association labels unavailable in reports and lists
- Cannot filter or segment by association labels
- Workflow retrieval requiring custom code

**Customer Examples:**

#### Example 1: Association Label Limits
**Frustration:** 5/5 | **MRR:** $4,049
> "Client wants to be able to have up to 900+ nested relationships, but we cap our association labels at 50."

**What this means:** Customers with complex business models (B2B2B, franchises) hit hard limits on relationship types, forcing them to abandon tracking or use workarounds.

[... 4 more examples ...]

**Why P0:** Highest volume (27.5% of all issues), increasing trend, critical for CRM functionality.

---

## Strategic Recommendations

### Immediate Actions (P0)
1. **Associations Crisis Management**
   - Action: Enable association labels in reports/lists
   - Impact: 468 issues, $141K MRR
   - Timeline: 30 days

[... continued ...]
```

## Testing Checklist

- [ ] Frontmatter present with name ≤64 chars, description ≤200 chars
- [ ] Description clearly states when to use ("analyze customer support data")
- [ ] YAML dependencies listed (python, openpyxl)
- [ ] At least one complete input/output example
- [ ] Resources files present and referenced
- [ ] No hardcoded customer data or secrets
- [ ] Priority framework is objective and consistent
- [ ] Example customer quotes are real (not generated)

## Security & Privacy

**Data Handling:**
- Support data may contain customer PII (names, emails, company names)
- Do NOT redact customer examples in internal reports (needed for context)
- Do NOT include customer data in Skill files themselves (only process at runtime)
- If creating external reports, ask user if customer names should be redacted

**File Storage:**
- Converted CSV files stored in /tmp (ephemeral)
- Final reports saved to user-specified location (default: ~/Downloads)
- Do not commit support data to git repositories

**MRR Data:**
- Treat MRR values as confidential
- Include in internal reports but flag if report will be shared externally

## Resources

See `resources/` folder for:
- **PRIORITIZATION_FRAMEWORK.md**: Detailed criteria for assigning P0-P3
- **REPORT_TEMPLATE.md**: Complete markdown template with all sections
- **EXAMPLES.md**: Sample analyses with annotations
- **ANALYSIS_SCRIPT.py**: Python helper for data processing (optional)
