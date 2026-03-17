---
name: Python Flynt F-String Converter
description: "Use flynt to convert old Python string formatting to f-strings. Activate when: (1) Converting %-formatting to f-strings, (2) Converting .format() calls to f-strings, (3) Modernizing string concatenation to f-strings, (4) Improving code readability through f-string adoption, or (5) Batch-converting legacy Python codebases."
---

# Python Flynt F-String Converter

## Overview

Flynt is an automated tool that transforms Python string formatting from older styles (%-formatting and `.format()`) into modern f-strings, available since Python 3.6.

**Why f-strings?**
- More readable and concise
- Less prone to errors
- Faster execution than older methods
- Easier to maintain

## Key Capabilities

- **Automatic conversion**: Transforms both %-formatting and .format() to f-strings
- **Directory recursion**: Processes entire projects at once
- **Safe transformations**: Skips complex cases that might change behavior
- **String concatenation**: Can convert `+` operations to f-strings (Python 3.9+)
- **Static joins**: Can convert `.join()` on static lists (Python 3.9+)

## Quick Reference

### Basic Commands

```bash
# Convert a single file
flynt file.py

# Convert entire directory (recursive)
flynt src/

# Dry run - see what would change
flynt --dry-run src/

# Print result to stdout instead of modifying
flynt --stdout file.py

# Convert a string snippet
flynt -s '"Hello, %s" % name'

# Verbose output
flynt -v src/

# Quiet mode (no statistics)
flynt -q src/
```

### Conversion Control

```bash
# Skip %-formatting, only convert .format()
flynt --no-tp src/

# Skip .format(), only convert %-formatting
flynt --no-tf src/

# Convert string concatenations (Python 3.9+)
flynt --transform-concats src/

# Convert static joins (Python 3.9+)
flynt --transform-joins src/

# Limit line length for multiline conversions
flynt --line-length 100 src/

# Only convert single-line expressions
flynt --no-multiline src/

# Aggressive mode (may alter some edge case behavior)
flynt --aggressive src/
```

### CI/CD Integration

```bash
# Fail if any changes would be made (for CI)
flynt --fail-on-change src/

# Dry run with diff output
flynt --dry-run src/
```

## Transformations

### Printf-style (%-formatting)

```python
# Before
"Hello, %s" % name
"Hello, %s %s" % (first, last)
"Value: %d, Price: %.2f" % (count, price)
"%(name)s is %(age)d years old" % {"name": name, "age": age}

# After
f"Hello, {name}"
f"Hello, {first} {last}"
f"Value: {count}, Price: {price:.2f}"
f"{name} is {age} years old"
```

### .format() Style

```python
# Before
"Hello, {}".format(name)
"Hello, {0} {1}".format(first, last)
"Hello, {name}".format(name=name)
"{} + {} = {}".format(a, b, a + b)
"{:.2f}".format(value)

# After
f"Hello, {name}"
f"Hello, {first} {last}"
f"Hello, {name}"
f"{a} + {b} = {a + b}"
f"{value:.2f}"
```

### String Concatenation (--transform-concats)

```python
# Before
"Hello, " + name + "!"
"Value: " + str(count)
first + " " + last

# After
f"Hello, {name}!"
f"Value: {count}"
f"{first} {last}"
```

### Static Joins (--transform-joins)

```python
# Before
", ".join(["a", "b", "c"])
" ".join([first, middle, last])

# After
"a, b, c"
f"{first} {middle} {last}"
```

## Configuration

### pyproject.toml

```toml
[tool.flynt]
line-length = 88
transform-concats = true
transform-joins = false
aggressive = false
no-multiline = false
```

### Global Config (Unix)

Create `~/.config/flynt.toml`:

```toml
line-length = 100
verbose = true
```

### Global Config (Windows)

Create `~/.flynt.toml`:

```toml
line-length = 100
verbose = true
```

## Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/ikamensh/flynt
    rev: '1.0.0'
    hooks:
      - id: flynt
```

### Skip Specific Lines

```python
# Skip a single line
message = "Hello, %s" % name  # noqa: flynt

# Alternative syntax
message = "Hello, %s" % name  # flynt: skip
```

## Common Workflows

### Convert Entire Project

```bash
# Backup first (or use git)
git add -A && git commit -m "Before flynt conversion"

# Run flynt on source directory
flynt src/

# Review changes
git diff

# Run tests to verify
pytest
```

### Gradual Adoption

```bash
# Start with dry run
flynt --dry-run src/

# Convert file by file
flynt src/module1.py
pytest tests/test_module1.py

flynt src/module2.py
pytest tests/test_module2.py
```

### CI Pipeline Check

```bash
# In CI, fail if unconverted strings exist
flynt --fail-on-change --quiet src/
```

### Preview Mode

```bash
# See exact changes without modifying
flynt --dry-run src/ 2>&1 | less

# Or output to file
flynt --dry-run src/ > flynt-changes.txt 2>&1
```

## Best Practices

1. **Use version control**: Always commit before running flynt
2. **Run tests after**: F-strings can expose subtle bugs in edge cases
3. **Review aggressive mode**: `--aggressive` may change behavior in edge cases
4. **Start conservative**: Run without `--aggressive` first
5. **Combine with other tools**: Run Black/Ruff format after flynt

## Caveats and Edge Cases

### Behavior Differences

F-string conversion may alter behavior in edge cases:

```python
# Before: prints "1"
'%s' % (1,)

# After: prints "(1,)"
f'{(1,)}'
```

### Complex Expressions

Flynt skips conversions that would make code less readable:

```python
# Flynt may skip this (too complex)
"result: {}".format(
    very_long_function_call_with_many_arguments(
        arg1, arg2, arg3
    )
)
```

### Type Requirements

F-strings are stricter about types:

```python
# Before: works with implicit conversion
"count: %s" % some_object

# After: may need explicit str()
f"count: {some_object}"  # Works if __str__ defined
```

## Comparison with Alternatives

| Tool | F-string Conversion | Other Features |
|------|---------------------|----------------|
| **Flynt** | Specialized, thorough | Concat/join conversion |
| **Ruff UP032** | Basic conversion | Full linter suite |
| **Pyupgrade** | Conservative conversion | Full syntax upgrades |

### When to Use Flynt

- Primary focus on f-string conversion
- Need concat/join transformations
- Want specialized f-string tool

### When to Use Ruff/Pyupgrade

- Already using these tools
- Want all-in-one solution
- Simpler conversions are sufficient

## Detailed Reference

For comprehensive pattern examples, see [references/fstring-patterns.md](references/fstring-patterns.md).

## External Links

- [GitHub Repository](https://github.com/ikamensh/flynt)
- [PyPI Package](https://pypi.org/project/flynt/)
- [PEP 498 - Literal String Interpolation](https://peps.python.org/pep-0498/)
