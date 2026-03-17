---
name: tm1py-expert
description: Expert guidance for TM1py Python package for IBM Planning Analytics (TM1). Master connection management, data operations (MDX, views, DataFrames), metadata CRUD, performance optimization, and best practices. Use when working with TM1py, IBM Planning Analytics API, or when user mentions TM1, Planning Analytics, TM1 REST API, MDX queries, cube operations, dimension management, or Python TM1 development.
license: MIT
metadata:
  version: "1.0.0"
  author: tm1py-expert contributors
compatibility: Requires Python 3.7+, TM1py package, TM1/Planning Analytics v11+
---

# TM1py Expert

This skill provides expert guidance for working with TM1py, the Python package that wraps the IBM Planning Analytics (TM1) REST API. TM1py enables programmatic interaction with TM1 servers for data operations, metadata management, and automation.

## When to Use This Skill

Activate this skill when:
- **Connecting to TM1/Planning Analytics** servers from Python
- **Reading or writing data** from TM1 cubes (via MDX, views, or DataFrames)
- **Managing TM1 metadata** (dimensions, cubes, processes, chores, subsets)
- **Optimizing performance** with async operations or bulk data transfers
- **Troubleshooting TM1py** connection or operation issues
- **Designing TM1 automation** workflows
- User mentions: TM1py, IBM Planning Analytics, TM1 REST API, MDX queries, cube operations, dimension management, TI processes, Planning Analytics Workspace, tm1 automation

## Prerequisites

### Required
- Python 3.7 or higher
- TM1py package: `pip install tm1py` or `pip install "tm1py[pandas]"` (recommended)
- Access to a TM1/Planning Analytics server (v11 or higher)
- Valid TM1 credentials (username and password)
#### Recommended (TM1py 2.1+)
- TM1py 2.1 or higher for advanced features:
  - Auto-reconnect on network failures
  - Hybrid sync/async request modes
  - Built-in retry logic for resilience
### Optional
- pandas library (for DataFrame operations)
- networkx library (for hierarchy analysis)

## Core Concepts

### TM1Service - The Main Entry Point

All TM1py functionality is accessed through the `TM1Service` class, which establishes and manages your connection to TM1:

```python
from TM1py import TM1Service

# Use context manager (recommended - handles cleanup automatically)
with TM1Service(address='localhost', port=8001, user='admin', password='apple', ssl=True) as tm1:
    # Your TM1 operations here
    print(tm1.server.get_product_version())
```

### Service Architecture

TM1py organizes functionality into specialized services accessible via `tm1.<service>`:

- **tm1.cells**: Read/write cube data
- **tm1.dimensions**: Manage dimensions
- **tm1.hierarchies**: Manage hierarchies  
- **tm1.elements**: Manage elements and attributes
- **tm1.cubes**: Manage cubes
- **tm1.processes**: Execute and manage TI processes
- **tm1.chores**: Manage chores
- **tm1.subsets**: Manage subsets
- **tm1.views**: Manage cube views
- **tm1.sandboxes**: Manage sandboxes
- **tm1.security**: Manage users and groups
- **tm1.server**: Server information and operations
- **tm1.monitoring**: Monitor threads and sessions

See `references/API_REFERENCE.md` for comprehensive service documentation.

## Step-by-Step Instructions

### Task 1: Connect to TM1

#### TM1 11 On-Premise

```python
from TM1py import TM1Service

with TM1Service(
    address='localhost',
    port=8001,
    user='admin',
    password='apple',
    ssl=True,
    verify=False  # Set to True to verify SSL certificate
) as tm1:
    print(f"Connected to {tm1.server.get_server_name()}")
```

#### TM1 11 IBM Cloud

```python
with TM1Service(
    base_url='https://mycompany.planning-analytics.ibmcloud.com/tm1/api/tm1/',
    user='non_interactive_user',
    namespace='LDAP',
    password='your_password',
    ssl=True,
    verify=True,
    async_requests_mode=True
) as tm1:
    print("Connected to IBM Cloud")
```

#### TM1 12 PAaaS

```python
params = {
    "base_url": "https://us-east-1.planninganalytics.saas.ibm.com/api/<TenantId>/v0/tm1/<DatabaseName>/",
    "user": "apikey",
    "password": "<TheActualApiKey>",
    "async_requests_mode": True,
    "ssl": True,
    "verify": True
}

with TM1Service(**params) as tm1:
    print("Connected to PAaaS")
```

See `references/CONNECTION_GUIDE.md` for all connection patterns including TM1 12 on-premise and Cloud Pak for Data.

### Task 2: Read Data from Cubes

#### Execute MDX Query

