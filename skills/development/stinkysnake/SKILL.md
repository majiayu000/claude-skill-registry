---
name: stinkysnake
description: Progressive Python quality improvement with static analysis, type refinement, modernization planning, plan review, and test-driven implementation. Use when addressing technical debt, eliminating Any types, applying modern Python patterns, or refactoring for better design.
user-invocable: true
argument-hint: "[file-paths-or-module]"
---

# Python Quality Improvement System

Systematic Python code quality improvement through static analysis, type refinement, modernization planning with review, and test-driven implementation.

## Arguments

$ARGUMENTS

## Workflow Overview

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STINKYSNAKE WORKFLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Phase 1: STATIC ANALYSIS                                                   │
│  ├── Run formatters (ruff format)                                           │
│  ├── Run linters (ruff check --fix)                                         │
│  ├── Run type checkers (mypy, pyright)                                      │
│  └── Auto-fix all resolvable issues                                         │
│           │                                                                 │
│           ▼                                                                 │
│  Phase 2: TYPE ANALYSIS                                                     │
│  ├── Determine minimum Python version                                       │
│  ├── Inventory all `Any` types                                              │
│  ├── Map type dependencies                                                  │
│  └── Identify typing gaps                                                   │
│           │                                                                 │
│           ▼                                                                 │
│  Phase 3: MODERNIZATION PLANNING                                            │
│  ├── Plan Protocol usage for duck typing                                    │
│  ├── Plan Generic type parameters                                           │
│  ├── Plan TypeGuard narrowing                                               │
│  ├── Plan TypeAlias definitions                                             │
│  ├── Plan TypedDict for dict shapes                                         │
│  ├── Plan dataclass/Pydantic models                                         │
│  └── Plan library modernization (httpx, orjson, etc.)                       │
│           │                                                                 │
│           ▼                                                                 │
│  Phase 4: PLAN REVIEW (context: fork)                                       │
│  ├── Review against pythonic best practices                                 │
│  ├── Verify against online references                                       │
│  ├── Check feasibility                                                      │
│  ├── Identify breaking changes                                              │
│  └── Produce review report                                                  │
│           │                                                                 │
│           ▼                                                                 │
│  Phase 5: PLAN REFINEMENT                                                   │
│  └── Update plan based on review feedback                                   │
│           │                                                                 │
│           ▼                                                                 │
│  Phase 6: DOCUMENTATION DISCOVERY                                           │
│  ├── Find docs requiring updates                                            │
│  └── Note what changes are needed                                           │
│           │                                                                 │
│           ▼                                                                 │
│  Phase 7: INTERFACE DESIGN                                                  │
│  └── Create interfaces/protocols first                                      │
│           │                                                                 │
│           ▼                                                                 │
│  Phase 8: TEST-FIRST (context: fork, python-pytest-architect)               │
│  ├── Write failing tests against interfaces                                 │
│  └── Stop after tests written                                               │
│           │                                                                 │
│           ▼                                                                 │
│  Phase 9: IMPLEMENTATION (/snakepolish)                                     │
│  ├── context: fork with python-cli-architect                                │
│  ├── Follow plans and implement functions                                   │
│  └── Run tests until passing                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Companion Plugins

This skill integrates with plugins in the same marketplace:

### holistic-linting Plugin

**Activation**: `Skill(command: "holistic-linting")`

Provides: Linting rules knowledge base, `linting-root-cause-resolver` agent, automatic linter detection.

### pre-commit Plugin

**Activation**: `Skill(command: "pre-commit")`

Provides: Git hook automation for quality gates.

---

## Phase 1: Static Analysis

Run automated tools to fix all resolvable issues before manual work begins.

### Step 1.1: Format Code

```bash
# Format all Python files
uv run ruff format $ARGUMENTS

# Verify formatting
uv run ruff format --check $ARGUMENTS
```

### Step 1.2: Auto-Fix Linting Issues

```bash
# Fix all auto-fixable issues
uv run ruff check --fix $ARGUMENTS

# Fix unsafe fixes if appropriate
uv run ruff check --fix --unsafe-fixes $ARGUMENTS
```

### Step 1.3: Run Type Checkers

