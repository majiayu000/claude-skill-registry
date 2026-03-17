---
name: "excel-to-bim"
description: "Push Excel data back to BIM models. Update parameters, properties, and attributes from structured spreadsheets."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📄", "os": ["win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"], "anyBins": ["ifcopenshell"]}}}
---
# Excel to BIM Update

## Business Case

### Problem Statement
After extracting BIM data to Excel and enriching it (cost codes, classifications, custom data):
- Changes need to flow back to the BIM model
- Manual re-entry is error-prone
- Updates must match by element ID

### Solution
Push Excel data back to BIM models, updating element parameters and properties from spreadsheet changes.

### Business Value
- **Bi-directional workflow** - BIM → Excel → BIM
- **Bulk updates** - Change thousands of parameters
- **Data enrichment** - Add classifications, codes, costs
- **Consistency** - Spreadsheet as single source of truth

## Technical Implementation

### Workflow
```
BIM Model (Revit/IFC) → Excel Export → Data Enrichment → Excel Update → BIM Model
```

### Python Implementation

```python
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json


class UpdateType(Enum):
    """Type of BIM parameter update."""
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ELEMENT_ID = "element_id"


@dataclass
class ParameterMapping:
    """Mapping between Excel column and BIM parameter."""
    excel_column: str
    bim_parameter: str
    update_type: UpdateType
    transform: Optional[str] = None  # Optional transformation


@dataclass
class UpdateResult:
    """Result of single element update."""
    element_id: str
    parameters_updated: List[str]
    success: bool
    error: Optional[str] = None


@dataclass
class BatchUpdateResult:
    """Result of batch update operation."""
    total_elements: int
    updated: int
    failed: int
    skipped: int
    results: List[UpdateResult]


class ExcelToBIMUpdater:
    """Update BIM models from Excel data."""

    # Standard ID column names
    ID_COLUMNS = ['ElementId', 'GlobalId', 'GUID', 'Id', 'UniqueId']

    def __init__(self):
        self.mappings: List[ParameterMapping] = []

    def add_mapping(self, excel_col: str, bim_param: str,
                    update_type: UpdateType = UpdateType.TEXT):
        """Add column to parameter mapping."""
        self.mappings.append(ParameterMapping(
            excel_column=excel_col,
            bim_parameter=bim_param,
            update_type=update_type
        ))

    def load_excel(self, file_path: str,
                   sheet_name: str = None) -> pd.DataFrame:
        """Load Excel data for update."""
        if sheet_name:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        return pd.read_excel(file_path)

    def detect_id_column(self, df: pd.DataFrame) -> Optional[str]:
        """Detect element ID column in DataFrame."""
        for col in self.ID_COLUMNS:
            if col in df.columns:
                return col
            # Case-insensitive check
            for df_col in df.columns:
                if df_col.lower() == col.lower():
                    return df_col
        return None

    def prepare_updates(self, df: pd.DataFrame,
                        id_column: str = None) -> List[Dict[str, Any]]:
        """Prepare update instructions from DataFrame."""

        if id_column is None:
            id_column = self.detect_id_column(df)
            if id_column is None:
                raise ValueError("Cannot detect ID column")

        updates = []

        for _, row in df.iterrows():
            element_id = str(row[id_column])

            params = {}
            for mapping in self.mappings:
                if mapping.excel_column in df.columns:
                    value = row[mapping.excel_column]

                    # Convert value based on type
                    if mapping.update_type == UpdateType.NUMBER:
                        value = float(value) if pd.notna(value) else 0
                    elif mapping.update_type == UpdateType.BOOLEAN:
                        value = bool(value) if pd.notna(value) else False
                    elif mapping.update_type == UpdateType.TEXT:
                        value = str(value) if pd.notna(value) else ""

                    params[mapping.bim_parameter] = value

            if params:
                updates.append({
                    'element_id': element_id,
                    'parameters': params
                })

        return updates

    def generate_dynamo_script(self, updates: List[Dict],
                               output_path: str) -> str:
        """Generate Dynamo script for Revit updates."""

        # Generate Python code for Dynamo
        script = '''
# Dynamo Python Script for Revit Parameter Updates
# Generated by DDC Excel-to-BIM

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

# Update data
updates = '''
        script += json.dumps(updates, indent=2)
        script += '''

# Apply updates
TransactionManager.Instance.EnsureInTransaction(doc)

results = []
for update in updates:
    try:
        element_id = int(update['element_id'])
        element = doc.GetElement(ElementId(element_id))

        if element:
            for param_name, value in update['parameters'].items():
                param = element.LookupParameter(param_name)
                if param and not param.IsReadOnly:
                    if isinstance(value, (int, float)):
                        param.Set(float(value))
                    elif isinstance(value, bool):
                        param.Set(1 if value else 0)
                    else:
                        param.Set(str(value))
            results.append({'id': element_id, 'status': 'success'})
        else:
            results.append({'id': element_id, 'status': 'not found'})
    except Exception as e:
        results.append({'id': update['element_id'], 'status': str(e)})

TransactionManager.Instance.TransactionTaskDone()

OUT = results
'''

        with open(output_path, 'w') as f:
            f.write(script)

        return output_path

    def generate_ifc_updates(self, updates: List[Dict],
                             original_ifc: str,
                             output_ifc: str) -> str:
        """Generate updated IFC file (requires IfcOpenShell)."""

        try:
            import ifcopenshell
        except ImportError:
            raise ImportError("IfcOpenShell required for IFC updates")

        ifc = ifcopenshell.open(original_ifc)

        for update in updates:
            guid = update['element_id']

            # Find element by GUID
            element = ifc.by_guid(guid)
            if not element:
                continue

            # Update properties
            for param_name, value in update['parameters'].items():
                # This is simplified - actual IFC property handling is more complex
                # Would need to find/create property sets and properties
                pass

        ifc.write(output_ifc)
        return output_ifc

    def generate_update_report(self, original_df: pd.DataFrame,
                               updates: List[Dict],
                               output_path: str) -> str:
        """Generate report of planned updates."""

        report_data = []
        for update in updates:
            for param, value in update['parameters'].items():
                report_data.append({
                    'element_id': update['element_id'],
                    'parameter': param,
                    'new_value': value
                })

        report_df = pd.DataFrame(report_data)
        report_df.to_excel(output_path, index=False)
        return output_path


class RevitExcelUpdater(ExcelToBIMUpdater):
    """Specialized updater for Revit via ImportExcelToRevit."""

    def __init__(self, tool_path: str = "ImportExcelToRevit.exe"):
        super().__init__()
        self.tool_path = Path(tool_path)

    def update_revit(self, excel_file: str,
                     rvt_file: str,
                     sheet_name: str = "Elements") -> BatchUpdateResult:
        """Update Revit file from Excel using CLI tool."""

        import subprocess

        # This assumes ImportExcelToRevit CLI tool
        cmd = [
            str(self.tool_path),
            rvt_file,
            excel_file,
            sheet_name
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Parse results (format depends on tool output)
        if result.returncode == 0:
            return BatchUpdateResult(
                total_elements=0,  # Would parse from output
                updated=0,
                failed=0,
                skipped=0,
                results=[]
            )
        else:
            raise RuntimeError(f"Update failed: {result.stderr}")


class DataEnrichmentWorkflow:
    """Complete workflow for data enrichment and update."""

    def __init__(self):
        self.updater = ExcelToBIMUpdater()

    def enrich_and_update(self, original_excel: str,
                          enrichment_excel: str,
                          merge_column: str) -> pd.DataFrame:
        """Merge enrichment data with original export."""

        original = pd.read_excel(original_excel)
        enrichment = pd.read_excel(enrichment_excel)

        # Merge on specified column
        merged = original.merge(enrichment, on=merge_column, how='left',
                                suffixes=('', '_enriched'))

        return merged

    def create_classification_mapping(self, df: pd.DataFrame,
                                      type_column: str,
                                      classification_file: str) -> pd.DataFrame:
        """Map BIM types to classification codes."""

        classifications = pd.read_excel(classification_file)

        # Fuzzy matching could be added here
        merged = df.merge(classifications,
                          left_on=type_column,
                          right_on='type_description',
                          how='left')

        return merged
```

