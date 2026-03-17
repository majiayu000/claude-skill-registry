---
name: sc-principles
description: Enforce KISS, Purity, SOLID, and Let It Crash principles through mandatory validation gates. Detects complexity violations, impure functions, design anti-patterns, and error handling issues.
---

# /sc:principles - Code Principles Validator

Mandatory validation skill enforcing four fundamental software engineering principles:

1. **KISS (Keep It Simple, Stupid)** - Code should be as simple as possible
2. **Functional Core, Imperative Shell** - Business logic must be pure; I/O belongs at edges
3. **SOLID** - Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
4. **Let It Crash** - Fail fast for bugs; handle errors explicitly at boundaries

## Quick Start

```bash
# Full validation (all four principles)
/sc:principles src/

# KISS only validation
/sc:principles src/ --kiss-only

# Purity only validation
/sc:principles src/ --purity-only

# SOLID only validation
/sc:principles src/ --solid-only

# Let It Crash only validation
/sc:principles src/ --crash-only

# Strict mode (warnings become errors)
/sc:principles src/ --strict

# Generate detailed report
/sc:principles src/ --report
```

## Behavioral Flow

```
1. INITIALIZE
   ├── Detect scope root
   ├── Find changed Python files (git diff)
   └── Determine file contexts (core vs shell)

2. ANALYZE
   ├── Parse AST for each file
   ├── Calculate complexity metrics (KISS)
   ├── Detect I/O patterns (Purity)
   ├── Check structural patterns (SOLID)
   └── Analyze error handling (Let It Crash)

3. VALIDATE
   ├── Compare against thresholds
   ├── Classify violations (error vs warning)
   └── Apply context rules (core stricter than shell)

4. REPORT/BLOCK
   ├── Output violations with locations
   ├── Generate actionable recommendations
   └── Exit 0 (pass) or 2 (blocked)
```

## Validation Rules

### KISS Gate

| Metric | Threshold | Severity | Description |
|--------|-----------|----------|-------------|
| Cyclomatic Complexity | > 10 | error | Number of independent paths through code |
| Cyclomatic Complexity | > 7 | warning | Early warning for growing complexity |
| Cognitive Complexity | > 15 | error | Weighted complexity (nested structures count more) |
| Function Length | > 50 lines | error | Lines of code per function (inclusive count) |
| Nesting Depth | > 4 levels | error | If/for/while/with/try nesting |
| Parameter Count | > 5 | warning | Function parameters |

**Cognitive vs Cyclomatic Complexity:**
- Cyclomatic counts decision points (branches)
- Cognitive weights nested structures more heavily: `1 + nesting_depth` per control structure
- Example: `if (if (if ...))` has low cyclomatic but high cognitive (hard to read)

### Purity Gate

The "Functional Core, Imperative Shell" pattern:

| Layer | Path Patterns | I/O Allowed | Severity |
|-------|---------------|-------------|----------|
| Core | `*/domain/*`, `*/logic/*`, `*/services/*`, `*/utils/*`, `*/core/*` | NO | error |
| Shell | `*/handlers/*`, `*/adapters/*`, `*/api/*`, `*/cli/*`, `*/scripts/*`, `*/tests/*` | YES | warning |

**Note:** Files in `*/archive/*`, `*/examples/*`, `*/benchmarks/*`, `conftest.py`, `setup.py`, and `*__main__.py` are treated as shell (I/O allowed).

**Detected I/O Patterns:**

| Category | Examples |
|----------|----------|
| File I/O | `open()`, `read()`, `write()`, `Path.read_text()` |
| Network | `requests.get()`, `httpx`, `urllib`, `socket` |
| Database | `execute()`, `query()`, `session.add()`, `cursor` |
| Subprocess | `subprocess.run()`, `os.system()`, `Popen` |
| Global State | `global`, `nonlocal` keywords |
| Side Effects | `print()`, `logging.*`, `logger.*` |
| Async I/O | `async def`, `await`, `async for`, `async with` |

### SOLID Gate

Detects structural violations of SOLID design principles.

| Principle | Detection | Severity | Description |
|-----------|-----------|----------|-------------|
| SRP | File >300 lines, class with >5 public methods | warning | Single Responsibility - one reason to change |
| OCP | `if/elif` chains on type, `isinstance` cascades | warning | Open-Closed - extend, don't modify |
| LSP | Override that raises `NotImplementedError` | error | Liskov Substitution - honor contracts |
| ISP | Interface/protocol with >7 methods | warning | Interface Segregation - small interfaces |
| DIP | Direct instantiation in business logic | warning | Dependency Inversion - depend on abstractions |

**Code Smells to Flag:**

| Smell | Principle | Recommended Fix |
|-------|-----------|-----------------|
| File >300 lines | SRP | Extract responsibilities into modules |
| if/else type chains | OCP | Strategy pattern or registry |
| Override that throws | LSP | Honor base contract or don't inherit |
| 10+ method interface | ISP | Split into focused interfaces |
| `new Service()` in logic | DIP | Dependency injection |

