---
name: python-project-creator
description: >
  Creates Python projects with proper structure, virtual environments, and dependency management.
  Use when users request to create a new Python project, set up a Python development environment,
  or initialize a Python application with standard tooling.
---

# Python Project Creator

## Critical Corrections

**Use 'uv' instead of 'pip'**

- ✗ Don't: pip install, pip freeze
- ✓ Do: uv pip install, uv pip freeze (uv is faster and more modern)

**Always use pytest, never unittest**

- ✗ Don't: unittest framework
- ✓ Do: pytest for all testing needs

## Overview

This skill creates well-structured Python projects with best practices for dependency management,
testing, and code organization. It sets up virtual environments, installs dependencies, and
configures common development tools.

## Project Creation Workflow

### 1. Understand Requirements

Ask the user about:
- **Project name** and purpose
- **Type**: CLI tool, web app, library, data science project
- **Dependencies**: Required packages
- **Testing**: Testing framework preference (pytest, unittest)

### 2. Create Project Structure

Standard Python project structure:

```
project-name/
├── src/
│   └── project_name/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py (optional, for libraries)
```

### 3. Virtual Environment Setup

Create and activate virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate (instructions for user)
# macOS/Linux: source venv/bin/activate
# Windows: venv\Scripts\activate
```

### 4. Install Dependencies

Install packages using uv:

```bash
uv pip install <package-name>
uv pip freeze > requirements.txt
```

For development dependencies:

```bash
uv pip install pytest black flake8 mypy
```

### 5. Initialize Git

```bash
git init
git add .
git commit -m "Initial commit: project setup"
```

## Project Types

### CLI Application

- Use `argparse` or `click` for command-line arguments
- Include `main.py` with proper entry point
- Add `if __name__ == "__main__":` guard

### Web Application

- Flask: Lightweight, good for small APIs
- FastAPI: Modern, async, auto-documentation
- Django: Full-featured, batteries included

### Library/Package

- Include `setup.py` for packaging
- Follow semantic versioning
- Add comprehensive docstrings

### Data Science

- Include `notebooks/` directory for Jupyter notebooks
- Add `data/` directory (with .gitignore)
- Common packages: pandas, numpy, matplotlib, scikit-learn

## Testing Setup

### pytest (Required)

Always use pytest for testing:

```bash
uv pip install pytest pytest-cov
```

Example test file:

```python
# tests/test_main.py
import pytest
from src.project_name.main import my_function

def test_my_function():
    assert my_function(2, 3) == 5
```

Run tests:

```bash
pytest
pytest --cov=src  # with coverage
```

## Code Quality Tools

### Black (Code Formatter)

```bash
uv pip install black
black src/ tests/
```

### Flake8 (Linter)

```bash
uv pip install flake8
flake8 src/ tests/
```

### mypy (Type Checker)

```bash
uv pip install mypy
mypy src/
```

## Common Patterns

### Entry Point Pattern

```python
# src/project_name/main.py

def main():
    """Main application entry point."""
    print("Hello, World!")

if __name__ == "__main__":
    main()
```

### Configuration Pattern

```python
# src/project_name/config.py

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Load environment variables
DEBUG = os.getenv("DEBUG", "False") == "True"
```

### Error Handling Pattern

```python
class ProjectError(Exception):
    """Base exception for this project."""
    pass

class ConfigError(ProjectError):
    """Configuration-related errors."""
    pass
```

## .gitignore Template

```
# Virtual environment
venv/
env/
.venv/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
```

## Best Practices

### Dependency Management

- Pin exact versions in production: `package==1.2.3`
- Use ranges for libraries: `package>=1.2,<2.0`
- Separate dev dependencies from production
- Keep requirements.txt minimal

### Project Structure

- Use `src/` layout to avoid import issues
- Keep tests separate from source code
- One module per file, clear naming
- Flat is better than nested (within reason)

### Documentation

- Write clear README.md with setup instructions
- Add docstrings to all public functions/classes
- Include usage examples in README
- Document environment variables

### Version Control

- Initialize git from the start
- Write meaningful commit messages
- Create .gitignore before first commit
- Never commit secrets or credentials

## Quick Start Examples

### Minimal CLI Tool

```bash
mkdir my-cli-tool && cd my-cli-tool
python3 -m venv venv
source venv/bin/activate
uv pip install click
# Create main.py, tests, etc.
```

### FastAPI Web Service

```bash
mkdir my-api && cd my-api
python3 -m venv venv
source venv/bin/activate
uv pip install fastapi uvicorn
# Create app structure
```

### Data Science Project

```bash
mkdir my-analysis && cd my-analysis
python3 -m venv venv
source venv/bin/activate
uv pip install pandas numpy matplotlib jupyter
# Create notebooks/, data/, src/
```

## Resources

This skill includes examples in the bundled directories:

### scripts/
- `example.py` - Template Python script with best practices

### references/
- `api_reference.md` - Common library documentation references

### assets/
- Project templates and boilerplate code
