---
name: shipping-data-analysis
description: |
  Shipping Data Analysis - Brock's Reusable Prompt v4.0
  Analyzes any shipping dataset with FirstMile-branded deliverables, normalized address grouping,
  and conditional advanced analytics based on available data fields.

  Use when:
  (1) Prospect provides shipping data (PLD, exports, etc.)
  (2) "analyze shipping data" or "shipping analysis"
  (3) "run Brock's prompt" or "data analysis v4.0"
  (4) Need DIM exposure, zone distribution, or cost intelligence reports
  (5) Creating prospect-facing shipping profile analysis

  Triggers on: "shipping analysis", "analyze shipping", "PLD analysis", "Brock's prompt",
               "data analysis v4.0", "shipping profile", "DIM exposure", "zone distribution"
---

# Shipping Data Analysis Skill

> *Brock Hansen's Reusable Prompt v4.0 - FirstMile branded shipping analytics*
> *Updated: January 7, 2026 - F.R.O.G. Fulfillment analysis learnings*

## Overview

This skill generates comprehensive shipping analysis workbooks using Brock's standardized v4.0 prompt structure. It produces up to 16 Excel sheets with FirstMile branding, intelligent address normalization, and conditional advanced analytics.

## Quick Start

```
/shipping-analysis [file.xlsx] --company "Company Name"
```

## Required Inputs

| Input | Description |
|-------|-------------|
| **File** | Excel/CSV with shipping data |
| **Company Name** | Used in all report titles |
| **Column Mapping** | Map your columns to standard fields |

## Column Mapping (Required)

| Field | Your Column | Notes |
|-------|-------------|-------|
| Order Date | _____ | "Label Processed On", "Order Date", "Ship Date" |
| Ship Address (Origin) | _____ | Warehouse/fulfillment center or Client Name as proxy |
| Service Level | _____ | Carrier service name |
| Tracking Number | _____ | For carrier inference |
| Weight | _____ | Specify oz or lbs |
| Dimensions | _____ | L/W/H or DIMS Grouped |

### Date Column Detection Priority

**CRITICAL**: PLD exports often have empty "Ship Date" columns. Check these in order:
1. `Label Processed On` - Usually has actual timestamps (e.g., "9/12/2025 2:47:54 PM")
2. `Ship Date` - Often empty in PLD exports
3. `Order Date`, `Created Date` - Fallback options

```python
# Detection logic
if 'Label Processed On' in df.columns:
    date_col = 'Label Processed On'  # Priority - usually has data
else:
    # Fall back to keyword search
    for col in df.columns:
        if 'date' in col.lower() or 'processed' in col.lower():
            # Verify column has actual date values
            test = pd.to_datetime(df[col].dropna().head(10), errors='coerce')
            if test.notna().sum() > 5:
                date_col = col
                break
```

## Optional Columns (Enable Advanced Modules)

| Field | Enables |
|-------|---------|
| Delivered Date | Transit time & on-time analysis |
| Destination ZIP/State | Zone distribution & lane analysis |
| Zone | Zone distribution sheet |
| Total Charge/Cost | Cost intelligence module |
| Surcharges | Surcharge mix analysis |
| L/W/H Dimensions | DIM exposure analysis |

## Output Structure

### Core Sheets (Always Generated)

| # | Sheet | Content |
|---|-------|---------|
| 1 | Executive Summary | 3-column layout: Metrics, Top Origins, Weight Bands |
| 2 | Monthly Shipments | Monthly breakdown with percentages |
| 3 | Bill Weight Distribution | Individual weights (1 oz, 2 oz... 1 lb, 2 lb...) |
| 4 | DIMS Grouped Distribution | Dimension combos by count |
| 5 | Ship Address Distribution | Normalized addresses or Client as proxy |
| 6 | Service Level Distribution | Carrier x Service matrix |

### Conditional Sheets (If Data Exists)

