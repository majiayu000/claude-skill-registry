---
name: language-python
description: Python language patterns and best practices. Use when language python guidance is required or when selecting a primary language for non-trivial automation.
allowed-tools:
  - Bash(uv)
  - Bash(uvx)
  - Bash(ruff)
  - Bash(ty)
  - Bash(pytest)
---
## Key Execution Capabilities

### Code Validation

- Run syntax and type checking: `uvx ruff check`, `uvx ty`
- Execute linting and formatting with ruff: `uvx ruff format`
- Run tests with pytest: `uvx pytest`
- Validate project structure and dependencies

### Tool Integration

- Use `ruff` for linting, formatting, and code analysis
- Use `ty` for fast type checking
- Leverage `uvx` for one-off tool execution without installation
- Apply pytest for testing frameworks

### Execution Context

- Process Python files from filesystem layer
- Generate structured reports with findings
- Create minimal, rule-compliant patches for violations
- Maintain separation between governance rules and execution tools

## Error Handling

This skill provides execution-layer error handling for Python code analysis:
- Invalid Python syntax or imports
- Missing dependencies or tools
- Type checking failures (ty)
- Test execution errors

## Usage Notes

- Always delegate to governance rules for policy decisions
- Focus on concrete tool execution and result processing
- Provide deterministic, tool-first analysis results
- Maintain separation between rule definition and rule application
