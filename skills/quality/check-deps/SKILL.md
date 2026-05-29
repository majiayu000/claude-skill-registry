---
name: check_deps
description: ソースコード内のimportとpyproject.tomlの依存関係の整合性をチェックする
---

# Check Dependencies

This skill verifies that all imported packages are declared in the project dependencies.

## Instructions

1.  **Scan Imports**:
    *   Use `grep` or a script to find all `import ...` and `from ... import` statements in `gwexpy/`.
    *   Extract top-level package names (e.g., from `numpy.linalg` get `numpy`).

2.  **Read Configuration**:
    *   Read `dependencies` and `project.optional-dependencies` sections in `pyproject.toml`.

3.  **Compare**:
    *   Identify packages imported but missing from configuration (Potential `ModuleNotFoundError`).
    *   Identify packages in configuration but never imported (Bloat).
    *   *Note*: Ignore standard library modules (e.g., `os`, `sys`, `typing`) and dev dependencies used only in `tests/`.

4.  **Report**:
    *   List missing dependencies.
    *   List potentially unused dependencies.