```bash
# Run mypy
uv run mypy $ARGUMENTS

# Run pyright if configured
uv run pyright $ARGUMENTS
```

### Step 1.4: Document Remaining Issues

Create inventory of issues that cannot be auto-fixed:

```text
## Static Analysis Results

### Auto-Fixed
- [X] Formatting issues: N fixed
- [X] Import sorting: N fixed
- [X] Safe linting fixes: N fixed

### Requires Manual Resolution
| File:Line | Rule | Issue | Complexity |
|-----------|------|-------|------------|
| src/api.py:45 | ANN001 | Missing type annotation | Low |
| src/models.py:120 | B006 | Mutable default | Medium |
```

---

## Phase 2: Type Analysis

Determine Python compatibility and inventory typing gaps.

### Step 2.1: Determine Minimum Python Version

Check project configuration:

```bash
# Check pyproject.toml
grep -E "requires-python|python_requires" pyproject.toml

# Check setup.py if exists
grep -E "python_requires" setup.py
```

**Document the constraint**:

```text
## Python Version Constraint

Minimum Version: Python 3.11
Reason: [from pyproject.toml requires-python = ">=3.11"]

Available Language Features:
- Native generics (list[str], dict[str, int])
- Union syntax (str | None)
- Pattern matching (match/case)
- Exception groups
- Self type
- TypeVarTuple
- Required/NotRequired in TypedDict
```

### Step 2.2: Inventory All `Any` Types

Search for explicit and implicit `Any` usage:

```bash
# Find explicit Any imports and usage
uv run rg "from typing import.*Any|: Any|-> Any" $ARGUMENTS

# Run mypy with strict mode to find implicit Any
uv run mypy --strict $ARGUMENTS 2>&1 | grep -E "has type.*Any|Implicit.*Any"
```

**Create inventory**:

```text
## Any Type Inventory

### Explicit Any Usage
| Location | Variable | Current Type | Proposed Type |
|----------|----------|--------------|---------------|
| api.py:23 | response | Any | dict[str, JSONValue] |
| utils.py:45 | callback | Any | Callable[[str], None] |

### Implicit Any (from untyped libraries)
| Location | Source | Mitigation |
|----------|--------|------------|
| client.py:12 | third_party.get() | Add type stub or cast |
```

### Step 2.3: Map Type Dependencies

Understand how types flow through the codebase:

```text
## Type Dependency Map

Entry Points (public API):
- cli.main() -> int
- api.fetch_data(url: str) -> ???  # Needs typing

Internal Flow:
fetch_data() -> parse_response() -> validate() -> Model

Type Gaps:
- parse_response returns Any
- validate accepts Any
```

---

## Phase 3: Modernization Planning

Plan how to apply modern Python features to eliminate type gaps and improve design.

### Step 3.1: Load modernpython Skill

```text
Skill(command: "modernpython")
```

### Step 3.2: Plan Type System Improvements

For each `Any` in the inventory, plan the replacement using appropriate constructs:

#### Protocol (Structural Subtyping)

Use when: Multiple unrelated classes share behavior but not inheritance.

```python
# Before: Any for duck-typed objects
def process(handler: Any) -> None:
    handler.handle(data)

# After: Protocol defines required interface
class Handler(Protocol):
    def handle(self, data: bytes) -> None: ...

def process(handler: Handler) -> None:
    handler.handle(data)
```

#### Generic (Parameterized Types)

Use when: Container or function works with multiple types while preserving type info.

```python
# Before: Any loses type information
def first(items: list[Any]) -> Any:
    return items[0]

# After: Generic preserves type
T = TypeVar("T")
def first(items: list[T]) -> T:
    return items[0]
```

#### TypeGuard (Type Narrowing)

Use when: Runtime check should narrow type for type checker.

```python
# Before: Type checker doesn't understand the check
def process(data: str | dict[str, Any]) -> None:
    if isinstance(data, dict):
        # data still str | dict here without TypeGuard

# After: TypeGuard narrows the type
def is_dict_response(data: str | dict[str, Any]) -> TypeGuard[dict[str, Any]]:
    return isinstance(data, dict)

def process(data: str | dict[str, Any]) -> None:
    if is_dict_response(data):
        # data is dict[str, Any] here
```

