---
name: test_code
description: pytestを使用してプロジェクトのテストスイートを実行する
---

# Test Code

This skill handles running the project's tests, including core types and general functionality.

## Usage

To run all tests:
```bash
pytest
```

To run and check core metadata propagation (TimeSeries/Spectrogram matrices):
```bash
pytest tests/ -k "metadata" # or relevant pattern
```

## Focus Areas (Core Verification)
- **Metadata Propagation**: Verify `radian()`, `degree()`, `to_matrix()` keep axes and units.
- **Ufuncs**: Check that arithmetic operations respect units.
- **Collections**: Ensure `List/Dict` to `Matrix` conversion inherits metadata correctly.
