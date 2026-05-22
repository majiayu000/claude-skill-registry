---
name: dbt-transformations
description: ALWAYS USE when working with dbt models, SQL transformations, tests, snapshots, or macros. Use IMMEDIATELY when editing dbt_project.yml, profiles.yml, or creating SQL models. MUST be loaded before any transform-layer work. Enforces dbt owns SQL principle - never parse, validate, or transform SQL in Python.
---

# dbt Core Development (Research-Driven)

## Philosophy

This skill does NOT prescribe specific SQL patterns or dbt project structures. Instead, it guides you to:
1. **Research** the current dbt Core version and capabilities
2. **Discover** existing dbt project patterns in the codebase
3. **Validate** your implementations against dbt documentation
4. **Verify** integration with Dagster orchestration and Iceberg storage

**CRITICAL**: dbt **owns SQL**. Never parse, validate, or transform SQL in Python. Let dbt handle all SQL dialect translation and execution.

## Pre-Implementation Research Protocol

### Step 1: Verify Runtime Environment

**ALWAYS run this first**:
```bash
dbt --version
python -c "import dbt.version; print(f'dbt-core {dbt.version.__version__}')"
```

**Critical Questions to Answer**:
- What version is installed? (1.x series recommended)
- What adapters are installed? (duckdb, snowflake, bigquery, etc.)
- Does it match the documented requirements?

### Step 2: Research SDK State (if unfamiliar)

**When to research**: If you encounter unfamiliar dbt features or need to validate patterns

**Research queries** (use WebSearch):
- "dbt Core [feature] documentation 2025" (e.g., "dbt Core snapshots documentation 2025")
- "dbt programmatic invocation dbtRunner 2025"
- "dbt [adapter] configuration 2025" (e.g., "dbt duckdb configuration 2025")

**Official documentation**: https://docs.getdbt.com

**Key documentation sections**:
- Models: https://docs.getdbt.com/docs/build/models
- Tests: https://docs.getdbt.com/docs/build/data-tests
- Snapshots: https://docs.getdbt.com/docs/build/snapshots
- Programmatic invocations: https://docs.getdbt.com/reference/programmatic-invocations

### Step 3: Discover Existing Patterns

**BEFORE creating new dbt resources**, search for existing implementations:

```bash
# Find dbt project directories
find . -name "dbt_project.yml"

# Find existing models
find . -path "*/models/*.sql" -o -path "*/models/*.py"

# Find existing tests
find . -path "*/tests/*.sql"

# Find macros
find . -path "*/macros/*.sql"

# Check profiles.yml location
echo $DBT_PROFILES_DIR
find . -name "profiles.yml"
```

**Key questions**:
- What dbt project structure exists?
- What naming conventions are used for models?
- What adapters are configured in profiles.yml?
- What macros or custom tests exist?

### Step 4: Validate Against Architecture

Check architecture docs for integration requirements:
- Read `/docs/` for CompiledArtifacts contract (dbt paths, profiles)
- Understand compute targets (how they map to dbt profiles)
- Verify Iceberg integration requirements
- Check governance requirements (classification metadata in model `meta`)

## Implementation Guidance (Not Prescriptive)

### dbt Project Structure

**Core concept**: dbt projects organize transformations into models, tests, snapshots, seeds, and macros

**Research questions**:
- Where should the dbt project live? (monorepo package structure)
- What directory structure makes sense? (staging, intermediate, marts)
- How should models be organized? (by source system, by domain)
- What naming conventions should be used?

**SDK features to research**:
- `dbt_project.yml`: Project configuration
- `profiles.yml`: Connection profiles for compute targets
- Model directories: `models/staging/`, `models/marts/`
- Resource paths: `analysis-paths`, `test-paths`, `macro-paths`

### Models (SQL and Python)

**Core concept**: Models are SELECT statements that create tables/views in the data warehouse

**Research questions**:
- Should this be a SQL or Python model?
- What materialization? (table, view, incremental, ephemeral)
- What dependencies exist? (use `{{ ref('model_name') }}`)
- What sources? (use `{{ source('source_name', 'table_name') }}`)

**SDK features to research**:
- SQL models: `.sql` files with Jinja templating
- Python models: `.py` files with `dbt.ref()` and `dbt.source()`
- Materializations: `{{ config(materialized='table') }}`
- Incremental models: `is_incremental()`, incremental strategies
- Model configurations: tags, meta, pre/post hooks

