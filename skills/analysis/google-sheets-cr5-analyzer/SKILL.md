---
name: google-sheets-cr5-analyzer
description: Calculates CR5 concentration indices for World Bank geographical regions from Google Sheets GDP data. Reads country and region data, maps countries to regions, identifies top 5 GDP countries per region, computes CR5 ratio, and creates a new spreadsheet with sorted results.
---
# Skill: Google Sheets CR5 Analyzer

## Purpose
Calculate the CR5 (Concentration Ratio of top 5) economic index for the seven major World Bank geographical regions using GDP data from Google Sheets. The skill reads source data, performs calculations, and outputs results to a new spreadsheet.

## Trigger Phrases
- "Calculate CR5 index"
- "Concentration ratio analysis"
- "Top 5 countries by GDP per region"
- "World Bank regional GDP concentration"
- "CR5 analysis from Google Sheets"
- "Regional economic concentration metrics"

## Required Input Data Structure
The skill expects a Google Sheets spreadsheet containing:
1. **Country sheet**: Must include columns for Country Code, Country Name, and GDP (in millions of US dollars)
2. **Region sheet**: Must include columns for Region Code, Region Name, and Regional GDP total

## Core Workflow

### 1. Data Acquisition
- Locate the source spreadsheet by title or ID
- Read both Country and Region sheet data
- Extract country names, GDP values, and regional totals

### 2. Country-Region Mapping
- Use the World Bank's official geographical classification for 7 regions:
  - East Asia & Pacific (EAS)
  - Europe & Central Asia (ECS)
  - Latin America & Caribbean (LCN)
  - Middle East & North Africa (MEA)
  - North America (NAC)
  - South Asia (SAS)
  - Sub-Saharan Africa (SSF)

**Important**: The mapping must use exact country names as they appear in the source data. See `references/world_bank_regions.md` for the complete mapping.

### 3. CR5 Calculation
For each of the 7 regions:
- Filter countries belonging to the region
- Sort countries by GDP (descending)
- Select top 5 countries (or all if region has fewer than 5)
- Calculate: `CR5_Ratio = (Sum of top 5 GDP / Regional GDP total) × 100`
- Round CR5 ratio to 2 decimal places

### 4. Output Generation
- Create new spreadsheet titled "GDP CR5 Analysis"
- Create sheet titled "gdp_cr5_analysis"
- Populate with headers: `Region`, `Top5_Countries`, `Top5_GDP_Sum`, `Region_GDP_Total`, `CR5_Ratio`
- Sort results by CR5_Ratio (descending)
- Format CR5_Ratio as percentage with 2 decimal places

## Error Handling
- If a country name doesn't match the World Bank mapping, log it but continue processing
- If a region has no countries in the data, skip it from results
- If GDP values are missing or zero, handle gracefully in calculations

## Quality Checks
- Verify all 7 World Bank regions are represented
- Ensure CR5 ratios are between 0-100% (or >100% only if data errors)
- Cross-check regional GDP totals match sum of constituent countries (within reasonable tolerance)

## Notes
- North America typically has only 3 countries (US, Canada, Bermuda), so CR5 will include all available countries
- The skill focuses on geographical regions, not income-based classifications (LIC, LMC, UMC, HIC)