## Quick Start

```python
# Initialize updater
updater = ExcelToBIMUpdater()

# Define mappings
updater.add_mapping('Classification_Code', 'OmniClassCode', UpdateType.TEXT)
updater.add_mapping('Unit_Cost', 'Cost', UpdateType.NUMBER)

# Load enriched Excel
df = updater.load_excel("enriched_model.xlsx")

# Prepare updates
updates = updater.prepare_updates(df)
print(f"Prepared {len(updates)} updates")

# Generate Dynamo script for Revit
updater.generate_dynamo_script(updates, "update_parameters.py")
```

## Common Use Cases

### 1. Add Classification Codes
```python
updater = ExcelToBIMUpdater()
updater.add_mapping('Omniclass', 'OmniClass_Number', UpdateType.TEXT)
updater.add_mapping('Uniclass', 'Uniclass_Code', UpdateType.TEXT)

df = updater.load_excel("classified_elements.xlsx")
updates = updater.prepare_updates(df)
```

### 2. Cost Data Integration
```python
updater.add_mapping('Material_Cost', 'Pset_MaterialCost', UpdateType.NUMBER)
updater.add_mapping('Labor_Cost', 'Pset_LaborCost', UpdateType.NUMBER)
```

### 3. Generate Update Report
```python
report = updater.generate_update_report(df, updates, "planned_updates.xlsx")
```

## Integration with DDC Pipeline

```python
# Full round-trip: Revit → Excel → Enrich → Update → Revit

# 1. Export from Revit
# RvtExporter.exe model.rvt complete

# 2. Enrich in Python/Excel
df = pd.read_excel("model.xlsx")
# Add classifications, costs, etc.
df['OmniClass'] = df['Type Name'].map(classification_dict)
df.to_excel("enriched_model.xlsx")

# 3. Generate update script
updater = ExcelToBIMUpdater()
updater.add_mapping('OmniClass', 'OmniClass_Number')
updates = updater.prepare_updates(df)
updater.generate_dynamo_script(updates, "apply_updates.py")

# 4. Run in Dynamo to update Revit
```

## Resources
- **GitHub**: [DDC Update Revit from Excel](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto/tree/main/DDC_Update_Revit_from_Excel)
- **DDC Book**: Chapter 2.4 - Bidirectional Data Flow
