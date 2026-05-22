---
name: kinemotion-development
description: Apply kinemotion development standards. Use when writing Python code, creating tests, modifying the kinemotion codebase, or reviewing code quality.
---

# Kinemotion Development Standards

## Pre-Commit Checklist

Always run before committing:

```bash
uv run ruff check --fix   # Auto-fix linting
uv run ruff format        # Format code
uv run pyright            # Type check (strict)
uv run pytest             # Run all tests
```

Or combined:

```bash
uv run ruff check --fix && uv run ruff format && uv run pyright && uv run pytest
```

## Quality Targets

| Metric           | Target | Current |
| ---------------- | ------ | ------- |
| Test coverage    | ≥ 50%  | 80.86%  |
| Code duplication | < 3%   | 2.96%   |
| Type errors      | 0      | 0       |
| Lint errors      | 0      | 0       |

Check duplication: `npx jscpd src/kinemotion`

## Type Hints

- Use `NDArray[np.float64]` for numpy arrays
- Use `TypedDict` for metric dictionaries
- Use `Literal` for string unions
- Pyright strict mode enforced

```python
from numpy.typing import NDArray
from typing import TypedDict, Literal

QualityPreset = Literal["fast", "balanced", "accurate"]

class CMJMetrics(TypedDict):
    jump_height_cm: float
    flight_time_ms: float
```

## Module Structure

```
src/kinemotion/
├── cli.py                  # Main CLI entry point
├── api.py                  # Public Python API
├── core/                   # Shared utilities
│   ├── validation.py       # Base validation classes
│   ├── pose.py             # MediaPipe wrapper
│   ├── filtering.py        # Signal processing
│   └── video_io.py         # Video I/O handling
├── cmj/                    # CMJ analysis module
│   ├── cli.py              # CMJ CLI subcommand
│   ├── analysis.py         # Core CMJ algorithm
│   ├── kinematics.py       # Velocity, position calc
│   └── validation_bounds.py # CMJ-specific bounds
└── dropjump/               # Drop jump module
    ├── cli.py              # Drop jump CLI subcommand
    ├── analysis.py         # Core drop jump algorithm
    └── validation_bounds.py # Drop jump bounds
```

## Testing

### Structure

Mirror source: `tests/core/`, `tests/cmj/`, `tests/dropjump/`, `tests/cli/`

### Fixtures

Use centralized fixtures from `tests/conftest.py`:

- `cli_runner`: Click test runner
- `minimal_video`: Synthetic test video
- `sample_video_path`: Path to test fixture

### Edge Cases to Test

- Empty arrays
- Single frame videos
- NaN values in landmarks
- Missing landmarks (occlusion)
- Zero velocity scenarios

```python
@pytest.mark.parametrize("input_data,expected", [
    (np.array([]), None),  # Empty
    (np.array([1.0]), 1.0),  # Single value
    (np.array([np.nan, 1.0, 2.0]), None),  # NaN handling
])
def test_edge_cases(input_data, expected):
    ...
```

## Key Algorithm Differences

| Aspect            | CMJ                        | Drop Jump            |
| ----------------- | -------------------------- | -------------------- |
| Search direction  | Backward (from peak)       | Forward              |
| Velocity type     | Signed (direction matters) | Absolute (magnitude) |
| Key phase         | Countermovement detection  | Ground contact       |
| Starting position | Floor level                | Elevated (box)       |

## Common Gotchas

1. **CMJ velocity must be signed** - backward search requires knowing direction
2. **Convert NumPy for JSON** - use `int()`, `float()` before serialization
3. **Handle video rotation** - mobile videos have rotation metadata
4. **Read first frame for dimensions** - don't trust OpenCV properties

## Commit Format

Use Conventional Commits:

```
<type>(<scope>): <description>

Types: feat, fix, docs, test, refactor, perf, chore
```

Examples:

```
feat(cmj): add triple extension tracking
fix(dropjump): correct ground contact detection
test(core): add filtering edge case tests
```

## Code Style

- 88 character line limit (ruff)
- Use early returns to reduce nesting
- Extract methods for complexity > 15
- Prefer composition over inheritance
- Single Responsibility for all functions

## Tools Usage

- **Documentation**: Use `ref_search_documentation` and `ref_read_url` to consult external library documentation (OpenCV, MediaPipe, NumPy, etc.) when needing clarification on APIs.
- **Code Context**: Use `get_code_context_exa` to find best practices and modern examples for specific coding tasks.
- **Memory**: Use `save_memory` or `write_note` (Serena) to persist important architectural decisions or validation results.