| # | Sheet | Requires |
|---|-------|----------|
| 7 | Zone Distribution | Zone column |
| 8 | Destination Footprint | Dest State/ZIP |
| 9 | Transit Time Analysis | Delivered Date + Ship Date |
| 10 | Cost Intelligence | Total Charge/Cost |
| 11 | Surcharge Analysis | Surcharge columns |
| 12 | DIM Exposure Analysis | L/W/H + Scale Weight |
| 13 | Service Level Mismatch | Delivered Date |
| 14 | Operational Trends | 4+ weeks data |
| 15 | Data Quality & Exceptions | All fields (checks missing) |
| 16 | Claims/Exception Exposure | Exception Code/Status |

## Executive Summary - 3-Column Layout

**CRITICAL**: Executive Summary must use the 3-column side-by-side layout:

```
| Metrics (A-B)          | Top Origins (D-F)      | Weight Bands (G-I)     |
|------------------------|------------------------|------------------------|
| Total Shipments: X     | Client: Count (%)      | 1 oz: Count (%)        |
| Date Range: X to Y     | Client: Count (%)      | 2 oz: Count (%)        |
| Days Covered: X        | Client: Count (%)      | ...                    |
| Avg Monthly Volume: X  | ...                    | 15.99 oz: Count (%)    |
| Unique Clients: X      |                        | 1 lb: Count (%)        |
| Avg Weight (lb): X     |                        | 2 lb: Count (%)        |
| Median Weight (lb): X  |                        | ...                    |
| Avg Weight (oz): X     |                        | 50 lb: Count (%)       |
| Median Weight (oz): X  |                        | 50+ lbs: Count (%)     |
```

### Layout Structure

- **Row 1**: Navy title spanning all columns (A1:I1 merged)
- **Row 2**: Green section headers (Metric|Value, Top Origin IDs, Weight Band Breakdown)
- **Row 3**: Green sub-headers for middle/right sections
- **Row 4+**: Data rows

## Weight Distribution Format

**CRITICAL**: Use individual weights, NOT bands like "0-5 lb" or "5-10 lb".

### Correct Format (Individual Weights)

```
1 oz      181     0.35%
2 oz      194     0.37%
3 oz      937     1.79%
...
15 oz      70     0.13%
15.99 oz  288     0.55%
1 lb    1,768     3.39%
2 lb    1,570     3.01%
...
50 lb       6     0.01%
50+ lbs    15     0.03%
```

### Implementation

```python
weight_data = []
# Individual ounces 1-15
for oz in range(1, 16):
    count = len(df[(df['Weight_oz'] > oz-1) & (df['Weight_oz'] <= oz)])
    if count > 0:
        weight_data.append((f"{oz} oz", count, count/total))

# 15.99 oz (15-16 oz boundary)
count_1599 = len(df[(df['Weight_oz'] > 15) & (df['Weight_oz'] <= 16)])
if count_1599 > 0:
    weight_data.append(("15.99 oz", count_1599, count_1599/total))

# Individual pounds 1-50
for lb in range(1, 51):
    lb_oz_low = lb * 16
    lb_oz_high = (lb + 1) * 16
    count = len(df[(df['Weight_oz'] > lb_oz_low) & (df['Weight_oz'] <= lb_oz_high)])
    if count > 0:
        weight_data.append((f"{lb} lb", count, count/total))

# 50+ lbs
count_50plus = len(df[df['Weight_oz'] > 800])
if count_50plus > 0:
    weight_data.append(("50+ lbs", count_50plus, count_50plus/total))
```

## FirstMile Branding

| Element | Style | Hex Code |
|---------|-------|----------|
| Title Row | Navy background, white bold text | #192F66 |
| Section Headers | Light green background, black bold | #B0D67B |
| Alternating Rows | Beige / white | #FAF9F5 |
| Green accent | FirstMile green | #4DA519 |
| Borders | Thin gray | #DDDDDD |

### Formatting Standards

| Element | Format | Example |
|---------|--------|---------|
| Percentages | Two decimals with % | `79.22%` not `0.792247` |
| Numbers | Comma thousands | `41,368` not `41368` |
| Labels | Left-aligned | - |
| Values | Right-aligned | - |
| Data cells | Center-aligned (tables) | - |

### Formatting Functions