### Let It Crash Gate

Detects anti-patterns in error handling based on the "Let It Crash" philosophy.

| Pattern | Severity | Description |
|---------|----------|-------------|
| Bare `except:` | error | Catches all exceptions including KeyboardInterrupt |
| `except Exception:` (no re-raise) | warning | Swallows errors without handling |
| `except: pass` | error | Silent failure, debugging nightmare |
| Defensive `if not x: return` chains | warning | Masks root cause of bugs |
| Nested try/except fallbacks | warning | Complex error paths, hard to debug |

**When to Let It Crash:**
- Validation failures → crash with clear error
- Programming errors → surface immediately
- Internal operations → let them fail

**When to Handle Errors (exceptions to rule):**
- Data persistence → protect against data loss
- External APIs → retry, fallback, graceful degradation
- Resource cleanup → RAII, finally blocks
- User-facing operations → graceful error messages

**Not Flagged (appropriate handling):**
- Error handling in `*/adapters/*`, `*/api/*`, `*/cli/*` paths
- Explicit logging before swallowing
- Re-raise after logging

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--kiss-only` | bool | false | Run only KISS validation |
| `--purity-only` | bool | false | Run only purity validation |
| `--solid-only` | bool | false | Run only SOLID validation |
| `--crash-only` | bool | false | Run only Let It Crash validation |
| `--no-kiss` | bool | false | Skip KISS validation |
| `--no-purity` | bool | false | Skip purity validation |
| `--no-solid` | bool | false | Skip SOLID validation |
| `--no-crash` | bool | false | Skip Let It Crash validation |
| `--threshold` | int | 10 | Max cyclomatic complexity |
| `--max-cognitive` | int | 15 | Max cognitive complexity |
| `--max-lines` | int | 50 | Max function line count |
| `--max-depth` | int | 4 | Max nesting depth |
| `--max-params` | int | 5 | Max parameter count |
| `--max-file-lines` | int | 300 | Max file line count (SRP) |
| `--max-interface-methods` | int | 7 | Max interface methods (ISP) |
| `--strict` | bool | false | Treat all warnings as errors |
| `--core-only` | bool | false | Only validate core layer files |
| `--all` | bool | false | Analyze all files, not just changed |
| `--report` | bool | false | Generate detailed JSON report |

## Integration Flags

For use by other skills and pre-commit hooks:

| Flag | Description |
|------|-------------|
| `--pre-commit` | Run as pre-commit hook (blocks commit on failure) |
| `--inline` | Real-time validation during implementation |
| `--json` | Output JSON format for programmatic use |

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Validation passed | Proceed |
| 2 | Violations detected | Blocked - refactor required |
| 3 | Validation error | Manual intervention needed |

## Personas Activated

- **code-warden** - Primary reviewer for principles enforcement
- **refactoring-expert** - For complex refactoring guidance
- **quality-engineer** - For metrics integration

## Validator Scripts

Located in `scripts/` directory:

### validate_kiss.py

```bash
python .claude/skills/sc-principles/scripts/validate_kiss.py \
  --scope-root . \
  --threshold 10 \
  --max-lines 50 \
  --json
```

### validate_purity.py

```bash
python .claude/skills/sc-principles/scripts/validate_purity.py \
  --scope-root . \
  --core-only \
  --json
```

## Pre-commit Integration

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: kiss-check
        name: KISS Validation
        entry: python .claude/skills/sc-principles/scripts/validate_kiss.py --scope-root . --json
        language: python
        types: [python]
        pass_filenames: false

      - id: purity-check
        name: Purity Validation
        entry: python .claude/skills/sc-principles/scripts/validate_purity.py --scope-root . --json
        language: python
        types: [python]
        pass_filenames: false
```

## Refactoring Guidance

When violations are detected, apply these patterns:

### For Complexity Violations

1. **Extract Method** - Split large functions into smaller, named pieces
2. **Guard Clauses** - Replace nested if/else with early returns
3. **Strategy Pattern** - Replace complex switch/if-else with polymorphism
4. **Decompose Conditional** - Name complex conditions as explaining variables

**Before:**
```python
def process(data, config, user):
    if data:
        if config.enabled:
            if user.has_permission:
                for item in data:
                    if item.valid:
                        # deep logic here
```

**After:**
```python
def process(data, config, user):
    if not can_process(data, config, user):
        return None
    return process_items(data)

def can_process(data, config, user):
    return data and config.enabled and user.has_permission

def process_items(data):
    return [process_item(item) for item in data if item.valid]
```

### For Purity Violations

1. **Dependency Injection** - Pass dependencies as arguments
2. **Repository Pattern** - Isolate database operations
3. **Adapter Pattern** - Wrap external APIs
4. **Return Don't Print** - Return values, let callers handle output

**Before:**
```python
# In domain/calculator.py (CORE - should be pure)
def calculate_discount(user_id):
    user = db.query(User).get(user_id)  # I/O in core!
    print(f"Calculating for {user.name}")  # Side effect!
    return 0.2 if user.is_premium else 0.1
```

