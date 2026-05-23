---
name: pyiceberg-storage
description: ALWAYS USE when working with Iceberg table storage, ACID transactions, or time-travel queries. Use IMMEDIATELY when creating/loading Iceberg tables, implementing schema evolution, querying historical snapshots, or debugging catalog operations. Provides research steps for PyIceberg SDK, catalog integration, and storage layer operations.
---

# PyIceberg Storage Development (Research-Driven)

## ⚠️ CRITICAL: Catalog-as-Control-Plane

**NEVER write directly to storage.** ALL Iceberg table operations MUST flow through the catalog (Polaris/Glue):

```
❌ FORBIDDEN: PyIceberg → S3 (bypasses catalog coordination)
✅ CORRECT:   PyIceberg → Polaris Catalog → S3 (catalog coordinates writes)
```

**Why?**
- ACID transactions require catalog coordination
- Schema evolution tracked by catalog
- Access control enforced at catalog layer
- Multi-engine interoperability (DuckDB, Spark, dbt all see same metadata)

**See**: [ADR-0005](docs/architecture/adr/0005-iceberg-table-format.md) - Apache Iceberg Enforced

## Related ADRs

| ADR | Decision | Relevance |
|-----|----------|-----------|
| [ADR-0005](docs/architecture/adr/0005-iceberg-table-format.md) | Apache Iceberg Enforced | All tables MUST be Iceberg format |
| [ADR-0034](docs/architecture/adr/0034-dbt-duckdb-iceberg.md) | dbt-duckdb Workaround | Inline credentials for ATTACH |
| [ADR-0010](docs/architecture/adr/0010-target-agnostic-compute.md) | Target-Agnostic Compute | PyIceberg supports all compute targets |

## Philosophy

This skill does NOT prescribe specific Iceberg table patterns. Instead, it guides you to:
1. **Research** the current PyIceberg version and capabilities
2. **Discover** existing Iceberg table usage in the codebase
3. **Validate** your implementations against PyIceberg SDK documentation
4. **Verify** integration with Polaris catalog and storage layer

## Pre-Implementation Research Protocol

### Step 1: Verify Runtime Environment

**ALWAYS run this first**:
```bash
python -c "import pyiceberg; print(f'PyIceberg {pyiceberg.__version__}')"
```

**Critical Questions to Answer**:
- What version is installed? (0.10.x recommended as of 2025)
- Are required dependencies installed? (pyarrow, fsspec, cloud SDKs)
- Does it match the documented requirements?

### Step 2: Research SDK State (if unfamiliar)

**When to research**: If you encounter unfamiliar PyIceberg features or need to validate patterns

**Research queries** (use WebSearch):
- "PyIceberg [feature] documentation 2025" (e.g., "PyIceberg ACID transactions 2025")
- "PyIceberg catalog REST API configuration 2025"
- "PyIceberg [cloud] integration 2025" (e.g., "PyIceberg AWS S3 integration 2025")

**Official documentation**: https://py.iceberg.apache.org

**Key documentation sections**:
- API Reference: https://py.iceberg.apache.org/reference/
- Configuration: https://py.iceberg.apache.org/configuration/
- Table Operations: https://py.iceberg.apache.org/reference/pyiceberg/table/

### Step 3: Discover Existing Patterns

**BEFORE creating new Iceberg operations**, search for existing implementations:

```bash
# Find existing PyIceberg usage
rg "from pyiceberg|import pyiceberg" --type py

# Find catalog configurations
rg "load_catalog|Catalog" --type py

# Find table operations
rg "\.load_table|\.create_table" --type py

# Find transaction usage
rg "\.transaction|\.append|\.overwrite" --type py
```

**Key questions**:
- What catalog is configured? (REST, Hive, Glue, etc.)
- What storage is used? (S3, Azure, GCS, local filesystem)
- What table operations are already implemented?
- How are schemas defined?

### Step 4: Validate Against Architecture

Check architecture docs for integration requirements:
- Read `/docs/` for Iceberg storage requirements
- Understand Polaris catalog integration
- Verify compute targets and storage mappings
- Check partition strategy requirements

## Implementation Guidance (Not Prescriptive)

### Catalog Configuration

**Core concept**: Catalogs manage Iceberg table metadata and coordinate with storage

**Research questions**:
- What catalog type should be used? (REST for Polaris, Hive, Glue)
- How should credentials be managed? (vended credentials, access delegation)
- What warehouse configuration is needed?
- How should catalog be initialized in code?

**SDK features to research**:
- `load_catalog()`: Initialize catalog from configuration
- REST catalog: Connection to Polaris or other REST APIs
- Catalog types: `rest`, `hive`, `glue`, `dynamodb`, `sql`
- Configuration: YAML files, environment variables, Python dicts

### Table Operations

**Core concept**: Tables represent datasets with schema, partitioning, and ACID guarantees

