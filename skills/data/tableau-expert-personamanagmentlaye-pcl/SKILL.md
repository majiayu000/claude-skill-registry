---
name: tableau-expert
version: 1.0.0
description: Expert-level Tableau Desktop/Server, calculated fields, LOD expressions, dashboards, data blending, and performance optimization
category: data
author: PCL Team
license: Apache-2.0
tags:
  - tableau
  - bi
  - visualization
  - dashboards
  - lod
  - analytics
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
requirements:
  tableau-api-lib: ">=0.1.0"
---

# Tableau Expert

You are an expert in Tableau with deep knowledge of calculated fields, LOD (Level of Detail) expressions, parameters, dashboards, data blending, extracts, and performance optimization. You create interactive, performant dashboards that deliver actionable insights.

## Core Expertise

### Calculated Fields

**Basic Calculations:**
```tableau
// String manipulation
Full Name
UPPER([First Name]) + " " + UPPER([Last Name])

Email Domain
SPLIT([Email], "@", 2)

// Numeric calculations
Profit Margin
[Profit] / [Sales]

Discounted Price
[Price] * (1 - [Discount])

// Date calculations
Days Since Order
DATEDIFF('day', [Order Date], TODAY())

Order Year
YEAR([Order Date])

Order Quarter
"Q" + STR(DATEPART('quarter', [Order Date]))

// Conditional logic
Order Priority
IF [Days Since Order] <= 2 THEN "Urgent"
ELSEIF [Days Since Order] <= 7 THEN "High"
ELSEIF [Days Since Order] <= 14 THEN "Medium"
ELSE "Low"
END

// Case statement
Customer Segment
CASE [Lifetime Value]
    WHEN >= 10000 THEN "VIP"
    WHEN >= 5000 THEN "High Value"
    WHEN >= 1000 THEN "Medium Value"
    ELSE "Low Value"
END

// Aggregations
Total Revenue
SUM([Order Amount])

Average Order Value
AVG([Order Amount])

Distinct Customer Count
COUNTD([Customer ID])
```

**Advanced Calculations:**
```tableau
// Window calculations
Running Total
RUNNING_SUM(SUM([Sales]))

Moving Average (7 days)
WINDOW_AVG(SUM([Sales]), -6, 0)

Percent of Total
SUM([Sales]) / TOTAL(SUM([Sales]))

Rank by Sales
RANK_UNIQUE(SUM([Sales]), 'desc')

Previous Period Sales
LOOKUP(SUM([Sales]), -1)

// Quick table calculations
// Right-click measure -> Quick Table Calculation
// - Running Total
// - Difference
// - Percent Difference
// - Percent of Total
// - Rank
// - Percentile
// - Moving Average

// Year over Year Growth
YoY Growth
(SUM([Sales]) - LOOKUP(SUM([Sales]), -12)) / LOOKUP(SUM([Sales]), -12)

// Compound growth rate
CAGR
POWER(
    SUM([Current Year Sales]) / SUM([First Year Sales]),
    1 / [Years]
) - 1
```

### Level of Detail (LOD) Expressions

**FIXED LOD:**
```tableau
// Customer lifetime value (fixed at customer level)
{ FIXED [Customer ID] : SUM([Order Amount]) }

// First order date per customer
{ FIXED [Customer ID] : MIN([Order Date]) }

// Category-level average (ignore other dimensions)
{ FIXED [Category] : AVG([Sales]) }

// Overall average (ignore all dimensions)
{ FIXED : AVG([Sales]) }

// Cohort analysis
Cohort Month
{ FIXED [Customer ID] : MIN(DATETRUNC('month', [Order Date])) }

// Customer acquisition cost per month
{ FIXED [Acquisition Month] : SUM([Marketing Spend]) / COUNTD([Customer ID]) }
```

**INCLUDE LOD:**
```tableau
// Add dimension to aggregation
{ INCLUDE [Region] : SUM([Sales]) }

// Product sales including subcategory
{ INCLUDE [Sub-Category] : SUM([Sales]) }

// Use case: Show product sales with category total
Product Sales
SUM([Sales])

Category Sales
{ INCLUDE [Category] : SUM([Sales]) }

Percent of Category
[Product Sales] / [Category Sales]
```

**EXCLUDE LOD:**
```tableau
// Remove dimension from aggregation
{ EXCLUDE [Region] : SUM([Sales]) }

// Total sales excluding customer dimension
{ EXCLUDE [Customer ID] : SUM([Sales]) }

// Use case: Compare individual to group
Individual Sales
SUM([Sales])

Group Average (excluding individual)
{ EXCLUDE [Salesperson] : AVG([Sales]) }

Performance vs Group
[Individual Sales] - [Group Average]
```

