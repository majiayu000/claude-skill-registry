---
name: "ifc-qto-extraction"
description: "Extract quantities from IFC/Revit models for quantity takeoff. Uses DDC converters to get element counts, areas, volumes, lengths with grouping and reporting."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw":{"emoji":"📐","os":["darwin","linux","win32"],"homepage":"https://datadrivenconstruction.io","requires":{"bins":["python3"],"anyBins":["IfcConvert","ifcopenshell"]}}}
---

# IFC Quantity Takeoff Extraction

Extract structured quantity data from BIM models (IFC, Revit) for cost estimation, material ordering, and progress tracking.

## Business Case

**Problem**: Manual quantity takeoff is:
- Time-consuming (40-80 hours for medium project)
- Error-prone (human counting mistakes)
- Not repeatable (changes require full rework)
- Disconnected from design (no live updates)

**Solution**: Automated QTO from BIM that:
- Extracts all quantities in minutes
- Groups by type, level, zone
- Updates instantly with model changes
- Exports to Excel for pricing

**ROI**: 90% reduction in QTO time, near-zero counting errors

## DDC Tools Used

```
┌──────────────────────────────────────────────────────────────────────┐
│                      QTO EXTRACTION PIPELINE                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   INPUT                 CONVERT                 ANALYZE               │
│   ┌─────────┐          ┌─────────┐            ┌─────────┐            │
│   │ .rvt    │          │ DDC     │            │ Python  │            │
│   │ .ifc    │─────────►│Converter│───────────►│ pandas  │            │
│   │ .dwg    │          │         │            │         │            │
│   └─────────┘          └─────────┘            └─────────┘            │
│                              │                      │                 │
│                              ▼                      ▼                 │
│                        ┌─────────┐            ┌─────────┐            │
│                        │ .xlsx   │            │ Grouped │            │
│                        │ raw data│            │ QTO     │            │
│                        └─────────┘            └─────────┘            │
│                                                    │                  │
│   OUTPUT                                           ▼                  │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  QTO Report                                                  │   │
│   │  • Element counts by type                                    │   │
│   │  • Areas (m², ft²)                                           │   │
│   │  • Volumes (m³, ft³)                                         │   │
│   │  • Lengths (m, ft)                                           │   │
│   │  • Weights (kg, tons)                                        │   │
│   │  • Grouped by level/zone/system                              │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## CLI Commands

### Revit to Excel (with BBox for volumes)

```bash
# Basic extraction
RvtExporter.exe "C:\Models\Building.rvt"

# Full extraction with bounding boxes (for volume calculations)
RvtExporter.exe "C:\Models\Building.rvt" complete bbox

# Include schedules (Revit's built-in QTO)
RvtExporter.exe "C:\Models\Building.rvt" complete bbox schedule
```

### IFC to Excel

```bash
# Extract IFC data
IfcExporter.exe "C:\Models\Building.ifc"

# Output: Building.xlsx with all IFC entities
```

### DWG to Excel (2D areas)

```bash
# Extract DWG blocks and areas
DwgExporter.exe "C:\Drawings\FloorPlan.dwg"
```

## Python Implementation

```python
import pandas as pd
import numpy as np
from pathlib import Path
import subprocess
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class QuantityItem:
    """Single quantity line item"""
    category: str
    type_name: str
    count: int
    area: float = 0.0
    volume: float = 0.0
    length: float = 0.0
    weight: float = 0.0
    unit_area: str = "m²"
    unit_volume: str = "m³"
    unit_length: str = "m"
    level: str = ""
    zone: str = ""


