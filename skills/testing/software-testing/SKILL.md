---
name: software-testing
description: Always use this skill when writing or editing software tests!
---
# software-testing

- When writing tests, avoid mocking too much otherwise your tests will be unmaintainable.
  - Always prefer one or two simple integration tests over a bunch of fully mocked unit tests.
  - Use real models and data structures whenever possible.
- Print local variables to stdout on tests.
  - Focus on inputs and outputs to make it easier to debug it when tests fail.
  - Prefer running tests individually rather than the entire suite when facing errors.
- Validate using models (e.g.: pydantic) instead of countless field-by-field assertions.
  - `data = MyDataModel(**obj)` validates structure and types.
  - then assert `data == expected_data`.
- When testing file operations (reading/writing), use `tmp_path` fixture.
  - Files are automatically cleaned up after the test.
- When reading Excel/CSV files for comparison with Pydantic models:
  - Use `pd.read_excel(..., dtype=str, keep_default_na=False)` to avoid type coercion issues.
  - Pandas converts numeric strings to int/float and empty cells to NaN, breaking Pydantic validation.