**After:**
```python
# In domain/calculator.py (CORE - now pure)
def calculate_discount(user: User) -> float:
    """Pure function - no I/O, just logic."""
    return 0.2 if user.is_premium else 0.1

# In adapters/discount_service.py (SHELL - I/O allowed)
def get_user_discount(user_id: int) -> float:
    user = user_repository.get(user_id)
    discount = calculate_discount(user)
    logger.info(f"Discount for {user.name}: {discount}")
    return discount
```

### For SOLID Violations

1. **SRP (Single Responsibility)** - Extract into modules
2. **OCP (Open-Closed)** - Use strategy pattern or registry
3. **LSP (Liskov Substitution)** - Honor base contracts
4. **ISP (Interface Segregation)** - Split fat interfaces
5. **DIP (Dependency Inversion)** - Inject dependencies

**Before (OCP violation):**
```python
def process_payment(payment_type, amount):
    if payment_type == "credit":
        return process_credit(amount)
    elif payment_type == "debit":
        return process_debit(amount)
    elif payment_type == "crypto":  # New type = code change!
        return process_crypto(amount)
```

**After (OCP compliant):**
```python
PROCESSORS = {
    "credit": process_credit,
    "debit": process_debit,
    "crypto": process_crypto,  # Add here, no function change
}

def process_payment(payment_type, amount):
    processor = PROCESSORS.get(payment_type)
    if not processor:
        raise ValueError(f"Unknown payment type: {payment_type}")
    return processor(amount)
```

### For Let It Crash Violations

1. **Remove catch-all blocks** - Let bugs surface
2. **Remove defensive guards** - Validate at boundaries instead
3. **Flatten try/except** - Handle at edges, not everywhere

**Before (catch-all anti-pattern):**
```python
def get_user(user_id):
    try:
        user = db.query(User).get(user_id)
        return user
    except:  # BAD: catches everything, hides bugs
        return None
```

**After (let it crash):**
```python
def get_user(user_id):
    # Let database errors surface - they indicate real problems
    return db.query(User).get(user_id)

# Handle at the boundary (API layer)
@app.get("/users/{user_id}")
def api_get_user(user_id: int):
    try:
        return get_user(user_id)
    except DBError as e:
        logger.error("Database error", error=e, user_id=user_id)
        raise HTTPException(500, "Database unavailable")
```

## Examples

### Example 1: Full Validation

```bash
$ /sc:principles src/ --report

KISS Validation: BLOCKED
Files analyzed: 12
Errors: 3, Warnings: 5

Violations:
  [ERROR] src/services/order.py:45 process_order: complexity = 15 (max: 10)
  [ERROR] src/utils/parser.py:12 parse_data: length = 78 (max: 50)
  [WARNING] src/domain/calc.py:8 calculate: parameters = 7 (max: 5)

Purity Validation: BLOCKED
Core violations: 2, Shell warnings: 1

Violations:
  [ERROR] src/domain/user.py:23 get_status: database - db.query (context: core)
  [ERROR] src/services/report.py:56 generate: file_io - open (context: core)

Recommendations:
  - COMPLEXITY: Extract helper functions, use early returns
  - DATABASE: Use repository pattern. Business logic receives data, not queries
  - FILE I/O: Move file operations to adapter layer
```

### Example 2: KISS Only

```bash
$ /sc:principles src/ --kiss-only --threshold 8

KISS Validation: PASSED
Files analyzed: 12
Errors: 0, Warnings: 2
```

### Example 3: Strict Mode

```bash
$ /sc:principles src/ --strict

# All warnings become errors
# Any warning will block
```

## Quality Integration

This skill integrates with SuperClaude quality gates:

- Contributes to `simplicity` dimension (weight: 0.08)
- Contributes to `purity` dimension (weight: 0.02)
- Triggers `simplification` strategy when simplicity < 70
- Triggers `purification` strategy when purity < 70

## Related Skills

- `/sc:improve --type principles` - Auto-refactor for principles compliance
- `/sc:implement` - Includes principles validation by default
- `/sc:analyze` - Code analysis includes principles metrics

---

## Test Coverage

The validators have comprehensive test coverage (27 tests):

**Purity Validator Tests:**
- Async function detection (`async def`)
- Await expression detection
- Async for loop detection
- Async with context manager detection
- Shell vs core severity differentiation
- Edge cases (syntax errors, unicode, empty files)

**KISS Validator Tests:**
- Function length (inclusive count)
- Cyclomatic complexity
- Cognitive complexity
- Nesting depth
- Parameter count
- Edge cases (syntax errors, unicode, empty files)

Run tests:
```bash
python -m pytest .claude/skills/sc-principles/tests/ -v
```

---

**Version**: 2.0.0
**Validators**: `validate_kiss.py`, `validate_purity.py`, `validate_solid.py` (heuristic), `validate_crash.py` (heuristic)
**Agent**: `code-warden`
**Traits**: `solid-aligned`, `crash-resilient`
**Tests**: 27 passing (KISS + Purity)
