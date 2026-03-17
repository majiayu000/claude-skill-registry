---
name: uv-discohy
description: UV/UVX/Ruff toolchain for DiscoHy Thread Operad with Python packaging and linting
trit: 0
---

# UV-DiscoHy Skill: Modern Python Tooling for Thread Operads

**Status**: ✅ Production Ready
**Trit**: 0 (ERGODIC - toolchain neutral)
**Toolchain**: uv + uvx + ruff
**Package**: music-topos with discohy_thread_operad

---

## Overview

This skill provides the **uv/uvx/ruff** toolchain integration for the DiscoHy Thread Operad system. It enables:

1. **Fast dependency management** via uv (10-100x faster than pip)
2. **One-shot tool execution** via uvx (no install required)
3. **Modern linting/formatting** via ruff (replaces black, isort, flake8)
4. **Python packaging** via pyproject.toml with hatchling

## Quick Start

```bash
# Initialize the environment
just uv-init

# Run the DiscoHy operad demo
just uv-discohy

# Lint and format
just uv-lint
just uv-format

# Run with specific variant
just uv-discohy-variant 2-transducer
```

## UV Commands

### Package Management

```bash
# Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"

# Add a dependency
uv pip install discopy>=1.1.0

# Sync all dependencies from pyproject.toml
uv pip sync pyproject.toml

# Show dependency tree
uv pip tree
```

### UVX: One-Shot Tool Execution

```bash
# Run ruff without installing
uvx ruff check src/

# Run pytest without installing
uvx pytest tests/

# Run a specific version
uvx --python 3.12 ruff check src/
```

## Ruff Configuration

From `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py311"
line-length = 100
indent-width = 4

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Ruff Commands

```bash
# Check for issues
ruff check src/ lib/

# Auto-fix issues
ruff check --fix src/

# Format code
ruff format src/

# Check and format in one pass
ruff check --fix src/ && ruff format src/
```

## DiscoHy Thread Operad Integration

### Python API

```python
from discohy_thread_operad import (
    RootedColorOperad,
    ThreadOperadNode,
    OPERAD_VARIANTS,
    build_operad_from_threads,
    operad_to_mermaid,
)

# Build operad from thread list
threads = [
    {"id": "T-root", "title": "Root Thread", "created": 0},
    {"id": "T-child", "title": "Child Thread", "created": 1},
]
operad = build_operad_from_threads(threads, variant="dendroidal")

# Switch variant dynamically
operad.set_variant("2-transducer")

# Check GF(3) conservation
gf3 = operad.gf3_conservation()
print(f"Conserved: {gf3['conserved']}")

# Generate Mermaid diagram
mermaid = operad_to_mermaid(operad)
print(mermaid)
```

### Operad Variants

| Variant | Trit | UV Package | Description |
|---------|------|------------|-------------|
| `dendroidal` | 0 | discopy | Tree grafting (Ω(T)) |
| `colored-symmetric` | -1 | discopy | Σ-colored with permutations |
| `actegory` | 0 | discopy | Monoidal action |
| `2-transducer` | +1 | discopy | Day convolution on state |

### 3 Parallel Color Streams

Each thread has 3 deterministic color streams:

```python
node = ThreadOperadNode("T-123", "My Thread")

# Access streams
live_color = node.get_color("LIVE")      # +1 trit
verify_color = node.get_color("VERIFY")  # 0 trit
backfill_color = node.get_color("BACKFILL")  # -1 trit

# Get trit from hue
trit = live_color.to_trit()  # -1, 0, or +1
```

## Project Structure

```
music-topos/
├── pyproject.toml          # UV/Ruff/Hatch configuration
├── src/
│   └── discohy_thread_operad.py  # Python implementation
├── lib/
│   └── discohy_thread_operad.hy  # Hy implementation
├── db/
│   └── thread_operad_schema.sql  # DuckDB materialization
└── tests/
    └── test_discohy_operad.py    # Pytest tests
```

## GF(3) Conservation

The system verifies that sibling triplets satisfy:

```
sum(trits) ≡ 0 (mod 3)
```

Where:
- `+1` (LIVE) = warm hues (0-60°, 300-360°)
- `0` (VERIFY) = neutral hues (60-180°)
- `-1` (BACKFILL) = cool hues (180-300°)

## Justfile Commands

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# UV/UVX/RUFF TOOLCHAIN
# ═══════════════════════════════════════════════════════════════════════════════

# Initialize uv environment
uv-init:
    uv venv
    uv pip install -e ".[dev]"

# Run DiscoHy operad demo
uv-discohy:
    uv run python src/discohy_thread_operad.py

# Run with specific variant
uv-discohy-variant variant:
    uv run python -c "from discohy_thread_operad import *; demo_variant('{{variant}}')"

# Lint with ruff
uv-lint:
    uvx ruff check src/ lib/

# Format with ruff
uv-format:
    uvx ruff format src/

# Fix and format
uv-fix:
    uvx ruff check --fix src/ && uvx ruff format src/

# Run tests
uv-test:
    uvx pytest tests/ -v

# Type check
uv-typecheck:
    uvx mypy src/

# Full check (lint + format + test)
uv-check:
    uvx ruff check src/
    uvx ruff format --check src/
    uvx pytest tests/ -v
```

## Integration with Other Skills

### Triad: uv-discohy + acsets + gay-mcp = 0 ✓

| Skill | Trit | Role |
|-------|------|------|
| `uv-discohy` | 0 | Coordinator (toolchain) |
| `acsets` | 0 | Coordinator (schema) |
| `gay-mcp` | +1 | Generator (colors) |
| → Need `-1` | | Add `three-match` or `slime-lisp` |

### With DiscoHy Streams

```python
# From discohy-streams skill
color_url = f"color://{thread_id}/LIVE"
# Get color at index via MCP
```

### With ACSets

```julia
# Thread operad as ACSet
@present SchThreadOperad(FreeSchema) begin
  Thread::Ob
  continuation::Hom(Thread, Thread)
  Trit::AttrType
  trit::Attr(Thread, Trit)
end
```

## Environment Variables

```bash
# UV cache directory (optional)
export UV_CACHE_DIR=~/.cache/uv

# Ruff cache (optional)
export RUFF_CACHE_DIR=~/.cache/ruff

# Python version (optional)
export UV_PYTHON=3.12
```

## Troubleshooting

### UV Not Found

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

### Ruff Errors

```bash
# Show all available rules
uvx ruff linter

# Ignore specific rule
uvx ruff check --ignore E501 src/
```

### Hy Not Found

```bash
# Install hy via uv
uv pip install hy>=1.0.0

# Run hy file
uv run hy lib/discohy_thread_operad.hy
```

## References

- [UV Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [DisCoPy](https://discopy.readthedocs.io/)
- [Hy Language](https://docs.hylang.org/)
- [DuckDB](https://duckdb.org/docs/)

---

**Skill Name**: uv-discohy
**Type**: Python Toolchain / DiscoHy Integration
**Trit**: 0 (ERGODIC)
**Toolchain**: uv + uvx + ruff
**Package Format**: pyproject.toml + hatchling
