---
name: pyo3-maturin-bindings
description: "Python bindings for Rust libraries using PyO3 and maturin. Use when working on Python bindings to Rust code, including creating or modifying pyfunction/pyclass definitions, converting types between Rust and Python, handling errors across the FFI boundary, managing the GIL and memory, building wheels with maturin, publishing to PyPI, testing binding code, or debugging binding issues. Tuned for CQLite (Cassandra CQL bindings) with feature parity tracking."
---

# PyO3 + Maturin Python Bindings

## Project Structure

```
my-rust-lib/
├── Cargo.toml          # [lib] crate-type = ["cdylib", "rlib"]
├── pyproject.toml      # maturin build config
├── src/
│   ├── lib.rs          # Core Rust library
│   └── python/         # Python binding module
│       ├── mod.rs      # #[pymodule] definition
│       ├── types.rs    # #[pyclass] wrappers
│       └── errors.rs   # Python exception types
├── python/
│   └── my_lib/         # Pure Python additions (optional)
│       ├── __init__.py
│       └── py.typed    # PEP 561 marker
└── tests/
    ├── rust/           # Rust unit tests
    └── python/         # Python integration tests
```

## Core Workflow

### 1. Expose Rust Types

```rust
use pyo3::prelude::*;

#[pyclass]
#[derive(Clone)]
pub struct MyType {
    inner: RustType,  // Keep Rust type private
}

#[pymethods]
impl MyType {
    #[new]
    fn new(value: i64) -> PyResult<Self> {
        Ok(Self { inner: RustType::new(value)? })
    }
    
    fn process(&self) -> PyResult<String> {
        self.inner.process().map_err(|e| e.into())
    }
}
```

### 2. Register Module

```rust
#[pymodule]
fn my_lib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MyType>()?;
    m.add_function(wrap_pyfunction!(my_function, m)?)?;
    Ok(())
}
```

### 3. Build & Test

```bash
maturin develop          # Install in current venv for testing
maturin build --release  # Build wheel
pytest tests/python/     # Run Python tests
```

## Reference Guides

Load these as needed based on the task:

| Task | Reference |
|------|-----------|
| Type mapping between Rust ↔ Python | [type-conversions.md](references/type-conversions.md) |
| Converting Rust errors to Python exceptions | [error-handling.md](references/error-handling.md) |
| GIL management and memory safety | [memory-gil.md](references/memory-gil.md) |
| Building wheels and publishing to PyPI | [build-publish.md](references/build-publish.md) |
| Testing strategies (Rust + Python) | [testing.md](references/testing.md) |
| Debugging common binding issues | [debugging.md](references/debugging.md) |
| CQLite CQL feature parity checklist | [cqlite-parity.md](references/cqlite-parity.md) |

## Quick Reference

### Common Cargo.toml Setup

```toml
[lib]
name = "my_lib"
crate-type = ["cdylib", "rlib"]

[dependencies]
pyo3 = { version = "0.22", features = ["extension-module"] }

[features]
extension-module = ["pyo3/extension-module"]
```

### Common pyproject.toml

```toml
[build-system]
requires = ["maturin>=1.0,<2.0"]
build-backend = "maturin"

[project]
name = "my-lib"
requires-python = ">=3.8"
classifiers = ["Programming Language :: Rust"]

[tool.maturin]
features = ["pyo3/extension-module"]
python-source = "python"  # If you have pure Python code
```

### PyO3 Attribute Quick Reference

| Attribute | Use |
|-----------|-----|
| `#[pyclass]` | Expose struct to Python |
| `#[pymethods]` | Impl block with Python-visible methods |
| `#[new]` | `__init__` constructor |
| `#[getter]` / `#[setter]` | Property access |
| `#[staticmethod]` | No `self` parameter |
| `#[classmethod]` | Receives `cls: &Bound<'_, PyType>` |
| `#[pyo3(name = "...")]` | Rename in Python |
| `#[pyo3(signature = (...))]` | Custom signature with defaults |
