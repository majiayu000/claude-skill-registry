---
name: rvt-to-excel
description: "Convert RVT/RFA files to Excel databases. Extract BIM element data, properties, and quantities."
---

# RVT to Excel Conversion

## Business Case

### Problem Statement
BIM data inside RVT files needs to be extracted for:
- Processing multiple projects in batch
- Integrating BIM data with analytics pipelines
- Sharing structured data with stakeholders
- Generating reports and quantity takeoffs

### Solution
Convert RVT files to structured Excel databases for analysis and reporting.

### Business Value
- **Batch processing** - Convert multiple projects
- **Data accessibility** - Excel format for universal access
- **Pipeline integration** - Feed data to BI tools, ML models
- **Structured output** - Organized element data and properties

## Technical Implementation

### CLI Syntax
```bash
RvtExporter.exe <input_path> [export_mode] [options]
```

### Export Modes
| Mode | Categories | Description |
|------|-----------|-------------|
| `basic` | 309 | Essential structural elements |
| `standard` | 724 | Standard BIM categories |
| `complete` | 1209 | All Revit categories |
| `custom` | User-defined | Specific categories only |

### Options
| Option | Description |
|--------|-------------|
| `bbox` | Include bounding box coordinates |
| `rooms` | Include room associations |
| `schedules` | Export all schedules to sheets |
| `sheets` | Export sheets to PDF |

### Examples

```bash
# Basic export
RvtExporter.exe "C:\Projects\Building.rvt" basic

# Complete with bounding boxes
RvtExporter.exe "C:\Projects\Building.rvt" complete bbox

# Full export with all options
RvtExporter.exe "C:\Projects\Building.rvt" complete bbox rooms schedules sheets

# Batch processing
for /R "C:\Projects" %f in (*.rvt) do RvtExporter.exe "%f" standard bbox
```

### Python Integration

```python
import subprocess
import pandas as pd
from pathlib import Path
from typing import List, Optional

class RevitExporter:
    def __init__(self, exporter_path: str = "RvtExporter.exe"):
        self.exporter = Path(exporter_path)
        if not self.exporter.exists():
            raise FileNotFoundError(f"RvtExporter not found: {exporter_path}")

    def convert(self, rvt_file: str, mode: str = "complete",
                options: List[str] = None) -> Path:
        """Convert Revit file to Excel."""
        rvt_path = Path(rvt_file)
        if not rvt_path.exists():
            raise FileNotFoundError(f"Revit file not found: {rvt_file}")

        cmd = [str(self.exporter), str(rvt_path), mode]
        if options:
            cmd.extend(options)

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Export failed: {result.stderr}")

        # Output file is same name with .xlsx extension
        output_file = rvt_path.with_suffix('.xlsx')
        return output_file

    def batch_convert(self, folder: str, mode: str = "standard",
                      pattern: str = "*.rvt") -> List[Path]:
        """Convert all Revit files in folder."""
        folder_path = Path(folder)
        converted = []

        for rvt_file in folder_path.glob(pattern):
            try:
                output = self.convert(str(rvt_file), mode)
                converted.append(output)
                print(f"Converted: {rvt_file.name}")
            except Exception as e:
                print(f"Failed: {rvt_file.name} - {e}")

        return converted

    def read_elements(self, xlsx_file: str) -> pd.DataFrame:
        """Read converted Excel as DataFrame."""
        return pd.read_excel(xlsx_file, sheet_name="Elements")

    def get_quantities(self, xlsx_file: str,
                       group_by: str = "Category") -> pd.DataFrame:
        """Get quantity summary grouped by category."""
        df = self.read_elements(xlsx_file)

        # Group and count
        summary = df.groupby(group_by).agg({
            'ElementId': 'count',
            'Area': 'sum',
            'Volume': 'sum'
        }).reset_index()

        summary.columns = [group_by, 'Count', 'Total_Area', 'Total_Volume']
        return summary
```

## Output Structure

### Excel Sheets
| Sheet | Content |
|-------|---------|
| Elements | All BIM elements with properties |
| Categories | Element categories summary |
| Levels | Building levels |
| Materials | Material definitions |
| Parameters | Shared parameters |

### Element Columns
| Column | Type | Description |
|--------|------|-------------|
| ElementId | int | Unique Revit ID |
| Category | string | Element category |
| Family | string | Family name |
| Type | string | Type name |
| Level | string | Associated level |
| Area | float | Surface area (m²) |
| Volume | float | Volume (m³) |
| BBox_MinX/Y/Z | float | Bounding box min |
| BBox_MaxX/Y/Z | float | Bounding box max |

## Usage Example

```python
# Initialize exporter
exporter = RevitExporter("C:/Tools/RvtExporter.exe")

# Convert single file
xlsx = exporter.convert("C:/Projects/Office.rvt", "complete", ["bbox", "rooms"])

# Read and analyze
df = exporter.read_elements(str(xlsx))
print(f"Total elements: {len(df)}")

# Quantity summary
quantities = exporter.get_quantities(str(xlsx))
print(quantities)

# Export to CSV for further processing
df.to_csv("elements.csv", index=False)
```

## Integration with DDC Pipeline

```python
# Full pipeline: Revit → Excel → Cost Estimate
from semantic_search import CWICRSemanticSearch

# 1. Convert Revit
exporter = RevitExporter()
xlsx = exporter.convert("project.rvt", "complete", ["bbox"])

# 2. Extract quantities
df = exporter.read_elements(str(xlsx))
quantities = df.groupby('Category')['Volume'].sum().to_dict()

# 3. Search CWICR for pricing
search = CWICRSemanticSearch()
costs = {}
for category, volume in quantities.items():
    results = search.search_work_items(category, limit=5)
    if not results.empty:
        avg_price = results['unit_price'].mean()
        costs[category] = volume * avg_price

print(f"Total estimate: ${sum(costs.values()):,.2f}")
```

## Best Practices

1. **Use appropriate mode** - `basic` for quick analysis, `complete` for full data
2. **Include bbox** - Required for spatial analysis and visualization
3. **Batch carefully** - Large files may take time; process overnight
4. **Validate output** - Check element counts against Revit schedules

## Resources

- **GitHub**: [cad2data Pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto)
- **Download**: See repository releases for RvtExporter.exe
