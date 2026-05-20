---
name: doc-generator
description: Generate markdown documentation from Python codebases by analyzing source files, extracting docstrings, type hints, and code structure. Use when the user asks to document Python code, create API docs, or generate README files from source code.
---

# Python Documentation Generator

Generate comprehensive markdown documentation from Python source code.

## When to Use This Skill

- User asks to "document this code" or "generate docs"
- Creating API documentation from Python modules
- Generating README files with usage examples
- Extracting docstrings and type signatures into readable format
- User mentions "documentation", "docstrings", or "API reference"

## Input

Accept either:
- Single Python file path
- Directory path (recursively process .py files)
- List of specific files

## Output Format

Generate standard markdown with:

```markdown
# Module Name

Brief description from module docstring.

## Classes

### ClassName

Description from class docstring.

**Methods:**
- `method_name(param: type) -> return_type`: Brief description

## Functions

### function_name(param: type) -> return_type

Description from docstring.

**Parameters:**
- `param` (type): Description

**Returns:**
- type: Description

## Usage Examples

```python
# Extract from docstring examples or generate basic usage
```
```

## Analysis Approach

1. **Parse Python files** using AST or inspection
2. **Extract key elements:**
   - Module-level docstrings
   - Class definitions and docstrings
   - Function/method signatures with type hints
   - Docstring content (support Google, NumPy, Sphinx formats)
3. **Organize hierarchically** (modules -> classes -> methods -> functions)
4. **Generate clean markdown** with consistent formatting

## Quality Guidelines

- Preserve original docstring formatting when meaningful
- Include type hints prominently in signatures
- Group related items (all classes together, all functions together)
- Add table of contents for large modules
- Skip private members (leading underscore) unless explicitly requested
- Handle missing docstrings gracefully (note "No description provided")

## Python Tools

Prefer standard library:
- `ast` module for parsing
- `inspect` module for runtime introspection
- `pathlib` for file handling

No external dependencies required for basic documentation generation.

## Error Handling

- Skip files with syntax errors (log warning)
- Handle missing type hints gracefully
- Warn if no docstrings found but continue processing
- Validate file paths exist before processing
