---
name: file-processing
description: Process and analyze CSV, JSON, and text files with data transformation, cleaning, analysis, and visualization capabilities
allowed-tools:
  - shell
---

# File Processing Skill

## Purpose

Process structured data files (CSV, JSON, text) with comprehensive capabilities for data cleaning, transformation, analysis, and export. This skill enables working with data files without requiring users to write code.

## When to Use This Skill

Use this skill when you need to:
- Load and parse CSV or JSON files
- Clean and transform data
- Perform statistical analysis
- Filter, sort, or aggregate data
- Merge or join datasets
- Convert between formats (CSV ↔ JSON)
- Generate summary reports

## Capabilities

### 1. Data Loading

Supported formats:
- **CSV files**: Any delimiter (comma, tab, semicolon, etc.)
- **JSON files**: Single objects or arrays of objects
- **Text files**: Custom delimited formats

### 2. Data Cleaning

Available operations:
- Remove duplicate rows
- Handle missing values (drop, fill, interpolate)
- Normalize text (trim whitespace, standardize case)
- Convert data types
- Remove outliers
- Validate data against rules

### 3. Data Transformation

Available operations:
- **Filter**: Select rows based on conditions
- **Select**: Choose specific columns
- **Sort**: Order by one or more columns
- **Group**: Aggregate data by categories
- **Pivot**: Reshape data (wide ↔ long format)
- **Merge**: Combine multiple datasets
- **Calculate**: Add derived columns

### 4. Data Analysis

Available analyses:
- Descriptive statistics (mean, median, std, etc.)
- Frequency distributions
- Correlation analysis
- Trend detection
- Missing data analysis
- Data quality assessment

### 5. Export

Output formats:
- CSV files
- JSON files (objects or arrays)
- Markdown tables
- Summary reports

## Instructions for Execution

When this skill is activated, follow these steps:

### Step 1: Understand the Request

Ask clarifying questions if needed:
- What file(s) need to be processed?
- What specific analysis or transformation is required?
- What output format is desired?
- Are there any specific requirements or constraints?

### Step 2: Load the Data

Use `shell` to load and process data:

```python
# For CSV files
import csv

# Read from file path
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# For JSON files
import json
with open('data.json', 'r') as f:
    data = json.load(f)
```

Alternatively, use the supporting scripts:
```python
# Execute the helper script
("scripts/process.py")
```

### Step 3: Perform Operations

Apply the requested transformations or analyses:

```python
# Example: Filter and aggregate
filtered = [row for row in data if float(row['amount']) > 100]

# Example: Calculate statistics
from statistics import mean, median
amounts = [float(row['amount']) for row in data]
avg = mean(amounts)
med = median(amounts)
```

### Step 4: Generate Output

Format results according to user needs:

```python
# As markdown table
def to_markdown_table(data, columns=None):
    if not data:
        return "No data"

    if columns is None:
        columns = list(data[0].keys())

    # Header
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    # Rows
    rows = []
    for row in data:
        row_str = "| " + " | ".join(str(row.get(col, "")) for col in columns) + " |"
        rows.append(row_str)

    return "\n".join([header, separator] + rows)

print(to_markdown_table(filtered))
```

## Common Use Cases

### Use Case 1: CSV Analysis

```python
# Example: Analyze sales data
import csv
from io import StringIO
from statistics import mean, sum as total

# Load CSV
reader = csv.DictReader(StringIO(file_content))
data = list(reader)

# Calculate metrics
total_sales = sum(float(row['amount']) for row in data)
avg_sales = mean(float(row['amount']) for row in data)
unique_customers = len(set(row['customer_id'] for row in data))

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Average Sale: ${avg_sales:,.2f}")
print(f"Unique Customers: {unique_customers}")
```

### Use Case 2: Data Filtering

```python
# Example: Filter records by criteria
filtered = [
    row for row in data
    if row['status'] == 'active' and float(row['score']) >= 80
]

print(f"Found {len(filtered)} matching records")
```

### Use Case 3: Data Grouping

```python
# Example: Group and aggregate
from collections import defaultdict

grouped = defaultdict(list)
for row in data:
    grouped[row['category']].append(float(row['value']))

summary = {}
for category, values in grouped.items():
    summary[category] = {
        'count': len(values),
        'total': sum(values),
        'average': sum(values) / len(values)
    }

for category, stats in summary.items():
    print(f"{category}: {stats['count']} items, avg = {stats['average']:.2f}")
```

### Use Case 4: Format Conversion

```python
# Example: CSV to JSON
import csv
import json
from io import StringIO

reader = csv.DictReader(StringIO(file_content))
data = list(reader)

# Convert to JSON
json_output = json.dumps(data, indent=2)
print(json_output)
```

## Supporting Scripts

- `scripts/process.py`: Data processing utility functions

## Data Processing Patterns

### Pattern 1: ETL (Extract, Transform, Load)

```python
# Extract
data = load_file(file_content)

# Transform
cleaned = remove_duplicates(data)
filtered = apply_filters(cleaned, conditions)
enriched = add_calculated_fields(filtered)

# Load (output)
output = format_as_markdown(enriched)
print(output)
```

### Pattern 2: Aggregation Pipeline

```python
# Pipeline: filter → group → aggregate → sort
result = (
    filter_data(data, conditions)
    | group_by(key='category')
    | aggregate(metrics=['sum', 'average'])
    | sort_by(column='total', descending=True)
)
```

## Best Practices

1. **Validate Input**: Check file format and structure before processing
2. **Handle Errors**: Gracefully handle missing columns or invalid data
3. **Show Progress**: For large files, indicate what's being processed
4. **Explain Results**: Provide context for statistics and findings
5. **Suggest Next Steps**: Recommend additional analyses if relevant

## Limitations

- **File Size**: Large files (>100MB) may be slow or cause memory issues
- **Complex Operations**: Very complex transformations may require multiple steps
- **Performance**: Pure Python processing; not optimized for big data

## Tips for Users

- **Provide Examples**: Show a sample of your data format
- **Be Specific**: Clearly describe what transformation you need
- **Start Simple**: Begin with basic operations, then add complexity
- **Check Output**: Verify results make sense for your data
