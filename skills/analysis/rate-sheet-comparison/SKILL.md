---
name: rate-sheet-comparison
description: FirstMile Xparcel rate sheet year-over-year comparison tool. Use when user provides two rate sheet Excel files (prior year and current year) and wants to compare Xparcel Expedited and Ground rates. Triggers on phrases like "compare rate sheets", "rate comparison", "2025 vs 2026 rates", "analyze pricing changes", "rate sheet analysis", or when two FirstMile Xparcel rate sheet files are mentioned. Generates Excel output with side-by-side rates, $ difference, % difference, weight band summaries, and conditional formatting.
---

# Rate Sheet Comparison Tool

## Purpose

Compares two FirstMile Xparcel rate sheets (prior year vs current year) and generates a professional Excel report with:
- Weight band summary (avg % change by band)
- Side-by-side rate comparison (National & Select)
- $ Difference and % Difference columns
- Conditional formatting: Green (<0%), Yellow (0-6.99%), Orange (7-10.99%), Red (11%+)

## Execution

### Step 1: Identify Files

User will provide two rate sheet Excel files. Determine which is prior/current by:
- Filename date indicators (e.g., "2025" vs "2026")
- File modification dates
- Ask user if unclear

### Step 2: Run Comparison

```bash
python ".claude/skills/rate-sheet-comparison/scripts/compare_rates.py" "<PRIOR_YEAR_FILE>" "<CURRENT_YEAR_FILE>" "<OUTPUT_PATH>"
```

**Example:**
```bash
python ".claude/skills/rate-sheet-comparison/scripts/compare_rates.py" "C:\Users\BrettWalker\Downloads\BoxiiShip_2025_Rates.xlsx" "C:\Users\BrettWalker\Downloads\BoxiiShip_2026_Rates.xlsx" "C:\Users\BrettWalker\FirstMile_Deals\Rate_Comparison_Output.xlsx"
```

### Step 3: Present Results

Open the output file and summarize key findings:
- Which weight bands saw largest increases?
- National vs Select differences
- Any bands with decreases (green)?

## Input Requirements

Rate sheet Excel files must contain these tabs:
- `Xparcel Expedited SLT_NATL`
- `Xparcel Ground SLT_NATL`

Standard FirstMile rate sheet format with:
- Customer name in cell B4
- Weight labels in column B starting row 9
- Select rates in columns C:J (rows 9-49)
- National rates in columns M:T (rows 9-49)

## Output Format

Excel workbook with two sheets:
1. **Ground** - Xparcel Ground comparison
2. **Expedited** - Xparcel Expedited comparison

Each sheet contains:
- Title with customer name and year comparison
- Weight band summary table with color coding
- Legend for color meanings
- Full rate comparison (40 columns): Prior Year | Current Year | $ Diff | % Diff

## Weight Bands

| Band | Weights |
|------|---------|
| 1-5 oz | 1, 2, 3, 4, 5 oz |
| 6-10 oz | 6, 7, 8, 9, 10 oz |
| 11-15.99 oz | 11, 12, 13, 14, 15, 15.99 oz |
| 1 lb | 1 lb |
| 2 lb | 2 lb |
| 3 lb | 3 lb |
| 4 lb | 4 lb |

## Color Legend

| Color | Range | Meaning |
|-------|-------|---------|
| Green | < 0% | Rate decrease (better) |
| Yellow | 0% - 6.99% | Modest increase |
| Orange | 7% - 10.99% | Significant increase |
| Red | 11%+ | Major increase |
