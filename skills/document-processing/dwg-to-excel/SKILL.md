---
name: dwg-to-excel
description: "Convert AutoCAD DWG files (1983-2026) to Excel databases using DwgExporter CLI. Extract layers, blocks, attributes, and geometry data without Autodesk licenses."
---

# DWG to Excel Conversion

## Business Case

### Problem Statement
AutoCAD DWG files contain valuable project data locked in proprietary format:
- Layer structures with drawing organization
- Block references with attribute data
- Text annotations and dimensions
- Geometric entities (lines, polylines, arcs)
- External references (xrefs)

Extracting this data typically requires AutoCAD licenses or complex programming.

### Solution
DwgExporter.exe converts DWG files to structured Excel databases offline, without Autodesk licenses.

### Business Value
- **Zero license cost** - No AutoCAD license required
- **Legacy support** - Reads DWG files from 1983 to 2026
- **Data extraction** - Layers, blocks, attributes, text, geometry
- **PDF export** - Generate drawings from DWG layouts
- **Batch processing** - Convert thousands of DWG files

## Technical Implementation

### CLI Syntax
```bash
DwgExporter.exe <input_dwg> [options]
```

### Output Formats
| Output | Description |
|--------|-------------|
| `.xlsx` | Excel database with all entities |
| `.pdf` | PDF drawings from layouts |

### Supported Versions
| Version Range | Description |
|---------------|-------------|
| R12 (1992) | Legacy DWG |
| R14 (1997) | AutoCAD 14 |
| 2000-2002 | DWG 2000 format |
| 2004-2006 | DWG 2004 format |
| 2007-2009 | DWG 2007 format |
| 2010-2012 | DWG 2010 format |
| 2013-2017 | DWG 2013 format |
| 2018-2026 | DWG 2018 format |

### Examples

```bash
# Basic conversion
DwgExporter.exe "C:\Projects\FloorPlan.dwg"

# Export with PDF drawings
DwgExporter.exe "C:\Projects\FloorPlan.dwg" sheets2pdf

# Batch processing all DWG in folder
for /R "C:\Projects" %f in (*.dwg) do DwgExporter.exe "%f"

# PowerShell batch conversion
Get-ChildItem "C:\Projects\*.dwg" -Recurse | ForEach-Object {
    & "C:\DDC\DwgExporter.exe" $_.FullName
}
```

### Python Integration

