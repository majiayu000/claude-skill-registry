---
name: Shipping Carrier Analysis (Enhanced)
version: 2.0
description: Analyzes shipping data with intelligent preprocessing to handle raw, unstructured data from various sources. Automatically detects, maps, and cleans data before creating comprehensive carrier dashboards with volume breakdown, cost analysis, pivot tables, and cost-saving opportunities.
---

# Shipping Carrier Analysis Skill v2.0 (Enhanced)

## New Features in v2.0

- ✅ Flexible column detection and mapping
- ✅ Data validation and quality checks
- ✅ Automatic data cleaning and normalization
- ✅ Support for multiple data export formats
- ✅ User prompts for missing/ambiguous data

---

## Execution Steps

### Step 0: Data Validation and Preparation (NEW)

#### 0.1 Column Detection & Mapping

Intelligently identify columns using fuzzy matching:

**Carrier Column** - Look for:
- Exact: `Carrier`, `carrier`
- Variations: `Shipper`, `Shipping Carrier`, `Carrier Name`, `Service Provider`, `Ship Via`

**Shipping Method Column** - Look for:
- Exact: `Shipping Method`, `Method`
- Variations: `Service`, `Service Level`, `Ship Method`, `Delivery Method`, `Ship Type`

**Cost Column** - Look for:
- Exact: `Label Cost`, `Total Cost`, `Cost`
- Variations: `Shipping Cost`, `Ship Cost`, `Price`, `Amount`, `Charge`, `Rate`

**Quantity Column** - Look for:
- Exact: `Quantity shipped`, `Units Shipped`, `Quantity`
- Variations: `Qty`, `Units`, `Pieces`, `Items`, `Count`

**Weight Column** - Look for:
- Exact: `Weight (lb)`, `Total Weight`, `Weight`
- Variations: `Wt`, `Weight in lbs`, `Package Weight`, `Shipment Weight`

#### 0.2 Data Validation Checks

**Required Column Validation:**
```
IF any required column is missing:
  - List detected columns
  - Prompt user: "I couldn't find a [Carrier/Method/Cost/etc.] column.
    Please tell me which column contains this data, or confirm if it's missing."
  - Wait for user input before proceeding
```

**Data Quality Checks:**
1. **Empty Cells**: Count rows with missing required data
2. **Data Types**: Verify numeric columns contain numbers (Cost, Quantity, Weight)
3. **Date Format**: Check if dates are properly formatted
4. **Consistency**: Look for unusual values (negative costs, zero quantities)

#### 0.3 Data Cleaning & Normalization

If data quality issues found, create a **"Data_Cleaned"** sheet:

**Carrier Name Standardization:**
```
ups, UPS, U.P.S → "UPS"
fedex, FedEx, Federal Express → "FedEx"
usps, USPS, U.S.P.S → "USPS"
shippo__usps → "USPS (Shippo)"
amazon_shipping, Amazon, AMZ → "Amazon Shipping"
dhl, DHL Express → "DHL"
```

**Handle Empty/Invalid Values:**
- Empty Carrier → "(Unknown Carrier)"
- Empty Method → "(Unspecified)"
- Non-numeric Cost → 0 or flag for review
- Missing Weight → Calculate average or use 0

**Text Cleaning:**
- Trim extra spaces
- Remove special characters from carrier names
- Standardize capitalization
- Handle merged cells

#### 0.4 Create Normalized Data Sheet

**If original data needs cleaning:**

1. Create new sheet: **"Data_Normalized"**
2. Copy all data
3. Add standardized columns:
   - `Carrier_Clean` - Normalized carrier names
   - `Method_Clean` - Cleaned method descriptions
   - `Cost_Numeric` - Validated numeric costs
   - `Qty_Numeric` - Validated quantities
   - `Weight_Numeric` - Validated weights
4. Flag problematic rows in a `Data_Issues` column
5. Add summary at top noting:
   - Number of rows processed
   - Issues found and fixed
   - Rows with warnings

**Column Mapping Reference:**
Create a small reference table showing:
```
Original Column → Mapped To → Data Type
"carrier"       → Carrier   → Text
"ship_cost"     → Cost      → Currency
```

---

### Step 1: Identify Data (Updated)

- Detect source sheet (original or Data_Normalized)
- Use mapped column positions from Step 0
- Confirm data range includes all valid rows
- Log any skipped rows (if quality issues detected)

---

### Step 2: Create Carrier-Analysis Sheet

Create a new sheet with:

**Header:** "SHIPPING CARRIER ANALYSIS" with total shipment count

**Carrier Summary Table** (columns):
- Carrier
- Shipments
- % of Total
- Total Cost
- Avg Cost/Shipment
- Units Shipped
- Total Weight

Use formulas referencing source data. Include TOTAL row with SUM formulas.

**Shipping Method Breakdown** (columns):
- Carrier
- Shipping Method
- Shipments
- % of Total
- Total Cost
- Avg Cost

