---
name: code-smell-detector
version: 1.0.0
description: |
  Identifies anti-patterns specific to amplihack philosophy.
  Use when reviewing code for quality issues or refactoring.
  Detects: over-abstraction, complex inheritance, large functions (>50 lines), tight coupling, missing __all__ exports.
  Provides specific fixes and explanations for each smell.
---

# Code Smell Detector Skill

## Purpose

This skill identifies anti-patterns that violate amplihack's development philosophy and provides constructive, specific fixes. It ensures code maintains ruthless simplicity, modular design, and zero-BS implementations.

## When to Use This Skill

- **Code review**: Identify violations before merging
- **Refactoring**: Find opportunities to simplify and improve code quality
- **New module creation**: Catch issues early in development
- **Philosophy compliance**: Ensure code aligns with amplihack principles
- **Learning**: Understand why patterns are problematic and how to fix them
- **Mentoring**: Educate team members on philosophy-aligned code patterns

## Core Philosophy Reference

**Amplihack Development Philosophy focuses on:**

- **Ruthless Simplicity**: Every abstraction must justify its existence
- **Modular Design (Bricks & Studs)**: Self-contained modules with clear connection points
- **Zero-BS Implementation**: No stubs, no placeholders, only working code
- **Single Responsibility**: Each module/function has ONE clear job

## Code Smells Detected

### 1. Over-Abstraction

**What It Is**: Unnecessary layers of abstraction, generic base classes, or interfaces that don't provide clear value.

**Why It's Bad**: Violates "ruthless simplicity" - adds complexity without proportional benefit. Makes code harder to understand and maintain.

**Red Flags**:

- Abstract base classes with only one implementation
- Generic helper classes that do very little
- Deep inheritance hierarchies (3+ levels)
- Interfaces for single implementations
- Over-parameterized functions

**Example - SMELL**:

```python
# BAD: Over-abstracted
class DataProcessor(ABC):
    @abstractmethod
    def process(self, data):
        pass

class SimpleDataProcessor(DataProcessor):
    def process(self, data):
        return data * 2
```

**Example - FIXED**:

```python
# GOOD: Direct implementation
def process_data(data):
    """Process data by doubling it."""
    return data * 2
```

**Detection Checklist**:

- [ ] Abstract classes with only 1-2 concrete implementations
- [ ] Generic utility classes that don't encapsulate state
- [ ] Type hierarchies deeper than 2 levels
- [ ] Mixins solving single problems

**Fix Strategy**:

1. Identify what the abstraction solves
2. Check if you really need multiple implementations now
3. Delete the abstraction - use direct implementation
4. If multiple implementations needed later, refactor then
5. Principle: Avoid future-proofing

---

### 2. Complex Inheritance

**What It Is**: Deep inheritance chains, multiple inheritance, or convoluted class hierarchies that obscure code flow.

**Why It's Bad**: Makes code hard to follow, creates tight coupling, violates simplicity principle. Who does what becomes unclear.

**Red Flags**:

- 3+ levels of inheritance (GrandparentClass -> ParentClass -> ChildClass)
- Multiple inheritance from non-interface classes
- Inheritance used for code reuse instead of composition
- Overriding multiple levels of methods
- "Mixin" classes for cross-cutting concerns

**Example - SMELL**:

```python
# BAD: Complex inheritance
class Entity:
    def save(self): pass
    def load(self): pass

class TimestampedEntity(Entity):
    def add_timestamp(self): pass

class AuditableEntity(TimestampedEntity):
    def audit_log(self): pass

class User(AuditableEntity):
    def authenticate(self): pass
```

**Example - FIXED**:

```python
# GOOD: Composition over inheritance
class User:
    def __init__(self, storage, timestamp_service, audit_log):
        self.storage = storage
        self.timestamps = timestamp_service
        self.audit = audit_log

    def save(self):
        self.storage.save(self)
        self.timestamps.record()
        self.audit.log("saved user")
```

**Detection Checklist**:

- [ ] Inheritance depth > 2 levels
- [ ] Multiple inheritance from concrete classes
- [ ] Methods overridden at multiple inheritance levels
- [ ] Inheritance hierarchy with no code reuse

**Fix Strategy**:

1. Use composition instead of inheritance
2. Pass services as constructor arguments
3. Each class handles its own responsibility
4. Easier to test, understand, and modify