**Complex LOD Use Cases:**
```tableau
// New vs Returning Customers
Is First Order
{ FIXED [Customer ID] : MIN([Order Date]) } = [Order Date]

New Customers
IF [Is First Order] THEN 1 ELSE 0 END

// Customer lifetime metrics
Orders Per Customer
{ FIXED [Customer ID] : COUNTD([Order ID]) }

Days Since First Order
DATEDIFF('day',
    { FIXED [Customer ID] : MIN([Order Date]) },
    [Order Date]
)

// Cohort retention
Months Since First Order
DATEDIFF('month',
    { FIXED [Customer ID] : MIN([Order Date]) },
    [Order Date]
)

Cohort Size
{ FIXED [Cohort Month] : COUNTD([Customer ID]) }

Retention Rate
COUNTD([Customer ID]) / [Cohort Size]

// Top N with LOD
Top 10 Products by Revenue
{ FIXED [Product] : SUM([Revenue]) }

Is Top 10
RANK_UNIQUE([Top 10 Products by Revenue]) <= 10

// Percentile calculation
Revenue Percentile
{ FIXED [Customer ID] : SUM([Revenue]) }

Customer Percentile
IF PERCENTILE([Revenue Percentile], 0.9) THEN "Top 10%"
ELSEIF PERCENTILE([Revenue Percentile], 0.75) THEN "Top 25%"
ELSE "Other"
END
```

### Parameters and Dynamic Calculations

**Parameter Creation:**
```tableau
// Metric selector parameter
Metric Selector (String)
Values: Revenue, Profit, Quantity, Orders

// Dynamic measure based on parameter
Selected Metric
CASE [Metric Selector]
    WHEN "Revenue" THEN SUM([Sales])
    WHEN "Profit" THEN SUM([Profit])
    WHEN "Quantity" THEN SUM([Quantity])
    WHEN "Orders" THEN COUNTD([Order ID])
END

// Date range parameter
Number of Days (Integer)
Current value: 30
Range: 7 to 365

// Filter with parameter
Order Date Filter
[Order Date] >= DATEADD('day', -[Number of Days], TODAY())

// Top N parameter
Top N (Integer)
Current value: 10
Range: 5 to 50

// Top N filter
Top N Products
RANK_UNIQUE(SUM([Sales]), 'desc') <= [Top N]

// Timeframe parameter
Time Dimension (String)
Values: Day, Week, Month, Quarter, Year

// Dynamic timeframe
Dynamic Time
CASE [Time Dimension]
    WHEN "Day" THEN STR([Order Date])
    WHEN "Week" THEN "Week " + STR(DATEPART('week', [Order Date]))
    WHEN "Month" THEN DATENAME('month', [Order Date]) + " " + STR(YEAR([Order Date]))
    WHEN "Quarter" THEN "Q" + STR(DATEPART('quarter', [Order Date])) + " " + STR(YEAR([Order Date]))
    WHEN "Year" THEN STR(YEAR([Order Date]))
END
```

**Advanced Parameter Usage:**
```tableau
// Comparison period parameter
Compare To (String)
Values: Previous Period, Previous Year, Custom

// Comparison calculation
Previous Period Sales
CASE [Compare To]
    WHEN "Previous Period" THEN
        LOOKUP(SUM([Sales]), -1)
    WHEN "Previous Year" THEN
        LOOKUP(SUM([Sales]), -12)
    WHEN "Custom" THEN
        // Use another parameter for custom offset
        LOOKUP(SUM([Sales]), -[Custom Offset])
END

Percent Change
(SUM([Sales]) - [Previous Period Sales]) / [Previous Period Sales]

// Threshold parameter
Sales Threshold (Float)
Current value: 1000
Range: 0 to 10000

// Color coding with parameter
Sales Performance
IF SUM([Sales]) >= [Sales Threshold] THEN "Above Target"
ELSE "Below Target"
END

// Multiple metric comparison
Metric 1 (String)
Metric 2 (String)

Metric 1 Value
CASE [Metric 1]
    WHEN "Revenue" THEN SUM([Sales])
    WHEN "Profit" THEN SUM([Profit])
    WHEN "Orders" THEN COUNTD([Order ID])
END

Metric 2 Value
CASE [Metric 2]
    WHEN "Revenue" THEN SUM([Sales])
    WHEN "Profit" THEN SUM([Profit])
    WHEN "Orders" THEN COUNTD([Order ID])
END
```

### Data Blending and Relationships

**Data Relationships (Tableau 2020.2+):**
```tableau
// Physical layer: Tables joined
Sales (LEFT JOIN) Returns ON Sales.Order ID = Returns.Order ID

// Logical layer: Relationships
Orders -> Order Items (Order ID)
Orders -> Customers (Customer ID)
Products -> Order Items (Product ID)

// Multi-fact analysis with relationships
// Automatically handles different grain levels
Revenue from Orders
SUM([Orders].[Amount])

Return Rate from Returns
COUNTD([Returns].[Return ID]) / COUNTD([Orders].[Order ID])
```

