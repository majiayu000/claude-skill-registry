---
slug: "qto-report"
display_name: "QTO Report"
description: "Generate Quantity Take-Off (QTO) reports from BIM/CAD data. Extract volumes, areas, counts by category. Group elements, apply calculation rules, and create cost estimates automatically."
---

# Quantity Take-Off (QTO) Report Generation

## Overview

Based on DDC methodology (Chapter 3.2), this skill automates the extraction and grouping of quantities from BIM/CAD data. QTO is the foundation for cost estimation, scheduling, and project planning in construction.

**Book Reference:** "Quantity Take-Off и автоматическое создание смет" / "QTO and Automated Estimates"

> "QTO Quantity Take-Off: группировка данных по атрибутам позволяет автоматически извлекать объемы и количества из BIM-моделей для расчета стоимости."
> — DDC Book, Chapter 3.2

## 5D BIM Concept

The QTO process is central to 5D BIM:
- **3D**: Geometry (volume, area, length)
- **4D**: Time (schedule integration)
- **5D**: Cost (quantity × unit price)

## Quick Start

```python
import pandas as pd

# Load BIM element data
df = pd.read_csv("revit_export.csv")

# Generate QTO by category
qto = df.groupby('Category').agg({
    'Volume': 'sum',
    'Area': 'sum',
    'ElementId': 'count'
}).rename(columns={'ElementId': 'Count'})

# Calculate cost (if unit prices available)
qto['Unit_Price'] = [150, 80, 450, 200]  # $/m³
qto['Total_Cost'] = qto['Volume'] * qto['Unit_Price']

qto.to_excel("qto_report.xlsx")
```

## Core QTO Functions

### Basic QTO by Category

```python
import pandas as pd

def generate_qto(df, group_by='Category'):
    """
    Generate Quantity Take-Off grouped by specified column

    Args:
        df: DataFrame with BIM elements
        group_by: Column(s) to group by

    Returns:
        QTO summary DataFrame
    """
    # Define aggregations based on available columns
    agg_dict = {}

    if 'Volume' in df.columns:
        agg_dict['Volume'] = 'sum'
    if 'Area' in df.columns:
        agg_dict['Area'] = 'sum'
    if 'Length' in df.columns:
        agg_dict['Length'] = 'sum'
    if 'Count' in df.columns:
        agg_dict['Count'] = 'sum'
    else:
        agg_dict['ElementId'] = 'count'

    qto = df.groupby(group_by).agg(agg_dict)

    if 'ElementId' in agg_dict:
        qto = qto.rename(columns={'ElementId': 'Count'})

    return qto.round(2)

# Usage
qto = generate_qto(df, group_by='Category')
print(qto)
```

### Multi-Level QTO

```python
def generate_multi_level_qto(df):
    """Generate QTO grouped by multiple levels"""
    qto = df.groupby(['Level', 'Category', 'Material']).agg({
        'Volume': ['sum', 'count'],
        'Area': 'sum'
    }).round(2)

    # Flatten column names
    qto.columns = ['Volume_m3', 'Element_Count', 'Area_m2']

    # Add percentages
    qto['Volume_Pct'] = (qto['Volume_m3'] /
                          qto['Volume_m3'].sum() * 100).round(1)

    return qto.sort_values('Volume_m3', ascending=False)

# Usage
qto = generate_multi_level_qto(df)
qto.to_excel("qto_multi_level.xlsx")
```

### QTO with Pivot Table

```python
def generate_qto_pivot(df, values='Volume', index='Level', columns='Category'):
    """Generate QTO as pivot table"""
    pivot = pd.pivot_table(
        df,
        values=values,
        index=index,
        columns=columns,
        aggfunc='sum',
        fill_value=0,
        margins=True,
        margins_name='TOTAL'
    ).round(2)

    return pivot

# Usage - Volume by Level and Category
qto_pivot = generate_qto_pivot(df, values='Volume')
qto_pivot.to_excel("qto_pivot.xlsx")
```

## Cost Calculation from QTO

### Apply Unit Prices