### Tests

**Core concept**: Tests assert data quality on models, sources, seeds, and snapshots

**Research questions**:
- What data quality assertions are needed?
- Should I use generic tests (unique, not_null) or singular tests?
- What custom tests are needed?
- How should test severity be configured? (warn vs error)

**SDK features to research**:
- Generic tests: `unique`, `not_null`, `accepted_values`, `relationships`
- Singular tests: SQL files in `tests/` directory
- Custom generic tests: Macros in `macros/` with `{% test %}`
- Test configurations: `severity`, `error_if`, `warn_if`

### Snapshots

**Core concept**: Snapshots capture Type 2 slowly changing dimensions (historical records)

**Research questions**:
- What tables need historical tracking?
- What snapshot strategy? (timestamp, check)
- How should snapshot metadata be named?
- What should happen to hard deletes?

**SDK features to research**:
- Snapshot strategies: `timestamp`, `check`
- YAML configuration (v1.9+): cleaner snapshot setup
- `snapshot_meta_column_names`: Customize dbt_valid_from, dbt_valid_to
- `hard_deletes`: `ignore`, `invalidate`, `new_record`

### Sources

**Core concept**: Sources represent raw tables in external systems

**Research questions**:
- What raw data sources exist?
- How should source freshness be validated?
- What source metadata is needed?
- Should source tests be added?

**SDK features to research**:
- `sources.yml`: Source definitions
- `{{ source('source_name', 'table_name') }}`: Referencing sources
- Source freshness: `loaded_at_field`, `freshness` checks
- Source tests: Generic tests on source columns

### Macros

**Core concept**: Macros are reusable SQL snippets (Jinja templates)

**Research questions**:
- What SQL patterns are repeated?
- Should I create a custom generic test?
- Are there adapter-specific needs?

**SDK features to research**:
- Macro syntax: `{% macro name(args) %}`
- `{{ return() }}`: Returning values from macros
- Adapter dispatch: `adapter.dispatch()`
- Package macros: `dbt_utils`, custom packages

### Programmatic Invocation (Python API)

**Core concept**: dbtRunner allows calling dbt commands from Python (for Dagster integration)

**Research questions**:
- What dbt commands need to be run from Python? (compile, run, test)
- How should errors be handled?
- Should manifest be cached for performance?
- What context is needed (profiles dir, project dir, target)?

**SDK features to research**:
- `dbtRunner`: Entry point for programmatic invocation
- `dbtRunnerResult`: Return object with results and exceptions
- `.invoke(cli_args)`: Execute dbt commands
- Manifest reuse: Avoid reparsing for performance

**CRITICAL**: dbt-core does NOT support safe parallel execution in the same process

## Validation Workflow

### Before Implementation
1. ✅ Verified dbt Core version and adapter
2. ✅ Searched for existing dbt project structure
3. ✅ Read architecture docs for compute targets and profiles
4. ✅ Identified data sources and transformation requirements
5. ✅ Researched unfamiliar dbt features

### During Implementation
1. ✅ SQL models using Jinja (`{{ ref() }}`, `{{ source() }}`)
2. ✅ Proper materialization configured for performance
3. ✅ Tests added for data quality (generic and singular)
4. ✅ Metadata added to model `meta` for governance (classifications)
5. ✅ Dependencies correctly specified
6. ✅ **NEVER parse or validate SQL in Python** (dbt owns SQL)

### After Implementation
1. ✅ Run `dbt debug` to verify connection
2. ✅ Run `dbt compile` to verify SQL generation
3. ✅ Run `dbt run --select model_name` to test model
4. ✅ Run `dbt test` to validate data quality
5. ✅ Check `target/manifest.json` for metadata
6. ✅ Verify integration with Dagster (if applicable)

## Context Injection (For Future Claude Instances)

When this skill is invoked, you should:

