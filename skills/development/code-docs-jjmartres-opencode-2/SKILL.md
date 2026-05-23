---
name: code-docs
description: Apply Google Style documentation standards to Python, Go, and Terraform code. Use when writing or reviewing code that needs docstrings/comments, when asked to "document this code", "add docstrings", "follow Google Style", or when improving code documentation quality. Supports Python docstrings, Go comments, and Terraform variable/output descriptions. Enforces consistent, professional documentation standards.
license: MIT
compatibility: opencode
---

# Code Documentation Standards

Apply Google Style documentation standards to Python (docstrings), Go (comments), and Terraform (descriptions). Ensures consistent, professional, and comprehensive code documentation across multiple languages.

## When to Apply This Skill

Use this skill when:

- Writing new functions, classes, or packages
- Reviewing code for documentation quality
- User requests "document this code" or "add docstrings"
- User mentions "Google Style" or documentation standards
- Refactoring code that lacks proper documentation
- Creating code examples that should be well-documented

## Core Principles

1. **Clarity**: Documentation should be immediately understandable
2. **Completeness**: Document all public APIs, parameters, returns, exceptions
3. **Consistency**: Follow language-specific Google Style conventions
4. **Conciseness**: Be thorough but avoid redundancy
5. **Examples**: Include usage examples for complex functionality

## Workflow

### 1. Detect Language

Identify the programming language:

- **Python**: Look for `.py` files, `def`, `class` keywords, type hints
- **Go**: Look for `.go` files, `func`, `type`, `package` keywords
- **Terraform**: Look for `.tf` files, `resource`, `variable`, `module` keywords

### 2. Apply Appropriate Standard

Read the corresponding reference file:

- **Python**: Read `references/python_google_style.md` for complete docstring standards
- **Go**: Read `references/go_google_style.md` for complete comment standards
- **Terraform**: Read `references/terraform_style.md` for complete description standards

### 3. Document Code Elements

Apply documentation to all appropriate code elements:

**Python**:

- Module-level docstrings
- Class docstrings
- Method/function docstrings
- Important variables/constants

**Go**:

- Package comments
- Type comments
- Function comments
- Important constants/variables

**Terraform**:

- Variable descriptions
- Output descriptions
- Resource comments
- Module descriptions

### 4. Quality Checks

Before finalizing, verify:

- All public APIs are documented
- Parameters and returns are described
- Exceptions/errors are documented
- Examples are provided for complex functions
- Formatting follows Google Style exactly
- No redundant or obvious documentation

### 5. Provide Feedback

When reviewing code:

- Point out missing documentation
- Suggest improvements to existing docs
- Provide corrected examples
- Explain why certain documentation is important

## Documentation Coverage

### Python - What to Document

**Always Document**:

- Public modules (module-level docstring)
- Public classes (class docstring)
- Public methods and functions (method docstring)
- `__init__` methods (explain parameters)

**Consider Documenting**:

- Complex private functions (with leading underscore)
- Non-obvious class attributes
- Module-level constants

**Don't Document**:

- Self-explanatory code (e.g., simple getters/setters)
- Override methods that just call super() without changes
- Trivial one-liner functions with obvious behavior

### Go - What to Document

**Always Document**:

- Package (package comment before package declaration)
- Exported types (structs, interfaces)
- Exported functions and methods
- Exported constants and variables

**Consider Documenting**:

- Complex unexported functions
- Non-obvious implementation details
- Important internal structures

**Don't Document**:

- Trivial getters/setters
- Self-explanatory code
- Override methods without new behavior

### Terraform - What to Document

**Always Document**:

- All variables (description field)
- All outputs (description field)
- Module purpose (README.md)
- Complex resources (inline comments)

**Consider Documenting**:

- Data sources with complex filters
- Non-obvious resource dependencies
- Conditional resource creation logic

**Don't Document**:

- Self-explanatory variable names
- Simple pass-through outputs
- Standard resource configurations

## Special Cases

### Python Type Hints

When using type hints, docstrings can be more concise:

```python
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The sum of a and b.
    """
    return a + b
```

Type information is already in the signature, so Args and Returns can be brief.

### Go Error Returns

Always document what errors a function can return:

```go
// ReadConfig reads and parses the configuration file.
//
// Returns an error if the file cannot be read or contains invalid YAML.
func ReadConfig(path string) (*Config, error) {
    // implementation
}
```

### Complex Algorithms

For complex logic, add inline comments AND comprehensive function documentation:

```python
def dijkstra(graph: Graph, start: Node) -> dict[Node, float]:
    """Find shortest paths using Dijkstra's algorithm.

    Implements Dijkstra's single-source shortest path algorithm
    using a priority queue for O((V + E) log V) complexity.

    Args:
        graph: Weighted graph with non-negative edge weights.
        start: Starting node for path calculations.

    Returns:
        Dictionary mapping each node to its shortest distance from start.
        Unreachable nodes are not included in the result.

    Raises:
        ValueError: If graph contains negative edge weights.

    Example:
        >>> graph = Graph()
        >>> graph.add_edge("A", "B", 4)
        >>> graph.add_edge("A", "C", 2)
        >>> distances = dijkstra(graph, "A")
        >>> distances["B"]
        4
    """
    # Implementation with inline comments for complex parts
```

## Output Format

When adding documentation to code:

1. **Present the documented code** with proper formatting
2. **Explain what was added** if the changes are significant
3. **Highlight any decisions** made about what to document or not document

## Avoid

- Generic or placeholder documentation ("This function does stuff")
- Redundant documentation that just repeats the code ("This adds a and b")
- Over-documentation of obvious code
- Inconsistent formatting within the same file
- Missing critical information (parameters, exceptions, edge cases)
- Documentation that becomes outdated as code changes

### references/terraform_style.md

Complete Terraform documentation standard with:

- Variable description format
- Output description format
- Module documentation structure
- Inline comments for complex resources
- Examples for common patterns
- terraform-docs integration

## Resources

### references/python_google_style.md

Complete Python docstring standard with:

- Module, class, and function docstring formats
- Args, Returns, Raises, Yields sections
- Type hint integration
- Examples for common patterns
- Edge cases and best practices

### references/go_google_style.md

Complete Go comment standard with:

- Package comment format
- Function and method comment format
- Type comment format
- Documentation for errors
- Examples for common patterns
- godoc integration notes

## Quality Standards

All code documentation must:

- Start with a concise one-line summary
- Use proper grammar and punctuation
- Follow language-specific formatting (indentation, delimiters)
- Include examples for non-trivial public APIs
- Document all parameters, returns, and errors/exceptions
- Be maintained when code changes