```python
import subprocess
import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class DWGEntityType(Enum):
    """DWG entity types."""
    LINE = "LINE"
    POLYLINE = "POLYLINE"
    LWPOLYLINE = "LWPOLYLINE"
    CIRCLE = "CIRCLE"
    ARC = "ARC"
    ELLIPSE = "ELLIPSE"
    SPLINE = "SPLINE"
    TEXT = "TEXT"
    MTEXT = "MTEXT"
    DIMENSION = "DIMENSION"
    INSERT = "INSERT"  # Block reference
    HATCH = "HATCH"
    SOLID = "SOLID"
    POINT = "POINT"
    ATTRIB = "ATTRIB"
    ATTDEF = "ATTDEF"


@dataclass
class DWGEntity:
    """Represents a DWG entity."""
    handle: str
    entity_type: str
    layer: str
    color: int
    linetype: str
    lineweight: float

    # Geometry (depends on entity type)
    start_x: Optional[float] = None
    start_y: Optional[float] = None
    end_x: Optional[float] = None
    end_y: Optional[float] = None

    # Block reference data
    block_name: Optional[str] = None
    rotation: Optional[float] = None
    scale_x: Optional[float] = None
    scale_y: Optional[float] = None

    # Text data
    text_content: Optional[str] = None
    text_height: Optional[float] = None


@dataclass
class DWGBlock:
    """Represents a DWG block definition."""
    name: str
    base_point_x: float
    base_point_y: float
    entity_count: int
    is_dynamic: bool
    attributes: List[str]


@dataclass
class DWGLayer:
    """Represents a DWG layer."""
    name: str
    color: int
    linetype: str
    is_on: bool
    is_frozen: bool
    is_locked: bool
    lineweight: float
    entity_count: int


class DWGExporter:
    """DWG to Excel converter using DDC DwgExporter CLI."""

    def __init__(self, exporter_path: str = "DwgExporter.exe"):
        self.exporter = Path(exporter_path)
        if not self.exporter.exists():
            raise FileNotFoundError(f"DwgExporter not found: {exporter_path}")

    def convert(self, dwg_file: str,
                export_pdf: bool = False) -> Path:
        """Convert DWG file to Excel."""
        dwg_path = Path(dwg_file)
        if not dwg_path.exists():
            raise FileNotFoundError(f"DWG file not found: {dwg_file}")

        cmd = [str(self.exporter), str(dwg_path)]
        if export_pdf:
            cmd.append("sheets2pdf")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Export failed: {result.stderr}")

        # Output file is same name with .xlsx extension
        return dwg_path.with_suffix('.xlsx')

    def batch_convert(self, folder: str,
                      include_subfolders: bool = True,
                      export_pdf: bool = False) -> List[Dict[str, Any]]:
        """Convert all DWG files in folder."""
        folder_path = Path(folder)
        pattern = "**/*.dwg" if include_subfolders else "*.dwg"

        results = []
        for dwg_file in folder_path.glob(pattern):
            try:
                output = self.convert(str(dwg_file), export_pdf)
                results.append({
                    'input': str(dwg_file),
                    'output': str(output),
                    'status': 'success'
                })
                print(f"✓ Converted: {dwg_file.name}")
            except Exception as e:
                results.append({
                    'input': str(dwg_file),
                    'output': None,
                    'status': 'failed',
                    'error': str(e)
                })
                print(f"✗ Failed: {dwg_file.name} - {e}")

        return results

    def read_entities(self, xlsx_file: str) -> pd.DataFrame:
        """Read converted Excel as DataFrame."""
        xlsx_path = Path(xlsx_file)
        if not xlsx_path.exists():
            raise FileNotFoundError(f"Excel file not found: {xlsx_file}")

        return pd.read_excel(xlsx_file, sheet_name="Elements")

    def get_layers(self, xlsx_file: str) -> pd.DataFrame:
        """Get layer summary from converted file."""
        df = self.read_entities(xlsx_file)

        if 'Layer' not in df.columns:
            raise ValueError("Layer column not found in data")

        summary = df.groupby('Layer').agg({
            'Handle': 'count'
        }).reset_index()
        summary.columns = ['Layer', 'Entity_Count']
        return summary.sort_values('Entity_Count', ascending=False)

    def get_blocks(self, xlsx_file: str) -> pd.DataFrame:
        """Get block reference summary."""
        df = self.read_entities(xlsx_file)

        # Filter to INSERT entities (block references)
        blocks = df[df['EntityType'] == 'INSERT']

        if blocks.empty:
            return pd.DataFrame(columns=['Block_Name', 'Count'])

        summary = blocks.groupby('BlockName').agg({
            'Handle': 'count'
        }).reset_index()
        summary.columns = ['Block_Name', 'Count']
        return summary.sort_values('Count', ascending=False)

    def get_text_content(self, xlsx_file: str) -> pd.DataFrame:
        """Extract all text content from DWG."""
        df = self.read_entities(xlsx_file)

        # Filter to text entities
        text_types = ['TEXT', 'MTEXT', 'ATTRIB']
        texts = df[df['EntityType'].isin(text_types)]

        if 'TextContent' in texts.columns:
            return texts[['Handle', 'EntityType', 'Layer', 'TextContent']].copy()
        return texts[['Handle', 'EntityType', 'Layer']].copy()

    def get_entity_statistics(self, xlsx_file: str) -> Dict[str, int]:
        """Get entity type statistics."""
        df = self.read_entities(xlsx_file)

        if 'EntityType' not in df.columns:
            return {}

        return df['EntityType'].value_counts().to_dict()

    def extract_block_attributes(self, xlsx_file: str,
                                  block_name: str) -> pd.DataFrame:
        """Extract attributes from specific block type."""
        df = self.read_entities(xlsx_file)

        # Find block references
        blocks = df[(df['EntityType'] == 'INSERT') &
                    (df['BlockName'] == block_name)]

        # Find associated attributes
        # Attributes typically follow their parent INSERT in handle order
        result_data = []

        for _, block in blocks.iterrows():
            block_handle = block['Handle']
            block_data = {
                'Block_Handle': block_handle,
                'X': block.get('InsertX', 0),
                'Y': block.get('InsertY', 0),
                'Rotation': block.get('Rotation', 0)
            }

            # Add any attribute columns
            for col in df.columns:
                if col.startswith('Attr_'):
                    block_data[col] = block.get(col)

            result_data.append(block_data)

        return pd.DataFrame(result_data)


class DWGAnalyzer:
    """Advanced DWG analysis tools."""

    def __init__(self, exporter: DWGExporter):
        self.exporter = exporter

    def analyze_drawing_structure(self, dwg_file: str) -> Dict[str, Any]:
        """Analyze complete drawing structure."""
        xlsx = self.exporter.convert(dwg_file)
        df = self.exporter.read_entities(str(xlsx))

        analysis = {
            'file': dwg_file,
            'total_entities': len(df),
            'layers': self.exporter.get_layers(str(xlsx)).to_dict('records'),
            'entity_types': self.exporter.get_entity_statistics(str(xlsx)),
            'blocks': self.exporter.get_blocks(str(xlsx)).to_dict('records')
        }

        # Calculate extents if coordinates available
        if 'X' in df.columns and 'Y' in df.columns:
            analysis['extents'] = {
                'min_x': df['X'].min(),
                'max_x': df['X'].max(),
                'min_y': df['Y'].min(),
                'max_y': df['Y'].max()
            }

        return analysis

    def compare_drawings(self, dwg1: str, dwg2: str) -> Dict[str, Any]:
        """Compare two DWG files."""
        xlsx1 = self.exporter.convert(dwg1)
        xlsx2 = self.exporter.convert(dwg2)

        df1 = self.exporter.read_entities(str(xlsx1))
        df2 = self.exporter.read_entities(str(xlsx2))

        layers1 = set(df1['Layer'].unique()) if 'Layer' in df1.columns else set()
        layers2 = set(df2['Layer'].unique()) if 'Layer' in df2.columns else set()

        return {
            'file1': dwg1,
            'file2': dwg2,
            'entity_count_diff': len(df2) - len(df1),
            'layers_added': list(layers2 - layers1),
            'layers_removed': list(layers1 - layers2),
            'common_layers': list(layers1 & layers2)
        }

    def find_duplicates(self, xlsx_file: str,
                        tolerance: float = 0.001) -> pd.DataFrame:
        """Find duplicate entities at same location."""
        df = self.exporter.read_entities(xlsx_file)

        if 'X' not in df.columns or 'Y' not in df.columns:
            return pd.DataFrame()

        # Round coordinates for grouping
        df['X_rounded'] = (df['X'] / tolerance).round() * tolerance
        df['Y_rounded'] = (df['Y'] / tolerance).round() * tolerance

        # Find duplicates
        duplicates = df[df.duplicated(
            subset=['EntityType', 'Layer', 'X_rounded', 'Y_rounded'],
            keep=False
        )]

        return duplicates.sort_values(['X_rounded', 'Y_rounded'])


# Convenience functions
def convert_dwg_to_excel(dwg_file: str,
                         exporter_path: str = "DwgExporter.exe") -> str:
    """Quick conversion of DWG to Excel."""
    exporter = DWGExporter(exporter_path)
    output = exporter.convert(dwg_file)
    return str(output)


def batch_convert_dwg(folder: str,
                      exporter_path: str = "DwgExporter.exe",
                      include_subfolders: bool = True) -> List[str]:
    """Batch convert all DWG files in folder."""
    exporter = DWGExporter(exporter_path)
    results = exporter.batch_convert(folder, include_subfolders)
    return [r['output'] for r in results if r['status'] == 'success']
```

