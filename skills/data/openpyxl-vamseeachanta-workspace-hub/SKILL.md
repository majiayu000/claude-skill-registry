---
name: openpyxl
description: Create and manipulate Microsoft Excel workbooks programmatically. Build spreadsheets with formulas, charts, conditional formatting, and pivot tables. Handle large datasets efficiently with streaming mode.
version: 1.0.0
category: office-docs
type: skill
capabilities:
  - workbook_creation
  - cell_formatting
  - formula_support
  - chart_generation
  - conditional_formatting
  - pivot_tables
  - large_dataset_handling
  - streaming_mode
tools:
  - python
  - openpyxl
  - pandas
tags: [excel, xlsx, spreadsheet, formulas, charts, data-analysis, office-automation]
platforms: [windows, macos, linux]
related_skills:
  - pandas-data-processing
  - python-docx
  - plotly
---

# Openpyxl Excel Automation Skill

## Overview

Openpyxl is a Python library for reading and writing Excel 2010+ xlsx/xlsm files. This skill covers comprehensive patterns for spreadsheet automation including:

- **Workbook creation** with multiple worksheets
- **Cell operations** including formatting, merging, and data validation
- **Formula support** for calculations and dynamic content
- **Chart generation** for data visualization within Excel
- **Conditional formatting** for visual data analysis
- **Large dataset handling** with optimized read/write modes
- **Pivot table creation** for data summarization
- **Style management** for professional appearances

## When to Use This Skill

### USE when:
- Creating Excel reports with formulas and calculations
- Generating spreadsheets from database queries
- Automating financial reports and dashboards
- Building Excel templates with formatting
- Processing and transforming existing Excel files
- Creating charts and visualizations in Excel
- Applying conditional formatting rules
- Building data entry forms with validation
- Handling large datasets (100k+ rows)
- Creating pivot tables programmatically

### DON'T USE when:
- Only need to read data into pandas (use pandas.read_excel directly)
- Need real-time Excel manipulation (use xlwings on Windows)
- Working with .xls format (use xlrd/xlwt)
- Creating complex macros (requires VBA)
- Need Excel-specific features like Power Query

## Prerequisites

### Installation

```bash
# Basic installation
pip install openpyxl

# Using uv (recommended)
uv pip install openpyxl

# With image support
pip install openpyxl Pillow

# With pandas integration
pip install openpyxl pandas

# Full installation
pip install openpyxl Pillow pandas numpy
```

### Verify Installation

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border
from openpyxl.chart import BarChart, LineChart, PieChart
from openpyxl.utils.dataframe import dataframe_to_rows

