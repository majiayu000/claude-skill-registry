---
name: python-fastapi-ddd-testing-skill
description: Guides unit testing for Python DDD + Onion Architecture apps (Domain Entities/Value Objects and UseCases) using pytest and repository mocks, based on the dddpy reference. Use when adding tests, choosing what to mock, or structuring test folders for a DDD FastAPI project.
license: Apache-2.0
metadata:
  author: Takahiro Ikeuchi
  version: "1.0.0"
---

# Testing DDD Layers with pytest (Domain / UseCase)

This skill focuses on **unit tests** for the inner layers:

- **Domain**: Value Objects + Entities (pure business rules)
- **UseCase**: application workflows that orchestrate Domain + Repository interfaces

It intentionally avoids full HTTP/API tests unless explicitly requested.

## Test strategy (recommended)

1. **Domain tests**: no mocks, assert invariants and state transitions.
2. **UseCase tests**: mock repository interfaces (`Mock(spec=...)`), assert:
   - correct repository method calls
   - correct domain exceptions raised
   - correct entity state transitions
3. **Infrastructure/Presentation**: add integration tests separately (optional).

## Folder structure

Mirror the Onion layers:

```
tests/
  domain/{aggregate}/...
  usecase/{aggregate}/...
  infrastructure/...   # optional integration tests
  presentation/...     # optional API tests
```

## UseCase testing pattern (dddpy-based)

Use `unittest.mock.Mock(spec=RepoInterface)` so typos fail fast.

```python
from unittest.mock import Mock
import pytest

@pytest.fixture
def todo_repository_mock():
    return Mock(spec=TodoRepository)

def test_create_todo_calls_save(todo_repository_mock):
    usecase = CreateTodoUseCaseImpl(todo_repository_mock)
    title = TodoTitle("Test")

    todo = usecase.execute(title=title)

    todo_repository_mock.save.assert_called_once_with(todo)
```

For more examples (Value Object validation, entity lifecycle tests, and exception cases), read `references/TESTING.md`.

