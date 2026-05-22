---
name: generate-api-docs
description: "Create API reference documentation from docstrings. Use when documenting public module interfaces."
mcp_fallback: none
category: generation
tier: 2
user-invocable: false
---

# Generate API Docs

Extract docstrings from functions and classes to automatically generate API reference documentation.

## When to Use

- Documenting public module interfaces
- Creating reference guides for libraries
- Generating HTML API documentation
- Maintaining up-to-date API specs

## Quick Reference

```bash
# Python with pdoc
pdoc --html module_name -o docs/

# Python with Sphinx
sphinx-quickstart docs/
make -C docs html

# Extract docstrings
python3 -c "import module; help(module.function)"
```

## Workflow

1. **Ensure docstrings**: Verify all public functions/classes have docstrings
2. **Validate format**: Check docstring format (Google, NumPy, or reStructuredText)
3. **Extract metadata**: Parse function signatures, parameter types, return types
4. **Generate documentation**: Create HTML or Markdown API reference
5. **Validate output**: Verify links work and examples are correct

## Output Format

API documentation:

- Module overview
- Function/class signatures with type hints
- Parameter documentation (type, description, default)
- Return value documentation
- Raises/exceptions
- Code examples
- Cross-references to related APIs

## References

- See `generate-docstrings` skill for creating docstrings
- See CLAUDE.md > Documentation for standards
- See `doc-issue-readme` skill for issue documentation
