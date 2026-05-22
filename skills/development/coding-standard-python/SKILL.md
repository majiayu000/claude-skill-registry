---
name: coding-standard-python
description: Enforce Python PEP 8 coding standards including snake_case variables, PascalCase classes, and snake_case filenames.
---

# Python Coding Standards (PEP 8)

When reviewing or generating Python code, follow these rules:

## File Naming
- **Source files:** Use snake_case (e.g., `user_service.py`, `api_client.py`)
- **Package directories:** Use snake_case (e.g., `data_processing/`, `utils/`)
- **Test files:** Use `test_` prefix (e.g., `test_user_service.py`)
- **Config files:** Use snake_case (e.g., `config_settings.py`)

## Variable Naming
- **Variables:** snake_case (e.g., `user_name`, `is_active`, `total_count`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`, `API_BASE_URL`)
- **Boolean variables:** Prefix with `is_`, `has_`, `can_`, `should_` (e.g., `is_loading`, `has_error`)
- **Protected variables:** Single underscore prefix (e.g., `_internal_data`)
- **Private variables:** Double underscore prefix (e.g., `__private_data`)

## Function Naming
- **Functions:** snake_case (e.g., `calculate_total()`, `fetch_user_data()`)
- **Private functions:** Prefix with underscore (e.g., `_validate_input()`, `_process_data()`)
- **Dunder methods:** Double underscores (e.g., `__init__`, `__str__`, `__repr__`)

## Class Naming
- **Classes:** PascalCase (e.g., `UserService`, `DataProcessor`, `ApiClient`)
- **Exception classes:** PascalCase with `Error` or `Exception` suffix (e.g., `ValidationError`)
- **Abstract classes:** PascalCase, optionally prefix with `Base` or `Abstract` (e.g., `BaseHandler`)

## Method Naming
- **Instance methods:** snake_case (e.g., `get_user()`, `process_data()`)
- **Class methods:** snake_case with `@classmethod` decorator
- **Static methods:** snake_case with `@staticmethod` decorator
- **Properties:** snake_case with `@property` decorator

## Module Organization
- Imports at the top: standard library, third-party, local imports (separated by blank lines)
- Module-level dunder names after imports (`__all__`, `__version__`)
- One class per file for large classes; multiple related classes okay for small ones
- Use `__all__` to define public API
