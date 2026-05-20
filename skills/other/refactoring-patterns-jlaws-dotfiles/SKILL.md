---
name: refactoring-patterns
description: "Use when systematically refactoring code. Provides a catalog of safe refactoring operations, test-verify-commit cadence, and strategies for large-scale refactors including strangler fig and branch-by-abstraction."
---

# Refactoring Patterns

## The Discipline

```
TEST → REFACTOR → VERIFY → COMMIT
Never skip a step. Never combine refactoring with behavior changes.
```

A refactoring changes structure without changing behavior. If you're adding features or fixing bugs at the same time, you're not refactoring -- you're gambling.

## The Cadence

1. **Ensure tests pass** (run full suite, green baseline)
2. **Make ONE structural change** (single refactoring operation)
3. **Run tests again** (must still pass -- if not, revert immediately)
4. **Commit** (small atomic commit, message describes the refactoring)
5. **Repeat**

Each commit is a safe rollback point. If anything breaks, `git revert` is trivial.

## Refactoring Catalog

### Extract Function / Method

**When**: Code block needs a comment to explain intent, or is duplicated.

```python
# Before
def process_order(order):
    # Calculate discount
    if order.customer.is_premium and order.total > 100:
        discount = order.total * 0.15
    elif order.total > 200:
        discount = order.total * 0.10
    else:
        discount = 0
    order.total -= discount
    # ... more processing

# After
def calculate_discount(order):
    if order.customer.is_premium and order.total > 100:
        return order.total * 0.15
    if order.total > 200:
        return order.total * 0.10
    return 0

def process_order(order):
    order.total -= calculate_discount(order)
    # ... more processing
```

### Extract Class / Module

**When**: A class has multiple responsibilities or a module is >300 lines with distinct sections.

Split by responsibility. Each resulting unit should have a single reason to change.

### Inline Function / Variable

**When**: Indirection adds no clarity. The function body is as clear as the name.

```typescript
// Before
function isEligible(age: number): boolean {
    return age >= 18;
}
const eligible = isEligible(user.age);

// After (if only used once and meaning is obvious)
const eligible = user.age >= 18;
```

### Rename

**When**: Name doesn't communicate intent. Most impactful, least risky refactoring.

Use IDE rename (F2 in VS Code) for safety. Manual rename risks missing references.

### Replace Conditional with Polymorphism

**When**: Switch/if-else chain on a type field that appears in multiple places.

```typescript
// Before
function getArea(shape: Shape): number {
    switch (shape.type) {
        case 'circle': return Math.PI * shape.radius ** 2;
        case 'rectangle': return shape.width * shape.height;
        case 'triangle': return 0.5 * shape.base * shape.height;
    }
}

// After
interface Shape {
    getArea(): number;
}
class Circle implements Shape {
    getArea() { return Math.PI * this.radius ** 2; }
}
class Rectangle implements Shape {
    getArea() { return this.width * this.height; }
}
```

**Caution**: Only worth it if the switch appears in 3+ places. One switch is fine.

### Replace Inheritance with Composition

**When**: Subclass only uses a fraction of parent, or "is-a" relationship is forced.

```python
# Before
class AudioPlayer(MediaWidget):  # inherits 50 methods, uses 5
    pass

# After
class AudioPlayer:
    def __init__(self):
        self.media = MediaWidget()  # delegate what you need
```

### Introduce Parameter Object

**When**: 3+ parameters travel together across multiple functions.

```go
// Before
func createUser(name string, email string, age int, role string, dept string) {}

// After
type CreateUserParams struct {
    Name  string
    Email string
    Age   int
    Role  string
    Dept  string
}
func createUser(params CreateUserParams) {}
```

### Pull Up / Push Down Method

**When**: Method exists in some subclasses but belongs in parent (pull up), or exists in parent but only used by one subclass (push down).

Pull up when multiple subclasses share identical implementation. Push down when only one subclass needs it.

### Replace Magic Values with Constants

```python
# Before
if response.status_code == 429:
    time.sleep(60)

# After
RATE_LIMIT_STATUS = 429
RATE_LIMIT_COOLDOWN_SECONDS = 60
if response.status_code == RATE_LIMIT_STATUS:
    time.sleep(RATE_LIMIT_COOLDOWN_SECONDS)
```

## Code Smell to Refactoring Mapping

