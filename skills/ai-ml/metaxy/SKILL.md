---
name: metaxy
description: This skill should be used when the user asks to "define a feature", "create a BaseFeature class", "track feature versions", "set up metadata store", "field-level dependencies", "FieldSpec", "FeatureDep", "run metaxy CLI", "metaxy migrations", or needs guidance on metaxy feature definitions, versioning, metadata stores, CLI commands, or testing patterns.
---

# Metaxy

Metaxy is a metadata layer for multi-modal Data and ML pipelines that manages and tracks feature versions, dependencies, and data lineage across complex computational graphs.

## Core Concepts

### Feature Definitions

To define a feature, create a class inheriting from `mx.BaseFeature` with a `FeatureSpec` metaclass argument:

```python
import metaxy as mx


class MyFeature(
    mx.BaseFeature,
    spec=mx.FeatureSpec(
        key="my/feature",
        id_columns=["sample_id"],
        fields=["embedding", "score"],
    ),
):
    sample_id: str
    embedding: list[float]
    score: float
```

To add dependencies between features, use the `deps` parameter with `FeatureDep`. To specify field-level dependencies (for partial data dependencies processing), use `FieldSpec` with `FieldDep` or `FieldsMapping`.

### Data Versioning

Metaxy automatically tracks sample versions and propagates changes through the dependency graph. To trigger recomputation when code changes, set `code_version` on `FieldSpec`:

```python
fields = [
    mx.FieldSpec(key="embedding", code_version="2"),  # Bump to invalidate downstream
]
```

### Metadata Stores

To configure a metadata store, create a `metaxy.toml` file or use programmatic configuration:

```python
with mx.MetaxyConfig(stores={"dev": mx.DeltaMetadataStore(root_path="/tmp/metaxy")}).use() as config:
    store = config.get_store("dev")
```

Supported backends: DuckDB, ClickHouse, BigQuery, LanceDB, Delta Lake.

### Feature Graph

To visualize and manage the feature dependency graph, use the CLI:

```bash
mx graph render            # Terminal visualization
mx graph push --store dev  # Push graph to store
```

## CLI

Metaxy provides a CLI (`metaxy` or `mx` alias) for managing features, metadata, and migrations:

```bash
mx list features --verbose     # List features with dependencies
mx graph render                # Visualize feature graph
mx metadata status --all-features  # Check metadata freshness (expensive!)
mx migrations apply            # Apply pending migrations
mx mcp                         # Start MCP server for AI assistants
```

## Testing

To test features in isolation, use context managers to avoid polluting the global registry:

```python
import pytest
import metaxy as mx
from metaxy.metadata_store.delta import DeltaMetadataStore


@pytest.fixture
def metaxy_env(tmp_path):
    with mx.FeatureGraph().use():
        store = DeltaMetadataStore(root_path=tmp_path / "delta_test")
        with mx.MetaxyConfig(stores={"test": store}).use() as config:
            yield config
```

## Examples

For complete code examples, see:

- `examples/feature-definitions.md` - Feature classes with dependencies and field-level deps
- `examples/configuration.md` - TOML and programmatic configuration
- `examples/metadata-stores.md` - Store operations
- `examples/testing.md` - Test isolation patterns
- `examples/cli.md` - CLI command reference

## Documentation

For comprehensive documentation: https://anam-org.github.io/metaxy/

Key pages:

- **Quickstart**: https://anam-org.github.io/metaxy/guide/overview/quickstart/
- **Feature Definitions**: https://anam-org.github.io/metaxy/guide/learn/feature-definitions/
- **Data Versioning**: https://anam-org.github.io/metaxy/guide/learn/data-versioning/
- **Metadata Stores**: https://anam-org.github.io/metaxy/guide/learn/metadata-stores/
- **CLI Reference**: https://anam-org.github.io/metaxy/reference/cli/
- **API Reference**: https://anam-org.github.io/metaxy/reference/api/
