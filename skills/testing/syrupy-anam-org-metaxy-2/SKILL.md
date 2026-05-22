---
name: syrupy
description: Use syrupy for pytest snapshot testing to ensure the immutability of computed results, manage snapshots, customize serialization, and handle complex data structures with built-in matchers and filters.
---

# Syrupy - Pytest Snapshot Testing

Syrupy is a zero-dependency pytest snapshot testing plugin that enables asserting the immutability of computed results through simple, idiomatic assertions.

Docs: https://syrupy-project.github.io/syrupy/

## What is Syrupy?

Syrupy is a snapshot testing library that:

- Captures the output/state of code at a point in time
- Compares future test runs against saved snapshots
- Automatically manages snapshot files in `__snapshots__` directories
- Integrates naturally with pytest's assertion syntax

## Core Philosophy

**Three Design Principles:**

1. **Extensible**: Easy to add support for custom/unsupported data types
2. **Idiomatic**: Natural pytest-style assertions (`assert x == snapshot`)
3. **Sound**: Fails tests if snapshots are missing or different

**Target Use Case:**
Testing complex data structures, API responses, UI components, or any computed results that should remain stable over time.

## Snapshot Fixture API

### Core Methods

The `snapshot` fixture accepts several options per assertion:

- `matcher`: Control how objects are serialized
- `exclude`: Filter out properties from snapshots
- `include`: Include only specific properties
- `extension_class`: Use a different serialization format
- `diff`: Capture only differences from a base
- `name`: Custom name for the snapshot

### Usage with Options

```python
assert data == snapshot(matcher=my_matcher, exclude=my_filter, name="custom_name")
```

## Built-in Extensions

Syrupy provides several snapshot extensions for different use cases:

### AmberSnapshotExtension (Default)

- Human-readable format
- Stores all snapshots in `.ambr` files
- Supports all Python built-in types
- Custom object representation via `__repr__`

### JSONSnapshotExtension

- Stores snapshots as JSON files (`.json` extension)
- Useful for API responses and complex data structures
- Machine-readable format
- Import from `syrupy.extensions.json`

**Usage Example:**

```python
import pytest
from syrupy.extensions.json import JSONSnapshotExtension


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.use_extension(JSONSnapshotExtension)


def test_api_call(client, snapshot_json):
    resp = client.post("/endpoint")
    assert resp.status_code == 200
    assert snapshot_json == resp.json()
```

**Handling Dynamic Data in JSON:**

```python
from datetime import datetime
from syrupy.matchers import path_type


def test_api_call(client, snapshot_json):
    resp = client.post("/user", json={"name": "Jane"})
    matcher = path_type({"id": (int,), "registeredAt": (datetime,)})
    assert snapshot_json(matcher=matcher) == resp.json()
```

### SingleFileSnapshotExtension

- One file per snapshot
- Configurable file extensions
- Useful for binary data or large snapshots

### PNGSnapshotExtension

- For image snapshot testing
- Compares PNG image data

### SVGSnapshotExtension

- For SVG vector graphics
- Text-based comparison of SVG content

## Matchers

Matchers control how specific values are serialized during snapshot creation.

### path_type

Match specific paths in data structures to types:

```python
from syrupy.matchers import path_type
import datetime

matcher = path_type({"date_created": (datetime,), "user.id": (int,), "nested.*.timestamp": (datetime,)})
```

### path_value

Match paths and replace with specific values:

```python
from syrupy.matchers import path_value

matcher = path_value({"id": "REDACTED_ID", "token": "***"})
```

## Filters

Filters control which properties are included/excluded from snapshots.

### Custom Exclude Function

The `exclude` parameter accepts a custom filter function with this signature:

```python
def my_filter(prop, path):
    """
    Args:
        prop: The current property (any hashable value: int, str, object, etc.)
        path: Ordered sequence of traversed locations, e.g.,
              (("a", dict), ("b", dict)) when navigating {"a": {"b": {"c": 1}}}

    Returns:
        True to exclude the property, False to include it
    """
    return should_exclude
```

**Example:**

```python
def limit_foo_attrs(prop, path):
    allowed_attrs = {"only", "serialize", "these", "attrs"}
    return isinstance(path[-1][1], Foo) and prop in allowed_attrs


def test_bar(snapshot):
    actual = Foo(...)
    assert actual == snapshot(exclude=limit_foo_attrs)
```

### props

Filter by property names (shallow):

```python
from syrupy.filters import props

# Exclude specific properties
exclude = props("id", "timestamp", "random_value")

# Include only specific properties
include = props("name", "type", "data")

# Works with indexed iterables
exclude = props("id", "1")  # Excludes "id" and index 1
```

### paths

Filter by full property paths using dot-delimited strings:

```python
from syrupy.filters import paths

# Exclude nested paths
exclude = paths("user.password", "response.headers.authorization", "items.*.id")

# Works with list indices
exclude = paths("date", "list.1")
```

## CLI Options

Syrupy adds several pytest command-line options:

- `--snapshot-update`: Update snapshots with current values
- `--snapshot-warn-unused`: Warn about unused snapshots
- `--snapshot-details`: Show detailed snapshot information
- `--snapshot-default-extension`: Change default extension class
- `--snapshot-no-colors`: Disable colored output

## Advanced Configuration

### Custom Snapshot Names

```python
def test_multiple_cases(snapshot):
    assert case_1 == snapshot(name="case_1")
    assert case_2 == snapshot(name="case_2")
```

**Note:** Custom names must be unique within a test function.

### Persistent Configuration

Create a snapshot instance with default values:

```python
def test_api_responses(snapshot):
    api_snapshot = snapshot.with_defaults(
        extension_class=JSONSnapshotExtension, exclude=props("timestamp", "request_id")
    )

    assert response1 == api_snapshot
    assert response2 == api_snapshot  # Uses same defaults
```

### Custom Extensions

Create custom snapshot serializers by extending `AbstractSnapshotExtension`:

```python
from syrupy.extensions.base import AbstractSnapshotExtension


class MyExtension(AbstractSnapshotExtension):
    def serialize(self, data, **kwargs):
        # Custom serialization logic
        return str(data)

    def matches(self, *, serialized_data, snapshot_data):
        # Custom comparison logic
        return serialized_data == snapshot_data
```

## Snapshot Lifecycle

### Creation Flow

1. Run test without existing snapshot
2. Test fails with "snapshot does not exist"
3. Run with `--snapshot-update` to create
4. Snapshot file created in `__snapshots__/`
5. Commit snapshot to version control

### Update Flow

1. Code changes cause snapshot mismatch
2. Test fails showing difference
3. Review changes to ensure correctness
4. Run with `--snapshot-update` if changes are expected
5. Commit updated snapshot

### Cleanup

Remove unused snapshots:

```bash
pytest --snapshot-update --snapshot-warn-unused
```

## Data Type Support

### Built-in Types

All Python built-in types are supported:

- Primitives: `int`, `float`, `str`, `bool`, `None`
- Collections: `list`, `tuple`, `set`, `dict`
- Complex: `datetime`, `bytes`, custom objects (via `__repr__`)

### Custom Objects

Options for custom object snapshots:

1. Override `__repr__` method
2. Use custom matcher
3. Create custom extension
4. Use exclude/include filters

## Best Practices

### DO

1. **Commit snapshots to version control**: They're part of your test suite
2. **Review snapshot changes carefully**: Ensure changes are intentional
3. **Use meaningful test names**: Helps identify snapshot purpose
4. **Keep snapshots focused**: Test one thing per snapshot
5. **Use matchers for non-deterministic data**: Dates, IDs, timestamps

### DON'T

1. **Don't snapshot entire responses blindly**: Filter out volatile data
2. **Don't ignore snapshot changes**: They indicate behavior changes
3. **Don't use generic test names**: Makes debugging harder
4. **Don't snapshot huge data structures**: Use filters or separate tests
5. **Don't update snapshots without review**: Verify changes are correct

## Common Patterns

### API Response Testing

Use JSON extension with filters:

```python
@pytest.fixture
def api_snapshot(snapshot):
    return snapshot.use_extension(JSONSnapshotExtension).with_defaults(
        exclude=props("timestamp", "request_id", "session")
    )
```

### Dynamic Data Handling

Use matchers for non-deterministic values:

```python
from syrupy.matchers import path_type
import uuid
import datetime

assert response == snapshot(
    matcher=path_type(
        {
            "id": (uuid.UUID,),
            "created_at": (datetime.datetime,),
            "*.timestamp": (datetime.datetime,),
        }
    )
)
```

### Diff-Based Snapshots

Capture only changes from a baseline:

```python
def test_incremental_changes(snapshot):
    baseline = {"config": {...}}
    modified = apply_changes(baseline)

    assert modified == snapshot(diff=baseline)
```

## Important Constraints

1. **Python/pytest versions**: Requires Python 3.10+ and pytest 8+
2. **Snapshot immutability**: Never edit snapshot files manually
3. **Name uniqueness**: Custom snapshot names must be unique per test
4. **Path separators**: Use dots for nested paths in filters/matchers
5. **Zero dependencies**: Syrupy has no external dependencies

## Troubleshooting

### Common Issues

1. **Snapshot not found**: Run with `--snapshot-update`
2. **Unexpected differences**: Check for non-deterministic data
3. **Large diffs**: Use filters to focus on relevant data
4. **Flaky tests**: Use matchers for dynamic values
5. **Merge conflicts**: Update snapshots after resolving

### Debug Options

- Use `--snapshot-details` for verbose output
- Check `__snapshots__/` directory for actual files
- Use `exclude` to isolate problematic fields
- Test with smaller data sets first

## Migration from Other Libraries

### From pytest-snapshot

- Similar API, minimal changes needed
- Update import statements
- Regenerate snapshots

### From snapshottest

- Change `snapshot.assert_match()` to `assert x == snapshot`
- Update fixture name if customized
- Regenerate all snapshots
