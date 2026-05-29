---
name: snakepolish
description: Implementation phase for stinkysnake workflow. Use when tests are written and plan is ready. Implements functions following the modernization plan, runs tests until passing.
user-invocable: true
argument-hint: "[file-paths-or-module]"
context: fork
agent: python-cli-architect
---

# Snake Polish - Implementation Phase

Execute the implementation plan from `/stinkysnake` Phase 9. Implement functions following the modernization plan, run tests iteratively until all pass.

## Arguments

$ARGUMENTS

## Prerequisites

Before invoking this skill, ensure:

1. `/stinkysnake` phases 1-8 completed
2. Modernization plan reviewed and refined
3. Interfaces designed and documented
4. Failing tests written by `python-pytest-architect`

## Instructions

### Step 1: Load Context

Read the stinkysnake plan artifacts:

```text
ARTIFACTS TO LOAD:
- [ ] Modernization plan (Phase 3 output)
- [ ] Plan review feedback (Phase 4-5 output)
- [ ] Interface definitions (Phase 7 output)
- [ ] Failing test files (Phase 8 output)
```

### Step 2: Verify Test Baseline

Run tests to confirm failing state:

```bash
uv run pytest $ARGUMENTS -v --tb=short 2>&1 | head -100
```

**Expected**: Tests fail because implementations don't exist yet.

**If tests pass**: Stop. Implementation already complete or tests are not testing the right things.

### Step 3: Implementation Order

Follow this implementation sequence:

```text
IMPLEMENTATION ORDER:
1. Type definitions (TypeAlias, TypedDict, Protocol)
2. Data structures (dataclass, Pydantic models)
3. Utility functions (pure functions, no side effects)
4. Core business logic
5. Integration points (API clients, file I/O)
6. Entry points (CLI commands, handlers)
```

### Step 4: Implement Following Plan

For each planned change:

```text
FOR EACH IMPLEMENTATION ITEM:
1. Read the interface/protocol definition
2. Read the failing test(s) for this component
3. Implement the function/class
4. Run targeted tests: uv run pytest -k "test_name" -v
5. If fails: debug and fix
6. If passes: move to next item
```

### Step 5: Modern Python Patterns

Apply these patterns during implementation:

#### Type Annotations

```python
# Use modern union syntax
def process(data: str | None) -> dict[str, Any]:
    ...

# Use TypeGuard for narrowing
def is_valid_user(obj: object) -> TypeGuard[User]:
    return isinstance(obj, dict) and "id" in obj
```

#### Protocol-Based Design

```python
from typing import Protocol

class Serializable(Protocol):
    def to_dict(self) -> dict[str, Any]: ...

def save(item: Serializable) -> None:
    data = item.to_dict()
    ...
```

#### Dataclass Patterns

```python
from dataclasses import dataclass, field

@dataclass(slots=True, frozen=True)
class Config:
    name: str
    options: list[str] = field(default_factory=list)
```

#### Pydantic for Validation

```python
from pydantic import BaseModel, Field

class APIResponse(BaseModel):
    status: int = Field(ge=100, le=599)
    data: dict[str, Any]

    model_config = {"strict": True}
```

#### Modern Libraries

```python
# httpx for async HTTP
async with httpx.AsyncClient() as client:
    response = await client.get(url)

# orjson for fast JSON
data = orjson.loads(response.content)
output = orjson.dumps(result, option=orjson.OPT_INDENT_2)

# tomlkit for TOML with comments preserved
doc = tomlkit.parse(content)
doc["section"]["key"] = value
```

### Step 6: Iterative Test Loop

After each implementation batch:

```bash
# Run full test suite
uv run pytest $ARGUMENTS -v --tb=short

# If failures remain, focus on failing tests
uv run pytest $ARGUMENTS -v --tb=long -x  # Stop on first failure
```

### Step 7: Static Analysis Verification

Before completion, verify code quality:

```bash
# Format check
uv run ruff format --check $ARGUMENTS

# Lint check
uv run ruff check $ARGUMENTS

# Type check
uv run mypy $ARGUMENTS --strict
```

Fix any issues that arise.

### Step 8: Final Test Run

Confirm all tests pass:

```bash
uv run pytest $ARGUMENTS -v --cov --cov-report=term-missing
```

**Success Criteria**:

- All tests pass
- No type errors
- No lint errors
- Coverage meets project threshold (typically 80%+)

## Completion

When all tests pass and static analysis is clean:

1. Report implementation summary
2. List any deferred items or technical debt
3. Reference documentation updates needed (from Phase 6)

## Error Handling

### Test Failures That Indicate Test Bugs

If a test failure appears to be a test bug rather than implementation bug:

1. Document the suspected test issue
2. Check the test against the interface specification
3. If test is wrong: fix the test, document the fix
4. If unclear: flag for review, continue with other implementations

### Blocked Implementations

If an implementation is blocked:

1. Document the blocker
2. Check if it's a dependency ordering issue
3. If external dependency: note and continue with independent items
4. If architectural issue: flag for plan revision

## References

- [stinkysnake skill](../stinkysnake/SKILL.md) - Parent workflow
- [python-cli-architect agent](../../agents/python-cli-architect.md) - Implementation agent
- [python3-development skill](../python3-development/SKILL.md) - Modern Python patterns
