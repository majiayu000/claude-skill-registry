---
name: core-python-best-practices
description: Essential guidelines for writing modern, type-safe, and idiomatic Python 3 code.
license: MIT
metadata:
  author: AI Group
  version: "1.0.0"
  category: Software_Engineering
compatibility:
  - system: Python 3.10+
allowed-tools:
  - read_file
  - replace
  - write_file
---

# Core Python Best Practices

This skill defines the coding standards for Python development within the project. It emphasizes modern features, type safety, and readability.

## When to Use This Skill

*   **New Scripts**: Starting a new agent or tool.
*   **Refactoring**: Modernizing legacy code.
*   **Library Design**: Creating reusable modules.

## Core Capabilities

1.  **Type Hinting**: Mandatory use of `typing` module or native types (Python 3.9+).
2.  **Data Classes**: Using `@dataclass` or `Pydantic` for data containers instead of raw dictionaries/tuples.
3.  **Modern Control Flow**: Using `match/case` (Python 3.10) where appropriate.
4.  **Error Handling**: Proper use of `try/except` chains and custom exceptions.

## Workflow

1.  **Define Interface**: Start with function signatures and type hints.
2.  **Select Structure**: Choose between a simple function, a class, or a dataclass.
3.  **Implement**: Write logic using list comprehensions and generators where possible.
4.  **Document**: Add docstrings (Google or NumPy style).

## Example Usage

**User**: "Write a function to process a list of users."

**Agent Action**:
1.  Reads `references/rules.md`.
2.  Generates:
    ```python
    from dataclasses import dataclass
    
    @dataclass
    class User:
        id: int
        name: str

    def process_users(users: list[User]) -> None:
        """Processes a list of users."""
        for user in users:
            ...
    ```