| Code Smell | Refactoring(s) |
|------------|-----------------|
| Long method (>30 lines) | Extract function |
| Long parameter list (>3) | Introduce parameter object |
| Duplicated code | Extract function / Extract base class |
| Feature envy (method uses another class's data more than its own) | Move method |
| Data clumps (same fields grouped repeatedly) | Extract class / Introduce parameter object |
| Switch statements (on type, in multiple places) | Replace conditional with polymorphism |
| Divergent change (one class changed for multiple reasons) | Extract class (split by responsibility) |
| Shotgun surgery (one change touches many files) | Move method / Inline class (consolidate) |
| Primitive obsession (strings/ints for domain concepts) | Introduce value object |
| Speculative generality (unused abstractions) | Inline class / Remove dead code |
| Dead code | Delete it. Git has history. |

## Large-Scale Refactoring Strategies

### Strangler Fig

Gradually replace a legacy system by routing new functionality to a new implementation while keeping the old one running.

```
1. Identify the boundary (API, module interface, route)
2. Build new implementation behind the same interface
3. Route traffic/calls incrementally (feature flag, proxy, or router)
4. Monitor both paths (correctness + performance)
5. Remove old implementation when 100% migrated
```

**Best for**: Replacing entire subsystems, migrating frameworks, rewriting services.

### Branch by Abstraction

Introduce an abstraction layer to swap implementations without long-lived feature branches.

```
1. Create an interface/protocol that wraps the current implementation
2. Update all callers to use the abstraction (test + commit)
3. Build new implementation behind the same abstraction
4. Switch (toggle, config, or just swap) to new implementation
5. Remove old implementation and (optionally) the abstraction
```

**Best for**: Replacing libraries, changing data stores, swapping algorithms.

### Parallel Implementation

Run old and new code simultaneously, compare outputs, converge when confident.

```python
def process(data):
    old_result = old_implementation(data)
    new_result = new_implementation(data)
    if old_result != new_result:
        log.warning(f"Mismatch: {old_result} vs {new_result}")
    return old_result  # switch to new_result when confident
```

**Best for**: High-risk logic changes where correctness is critical (payment processing, data pipelines).

## Safe Refactoring Sequences

Order matters. Some refactorings enable others.

| Goal | Sequence |
|------|----------|
| Break up god class | 1. Extract methods → 2. Group related methods → 3. Extract classes → 4. Define interfaces |
| Remove inheritance | 1. Push down unused methods → 2. Extract interface → 3. Replace inheritance with delegation → 4. Remove base class |
| Simplify complex conditional | 1. Extract each branch into named function → 2. Replace with lookup map or polymorphism |
| Migrate to new API | 1. Introduce adapter → 2. Route calls through adapter → 3. Swap adapter implementation → 4. Inline adapter if trivial |

## IDE-Assisted vs Manual Refactoring

| Refactoring | IDE-Assisted? | Notes |
|-------------|:---:|-------|
| Rename | Yes | Always use IDE -- catches all references |
| Extract function | Yes | IDE infers parameters and return type |
| Move file/module | Yes | Updates import paths automatically |
| Inline variable | Yes | Safe with IDE; manual risks missing usages |
| Change signature | Yes | IDE updates all call sites |
| Replace conditional with polymorphism | No | Requires architectural judgment |
| Introduce abstraction layer | No | Requires design decisions |
| Strangler fig / Branch by abstraction | No | Strategy, not mechanical transformation |

**Rule**: If your IDE can do it, let your IDE do it. Manual refactoring of renames and moves is error-prone.

## When NOT to Refactor

| Situation | Why Not |
|-----------|---------|
| No tests covering the code | You can't verify behavior preservation. Write tests first. |
| Under deadline pressure | Refactoring is investment, not firefighting. Ship first, refactor next sprint. |
| Code is being deleted soon | Don't polish what you're throwing away. |
| "While I'm in here..." | Resist scope creep for large refactors -- file a ticket, do it separately. **Exception**: small, proportional nearby improvements (boy scout rule) are encouraged -- rename a confusing variable, fix a broken docstring, extract an obvious helper. The distinction is proportionality. See `workflow:technical-debt-remediation` Boy Scout Rule. |
| Single ugly function that works | Ugly but correct and isolated code is fine. Refactor when you need to change it. |
| Premature -- only one implementation | Don't create abstractions for a single concrete case. Wait for the second. |

## Gotchas

- Refactoring without tests is walking a tightrope without a net. If coverage is low, write characterization tests first (tests that capture current behavior, even if "wrong")
- "Refactoring" that changes behavior is not refactoring -- it's rewriting. Separate the two activities into distinct commits
- Large PRs labeled "refactoring" are suspicious. Each refactoring step should be its own commit; the PR can be large but each commit must be atomic and green
- Rename refactoring across module boundaries can break dynamic references (string-based imports, reflection, serialized class names)
- Extract function can accidentally change evaluation order or introduce performance overhead in hot paths -- verify with benchmarks if relevant
- Strangler fig requires maintaining two implementations simultaneously; budget for the maintenance cost
- Branch by abstraction's "temporary" interface layer has a tendency to become permanent; set a deadline for removal

## Cross-References

- **workflow:code-quality** -- code smells, style conventions, refactoring decision framework
- **workflow:technical-debt-remediation** -- prioritizing and scheduling refactoring work
- **workflow:verification-before-completion** -- ensuring refactoring is verified before claiming done