1. **Verify runtime state** (don't assume):
   ```bash
   dbt --version
   dbt debug  # Verify connection to target
   ```

2. **Discover existing patterns** (don't invent):
   ```bash
   find . -name "dbt_project.yml"
   find . -path "*/models/*.sql"
   ```

3. **Research when uncertain** (don't guess):
   - Use WebSearch for "dbt Core [feature] documentation 2025"
   - Check official docs: https://docs.getdbt.com

4. **Validate against architecture** (don't assume requirements):
   - Read relevant architecture docs in `/docs/`
   - Understand compute targets and how they map to dbt profiles
   - Check CompiledArtifacts contract for dbt paths

5. **NEVER parse SQL** (dbt owns SQL):
   - Don't validate SQL syntax in Python
   - Don't transform SQL dialects manually
   - Let dbt handle all SQL compilation and execution

## Quick Reference: Common Research Queries

Use these WebSearch queries when encountering specific needs:

- **Models**: "dbt Core models materialization documentation 2025"
- **Incremental models**: "dbt Core incremental models strategies 2025"
- **Tests**: "dbt Core data tests custom tests 2025"
- **Snapshots**: "dbt Core snapshots YAML configuration 2025"
- **Sources**: "dbt Core sources freshness documentation 2025"
- **Macros**: "dbt Core macros Jinja examples 2025"
- **Programmatic invocation**: "dbt Core dbtRunner programmatic invocation 2025"
- **Adapters**: "dbt [adapter] configuration 2025" (e.g., "dbt duckdb configuration 2025")
- **Python models**: "dbt Core Python models documentation 2025"
- **Governance**: "dbt Core model meta tags documentation 2025"

## Integration Points to Research

### CompiledArtifacts → dbt profiles.yml

**Key question**: How does CompiledArtifacts generate profiles.yml?

Research areas:
- What compute targets are defined in CompiledArtifacts?
- How do compute types map to dbt adapters? (duckdb, snowflake, bigquery)
- Where should profiles.yml be written? (DBT_PROFILES_DIR)
- What connection parameters are needed for each adapter?

### dbt → Dagster Integration

**Key question**: How are dbt models represented as Dagster assets?

Research areas:
- `dagster-dbt` library usage
- `load_assets_from_dbt_manifest()` vs `load_assets_from_dbt_project()`
- dbtRunner for programmatic invocation
- Manifest.json location (target/manifest.json)
- Metadata extraction (model meta, column classifications)

### dbt → Iceberg Storage

**Key question**: How do dbt models write to Iceberg tables?

Research areas:
- dbt adapter for Iceberg (does one exist?)
- External tables pattern (dbt creates views, separate process writes Iceberg)
- Python models writing to PyIceberg
- Post-hooks for Iceberg table creation

### Governance Metadata (dbt meta)

**Key question**: How should classifications be tagged in dbt models?

Research areas:
- Model-level meta tags
- Column-level meta tags
- Custom schema tests for governance
- Metadata extraction in CompiledArtifacts

## dbt Development Workflow

### Local Development
```bash
# Install dbt with adapter
pip install dbt-core dbt-duckdb

# Verify installation
dbt --version

# Initialize project (if needed)
dbt init my_project

# Verify connection
dbt debug

# Compile models (generate SQL)
dbt compile

# Run models
dbt run

# Run specific model
dbt run --select my_model

# Test data quality
dbt test

# Generate documentation
dbt docs generate
dbt docs serve  # View at localhost:8080
```

### Programmatic Invocation (Python)
```python
from dbt.cli.main import dbtRunner, dbtRunnerResult

# Initialize runner
dbt = dbtRunner()

# Run dbt command
cli_args = ["run", "--select", "tag:daily"]
res: dbtRunnerResult = dbt.invoke(cli_args)

# Check results
if res.success:
    for r in res.result:
        print(f"{r.node.name}: {r.status}")
else:
    print(f"Error: {res.exception}")
```

## References

- [dbt Documentation](https://docs.getdbt.com): Official documentation
- [dbt Core on PyPI](https://pypi.org/project/dbt-core/): Package information
- [Programmatic Invocations](https://docs.getdbt.com/reference/programmatic-invocations): dbtRunner API
- [Models](https://docs.getdbt.com/docs/build/models): Model documentation
- [Tests](https://docs.getdbt.com/docs/build/data-tests): Testing documentation
- [Snapshots](https://docs.getdbt.com/docs/build/snapshots): Snapshot documentation
- [GitHub Repository](https://github.com/dbt-labs/dbt-core): dbt-core source

---

**Remember**: This skill provides research guidance, NOT prescriptive SQL patterns. Always:
1. Verify the dbt version and adapter compatibility
2. Discover existing dbt project structure and conventions
3. Research dbt capabilities when needed (use WebSearch liberally)
4. Validate against actual CompiledArtifacts contract requirements
5. **NEVER parse or validate SQL in Python** - dbt owns SQL
6. Test with `dbt run` and `dbt test` before considering complete
