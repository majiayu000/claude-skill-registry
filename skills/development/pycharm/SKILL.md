---
name: pycharm
description: PyCharm Python IDE with debugging and testing. Use for Python development.
---

# PyCharm

PyCharm is the best IDE for serious Python development. It excels in **Django** support, **Data Science** (Jupyter), and virtualenv management.

## When to Use

- **Django/Flask**: It understands templates, routes, and ORM models better than VS Code.
- **Data Science**: Integrated "SciView" for pandas dataframes and plotting.
- **Testing**: Visual test runner for `pytest`.

## Core Concepts

### Virtual Environment Support

Auto-detects and activates venvs. Handles `pip`, `poetry`, and `uv`.

### Debugger

One of the best visual Python debuggers. Conditional breakpoints, evaluate expression.

### Type Checking

Performs robust static analysis even without type hints, but works best with them.

## Best Practices (2025)

**Do**:

- **Use "Python > Data Science" mode**: If working with notebooks, the UI adapts.
- **Use Endpoints View**: Visualizes all API routes in your Django/FastAPI app.
- **Configure Interpreter**: Ensure the correct `venv` is selected in bottom right.

**Don't**:

- **Don't ignore the yellow**: PyCharm's PEP 8 warnings teach you better Python.

## References

- [PyCharm Documentation](https://www.jetbrains.com/pycharm/documentation/)
