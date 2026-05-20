---
name: coding-style
description: Coding style principles including immutability, guard clauses, and single responsibility. Use when writing, modifying, or refactoring source code. Do NOT use for documentation-only changes or config file edits.
durability: encoded-preference
---

# Coding Style

## Core Principles

- **KISS** (Keep It Simple) - Simplest solution that works
- **DRY** (Don't Repeat Yourself) - Extract common logic into functions
- **YAGNI** (You Aren't Gonna Need It) - Don't build features before needed
- **Boy Scout Rule** - Leave code better than you found it; refactor bad design in code you touch

### DRY Across Iteration Boundaries

DRY applies across ALL code in the project, including code committed in earlier User Stories or iterations. Previously-committed code with passing tests is not frozen -- it is a refactoring target when duplication is detected.

## Code Quality Checklist

Before marking work complete:
- [ ] Code is readable and well-named
- [ ] Functions are small (<50 lines)
- [ ] Files are focused (<800 lines)
- [ ] No deep nesting (>4 levels)
- [ ] Guard clauses used for early returns
- [ ] Single responsibility per function
- [ ] Data + functions preferred over classes
- [ ] Proper error handling
- [ ] No console.log statements
- [ ] No magic numbers (use named constants)
- [ ] No dummy/test data in production code (hardcoded values to pass tests, stub returns, placeholder strings)
- [ ] No mutation (immutable patterns used)
- [ ] No comments with arbitrary IDs (SR-001, CR-042, etc.)
- [ ] No WHAT comments remain (actively deleted, not just avoided)
- [ ] Remaining comments explain WHY (non-obvious reasoning only)

## Immutability (CRITICAL)

ALWAYS create new objects, NEVER mutate:

```javascript
// WRONG: Mutation
function updateUser(user, name) {
  user.name = name  // MUTATION!
  return user
}

// CORRECT: Immutability
function updateUser(user, name) {
  return {
    ...user,
    name
  }
}
```

## Data + Functions over Classes

Prefer simple data structures with pure functions over classes:

```python
# WRONG: Unnecessary class
class Order:
    def __init__(self, items):
        self.items = items
        self.discount = 0

    def set_discount(self, rate):
        self.discount = rate

    def calculate_total(self):
        subtotal = sum(item['price'] * item['qty'] for item in self.items)
        return subtotal * (1 - self.discount)

# CORRECT: Data structure + functions
@dataclass(frozen=True)
class Order:
    items: list[dict]
    discount: float = 0.0

def calculate_subtotal(order: Order) -> float:
    return sum(item['price'] * item['qty'] for item in order.items)

def calculate_total(order: Order) -> float:
    return calculate_subtotal(order) * (1 - order.discount)

def apply_discount(order: Order, rate: float) -> Order:
    return Order(items=order.items, discount=rate)
```

### When Classes ARE Justified

- Polymorphism is genuinely needed (multiple implementations of same interface)
- Framework requires it (Django models, React components)
- Complex state machine with invariants that must be enforced

### Prefer for Data

- Python: `dataclass(frozen=True)`, `NamedTuple`, `TypedDict`
- TypeScript: `interface`, `type`
- Go: `struct`

## Guard Clauses (Early Returns)

Convert nested conditionals to early returns:

```javascript
// WRONG: Deep nesting
function process(data) {
  if (data) {
    if (data.isValid) {
      if (data.items.length > 0) {
        return processItems(data.items);
      }
    }
  }
  return null;
}

// CORRECT: Guard clauses
function process(data) {
  if (!data) return null;
  if (!data.isValid) return null;
  if (data.items.length === 0) return null;

  return processItems(data.items);
}
```

## Single Responsibility

Each function should do one thing well:

```python
# WRONG: Multiple responsibilities
def process_and_save_user(data):
    # Validation, processing, saving, notification all in one
    ...

# CORRECT: Single responsibility
def validate_user_data(data): ...
def create_user_from_data(data): ...
def save_user(user): ...
def notify_user_creation(user): ...

def process_and_save_user(data):
    validate_user_data(data)
    user = create_user_from_data(data)
    save_user(user)
    notify_user_creation(user)
    return user
```

## Self-Documenting Code

Write code that doesn't need comments:

```python
# WRONG: Needs comments to understand
def calc(x, y, t):
    # Calculate compound interest
    # x is principal, y is rate, t is time
    return x * (1 + y) ** t

# CORRECT: Self-documenting
def calculate_compound_interest(principal, annual_rate, years):
    return principal * (1 + annual_rate) ** years
```

### Comment Anti-Patterns

**Forbidden: Arbitrary ID prefixes**
```python
# WRONG
# SR-001: Check if path exists
# CR-042: Handle edge case

# CORRECT: No IDs in code comments
# IDs belong in issue trackers, not code
```

**Forbidden: Comments explaining WHAT**
```python
# WRONG: Comment should be a function name
# Validate cwd is a valid directory
project_root = Path(cwd).resolve()

# CORRECT: Function name explains WHAT
project_root = resolve_project_root(cwd)
```

**WHAT Comment Detection Heuristics**

A comment is likely a WHAT comment if it:
- Starts with a verb: Check, Validate, Get, Set, Handle, Process, Create, Update, Delete, Parse, Convert, Calculate, Filter, Sort, Find, Initialize, Setup, Configure, Apply, Extract, Build
- Describes the immediate next line of code
- Could be replaced by a descriptive function name
- Provides no information beyond what the code shows

Examples of WHAT comments to DELETE:
```python
# Check if user is authenticated      <- DELETE (extract to is_authenticated())
# Parse the JSON response             <- DELETE (code shows json.loads())
# Loop through all items              <- DELETE (for item in items: is clear)
# Handle the error case               <- DELETE (except block is obvious)
# Initialize the counter              <- DELETE (counter = 0 is clear)
```

**Quick Test**: Cover the comment. Is the code still understandable? If yes, DELETE the comment.

**Mandatory Action: DELETE WHAT Comments**

WHEN you encounter or write a WHAT comment:
1. DELETE the comment immediately
2. Apply ONE of these alternatives:
   - Extract logic into a well-named function (preferred)
   - Use explaining variables for complex expressions
   - Use blank lines to separate logical blocks
   - If none apply, the code is already self-documenting

NEVER leave a WHAT comment "for now" or "for clarity" - this is the #1 source of comment debt.

**Alternatives to WHAT Comments**

| Instead of... | Use... |
|---------------|--------|
| `# Validate user input` + inline code | `validate_user_input(data)` function |
| `# Check if file exists` + if statement | `if file_exists(path):` or `if path.exists():` |
| `# Calculate the total price` + math | `total_price = calculate_total(items)` |
| `# Process each item` + for loop | Blank line before loop; loop is clear |
| `# Handle error case` + except block | Except block is self-documenting |

**Allowed: Comments explaining WHY**
```python
# Skip validation for admin users per SEC-2024 audit requirement
# Using setTimeout due to React 18 batching bug (fixed in 18.3)
# See RFC 7231 section 6.5.4 for 404 semantics
```

## Refactoring Patterns

Apply these patterns during TDD REFACTOR phase. See `references/refactoring-patterns.md` for detailed examples:

- **Extract Helper Functions** -- Break complex logic into well-named helpers
- **Explaining Variables & Constants** -- Replace magic values with named variables/constants
- **Chunk Statements** -- Group related code with blank lines
- **Normalize Symmetries** -- Make similar code look similar
- **Dead Code Removal** -- Remove unused functions, variables, imports, commented-out code
- **One Pile** -- Consolidate related code near its usage
- **Separation of Concerns** -- Separate business logic from presentation and I/O
- **Explicit Parameters** -- Make dependencies clear through function parameters

## Refactoring Safety Rules

1. **Maintain Functionality** - Never break existing behavior
2. **Small Steps** - Apply changes incrementally
3. **Test After Each Change** - Ensure tests pass after each refactoring
4. **Stage Large Changes** - Work in reviewable chunks
5. **Version Control** - Commit after each successful refactoring
6. **Preserve Tests** - Never delete tests without understanding their purpose
7. **Document Breaking Changes** - If API changes are necessary, document them

## File Organization

MANY SMALL FILES > FEW LARGE FILES:
- High cohesion, low coupling
- 200-400 lines typical, 800 max
- Extract utilities from large components
- Organize by feature/domain, not by type

## Error Handling

### Principle: Consistency Over Preference

Error handling paradigms vary by language and framework:

| Paradigm | Languages/Frameworks |
|----------|---------------------|
| try/catch (Exceptions) | JavaScript, Python, Java, C# |
| Result/Option types | Rust, Swift, Kotlin |
| Either monad | Haskell, Scala, fp-ts |
| Error return + defer | Go |
| Error return values | C |

**The worst anti-pattern is mixing paradigms in one project.**

### Rules

1. **Follow the project's existing convention** - Don't introduce a new paradigm
2. **Follow the language/framework idiom** - Go uses error returns + defer, Rust uses Result
3. **Be consistent** - If project uses try/catch, use try/catch everywhere
4. **Convert at boundaries** - When a library uses a different paradigm, wrap/convert errors at the integration point to match your project's style
5. **Handle errors at appropriate levels** - Don't catch and ignore

### Before Writing Error Handling, Check:
- What paradigm does this project already use?
- What is idiomatic for this language/framework?
- Does the library return errors differently? → Convert at boundary
- Am I maintaining consistency with existing code?

## Input Validation

ALWAYS validate user input:

```typescript
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150)
})

const validated = schema.parse(input)
```

## Logging (Server-Side)

ALWAYS use structured logging on server-side code:
- Use machine-parseable format (JSON, logfmt, etc.)
- Include: timestamp, level, message, requestId
- Never log sensitive data (passwords, tokens, PII) -- see security-patterns skill for attack vectors

