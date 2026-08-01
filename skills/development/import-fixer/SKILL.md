---
name: import-fixer
description: 'Fix import statements across the codebase to align with clean architecture
  layer boundaries. Use when: fixing imports, layer boundary violations, circular
  import issues, deprecated core imports, impor'
---

---
name: import-fixer
description: Fix import statements across the codebase to align with clean architecture layer boundaries. Use when: fixing imports, layer boundary violations, circular import issues, deprecated core imports, import order rules.
---

# Import Fixer

Fix imports to follow clean architecture principles.

## Common Issues

### Deprecated Core Imports

```python
# WRONG (deprecated):
from casare_rpa.core.types import DataType

# CORRECT:
from casare_rpa.domain.value_objects.types import DataType
```

### Layer Violations

```python
# WRONG: Presentation importing Infrastructure
from casare_rpa.infrastructure.resources import BrowserResourceManager

# CORRECT: Presentation imports from Application
from casare_rpa.application.use_cases import ExecuteWorkflowUseCase
```

### Circular Dependencies

```python
# Use TYPE_CHECKING for type hints only
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from module_b import ClassB

class ClassA:
    def use_b(self) -> 'ClassB':
        from module_b import ClassB  # Import at runtime
        return ClassB()
```

## Import Order

1. Standard library
2. Third-party
3. Local application

```python
# 1. Standard library
import os
from typing import Any

# 2. Third-party
from loguru import logger
from PySide6.QtCore import Qt

# 3. Local
from casare_rpa.domain.value_objects import ExecutionResult
```

## Layer Rules

```
Presentation → Application → Domain ← Infrastructure
```

**Forbidden:**
- Domain → Infrastructure
- Domain → Application
- Domain → Presentation
- Infrastructure → Presentation

## Verification

```bash
# Check for deprecated imports
grep -r "from casare_rpa.core" src/ tests/

# Check domain violations
grep -r "from casare_rpa.infrastructure" src/casare_rpa/domain/

# Check for circular dependencies
pydeps src/casare_rpa --show-cycles
```