## Output Structure

### Excel Sheets
| Sheet | Content |
|-------|---------|
| Elements | All DWG entities with properties |
| Layers | Layer definitions |
| Blocks | Block definitions |
| Layouts | Drawing layouts/sheets |

### Entity Columns
| Column | Type | Description |
|--------|------|-------------|
| Handle | string | Unique entity handle |
| EntityType | string | LINE, CIRCLE, INSERT, etc. |
| Layer | string | Layer name |
| Color | int | Color index (0-256) |
| Linetype | string | Linetype name |
| Lineweight | float | Line weight in mm |
| X, Y, Z | float | Entity coordinates |
| BlockName | string | For INSERT entities |
| TextContent | string | For TEXT/MTEXT |

## Quick Start

```python
# Initialize exporter
exporter = DWGExporter("C:/DDC/DwgExporter.exe")

# Convert single file
xlsx = exporter.convert("C:/Projects/Plan.dwg")
print(f"Output: {xlsx}")

# Read and analyze
df = exporter.read_entities(str(xlsx))
print(f"Total entities: {len(df)}")

# Get layer statistics
layers = exporter.get_layers(str(xlsx))
print(layers)

# Get block usage
blocks = exporter.get_blocks(str(xlsx))
print(blocks)

# Extract text annotations
texts = exporter.get_text_content(str(xlsx))
for _, row in texts.iterrows():
    print(f"{row['Layer']}: {row.get('TextContent', 'N/A')}")
```