**Data Blending:**
```tableau
// Primary data source: Sales
// Secondary data source: Targets

// Linked fields (blend on):
- Date (linked)
- Region (linked)

// Blended calculation
Sales vs Target
SUM([Sales].[Revenue]) - SUM([Targets].[Target Amount])

Target Achievement
SUM([Sales].[Revenue]) / SUM([Targets].[Target Amount])

// Handling missing data in blend
Revenue with Default
IFNULL(SUM([Sales].[Revenue]), 0)
```

**Cross-Database Joins:**
```tableau
// Join across different databases
PostgreSQL: Orders
MySQL: Customer Attributes
Snowflake: Product Catalog

// Join conditions
Orders.customer_id = Customer Attributes.id
Orders.product_id = Product Catalog.product_id
```

### Dashboard Design

**Dashboard Best Practices:**
```tableau
// Layout containers
Horizontal container
    - Title (text)
    - Filters (vertical container)
Vertical container
    - KPI cards (horizontal container)
    - Main visualization
    - Detail table

// Actions
Filter action:
    Source: Map
    Target: Detail table
    Run on: Select
    Clear selection: Show all values

Highlight action:
    Source: Bar chart
    Target: Line chart
    Run on: Hover
    Clear selection: Leave highlighted

URL action:
    Name: View Customer Details
    URL: https://crm.company.com/customer?id=<Customer ID>
    Run on: Menu

Set action:
    Source: Product list
    Target: Set field
    Run on: Select
    Use: Compare products

// Dashboard sizing
Fixed size: 1200 x 800 (desktop)
Automatic: Responsive
Range: 800-1200 (tablet)

// Device designer
Desktop layout (default)
Tablet layout (hide some filters, stack vertically)
Phone layout (single column, essential metrics only)
```

**Performance Dashboard:**
```tableau
// KPI cards
Total Revenue
SUM([Sales])
Format: Currency, $#,##0K

YoY Growth
([Current Year Revenue] - [Last Year Revenue]) / [Last Year Revenue]
Format: Percentage, 0.0%

// Trend with reference line
Line chart: Sales by Month
Reference line: Average
Trend line: Linear

// Top performers
Bar chart: Top 10 Products by Revenue
Filter: [Top N Products] = True
Sort: Descending by Revenue
Color: Profit Ratio (diverging)

// Comparison
Butterfly chart: Sales vs Budget by Category
Bars: Positive = Sales, Negative = Budget
Sort: By variance

// Geographic
Map: Sales by State
Color: Sales (gradient)
Size: Profit
Tooltip: State, Sales, Profit, Orders

// Drill-down hierarchy
Category -> Sub-Category -> Product
Action: Drill down on click
```

### Table Calculations

**Partitioning and Addressing:**
```tableau
// Compute using options:
// - Table (across)
// - Table (down)
// - Pane (across)
// - Pane (down)
// - Cell
// - Specific dimensions

// Running total partitioned by category
Compute using: Category (restart for each category)

// Percent of total within partition
Compute using: Pane (down)

// Rank by region
RANK_UNIQUE(SUM([Sales]))
Compute using: Region

// Window calculation with specific dimensions
Window average
Compute using: Month, Product
Addressing: Month
Partitioning: Product
```

**Advanced Table Calculations:**
```tableau
// First/Last in partition
Is First Order
FIRST() = 0

Is Last Order
LAST() = 0

// Index for row numbering
Row Number
INDEX()

// Size of partition
Total Rows
SIZE()

// Cumulative percent
Running Percent
RUNNING_SUM(SUM([Sales])) / TOTAL(SUM([Sales]))

// Period over period percent change
// Compute using: Month
Period Change
(ZN(SUM([Sales])) - LOOKUP(ZN(SUM([Sales])), -1)) /
ABS(LOOKUP(ZN(SUM([Sales])), -1))

// Month over month growth rate
// Partitioned by category
MoM Growth
Compute using: Table (across)
Addressing: Month
Partitioning: Category
```

### Extracts and Performance

**Extract Optimization:**
```tableau
// Extract filters
// Filter 1: Date >= 2020-01-01
// Filter 2: Country IN ['US', 'UK', 'CA']
// Filter 3: Is_Deleted = False

// Aggregation
Aggregate visible dimensions
Roll up dates to: Month

// Extract refresh
Full refresh: Replace all data
Incremental refresh: Add rows where Date > MAX(Date)

// Hyper extract
File format: .hyper (Tableau 10.5+)
Compression: High
```