```python
# Simple MDX query
mdx = """
SELECT
  {[Product].[Product].[ProductA], [Product].[Product].[ProductB]} ON ROWS,
  {[Period].[Period].[2024-Q1], [Period].[Period].[2024-Q2]} ON COLUMNS
FROM [SalesCube]
WHERE ([Measure].[Revenue])
"""

# Get data as dictionary
data_dict = tm1.cells.execute_mdx(mdx)
for coordinates, cell_properties in data_dict.items():
    print(f"{coordinates}: {cell_properties['Value']}")

# Get data as pandas DataFrame (requires pandas)
df = tm1.cells.execute_mdx_dataframe(mdx)
print(df)
```

#### Read from Cube View

```python
# Read from existing view
df = tm1.cells.execute_view_dataframe(
    cube_name='SalesCube',
    view_name='DefaultView',
    private=False
)
print(df)

# Read with performance optimizations
df = tm1.cells.execute_view_dataframe(
    cube_name='SalesCube',
    view_name='LargeView',
    private=False,
    use_blob=True,  # Faster for large datasets (requires admin)
    skip_zeros=True,  # Exclude zero values
    skip_consolidated_cells=True  # Exclude C-level cells
)
```

See `references/DATA_OPERATIONS.md` for advanced reading patterns.

### Task 3: Write Data to Cubes

#### Write Cell Values

```python
# Write a single value
tm1.cells.write_value(
    value=12345.67,
    cube_name='SalesCube',
    element_tuple=('ProductA', '2024-Q1', 'Revenue')
)

# Write multiple values
cellset = {
    ('ProductA', '2024-Q1', 'Revenue'): 12345,
    ('ProductB', '2024-Q1', 'Revenue'): 23456,
    ('ProductA', '2024-Q2', 'Revenue'): 34567
}

tm1.cells.write(
    cube_name='SalesCube',
    cellset_as_dict=cellset,
    dimensions=['Product', 'Period', 'Measure']  # Optional but improves performance
)
```

#### Write from DataFrame

```python
import pandas as pd

# DataFrame with cube structure
df = pd.DataFrame({
    'Product': ['ProductA', 'ProductB', 'ProductA'],
    'Period': ['2024-Q1', '2024-Q1', '2024-Q2'],
    'Measure': ['Revenue', 'Revenue', 'Revenue'],
    'Value': [12345, 23456, 34567]
})

tm1.cells.write_dataframe(
    cube_name='SalesCube',
    data=df
)
```

#### High-Performance Writes

```python
# Use TI process for bulk writes (requires admin permissions)
tm1.cells.write(
    cube_name='SalesCube',
    cellset_as_dict=large_cellset,
    use_ti=True  # Or use_blob=True for even better performance
)

# Async write for parallel processing
tm1.cells.write_async(
    cube_name='SalesCube',
    cells=very_large_cellset,
    max_workers=8,  # Number of parallel threads
    slice_size=250000  # Cells per thread
)
```

See `references/PERFORMANCE.md` for optimization strategies.

### Task 4: Manage Dimensions and Hierarchies

#### Get Dimension Information

```python
# Check if dimension exists
if tm1.dimensions.exists('Product'):
    print("Product dimension exists")

# Get dimension object
dim = tm1.dimensions.get('Product')
print(f"Dimension: {dim.name}")
print(f"Hierarchies: {dim.hierarchy_names}")

# Get all dimension names
all_dims = tm1.dimensions.get_all_names()
```

#### Work with Elements

```python
# Get all elements
elements = tm1.elements.get_element_names(
    dimension_name='Product',
    hierarchy_name='Product'
)

# Get elements as DataFrame
df = tm1.elements.get_elements_dataframe(
    dimension_name='Product',
    hierarchy_name='Product',
    skip_consolidations=False,
    attributes=['Description', 'Category']  # Include attributes
)

# Create a new element
from TM1py import Element

element = Element(name='ProductC', element_type='Numeric')
tm1.elements.create(
    dimension_name='Product',
    hierarchy_name='Product',
    element=element
)

# Add edge (parent-child relationship)
tm1.elements.add_edge(
    dimension_name='Product',
    hierarchy_name='Product',
    parent='All Products',
    component='ProductC',
    weight=1
)
```

See `references/METADATA_MANAGEMENT.md` for CRUD operations and `references/METADATA_MANAGEMENT_ADVANCED.md` for advanced patterns.

### Task 5: Execute TI Processes

#### Execute Process

```python
# Execute process without parameters
success, status, error_log = tm1.processes.execute_with_return(
    process_name='RefreshData'
)

if success:
    print("Process completed successfully")
else:
    print(f"Process failed: {error_log}")

# Execute with parameters
success, status, error_log = tm1.processes.execute_with_return(
    process_name='LoadData',
    pYear='2024',
    pMonth='01'
)
```

#### Execute Loose TI Code

