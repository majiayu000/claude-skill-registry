---
name: module-spec-generator
version: 1.0.0
description: |
  Generates module specifications following amplihack's brick philosophy template.
  Use when creating new modules or documenting existing ones to ensure they follow
  the brick & studs pattern. Analyzes code to extract: purpose, public contract,
  dependencies, test requirements.
---

# Module Spec Generator Skill

## Purpose

This skill automatically generates comprehensive module specifications from code analysis, ensuring adherence to amplihack's **brick philosophy** and enabling effective module regeneration without breaking system connections.

## When to Use This Skill

- **Creating new modules**: Generate specs before implementation to clarify requirements
- **Documenting existing modules**: Extract specifications from working code for future reference
- **Module reviews**: Verify specs accurately represent implemented contracts
- **Refactoring decisions**: Use specs to understand module boundaries and dependencies
- **Knowledge preservation**: Document expert patterns and design decisions

## Core Philosophy: Bricks & Studs

**Brick** = Self-contained module with ONE clear responsibility
**Stud** = Public contract (functions, API, data models) others connect to
**Regeneratable** = Can be rebuilt from specification without breaking connections

A good spec enables rebuilding ANY module independently while preserving its connection points.

## Specification Template

Every module specification includes these sections:

### 1. Module Overview

```
# [Module Name] Specification

## Purpose
One-sentence description of the module's core responsibility.

## Scope
What this module handles | What it explicitly does NOT handle

## Philosophy Alignment
How this module embodies brick principles and simplicity.
```

### 2. Public Contract (The "Studs")

```
## Public Interface

### Functions
- `function_name(param: Type) -> ReturnType`
  Brief description of what it does.

### Classes/Data Models
- `ClassName`
  - Fields: list with types
  - Key methods: list

### Constants/Enums
Important module-level constants and their purposes.
```

### 3. Dependencies

```
## Dependencies

### External Dependencies
- `library_name` (version): What it's used for

### Internal Dependencies
- `module_path`: How this module depends on it

### NO External Dependencies (Best Case)
Pure Python, standard library only.
```

### 4. Module Structure

```
## Module Structure

```

module_name/
├── **init**.py # Public interface via **all**
├── core.py # Main implementation
├── models.py # Data models (if needed)
├── utils.py # Internal utilities
├── tests/
│ ├── **init**.py
│ ├── test_core.py # Main functionality tests
│ ├── test_models.py # Data model tests (if needed)
│ └── fixtures/
│ └── sample_data.json
└── examples/
└── basic_usage.py # Usage examples

```

```

### 5. Test Requirements

```
## Test Requirements

### Unit Tests
- Test 1: Purpose and what it verifies
- Test 2: ...

### Integration Tests (if applicable)
- Test 1: ...

### Coverage Goal
Target test coverage percentage (typically 85%+)
```

### 6. Example Usage

````
## Example Usage

```python
from module_name import PublicFunction, DataModel

# Usage example 1
result = PublicFunction(input_data)

# Usage example 2
model = DataModel(field1="value", field2=123)
````

```

## Step-by-Step Analysis Process

### Step 1: Understand the Module
1. Read all module files (focus on `__init__.py` and core implementations)
2. Identify the single core responsibility
3. Note architectural patterns used (classes, functions, mixins, etc.)

### Step 2: Extract Public Contract
1. List all exports in `__all__` or equivalent
2. Document function signatures with full type hints
3. Identify data structures (classes, NamedTuple, dataclass)
4. Extract constants and their meanings
5. Include docstrings for each public item

### Step 3: Map Dependencies
1. Scan imports at module level
2. Categorize:
   - Standard library (good - include version constraints)
   - External packages (list version requirements)
   - Internal modules (note the module path)
3. Identify circular dependencies (red flag)

### Step 4: Analyze Module Structure
1. Map file organization
2. Identify what goes in each file
3. Note test fixtures and examples

### Step 5: Identify Test Requirements
1. What behaviors MUST be tested
2. What edge cases exist
3. What integration points need coverage
4. Suggest coverage target

### Step 6: Generate Spec Document
1. Create Specs/[module-name].md
2. Fill in all sections using analysis
3. Include example code
4. Verify spec allows module regeneration

## Usage Examples

### Example 1: Generate Spec for New Module

```

User: I'm creating a new authentication module.
Generate a spec that ensures it follows brick philosophy.

Claude:

1. Interviews user about module purpose, public functions, dependencies
2. Analyzes similar modules in codebase
3. Generates comprehensive spec with:
   - Clear single responsibility
   - Public contract defining studs
   - Test requirements
   - Example implementations
4. Saves to Specs/authentication.md

```

### Example 2: Document Existing Module

```

User: Generate a spec for the existing caching module.

Claude:

1. Analyzes .claude/tools/amplihack/caching/ directory
2. Extracts **all** exports
3. Documents public functions with signatures
4. Maps dependencies
5. Identifies test requirements
6. Creates Specs/caching.md
7. Offers to verify spec matches implementation

```

