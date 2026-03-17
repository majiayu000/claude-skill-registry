---
name: "etl-pipeline"
description: "Build automated ETL (Extract-Transform-Load) pipelines for construction data. Process PDFs, Excel, BIM exports. Generate reports, dashboards, and integrate with other systems. Orchestrate with Airflow or n8n."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "⚙️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# ETL Pipeline for Construction Data

## Overview

Based on DDC methodology (Chapter 4.2), this skill enables building automated data pipelines that extract information from various sources, transform it into useful formats, and load it into target systems or generate reports.

**Book Reference:** "ETL и автоматизация процессов" / "ETL and Process Automation"

> "ETL: переход от ручного управления к автоматизации позволяет компаниям обрабатывать данные без постоянного человеческого вмешательства."
> — DDC Book, Chapter 4.2

## ETL Components

```
┌─────────┐    ┌───────────┐    ┌────────┐
│ EXTRACT │ -> │ TRANSFORM │ -> │  LOAD  │
└─────────┘    └───────────┘    └────────┘
   │               │               │
   ▼               ▼               ▼
 Sources        Process         Outputs
 - PDF          - Clean         - Excel
 - Excel        - Validate      - PDF
 - CSV          - Calculate     - Database
 - BIM          - Merge         - API
 - API          - Aggregate     - Dashboard
```

## Quick Start

```python
import pandas as pd

# Simple ETL Pipeline
def simple_etl_pipeline(input_file, output_file):
    # EXTRACT
    df = pd.read_excel(input_file)

    # TRANSFORM
    df = df.dropna()  # Clean
    df['Total'] = df['Quantity'] * df['Unit_Price']  # Calculate
    summary = df.groupby('Category')['Total'].sum()  # Aggregate

    # LOAD
    summary.to_excel(output_file)
    return summary

# Run
result = simple_etl_pipeline("raw_data.xlsx", "processed_report.xlsx")
```

## Extract: Data Sources

### From Multiple Excel Files

```python
import pandas as pd
from pathlib import Path

def extract_excel_files(folder_path, pattern="*.xlsx"):
    """Extract data from multiple Excel files"""
    files = Path(folder_path).glob(pattern)
    all_data = []

    for file in files:
        try:
            df = pd.read_excel(file)
            df['_source_file'] = file.name
            all_data.append(df)
            print(f"Extracted: {file.name}")
        except Exception as e:
            print(f"Error reading {file.name}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

# Usage
df = extract_excel_files("./project_data/")
```

### From PDF Documents

```python
import pdfplumber
import pandas as pd

def extract_from_pdfs(pdf_folder):
    """Extract tables from all PDFs in folder"""
    files = Path(pdf_folder).glob("*.pdf")
    all_tables = []

    for pdf_path in files:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if table and len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        df['_source'] = pdf_path.name
                        all_tables.append(df)

    return pd.concat(all_tables, ignore_index=True) if all_tables else pd.DataFrame()
```

### From API

```python
import requests
import pandas as pd

def extract_from_api(api_url, headers=None):
    """Extract data from REST API"""
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        raise Exception(f"API error: {response.status_code}")

# Usage
df = extract_from_api("https://api.example.com/projects")
```

### From Database

```python
import pandas as pd
import sqlite3

def extract_from_database(db_path, query):
    """Extract data using SQL query"""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Usage
df = extract_from_database(
    "construction.db",
    "SELECT * FROM elements WHERE category = 'Wall'"
)
```

## Transform: Data Processing

### Data Cleaning

```python
def clean_construction_data(df):
    """Standard cleaning for construction data"""
    # Remove empty rows
    df = df.dropna(how='all')

    # Strip whitespace
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()

    # Standardize category names
    if 'Category' in df.columns:
        df['Category'] = df['Category'].str.title()

    # Convert numeric columns
    numeric_cols = ['Volume', 'Area', 'Length', 'Quantity', 'Cost']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove duplicates
    df = df.drop_duplicates()

    return df
```