print("openpyxl installed successfully!")
```

## Core Capabilities

### 1. Basic Workbook Creation

```python
"""
Create a basic Excel workbook with data and formatting.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

def create_basic_workbook(output_path: str) -> None:
    """Create a basic workbook with common elements."""
    # Create workbook and select active sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales Report"

    # Set document properties
    wb.properties.creator = "Excel Generator"
    wb.properties.title = "Monthly Sales Report"
    wb.properties.created = datetime.now()

    # Define styles
    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")

    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Headers
    headers = ["Product", "Q1", "Q2", "Q3", "Q4", "Total"]
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border

    # Data
    data = [
        ["Widget A", 1500, 1800, 2200, 2500],
        ["Widget B", 800, 950, 1100, 1300],
        ["Widget C", 2000, 2300, 2600, 2900],
        ["Widget D", 500, 600, 750, 900],
    ]

    for row_idx, row_data in enumerate(data, start=2):
        # Product name
        ws.cell(row=row_idx, column=1, value=row_data[0]).border = thin_border

        # Quarterly values
        for col_idx, value in enumerate(row_data[1:], start=2):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = thin_border
            cell.number_format = '#,##0'

        # Total formula
        total_cell = ws.cell(
            row=row_idx,
            column=6,
            value=f"=SUM(B{row_idx}:E{row_idx})"
        )
        total_cell.border = thin_border
        total_cell.font = Font(bold=True)
        total_cell.number_format = '#,##0'

    # Add totals row
    total_row = len(data) + 2
    ws.cell(row=total_row, column=1, value="TOTAL").font = Font(bold=True)

    for col in range(2, 7):
        col_letter = get_column_letter(col)
        cell = ws.cell(
            row=total_row,
            column=col,
            value=f"=SUM({col_letter}2:{col_letter}{total_row-1})"
        )
        cell.font = Font(bold=True)
        cell.number_format = '#,##0'
        cell.border = thin_border

    # Adjust column widths
    column_widths = [15, 12, 12, 12, 12, 14]
    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = width

    # Freeze header row
    ws.freeze_panes = "A2"

    # Save workbook
    wb.save(output_path)
    print(f"Workbook saved to {output_path}")


create_basic_workbook("sales_report.xlsx")
```

### 2. Advanced Cell Formatting

```python
"""
Advanced cell formatting with styles, merging, and data validation.
"""
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side,
    GradientFill, NamedStyle, Color
)
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import Rule, CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

def create_formatted_workbook(output_path: str) -> None:
    """Create workbook with advanced formatting."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Formatted Data"

    # Create named styles for reuse
    header_style = NamedStyle(name="header_style")
    header_style.font = Font(bold=True, color="FFFFFF", size=11)
    header_style.fill = PatternFill(start_color="2F5496", fill_type="solid")
    header_style.alignment = Alignment(horizontal="center", vertical="center")
    header_style.border = Border(
        bottom=Side(style='medium', color="1F4E79")
    )
    wb.add_named_style(header_style)

    currency_style = NamedStyle(name="currency_style")
    currency_style.number_format = '"$"#,##0.00'
    currency_style.alignment = Alignment(horizontal="right")
    wb.add_named_style(currency_style)

    percentage_style = NamedStyle(name="percentage_style")
    percentage_style.number_format = '0.0%'
    percentage_style.alignment = Alignment(horizontal="center")
    wb.add_named_style(percentage_style)

    # Title with merged cells
    ws.merge_cells('A1:F1')
    title_cell = ws['A1']
    title_cell.value = "Financial Summary Report"
    title_cell.font = Font(bold=True, size=16, color="1F4E79")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    # Subtitle
    ws.merge_cells('A2:F2')
    subtitle_cell = ws['A2']
    subtitle_cell.value = "Fiscal Year 2026"
    subtitle_cell.font = Font(italic=True, size=12, color="5B9BD5")
    subtitle_cell.alignment = Alignment(horizontal="center")
    ws.row_dimensions[2].height = 20

    # Headers row
    headers = ["Category", "Budget", "Actual", "Variance", "% of Budget", "Status"]
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=col, value=header)
        cell.style = "header_style"

    # Data with various formats
    data = [
        ["Revenue", 1000000, 1150000],
        ["Personnel", 500000, 485000],
        ["Operations", 200000, 215000],
        ["Marketing", 150000, 142000],
        ["Technology", 100000, 108000],
    ]

    for row_idx, (category, budget, actual) in enumerate(data, start=5):
        # Category
        ws.cell(row=row_idx, column=1, value=category)

        # Budget
        ws.cell(row=row_idx, column=2, value=budget).style = "currency_style"

        # Actual
        ws.cell(row=row_idx, column=3, value=actual).style = "currency_style"

        # Variance formula
        variance_cell = ws.cell(row=row_idx, column=4)
        variance_cell.value = f"=C{row_idx}-B{row_idx}"
        variance_cell.style = "currency_style"

        # Percentage formula
        pct_cell = ws.cell(row=row_idx, column=5)
        pct_cell.value = f"=C{row_idx}/B{row_idx}"
        pct_cell.style = "percentage_style"

        # Status (will be filled by conditional formatting)
        ws.cell(row=row_idx, column=6, value="")

    # Add conditional formatting for variance column
    # Green for positive, red for negative
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

    ws.conditional_formatting.add(
        'D5:D9',
        CellIsRule(
            operator='greaterThan',
            formula=['0'],
            fill=green_fill,
            font=Font(color="006100")
        )
    )

    ws.conditional_formatting.add(
        'D5:D9',
        CellIsRule(
            operator='lessThan',
            formula=['0'],
            fill=red_fill,
            font=Font(color="9C0006")
        )
    )

    # Data validation for status column
    status_validation = DataValidation(
        type="list",
        formula1='"On Track,At Risk,Over Budget,Under Budget"',
        allow_blank=True
    )
    status_validation.error = "Please select from the dropdown"
    status_validation.errorTitle = "Invalid Status"
    ws.add_data_validation(status_validation)
    status_validation.add('F5:F9')

    # Gradient fill example
    ws['A12'] = "Gradient Fill Example"
    ws['A12'].fill = GradientFill(
        stop=["4472C4", "70AD47"],
        degree=90
    )
    ws['A12'].font = Font(color="FFFFFF", bold=True)
    ws.merge_cells('A12:C12')

    # Column widths
    widths = {'A': 15, 'B': 15, 'C': 15, 'D': 15, 'E': 15, 'F': 15}
    for col, width in widths.items():
        ws.column_dimensions[col].width = width

    wb.save(output_path)
    print(f"Formatted workbook saved to {output_path}")


