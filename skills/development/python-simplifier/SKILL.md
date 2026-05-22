---
name: python-simplifier
description: Simplify overly complex Python code. Use when user asks to simplify, refactor, clean up, make more readable, reduce complexity, improve code quality, find code smells, detect duplicates, or analyze coupling in Python code. Triggers on requests like "simplify this code", "this is too complex", "make this more readable", "refactor this", "clean this up", "find issues", "analyze this codebase", or when reviewing code that exhibits complexity anti-patterns. For Django-specific analysis, use the django-simplifier skill instead.
---

# Python Code Simplifier

Transform complex, hard-to-maintain Python code into clean, readable, idiomatic solutions.

## Analysis Scripts

```bash
# Comprehensive analysis (runs all checks)
python scripts/analyze_all.py /path/to/project

# Individual analyzers:
python scripts/analyze_complexity.py .       # Cyclomatic/cognitive complexity
python scripts/find_code_smells.py .         # Mutable defaults, bare excepts, etc.
python scripts/find_overengineering.py .     # YAGNI violations, unused abstractions
python scripts/find_dead_code.py .           # Unused imports, functions, variables
python scripts/find_unpythonic.py .          # Non-idiomatic patterns
python scripts/find_coupling_issues.py .     # Feature envy, low cohesion
python scripts/find_duplicates.py .          # Structural duplicate detection

# JSON output for CI/tooling
python scripts/analyze_all.py . --format json > report.json
```

## Workflow

1. **Analyze**: Run `analyze_all.py` to identify all issues
2. **Prioritize**: Address high-severity issues (🔴) first
3. **Simplify**: Apply patterns below incrementally
4. **Verify**: Ensure simplified code is functionally equivalent

## Simplification Principles

1. **YAGNI**: Don't add abstractions until needed
2. **Preserve behavior**: Simplification ≠ changing functionality
3. **One change at a time**: Incremental is safer
4. **Readability over cleverness**: Clear beats "smart"
5. **Keep related code together**: Locality matters

## Common Simplification Patterns

### Extract and Name

```python
# Before: Complex inline condition
if user.age >= 18 and user.country in ALLOWED and not user.banned:

# After: Named condition
is_eligible = user.age >= 18 and user.country in ALLOWED and not user.banned
if is_eligible:
```

### Early Returns

```python
# Before: Deep nesting
def process(data):
    if data:
        if data.valid:
            if data.ready:
                return compute(data)
    return None

# After: Guard clauses
def process(data):
    if not data or not data.valid or not data.ready:
        return None
    return compute(data)
```

### Comprehensions

```python
# Before: Manual loop
result = []
for item in items:
    if item.active:
        result.append(item.name)

# After: List comprehension
result = [item.name for item in items if item.active]
```

### Dictionary Techniques

```python
# Before: Verbose key checking
if key in d:
    value = d[key]
else:
    value = default

# After: get() with default
value = d.get(key, default)

# Before: Manual grouping
groups = {}
for item in items:
    if item.category not in groups:
        groups[item.category] = []
    groups[item.category].append(item)

# After: defaultdict
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)
```

### Context Managers

```python
# Before: Manual cleanup
f = open('file.txt')
try:
    data = f.read()
finally:
    f.close()

# After: with statement
with open('file.txt') as f:
    data = f.read()
```

## Over-Engineering Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Single-impl interface | Abstract class with one subclass | Merge or wait for need |
| Unnecessary factory | Factory that creates one type | Direct instantiation |
| Premature strategy | Strategy pattern with one strategy | Simple function |
| Thin wrapper | Class that just delegates | Use wrapped class directly |
| Speculative generality | Code for "future needs" | Delete it (YAGNI) |
| Deep inheritance | 4+ levels of inheritance | Composition over inheritance |

## Code Smells Quick Reference

| Smell | Detection | Fix |
|-------|-----------|-----|
| Mutable default | `def f(x=[])` | Use `None`, create inside |
| Bare except | `except:` | `except Exception:` |
| God class | 15+ methods, 10+ attrs | Split into focused classes |
| Long function | 50+ lines | Extract helper functions |
| Deep nesting | 4+ levels | Early returns, extract |
| Feature envy | Method uses other class more | Move method |
| Magic numbers | Unexplained numeric literals | Named constants |

## Script Reference

| Script | What It Detects |
|--------|-----------------|
| `analyze_complexity.py` | Cyclomatic complexity, cognitive complexity, nesting depth, function length, parameter count, class size |
| `find_code_smells.py` | Mutable defaults, bare excepts, magic numbers, type comparisons, god classes, data classes, boolean blindness |
| `find_overengineering.py` | Single-implementation interfaces, unused abstractions, unnecessary factories/builders, thin wrappers, premature strategies |
| `find_dead_code.py` | Unused imports, unused functions/classes, unused parameters, unreachable code, constant conditions |
| `find_unpythonic.py` | `range(len())`, `== True/False/None`, swallowed exceptions, manual index tracking |
| `find_coupling_issues.py` | Feature envy, low cohesion (LCOM), message chains, middle man classes |
| `find_duplicates.py` | Structurally similar code blocks using AST normalization |

## When NOT to Simplify

- Working legacy code with no tests
- Performance-critical hot paths (measure first)
- Code that will be replaced soon
- External API constraints requiring complexity
