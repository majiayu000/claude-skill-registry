---
name: advanced-excel
description: "Perform advanced data analysis using Excel with Power Query, Power Pivot, DAX, pivot tables, macros, and VBA. Use for data transformation, building interactive dashboards, automating repetitive tasks, financial modeling, and creating dynamic reports with complex calculations."
---

# Advanced Excel

Master advanced Excel techniques for data analysis, automation, and dashboard creation.

## Overview

Advanced Excel goes beyond basic formulas and charts to leverage powerful tools like Power Query for data transformation, Power Pivot for data modeling, DAX for advanced calculations, and VBA for automation. This skill enables building sophisticated dashboards, automating workflows, and performing complex analyses entirely within Excel.

## Core Tools

| Tool | Purpose | Key Capabilities |
|------|---------|------------------|
| Power Query | ETL (Extract, Transform, Load) | Data import, cleaning, transformation |
| Power Pivot | Data modeling | Large datasets, relationships, DAX measures |
| Pivot Tables | Data summarization | Aggregation, grouping, analysis |
| VBA Macros | Automation | Repetitive tasks, custom functions |
| Advanced Formulas | Calculations | Array formulas, dynamic ranges |

## Power Query

### Data Import

**Supported Sources**:
- Files: CSV, Excel, XML, JSON, PDF
- Databases: SQL Server, MySQL, Oracle
- Web: HTML tables, APIs
- Cloud: SharePoint, OneDrive, Azure

**Import Process**:
1. Data → Get Data → From File/Database/Web
2. Select source and file
3. Transform data in Power Query Editor
4. Load to worksheet or Data Model

### Data Transformation

**Common Operations**:

```
// Remove duplicates
= Table.Distinct(Source)

// Filter rows
= Table.SelectRows(Source, each [Sales] > 1000)

// Add custom column
= Table.AddColumn(Source, "Revenue", each [Price] * [Quantity])

// Replace values
= Table.ReplaceValue(Source, "N/A", null, Replacer.ReplaceValue, {"Status"})

// Group by
= Table.Group(Source, {"Region"}, {{"Total Sales", each List.Sum([Sales]), type number}})

// Merge queries (join)
= Table.NestedJoin(Sales, {"ProductID"}, Products, {"ID"}, "Products", JoinKind.Inner)

// Append queries (union)
= Table.Combine({Query1, Query2})

// Pivot column
= Table.Pivot(Source, List.Distinct(Source[Category]), "Category", "Sales")

// Unpivot columns
= Table.UnpivotOtherColumns(Source, {"ID", "Name"}, "Attribute", "Value")
```

### M Language Basics

```
let
    // Step 1: Import data
    Source = Excel.CurrentWorkbook(){[Name="SalesData"]}[Content],
    
    // Step 2: Change types
    ChangedType = Table.TransformColumnTypes(Source, {{"Date", type date}, {"Sales", type number}}),
    
    // Step 3: Filter rows
    FilteredRows = Table.SelectRows(ChangedType, each [Date] >= #date(2024, 1, 1)),
    
    // Step 4: Add custom column
    AddedRevenue = Table.AddColumn(FilteredRows, "Revenue", each [Sales] * [Price]),
    
    // Step 5: Group and aggregate
    Grouped = Table.Group(AddedRevenue, {"Region"}, {
        {"Total Revenue", each List.Sum([Revenue]), type number},
        {"Avg Sales", each List.Average([Sales]), type number}
    })
in
    Grouped
```

### Best Practices

1. **Name steps clearly** — Descriptive names aid understanding
2. **Document transformations** — Add comments for complex logic
3. **Use parameters** — Make queries reusable
4. **Refresh regularly** — Set up automatic refresh schedule
5. **Optimize performance** — Filter early, fold queries when possible

## Power Pivot

### Data Model

**Creating Relationships**:
1. Add tables to Data Model
2. Diagram View → Drag to create relationships
3. Define cardinality (one-to-many, many-to-many)
4. Set active/inactive relationships

**Best Practices**:
- Star schema: Fact table + dimension tables
- One-to-many relationships preferred
- Avoid circular relationships
- Use surrogate keys when needed

### DAX (Data Analysis Expressions)