#### TypeAlias (Named Types)

Use when: Complex type is repeated or needs documentation.

```python
# Before: Repeated complex type
def fetch(url: str) -> dict[str, str | int | list[str] | None]: ...
def parse(data: dict[str, str | int | list[str] | None]) -> Model: ...

# After: Named alias
JSONValue: TypeAlias = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
APIResponse: TypeAlias = dict[str, JSONValue]

def fetch(url: str) -> APIResponse: ...
def parse(data: APIResponse) -> Model: ...
```

#### TypedDict (Dict Shape)

Use when: Dict has known keys with specific types.

```python
# Before: dict[str, Any]
def get_user() -> dict[str, Any]:
    return {"name": "Alice", "age": 30, "active": True}

# After: TypedDict defines shape
class User(TypedDict):
    name: str
    age: int
    active: bool

def get_user() -> User:
    return {"name": "Alice", "age": 30, "active": True}
```

#### Dataclass / Pydantic

Use when: Need structured data with validation.

```python
# Before: Plain dict or untyped class
user = {"name": "Alice", "email": "alice@example.com"}

# After: Dataclass for internal data
@dataclass
class User:
    name: str
    email: str

# After: Pydantic for external/validated data
class UserInput(BaseModel):
    name: str
    email: EmailStr
```

### Step 3.3: Plan Library Modernization

| Legacy     | Modern    | Benefit                           |
| ---------- | --------- | --------------------------------- |
| `requests` | `httpx`   | Async support, HTTP/2, type hints |
| `json`     | `orjson`  | 10x faster, better types          |
| `toml`     | `tomlkit` | Preserves formatting, comments    |
| `argparse` | `typer`   | Type-driven CLI, auto-help        |
| `print()`  | `rich`    | Formatted output, progress bars   |
| `curses`   | `textual` | Modern TUI framework              |

### Step 3.4: Create Modernization Plan Document

```text
## Modernization Plan

### Type System Changes

1. **Eliminate Any in api.py**
   - Line 23: response: Any → response: APIResponse (TypeAlias)
   - Line 45: callback: Any → callback: Callable[[Event], None]
   - Line 67: data: Any → data: UserData (TypedDict)

2. **Add Protocols for duck typing**
   - Create Handler protocol for plugin system
   - Create Serializable protocol for export functions

3. **Add Generics for containers**
   - Cache[T] generic class
   - Result[T, E] for error handling

### Library Migrations

1. **requests → httpx**
   - Files affected: api.py, client.py
   - Breaking changes: Session → Client, response.json() typing
   - Async opportunity: Yes

2. **json → orjson**
   - Files affected: serialization.py
   - Breaking changes: orjson.dumps returns bytes
   - Performance gain: ~10x

### Estimated Impact
- Files to modify: 12
- New type definitions: 8
- Breaking changes: 3 (internal only)
```

---

## Phase 4: Plan Review

Delegate to a review agent with context fork to critique the plan.

### Step 4.1: Launch Plan Review Agent

```text
Task(
  agent="python-code-reviewer",
  prompt="Review the modernization plan at .claude/plans/stinkysnake-plan.md

REVIEW CRITERIA:

1. **Pythonic Best Practices**
   - Are the proposed patterns idiomatic Python?
   - Do they follow PEP guidelines?
   - Are simpler solutions available?

2. **Online Verification**
   - Verify type patterns against mypy/pyright docs
   - Check library recommendations against current best practices
   - Confirm version compatibility claims

3. **Feasibility Assessment**
   - Are the proposed changes realistic?
   - What is the effort vs benefit ratio?
   - Are there hidden dependencies?

4. **Breaking Change Analysis**
   - What interfaces change?
   - What downstream code is affected?
   - Is backward compatibility needed?

5. **Risk Assessment**
   - What could go wrong?
   - What tests are needed?
   - What rollback plan exists?

OUTPUT:
Create review report at .claude/reports/plan-review-{timestamp}.md with:
- Issues found (blocking, warning, suggestion)
- Verification results with sources
- Feasibility scores per change
- Breaking change inventory
- Recommended modifications"
)
```

