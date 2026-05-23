---
name: minimal-abstractions
description: |
  Evaluates and prevents unnecessary abstractions by analyzing interfaces, layers, and patterns
  against concrete requirements. Use when evaluating new abstractions, reviewing architecture proposals,
  detecting over-engineering, or simplifying existing code. Triggers on "is this abstraction necessary",
  "too many layers", "simplify architecture", "reduce complexity", "over-engineered", "do we need
  this interface", or when reviewing design patterns.
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Minimal Abstractions

## Quick Start

Before adding a new abstraction (interface, abstract class, wrapper, layer), ask:
1. Does a similar abstraction already exist in this project?
2. Are there 2+ concrete use cases requiring this abstraction RIGHT NOW?
3. Is the complexity cost justified by actual flexibility needs?

If any answer is "no" or "maybe" → Don't add it. Use the simplest solution that works.

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Core Philosophy
4. Abstraction Evaluation Checklist
5. Detection Patterns (Red Flags)
6. Examples: Good vs Over-Engineered
7. Integration with Architecture Validation
8. Expected Outcomes
9. Red Flags to Avoid

## When to Use This Skill

**Explicit Triggers (User asks):**
- "Is this abstraction necessary?"
- "Are we over-engineering this?"
- "Too many layers in this code"
- "Simplify this architecture"
- "Reduce complexity"
- "Do we need this interface/wrapper/layer?"
- "Should we use [design pattern]?"

**Implicit Triggers (Autonomous invocation):**
- Reviewing pull requests with new interfaces/abstract classes
- Architecture proposals introducing new layers
- Code reviews where new patterns are introduced
- Refactoring tasks aimed at simplification
- When a new abstraction is proposed and only one implementation exists

**Debugging/Problem Triggers:**
- Maintenance burden is high due to abstraction complexity
- Team members confused by excessive indirection
- Tests are difficult to write due to layering
- Simple changes require touching multiple abstraction layers

## What This Skill Does

This skill provides a systematic framework for:
- Evaluating whether new abstractions are warranted
- Detecting over-engineering and unnecessary complexity
- Guiding developers to use existing project abstractions
- Preventing abstraction proliferation
- Simplifying code by removing unneeded layers

## Instructions

When evaluating an abstraction:

1. **Search for existing abstractions** - Use Grep/Read to find similar patterns in codebase
2. **Apply the evaluation checklist** - Run through all 5 questions in section 4
3. **Check for red flags** - Scan code for patterns in section 5
4. **Recommend simpler alternative** - Provide concrete code example
5. **Document decision** - Explain why abstraction is/isn't needed

## Core Philosophy

### The Abstraction Principle

**Abstractions are not free** - every interface, wrapper, layer, or pattern adds:
- Cognitive load (developers must understand the abstraction)
- Maintenance burden (more code to test, debug, refactor)
- Indirection cost (harder to trace execution flow)
- Rigidity (abstractions create assumptions that resist change)

**When abstractions ARE valuable:**
- Multiple concrete implementations exist or are planned imminently
- Decoupling is critical (e.g., domain from infrastructure in Clean Architecture)
- Testability requires dependency injection
- Third-party integrations need isolation