```python
def calculate_cost_from_qto(qto_df, prices_df, quantity_col='Volume'):
    """
    Calculate costs by applying unit prices to quantities

    Args:
        qto_df: QTO DataFrame with quantities
        prices_df: DataFrame with Category and Unit_Price
        quantity_col: Column containing quantities
    """
    # Merge with prices
    result = qto_df.reset_index().merge(
        prices_df, on='Category', how='left'
    )

    # Calculate costs
    result['Total_Cost'] = result[quantity_col] * result['Unit_Price']
    result['Cost_Pct'] = (result['Total_Cost'] /
                          result['Total_Cost'].sum() * 100).round(1)

    # Summary
    grand_total = result['Total_Cost'].sum()
    print(f"Grand Total: ${grand_total:,.2f}")

    return result

# Unit prices database
prices = pd.DataFrame({
    'Category': ['Wall', 'Floor', 'Column', 'Beam', 'Foundation'],
    'Unit_Price': [150, 80, 450, 200, 120],  # $/m³
    'Unit': ['m³', 'm³', 'm³', 'm³', 'm³']
})

# Calculate
cost_estimate = calculate_cost_from_qto(qto, prices)
cost_estimate.to_excel("cost_estimate.xlsx", index=False)
```

### Apply Rules from Excel

```python
def apply_excel_rules(df, rules_path):
    """
    Apply calculation rules defined in Excel file

    Excel format:
    | Category | Formula_Type | Factor | Unit |
    | Wall     | volume       | 1.05   | m³   |
    | Floor    | area         | 1.10   | m²   |
    """
    rules = pd.read_excel(rules_path)

    results = []
    for _, rule in rules.iterrows():
        category = rule['Category']
        formula_type = rule['Formula_Type']
        factor = rule['Factor']

        category_data = df[df['Category'] == category].copy()

        if formula_type == 'volume':
            category_data['Quantity'] = category_data['Volume'] * factor
        elif formula_type == 'area':
            category_data['Quantity'] = category_data['Area'] * factor
        elif formula_type == 'length':
            category_data['Quantity'] = category_data['Length'] * factor
        elif formula_type == 'count':
            category_data['Quantity'] = category_data.groupby('Category').ngroup() + 1

        category_data['Unit'] = rule['Unit']
        results.append(category_data)

    return pd.concat(results, ignore_index=True)

# Usage
df_with_quantities = apply_excel_rules(df, "calculation_rules.xlsx")
```

## BIM Data Extraction Patterns

### From Revit Export (CSV)

```python
def process_revit_export(csv_path):
    """Process standard Revit schedule export"""
    df = pd.read_csv(csv_path)

    # Standardize column names
    column_mapping = {
        'Family and Type': 'Type',
        'Volume': 'Volume',
        'Area': 'Area',
        'Count': 'Count',
        'Level': 'Level',
        'Category': 'Category'
    }

    df = df.rename(columns={
        k: v for k, v in column_mapping.items()
        if k in df.columns
    })

    # Convert volume from cubic feet to cubic meters (if needed)
    if 'Volume' in df.columns:
        # Revit exports in cubic feet by default
        df['Volume_m3'] = df['Volume'] * 0.0283168

    return df

# Usage
df = process_revit_export("revit_schedule.csv")
qto = generate_qto(df)
```

### From IFC Export

```python
# Using IfcOpenShell
import ifcopenshell
import pandas as pd

def extract_qto_from_ifc(ifc_path):
    """Extract quantities from IFC file"""
    ifc = ifcopenshell.open(ifc_path)

    elements = []
    for element in ifc.by_type("IfcBuildingElement"):
        # Get properties
        props = {
            'GlobalId': element.GlobalId,
            'Name': element.Name,
            'Type': element.is_a(),
            'Material': None,
            'Volume': None,
            'Area': None
        }

        # Extract quantities from property sets
        for definition in element.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                pset = definition.RelatingPropertyDefinition
                if pset.is_a('IfcElementQuantity'):
                    for qty in pset.Quantities:
                        if qty.is_a('IfcQuantityVolume'):
                            props['Volume'] = qty.VolumeValue
                        elif qty.is_a('IfcQuantityArea'):
                            props['Area'] = qty.AreaValue

        elements.append(props)

    return pd.DataFrame(elements)

# Usage
df = extract_qto_from_ifc("model.ifc")
qto = generate_qto(df, group_by='Type')
```

## Advanced QTO Reports

### Detailed Material Breakdown

