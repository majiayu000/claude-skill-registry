---
name: python-repo-quickstart
description: Quickly analyzes Python repositories to understand their purpose, structure, and setup requirements. Use when Claude needs to onboard to a new Python codebase, understand project structure, identify entry points, determine dependencies, or generate setup instructions. Trigger when users ask to "analyze this Python repo", "understand this codebase", "how do I run this project", "what does this repo do", or provide a Python repository path for quick start guidance.
---

# Python Repository Quick Start

Rapidly analyze and understand Python repositories to get started quickly.

## Quick Start

When a user provides a Python repository:

1. **Scan repository structure**: Identify key files and directories
2. **Determine project type**: Web app, CLI tool, library, data science, etc.
3. **Find entry points**: Locate main execution files
4. **Identify dependencies**: Find requirements and dependency management
5. **Extract setup instructions**: Determine how to install and run
6. **Summarize functionality**: Understand what the project does

## What This Skill Analyzes

### Project Purpose & Type
- Identify project category (web app, CLI, library, data science)
- Understand main functionality from README and code structure
- Determine intended use case

### Repository Structure
- Entry points (main.py, app.py, manage.py, etc.)
- Package organization (src/, app/, lib/)
- Test structure (tests/, test_*.py)
- Documentation (docs/, README.md)
- Configuration files

### Dependencies & Requirements
- requirements.txt (pip)
- Pipfile/Pipfile.lock (Pipenv)
- pyproject.toml/poetry.lock (Poetry)
- environment.yml (Conda)
- setup.py/setup.cfg (setuptools)

### Setup & Execution
- Virtual environment setup
- Installation commands
- Environment variables needed
- How to run the application
- How to run tests

## Analysis Workflow

### 1. Initial Scan

**Automated analysis:**
```bash
python scripts/analyze_repo.py <repo_path>
```

**Manual analysis:**
- List top-level files and directories
- Identify key indicator files
- Check for README

### 2. Identify Project Type

**Check for framework indicators:**

**Django:**
- `manage.py` present
- `settings.py` in project
- Django in dependencies

**Flask:**
- `app.py` or `application.py`
- Flask imports in code
- `templates/` and `static/` directories

**FastAPI:**
- FastAPI imports
- `main.py` with app definition
- `uvicorn` in dependencies

**CLI Tool:**
- `cli.py` or `__main__.py`
- `argparse`, `click`, or `typer` usage
- Console scripts in setup

**Library/Package:**
- `src/` directory structure
- `setup.py` or `pyproject.toml`
- No obvious entry point

**Data Science:**
- `.ipynb` files
- `notebooks/` directory
- pandas, numpy, scikit-learn dependencies

**See:** [python-patterns.md](references/python-patterns.md) for detailed patterns

### 3. Find Entry Points

**Common entry points:**
- `main.py` - Standard entry point
- `app.py` / `run.py` - Web application
- `manage.py` - Django management
- `cli.py` - Command-line interface
- `__main__.py` - Package entry (python -m)

**Check for:**
- `if __name__ == "__main__":` blocks
- Function definitions that look like entry points
- Console scripts in setup.py/pyproject.toml

### 4. Analyze Dependencies

**Find dependency files:**
- `requirements.txt` - Most common
- `requirements-dev.txt` - Development dependencies
- `Pipfile` - Pipenv
- `pyproject.toml` - Poetry or modern setup
- `environment.yml` - Conda

**Extract key dependencies:**
- Web frameworks (Flask, Django, FastAPI)
- Database libraries (SQLAlchemy, psycopg2)
- Testing frameworks (pytest, unittest)
- CLI libraries (click, typer, argparse)
- Data science (pandas, numpy, scikit-learn)

### 5. Determine Setup Instructions

**Virtual environment:**
```bash
# Standard venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**Installation:**
```bash
# pip
pip install -r requirements.txt

# Development mode
pip install -e .

# Poetry
poetry install

# Pipenv
pipenv install

# Conda
conda env create -f environment.yml
```

**Configuration:**
- Check for `.env.example` or `.env.template`
- Look for config.py or settings.py
- Identify required environment variables

**Running:**
```bash
# Direct execution
python main.py

# Module execution
python -m package_name

# Web frameworks
flask run
uvicorn main:app --reload
python manage.py runserver

# CLI tools
python cli.py --help
package-name --help
```

### 6. Extract Functionality

**From README:**
- Project description
- Features list
- Usage examples
- API documentation

**From code structure:**
- Module names indicate functionality
- Class and function names
- Comments and docstrings
- Test files reveal features

**From dependencies:**
- Web framework → web application
- Database libraries → data persistence
- ML libraries → machine learning
- API clients → integration with services

## Output Format

Generate a quick start guide with:

### Project Overview
```
Project: [Name]
Type: [Web App / CLI Tool / Library / Data Science / etc.]
Purpose: [Brief description]
```

### Prerequisites
```
- Python [version]
- [Other system requirements]
```

### Quick Setup
```bash
# 1. Clone repository (if needed)
git clone [url]

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (if needed)
cp .env.example .env
# Edit .env with your settings

# 5. Run application
python main.py
```

### Entry Points
```
- main.py: Main application entry
- cli.py: Command-line interface
- tests/: Test suite
```

### Key Dependencies
```
- flask: Web framework
- sqlalchemy: Database ORM
- pytest: Testing framework
```

### Main Functionality
```
- Feature 1: Description
- Feature 2: Description
- Feature 3: Description
```

### Running Tests
```bash
pytest
# or
python -m pytest tests/
```

### Additional Notes
```
- Configuration details
- Known issues
- Development tips
```

## Example Usage Patterns

**User:** "Analyze this Python repository"
→ Scan structure, identify type, generate quick start guide

**User:** "How do I run this project?"
→ Find entry points, dependencies, provide setup and run instructions

**User:** "What does this codebase do?"
→ Analyze README, code structure, dependencies to summarize functionality

**User:** "Help me understand this Python repo structure"
→ Explain directory organization, identify key components

**User:** "What are the prerequisites for this project?"
→ Identify Python version, system requirements, dependencies

**User:** "Generate setup instructions for this repo"
→ Create step-by-step installation and configuration guide

## Best Practices

### Analysis
- Start with README for high-level understanding
- Check multiple dependency files (may have both requirements.txt and pyproject.toml)
- Look for .env.example to understand configuration needs
- Examine test files to understand features

### Documentation
- Be specific about Python version requirements
- Include both installation and running instructions
- Note any system-level dependencies (databases, Redis, etc.)
- Mention common gotchas or setup issues

### Clarity
- Use clear section headers
- Provide copy-paste ready commands
- Explain what each step does
- Include troubleshooting tips when relevant

## Automated Analysis

Use the provided script for quick automated analysis:

```bash
python scripts/analyze_repo.py /path/to/repo
```

**Output includes:**
- Project type identification
- Entry points
- Dependency management approach
- Configuration files
- Test presence
- Documentation availability

**Limitations:**
- Heuristic-based detection
- May miss custom structures
- Requires manual verification for complex projects