### Data Validation

```python
def validate_construction_data(df, rules):
    """
    Validate data against rules

    Args:
        rules: list of dicts like
        [{'column': 'Volume', 'rule': 'positive'},
         {'column': 'Category', 'rule': 'not_null'}]
    """
    errors = []

    for rule in rules:
        col = rule['column']
        rule_type = rule['rule']

        if col not in df.columns:
            errors.append(f"Missing column: {col}")
            continue

        if rule_type == 'positive':
            invalid = df[df[col] <= 0]
            if len(invalid) > 0:
                errors.append(f"{len(invalid)} rows with non-positive {col}")

        elif rule_type == 'not_null':
            null_count = df[col].isna().sum()
            if null_count > 0:
                errors.append(f"{null_count} null values in {col}")

        elif rule_type == 'unique':
            duplicates = df[col].duplicated().sum()
            if duplicates > 0:
                errors.append(f"{duplicates} duplicate values in {col}")

    return errors

# Usage
validation_rules = [
    {'column': 'Volume', 'rule': 'positive'},
    {'column': 'Category', 'rule': 'not_null'},
    {'column': 'ElementId', 'rule': 'unique'}
]
errors = validate_construction_data(df, validation_rules)
```

### Data Aggregation

```python
def aggregate_by_hierarchy(df, hierarchy=['Project', 'Building', 'Level', 'Category']):
    """Aggregate data at different hierarchy levels"""
    results = {}

    for i in range(1, len(hierarchy) + 1):
        level_cols = hierarchy[:i]
        if all(col in df.columns for col in level_cols):
            agg = df.groupby(level_cols).agg({
                'Volume': 'sum',
                'Cost': 'sum',
                'ElementId': 'count'
            }).rename(columns={'ElementId': 'Count'})

            level_name = '_'.join(level_cols)
            results[level_name] = agg

    return results

# Usage
aggregations = aggregate_by_hierarchy(df)
for name, data in aggregations.items():
    print(f"\n{name}:")
    print(data.head())
```

### Data Enrichment

```python
def enrich_with_prices(df, prices_df):
    """Enrich element data with pricing information"""
    # Merge with price database
    enriched = df.merge(prices_df, on='Category', how='left')

    # Calculate costs
    enriched['Material_Cost'] = enriched['Volume'] * enriched['Unit_Price']
    enriched['Labor_Cost'] = enriched['Volume'] * enriched['Labor_Rate']
    enriched['Total_Cost'] = enriched['Material_Cost'] + enriched['Labor_Cost']

    return enriched
```

## Load: Output Generation

### Generate Excel Report

```python
def generate_excel_report(df, summary, output_path):
    """Generate formatted Excel report"""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Raw data
        df.to_excel(writer, sheet_name='Data', index=False)

        # Summary by category
        summary.to_excel(writer, sheet_name='Summary')

        # Pivot table
        if 'Level' in df.columns and 'Category' in df.columns:
            pivot = pd.pivot_table(
                df, values='Volume',
                index='Level', columns='Category',
                aggfunc='sum', fill_value=0
            )
            pivot.to_excel(writer, sheet_name='By_Level')

    print(f"Report saved: {output_path}")

# Usage
generate_excel_report(df, summary, "project_report.xlsx")
```

### Generate PDF Report

```python
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(df, output_path, title="Construction Report"):
    """Generate PDF report from DataFrame"""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph(title, styles['Title']))

    # Convert DataFrame to table
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data)

    # Style the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)
    print(f"PDF saved: {output_path}")

# Usage
generate_pdf_report(summary, "report.pdf")
```

### Load to Database

```python
import sqlite3

def load_to_database(df, db_path, table_name, if_exists='replace'):
    """Load DataFrame to SQLite database"""
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    conn.close()
    print(f"Loaded {len(df)} rows to {table_name}")

# Usage
load_to_database(df, "construction.db", "elements")
```

## Complete ETL Pipeline