**Calculated Columns**:
```dax
// Add column to table
Revenue = Sales[Quantity] * Sales[Price]

// Conditional column
Category = 
IF(Sales[Amount] > 10000, "High",
   IF(Sales[Amount] > 5000, "Medium", "Low"))

// Related table lookup
Product Name = RELATED(Products[Name])
```

**Measures** (preferred over calculated columns):
```dax
// Total Sales
Total Sales = SUM(Sales[Amount])

// Year-to-Date
YTD Sales = TOTALYTD([Total Sales], Calendar[Date])

// Previous Year
PY Sales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date]))

// Year-over-Year Growth
YoY Growth = 
DIVIDE(
    [Total Sales] - [PY Sales],
    [PY Sales],
    0
)

// Moving Average
MA 3 Months = 
CALCULATE(
    [Total Sales],
    DATESINPERIOD(Calendar[Date], LASTDATE(Calendar[Date]), -3, MONTH)
) / 3

// Rank
Sales Rank = RANKX(ALL(Products[Name]), [Total Sales], , DESC)

// Top N
Top 10 Sales = 
CALCULATE(
    [Total Sales],
    TOPN(10, ALL(Products[Name]), [Total Sales], DESC)
)

// Percentage of Total
% of Total = 
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALL(Products))
)
```

**Time Intelligence**:
```dax
// Requires date table with continuous dates

// Year-to-Date
YTD = TOTALYTD([Total Sales], Calendar[Date])

// Quarter-to-Date
QTD = TOTALQTD([Total Sales], Calendar[Date])

// Month-to-Date
MTD = TOTALMTD([Total Sales], Calendar[Date])

// Previous Month
PM = CALCULATE([Total Sales], PREVIOUSMONTH(Calendar[Date]))

// Same Period Last Year
SPLY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date]))

// Rolling 12 Months
R12M = 
CALCULATE(
    [Total Sales],
    DATESINPERIOD(Calendar[Date], LASTDATE(Calendar[Date]), -12, MONTH)
)
```

**Filter Context**:
```dax
// ALL - Remove filters
All Sales = CALCULATE([Total Sales], ALL(Sales))

// FILTER - Add filter
High Value Sales = CALCULATE([Total Sales], FILTER(Sales, Sales[Amount] > 1000))

// KEEPFILTERS - Respect existing filters
Filtered Sales = CALCULATE([Total Sales], KEEPFILTERS(Products[Category] = "Electronics"))

// VALUES - Get distinct values
Product Count = COUNTROWS(VALUES(Products[Name]))
```

## Pivot Tables

### Creating Effective Pivot Tables

**Structure**:
- Rows: Categories to group by
- Columns: Additional grouping dimension
- Values: Metrics to aggregate
- Filters: Limit data scope

**Aggregation Functions**:
- Sum, Average, Count
- Min, Max
- StdDev, Var
- Distinct Count (requires Data Model)

### Advanced Techniques

**Calculated Fields**:
```
// In Pivot Table
Insert → Calculated Field
Name: Profit Margin
Formula: =Profit/Revenue
```

**Calculated Items**:
```
// Within a field
Insert → Calculated Item
Name: Q1
Formula: =Jan+Feb+Mar
```

**Grouping**:
- Dates: Group by month, quarter, year
- Numbers: Create bins
- Text: Manual grouping

**Show Values As**:
- % of Grand Total
- % of Column Total
- % of Row Total
- Running Total
- Rank
- % Difference From
- Index

### Slicers and Timelines

**Slicers**:
1. Insert → Slicer
2. Select field
3. Format and position
4. Connect to multiple pivot tables

**Timelines**:
1. Insert → Timeline
2. Select date field
3. Choose period (days, months, quarters, years)
4. Filter date range

## VBA Macros

### Recording Macros

1. Developer → Record Macro
2. Perform actions
3. Stop Recording
4. View code: Alt + F11

### Basic VBA Structure

```vba
Sub MacroName()
    ' Variable declarations
    Dim ws As Worksheet
    Dim lastRow As Long
    
    ' Set worksheet
    Set ws = ThisWorkbook.Sheets("Sheet1")
    
    ' Find last row
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    
    ' Loop through rows
    Dim i As Long
    For i = 2 To lastRow
        ' Perform action
        ws.Cells(i, 3).Value = ws.Cells(i, 1).Value * ws.Cells(i, 2).Value
    Next i
    
    ' Message box
    MsgBox "Macro completed!", vbInformation
End Sub
```