```python
def material_breakdown_qto(df):
    """Detailed breakdown by material type"""
    breakdown = df.groupby(['Category', 'Material', 'Type']).agg({
        'Volume': 'sum',
        'Area': 'sum',
        'ElementId': 'nunique'
    }).rename(columns={'ElementId': 'Unique_Elements'})

    # Add subtotals for each category
    category_totals = df.groupby('Category').agg({
        'Volume': 'sum',
        'Area': 'sum'
    })

    breakdown['Category_Volume_Pct'] = breakdown.apply(
        lambda row: (row['Volume'] /
                    category_totals.loc[row.name[0], 'Volume'] * 100),
        axis=1
    ).round(1)

    return breakdown

# Usage
material_qto = material_breakdown_qto(df)
material_qto.to_excel("material_breakdown.xlsx")
```

### QTO with Waste Factors

```python
def qto_with_waste(df, waste_factors):
    """
    Apply waste factors to quantities

    Args:
        waste_factors: dict like {'Concrete': 1.05, 'Steel': 1.03}
    """
    qto = df.groupby(['Category', 'Material']).agg({
        'Volume': 'sum'
    }).reset_index()

    # Apply waste factors
    qto['Waste_Factor'] = qto['Material'].map(waste_factors).fillna(1.0)
    qto['Net_Volume'] = qto['Volume']
    qto['Gross_Volume'] = qto['Volume'] * qto['Waste_Factor']
    qto['Waste_Volume'] = qto['Gross_Volume'] - qto['Net_Volume']

    return qto

# Usage
waste = {'Concrete': 1.05, 'Brick': 1.08, 'Steel': 1.03}
qto = qto_with_waste(df, waste)
```

### QTO Comparison (Design vs As-Built)

```python
def compare_qto(design_df, asbuilt_df, group_by='Category'):
    """Compare designed vs as-built quantities"""
    design_qto = design_df.groupby(group_by)['Volume'].sum()
    asbuilt_qto = asbuilt_df.groupby(group_by)['Volume'].sum()

    comparison = pd.DataFrame({
        'Design': design_qto,
        'AsBuilt': asbuilt_qto
    })

    comparison['Difference'] = comparison['AsBuilt'] - comparison['Design']
    comparison['Variance_%'] = (
        (comparison['AsBuilt'] - comparison['Design']) /
        comparison['Design'] * 100
    ).round(1)

    return comparison

# Usage
comparison = compare_qto(design_df, asbuilt_df)
print(comparison)
```

## Export Functions

### Export to Multiple Formats

```python
def export_qto_report(qto_df, base_name, include_charts=True):
    """Export QTO to Excel with formatting and charts"""
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, Reference

    # Excel with multiple sheets
    with pd.ExcelWriter(f"{base_name}.xlsx", engine='openpyxl') as writer:
        # Summary sheet
        qto_df.to_excel(writer, sheet_name='Summary')

        # Detailed data
        if hasattr(qto_df, 'reset_index'):
            qto_df.reset_index().to_excel(
                writer, sheet_name='Details', index=False
            )

    # CSV for integration
    qto_df.to_csv(f"{base_name}.csv")

    # JSON for API
    qto_df.reset_index().to_json(
        f"{base_name}.json", orient='records', indent=2
    )

    print(f"Exported: {base_name}.xlsx, .csv, .json")

# Usage
export_qto_report(qto, "project_qto")
```

## Quick Reference

| Task | Code |
|------|------|
| Basic QTO | `df.groupby('Category')['Volume'].sum()` |
| Multi-column QTO | `df.groupby(['Level', 'Category']).agg({...})` |
| Pivot QTO | `pd.pivot_table(df, values='Volume', ...)` |
| Apply prices | `qto.merge(prices, on='Category')` |
| Calculate cost | `df['Cost'] = df['Volume'] * df['Unit_Price']` |
| Add waste factor | `df['Gross'] = df['Net'] * waste_factor` |

## Resources

- **Book**: "Data-Driven Construction" by Artem Boiko, Chapter 3.2
- **Website**: https://datadrivenconstruction.io
- **IfcOpenShell**: https://ifcopenshell.org

## Next Steps

- See `cost-estimation-resource` for detailed cost calculations
- See `auto-estimate-generator` for automated estimate creation
- See `gantt-chart` for 4D scheduling integration
- See `co2-estimation` for carbon footprint calculations
