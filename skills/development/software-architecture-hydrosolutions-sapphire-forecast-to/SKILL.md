---
name: software-architecture
description: Guide for Python software architecture in the SAPPHIRE forecast tools project. Use when writing code, designing module structure, refactoring, or making architectural decisions. Provides project-specific conventions for Python, Docker, and scientific computing patterns.
---

# Software Architecture Guide

Quality-focused software development patterns for SAPPHIRE forecast tools.

## Project-Specific Conventions

### Module Structure

Each module in `apps/` follows this pattern:
```
apps/<module_name>/
├── <module_name>.py      # Entry point script
├── src/                  # Source code
│   ├── __init__.py
│   ├── src.py           # Main module logic (or domain-specific names)
│   └── config.py        # Module configuration (if needed)
├── test/                # Tests (pytest)
├── pyproject.toml       # Dependencies (uv)
├── Dockerfile.py312     # Docker build
└── config.yaml          # Module-specific settings (if needed)
```

### Python Style

- **Python version**: 3.12 (migrating from 3.11)
- **Package manager**: uv with pyproject.toml
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Docstrings**: Google style
- **Type hints**: Required for new code
- **Logging**: Use `logger` (from logging module), not `print()`

### Code Patterns

**Early returns** for readability:
```python
def process_data(data):
    if data is None:
        return None
    if data.empty:
        logger.warning("Empty data received")
        return pd.DataFrame()
    # Main logic here
```

**Environment variables** for configuration:
```python
config_path = os.getenv('ieasyforecast_configuration_path')
if config_path is None:
    raise ValueError("ieasyforecast_configuration_path not set")
```

**Error handling** with informative messages:
```python
try:
    result = fetch_data(site_id)
except ConnectionError as e:
    logger.error(f"Failed to connect to data source for site {site_id}: {e}")
    raise
```

## General Principles

### Library-First Approach

- Check PyPI for existing solutions before writing custom code
- Use established libraries: pandas, numpy, xarray for data; requests for HTTP
- **When custom code IS justified:**
  - Domain-specific hydrology/forecasting logic
  - Integration with iEasyHydro SDK
  - Performance-critical numerical code

### Naming Conventions

- **AVOID** generic names: `utils.py`, `helpers.py`, `common.py`
- **USE** domain-specific names: `runoff_processor.py`, `forecast_calculator.py`
- Module names should describe their single purpose

### Separation of Concerns

- Keep data fetching separate from data processing
- Keep business logic separate from I/O operations
- Each function should do one thing well

### Code Quality Guidelines

- Functions under 50 lines when possible
- Files under 300 lines (split if larger)
- Max 3 levels of nesting
- Add comments for non-obvious hydrology/meteorology logic

## Docker Patterns

- Base image: `mabesa/sapphire-pythonbaseimage:py312`
- Use multi-stage builds for smaller images
- Copy only necessary files (not entire repo)
- Set `PYTHONUNBUFFERED=1` for log visibility

## Testing

- Use pytest with `SAPPHIRE_TEST_ENV=True`
- Mock external services (iEasyHydro SDK, file I/O)
- Test data processing logic independently from I/O