### Step 4.2: Review Report Structure

The reviewer produces:

```text
## Plan Review Report

### Summary
- Blocking Issues: N
- Warnings: N
- Suggestions: N
- Overall Feasibility: High/Medium/Low

### Blocking Issues

#### Issue 1: Protocol misuse in Handler
**Location**: Plan section 2.1
**Problem**: Protocol used where ABC is more appropriate
**Evidence**: [link to mypy docs on Protocol vs ABC]
**Recommendation**: Use ABC with @abstractmethod

### Warnings

#### Warning 1: orjson bytes return
**Location**: Library migration section
**Risk**: Downstream code expects str from json.dumps
**Mitigation**: Add .decode() or update all callers

### Verification Results

| Claim | Verified | Source |
|-------|----------|--------|
| TypeGuard narrows in if blocks | ✓ | mypy docs |
| httpx is drop-in for requests | ✗ | API differs |
| orjson 10x faster | ✓ | benchmark link |

### Breaking Change Inventory

| Change | Affected Code | Severity |
|--------|--------------|----------|
| APIResponse type | 5 functions | Medium |
| httpx migration | 12 call sites | High |

### Recommended Modifications

1. Split httpx migration into separate PR
2. Add compatibility shim for json.dumps
3. Use ABC instead of Protocol for Handler
```

---

## Phase 5: Plan Refinement

Update the plan based on review feedback.

### Step 5.1: Address Blocking Issues

For each blocking issue:

1. Understand the concern
2. Research alternatives
3. Update the plan
4. Document the change

### Step 5.2: Acknowledge Warnings

For each warning:

1. Add mitigation to the plan
2. Or accept risk with justification

### Step 5.3: Consider Suggestions

For each suggestion:

1. Evaluate effort vs benefit
2. Include if beneficial, defer if not

### Step 5.4: Update Plan Document

```text
## Modernization Plan (Revised)

### Changes from Review

1. **Handler: Protocol → ABC**
   - Reason: Plugin system requires inheritance
   - Evidence: [reviewer's mypy docs link]

2. **httpx migration: Deferred**
   - Reason: High breaking change risk
   - Alternative: Create separate PR after core changes

3. **orjson: Added decode shim**
   - Added: compat.dumps() wrapper returning str

### Updated Implementation Order

1. Type aliases and TypedDicts (no breaking changes)
2. Protocol/ABC additions (additive)
3. Generic containers (additive)
4. Any elimination (may require caller updates)
5. [DEFERRED] httpx migration
```

---

## Phase 6: Documentation Discovery

Find documentation that needs updating after code changes.

### Step 6.1: Inventory Documentation

```bash
# Find all documentation files
fd -e md -e rst -e txt . docs/ README.md CHANGELOG.md

# Find docstrings in affected files
uv run rg "^\s+\"\"\"" $ARGUMENTS
```

### Step 6.2: Map Code to Docs

```text
## Documentation Update Plan

### Files to Update

| Doc File | Section | Change Needed |
|----------|---------|---------------|
| README.md | Installation | Add orjson dependency |
| docs/api.md | fetch_data() | Update return type |
| CHANGELOG.md | Unreleased | Add type improvements |

### Docstrings to Update

| Code File | Function | Docstring Change |
|-----------|----------|------------------|
| api.py | fetch_data | Update return type docs |
| models.py | User | Add field descriptions |

### New Documentation Needed

- docs/types.md: Document TypeAliases
- docs/migration.md: Breaking change guide
```

---

## Phase 7: Interface Design

Create interfaces and protocols before implementation.

### Step 7.1: Define Type Aliases

```python
# src/types.py
from typing import TypeAlias

JSONValue: TypeAlias = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
APIResponse: TypeAlias = dict[str, JSONValue]
```

### Step 7.2: Define Protocols

```python
# src/protocols.py
from typing import Protocol

class Handler(Protocol):
    def handle(self, data: bytes) -> None: ...

class Serializable(Protocol):
    def to_dict(self) -> dict[str, Any]: ...
```

### Step 7.3: Define TypedDicts

