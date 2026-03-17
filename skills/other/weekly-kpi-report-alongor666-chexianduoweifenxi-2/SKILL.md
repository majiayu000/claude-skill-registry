---
name: weekly-kpi-report
description: Generate McKinsey-style board presentation PPTs from weekly auto insurance data. Automatically calculates 16+ KPIs, creates executive-level slides with actionable insights, and supports week-over-week comparisons. Use when user uploads insurance cost data (Excel/CSV) and requests board report, weekly presentation, executive briefing, or mentions keywords like 董事会汇报, 周报PPT, 经营分析演示, McKinsey-style reports.
---

# Weekly KPI Report Generator (McKinsey Style)

## Purpose

Transform weekly auto insurance policy cost data into executive-ready board presentation slides using McKinsey consulting design principles. Generate data-driven insights with conclusion-first structure, professional visualization, and actionable recommendations.

## Quick Start

### Three-Step Generation Process

1. **Upload Data**: Provide weekly insurance cost data file (Excel/CSV)
2. **Automatic Processing**: Skill validates data, calculates KPIs, and generates insights
3. **Download PPT**: Receive McKinsey-style board presentation ready for executive meeting

### Basic Usage Example

```
User: "Generate board report from this week's insurance data"

Assistant (using this skill):
1. Validates uploaded file and extracts week number
2. Calculates 16+ KPIs (cost rates, premium progress, loss ratios)
3. Generates 12-13 slide deck with:
   - Executive summary with key insights
   - Institutional and customer segment analysis
   - Problem-oriented headlines with actionable recommendations
4. Returns: "{Organization}_Week{N}_McKinsey_Report.pptx"
```

### Minimal Requirements

- **Input**: Excel/CSV file with insurance policy cost data
- **Week Number**: Extracted from filename or user-provided
- **Configuration** (optional): Custom thresholds in `references/config.json`
- **Output**: Professional PPT with charts, insights, and recommendations

## When to Use This Skill

Trigger this skill when:

- User uploads auto insurance weekly cost data (Excel/CSV format) and requests board presentation
- User mentions keywords: "董事会汇报", "周报PPT", "经营分析演示", "board report", "executive briefing"
- User asks to generate presentation slides from insurance data
- User requests McKinsey-style or consulting-style reports

## Core Workflow

### Step 1: Data Validation

Execute the data validator to ensure data quality:

```bash
python scripts/data_validator.py <uploaded_file_path>
```

The validator checks:

- Required field completeness (policy numbers, premium amounts, cost rates)
- Data type correctness (numeric fields, date formats)
- Week number extraction from filename (e.g., "第45周" → Week 45)
- Record count and date range calculation

### Step 2: KPI Calculation

Calculate board-level KPIs (not raw data dumps):

```bash
python scripts/kpi_calculator.py <file_path> <week_number>
```

**Four KPI Categories:**

1. **Business Scale**
   - Weekly premium revenue and growth rate
   - Policy count and average premium per policy
   - Business type distribution (truck/passenger/private)

2. **Profitability**
   - Combined ratio (loss ratio + expense ratio)
   - Variable cost rate distribution and outliers
   - Profitability comparison by customer segment

3. **Business Structure**
   - New energy vehicle (NEV) penetration rate and trend
   - Renewal rate vs. new policy ratio
   - Contribution by distribution channel

4. **Risk Management**
   - Claims frequency and high-risk business proportion
   - Average claim amount changes
   - Risk exposure in high-risk segments (e.g., highway freight)

### Step 3: Generate McKinsey-Style PPT

Create presentation slides with consulting-grade design:

```bash
python scripts/board_ppt_generator.py <week_number> <kpi_data_json>
```

**Slide Structure (7 slides):**

1. **Cover** - Title, date range, presenter
2. **Executive Summary** - Core metrics with top 3 highlights/risks
3. **Premium Analysis** - Revenue trends, business mix, YoY comparison
4. **Profitability Analysis** - Combined ratio breakdown, cost rate by segment
5. **NEV Business Focus** - NEV penetration, loss ratio comparison vs. traditional vehicles
6. **Risk Management** - Claims frequency heatmap, high-risk business list
7. **Action Items** - Auto-generated recommendations based on data patterns

