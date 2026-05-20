---
slug: "erp-data-extractor"
display_name: "Erp Data Extractor"
description: "Extract and analyze data from construction ERP systems. Pull project data for analytics, reporting, and integration."
---

# ERP Data Extractor

## Business Case

### Problem Statement
ERP data extraction challenges:
- Complex database structures
- Multiple interconnected modules
- Data transformation needs
- Integration with analytics

### Solution
Structured extraction and transformation of construction ERP data for analytics, reporting, and cross-system integration.

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
import json


class ERPModule(Enum):
    PROJECT = "project"
    COST = "cost"
    PROCUREMENT = "procurement"
    INVENTORY = "inventory"
    HR = "hr"
    EQUIPMENT = "equipment"
    SUBCONTRACT = "subcontract"
    BILLING = "billing"


@dataclass
class DataSource:
    name: str
    module: ERPModule
    table_name: str
    columns: List[str]
    filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedData:
    source: str
    module: ERPModule
    data: pd.DataFrame
    extracted_at: datetime
    record_count: int


class ERPDataExtractor:
    """Extract and transform data from construction ERP systems."""

    def __init__(self, erp_name: str = "Generic"):
        self.erp_name = erp_name
        self.data_sources: List[DataSource] = []
        self.extracted_data: Dict[str, ExtractedData] = {}
        self._connection = None

    def add_data_source(self, source: DataSource):
        """Add data source for extraction."""
        self.data_sources.append(source)

    def define_project_extraction(self):
        """Define standard project data extraction."""

        self.add_data_source(DataSource(
            name="projects",
            module=ERPModule.PROJECT,
            table_name="projects",
            columns=["id", "code", "name", "status", "start_date", "end_date", "budget", "client_id"]
        ))

        self.add_data_source(DataSource(
            name="project_phases",
            module=ERPModule.PROJECT,
            table_name="project_phases",
            columns=["id", "project_id", "phase_name", "start_date", "end_date", "status"]
        ))

    def define_cost_extraction(self):
        """Define standard cost data extraction."""

        self.add_data_source(DataSource(
            name="cost_items",
            module=ERPModule.COST,
            table_name="cost_items",
            columns=["id", "project_id", "wbs_code", "description", "budgeted", "actual", "committed"]
        ))

        self.add_data_source(DataSource(
            name="cost_transactions",
            module=ERPModule.COST,
            table_name="cost_transactions",
            columns=["id", "project_id", "cost_item_id", "amount", "transaction_date", "type"]
        ))

    def define_procurement_extraction(self):
        """Define procurement data extraction."""

        self.add_data_source(DataSource(
            name="purchase_orders",
            module=ERPModule.PROCUREMENT,
            table_name="purchase_orders",
            columns=["id", "project_id", "vendor_id", "amount", "status", "order_date", "delivery_date"]
        ))

        self.add_data_source(DataSource(
            name="vendors",
            module=ERPModule.PROCUREMENT,
            table_name="vendors",
            columns=["id", "name", "category", "rating", "status"]
        ))

    def extract_from_dataframe(self, source_name: str, df: pd.DataFrame):
        """Extract data from DataFrame (simulating ERP extraction)."""

        source = next((s for s in self.data_sources if s.name == source_name), None)
        if not source:
            return None

        # Apply column selection
        available_cols = [c for c in source.columns if c in df.columns]
        extracted = df[available_cols].copy()

        # Apply filters
        for col, value in source.filters.items():
            if col in extracted.columns:
                extracted = extracted[extracted[col] == value]

        self.extracted_data[source_name] = ExtractedData(
            source=source_name,
            module=source.module,
            data=extracted,
            extracted_at=datetime.now(),
            record_count=len(extracted)
        )

        return self.extracted_data[source_name]

    def transform_data(self, source_name: str,
                       transformations: List[Dict[str, Any]]) -> pd.DataFrame:
        """Apply transformations to extracted data."""

        if source_name not in self.extracted_data:
            return pd.DataFrame()

        df = self.extracted_data[source_name].data.copy()

        for transform in transformations:
            action = transform.get('action')

            if action == 'rename':
                df = df.rename(columns=transform.get('mapping', {}))

            elif action == 'filter':
                col = transform.get('column')
                op = transform.get('operator', '==')
                val = transform.get('value')
                if op == '==':
                    df = df[df[col] == val]
                elif op == '>':
                    df = df[df[col] > val]
                elif op == '<':
                    df = df[df[col] < val]

            elif action == 'calculate':
                new_col = transform.get('new_column')
                formula = transform.get('formula')
                if formula == 'variance':
                    df[new_col] = df[transform['col1']] - df[transform['col2']]

            elif action == 'date_parse':
                col = transform.get('column')
                df[col] = pd.to_datetime(df[col])

        return df

    def join_data(self, left_source: str, right_source: str,
                  left_key: str, right_key: str,
                  join_type: str = "left") -> pd.DataFrame:
        """Join two extracted data sources."""

        if left_source not in self.extracted_data or right_source not in self.extracted_data:
            return pd.DataFrame()

        left_df = self.extracted_data[left_source].data
        right_df = self.extracted_data[right_source].data

        return pd.merge(left_df, right_df, left_on=left_key, right_on=right_key, how=join_type)

    def aggregate_data(self, source_name: str,
                       group_by: List[str],
                       aggregations: Dict[str, str]) -> pd.DataFrame:
        """Aggregate extracted data."""

        if source_name not in self.extracted_data:
            return pd.DataFrame()

        df = self.extracted_data[source_name].data
        return df.groupby(group_by).agg(aggregations).reset_index()

    def get_extraction_summary(self) -> Dict[str, Any]:
        """Get summary of all extractions."""

        summary = {
            'erp_system': self.erp_name,
            'sources_defined': len(self.data_sources),
            'sources_extracted': len(self.extracted_data),
            'total_records': sum(e.record_count for e in self.extracted_data.values()),
            'by_module': {}
        }

        for ext in self.extracted_data.values():
            module = ext.module.value
            if module not in summary['by_module']:
                summary['by_module'][module] = {'sources': 0, 'records': 0}
            summary['by_module'][module]['sources'] += 1
            summary['by_module'][module]['records'] += ext.record_count

        return summary

    def export_to_excel(self, output_path: str) -> str:
        """Export all extracted data to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary = self.get_extraction_summary()
            summary_df = pd.DataFrame([{
                'ERP System': summary['erp_system'],
                'Sources Defined': summary['sources_defined'],
                'Sources Extracted': summary['sources_extracted'],
                'Total Records': summary['total_records']
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Each extracted source
            for name, extracted in self.extracted_data.items():
                sheet_name = name[:31]  # Excel sheet name limit
                extracted.data.to_excel(writer, sheet_name=sheet_name, index=False)

        return output_path

    def export_to_json(self, output_path: str) -> str:
        """Export extracted data to JSON."""

        output = {
            'summary': self.get_extraction_summary(),
            'data': {}
        }

        for name, extracted in self.extracted_data.items():
            output['data'][name] = {
                'module': extracted.module.value,
                'extracted_at': extracted.extracted_at.isoformat(),
                'record_count': extracted.record_count,
                'records': extracted.data.to_dict(orient='records')
            }

        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2, default=str)

        return output_path

    def generate_sql_query(self, source: DataSource) -> str:
        """Generate SQL query for data source."""

        columns = ", ".join(source.columns)
        query = f"SELECT {columns}\nFROM {source.table_name}"

        if source.filters:
            conditions = []
            for col, value in source.filters.items():
                if isinstance(value, str):
                    conditions.append(f"{col} = '{value}'")
                else:
                    conditions.append(f"{col} = {value}")
            query += "\nWHERE " + " AND ".join(conditions)

        return query + ";"
```

## Quick Start

```python
# Initialize extractor
extractor = ERPDataExtractor("Procore")

# Define standard extractions
extractor.define_project_extraction()
extractor.define_cost_extraction()

# Simulate extraction from DataFrames
projects_df = pd.DataFrame([
    {"id": 1, "code": "PRJ-001", "name": "Office Building", "status": "Active", "budget": 5000000},
    {"id": 2, "code": "PRJ-002", "name": "Warehouse", "status": "Planning", "budget": 2000000}
])

extractor.extract_from_dataframe("projects", projects_df)

# Get summary
summary = extractor.get_extraction_summary()
print(f"Total records: {summary['total_records']}")
```

## Common Use Cases

### 1. Transform Data
```python
transformed = extractor.transform_data("cost_items", [
    {"action": "rename", "mapping": {"budgeted": "budget", "actual": "spent"}},
    {"action": "calculate", "new_column": "variance", "formula": "variance", "col1": "budget", "col2": "spent"}
])
```

### 2. Join Sources
```python
joined = extractor.join_data("cost_items", "projects", "project_id", "id")
```

### 3. Aggregate
```python
by_project = extractor.aggregate_data("cost_items", ["project_id"], {"budgeted": "sum", "actual": "sum"})
```

## Resources
- **DDC Book**: Chapter 3.4 - Construction ERP Systems
- **Website**: https://datadrivenconstruction.io
