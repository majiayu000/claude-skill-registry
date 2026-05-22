---
name: analyze-code-structure
description: "Examine code organization and identify structural patterns. Use when reviewing module design or understanding architecture."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Analyze Code Structure

Examine code organization, dependencies, and architectural patterns to understand how modules are organized.

## When to Use

- Reviewing module design before implementation
- Understanding how components connect
- Identifying structural improvements needed
- Planning refactoring strategies

## Quick Reference

```bash
# Analyze Python file structure
python3 << 'EOF'
import ast
import sys

def analyze_structure(filepath):
    with open(filepath) as f:
        tree = ast.parse(f.read())

    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    print(f"Classes: {classes}")
    print(f"Functions: {functions}")

analyze_structure(sys.argv[1])
EOF
```

## Workflow

1. **Identify module components**: List classes, functions, and major imports
2. **Map dependencies**: Trace how modules import and reference each other
3. **Analyze layers**: Categorize code into logical layers (interface, business logic, persistence)
4. **Document patterns**: Note recurring architectural patterns (factory, singleton, observer)
5. **Propose improvements**: Identify coupling issues or missing separation of concerns

## Output Format

Structured analysis report:

- Component inventory (classes, functions, data structures)
- Dependency graph (which modules import which)
- Layer organization (presentation, business, data)
- Design patterns identified
- Recommendations for improvement

## References

- See CLAUDE.md > Modularity section for design principles
- See `identify-architecture` skill for full architecture analysis
- See CLAUDE.md > SOLID principles for structural best practices