### Example 3: Verify Module Spec Accuracy

```

User: Check if the existing session management spec
accurately describes the implementation.

Claude:

1. Reads Specs/session-management.md
2. Analyzes actual code in .claude/tools/amplihack/session/
3. Compares:
   - Public contract (functions, signatures)
   - Dependencies listed
   - Test coverage
4. Reports discrepancies
5. Suggests spec updates if needed

````

## Analysis Checklist

### Code Analysis
- [ ] Read all Python files in module
- [ ] Identify `__all__` or equivalent public interface
- [ ] Extract all public function signatures
- [ ] Document all public classes with fields and methods
- [ ] List module-level constants
- [ ] Map all imports (external and internal)

### Philosophy Verification
- [ ] Single clear responsibility
- [ ] No unnecessary abstractions
- [ ] Public interface clear and minimal
- [ ] Dependencies are justified
- [ ] No external dependencies (if possible)
- [ ] Patterns align with amplihack principles

### Specification Quality
- [ ] Spec is complete and precise
- [ ] Code examples are accurate and working
- [ ] Test requirements are realistic
- [ ] Module structure is clear
- [ ] Someone could rebuild module from spec
- [ ] Regeneration preserves all connections

## Template for Module Specs

```markdown
# [Module Name] Specification

## Purpose
[Single sentence describing core responsibility]

## Scope
**Handles**: [What this module does]
**Does NOT handle**: [What is explicitly out of scope]

## Philosophy Alignment
- ✅ Ruthless Simplicity: [How it embodies this]
- ✅ Single Responsibility: [Core job]
- ✅ No External Dependencies: [True/False with reason]
- ✅ Regeneratable: [Yes, module can be rebuilt from this spec]

## Public Interface (The "Studs")

### Functions
```python
def primary_function(param: Type) -> ReturnType:
    """Brief description.

    Args:
        param: Description with constraints

    Returns:
        Description of return value
    """
````

### Classes

```python
class DataModel:
    """Brief description of responsibility.

    Attributes:
        field1 (Type): Description
        field2 (Type): Description
    """
```

### Constants

- `CONSTANT_NAME`: Description and usage

## Dependencies

### External

None - pure Python standard library

### Internal

- `.models`: Data structures
- `.utils`: Shared utilities

## Module Structure

```
module_name/
├── __init__.py       # Exports via __all__
├── core.py          # Implementation
├── models.py        # Data models
├── utils.py         # Utilities
├── tests/
│   └── test_core.py
└── examples/
    └── usage.py
```

## Test Requirements

### Core Functionality Tests

- ✅ Test primary_function with valid input
- ✅ Test error handling with invalid input
- ✅ Test edge cases

### Contract Verification

- ✅ All exported items in **all** work
- ✅ Type hints match actual behavior
- ✅ Return values match documentation

### Coverage Target

85%+ line coverage

## Example Usage

```python
from module_name import primary_function, DataModel

# Basic usage
result = primary_function(input_data)

# Data model usage
model = DataModel(field1="value", field2=123)
print(model.field1)
```

## Regeneration Notes

This module can be rebuilt from this specification while maintaining:

- ✅ Public contract (all "studs" preserved)
- ✅ Dependencies (same external/internal deps)
- ✅ Test interface (same test requirements)
- ✅ Module structure (same file organization)

```

## Output Location

Specifications are saved to: `Specs/[module-name].md`

This keeps all module specifications in a central, discoverable location.

## Integration with Builder Agent

After spec generation, the Builder Agent can:
1. Read the specification
2. Implement the module exactly as specified
3. Verify implementation matches spec
4. Run tests defined in spec
5. Regenerate modules when requirements change

## Quality Checks

After generating a spec, verify:

1. **Can someone rebuild the module from this spec?**
   - Yes = spec is complete
   - No = add missing details

2. **Does every exported function have a clear purpose?**
   - Yes = public interface is clear
   - No = combine or clarify functions

3. **Are all dependencies justified?**
   - Yes = move forward
   - No = remove or replace with simpler approach

4. **Would this prevent breaking other modules?**
   - Yes = studs are well-defined
   - No = clarify connection points

## Common Pitfalls to Avoid

- **Over-specification**: Don't specify implementation details
- **Under-documentation**: Document WHY, not just WHAT
- **Ambiguous contracts**: Be precise about inputs/outputs
- **Unclear dependencies**: Explicitly list all external/internal deps
- **Missing examples**: Always include working code examples
- **Ignored test requirements**: Tests define contract completeness

## Success Criteria

A good module spec:
- [ ] Single, clear responsibility
- [ ] Complete public interface documentation
- [ ] Explicit dependency list
- [ ] Realistic test requirements
- [ ] Working code examples
- [ ] Someone can rebuild module from it
- [ ] Regeneration preserves all connections
- [ ] Follows brick philosophy
- [ ] No future-proofing or speculation
- [ ] Regeneratable without breaking system
```
