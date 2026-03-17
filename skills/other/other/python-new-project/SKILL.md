---
name: python-new-project
description: Create a new modern Python project using `uv` and src-layout.
---

# Modern Python Project Generator (uv + src-layout)

This skill guides the creation of a new Python project using `uv` for package management and the `src` layout for better packaging and testing practices.

## Prerequisite

- `uv` installed (`uv --version`)

## Installation

If `uv` is not installed, install it using the following command (Windows):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

For other OS, refer to [astral.sh/uv](https://astral.sh/uv).

## Directory Structure

The final structure will look like this:

```
project-name/
├── pyproject.toml      # Project configuration and dependencies
├── README.md
├── .python-version
├── src/
│   └── project_name/   # Actual source code
│       └── __init__.py
└── tests/              # Tests directory
```

## Step-by-Step Instructions

### 1. Initialize Project

Use `uv` to initialize a new project with the library/package structure (which uses `src` layout by default in newer versions or check manually).

```bash
# Initialize new project with package structure
uv init __PROJECT_NAME__ --package
```

### 2. Verify Structure

Ensure the `src` directory exists. If `uv init` created a flat layout (older versions), move the package manually:

```bash
cd __PROJECT_NAME__
# If src doesn't exist but a folder with project name does:
# mkdir src
# mv __PROJECT_NAME__ src/
```

### 3. Setup Environment

```bash
# Sync dependencies and create virtual environment
uv sync
```

### 4. Project Configuration (pyproject.toml)

Ensure `pyproject.toml` includes standard modern metadata. The `uv init` command should have generated a good starting point.
Add common useful dependencies if requested (e.g., `ruff`, `pytest`):

```bash
uv add --dev ruff pytest
```

## Verification

Run the tests or check imports to ensure `src` layout is working.

```bash
uv run pytest
```


## Parent Hub
- [_data-ai-mastery](../_data-ai-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