```python
# Execute TI statements directly
prolog = [
    "sYear = '2024';",
    "sMessage = 'Processing year: ' | sYear;",
    "TextOutput('TM1ProcessError.log', sMessage);"
]

epilog = [
    "TextOutput('TM1ProcessError.log', 'Process completed');"
]

tm1.processes.execute_ti_code(lines_prolog=prolog, lines_epilog=epilog)
```

### Task 6: Work with Cubes

#### Get Cube Information

```python
# Get cube
cube = tm1.cubes.get('SalesCube')
print(f"Dimensions: {cube.dimensions}")
print(f"Has Rules: {cube.has_rules}")

# Get all cube names
all_cubes = tm1.cubes.get_all_names(skip_control_cubes=True)
```

#### Create a Cube

```python
from TM1py import Cube

# Create new cube
cube = Cube(
    name='NewSalesCube',
    dimensions=['Product', 'Period', 'Measure', 'Version']
)

tm1.cubes.create(cube)
```

## Examples

### Example 1: Export Cube Data to CSV

```python
# Read data and export to CSV
df = tm1.cells.execute_view_dataframe(
    cube_name='SalesCube',
    view_name='ExportView',
    private=False,
    skip_zeros=True
)

df.to_csv('sales_data.csv', index=False)
print(f"Exported {len(df)} rows to sales_data.csv")
```

### Example 2: Bulk Update with Error Handling

```python
# Safe bulk write with validation
try:
    success, status, error_log = tm1.processes.execute_with_return(
        process_name='LoadSalesData',
        pYear='2024',
        pRegion='EMEA'
    )
    
    if success:
        print(f"Process completed: {status}")
    else:
        print(f"Process failed, check: {error_log}")
        
except Exception as e:
    print(f"Error executing process: {str(e)}")
```

See `references/EXAMPLES.md` for more complex automation patterns and use cases.

## Troubleshooting

### Connection Failed
- **Check**: Server address, port, SSL settings (`ssl=True`/`False`), credentials
- **IBM Cloud**: Use `async_requests_mode=True` to avoid 60s timeout
- **SSL Issues**: Set `verify=False` for self-signed certificates (not production)

### MDX Query Returns No Data
- **Verify**: MDX syntax, element names, user READ permissions
- **Try**: `skip_zeros=False`, test query in PA Workspace first

### Write Operation Fails  
- **Check**: WRITE permissions, cells not rule-derived, elements exist
- **Use**: `skip_non_updateable=True` to skip rule cells
- **Note**: Consolidated cells spread data proportionally

### Performance Issues
- **Use**: `use_blob=True` (requires admin), async operations
- **Enable**: `skip_zeros=True`, `skip_consolidated_cells=True`
- **Optimize**: Specify dimensions explicitly, use views over MDX

### Import Errors
- **Install**: `pip install "tm1py[pandas]"` (Python 3.7+)
- **Fix**: Check virtual environment, reinstall if needed

## Best Practices

1. **Always use context managers** (`with` statement) for automatic cleanup
2. **Specify dimensions explicitly** in cell operations for better performance
3. **Use DataFrames** for bulk operations when pandas is available
4. **Leverage async operations** for parallel processing of large datasets
5. **Handle errors** with try-except blocks and check return values
6. **Close connections** explicitly if not using context managers
7. **Use service accounts** for automation (not personal accounts)
8. **Log operations** for audit trails and debugging
9. **Test in development** before deploying to production
10. **Keep TM1py updated** for latest features and bug fixes

## Reference Files

For detailed information, consult these reference documents:

- **API_REFERENCE.md**: Complete service-by-service API documentation with all methods and parameters
- **CONNECTION_GUIDE.md**: Connection patterns for all TM1 environments (on-prem, cloud, TM1 12)
- **DATA_OPERATIONS.md**: Deep dive into reading and writing data with all options and optimizations
- **METADATA_MANAGEMENT.md**: Comprehensive guide to CRUD operations for all TM1 objects
- **METADATA_MANAGEMENT_ADVANCED.md**: Advanced metadata patterns and reusable workflows
- **PERFORMANCE.md**: Performance optimization techniques, async operations, and benchmarking
- **EXAMPLES.md**: Extended code samples and real-world use cases

## Additional Resources

- **Official Documentation**: [https://tm1py.org/](https://tm1py.org/)
- **GitHub Repository**: [https://github.com/cubewise-code/tm1py](https://github.com/cubewise-code/tm1py)
- **Sample Scripts**: [https://github.com/cubewise-code/tm1py-samples](https://github.com/cubewise-code/tm1py-samples)
- **TM1 REST API Docs**: [IBM Planning Analytics REST API](https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=analytics-tm1-rest-api)
- **PyPI Package**: [https://pypi.org/project/TM1py/](https://pypi.org/project/TM1py/)
