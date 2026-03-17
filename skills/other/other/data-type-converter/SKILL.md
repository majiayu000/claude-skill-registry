---
name: data-type-converter
description: Convert between data formats (JSON, CSV, XML, YAML, TOML). Handles nested structures, arrays, and preserves data types where possible.
---

# Data Type Converter

Convert data between JSON, CSV, XML, YAML, and TOML formats. Handles nested structures, arrays, and complex data with intelligent flattening options.

## Quick Start

```python
from scripts.data_converter import DataTypeConverter

# JSON to CSV
converter = DataTypeConverter()
converter.convert("data.json", "data.csv")

# YAML to JSON
converter.convert("config.yaml", "config.json")

# With options
converter.convert("data.json", "data.csv", flatten=True)
```

## Features

- **5 Formats**: JSON, CSV, XML, YAML, TOML
- **Nested Data**: Flatten or preserve nested structures
- **Arrays**: Handle array data intelligently
- **Type Preservation**: Maintain data types where possible
- **Pretty Output**: Formatted, human-readable output
- **Batch Processing**: Convert multiple files

## API Reference

### Basic Conversion

```python
converter = DataTypeConverter()

# Auto-detect format from extension
converter.convert("input.json", "output.csv")
converter.convert("input.xml", "output.json")
converter.convert("input.yaml", "output.toml")
```

### With Options

```python
# Flatten nested structures for CSV
converter.convert("nested.json", "flat.csv", flatten=True)

# Pretty print output
converter.convert("data.json", "pretty.json", indent=4)

# Specify root element for XML
converter.convert("data.json", "data.xml", root="records")
```

### Programmatic Access

```python
# Load and convert in memory
data = converter.load("data.json")
converter.save(data, "data.yaml")

# String conversion
json_str = '{"name": "John", "age": 30}'
yaml_str = converter.convert_string(json_str, "json", "yaml")
```

### Batch Processing

```python
# Convert all JSON files to CSV
converter.batch_convert(
    input_dir="./json_files",
    output_dir="./csv_files",
    output_format="csv"
)
```

## CLI Usage

```bash
# Basic conversion
python data_converter.py --input data.json --output data.csv

# With flattening
python data_converter.py --input nested.json --output flat.csv --flatten

# Batch convert
python data_converter.py --input-dir ./json --output-dir ./csv --format csv

# Pretty print
python data_converter.py --input data.json --output pretty.json --indent 4
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input file | Required |
| `--output` | Output file | Required |
| `--input-dir` | Input directory for batch | - |
| `--output-dir` | Output directory | - |
| `--format` | Output format | From extension |
| `--flatten` | Flatten nested data | False |
| `--indent` | Indentation spaces | 2 |
| `--root` | XML root element | root |

## Conversion Matrix

| From/To | JSON | CSV | XML | YAML | TOML |
|---------|------|-----|-----|------|------|
| **JSON** | - | Yes | Yes | Yes | Yes |
| **CSV** | Yes | - | Yes | Yes | Yes |
| **XML** | Yes | Yes | - | Yes | Yes |
| **YAML** | Yes | Yes | Yes | - | Yes |
| **TOML** | Yes | Yes | Yes | Yes | - |

## Examples

### JSON to CSV (Flat)

```python
converter = DataTypeConverter()

# Input: data.json
# [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]

converter.convert("data.json", "data.csv")

# Output: data.csv
# name,age
# John,30
# Jane,25
```

### Nested JSON to Flat CSV

```python
# Input: nested.json
# [{"user": {"name": "John", "email": "j@test.com"}, "orders": 5}]

converter.convert("nested.json", "flat.csv", flatten=True)

# Output: flat.csv
# user.name,user.email,orders
# John,j@test.com,5
```

### YAML Config to JSON

```python
# Input: config.yaml
# database:
#   host: localhost
#   port: 5432
# debug: true

converter.convert("config.yaml", "config.json")

# Output: config.json
# {"database": {"host": "localhost", "port": 5432}, "debug": true}
```

### XML to JSON

```python
# Input: data.xml
# <users>
#   <user><name>John</name><age>30</age></user>
# </users>

converter.convert("data.xml", "data.json")

# Output: data.json
# {"users": {"user": {"name": "John", "age": "30"}}}
```

## Dependencies

```
pyyaml>=6.0
toml>=0.10.0
xmltodict>=0.13.0
pandas>=2.0.0
```

## Limitations

- CSV doesn't support nested data (requires flattening)
- XML attribute handling is basic
- TOML doesn't support null values
- Very deep nesting may cause issues with some formats
- Array handling varies by format
