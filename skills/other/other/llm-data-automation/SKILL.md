---
name: "llm-data-automation"
description: "Automate construction data processing using LLM (ChatGPT, Claude, LLaMA). Generate Python/Pandas scripts, extract data from documents, and create automated pipelines without deep programming knowledge."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🐼", "os": ["win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# LLM Data Automation for Construction

## Overview

Based on DDC methodology (Chapter 2.3), this skill enables automation of construction data processing using Large Language Models (LLM). Instead of manually coding data transformations, you describe what you need in natural language, and the LLM generates the necessary Python/Pandas code.

**Book Reference:** "Pandas DataFrame и LLM ChatGPT" / "Pandas DataFrame and LLM ChatGPT"

> "LLM-модели, такие как ChatGPT и LLaMA, позволяют специалистам без глубоких знаний программирования внести свой вклад в автоматизацию и улучшение бизнес-процессов компании."
> — DDC Book, Chapter 2.3

## Quick Start

### Option 1: Use ChatGPT/Claude Online
Simply describe your data processing task in natural language:

```
Prompt: "Write Python code to read an Excel file with construction materials,
filter rows where quantity > 100, and save to CSV."
```

### Option 2: Run Local LLM (Ollama)
```bash
# Install Ollama from ollama.com
ollama pull mistral

# Run a query
ollama run mistral "Write Pandas code to calculate total cost from quantity * unit_price"
```

### Option 3: Use LM Studio (GUI)
1. Download from lmstudio.ai
2. Install and select a model (e.g., Mistral, LLaMA)
3. Start chatting with your local AI

## Core Concepts

### DataFrame as Universal Format
```python
import pandas as pd

# Construction project as DataFrame
# Rows = elements, Columns = attributes
df = pd.DataFrame({
    'element_id': ['W001', 'W002', 'C001'],
    'category': ['Wall', 'Wall', 'Column'],
    'material': ['Concrete', 'Brick', 'Steel'],
    'volume_m3': [45.5, 32.0, 8.2],
    'cost_per_m3': [150, 80, 450]
})

# Calculate total cost
df['total_cost'] = df['volume_m3'] * df['cost_per_m3']
print(df)
```

### LLM Prompts for Construction Tasks

**Data Import:**
```
"Write code to import Excel file with construction schedule,
parse dates, and create a Pandas DataFrame"
```

**Data Filtering:**
```
"Filter construction elements where category is 'Structural'
and cost exceeds budget limit of 50000"
```

**Data Aggregation:**
```
"Group construction data by floor level,
calculate total volume and cost for each floor"
```

**Report Generation:**
```
"Create summary report with material quantities grouped by category,
export to Excel with formatting"
```

## Common Use Cases

### 1. Extract Data from PDF Documents
```python
# Prompt to ChatGPT:
# "Write code to extract tables from PDF and convert to DataFrame"

import pdfplumber
import pandas as pd

def pdf_to_dataframe(pdf_path):
    """Extract tables from PDF file"""
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)

    if all_tables:
        return pd.concat(all_tables, ignore_index=True)
    return pd.DataFrame()

# Usage
df = pdf_to_dataframe("construction_spec.pdf")
df.to_excel("extracted_data.xlsx", index=False)
```

### 2. Process BIM Element Data
```python
# Prompt: "Analyze BIM elements, group by category, calculate volumes"

import pandas as pd

def analyze_bim_elements(csv_path):
    """Analyze BIM element data from CSV export"""
    df = pd.read_csv(csv_path)

    # Group by category
    summary = df.groupby('Category').agg({
        'Volume': 'sum',
        'Area': 'sum',
        'ElementId': 'count'
    }).rename(columns={'ElementId': 'Count'})

    return summary

# Usage
summary = analyze_bim_elements("revit_export.csv")
print(summary)
```