create_formatted_workbook("formatted_report.xlsx")
```

### 3. Chart Generation

```python
"""
Create various chart types in Excel.
"""
from openpyxl import Workbook
from openpyxl.chart import (
    BarChart, LineChart, PieChart, AreaChart, ScatterChart,
    Reference, Series
)
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.layout import Layout, ManualLayout

def create_charts_workbook(output_path: str) -> None:
    """Create workbook with various chart examples."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Chart Data"

    # Sample data for charts
    data = [
        ["Month", "Sales", "Expenses", "Profit"],
        ["Jan", 15000, 12000, 3000],
        ["Feb", 18000, 13000, 5000],
        ["Mar", 22000, 14500, 7500],
        ["Apr", 20000, 14000, 6000],
        ["May", 25000, 15000, 10000],
        ["Jun", 28000, 16000, 12000],
    ]

    for row in data:
        ws.append(row)

    # Bar Chart
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.grouping = "clustered"
    bar_chart.title = "Monthly Financial Overview"
    bar_chart.y_axis.title = "Amount ($)"
    bar_chart.x_axis.title = "Month"

    # Data references
    data_ref = Reference(ws, min_col=2, max_col=4, min_row=1, max_row=7)
    cats_ref = Reference(ws, min_col=1, min_row=2, max_row=7)

    bar_chart.add_data(data_ref, titles_from_data=True)
    bar_chart.set_categories(cats_ref)
    bar_chart.shape = 4  # Rounded corners

    # Style the chart
    bar_chart.style = 10
    bar_chart.width = 15
    bar_chart.height = 10

    ws.add_chart(bar_chart, "F2")

    # Line Chart
    line_chart = LineChart()
    line_chart.title = "Profit Trend"
    line_chart.y_axis.title = "Profit ($)"
    line_chart.x_axis.title = "Month"
    line_chart.style = 12

    profit_data = Reference(ws, min_col=4, min_row=1, max_row=7)
    line_chart.add_data(profit_data, titles_from_data=True)
    line_chart.set_categories(cats_ref)

    # Add markers
    line_chart.series[0].marker.symbol = "circle"
    line_chart.series[0].marker.size = 7
    line_chart.series[0].graphicalProperties.line.width = 25000  # in EMUs

    ws.add_chart(line_chart, "F18")

    # Pie Chart on new sheet
    pie_ws = wb.create_sheet("Pie Chart")

    pie_data = [
        ["Category", "Value"],
        ["Product A", 35],
        ["Product B", 25],
        ["Product C", 20],
        ["Product D", 15],
        ["Other", 5],
    ]

    for row in pie_data:
        pie_ws.append(row)

    pie_chart = PieChart()
    pie_chart.title = "Sales by Product Category"

    pie_data_ref = Reference(pie_ws, min_col=2, min_row=2, max_row=6)
    pie_labels_ref = Reference(pie_ws, min_col=1, min_row=2, max_row=6)

    pie_chart.add_data(pie_data_ref)
    pie_chart.set_categories(pie_labels_ref)

    # Add data labels with percentages
    pie_chart.dataLabels = DataLabelList()
    pie_chart.dataLabels.showPercent = True
    pie_chart.dataLabels.showVal = False
    pie_chart.dataLabels.showCatName = True

    pie_ws.add_chart(pie_chart, "D2")

    # Stacked Area Chart
    area_ws = wb.create_sheet("Area Chart")

    area_data = [
        ["Quarter", "Region A", "Region B", "Region C"],
        ["Q1", 5000, 4000, 3000],
        ["Q2", 6000, 4500, 3500],
        ["Q3", 7000, 5000, 4000],
        ["Q4", 8000, 5500, 4500],
    ]

    for row in area_data:
        area_ws.append(row)

    area_chart = AreaChart()
    area_chart.title = "Regional Sales Growth"
    area_chart.style = 13
    area_chart.grouping = "stacked"

    area_data_ref = Reference(area_ws, min_col=2, max_col=4, min_row=1, max_row=5)
    area_cats_ref = Reference(area_ws, min_col=1, min_row=2, max_row=5)

    area_chart.add_data(area_data_ref, titles_from_data=True)
    area_chart.set_categories(area_cats_ref)

    area_ws.add_chart(area_chart, "F2")

    # Scatter Chart
    scatter_ws = wb.create_sheet("Scatter Chart")

    scatter_data = [
        ["X", "Y"],
        [1, 2.5],
        [2, 4.1],
        [3, 5.8],
        [4, 8.2],
        [5, 10.1],
        [6, 12.5],
        [7, 14.8],
    ]

    for row in scatter_data:
        scatter_ws.append(row)

    scatter_chart = ScatterChart()
    scatter_chart.title = "Correlation Analysis"
    scatter_chart.x_axis.title = "X Values"
    scatter_chart.y_axis.title = "Y Values"
    scatter_chart.style = 13

    x_values = Reference(scatter_ws, min_col=1, min_row=2, max_row=8)
    y_values = Reference(scatter_ws, min_col=2, min_row=2, max_row=8)

    series = Series(y_values, x_values, title="Data Points")
    scatter_chart.series.append(series)

    # Add trendline
    from openpyxl.chart.trendline import Trendline
    series.trendline = Trendline(trendlineType='linear')

    scatter_ws.add_chart(scatter_chart, "D2")

    wb.save(output_path)
    print(f"Charts workbook saved to {output_path}")


create_charts_workbook("charts_example.xlsx")
```

### 4. Conditional Formatting

```python
"""
Apply conditional formatting rules for visual data analysis.
"""
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Border, Side
from openpyxl.formatting.rule import (
    ColorScaleRule, DataBarRule, IconSetRule,
    CellIsRule, FormulaRule, Rule
)
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.utils import get_column_letter

def create_conditional_formatting_workbook(output_path: str) -> None:
    """Create workbook demonstrating conditional formatting."""
    wb = Workbook()

    # Sheet 1: Color Scales
    ws1 = wb.active
    ws1.title = "Color Scales"

    # Header
    ws1['A1'] = "Performance Scores"
    ws1['A1'].font = Font(bold=True, size=14)

    # Data
    scores = [85, 72, 91, 68, 95, 78, 82, 60, 88, 75, 93, 71, 86, 79, 64]
    for i, score in enumerate(scores, start=3):
        ws1.cell(row=i, column=1, value=f"Employee {i-2}")
        ws1.cell(row=i, column=2, value=score)

    # Apply 3-color scale (red-yellow-green)
    color_scale_rule = ColorScaleRule(
        start_type='min',
        start_color='F8696B',  # Red
        mid_type='percentile',
        mid_value=50,
        mid_color='FFEB84',  # Yellow
        end_type='max',
        end_color='63BE7B'  # Green
    )
    ws1.conditional_formatting.add('B3:B17', color_scale_rule)

    # Sheet 2: Data Bars
    ws2 = wb.create_sheet("Data Bars")

    ws2['A1'] = "Sales by Region"
    ws2['A1'].font = Font(bold=True, size=14)

    regions = [
        ("North", 125000),
        ("South", 98000),
        ("East", 145000),
        ("West", 112000),
        ("Central", 87000),
    ]

    for i, (region, sales) in enumerate(regions, start=3):
        ws2.cell(row=i, column=1, value=region)
        ws2.cell(row=i, column=2, value=sales)

    # Apply data bars
    data_bar_rule = DataBarRule(
        start_type='num',
        start_value=0,
        end_type='max',
        color='5B9BD5',
        showValue=True,
        minLength=None,
        maxLength=None
    )
    ws2.conditional_formatting.add('B3:B7', data_bar_rule)

    # Set column width for visibility
    ws2.column_dimensions['B'].width = 25

    # Sheet 3: Icon Sets
    ws3 = wb.create_sheet("Icon Sets")

    ws3['A1'] = "Project Status"
    ws3['A1'].font = Font(bold=True, size=14)

    # Headers
    ws3['A2'] = "Project"
    ws3['B2'] = "Completion %"
    ws3['C2'] = "Status"

    projects = [
        ("Project Alpha", 95),
        ("Project Beta", 60),
        ("Project Gamma", 30),
        ("Project Delta", 85),
        ("Project Epsilon", 45),
    ]

    for i, (project, completion) in enumerate(projects, start=3):
        ws3.cell(row=i, column=1, value=project)
        ws3.cell(row=i, column=2, value=completion / 100)
        ws3.cell(row=i, column=2).number_format = '0%'

    # Apply icon set (3 traffic lights)
    icon_set_rule = IconSetRule(
        '3TrafficLights1',
        'percent',
        [0, 33, 67],
        showValue=True,
        reverse=False
    )
    ws3.conditional_formatting.add('B3:B7', icon_set_rule)

    # Sheet 4: Cell Rules
    ws4 = wb.create_sheet("Cell Rules")

    ws4['A1'] = "Inventory Status"
    ws4['A1'].font = Font(bold=True, size=14)

    # Headers
    for col, header in enumerate(['Product', 'Stock', 'Reorder Level', 'Status'], start=1):
        ws4.cell(row=2, column=col, value=header).font = Font(bold=True)

    inventory = [
        ("Widget A", 150, 50),
        ("Widget B", 25, 50),
        ("Widget C", 80, 50),
        ("Widget D", 10, 50),
        ("Widget E", 200, 50),
    ]

    for i, (product, stock, reorder) in enumerate(inventory, start=3):
        ws4.cell(row=i, column=1, value=product)
        ws4.cell(row=i, column=2, value=stock)
        ws4.cell(row=i, column=3, value=reorder)

    # Highlight cells below reorder level
    red_fill = PatternFill(start_color='FFC7CE', fill_type='solid')
    red_font = Font(color='9C0006')

    ws4.conditional_formatting.add(
        'B3:B7',
        CellIsRule(
            operator='lessThan',
            formula=['C3'],
            fill=red_fill,
            font=red_font
        )
    )

    # Highlight cells above 100 with green
    green_fill = PatternFill(start_color='C6EFCE', fill_type='solid')
    green_font = Font(color='006100')

    ws4.conditional_formatting.add(
        'B3:B7',
        CellIsRule(
            operator='greaterThan',
            formula=['100'],
            fill=green_fill,
            font=green_font
        )
    )

    # Sheet 5: Formula-based Rules
    ws5 = wb.create_sheet("Formula Rules")

    ws5['A1'] = "Highlight Entire Rows"
    ws5['A1'].font = Font(bold=True, size=14)

    # Headers
    for col, header in enumerate(['Name', 'Dept', 'Salary', 'Status'], start=1):
        ws5.cell(row=2, column=col, value=header).font = Font(bold=True)

    employees = [
        ("Alice", "Engineering", 95000, "Active"),
        ("Bob", "Marketing", 72000, "Inactive"),
        ("Carol", "Engineering", 88000, "Active"),
        ("David", "Sales", 65000, "Inactive"),
        ("Eve", "Engineering", 102000, "Active"),
    ]

    for i, (name, dept, salary, status) in enumerate(employees, start=3):
        ws5.cell(row=i, column=1, value=name)
        ws5.cell(row=i, column=2, value=dept)
        ws5.cell(row=i, column=3, value=salary)
        ws5.cell(row=i, column=4, value=status)

    # Highlight entire row if Status is "Inactive"
    gray_fill = PatternFill(start_color='D9D9D9', fill_type='solid')

    ws5.conditional_formatting.add(
        'A3:D7',
        FormulaRule(
            formula=['$D3="Inactive"'],
            fill=gray_fill
        )
    )

    # Highlight Engineering department rows with blue
    blue_fill = PatternFill(start_color='BDD7EE', fill_type='solid')

    ws5.conditional_formatting.add(
        'A3:D7',
        FormulaRule(
            formula=['$B3="Engineering"'],
            fill=blue_fill
        )
    )

    wb.save(output_path)
    print(f"Conditional formatting workbook saved to {output_path}")


create_conditional_formatting_workbook("conditional_formatting.xlsx")
```

### 5. Large Dataset Handling with Streaming

```python
"""
Handle large datasets efficiently with read-only and write-only modes.
"""
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from typing import Generator, List, Dict, Any, Iterator
import time

def write_large_dataset_streaming(
    output_path: str,
    data_generator: Generator,
    headers: List[str],
    chunk_size: int = 10000
) -> int:
    """Write large dataset using write-only mode for memory efficiency."""
    # Use write_only mode for streaming
    wb = Workbook(write_only=True)
    ws = wb.create_sheet("Large Data")

    # Write headers
    ws.append(headers)

    rows_written = 0
    start_time = time.time()

    for row in data_generator:
        ws.append(row)
        rows_written += 1

        if rows_written % chunk_size == 0:
            elapsed = time.time() - start_time
            print(f"Written {rows_written:,} rows ({elapsed:.1f}s)")

    wb.save(output_path)

    total_time = time.time() - start_time
    print(f"Total: {rows_written:,} rows written in {total_time:.1f}s")

    return rows_written


def read_large_dataset_streaming(
    file_path: str,
    chunk_size: int = 1000
) -> Generator:
    """Read large dataset using read-only mode for memory efficiency."""
    # Use read_only mode for streaming
    wb = load_workbook(file_path, read_only=True)
    ws = wb.active

    chunk = []
    headers = None

    for row_idx, row in enumerate(ws.iter_rows(values_only=True)):
        if row_idx == 0:
            headers = row
            continue

        # Convert row to dictionary
        row_dict = dict(zip(headers, row))
        chunk.append(row_dict)

        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk

    wb.close()


def generate_sample_data(num_rows: int) -> Generator:
    """Generate sample data for testing."""
    import random
    from datetime import datetime, timedelta

    base_date = datetime(2026, 1, 1)
    categories = ["Electronics", "Clothing", "Food", "Books", "Home"]
    regions = ["North", "South", "East", "West"]

    for i in range(num_rows):
        yield [
            i + 1,  # ID
            f"Product_{i+1}",  # Product Name
            random.choice(categories),  # Category
            random.choice(regions),  # Region
            round(random.uniform(10, 1000), 2),  # Price
            random.randint(1, 100),  # Quantity
            (base_date + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),  # Date
        ]


def process_large_file_example() -> None:
    """Example of processing large Excel files."""
    # Generate large dataset
    headers = ["ID", "Product", "Category", "Region", "Price", "Quantity", "Date"]
    num_rows = 100000  # 100k rows

    print(f"Generating {num_rows:,} rows...")
    output_path = "large_dataset.xlsx"

    # Write large file
    rows_written = write_large_dataset_streaming(
        output_path,
        generate_sample_data(num_rows),
        headers
    )

    # Read and process in chunks
    print(f"\nReading file in chunks...")
    total_revenue = 0
    category_totals = {}

    for chunk in read_large_dataset_streaming(output_path, chunk_size=5000):
        for row in chunk:
            revenue = row['Price'] * row['Quantity']
            total_revenue += revenue

            category = row['Category']
            category_totals[category] = category_totals.get(category, 0) + revenue

    print(f"\nTotal Revenue: ${total_revenue:,.2f}")
    print("\nRevenue by Category:")
    for category, total in sorted(category_totals.items()):
        print(f"  {category}: ${total:,.2f}")


# process_large_file_example()
```

### 6. Pivot Table Creation

```python
"""
Create pivot table structures in Excel (note: full pivot table functionality
requires Excel to be installed and opened).
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from typing import List, Dict, Any
from collections import defaultdict