## Common Use Cases

### 1. Layer Audit
```python
exporter = DWGExporter()
xlsx = exporter.convert("drawing.dwg")
layers = exporter.get_layers(str(xlsx))

# Check for non-standard layers
standard_layers = ['0', 'WALLS', 'DOORS', 'WINDOWS', 'DIMENSIONS']
non_standard = layers[~layers['Layer'].isin(standard_layers)]
print("Non-standard layers:", non_standard['Layer'].tolist())
```

### 2. Block Schedule
```python
# Extract all door blocks with attributes
doors = exporter.extract_block_attributes(str(xlsx), "DOOR")
print(doors[['Block_Handle', 'Attr_DOOR_TYPE', 'Attr_DOOR_SIZE']])
```

### 3. Drawing Comparison
```python
analyzer = DWGAnalyzer(exporter)
diff = analyzer.compare_drawings("rev1.dwg", "rev2.dwg")
print(f"Entities added: {diff['entity_count_diff']}")
print(f"New layers: {diff['layers_added']}")
```

## Integration with DDC Pipeline

```python
# Full pipeline: DWG → Excel → Analysis → Report
from dwg_exporter import DWGExporter, DWGAnalyzer

# 1. Convert DWG
exporter = DWGExporter("C:/DDC/DwgExporter.exe")
xlsx = exporter.convert("project.dwg")

# 2. Analyze structure
analyzer = DWGAnalyzer(exporter)
analysis = analyzer.analyze_drawing_structure("project.dwg")

# 3. Generate report
print(f"Drawing: {analysis['file']}")
print(f"Entities: {analysis['total_entities']}")
print(f"Layers: {len(analysis['layers'])}")
print(f"Blocks: {len(analysis['blocks'])}")
```

## Best Practices

1. **Check DWG version** - Older files may have limited data
2. **Validate layer structure** - Clean up before processing
3. **Handle external references** - Bind xrefs if needed
4. **Batch overnight** - Large files take time
5. **Verify entity counts** - Compare with AutoCAD if possible

## Resources

- **GitHub**: [cad2data Pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto)
- **Video Tutorial**: [DWG to Excel Pipeline](https://www.youtube.com/watch?v=jVU7vlMNTO0)
- **DDC Book**: Chapter 2.4 - CAD Data Extraction
