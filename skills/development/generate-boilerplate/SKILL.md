---
name: generate-boilerplate
description: "Create starter code from templates. Use when setting up new modules or test files."
mcp_fallback: none
category: generation
tier: 1
user-invocable: false
---

# Generate Boilerplate

Create standard starter code templates for new modules, test files, and configuration files to accelerate development.

## When to Use

- Creating new modules or packages
- Setting up test file structure
- Initializing configuration files
- Standardizing code structure across project

## Quick Reference

```bash
# Generate from templates
cat > new_module.py << 'EOF'
"""Module docstring describing purpose."""

def main():
    """Main function."""
    pass

if __name__ == "__main__":
    main()
EOF

# Or use template generator
python3 << 'PYSCRIPT'
import os
def generate_module_boilerplate(name):
    return f'"""Module {name}."""\n\nclass {name.title()}:\n    pass\n'
PYSCRIPT
```

## Workflow

1. **Select template type**: Module, test, config, etc.
2. **Customize parameters**: Name, class structure, default content
3. **Generate file**: Create from template with substitutions
4. **Add to project**: Place in correct location
5. **Validate structure**: Ensure imports and basic structure work

## Output Format

Generated boilerplate:

- File(s) created with correct naming
- Standard header comments and docstrings
- Basic structure (class/function stubs)
- Import statements included
- Ready to compile/run (no syntax errors)

## References

- See templates/ directories in skill folders for examples
- See `generate-docstrings` skill for docstring templates
- See CLAUDE.md > Code Standards for project conventions
