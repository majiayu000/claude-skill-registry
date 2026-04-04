---
name: m4-api
description: Use the M4 Python API to query clinical datasets (MIMIC-IV, eICU) programmatically. Triggers on "M4 API", "query MIMIC with Python", "clinical data analysis", "EHR data", "execute SQL on MIMIC", or when writing code to access clinical databases.
---

# M4 Python API

The M4 Python API provides programmatic access to clinical datasets for code execution environments. It mirrors the MCP tools but returns native Python types (DataFrames, dicts) instead of formatted strings.

## When to Use the API vs MCP Tools

**Use the Python API when:**
- **Complex clinical analysis** - Multi-step analyses that require intermediate results, joins across queries, or statistical computations
- **Large result sets** - Query results with thousands of rows can be stored in DataFrames without dumping into context
- **Mathematical operations** - Aggregations, percentile calculations, statistical tests, and counting that benefit from pandas/numpy
- **Iterative exploration** - Building up analysis through multiple queries where each step informs the next

**Use MCP tools when:**
- Simple one-off queries where the result fits comfortably in context
- Interactive exploration where you want to see results immediately

## Required Workflow

**You must follow this sequence:**

1. `set_dataset()` - Select which dataset to query (REQUIRED FIRST)
2. `get_schema()` / `get_table_info()` - Explore available tables
3. `execute_query()` - Run SQL queries

```python
from m4 import set_dataset, get_schema, get_table_info, execute_query

# Step 1: Always set dataset first
set_dataset("mimic-iv")  # or "mimic-iv-demo", "eicu", "mimic-iv-note"

# Step 2: Explore schema
schema = get_schema()
print(schema['tables'])  # List of table names

# Step 3: Inspect specific tables before querying
info = get_table_info("hosp_patients")
print(info['schema'])  # DataFrame with column names, types
print(info['sample'])  # DataFrame with sample rows

# Step 4: Execute queries
df = execute_query("SELECT gender, COUNT(*) as n FROM hosp_patients GROUP BY gender")
# Returns pd.DataFrame - use pandas operations freely
```

## API Reference

### Dataset Management

| Function | Returns | Description |
|----------|---------|-------------|
| `list_datasets()` | `list[str]` | Available dataset names |
| `set_dataset(name)` | `str` | Set active dataset (confirmation message) |
| `get_active_dataset()` | `str` | Get current dataset name |

### Tabular Data (requires TABULAR modality)

| Function | Returns | Description |
|----------|---------|-------------|
| `get_schema()` | `dict` | `{'backend_info': str, 'tables': list[str]}` |
| `get_table_info(table, show_sample=True)` | `dict` | `{'schema': DataFrame, 'sample': DataFrame}` |
| `execute_query(sql)` | `DataFrame` | Query results as pandas DataFrame |

### Clinical Notes (requires NOTES modality)

| Function | Returns | Description |
|----------|---------|-------------|
| `search_notes(query, note_type, limit, snippet_length)` | `dict` | `{'results': dict[str, DataFrame]}` |
| `get_note(note_id, max_length)` | `dict` | `{'text': str, 'subject_id': int, ...}` |
| `list_patient_notes(subject_id, note_type, limit)` | `dict` | `{'notes': dict[str, DataFrame]}` |

## Error Handling

M4 uses a hierarchy of exceptions. Catch specific types to handle errors appropriately:

```
M4Error (base)
├── DatasetError      # Dataset doesn't exist or not configured
├── QueryError        # SQL syntax error, table not found, query failed
└── ModalityError     # Tool incompatible with dataset (e.g., notes on tabular-only)
```

**Recovery patterns:**

```python
from m4 import execute_query, set_dataset, DatasetError, QueryError, ModalityError

try:
    df = execute_query("SELECT * FROM hosp_patients")
except DatasetError as e:
    # No dataset selected, or dataset not found
    # Recovery: call set_dataset() first, or check list_datasets()
    set_dataset("mimic-iv")
    df = execute_query("SELECT * FROM hosp_patients")
except QueryError as e:
    # SQL error or table not found
    # Recovery: check table name with get_schema(), fix SQL syntax
    print(f"Query failed: {e}")
except ModalityError as e:
    # Tried notes function on tabular-only dataset
    # Recovery: switch to dataset with NOTES modality
    set_dataset("mimic-iv-note")
```

## Dataset State

**Important:** Dataset selection is module-level state that persists across function calls.

```python
set_dataset("mimic-iv")
df1 = execute_query("SELECT COUNT(*) FROM hosp_patients")  # Uses mimic-iv

set_dataset("eicu")
df2 = execute_query("SELECT COUNT(*) FROM patient")        # Uses eicu
```

## MCP Tool Equivalence

The Python API mirrors MCP tools but with better return types:

| MCP Tool | Python Function | MCP Returns | Python Returns |
|----------|-----------------|-------------|----------------|
| `execute_query` | `execute_query()` | Formatted string | `pd.DataFrame` |
| `get_database_schema` | `get_schema()` | Formatted string | `dict` with `tables` list |
| `get_table_info` | `get_table_info()` | Formatted string | `dict` with `schema`/`sample` DataFrames |

Use the Python API when you need to:
- Chain queries in analysis pipelines
- Perform pandas operations on results
- Avoid parsing formatted output