---

### 3. Large Functions (>50 Lines)

**What It Is**: Functions that do too many things and are difficult to understand, test, and modify.

**Why It's Bad**: Violates single responsibility, makes testing harder, increases bug surface area, reduces code reusability.

**Red Flags**:

- Functions with >50 lines of code
- Multiple indentation levels (3+ nested if/for)
- Functions with 5+ parameters
- Functions that need scrolling to see all of them
- Complex logic that's hard to name

**Example - SMELL**:

```python
# BAD: Large function doing multiple things
def process_user_data(user_dict, validate=True, save=True, notify=True, log=True):
    if validate:
        if not user_dict.get('email'):
            raise ValueError("Email required")
        if not '@' in user_dict['email']:
            raise ValueError("Invalid email")

    user = User(
        name=user_dict['name'],
        email=user_dict['email'],
        phone=user_dict['phone']
    )

    if save:
        db.save(user)

    if notify:
        email_service.send(user.email, "Welcome!")

    if log:
        logger.info(f"User {user.name} created")

    # ... 30+ more lines of mixed concerns
    return user
```

**Example - FIXED**:

```python
# GOOD: Separated concerns
def validate_user_data(user_dict):
    """Validate user data structure."""
    if not user_dict.get('email'):
        raise ValueError("Email required")
    if '@' not in user_dict['email']:
        raise ValueError("Invalid email")

def create_user(user_dict):
    """Create user object from data."""
    return User(
        name=user_dict['name'],
        email=user_dict['email'],
        phone=user_dict['phone']
    )

def process_user_data(user_dict):
    """Orchestrate user creation workflow."""
    validate_user_data(user_dict)
    user = create_user(user_dict)
    db.save(user)
    email_service.send(user.email, "Welcome!")
    logger.info(f"User {user.name} created")
    return user
```

**Detection Checklist**:

- [ ] Function body >50 lines
- [ ] 3+ levels of nesting
- [ ] Multiple unrelated operations
- [ ] Hard to name succinctly
- [ ] 5+ parameters

**Fix Strategy**:

1. Extract helper functions for each concern
2. Give each function a clear, single purpose
3. Compose small functions into larger workflows
4. Each function should fit on one screen
5. Easy to name = usually doing one thing

---

### 4. Tight Coupling

**What It Is**: Modules/classes directly depend on concrete implementations instead of abstractions, making them hard to test and modify.

**Why It's Bad**: Changes in one module break others. Hard to test in isolation. Violates modularity principle.

**Red Flags**:

- Direct instantiation of classes inside functions (`db = Database()`)
- Deep attribute access (`obj.service.repository.data`)
- Hardcoded class names in conditionals
- Module imports everything from another module
- Circular dependencies between modules

**Example - SMELL**:

```python
# BAD: Tight coupling
class UserService:
    def create_user(self, name, email):
        db = Database()  # Hardcoded dependency
        user = db.save_user(name, email)

        email_service = EmailService()  # Hardcoded dependency
        email_service.send(email, "Welcome!")

        return user

    def get_user(self, user_id):
        db = Database()
        return db.find_user(user_id)
```

**Example - FIXED**:

```python
# GOOD: Loose coupling via dependency injection
class UserService:
    def __init__(self, db, email_service):
        self.db = db
        self.email = email_service

    def create_user(self, name, email):
        user = self.db.save_user(name, email)
        self.email.send(email, "Welcome!")
        return user

    def get_user(self, user_id):
        return self.db.find_user(user_id)

# Usage:
user_service = UserService(db=PostgresDB(), email_service=SMTPService())
```

**Detection Checklist**:

- [ ] Class instantiation inside methods (`Service()`)
- [ ] Deep attribute chaining (3+ dots)
- [ ] Hardcoded class references
- [ ] Circular imports or dependencies
- [ ] Module can't be tested without other modules

**Fix Strategy**:

1. Accept dependencies as constructor parameters
2. Use dependency injection
3. Create test doubles (mocks) easily
4. Swap implementations without changing code
5. Each module is independently testable

---

### 5. Missing `__all__` Exports (Python)

**What It Is**: Python modules that don't explicitly define their public interface via `__all__`.

**Why It's Bad**: Unclear what's public vs internal. Users import private implementation details. Violates the "stud" concept - unclear connection points.