def create_pivot_like_table(
    data: List[Dict[str, Any]],
    row_field: str,
    col_field: str,
    value_field: str,
    aggregation: str = 'sum'
) -> Dict[str, Dict[str, float]]:
    """Create pivot table structure from data."""
    pivot_data = defaultdict(lambda: defaultdict(float))
    row_totals = defaultdict(float)
    col_totals = defaultdict(float)
    grand_total = 0

    for record in data:
        row_val = record[row_field]
        col_val = record[col_field]
        value = record[value_field]

        if aggregation == 'sum':
            pivot_data[row_val][col_val] += value
            row_totals[row_val] += value
            col_totals[col_val] += value
            grand_total += value
        elif aggregation == 'count':
            pivot_data[row_val][col_val] += 1
            row_totals[row_val] += 1
            col_totals[col_val] += 1
            grand_total += 1

    return {
        'data': dict(pivot_data),
        'row_totals': dict(row_totals),
        'col_totals': dict(col_totals),
        'grand_total': grand_total
    }


def write_pivot_table_to_excel(
    wb: Workbook,
    pivot_result: Dict,
    sheet_name: str,
    title: str
) -> None:
    """Write pivot table result to Excel sheet."""
    ws = wb.create_sheet(sheet_name)

    # Styles
    header_fill = PatternFill(start_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    total_fill = PatternFill(start_color="D9E2F3", fill_type="solid")
    total_font = Font(bold=True)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Title
    ws['A1'] = title
    ws['A1'].font = Font(bold=True, size=14)
    ws.merge_cells('A1:E1')

    pivot_data = pivot_result['data']
    row_totals = pivot_result['row_totals']
    col_totals = pivot_result['col_totals']
    grand_total = pivot_result['grand_total']

    # Get unique columns and rows
    all_cols = sorted(set(col for row_data in pivot_data.values() for col in row_data.keys()))
    all_rows = sorted(pivot_data.keys())

    # Write column headers
    start_row = 3
    ws.cell(row=start_row, column=1, value="").border = border

    for col_idx, col_name in enumerate(all_cols, start=2):
        cell = ws.cell(row=start_row, column=col_idx, value=col_name)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
        cell.border = border

    # Total column header
    total_col = len(all_cols) + 2
    cell = ws.cell(row=start_row, column=total_col, value="Total")
    cell.fill = header_fill
    cell.font = header_font
    cell.border = border

    # Write data rows
    for row_idx, row_name in enumerate(all_rows, start=start_row + 1):
        # Row header
        cell = ws.cell(row=row_idx, column=1, value=row_name)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border

        # Data cells
        for col_idx, col_name in enumerate(all_cols, start=2):
            value = pivot_data[row_name].get(col_name, 0)
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.number_format = '#,##0.00'
            cell.border = border

        # Row total
        cell = ws.cell(row=row_idx, column=total_col, value=row_totals[row_name])
        cell.fill = total_fill
        cell.font = total_font
        cell.number_format = '#,##0.00'
        cell.border = border

    # Write totals row
    totals_row = start_row + len(all_rows) + 1
    cell = ws.cell(row=totals_row, column=1, value="Total")
    cell.fill = header_fill
    cell.font = header_font
    cell.border = border

    for col_idx, col_name in enumerate(all_cols, start=2):
        cell = ws.cell(row=totals_row, column=col_idx, value=col_totals[col_name])
        cell.fill = total_fill
        cell.font = total_font
        cell.number_format = '#,##0.00'
        cell.border = border

    # Grand total
    cell = ws.cell(row=totals_row, column=total_col, value=grand_total)
    cell.fill = total_fill
    cell.font = total_font
    cell.number_format = '#,##0.00'
    cell.border = border

    # Adjust column widths
    for col_idx in range(1, total_col + 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = 15


def create_pivot_table_example(output_path: str) -> None:
    """Create example workbook with pivot table."""
    # Sample data
    sales_data = [
        {"Product": "Widget A", "Region": "North", "Sales": 15000},
        {"Product": "Widget A", "Region": "South", "Sales": 12000},
        {"Product": "Widget A", "Region": "East", "Sales": 18000},
        {"Product": "Widget B", "Region": "North", "Sales": 8000},
        {"Product": "Widget B", "Region": "South", "Sales": 9500},
        {"Product": "Widget B", "Region": "East", "Sales": 7200},
        {"Product": "Widget C", "Region": "North", "Sales": 22000},
        {"Product": "Widget C", "Region": "South", "Sales": 19000},
        {"Product": "Widget C", "Region": "East", "Sales": 25000},
    ]

    wb = Workbook()

    # Raw data sheet
    ws_data = wb.active
    ws_data.title = "Raw Data"

    headers = ["Product", "Region", "Sales"]
    ws_data.append(headers)
    for row in sales_data:
        ws_data.append([row["Product"], row["Region"], row["Sales"]])

    # Create pivot table
    pivot_result = create_pivot_like_table(
        sales_data,
        row_field="Product",
        col_field="Region",
        value_field="Sales",
        aggregation="sum"
    )

    write_pivot_table_to_excel(
        wb,
        pivot_result,
        "Pivot Table",
        "Sales by Product and Region"
    )

    wb.save(output_path)
    print(f"Pivot table workbook saved to {output_path}")


create_pivot_table_example("pivot_table_example.xlsx")
```

## Integration Examples

### Pandas Integration

```python
"""
Integration with pandas for data analysis workflows.
"""
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, PatternFill, Alignment

def dataframe_to_styled_excel(
    df: pd.DataFrame,
    output_path: str,
    sheet_name: str = "Data",
    header_color: str = "4472C4"
) -> None:
    """Export pandas DataFrame to styled Excel file."""
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    # Write DataFrame to worksheet
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True)):
        for c_idx, value in enumerate(row, start=1):
            cell = ws.cell(row=r_idx + 1, column=c_idx, value=value)

            # Style header row
            if r_idx == 0:
                cell.fill = PatternFill(start_color=header_color, fill_type="solid")
                cell.font = Font(bold=True, color="FFFFFF")
                cell.alignment = Alignment(horizontal="center")

    # Auto-adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        ws.column_dimensions[column_letter].width = min(max_length + 2, 50)

    wb.save(output_path)
    print(f"DataFrame exported to {output_path}")