class BIMQuantityExtractor:
    """Extract quantities from BIM models using DDC converters"""

    def __init__(self, converter_path: str):
        self.converter_path = Path(converter_path)

    def convert_model(self, model_path: str, options: List[str] = None) -> Path:
        """Convert BIM model to Excel"""

        model = Path(model_path)
        options = options or ["complete", "bbox"]

        # Determine converter
        ext = model.suffix.lower()
        converters = {
            '.rvt': 'RvtExporter.exe',
            '.rfa': 'RvtExporter.exe',
            '.ifc': 'IfcExporter.exe',
            '.dwg': 'DwgExporter.exe',
            '.dgn': 'DgnExporter.exe'
        }

        converter = self.converter_path / converters.get(ext, 'RvtExporter.exe')

        # Build command
        cmd = [str(converter), str(model)] + options

        # Execute
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Conversion failed: {result.stderr}")

        # Return path to generated Excel
        xlsx_path = model.with_suffix('.xlsx')
        return xlsx_path

    def load_bim_data(self, xlsx_path: str) -> pd.DataFrame:
        """Load converted BIM data from Excel"""

        xlsx = Path(xlsx_path)
        if not xlsx.exists():
            raise FileNotFoundError(f"Excel file not found: {xlsx}")

        # Read main data sheet
        df = pd.read_excel(xlsx, sheet_name=0)

        # Clean column names
        df.columns = df.columns.str.strip()

        return df

    def extract_quantities(
        self,
        df: pd.DataFrame,
        group_by: str = "Type Name",
        include_categories: List[str] = None
    ) -> List[QuantityItem]:
        """Extract quantities grouped by type"""

        # Filter categories if specified
        if include_categories and 'Category' in df.columns:
            df = df[df['Category'].isin(include_categories)]

        # Group and aggregate
        quantities = []

        for (category, type_name), group in df.groupby(['Category', group_by]):
            item = QuantityItem(
                category=str(category),
                type_name=str(type_name),
                count=len(group)
            )

            # Extract area
            area_cols = ['Area', 'Surface Area', 'Gross Area', 'Net Area']
            for col in area_cols:
                if col in group.columns:
                    item.area = group[col].sum()
                    break

            # Extract volume
            vol_cols = ['Volume', 'Gross Volume', 'Net Volume']
            for col in vol_cols:
                if col in group.columns:
                    item.volume = group[col].sum()
                    break

            # Extract length
            len_cols = ['Length', 'Curve Length', 'Unconnected Height']
            for col in len_cols:
                if col in group.columns:
                    item.length = group[col].sum()
                    break

            # Extract level if available
            if 'Level' in group.columns:
                levels = group['Level'].dropna().unique()
                item.level = ', '.join(str(l) for l in levels)

            quantities.append(item)

        return quantities

    def extract_by_level(
        self,
        df: pd.DataFrame,
        group_by: str = "Type Name"
    ) -> Dict[str, List[QuantityItem]]:
        """Extract quantities grouped by level"""

        result = {}

        if 'Level' not in df.columns:
            result['All Levels'] = self.extract_quantities(df, group_by)
            return result

        for level, level_df in df.groupby('Level'):
            level_name = str(level) if pd.notna(level) else 'Unassigned'
            result[level_name] = self.extract_quantities(level_df, group_by)

        return result

    def calculate_concrete_quantities(self, df: pd.DataFrame) -> dict:
        """Calculate concrete quantities for typical elements"""

        concrete_categories = [
            'Floors', 'Structural Floors',
            'Walls', 'Structural Walls',
            'Structural Foundations', 'Foundation',
            'Structural Columns', 'Columns',
            'Structural Framing', 'Beams'
        ]

        concrete_df = df[df['Category'].isin(concrete_categories)]

        return {
            'total_volume_m3': concrete_df['Volume'].sum() if 'Volume' in concrete_df.columns else 0,
            'by_category': concrete_df.groupby('Category')['Volume'].sum().to_dict() if 'Volume' in concrete_df.columns else {},
            'element_count': len(concrete_df)
        }

    def calculate_wall_quantities(self, df: pd.DataFrame) -> dict:
        """Calculate wall quantities"""

        wall_categories = ['Walls', 'Basic Wall', 'Curtain Wall']
        walls = df[df['Category'].isin(wall_categories)]

        result = {
            'total_area_m2': 0,
            'total_length_m': 0,
            'by_type': {}
        }

        if 'Area' in walls.columns:
            result['total_area_m2'] = walls['Area'].sum()

        if 'Length' in walls.columns:
            result['total_length_m'] = walls['Length'].sum()

        if 'Type Name' in walls.columns:
            for type_name, group in walls.groupby('Type Name'):
                result['by_type'][type_name] = {
                    'count': len(group),
                    'area': group['Area'].sum() if 'Area' in group.columns else 0,
                    'length': group['Length'].sum() if 'Length' in group.columns else 0
                }

        return result

    def generate_qto_report(
        self,
        quantities: List[QuantityItem],
        output_path: str,
        project_name: str = "Project"
    ) -> str:
        """Generate QTO Excel report"""

        # Convert to DataFrame
        records = []
        for q in quantities:
            records.append({
                'Category': q.category,
                'Type': q.type_name,
                'Count': q.count,
                'Area (m²)': round(q.area, 2),
                'Volume (m³)': round(q.volume, 3),
                'Length (m)': round(q.length, 2),
                'Level': q.level
            })

        df = pd.DataFrame(records)

        # Sort by category and type
        df = df.sort_values(['Category', 'Type'])

        # Write to Excel with formatting
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary sheet
            summary = df.groupby('Category').agg({
                'Count': 'sum',
                'Area (m²)': 'sum',
                'Volume (m³)': 'sum',
                'Length (m)': 'sum'
            }).round(2)
            summary.to_excel(writer, sheet_name='Summary')

            # Detail sheet
            df.to_excel(writer, sheet_name='Detail', index=False)

            # By Level sheet
            if 'Level' in df.columns and df['Level'].notna().any():
                level_summary = df.groupby(['Level', 'Category']).agg({
                    'Count': 'sum',
                    'Area (m²)': 'sum',
                    'Volume (m³)': 'sum'
                }).round(2)
                level_summary.to_excel(writer, sheet_name='By Level')

        return output_path

    def generate_html_report(
        self,
        quantities: List[QuantityItem],
        output_path: str,
        project_name: str = "Project"
    ) -> str:
        """Generate interactive HTML QTO report"""

        # Group by category
        by_category = {}
        for q in quantities:
            if q.category not in by_category:
                by_category[q.category] = []
            by_category[q.category].append(q)

        # Calculate totals
        total_count = sum(q.count for q in quantities)
        total_area = sum(q.area for q in quantities)
        total_volume = sum(q.volume for q in quantities)

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>QTO Report - {project_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; margin-bottom: 20px; }}
        .summary {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .summary-card {{ background: #ecf0f1; padding: 15px; border-radius: 5px; flex: 1; }}
        .summary-card h3 {{ margin: 0 0 10px 0; color: #7f8c8d; font-size: 14px; }}
        .summary-card .value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        th {{ background: #34495e; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
        .category-header {{ background: #3498db; color: white; font-weight: bold; }}
        .number {{ text-align: right; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Quantity Takeoff Report</h1>
        <p>Project: {project_name}</p>
    </div>

    <div class="summary">
        <div class="summary-card">
            <h3>Total Elements</h3>
            <div class="value">{total_count:,}</div>
        </div>
        <div class="summary-card">
            <h3>Total Area</h3>
            <div class="value">{total_area:,.2f} m²</div>
        </div>
        <div class="summary-card">
            <h3>Total Volume</h3>
            <div class="value">{total_volume:,.3f} m³</div>
        </div>
        <div class="summary-card">
            <h3>Categories</h3>
            <div class="value">{len(by_category)}</div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Category / Type</th>
                <th class="number">Count</th>
                <th class="number">Area (m²)</th>
                <th class="number">Volume (m³)</th>
                <th class="number">Length (m)</th>
            </tr>
        </thead>
        <tbody>
"""

        for category, items in sorted(by_category.items()):
            cat_count = sum(i.count for i in items)
            cat_area = sum(i.area for i in items)
            cat_volume = sum(i.volume for i in items)

            html += f"""
            <tr class="category-header">
                <td>{category}</td>
                <td class="number">{cat_count:,}</td>
                <td class="number">{cat_area:,.2f}</td>
                <td class="number">{cat_volume:,.3f}</td>
                <td class="number">-</td>
            </tr>
"""
            for item in sorted(items, key=lambda x: x.type_name):
                html += f"""
            <tr>
                <td>&nbsp;&nbsp;&nbsp;{item.type_name}</td>
                <td class="number">{item.count:,}</td>
                <td class="number">{item.area:,.2f}</td>
                <td class="number">{item.volume:,.3f}</td>
                <td class="number">{item.length:,.2f}</td>
            </tr>
"""

        html += """
        </tbody>
    </table>
</body>
</html>
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path


# Usage Example
def extract_qto_from_model(
    model_path: str,
    converter_path: str,
    output_dir: str = None
) -> dict:
    """Complete QTO extraction workflow"""

    from datetime import datetime

    extractor = BIMQuantityExtractor(converter_path)

    # Convert model
    print(f"Converting: {model_path}")
    xlsx_path = extractor.convert_model(model_path, ["complete", "bbox"])

    # Load data
    print(f"Loading data from: {xlsx_path}")
    df = extractor.load_bim_data(xlsx_path)

    # Extract quantities
    quantities = extractor.extract_quantities(df)

    # Generate reports
    output_dir = output_dir or Path(model_path).parent
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    excel_path = Path(output_dir) / f"QTO_{timestamp}.xlsx"
    html_path = Path(output_dir) / f"QTO_{timestamp}.html"

    extractor.generate_qto_report(quantities, str(excel_path))
    extractor.generate_html_report(quantities, str(html_path))

    # Calculate specific quantities
    concrete = extractor.calculate_concrete_quantities(df)
    walls = extractor.calculate_wall_quantities(df)

    return {
        'excel_report': str(excel_path),
        'html_report': str(html_path),
        'summary': {
            'total_elements': len(df),
            'categories': df['Category'].nunique() if 'Category' in df.columns else 0,
            'types': df['Type Name'].nunique() if 'Type Name' in df.columns else 0
        },
        'concrete': concrete,
        'walls': walls
    }


if __name__ == "__main__":
    result = extract_qto_from_model(
        model_path=r"C:\Projects\Building.rvt",
        converter_path=r"C:\DDC\Converters",
        output_dir=r"C:\Projects\QTO"
    )

    print(f"Excel: {result['excel_report']}")
    print(f"HTML: {result['html_report']}")
    print(f"Concrete Volume: {result['concrete']['total_volume_m3']:.2f} m³")
```

## n8n Workflow Integration

```yaml
name: BIM QTO Extraction
trigger:
  type: webhook
  path: /qto-extract

steps:
  - convert_model:
      node: Execute Command
      command: |
        "C:\DDC\RvtExporter.exe" "{{$json.model_path}}" complete bbox schedule

  - load_excel:
      node: Spreadsheet File
      operation: read
      file: "={{$json.model_path.replace('.rvt', '.xlsx')}}"

  - group_quantities:
      node: Code
      code: |
        const grouped = {};
        items.forEach(item => {
          const type = item.json['Type Name'];
          if (!grouped[type]) {
            grouped[type] = {
              count: 0,
              area: 0,
              volume: 0
            };
          }
          grouped[type].count++;
          grouped[type].area += parseFloat(item.json['Area'] || 0);
          grouped[type].volume += parseFloat(item.json['Volume'] || 0);
        });
        return Object.entries(grouped).map(([type, data]) => ({
          type,
          ...data
        }));

  - generate_report:
      node: Code
      code: |
        // Generate HTML report
        return generateHTMLReport(items);

  - save_report:
      node: Write Binary File
      path: "={{$json.output_path}}"
```

## Best Practices

1. **Model Quality**: Ensure BIM model has proper levels and types assigned
2. **Units**: Verify model units match expected output units
3. **Categories**: Use consistent category naming for grouping
4. **Updates**: Re-run QTO after design changes
5. **Validation**: Cross-check totals against manual spot checks

## Common Quantity Formulas

```python
# Concrete formwork area (approximate)
formwork_area = concrete_volume * 6  # m² per m³ of concrete

# Rebar quantity (approximate)
rebar_weight = concrete_volume * 100  # kg per m³ (typical)

# Paint area from wall area
paint_area = wall_area * 2  # both sides

# Ceiling area from floor area
ceiling_area = floor_area * 0.95  # typical ratio
```

---

*"Measure twice, cut once. Or better yet, measure automatically from the model."*