### Common VBA Tasks

**Data Manipulation**:
```vba
' Copy data
Range("A1:C10").Copy Destination:=Range("E1")

' Filter data
ws.Range("A1").AutoFilter Field:=2, Criteria1:=">100"

' Sort data
ws.Range("A1:C100").Sort Key1:=Range("B1"), Order1:=xlAscending

' Delete rows
ws.Rows("5:10").Delete

' Insert rows
ws.Rows("5:5").Insert
```

**Workbook Operations**:
```vba
' Open workbook
Workbooks.Open "C:\Path\To\File.xlsx"

' Save workbook
ThisWorkbook.Save

' Close workbook
Workbooks("File.xlsx").Close SaveChanges:=True

' Create new workbook
Workbooks.Add
```

**User Interaction**:
```vba
' Input box
Dim userInput As String
userInput = InputBox("Enter value:")

' Message box
MsgBox "Operation complete!", vbInformation, "Success"

' Yes/No dialog
Dim response As VbMsgBoxResult
response = MsgBox("Continue?", vbYesNo + vbQuestion)
If response = vbYes Then
    ' Proceed
End If
```

**Error Handling**:
```vba
Sub ErrorHandlingExample()
    On Error GoTo ErrorHandler
    
    ' Code that might cause error
    Dim result As Double
    result = 10 / 0
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Error: " & Err.Description, vbCritical
End Sub
```

### Automation Examples

**Refresh All Data**:
```vba
Sub RefreshAllData()
    ' Refresh Power Query queries
    ThisWorkbook.Queries.Refresh
    
    ' Refresh Pivot Tables
    Dim pt As PivotTable
    Dim ws As Worksheet
    
    For Each ws In ThisWorkbook.Worksheets
        For Each pt In ws.PivotTables
            pt.RefreshTable
        Next pt
    Next ws
    
    MsgBox "All data refreshed!", vbInformation
End Sub
```

**Export to PDF**:
```vba
Sub ExportToPDF()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Dashboard")
    
    Dim fileName As String
    fileName = ThisWorkbook.Path & "\Dashboard_" & Format(Date, "yyyy-mm-dd") & ".pdf"
    
    ws.ExportAsFixedFormat Type:=xlTypePDF, fileName:=fileName
    
    MsgBox "Exported to: " & fileName, vbInformation
End Sub
```

## Advanced Formulas

### Array Formulas

**Dynamic Arrays (Excel 365)**:
```excel
// FILTER
=FILTER(A2:C100, B2:B100>1000)

// SORT
=SORT(A2:C100, 2, -1)  // Sort by column 2, descending

// UNIQUE
=UNIQUE(A2:A100)

// SEQUENCE
=SEQUENCE(10, 1, 1, 1)  // 1 to 10

// XLOOKUP
=XLOOKUP(E2, A2:A100, C2:C100, "Not Found")

// XMATCH
=XMATCH(E2, A2:A100, 0)  // Exact match
```

**Legacy Array Formulas** (Ctrl+Shift+Enter):
```excel
// Sum if multiple criteria
{=SUM((A2:A100="North")*(B2:B100>1000)*C2:C100)}

// Count unique values
{=SUM(1/COUNTIF(A2:A100, A2:A100))}

// Max if
{=MAX(IF(A2:A100="North", B2:B100))}
```

### Dynamic Named Ranges

```excel
// Expand automatically
=OFFSET(Sheet1!$A$1, 0, 0, COUNTA(Sheet1!$A:$A), 1)

// Table reference
=Table1[Sales]


## Using the Reference Files

### When to Read Each Reference

**`/references/power-query-advanced.md`** — Read when building complex ETL workflows, optimizing query performance, or working with APIs.

**`/references/dax-comprehensive.md`** — Read when creating advanced measures, implementing time intelligence, or optimizing DAX performance.

**`/references/vba-automation.md`** — Read when automating repetitive tasks, building custom functions, or creating user forms.

**`/references/dashboard-examples.md`** — Read when designing dashboards, implementing interactivity, or looking for layout inspiration.