```python
class ConstructionETLPipeline:
    """Complete ETL pipeline for construction data"""

    def __init__(self, config):
        self.config = config
        self.data = None
        self.errors = []

    def extract(self):
        """Extract data from configured sources"""
        print("Extracting data...")
        sources = []

        # Excel files
        if 'excel_folder' in self.config:
            df = extract_excel_files(self.config['excel_folder'])
            sources.append(df)

        # PDF files
        if 'pdf_folder' in self.config:
            df = extract_from_pdfs(self.config['pdf_folder'])
            sources.append(df)

        self.data = pd.concat(sources, ignore_index=True)
        print(f"Extracted {len(self.data)} records")
        return self

    def transform(self):
        """Apply transformations"""
        print("Transforming data...")

        # Clean
        self.data = clean_construction_data(self.data)

        # Validate
        if 'validation_rules' in self.config:
            self.errors = validate_construction_data(
                self.data, self.config['validation_rules']
            )

        # Enrich with prices if available
        if 'prices_file' in self.config:
            prices = pd.read_excel(self.config['prices_file'])
            self.data = enrich_with_prices(self.data, prices)

        print(f"Transformed {len(self.data)} records")
        return self

    def load(self):
        """Load to configured outputs"""
        print("Loading data...")

        # Excel report
        if 'excel_output' in self.config:
            summary = self.data.groupby('Category').agg({
                'Volume': 'sum', 'Cost': 'sum'
            })
            generate_excel_report(
                self.data, summary, self.config['excel_output']
            )

        # Database
        if 'database' in self.config:
            load_to_database(
                self.data,
                self.config['database'],
                self.config.get('table_name', 'elements')
            )

        print("Pipeline complete!")
        return self

    def run(self):
        """Run complete pipeline"""
        return self.extract().transform().load()

# Usage
config = {
    'excel_folder': './input_data/',
    'prices_file': './prices.xlsx',
    'validation_rules': [
        {'column': 'Volume', 'rule': 'positive'},
        {'column': 'Category', 'rule': 'not_null'}
    ],
    'excel_output': './output/report.xlsx',
    'database': './output/project.db',
    'table_name': 'elements'
}

pipeline = ConstructionETLPipeline(config)
pipeline.run()
```

## Scheduling with Airflow

```python
# airflow_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'construction_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'construction_etl',
    default_args=default_args,
    description='Daily construction data ETL',
    schedule_interval='@daily',
)

def extract_task():
    # Extract logic
    pass

def transform_task():
    # Transform logic
    pass

def load_task():
    # Load logic
    pass

t1 = PythonOperator(task_id='extract', python_callable=extract_task, dag=dag)
t2 = PythonOperator(task_id='transform', python_callable=transform_task, dag=dag)
t3 = PythonOperator(task_id='load', python_callable=load_task, dag=dag)

t1 >> t2 >> t3
```

## Quick Reference

| Stage | Task | Tool/Method |
|-------|------|-------------|
| Extract | Read Excel | `pd.read_excel()` |
| Extract | Read CSV | `pd.read_csv()` |
| Extract | Read PDF | `pdfplumber` |
| Extract | Read API | `requests.get()` |
| Transform | Clean | `df.dropna()`, `df.str.strip()` |
| Transform | Validate | Custom validation functions |
| Transform | Calculate | `df['new'] = df['a'] * df['b']` |
| Transform | Aggregate | `df.groupby().agg()` |
| Load | Excel | `df.to_excel()` |
| Load | PDF | `reportlab` |
| Load | Database | `df.to_sql()` |
| Load | API | `requests.post()` |

## Resources

- **Book**: "Data-Driven Construction" by Artem Boiko, Chapter 4.2
- **Website**: https://datadrivenconstruction.io
- **Airflow**: https://airflow.apache.org
- **n8n**: https://n8n.io

## Next Steps

- See `bim-validation-pipeline` for BIM data validation
- See `pdf-report-generator` for advanced PDF generation
- See `workflow-automation` for n8n integration