def excel_to_dataframe_with_types(
    file_path: str,
    sheet_name: str = None,
    dtype_mapping: dict = None
) -> pd.DataFrame:
    """Read Excel file to pandas DataFrame with proper type handling."""
    # Read with openpyxl engine
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        engine='openpyxl'
    )

    # Apply type mappings if provided
    if dtype_mapping:
        for col, dtype in dtype_mapping.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

    return df


def create_multi_sheet_report(
    dataframes: dict,
    output_path: str
) -> None:
    """Create Excel workbook with multiple DataFrames on separate sheets."""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Access worksheet for formatting
            ws = writer.sheets[sheet_name]

            # Style header row
            for cell in ws[1]:
                cell.fill = PatternFill(start_color="4472C4", fill_type="solid")
                cell.font = Font(bold=True, color="FFFFFF")

    print(f"Multi-sheet report saved to {output_path}")


# Example usage
# df = pd.DataFrame({'A': [1, 2, 3], 'B': ['x', 'y', 'z']})
# dataframe_to_styled_excel(df, 'output.xlsx')
```

### Database Report Generation

```python
"""
Generate Excel reports from database queries.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
import sqlite3
from typing import List, Tuple, Any

def generate_database_report(
    db_path: str,
    queries: dict,
    output_path: str
) -> None:
    """Generate Excel report from multiple database queries."""
    conn = sqlite3.connect(db_path)
    wb = Workbook()

    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    header_fill = PatternFill(start_color="2F5496", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for sheet_name, query in queries.items():
        # Execute query
        cursor = conn.execute(query)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        # Create sheet
        ws = wb.create_sheet(sheet_name)

        # Add metadata
        ws['A1'] = f"Report: {sheet_name}"
        ws['A1'].font = Font(bold=True, size=14)
        ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ws['A2'].font = Font(italic=True, size=10)

        # Write headers
        for col_idx, header in enumerate(columns, start=1):
            cell = ws.cell(row=4, column=col_idx, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")
            cell.border = border

        # Write data
        for row_idx, row in enumerate(rows, start=5):
            for col_idx, value in enumerate(row, start=1):
                cell = ws.cell(row=row_idx, column=col_idx, value=value)
                cell.border = border

                # Format numbers
                if isinstance(value, (int, float)):
                    cell.number_format = '#,##0.00'

        # Auto-fit columns
        for col_idx in range(1, len(columns) + 1):
            ws.column_dimensions[get_column_letter(col_idx)].width = 15

        # Add row count
        ws.cell(row=len(rows) + 6, column=1, value=f"Total rows: {len(rows)}")

    conn.close()
    wb.save(output_path)
    print(f"Database report saved to {output_path}")
```

## Best Practices

### 1. Memory Management

```python
"""Best practices for memory-efficient Excel operations."""

# DO: Use write_only mode for large writes
wb = Workbook(write_only=True)
ws = wb.create_sheet()
for row in large_data:
    ws.append(row)  # Streams directly to file
wb.save('output.xlsx')

# DO: Use read_only mode for large reads
wb = load_workbook('large_file.xlsx', read_only=True)
for row in wb.active.iter_rows(values_only=True):
    process_row(row)
wb.close()  # Important: close when done

# DON'T: Load entire file into memory unnecessarily
# wb = load_workbook('large_file.xlsx')  # Loads all into memory
```

### 2. Style Reuse

```python
"""Reuse styles for better performance."""
from openpyxl.styles import NamedStyle

# DO: Create named styles once, apply many times
header_style = NamedStyle(name="header")
header_style.font = Font(bold=True, color="FFFFFF")
header_style.fill = PatternFill(start_color="4472C4", fill_type="solid")
wb.add_named_style(header_style)

# Apply to multiple cells efficiently
for cell in ws[1]:
    cell.style = "header"

# DON'T: Create style objects for each cell
# for cell in ws[1]:
#     cell.font = Font(bold=True)  # Creates new Font each time
```

### 3. Error Handling

```python
"""Robust error handling for Excel operations."""
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def safe_save_workbook(wb: Workbook, output_path: str) -> bool:
    """Safely save workbook with error handling."""
    try:
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Check if file is locked
        if Path(output_path).exists():
            try:
                Path(output_path).rename(output_path)
            except PermissionError:
                logger.error(f"File is locked: {output_path}")
                return False

        wb.save(output_path)
        logger.info(f"Workbook saved: {output_path}")
        return True

    except Exception as e:
        logger.exception(f"Failed to save workbook: {e}")
        return False
```

## Troubleshooting

### Common Issues

#### 1. Formula Not Calculating

```python
# Problem: Formulas show as text, not calculated
# Solution: Ensure proper formula format

# DO: Use equals sign and proper cell references
ws['A1'] = '=SUM(B1:B10)'

# DON'T: Use string that looks like formula
# ws['A1'] = 'SUM(B1:B10)'  # Missing =

# Note: Formulas are calculated when Excel opens the file
```

#### 2. Large File Performance

```python
# Problem: Memory error with large files
# Solution: Use streaming modes

# For writing
wb = Workbook(write_only=True)

# For reading
wb = load_workbook('file.xlsx', read_only=True, data_only=True)
```

#### 3. Style Not Appearing

```python
# Problem: Styles don't appear in Excel
# Solution: Ensure style is properly applied

# DO: Apply fill with fill_type
fill = PatternFill(start_color="FF0000", fill_type="solid")

# DON'T: Missing fill_type
# fill = PatternFill(start_color="FF0000")  # Won't show
```

## Version History

### 1.0.0 (2026-01-17)
- Initial skill creation
- Core capabilities documentation
- 6 complete code examples
- Large dataset handling patterns
- Integration with pandas

## Resources

- **Official Documentation**: https://openpyxl.readthedocs.io/
- **GitHub Repository**: https://github.com/theorchard/openpyxl
- **PyPI Package**: https://pypi.org/project/openpyxl/

## Related Skills

- **pandas-data-processing** - Data analysis and transformation
- **python-docx** - Word document generation
- **plotly** - Interactive chart generation
- **pypdf** - PDF manipulation

---

*This skill provides comprehensive patterns for Excel automation refined from production data processing systems.*