Refer to [references/mckinsey-style-guide.md](references/mckinsey-style-guide.md) for detailed design principles.

### Step 4 (Optional): Week-over-Week Comparison

When user provides data for two consecutive weeks:

```bash
python scripts/optional_modules/week_comparator.py <week1_kpis.json> <week2_kpis.json>
```

Generates additional comparison slide showing WoW changes in key metrics.

## Design Principles

**McKinsey Three Pillars:**

1. **Conclusion-First Titles** - Every slide title answers "So what?"
   - ❌ Wrong: "Profitability Analysis"
   - ✅ Right: "Profitability remains healthy with 83.9% combined ratio below industry benchmark"

2. **Minimalist Layout** - Less is more
   - Large white space (0.8" margins)
   - Single red accent line at top
   - No excessive decorations or logo stacking

3. **Left-Aligned Structure** - Professional business style
   - Title left-aligned (24pt, conclusion statement)
   - Left column: bullet points
   - Right column: supporting charts
   - Bottom: italic recommendations (12pt)

**Color Scheme:**
Uses client-specific colors extracted from corporate reports:

- Primary: Deep Red (#a02724) - 60% usage for core messages
- Alert: Bright Red (#c00000) - warnings and risks
- Text: Black (#000000) - titles and important text
- Background: White (#FFFFFF) - clean backdrop

Configure colors in [assets/mckinsey_config.json](assets/mckinsey_config.json).

## Configuration

### Alert Thresholds

Customize business rules in [config.json](config.json):

```json
{
  "预警阈值": {
    "综合成本率_上限": 95, // Alert if combined ratio > 95%
    "新能源车赔付率差距": 10 // Alert if NEV loss ratio > traditional + 10pp
  }
}
```

### Display Parameters

```json
{
  "报表参数": {
    "显示TOP业务类型数": 5, // Show top 5 business types
    "显示TOP机构数": 5 // Show top 5 distribution channels
  }
}
```

Refer to [references/config-guide.md](references/config-guide.md) for full configuration options.

## Usage Examples

**Example 1: Basic Usage**

```
User: 我上传了第45周的车险数据,帮我生成董事会汇报PPT

Execution:
1. Identify file: "车险保单变动成本清单__第45周_.xlsx"
2. Run data_validator.py
3. Run kpi_calculator.py with config.json thresholds
4. Run board_ppt_generator.py using assets/mckinsey_board_template.pptx
5. Output: "华安车险周报_第45周_麦肯锡版.pptx"
6. Return download link with brief data summary
```

## Error Handling

- **Missing week number in filename** → Prompt user to confirm week number
- **Missing required fields** → List missing columns and ask whether to proceed
- **All cost rates abnormal (>100%)** → Warning that data may be incorrect
- **Invalid JSON config** → Use default values and notify user

## Technical Stack

- **Data processing:** pandas, numpy
- **Visualization:** matplotlib (Chinese font handling), seaborn
- **PPT generation:** python-pptx
- **Template:** assets/mckinsey_board_template.pptx
- **Field Mapping:** field_mapping.json (支持中英文字段自动适配)
- **Supported Data Formats:**
  - Excel files (.xlsx, .xls) with Chinese field names
  - CSV files (.csv) with English field names (e.g., from transformed data)

## Output Location

Generated PPT files saved to: `/mnt/user-data/outputs/`

Filename format: `华安车险周报_第{week_number}周_麦肯锡版.pptx`

## Version Information

- **Version:** v2.0.0 (Field Mapping Support)
- **Last Updated:** 2025-12-08
- **Maintainer:** Alongor
- **Data Source:** Hua'an Insurance Sichuan Branch weekly auto insurance reports
- **Supported Formats:** Excel (.xlsx, .xls), CSV (.csv)
- **Supported Field Names:** Chinese (跟单保费, 业务类型分类) and English (signed_premium_yuan, business_type_category)