### 3. Cost Estimation Pipeline
```python
# Prompt: "Create cost estimation from quantities and unit prices"

import pandas as pd

def calculate_cost_estimate(quantities_df, prices_df):
    """
    Calculate project cost estimate

    Args:
        quantities_df: DataFrame with columns [item_code, quantity]
        prices_df: DataFrame with columns [item_code, unit_price, unit]

    Returns:
        DataFrame with cost calculations
    """
    # Merge quantities with prices
    result = quantities_df.merge(prices_df, on='item_code', how='left')

    # Calculate costs
    result['total_cost'] = result['quantity'] * result['unit_price']

    # Add summary
    result['cost_percentage'] = (result['total_cost'] /
                                  result['total_cost'].sum() * 100).round(2)

    return result

# Usage
quantities = pd.DataFrame({
    'item_code': ['C001', 'S001', 'W001'],
    'quantity': [150, 2000, 500]
})

prices = pd.DataFrame({
    'item_code': ['C001', 'S001', 'W001'],
    'unit_price': [120, 45, 85],
    'unit': ['m3', 'kg', 'm2']
})

estimate = calculate_cost_estimate(quantities, prices)
print(estimate)
```

### 4. Schedule Data Processing
```python
# Prompt: "Parse construction schedule, calculate durations, identify delays"

import pandas as pd
from datetime import datetime

def analyze_schedule(schedule_path):
    """Analyze construction schedule for delays"""
    df = pd.read_excel(schedule_path)

    # Parse dates
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df['actual_end'] = pd.to_datetime(df['actual_end'])

    # Calculate durations
    df['planned_duration'] = (df['end_date'] - df['start_date']).dt.days
    df['actual_duration'] = (df['actual_end'] - df['start_date']).dt.days

    # Identify delays
    df['delay_days'] = df['actual_duration'] - df['planned_duration']
    df['is_delayed'] = df['delay_days'] > 0

    return df

# Usage
schedule = analyze_schedule("project_schedule.xlsx")
delayed_tasks = schedule[schedule['is_delayed']]
print(f"Delayed tasks: {len(delayed_tasks)}")
```

## Local LLM Setup (No Internet Required)

### Using Ollama
```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Download models
ollama pull mistral      # General purpose, 7B params
ollama pull codellama    # Code-focused
ollama pull deepseek-coder  # Best for coding tasks

# Run
ollama run mistral "Write Pandas code to merge two DataFrames on project_id"
```

### Using LlamaIndex for Company Documents
```python
# Load company documents into local LLM
from llama_index import SimpleDirectoryReader, VectorStoreIndex

# Read all PDFs from folder
reader = SimpleDirectoryReader("company_documents/")
documents = reader.load_data()

# Create searchable index
index = VectorStoreIndex.from_documents(documents)

# Query your documents
query_engine = index.as_query_engine()
response = query_engine.query(
    "What are the standard concrete mix specifications?"
)
print(response)
```

## IDE Recommendations

| IDE | Best For | Features |
|-----|----------|----------|
| **Jupyter Notebook** | Learning, experiments | Interactive cells, visualizations |
| **Google Colab** | Free GPU, quick start | Cloud-based, pre-installed libs |
| **VS Code** | Professional development | Extensions, GitHub Copilot |
| **PyCharm** | Large projects | Advanced debugging, refactoring |

### Quick Setup with Jupyter
```bash
pip install jupyter pandas openpyxl pdfplumber
jupyter notebook
```

## Best Practices

1. **Start Simple**: Begin with clear, specific prompts
2. **Iterate**: Refine prompts based on results
3. **Validate**: Always check generated code before running
4. **Document**: Save working prompts for reuse
5. **Secure**: Use local LLM for sensitive company data

## Common Prompts Library

### Data Import
- "Read Excel file and show first 10 rows"
- "Import CSV with custom delimiter and encoding"
- "Load multiple Excel sheets into dictionary of DataFrames"

### Data Cleaning
- "Remove duplicate rows based on element_id"
- "Fill missing values with column mean"
- "Convert column to numeric, handling errors"

### Data Analysis
- "Calculate descriptive statistics for numeric columns"
- "Find correlation between cost and duration"
- "Identify outliers using IQR method"

### Data Export
- "Export to Excel with multiple sheets"
- "Save to CSV with specific encoding"
- "Generate formatted PDF report"

## Resources

- **Book**: "Data-Driven Construction" by Artem Boiko, Chapter 2.3
- **Website**: https://datadrivenconstruction.io
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Ollama**: https://ollama.com
- **LM Studio**: https://lmstudio.ai
- **Google Colab**: https://colab.research.google.com

## Next Steps

- See `pandas-construction-analysis` for advanced Pandas operations
- See `pdf-to-structured` for document processing
- See `etl-pipeline` for automated data pipelines
- See `rag-construction` for RAG implementation with construction documents