```python
def format_pct(val):
    """Format decimal as percentage: 0.792 -> '79.22%'"""
    if isinstance(val, (int, float)):
        return f"{val * 100:.2f}%"
    return val

def format_num(val):
    """Format number with commas: 41368 -> '41,368'"""
    if isinstance(val, (int, float)):
        return f"{int(val):,}"
    return val
```

## Key Features

### Address Normalization
Combines address variations like a pivot table:
- "300 Seabrook Parkway" + "300 SEABROOK PKWY" → Same warehouse
- Uppercase, standardize abbreviations (ST, AVE, BLVD)
- Reduces unique addresses by ~10-15%

**If no Ship Address column**: Use `Client Name` as origin proxy (common in 3PL data)

### DIM Exposure Analysis
- Standard DIM divisor: 139 (166 for USPS)
- Calculates: `dim_weight = (L x W x H) / 139 * 16`
- Identifies right-size opportunities

### Carrier Inference
From tracking number patterns:
- 9400, 9205, 9208, 9261 → USPS
- 12-15 digit numeric → FedEx
- Starts with "1Z" → UPS

## openpyxl Technical Notes

### MergedCell Handling

**CRITICAL**: Always check for MergedCell before accessing cell properties:

```python
from openpyxl.cell.cell import MergedCell

for row in ws.iter_rows():
    for cell in row:
        if isinstance(cell, MergedCell):
            continue  # Skip - MergedCells don't have normal properties
        cell.alignment = center_align
        cell.border = thin_border
```

### Period Objects Cannot Be Written to Excel

When using pandas `to_period()`, the resulting Period objects will cause errors when writing to Excel. Drop temporary columns before writing raw data:

```python
# Drop temp columns before Raw Data Sample sheet
temp_cols = ['_Month', 'Weight_oz', 'Weight_lb', 'DIM_Weight']
sample = df.drop(columns=[c for c in temp_cols if c in df.columns], errors='ignore')
```

### File Locking

If output file is open in Excel, you'll get `PermissionError`. Either:
1. Close the file in Excel
2. Change output filename (e.g., v6 → v7)

## Usage Examples

### Example 1: Full Analysis (F.R.O.G. Pattern)
```
File: PLD 9.12 - 10.12.xlsx (+ 2 more PLD files)
Company: F.R.O.G. Fulfillment

Column Mapping:
- Date: "Label Processed On" (NOT "Ship Date" - it's empty)
- Origin Proxy: "Client Name" (they're a 3PL)
- Service Level: "Service Code Description"
- Carrier: "Carrier"
- Weight (lbs): "Weight"
- Destination State: "Ship To State"
- Dimensions: "Box Length", "Box Width", "Box Height"

Output: 11-sheet workbook with 3-column Executive Summary
```

### Example 2: Basic Analysis (Limited Data)
```
File: Client_Export.xlsx
Company: Beta Brands

Column Mapping:
- Order Date: Column B
- Ship Address: Column G
- Service Level: Column K
- Weight (oz): Column R
- DIMS: L(S), W(T), H(U)

No cost or delivery data. Run core + DIM exposure.
```

## Workflow

1. **Upload file** and provide company name
2. **List all columns** - check for "Label Processed On" date column
3. **Map columns** to standard fields
4. **Identify optional columns** for advanced modules
5. **Generate analysis** - produces branded Excel workbook
6. **Verify formatting** - percentages, commas, alignment
7. **Review insights** - text summary of findings

## Reference Implementation

See `scripts/frog_combined_analysis.py` for complete working example with:
- 3-column Executive Summary layout
- Individual weight distribution (1 oz → 50+ lbs)
- FirstMile color scheme
- All formatting standards
- MergedCell handling
- Date column detection

## Reference Files

- `references/full-prompt.md` - Complete v4.0 prompt text
- `references/column-mapping.md` - Detailed field mapping guide
- `references/output-tables.md` - All table structures

---

*Source: Brock Hansen, VP of Sales - "Prompt for Quick Data Analysis" (Dec 17, 2025)*
*Updated: January 7, 2026 - F.R.O.G. Fulfillment analysis learnings*