**Red Flags**:

- No `__all__` in `__init__.py`
- Modules expose internal functions/classes
- Users uncertain what to import
- Private names (`_function`) still accessible
- Documentation doesn't match exports

**Example - SMELL**:

```python
# BAD: No __all__ - unclear public interface
# module/__init__.py
from .core import process_data, _internal_helper
from .utils import validate_input, LOG_LEVEL

# What should users import? All of it? Only some?
```

**Example - FIXED**:

```python
# GOOD: Clear public interface via __all__
# module/__init__.py
from .core import process_data
from .utils import validate_input

__all__ = ['process_data', 'validate_input']

# Users know exactly what's public and what to use
```

**Detection Checklist**:

- [ ] Missing `__all__` in `__init__.py`
- [ ] Internal functions (prefixed with `_`) exposed
- [ ] Unclear what's "public API"
- [ ] All imports at module level

**Fix Strategy**:

1. Add `__all__` to every `__init__.py`
2. List ONLY the public functions/classes
3. Prefix internal implementation with `_`
4. Update documentation to match `__all__`
5. Clear = users know exactly what to use

---

## Analysis Process

### Step 1: Scan Code Structure

1. Review file organization and module boundaries
2. Identify inheritance hierarchies
3. Scan for large functions (count lines)
4. Note `__all__` presence/absence
5. Check for tight coupling patterns

### Step 2: Analyze Each Smell

For each potential issue:

1. Confirm it violates philosophy
2. Measure severity (critical/major/minor)
3. Find specific line numbers
4. Note impact on system

### Step 3: Generate Fixes

For each smell found:

1. Provide clear explanation of WHY it's bad
2. Show BEFORE code
3. Show AFTER code with detailed comments
4. Explain philosophy principle violated
5. Give concrete refactoring steps

### Step 4: Create Report

1. List all smells found
2. Prioritize by severity/impact
3. Include specific examples
4. Provide actionable fixes
5. Reference philosophy docs

---

## Detection Rules

### Rule 1: Abstract Base Classes

**Check**: `class X(ABC)` with exactly 1 concrete implementation

```python
# BAD pattern detection
- Count implementations of abstract class
- If count <= 2 and not used as interface: FLAG
```

**Fix**: Remove abstraction, use direct implementation

### Rule 2: Inheritance Depth

**Check**: Class hierarchy depth

```python
# BAD pattern detection
- Follow inheritance chain: class -> parent -> grandparent...
- If depth > 2: FLAG
```

**Fix**: Use composition instead

### Rule 3: Function Line Count

**Check**: All function bodies

```python
# BAD pattern detection
- Count lines in function (excluding docstring)
- If > 50 lines: FLAG
- If > 3 nesting levels: FLAG
```

**Fix**: Extract helper functions

### Rule 4: Dependency Instantiation

**Check**: Class instantiation inside methods/functions

```python
# BAD pattern detection
- Search for "= ServiceName()" inside methods
- If found: FLAG
```

**Fix**: Pass as constructor argument

### Rule 5: Missing **all**

**Check**: Python modules

```python
# BAD pattern detection
- Look for __all__ definition
- If missing: FLAG
- If __all__ incomplete: FLAG
```

**Fix**: Define explicit `__all__`

---

## Common Code Smells & Quick Fixes

### Smell: "Utility Class" Holder

```python
# BAD
class StringUtils:
    @staticmethod
    def clean(s):
        return s.strip().lower()
```

**Fix**: Use direct function

```python
# GOOD
def clean_string(s):
    return s.strip().lower()
```

---

### Smell: "Manager" Class

```python
# BAD
class UserManager:
    def create(self): pass
    def update(self): pass
    def delete(self): pass
    def validate(self): pass
    def email(self): pass
```

**Fix**: Split into focused services

```python
# GOOD
class UserService:
    def __init__(self, db, email):
        self.db = db
        self.email = email

    def create(self): pass
    def update(self): pass
    def delete(self): pass

def validate_user(user): pass
```

---

### Smell: God Function

```python
# BAD - 200 line function doing everything
def process_order(order_data, validate, save, notify, etc...):
    # 200 lines mixing validation, transformation, DB, email, logging
```

**Fix**: Compose small functions