Top 20 methods by volume.

**Key Metrics Section:**
- Total shipments
- Total cost
- Avg cost
- Most/least cost-effective carriers

**Charts:**
- Pie chart for carrier volume
- Bar chart for costs

---

### Step 3: Create Carrier-Pivot Sheet

Add pivot table with:

**Row fields:** Carrier, Shipping Method (hierarchical)

**Value fields:**
- Count of shipments
- Sum of Label Cost
- Average of Label Cost
- Sum of Quantity shipped
- Sum of Weight

---

### Step 4: Create Dashboard (First Sheet)

Build executive dashboard with:

**KPI Cards:**
- Total Shipments
- Total Cost
- Avg Cost/Shipment
- Total Units

**Top 5 Carriers table** with COUNTIF formulas

**Top 5 Methods table** with COUNTIF/SUMIF formulas

**Cost-Saving Opportunities:**
- Opportunity 1: Carrier optimization (shift expensive to cheaper ground carriers)
- Opportunity 2: Reduce premium services (2nd Day Air → Ground)
- Calculate potential savings with formulas

**Charts:**
- Carrier mix pie chart
- Cost comparison bar chart

**Data Quality Summary** (if Step 0 processing occurred):
```
Source: [Original Sheet Name]
Rows Processed: [10,427]
Rows with Issues: [127]
Data Cleaning: [Applied/Not Needed]
Column Mapping: [Show mappings]
```

---

## Enhanced Expected Data Formats

### Format 1: Well-Structured (Original)
- ✅ Clean headers in Row 1
- ✅ All required columns present with standard names
- ✅ Data properly formatted
- → **Processes directly, no preprocessing needed**

### Format 2: Messy Export (NEW Support)
- ⚠️ Inconsistent column names
- ⚠️ Mixed case carrier names
- ⚠️ Empty cells scattered throughout
- ⚠️ Text in numeric columns
- → **Step 0 cleans and normalizes**

### Format 3: Partial Data (NEW Support)
- ⚠️ Some required columns missing
- ⚠️ User needs to map manually
- → **Interactive prompts guide user**

---

## User Interaction Examples

### Example 1: Missing Column
```
AI: "I found columns: Order_ID, Ship_Via, Service, Cost_USD, Quantity
     I couldn't identify a 'Carrier' column.
     Is 'Ship_Via' the carrier column? Or is it named differently?"

User: "Yes, Ship_Via is the carrier"

AI: "Got it! Mapping Ship_Via → Carrier. Proceeding with analysis..."
```

### Example 2: Data Quality Issues
```
AI: "I detected 127 rows with quality issues:
     - 15 rows with empty carrier names
     - 8 rows with non-numeric costs
     - 104 rows with missing weight data

     I'll create a cleaned version in 'Data_Normalized' sheet
     and flag these issues. Continue?"

User: "Yes"

AI: "Creating normalized data sheet..."
```

### Example 3: Ambiguous Columns
```
AI: "I found two possible cost columns: 'Base_Cost' and 'Total_Cost'
     Which should I use for the analysis?"

User: "Use Total_Cost"

AI: "Using Total_Cost for analysis..."
```

---

## Formatting Standards

- **Font:** Aptos Narrow, 10-12pt for data, 14-20pt for headers
- **Colors:**
  - `#1F4E79` (dark blue headers)
  - `#2E75B6` (section headers)
  - `#548235` (savings/green)
  - `#C65911` (orange highlights)
- **Currency:** Accounting format for costs
- **Percentages:** 0.0% format
- **Numbers:** #,##0 with thousands separator
- Hide gridlines for clean presentation

---

## Key Formulas

```excel
# Count shipments by carrier
=COUNTIF(Sheet1!M:M,"carrier_name")

# Sum costs by method
=SUMIF(Sheet1!N:N,"method",Sheet1!AB:AB)

# Average cost calculation
=SUMIF(...)/COUNTIF(...)

# Standardize carrier names
=IFS(
  LOWER(A2)="ups", "UPS",
  LOWER(A2)="fedex", "FedEx",
  LOWER(A2)="usps", "USPS",
  ISNUMBER(SEARCH("shippo",LOWER(A2))), "USPS (Shippo)",
  TRUE, PROPER(TRIM(A2))
)

# Convert text to numeric with error handling
=IFERROR(VALUE(B2), 0)

# Flag data issues
=IF(OR(ISBLANK(A2), NOT(ISNUMBER(C2)), C2<0),
    "⚠️ Review Needed",
    "✓")
```

---

## Output Structure

```
[workbook].xlsx
├── Dashboard (Sheet 1)
├── Carrier-Analysis
├── Carrier-Pivot
└── Data_Normalized (if cleaning applied)
```

---

*This enhanced version handles raw data exports from ShipStation, Shopify, WMS systems, or any shipping platform—not just perfectly formatted PLD data.*