**Performance Optimization:**
```tableau
// Data source filters (apply early)
Data Source Filter:
    [Order Date] >= DATE('2020-01-01')
    AND [Is_Deleted] = FALSE

// Context filters (create temp table)
Context: [Region] IN ['North', 'South']

// Filter order of operations:
1. Extract filters
2. Data source filters
3. Context filters
4. Dimension filters
5. Measure filters
6. Table calc filters

// Optimize calculations
// Bad: Nested LODs
{ FIXED [Customer] : MAX({ FIXED [Order] : SUM([Sales]) }) }

// Good: Single LOD with nested aggregation
{ FIXED [Customer] : SUM([Sales]) }

// Use boolean instead of string
// Bad:
Status = "Active"

// Good:
Is Active (boolean field)

// Reduce mark count
// Use aggregated data
// Filter to relevant data only
// Use extracts for large datasets

// Optimize dashboard
// Limit number of worksheets
// Use dashboard actions instead of filters
// Hide unused fields
// Reduce number of marks (<1000 ideal)
```

### Advanced Techniques

**Sets:**
```tableau
// Static set
Top 10 Customers
Condition: By field, Top 10 by SUM([Sales])

// Dynamic set
High Value Orders
Condition: SUM([Order Amount]) > [Threshold Parameter]

// Combined sets
VIP and Recent
[Top Customers] AND [Recent Purchasers]

// Set action
// Allow users to select items to add to set
Action: Add/Remove from Set
Source: Product list
Target Set: Selected Products
Run on: Select

// Using sets in calculations
Is Top Customer
[Customer] IN [Top 10 Customers]

Customer Type
IF [Customer] IN [VIP Set] THEN "VIP"
ELSEIF [Customer] IN [Top 100 Set] THEN "High Value"
ELSE "Standard"
END
```

**Analytics Pane:**
```tableau
// Reference lines
Average line: AVG(SUM([Sales]))
Median line: MEDIAN(SUM([Sales]))
Constant: [Target Parameter]

// Reference bands
Quartiles: 25th to 75th percentile
Custom: [Low Threshold] to [High Threshold]

// Distribution bands
Percentages: 60%, 80%, 95%
Standard deviation: 1, 2, 3 sigma

// Box plot
Whiskers: 1.5 * IQR
Outliers: Points beyond whiskers

// Trend lines
Linear, Logarithmic, Exponential, Polynomial
Show equation
Show R-squared value
Forecast: 12 months forward
Confidence interval: 95%

// Forecast
Automatic: Tableau selects model
Ignore last: N periods (for backtesting)
```

## Best Practices

### 1. Dashboard Design
- Keep dashboards focused (one story per dashboard)
- Use consistent color schemes and formatting
- Place most important information top-left
- Limit to 5-7 charts per dashboard
- Optimize for target screen size
- Use white space effectively

### 2. Performance
- Use extracts for large datasets
- Apply data source filters early
- Minimize use of COUNTD on high-cardinality fields
- Avoid nested LODs when possible
- Reduce number of marks (aggregate when possible)
- Use context filters for large dimension filters

### 3. Calculations
- Use LODs for complex aggregations
- Prefer table calculations for running totals and ranks
- Document complex calculations with comments
- Use parameters for user interactivity
- Test calculations with different filters

### 4. Data Modeling
- Use relationships instead of joins when possible
- Minimize use of data blending
- Clean data at source when possible
- Create calculated fields in data source
- Use appropriate data types

### 5. Governance
- Establish naming conventions
- Document data sources and calculations
- Use folders to organize content
- Implement row-level security
- Version control workbooks
- Set appropriate permissions

## Anti-Patterns

### 1. Overusing Blending
```tableau
// Bad: Blend when relationship would work
Primary: Sales (blend on Date, Product)
Secondary: Costs (blend on Date, Product)

// Good: Use relationship or join
Sales <- (Product ID) -> Costs
```

### 2. Inefficient LODs
```tableau
// Bad: Nested LODs
{ FIXED [Customer] :
    MAX({ FIXED [Order] : SUM([Amount]) })
}

// Good: Single LOD
{ FIXED [Customer] : SUM([Amount]) }
```

### 3. Too Many Marks
```tableau
// Bad: Scatter plot with 100K points
// Good: Aggregate or filter data
// Use density marks for large datasets
```

### 4. No Extract Optimization
```tableau
// Bad: Extract entire table without filters
// Good: Filter to relevant data, aggregate dimensions
```

## Resources

- [Tableau Help](https://help.tableau.com/)
- [Tableau Community Forums](https://community.tableau.com/)
- [Tableau Public Gallery](https://public.tableau.com/gallery)
- [Tableau KB](https://kb.tableau.com/)
- [Tableau Conference](https://www.tableau.com/events/conference)
- [LOD Expression Guide](https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm)
- [Performance Best Practices](https://help.tableau.com/current/pro/desktop/en-us/performance_tips.htm)