```python
# GOOD
def process_order(order_data):
    validate_order(order_data)
    order = create_order(order_data)
    save_order(order)
    notify_customer(order)
    log_creation(order)
```

---

### Smell: Brittle Inheritance

```python
# BAD
class Base:
    def work(self): pass
class Middle(Base):
    def work(self):
        return super().work()
class Derived(Middle):
    def work(self):
        return super().work()  # Which work()?
```

**Fix**: Use clear, testable composition

```python
# GOOD
class Worker:
    def __init__(self, validator, transformer):
        self.validator = validator
        self.transformer = transformer

    def work(self, data):
        self.validator.check(data)
        return self.transformer.apply(data)
```

---

### Smell: Hidden Dependencies

```python
# BAD
def fetch_data(user_id):
    db = Database()  # Where's this coming from?
    return db.query(f"SELECT * FROM users WHERE id={user_id}")
```

**Fix**: Inject dependencies explicitly

```python
# GOOD
def fetch_data(user_id, db):
    return db.query(f"SELECT * FROM users WHERE id={user_id}")

# Or in a class:
class UserRepository:
    def __init__(self, db):
        self.db = db

    def fetch(self, user_id):
        return self.db.query(f"SELECT * FROM users WHERE id={user_id}")
```

---

## Usage Examples

### Example 1: Review New Module

```
User: Review this new authentication module for code smells.

Claude:
1. Scans all Python files in module
2. Checks for each smell type
3. Finds:
   - Abstract base class with 1 implementation
   - Large 120-line authenticate() function
   - Missing __all__ in __init__.py
4. Provides specific fixes with before/after code
5. Explains philosophy violations
```

### Example 2: Identify Tight Coupling

```
User: Find tight coupling in this user service.

Claude:
1. Traces all dependencies
2. Finds hardcoded Database() instantiation
3. Finds direct EmailService() creation
4. Shows dependency injection fix
5. Includes test example showing why it matters
```

### Example 3: Simplify Inheritance

```
User: This class hierarchy is too complex.

Claude:
1. Maps inheritance tree (finds 4 levels)
2. Shows each level doing what
3. Suggests composition approach
4. Provides before/after refactoring
5. Explains how it aligns with brick philosophy
```

---

## Analysis Checklist

### Philosophy Compliance

- [ ] No unnecessary abstractions
- [ ] Single responsibility per class/function
- [ ] Clear public interface (`__all__`)
- [ ] Dependencies injected, not hidden
- [ ] Inheritance depth <= 2 levels
- [ ] Functions < 50 lines
- [ ] No dead code or stubs

### Code Quality

- [ ] Each function has one clear job
- [ ] Easy to understand at a glance
- [ ] Easy to test in isolation
- [ ] Easy to modify without breaking others
- [ ] Clear naming reflects responsibility

### Modularity

- [ ] Modules are independently testable
- [ ] Clear connection points ("studs")
- [ ] Loose coupling between modules
- [ ] Explicit dependencies

---

## Success Criteria for Review

A code review using this skill should:

- [ ] Identify all violations of philosophy
- [ ] Provide specific line numbers
- [ ] Show before/after examples
- [ ] Explain WHY each is a problem
- [ ] Suggest concrete fixes
- [ ] Include test strategies
- [ ] Reference philosophy docs
- [ ] Prioritize by severity
- [ ] Be constructive and educational
- [ ] Help writer improve future code

---

## Integration with Code Quality Tools

**When to Use This Skill**:

- During code review (before merge)
- In pull request comments
- Before creating new modules
- When refactoring legacy code
- To educate team members
- In design review meetings

**Works Well With**:

- Code review process
- Module spec generation
- Refactoring workflows
- Architecture discussions
- Mentoring and learning

---

## Resources

- **Philosophy**: `.claude/context/PHILOSOPHY.md`
- **Patterns**: `.claude/context/PATTERNS.md`
- **Brick Philosophy**: See "Modular Architecture for AI" in PHILOSOPHY.md
- **Zero-BS**: See "Zero-BS Implementations" in PHILOSOPHY.md

---

## Remember

This skill helps maintain code quality by:

1. Catching issues before they become technical debt
2. Educating developers on philosophy
3. Keeping code simple and maintainable
4. Preventing tightly-coupled systems
5. Making code easier to understand and modify

Use it constructively - the goal is learning and improvement, not criticism.