```python
# src/schemas.py
from typing import TypedDict, NotRequired

class UserData(TypedDict):
    name: str
    email: str
    age: NotRequired[int]
```

### Step 7.4: Define Data Classes

```python
# src/models.py
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int | None = None
```

---

## Phase 8: Test-First Implementation

Delegate to python-pytest-architect to write failing tests against the interfaces.

### Step 8.1: Launch Test Writing Agent

```text
Task(
  agent="python-pytest-architect",
  prompt="Write failing tests for the interfaces defined in the modernization plan.

CONTEXT:
- Plan: .claude/plans/stinkysnake-plan.md
- Interfaces: src/types.py, src/protocols.py, src/schemas.py

REQUIREMENTS:

1. **Test Each Protocol**
   - Test that protocol can be satisfied
   - Test that non-conforming types are rejected
   - Test protocol runtime behavior if applicable

2. **Test Each TypedDict**
   - Test required keys
   - Test optional keys (NotRequired)
   - Test type validation

3. **Test Each Function Signature**
   - Test return type matches TypeAlias
   - Test parameter types
   - Test edge cases

4. **Test Behavioral Expectations**
   - Test that refactored code maintains behavior
   - Test error handling patterns
   - Test async behavior if applicable

OUTPUT:
- Create test files in tests/
- Tests MUST fail (implementations don't exist yet)
- Stop after tests are written
- Report test file locations"
)
```

### Step 8.2: Verify Tests Fail

```bash
# Run tests - they should fail
uv run pytest tests/ -v

# Expected output: X failed, 0 passed
```

---

## Phase 9: Implementation

Use the `/snakepolish` skill to implement until tests pass.

### Step 9.1: Launch Implementation Skill

```text
/snakepolish $ARGUMENTS
```

This skill:

- Has `context: fork` to work in isolation
- Uses `agent: python-cli-architect` for implementation
- Follows the refined plan
- Runs tests after each change
- Continues until all tests pass

### Step 9.2: Verify All Tests Pass

```bash
# Final verification
uv run pytest tests/ -v
uv run mypy $ARGUMENTS --strict
uv run ruff check $ARGUMENTS
```

---

## Output Artifacts

The complete workflow produces:

| Artifact                | Location                                  | Purpose             |
| ----------------------- | ----------------------------------------- | ------------------- |
| Static Analysis Results | `.claude/reports/static-analysis-{ts}.md` | Auto-fix summary    |
| Type Inventory          | `.claude/reports/type-inventory-{ts}.md`  | Any types found     |
| Modernization Plan      | `.claude/plans/stinkysnake-plan.md`       | Implementation plan |
| Plan Review             | `.claude/reports/plan-review-{ts}.md`     | Review feedback     |
| Revised Plan            | `.claude/plans/stinkysnake-plan.md`       | Updated plan        |
| Doc Update Plan         | `.claude/reports/doc-updates-{ts}.md`     | Docs to change      |
| Test Files              | `tests/test_*.py`                         | Failing tests       |
| Implementation          | `src/`                                    | Passing code        |

---

## Quick Reference

### Skill Activations

```text
Skill(command: "holistic-linting")     # Linting workflows
Skill(command: "pre-commit")           # Git hooks
Skill(command: "modernpython")         # Python 3.11+ patterns
Skill(command: "python3-development")  # Core patterns
```

### Agent Delegations

```text
Task(agent="linting-root-cause-resolver", ...)  # Phase 1 linting
Task(agent="python-code-reviewer", ...)          # Phase 4 review
Task(agent="python-pytest-architect", ...)       # Phase 8 tests
```

### Related Skills

```text
/snakepolish  # Phase 9 implementation (context: fork)
```

---

## References

### External Documentation

- [Typing Module](https://docs.python.org/3/library/typing.html)
- [PEP 544 - Protocols](https://peps.python.org/pep-0544/)
- [PEP 589 - TypedDict](https://peps.python.org/pep-0589/)
- [PEP 647 - TypeGuard](https://peps.python.org/pep-0647/)
- [mypy Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

### Companion Plugins

- **holistic-linting** - Linting rules knowledge base
- **pre-commit** - Git hook automation
