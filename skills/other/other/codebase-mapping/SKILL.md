---
name: codebase-mapping
description: Repository structure and dependency analysis for understanding a codebase's architecture. Use when needing to (1) generate a file tree or structure map, (2) analyze import/dependency graphs, (3) identify entry points and module boundaries, (4) understand the overall layout of an unfamiliar codebase, or (5) prepare for deeper architectural analysis.
---

# Codebase Mapping

Maps repository structure and dependencies to enable targeted architectural analysis.

## Quick Start

Generate a structural map:

```bash
python scripts/map_codebase.py /path/to/repo --output structure.json
```

## Process

1. **Clone or access** the target repository
2. **Generate file tree** excluding noise (node_modules, __pycache__, .git, etc.)
3. **Parse imports** to build dependency graph
4. **Identify entry points** (main.py, index.ts, setup.py, pyproject.toml)
5. **Detect boundaries** - package structure and public APIs

## Output Artifacts

The skill produces:

- `file_tree.txt` - Annotated directory structure
- `dependencies.json` - Import graph in adjacency list format
- `entry_points.md` - Identified entry points with descriptions
- `module_map.md` - Package boundaries and public interfaces

## Key Patterns to Identify

### Entry Point Detection

Look for these patterns:

- Python: `if __name__ == "__main__"`, `setup.py`, `pyproject.toml`
- Node: `package.json` main/bin fields, `index.js`
- Frameworks: `app.py` (Flask), `manage.py` (Django), `main.ts` (Nest)

### Dependency Classification

Classify imports as:

- **External**: Third-party packages (from package manager)
- **Internal**: Project modules (relative imports)
- **Standard**: Language standard library

### Noise Exclusion

Always exclude:

```
node_modules/
__pycache__/
.git/
.venv/
venv/
dist/
build/
*.egg-info/
.mypy_cache/
.pytest_cache/
```

## Integration with Other Skills

This skill provides the foundation for:

- `data-substrate-analysis` → Focus on types.py, models.py
- `execution-engine-analysis` → Focus on runner files
- `control-loop-extraction` → Focus on agent.py, loop files
- `component-model-analysis` → Focus on base classes

## Example Output

```markdown
## Repository: langchain

### Structure Summary
- 342 Python modules across 28 packages
- Primary entry: langchain/__init__.py
- Core packages: agents, chains, llms, tools

### Key Files for Analysis
- Types: langchain/schema.py, langchain/types.py
- Execution: langchain/agents/executor.py
- Tools: langchain/tools/base.py
```
