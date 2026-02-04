---
name: snapshot-testing
description: Snapshot testing framework for asserting data structures don't change unexpectedly. Supports JSON serialization, automatic snapshot creation on first run, diff visualization on mismatches, max depth protection, and --update-snapshots flag.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T23:15:15.877Z"
  updated_at: "2026-01-29T23:15:15.877Z"
  version: "1"
  tags: "testing,snapshot,assertions,regression"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Provide snapshot testing capabilities for vibe_piper data structures.

# When To Use
- User wants to test that pipeline outputs, transformations, or data processing results remain consistent across code changes.
- Use snapshot testing to catch regressions in data processing logic.

# API
```python
from tests.helpers.snapshots import assert_match_snapshot, assert_json_snapshot, assert_snapshot_matches_data


# Create snapshot (auto-created on first run)
assert_match_snapshot(data, "my_pipeline_output")

# Compare against expected (shows diff if mismatch)
assert_match_snapshot(actual_data, "expected_snapshot")
```

# Features
- JSON-based snapshot storage in tests/snapshots/
- Automatic snapshot creation on first run
- Diff visualization with unified diff on mismatches
- Max depth protection for nested structures
- Sorted keys for reproducibility
- Support for --update-snapshots flag to update existing snapshots


# Data Types Supported
- Primitive types (str, int, float, bool, None)
- Collections (list, dict, tuple, set)
- Dataclasses with __dict__
- Nested structures up to max_depth (default 10)

# Configuration
- update: If True, update the snapshot with new value
- test_file_path: Override auto-detection of test file path
- max_depth: Maximum nesting depth for serialization

# Test Fixtures
- snapshot_tmp: Temporary directory for test snapshot files

# Error Handling
- Clear diff output showing expected vs actual
- Line-by-line comparison using unified diff
- Helpful error messages with snapshot name

# Usage Examples
```python
# Test pipeline output against snapshot
def test_pipeline_output():
    result = pipeline.execute(data)
    assert_match_snapshot(result, "pipeline_output_snapshot")

# Test API response matches expected format
def test_api_response():
    response = api_client.get_users()
    assert_json_snapshot(response, "api_users_snapshot")
```

# Dependencies
- Built-in: json, difflib, pathlib
- Test framework: pytest (via conftest and test imports)
- Vibe Piper types: Schema, DataRecord, etc.

# Files
- tests/helpers/snapshots.py - Core implementation
- tests/helpers/test_snapshots.py - Test suite
- tests/snapshots/ - Snapshot storage directory
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
