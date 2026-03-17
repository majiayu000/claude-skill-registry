---
name: dependency-analyzer
description: Analyze Python imports and dependencies. Use to understand project structure, find unused imports, or generate requirements.txt files.
---

# Dependency Analyzer

Analyze Python file imports and project dependencies.

## Features

- **Import Extraction**: List all imports from Python files
- **Dependency Graph**: Visualize import relationships
- **Unused Detection**: Find unused imports
- **Requirements Generation**: Auto-generate requirements.txt
- **Standard Library Detection**: Separate stdlib from third-party
- **Circular Import Detection**: Find circular dependencies

## Quick Start

```python
from dependency_analyzer import DependencyAnalyzer

analyzer = DependencyAnalyzer()

# Analyze single file
imports = analyzer.analyze_file("main.py")
print(imports)

# Analyze project
result = analyzer.analyze_project("./src")
print(result['third_party'])  # External dependencies
```

## CLI Usage

```bash
# Analyze single file
python dependency_analyzer.py --file main.py

# Analyze project directory
python dependency_analyzer.py --dir ./src

# Generate requirements.txt
python dependency_analyzer.py --dir ./src --requirements --output requirements.txt

# Find unused imports
python dependency_analyzer.py --file main.py --unused

# Show dependency graph
python dependency_analyzer.py --dir ./src --graph

# JSON output
python dependency_analyzer.py --dir ./src --json
```

## API Reference

### DependencyAnalyzer Class

```python
class DependencyAnalyzer:
    def __init__(self)

    # Analysis
    def analyze_file(self, filepath: str) -> dict
    def analyze_project(self, directory: str) -> dict

    # Detection
    def find_unused_imports(self, filepath: str) -> list
    def find_circular_imports(self, directory: str) -> list

    # Generation
    def generate_requirements(self, directory: str) -> list
    def save_requirements(self, deps: list, output: str)

    # Classification
    def is_stdlib(self, module: str) -> bool
    def is_local(self, module: str, directory: str) -> bool
```

## Output Format

### File Analysis
```python
{
    "file": "main.py",
    "imports": [
        {"module": "os", "type": "stdlib", "line": 1},
        {"module": "json", "type": "stdlib", "line": 2},
        {"module": "requests", "type": "third_party", "line": 3},
        {"module": "utils.helpers", "type": "local", "line": 4}
    ],
    "from_imports": [
        {"module": "typing", "names": ["Dict", "List"], "type": "stdlib"},
        {"module": "flask", "names": ["Flask", "request"], "type": "third_party"}
    ]
}
```

### Project Analysis
```python
{
    "directory": "./src",
    "files_analyzed": 15,
    "stdlib": ["os", "sys", "json", "typing", ...],
    "third_party": ["requests", "flask", "pandas", ...],
    "local": ["utils", "models", "config", ...],
    "by_file": {
        "main.py": {...},
        "app.py": {...}
    }
}
```

## Example Workflows

### Generate Requirements
```python
analyzer = DependencyAnalyzer()
deps = analyzer.generate_requirements("./src")
analyzer.save_requirements(deps, "requirements.txt")
```

### Find Unused Imports
```python
analyzer = DependencyAnalyzer()
unused = analyzer.find_unused_imports("main.py")
for imp in unused:
    print(f"Line {imp['line']}: {imp['module']} is unused")
```

### Analyze Project Structure
```python
analyzer = DependencyAnalyzer()
result = analyzer.analyze_project("./myproject")

print("Third-party dependencies:")
for dep in result['third_party']:
    print(f"  - {dep}")

print("\nLocal modules:")
for mod in result['local']:
    print(f"  - {mod}")
```

### Check for Circular Imports
```python
analyzer = DependencyAnalyzer()
circular = analyzer.find_circular_imports("./src")
if circular:
    print("Circular imports detected:")
    for cycle in circular:
        print(f"  {' -> '.join(cycle)}")
```

## Module Classification

| Type | Description | Example |
|------|-------------|---------|
| `stdlib` | Python standard library | `os`, `sys`, `json` |
| `third_party` | External packages | `requests`, `pandas` |
| `local` | Project modules | `utils.helpers` |

## Dependencies

No external dependencies - uses Python standard library (ast module).
