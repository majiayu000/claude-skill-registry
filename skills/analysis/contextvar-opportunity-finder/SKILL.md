---
name: contextvar-opportunity-finder
description: Detect explicit user_id parameters in functions to identify potential opportunities for using ambient context. This is an investigation tool that flags instances for human review, not a prescriptive analyzer.
---

# Contextvar Opportunity Finder

An intelligent grep tool that finds all explicit `user_id` usage patterns in Python code. Reports findings with context for human review.

---

## Core Principle

This is a **detection-only** skill - It finds and reports all instances of explicit user_id usage without making judgments about correctness.

Read every file completely, one at a time, and report findings for EACH file before moving to the next. No shortcuts, no grep tricks, no "I'll infer from 
patterns". Complete reads only!

**What it does**: Scans code, detects patterns, reports everything it finds.

**What it doesn't do**: Make recommendations, filter results, or determine what's "right" or "wrong".

---

## Detection Patterns

### Pattern 1: Direct user_id Parameter

Look for functions with `user_id` in their parameters:
```python
def function_name(..., user_id: str, ...):
def function_name(..., user_id: Optional[str], ...):
def function_name(..., user_id=None, ...):
```

### Pattern 2: user_id Extraction from Dicts/Objects

Look for functions extracting user_id from parameters:
```python
def function_name(self, context: Dict[str, Any]):
    user_id = context.get('user_id')

def function_name(self, event):
    user_id = event.user_id
```

### Pattern 3: Redundant Context Setting

Look for code that sets context then passes user_id:
```python
set_current_user_id(user_id)
result = some_function(user_id)  # Passing after setting
```

### Pattern 4: Threading Through Layers

Look for user_id passed through multiple function calls:
```python
def handle_request(user_id):
    result = process_data(user_id)

def process_data(user_id):
    return validate_data(user_id)

def validate_data(user_id):
    # Three layers deep
```

### Pattern 5: Bad Dual-Mode Pattern

Constructor accepts optional user_id but methods still require it:
```python
class Service:
    def __init__(self, user_id: Optional[str] = None):
        self.user_id = user_id or get_current_user_id()

    def get_data(self, user_id: str):  # Still requires parameter!
        # Ignores self.user_id
```

### Pattern 6: Convenience Function Wrappers

Functions that exist only to extract user_id and pass it:
```python
def store_api_key_for_current_user(service_name: str, api_key: str):
    user_id = get_current_user_id()
    service.store_credential(user_id, 'api_key', service_name, api_key)
```

### Pattern 7: Request Body User IDs

Models/endpoints accepting user_id in request payloads:
```python
class LogoutRequest(BaseModel):
    user_id: str  # Security risk!
```

---

## Context Clues to Report

When reporting each instance, note these surrounding context clues:

### Class/Inheritance Context
- What class is the method in?
- What does the class inherit from?
- Is it a service, repository, API handler, etc?

### Function Context
- Function name
- Decorators on the function
- Parameters beyond user_id
- Return type annotations

### Call Context
- What's calling this function?
- What's this function calling with user_id?
- Is it part of a chain of calls?

### Code Patterns
- Is there `set_current_user_id()` nearby?
- Is there `get_current_user_id()` in the same class/file?
- Are there convenience wrappers around this function?
- Does the constructor have a different pattern than methods?

### File/Module Context
- Filename and path
- What kind of module is it? (api/, services/, repositories/, tools/, etc)
- Import statements that might indicate usage patterns

---

## Investigation Process

1. **Find all user_id parameters** in the file or directory
2. **Detect which pattern it matches** (1-7)
3. **Note the context clues** around each instance
4. **Report everything found** without filtering

---

## Output Format

```
## Explicit user_id Usage Report

**Found N instances across M files**

### path/to/file.py
Line X: def function_name(self, user_id: str, data: Dict):
  Pattern: Direct user_id parameter
  Context: Method in SomeClass, inherits from BaseClass

Line Y: user_id = event.user_id
  Pattern: Extracting from object
  Context: Inside handle_event() method

Line Z: self.some_service.process(user_id, ...)
  Pattern: Threading through layers
  Context: Calling another service with user_id

### path/to/another.py
Line A: def __init__(self, user_id: Optional[str] = None):
        self.user_id = user_id or get_current_user_id()
Line B: def store_data(self, user_id: str, ...):
  Pattern: Bad dual-mode pattern
  Context: Constructor has dual-mode but methods require explicit

Line C: set_current_user_id(user_id)
        result = service.method(user_id)
  Pattern: Redundant context setting
  Context: Sets ambient context then passes explicitly

### path/to/models.py
Line D: class SomeRequest(BaseModel):
            user_id: str
  Pattern: Request body user_id
  Context: Pydantic model for API endpoint

... continues for all findings ...
```

The report simply shows:
- Where user_id appears
- What pattern it matches
- Basic context about its location
- No judgments about correctness

---

## What This Tool Does NOT Do

- Does NOT determine if explicit user_id is "wrong"
- Does NOT prescribe specific fixes
- Does NOT judge architectural decisions
- Does NOT whitelist certain files or patterns
- Does NOT make recommendations

This is purely an investigation tool that surfaces instances for human review.

---

## What This Tool Finds

1. All functions/methods with `user_id` parameters
2. Places where `user_id` is extracted from objects or dicts
3. Chains of functions passing `user_id` through multiple layers
4. Classes with inconsistent patterns (constructor vs methods)
5. Wrapper functions that exist just to handle `user_id`
6. API models accepting `user_id` in request bodies
7. Places where context is set but `user_id` is still passed

---

## Quick Reference

| Pattern | What to Look For | Example |
|---------|------------------|---------|
| `def fn(user_id: str)` | Functions with explicit user_id parameter | Service methods, API handlers |
| `user_id = context.get('user_id')` | Extracting from dicts/objects | Event handlers, context processing |
| `set_current_user_id(uid); fn(uid)` | Setting context then passing explicitly | API endpoints, request handlers |
| Multiple layers passing user_id | Threading through call chains | API → Service → Repository |
| `user_id: Optional[str] = None` | Optional parameters with fallback | Dual-mode constructors/methods |
| `class Request(user_id: str)` | Request body models | Pydantic models for endpoints |
| Convenience wrappers | Functions that just extract and pass | `*_for_current_user()` helpers |

## Summary

This is an intelligent grep tool for finding `user_id` usage patterns. It:

- **DOES**: Find all instances of explicit user_id usage
- **DOES**: Detect which pattern each instance matches
- **DOES**: Report context clues around each finding
- **DOES NOT**: Judge whether any instance is "wrong"
- **DOES NOT**: Make recommendations
- **DOES NOT**: Filter results

Think of it as "grep for user_id patterns" with better context awareness.