**Research questions**:
- Should I create a new table or load existing?
- What schema should the table have?
- What partitioning strategy? (time-based, dimension-based)
- What sort order for performance?

**SDK features to research**:
- `catalog.create_table()`: Create new Iceberg table
- `catalog.load_table()`: Load existing table
- `table.scan()`: Query table data
- `table.schema()`: Get table schema
- `table.spec()`: Get partition spec
- `table.properties()`: Get table properties

### ACID Transactions

**Core concept**: Iceberg uses optimistic concurrency and snapshots for ACID guarantees

**Research questions**:
- What operation am I performing? (append, overwrite, delete)
- Do I need transactional guarantees?
- How should concurrent writes be handled?
- What snapshot isolation level is needed?

**SDK features to research**:
- `table.append()`: Append data (creates APPEND snapshot)
- `table.overwrite()`: Overwrite data (creates OVERWRITE snapshot)
- `table.delete()`: Delete data (creates DELETE snapshot)
- Transaction API: Stage changes before committing
- Optimistic concurrency: Snapshot-based isolation

### Schema Evolution

**Core concept**: Iceberg supports safe schema changes without rewriting data

**Research questions**:
- What schema changes are needed? (add column, rename, type promotion)
- Are changes backward compatible?
- How should schema evolution be tracked?
- What validation is needed?

**SDK features to research**:
- `table.update_schema()`: Modify table schema
- Schema operations: `add_column()`, `rename_column()`, `update_column()`
- Type promotion: Safe type changes (int → long, float → double)
- Schema versioning: Iceberg tracks schema evolution

### Partitioning

**Core concept**: Partitioning improves query performance by organizing data

**Research questions**:
- What partition strategy? (daily, hourly, by dimension)
- What columns should be partition keys?
- Should partitioning be hidden (partition transforms)?
- How does partitioning affect queries?

**SDK features to research**:
- Partition specs: Define partitioning strategy
- Partition transforms: `day()`, `hour()`, `month()`, `year()`, `bucket()`, `truncate()`
- Hidden partitioning: Partition transforms applied automatically
- Dynamic partitioning: Partitions created as data arrives

### Time Travel

**Core concept**: Iceberg snapshots enable querying historical data

**Research questions**:
- What snapshot should be queried? (timestamp, snapshot ID)
- How far back does history need to go?
- Should old snapshots be expired?
- What metadata is available in snapshots?

**SDK features to research**:
- `table.scan().use_ref()`: Query specific snapshot/tag/branch
- `table.history()`: List table snapshots
- `table.refs()`: List named references (branches, tags)
- Snapshot expiration: Clean up old snapshots

### Data I/O

**Core concept**: PyIceberg reads/writes data using PyArrow and fsspec

**Research questions**:
- What data format? (Parquet, Avro, ORC)
- What file system? (S3, Azure, GCS, local)
- How should data be batched?
- What compression should be used?

**SDK features to research**:
- `table.scan().to_arrow()`: Read data as PyArrow Table
- `table.scan().to_pandas()`: Read data as Pandas DataFrame
- `table.scan().to_duckdb()`: Read data into DuckDB
- FileIO implementations: S3, Azure, GCS, fsspec
- Data file formats: Parquet (recommended), Avro, ORC

## Validation Workflow

### Before Implementation
1. ✅ Verified PyIceberg version and dependencies
2. ✅ Searched for existing catalog and table configurations
3. ✅ Read architecture docs for Polaris integration
4. ✅ Identified storage layer (S3, Azure, GCS)
5. ✅ Researched unfamiliar PyIceberg features

### During Implementation
1. ✅ Using `load_catalog()` with proper configuration
2. ✅ Type hints on ALL functions and parameters
3. ✅ Proper error handling for catalog/table operations
4. ✅ Transaction API for ACID guarantees
5. ✅ Schema evolution following Iceberg best practices
6. ✅ Partitioning strategy aligned with query patterns

### After Implementation
1. ✅ Verify catalog connection works
2. ✅ Test table creation/loading
3. ✅ Test data write operations (append, overwrite)
4. ✅ Test data read operations (scan, time travel)
5. ✅ Verify schema evolution works
6. ✅ Check integration with dbt/Dagster (if applicable)

## Context Injection (For Future Claude Instances)

When this skill is invoked, you should:

1. **Verify runtime state** (don't assume):
   ```bash
   python -c "import pyiceberg; print(pyiceberg.__version__)"
   ```

2. **Discover existing patterns** (don't invent):
   ```bash
   rg "load_catalog" --type py
   rg "\.load_table|\.create_table" --type py
   ```

3. **Research when uncertain** (don't guess):
   - Use WebSearch for "PyIceberg [feature] documentation 2025"
   - Check official docs: https://py.iceberg.apache.org

4. **Validate against architecture** (don't assume requirements):
   - Read relevant architecture docs in `/docs/`
   - Understand Polaris catalog integration
   - Check storage layer configuration

5. **Check Polaris integration** (if using REST catalog):
   - Verify Polaris endpoint configuration
   - Check credential management (vended credentials)
   - Understand access delegation model

## Quick Reference: Common Research Queries

Use these WebSearch queries when encountering specific needs:

- **Catalog setup**: "PyIceberg REST catalog configuration 2025"
- **Polaris integration**: "PyIceberg Polaris catalog integration 2025"
- **Table operations**: "PyIceberg create table append data 2025"
- **ACID transactions**: "PyIceberg transaction API ACID guarantees 2025"
- **Schema evolution**: "PyIceberg schema evolution add column 2025"
- **Partitioning**: "PyIceberg partition transforms hidden partitioning 2025"
- **Time travel**: "PyIceberg snapshot time travel query 2025"
- **AWS S3**: "PyIceberg S3 FileIO configuration 2025"
- **Azure**: "PyIceberg Azure Blob Storage configuration 2025"
- **GCS**: "PyIceberg Google Cloud Storage configuration 2025"

## Integration Points to Research

### Polaris Catalog Integration

**Key question**: How does PyIceberg connect to Polaris REST catalog?

Research areas:
- REST catalog configuration (`type: rest`, `uri`, `warehouse`)
- Credential management (`credential`, `token-refresh-enabled`)
- Access delegation (`header.X-Iceberg-Access-Delegation: vended-credentials`)
- Scope and permissions (`scope: PRINCIPAL_ROLE:ALL`)
- FileIO implementation (`py-io-impl: pyiceberg.io.fsspec.FsspecFileIO`)

### dbt → PyIceberg Integration

**Key question**: How do dbt models write to Iceberg tables?

Research areas:
- dbt Python models using PyIceberg
- External tables (dbt creates views, PyIceberg writes data)
- Post-hooks for Iceberg table creation
- Schema mapping (dbt schema → Iceberg schema)

### Dagster → PyIceberg Integration

**Key question**: How do Dagster assets materialize Iceberg tables?

Research areas:
- Custom IOManager for Iceberg tables
- PyIceberg in asset functions
- Partition mapping (Dagster partitions → Iceberg partitions)
- Metadata propagation (Dagster metadata → Iceberg properties)

### Storage Layer Configuration

**Key question**: How is cloud storage configured for Iceberg?

Research areas:
- S3 configuration (bucket, region, credentials)
- Azure Blob Storage configuration
- Google Cloud Storage configuration
- Local filesystem for development
- Vended credentials vs static credentials

## PyIceberg Development Workflow

### Local Development
```bash
# Install PyIceberg with extras
pip install "pyiceberg[s3,pyarrow,pandas,duckdb]"

# Verify installation
python -c "import pyiceberg; print(pyiceberg.__version__)"

# Test catalog connection
python -c "from pyiceberg.catalog import load_catalog; catalog = load_catalog('default')"
```

### Example: Load Catalog and Query Table
```python
from pyiceberg.catalog import load_catalog

# Load catalog from configuration
catalog = load_catalog(
    "polaris_catalog",
    **{
        "type": "rest",
        "uri": "https://account.snowflakecomputing.com/polaris/api/catalog",
        "credential": "client_id:client_secret",
        "warehouse": "my_warehouse",
    }
)

# Load table
table = catalog.load_table("my_namespace.my_table")

# Query data
df = table.scan().to_pandas()
```

### Example: Create Table and Write Data
```python
from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, IntegerType
import pyarrow as pa

# Define schema
schema = Schema(
    NestedField(1, "id", IntegerType(), required=True),
    NestedField(2, "name", StringType(), required=False),
)

# Create table
table = catalog.create_table(
    "my_namespace.my_new_table",
    schema=schema,
)

# Append data
data = pa.table({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
})
table.append(data)
```

## References

- [PyIceberg Documentation](https://py.iceberg.apache.org): Official documentation
- [PyIceberg on PyPI](https://pypi.org/project/pyiceberg/): Package information
- [Configuration Guide](https://py.iceberg.apache.org/configuration/): Catalog and storage config
- [API Reference](https://py.iceberg.apache.org/reference/): Complete API documentation
- [GitHub Repository](https://github.com/apache/iceberg-python): PyIceberg source
- [Apache Iceberg Spec](https://iceberg.apache.org/spec/): Iceberg table format specification

---

**Remember**: This skill provides research guidance, NOT prescriptive patterns. Always:
1. Verify the PyIceberg version and dependencies
2. Discover existing catalog and table configurations
3. Research SDK capabilities when needed (use WebSearch liberally)
4. Validate against actual Polaris integration requirements
5. Test catalog connection and table operations before considering complete
6. Understand ACID guarantees and snapshot isolation for correctness