**When abstractions are NOT valuable:**
- "We might need it someday" (YAGNI - You Aren't Gonna Need It)
- "It's a best practice" (without understanding why)
- Only one implementation exists and no others are planned
- Wrapping for wrapping's sake

### Prefer Existing Abstractions

Before creating a new abstraction:
1. Search the codebase for similar patterns
2. Extend or adapt existing abstractions
3. Reuse project-standard patterns (e.g., Repository, Service, Handler)
4. Only create new abstractions when existing ones truly don't fit

## Abstraction Evaluation Checklist

Use this checklist before adding ANY new abstraction (interface, abstract class, wrapper, layer):

### Question 1: Does this abstraction already exist?
- [ ] Searched codebase for similar interfaces/abstractions
- [ ] Checked project architecture docs for standard patterns
- [ ] Reviewed existing layers (domain, application, infrastructure)
- [ ] Considered extending existing abstractions instead

**Action:** If similar abstraction exists → Use it. Don't create a new one.

### Question 2: Do we have 2+ concrete implementations RIGHT NOW?
- [ ] Count current implementations (not hypothetical future ones)
- [ ] Verify implementations are actually different (not just copy-paste)
- [ ] Check if "multiple implementations" are really needed

**Action:** If <2 implementations → Skip the abstraction. Use concrete implementation directly.

### Question 3: Is there a concrete business/technical requirement?
- [ ] Can you name the specific requirement driving this abstraction?
- [ ] Is the requirement current (not speculative)?
- [ ] Would removing this abstraction make the code harder to maintain?

**Action:** If requirement is speculative → Don't build it yet. Wait for actual need.

### Question 4: What is the complexity cost?
- [ ] Count files touched to add this abstraction
- [ ] Estimate lines of code added (interface + implementations + tests)
- [ ] Consider cognitive load for new team members
- [ ] Evaluate impact on debugging and tracing

**Action:** If cost > benefit → Simplify. Use direct solution.

### Question 5: Can we solve this with simpler patterns?
- [ ] Would a simple function work instead of an interface?
- [ ] Could dependency injection handle this without abstraction?
- [ ] Is this trying to solve a problem we don't have?

**Action:** If simpler solution exists → Use it.

## Detection Patterns (Red Flags)

### Red Flag 1: Lonely Interface
```python
# ❌ Over-engineered: Interface with only one implementation
class DataProcessor(Protocol):
    def process(self, data: dict) -> dict: ...

class JsonDataProcessor:  # Only implementation
    def process(self, data: dict) -> dict:
        return transform_json(data)
```

**Why it's a red flag:** No actual polymorphism. The interface adds indirection without benefit.

**Better approach:**
```python
# ✅ Simple: Direct implementation
def process_json_data(data: dict) -> dict:
    return transform_json(data)
```

### Red Flag 2: Wrapper with No Value
```python
# ❌ Over-engineered: Wrapper that just forwards calls
class DatabaseWrapper:
    def __init__(self, db: Database):
        self._db = db

    def query(self, sql: str) -> list:
        return self._db.query(sql)  # Just forwarding
```

**Why it's a red flag:** No transformation, validation, or added behavior. Pure indirection.

**Better approach:** Use the database directly or add actual value (caching, retry, validation).

### Red Flag 3: Layer for Layer's Sake
```python
# ❌ Over-engineered: Unnecessary service layer
class UserRepository:  # Already exists
    def get_user(self, id: int) -> User: ...

class UserService:  # Adds nothing
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user(self, id: int) -> User:
        return self.repo.get_user(id)  # Just forwarding
```

**Why it's a red flag:** Service layer adds no business logic, validation, or orchestration.

**Better approach:** Use repository directly until business logic is needed.

### Red Flag 4: Pattern for Pattern's Sake
```python
# ❌ Over-engineered: Factory for single type
class UserFactory:
    @staticmethod
    def create_user(name: str, email: str) -> User:
        return User(name=name, email=email)
```

**Why it's a red flag:** Factory pattern used without variation or complexity justification.

**Better approach:**
```python
# ✅ Simple: Direct construction
user = User(name="Alice", email="alice@example.com")
```

### Red Flag 5: Premature Generalization
```python
# ❌ Over-engineered: Generic solution for specific problem
class ConfigLoader(Generic[T]):
    def load(self, source: str, parser: Parser[T]) -> T: ...

class JsonParser(Parser[dict]): ...
class YamlParser(Parser[dict]): ...
```

**Why it's a red flag:** Generic abstraction built before knowing actual requirements.

**Better approach:** Start with simple JSON config loader. Generalize when second format is needed.

## Examples: Good vs Over-Engineered

### Example 1: Repository Pattern

**Over-Engineered:**
```python
# Unnecessary: Abstract repository + generic base + implementation
class Repository(Protocol, Generic[T]):
    def get(self, id: int) -> T: ...
    def save(self, entity: T) -> None: ...

class BaseRepository(Generic[T]):  # Generic base
    def validate(self, entity: T) -> bool: ...

class UserRepository(BaseRepository[User]):  # Concrete
    def get(self, id: int) -> User: ...
    def save(self, user: User) -> None: ...
```

**Right-Sized:**
```python
# Clean Architecture: Protocol in domain, implementation in infrastructure
# domain/repositories.py
class UserRepository(Protocol):  # Interface for dependency inversion
    def get_user(self, id: int) -> User: ...
    def save_user(self, user: User) -> None: ...

# infrastructure/repositories.py
class SqlUserRepository:  # Concrete implementation
    def get_user(self, id: int) -> User: ...
    def save_user(self, user: User) -> None: ...
```

### Example 2: Service Layer

**Over-Engineered:**
```python
# Unnecessary: Service that just forwards to repository
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user(self, id: int) -> User:
        return self.repo.get_user(id)  # No business logic!
```

**Right-Sized:**
```python
# Use repository directly until business logic emerges
class AuthenticationHandler:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, email: str, password: str) -> Result[User, AuthError]:
        user = self.user_repo.get_user_by_email(email)
        if not user:
            return Err(AuthError.USER_NOT_FOUND)
        if not verify_password(password, user.password_hash):
            return Err(AuthError.INVALID_PASSWORD)
        return Ok(user)
```

### Example 3: Reusing Existing Abstractions

**Over-Engineered:**
```python
# Project already has Repository pattern
# Adding NEW abstraction for similar purpose:
class DataAccessLayer(Protocol):  # Duplicates Repository!
    def fetch(self, id: int) -> Entity: ...
    def persist(self, entity: Entity) -> None: ...
```

**Right-Sized:**
```python
# Use existing Repository pattern
class ProductRepository(Protocol):  # Follows project convention
    def get_product(self, id: int) -> Product: ...
    def save_product(self, product: Product) -> None: ...
```

## Integration with Architecture Validation

This skill complements existing architecture validation skills:

**Use with:**
- `architecture-validate-architecture` - Check layer boundaries while avoiding unnecessary layers
- `architecture-validate-layer-boundaries` - Ensure layers are necessary and well-justified
- `quality-code-review` - Evaluate abstractions during PR review

**Integration pattern:**
1. Run architecture validation to check existing patterns
2. Use minimal-abstractions to evaluate NEW abstractions
3. Ensure new code follows project patterns (don't reinvent)

## Expected Outcomes

### Successful Simplification

**Before:**
```
src/
├── domain/
│   ├── interfaces/user_repository.py
│   ├── interfaces/user_service.py
│   ├── interfaces/user_validator.py
├── application/
│   ├── services/user_service.py (forwards to repo)
│   ├── validators/user_validator.py (just calls validate())
├── infrastructure/
│   ├── repositories/user_repository.py
```

**After (applying minimal-abstractions):**
```
src/
├── domain/
│   ├── repositories.py (UserRepository protocol)
│   ├── models.py (User with validation)
├── application/
│   ├── handlers.py (CreateUserHandler with actual business logic)
├── infrastructure/
│   ├── repositories.py (SqlUserRepository)
```

**Metrics:**
- 40% fewer files
- 60% less indirection
- Same functionality
- Clearer execution paths

### Validation Output

```
Abstraction Evaluation: ProductService

✅ Checklist Results:
  ❌ Does abstraction already exist? YES - Repository pattern exists
  ❌ 2+ implementations? NO - Only one service planned
  ❌ Concrete requirement? NO - "We might need microservices later"
  ⚠️  Complexity cost: +3 files, +200 LOC, +2 layers indirection
  ✅ Simpler solution exists? YES - Use repository + handler directly

Recommendation: SKIP THIS ABSTRACTION
  - Use existing ProductRepository
  - Add business logic to ProductHandler
  - Wait for concrete multi-service requirement before abstracting
```

## Red Flags to Avoid

### Anti-Patterns
- ❌ "We might need it later" (YAGNI violation)
- ❌ Creating interfaces with only one implementation
- ❌ Wrappers that just forward calls without adding value
- ❌ Service layers that add no business logic
- ❌ Generic solutions for specific problems
- ❌ Design patterns used without understanding why
- ❌ Creating new abstractions when project patterns exist

### Good Practices
- ✅ Use existing project abstractions first
- ✅ Wait for 2+ concrete implementations before abstracting
- ✅ Justify every layer with concrete requirements
- ✅ Prefer simple, direct solutions
- ✅ Question every new abstraction
- ✅ Measure complexity cost vs benefit
- ✅ Remove abstractions when they're no longer needed

## Notes

**Key Principle:** Every abstraction must justify its existence with concrete, current requirements - not hypothetical future needs.

**Balance:** This skill advocates for minimal abstractions, but respects architectural patterns when they provide real value (e.g., Clean Architecture's dependency inversion).

**When in doubt:** Start simple. Add abstractions when pain points emerge, not before.
