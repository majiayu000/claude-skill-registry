---
name: investigate-dependencies
description: Conduct thorough dependency audits to identify redundant code, unused features, and improper usage patterns. Examines each import to ensure we're leveraging existing capabilities rather than reinventing functionality.
---

# Investigate Dependencies: Eliminating Redundant Code Through Dependency Mastery

## 🎯 Mission

Conduct line-by-line walkthroughs of modules to understand how we use external dependencies, identifying:
- **Redundant implementations** of functionality that already exists in imported modules
- **Unused capabilities** in dependencies that could simplify our code
- **Improper usage patterns** that don't align with the module's intended design
- **Missing error handling** for cases the dependency already covers

## 🔍 Investigation Protocol

### Step 1: Import Analysis

For each file under investigation, create an import inventory:

```markdown
## Import Inventory for [filename]

| Import | Source | Purpose | Documentation |
|--------|--------|---------|---------------|
| `uuid` | stdlib | Generate unique identifiers | https://docs.python.org/3/library/uuid.html |
| `FastAPI` | fastapi | Web framework | https://fastapi.tiangolo.com/ |
| `CustomUtil` | local | [Document what we think it does] | [Internal docs] |
```

### Step 2: Line-by-Line Dependency Usage Examination

For each location where an external module is used:

```markdown
### Usage Point: [Function/Method Name] (Lines X-Y)

**Code:**
```python
# Relevant code snippet showing dependency usage
```

**Questions to Answer:**
1. What are we using this dependency for?
2. What capabilities does this dependency offer beyond what we're using?
3. Are we reimplementing functionality the dependency already provides?
4. Does the dependency handle errors/edge cases we're also handling?
5. Are we using this dependency as the authors intended?

**Findings:**
- [Document any redundancies, missing capabilities, or misuse]
```

### Step 3: Documentation Deep Dive

For each significant dependency, review:

1. **Official documentation** - What does the module actually do?
2. **API reference** - What methods/functions are available?
3. **Error handling** - What exceptions does it raise?
4. **Best practices** - How do the authors recommend using it?
5. **Source code** (if needed) - What does the implementation reveal?

### Step 4: Redundancy Detection

Common areas where redundancy occurs:

#### Utility Functions
```python
# ❌ REDUNDANT: Reimplementing datetime.now(UTC)
def get_current_time():
    return datetime.datetime.now(datetime.timezone.utc)

# ✅ BETTER: Use the imported utility
from utils.timezone_utils import utc_now
current_time = utc_now()  # Already exists in the codebase
```

#### Error Handling
```python
# ❌ REDUNDANT: Manual JSON validation
def parse_json(data: str):
    try:
        result = json.loads(data)
        if not isinstance(result, dict):
            raise ValueError("Expected dict")
        return result
    except json.JSONDecodeError:
        return None

# ✅ BETTER: Use Pydantic which handles this
from pydantic import BaseModel
class MyData(BaseModel):
    # Pydantic handles JSON parsing, validation, and type checking
    pass
```

#### Data Validation
```python
# ❌ REDUNDANT: Manual UUID validation
def validate_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False

# ✅ BETTER: Use Pydantic's built-in UUID type
from uuid import UUID
from pydantic import BaseModel

class Request(BaseModel):
    user_id: UUID  # Pydantic validates this automatically
```

#### Configuration Management
```python
# ❌ REDUNDANT: Manual environment variable handling
def get_config():
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "5432"))
    # Manual type conversion, default handling, validation...

# ✅ BETTER: Use Pydantic Settings
from pydantic_settings import BaseSettings

class DatabaseConfig(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    # Pydantic handles env vars, types, defaults, validation
```

### Step 5: Capability Gap Analysis

For each dependency, document:

```markdown
## [Dependency Name] - Capability Analysis

### What We're Currently Using:
- [List actual usage]

### Available Capabilities We're Not Using:
- [Feature 1]: Could simplify [code location]
- [Feature 2]: Would eliminate [redundant implementation]
- [Feature 3]: Better error handling for [scenario]

### Recommendations:
1. [Specific refactoring suggestion with rationale]
2. [Another suggestion]
```

## 📋 Investigation Template

When conducting a dependency investigation, follow this structure:

```markdown
# Dependency Investigation: [filename]

## Executive Summary
- **Total Imports**: X (Y external, Z internal)
- **Redundancies Found**: N instances
- **Unused Capabilities**: M opportunities
- **Severity**: HIGH/MEDIUM/LOW

## Import Inventory
[Table of all imports with documentation links]

## Detailed Findings

### [Import 1]
**Usage Locations**: Lines X, Y, Z
**Current Usage**: [What we're doing with it]
**Available Features**: [What else it offers]
**Issues Found**:
- [Redundancy, misuse, or missed opportunity]
**Recommendation**: [Specific action to take]

### [Import 2]
[Same structure]

## Refactoring Recommendations

### Priority 1: Critical Redundancies
1. [High-impact changes that eliminate significant redundancy]

### Priority 2: Capability Enhancements
2. [Changes that leverage unused features]

### Priority 3: Code Simplification
3. [Minor improvements and cleanup]

## Implementation Impact
- **Lines Removed**: ~X
- **Complexity Reduction**: [Qualitative assessment]
- **Maintainability**: [How this improves long-term maintenance]
```

## 🎯 Focus Areas

### Common Redundancy Patterns

1. **Datetime Operations**
   - Check: Are we using `datetime.now()` instead of `utils.timezone_utils.utc_now()`?
   - Check: Manual timezone conversions vs. utility functions

2. **Type Validation**
   - Check: Manual `isinstance()` checks vs. Pydantic models
   - Check: Custom validators vs. Pydantic's Field validators

3. **JSON Handling**
   - Check: Manual `json.loads/dumps` vs. Pydantic's `.model_dump_json()`
   - Check: Custom serialization vs. FastAPI's `jsonable_encoder`

4. **UUID Operations**
   - Check: Manual UUID string conversion vs. type hints
   - Check: UUID validation vs. Pydantic UUID type

5. **Error Handling**
   - Check: Manual try/except around operations the library already handles
   - Check: Custom error messages vs. library's built-in messages

6. **Database Operations**
   - Check: Manual transaction management vs. framework's context managers
   - Check: Custom query builders vs. ORM capabilities

7. **Async Operations**
   - Check: Manual async coordination vs. framework utilities
   - Check: Custom timeouts vs. library-provided timeout mechanisms

## 🚨 Red Flags

Patterns that indicate potential redundancy:

- **"Wrapper" functions** that just call one library function with minimal logic
- **Type conversion utilities** when Pydantic could handle it
- **Custom validation** that duplicates Pydantic/FastAPI validation
- **Manual serialization** when libraries offer automatic serialization
- **Reimplemented utilities** that exist in the standard library
- **Defensive error handling** around well-behaved libraries

## ✅ Success Criteria

A successful dependency investigation produces:

1. **Complete documentation** of how each dependency is used
2. **Specific, actionable recommendations** for removing redundancy
3. **Evidence from official documentation** supporting recommendations
4. **Impact assessment** showing benefits of proposed changes
5. **No false positives** - only genuine redundancies, not legitimate custom logic

## 📚 Investigation Request Format

**Request Format:**

Please conduct a thorough walkthrough of [specific file/module], examining each line where we import or call external modules. For every external dependency referenced, investigate its source documentation and implementation to understand its full capabilities, error handling patterns, and intended usage. Document any instances where we're duplicating functionality that already exists in the imported module, implementing our own error handling for cases the module already covers, or not utilizing available features that could simplify our code. Pay special attention to utility functions, error handling, data validation, and configuration management - these are common areas where developers inadvertently reimplement existing functionality. The goal is to ensure we're properly leveraging our dependencies rather than writing redundant code, and that we're using these modules as their authors intended. Please create a summary noting any redundancies found and recommendations for refactoring to better utilize existing module capabilities.

## 🎓 Philosophy

**The Principle:** Every line of custom code is a maintenance burden. If a dependency we're already using can do it reliably and correctly, we should use it.

**The Balance:** Not all custom code is redundant. Sometimes we need custom logic for business requirements, performance optimization, or specific behavior. The investigation distinguishes between:
- **Redundant reimplementation** (bad) - doing what libraries already do
- **Custom business logic** (good) - domain-specific requirements
- **Performance optimization** (justifiable) - when library approach is insufficient

**The Goal:** A codebase that leverages dependencies fully, eliminating maintenance burden while preserving necessary custom logic.
