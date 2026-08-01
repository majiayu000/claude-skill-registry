---
name: type-safety-mastery
description: 'Master type safety patterns - fix type errors at source, never use type:
  ignore or any, prefer Pydantic models, use type stubs for external libraries'
---

---
name: type-safety-mastery
description: Master type safety patterns - fix type errors at source, never use type: ignore or any, prefer Pydantic models, use type stubs for external libraries
---

# Type Safety Mastery

Fix type errors at their source—never use `# type: ignore` to bypass warnings. When ty reports an error:

- Define proper types (Pydantic models, Protocol)
- Add type annotations to function signatures when library stubs are incomplete

## Never Use Type Ignores

**Never use `# type: ignore[return-value]` or any specific type ignore comments.** If a function's return type doesn't match:

- Fix the actual return type
- Use proper type annotations
- Refactor the code to match the declared type

## Never Use Any Type

**Never use `any` type.** It defeats the purpose of type checking. Instead:

- Use specific types or Union types
- Use TypeVar for generic types
- Use Protocol for duck-typed interfaces
- Use proper type annotations even if it requires more work

## Prefer Optional[T]

**Prefer `Optional[T]` over `T | None`:**

- Use `Optional[str]` instead of `str | None`
- It is more explicit and readable
- Consistent with the codebase style

## Minimize Cast and Runtime Workarounds

**Minimize use of `cast` and runtime workarounds:**

- Avoid using `cast(Type, val)` to silence type errors when possible
- Do not use `getattr(obj, 'attr')` or `setattr(obj, 'attr', val)` to bypass missing type definitions
- **Prefer fixing the root cause:** Update the type stubs in `typings/` instead
- When `cast` is unavoidable (for example, dynamically resolved methods), add a short comment explaining why

## Pydantic Over TypedDict

**Use Pydantic models instead of TypedDict for data structures:**

- Pydantic provides runtime validation
- Better consistency with the rest of the codebase
- Clear error messages when validation fails
- Better IDE support and autocomplete

**Always prefer `BaseModel` over `Dict`/`TypedDict`.** If you catch yourself annotating a variable as `dict[str, X]` (or using `TypedDict`) inside application code, extract a dedicated Pydantic model instead and expose helper methods (`get_size()`, `set_size()`, etc.) so callers never need `.get()` accessors.

**Bad example:**

```python
from typing import TypedDict

class LoRAData(TypedDict):
    id: int
    name: str
    weight: float
```

**Good example:**

```python
from pydantic import BaseModel, Field

class LoRAData(BaseModel):
    id: int = Field(..., description='Database ID')
    name: str = Field(..., description='Display name')
    weight: float = Field(..., ge=0.0, le=2.0, description='Weight/strength')
```

## Type Aliases

**Type aliases for complex types:** Create type aliases for frequently used complex types to improve readability.

**Bad example:**

```python
def list_files(
    self, id: str,
    repo_info: Optional[Union[ModelInfo, DatasetInfo, SpaceInfo]] = None
) -> List[str]:
    pass
```

**Good example:**

```python
# Define type alias once at module level
RepoInfo = Union[ModelInfo, DatasetInfo, SpaceInfo]

def list_files(self, id: str, repo_info: Optional[RepoInfo] = None) -> List[str]:
    pass
```

## Type Stubs for External Libraries

**Use type stubs (.pyi files) for external library types:**

- Create stub files in `typings/{package_name}/` instead of runtime wrapper classes
- **Update existing stubs** when you encounter missing attributes or methods
- Stubs provide type hints without runtime overhead
- Follow PEP 561 conventions (`.pyi` extension)
- Configure stub path in `pyproject.toml` under `[tool.ty.src]`
- Never use runtime assertions (`assert isinstance(...)`) to force types
- **Never use `TYPE_CHECKING`.** If you have to use it, then you did it wrong. Go back and find the root cause, then fix it

Use public interfaces by default (`lock`, `set_state()`) and reserve underscores for truly private implementation details.
