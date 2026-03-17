---
name: implement-repository-pattern
description: |
  Creates repository following Clean Architecture with Protocol in domain layer and Implementation
  in infrastructure layer. Use when adding new data access layer, creating database interaction,
  implementing persistence, or need to store/retrieve domain models. Enforces Protocol/ABC pattern
  with ServiceResult, ManagedResource lifecycle, and proper layer separation. Triggers on "create
  repository for X", "implement data access for Y", "add persistence layer", or "store/retrieve
  domain model".
allowed-tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Grep
  - Bash
---

Works with Python files in domain/repositories/ and infrastructure/ directories.
# Implement Repository Pattern

## Table of Contents

### Core Sections

- [Purpose](#purpose)
  - Core responsibility: Create repositories with Protocol/Implementation separation
- [Quick Start](#quick-start)
  - Fastest path: Create repository from user request to working implementation
- [Instructions](#instructions)
  - [Step 1: Create Domain Protocol (Interface)](#step-1-create-domain-protocol-interface)
  - [Step 2: Create Infrastructure Implementation](#step-2-create-infrastructure-implementation)
  - [Step 3: Add Cypher Queries](#step-3-add-cypher-queries)
  - [Step 4: Register in Container](#step-4-register-in-container)
  - [Step 5: Create Tests](#step-5-create-tests)
- [Examples](#examples)
  - [Example 1: Simple CRUD Repository](#example-1-simple-crud-repository)
  - [Example 2: Repository with Complex Domain Model](#example-2-repository-with-complex-domain-model)
  - [Example 3: Repository with Pagination](#example-3-repository-with-pagination)

### Patterns & Best Practices

- [Common Patterns](#common-patterns)
  - [Pattern 1: Query Parameter Validation](#pattern-1-query-parameter-validation)
  - [Pattern 2: ServiceResult Propagation](#pattern-2-serviceresult-propagation)
  - [Pattern 3: Resource Lifecycle](#pattern-3-resource-lifecycle)
- [Red Flags - STOP](#red-flags---stop)
  - Critical issues to watch for in repository implementation
- [Success Checklist](#success-checklist)
  - Complete validation before marking repository done

### Supporting Resources

- [Requirements](#requirements)
  - Dependencies, project structure, and setup requirements
- [See Also](#see-also)
  - [templates/protocol-template.py](./templates/protocol-template.py) - Repository protocol skeleton
  - [templates/implementation-template.py](./templates/implementation-template.py) - Neo4j implementation skeleton
  - [templates/test-template.py](./templates/test-template.py) - Test suite skeleton
  - [references/pattern-guide.md](./references/pattern-guide.md) - Complete pattern catalog
  - [references/troubleshooting.md](./references/troubleshooting.md) - Common issues and solutions
  - [scripts/analyze_queries.py](./scripts/analyze_queries.py) - Analyze Cypher queries in repository implementations
  - [scripts/generate_repository.py](./scripts/generate_repository.py) - Generate repository pattern files with domain protocol and implementation
  - [scripts/validate_repository_patterns.py](./scripts/validate_repository_patterns.py) - Validate repository pattern compliance across the codebase

## Purpose

Create repositories following Clean Architecture principles with Protocol (domain layer) and Implementation (infrastructure layer) separation. Ensures proper dependency inversion, ServiceResult return types, and resource lifecycle management.

## When to Use

Use this skill when:
- **Adding new data access layer** - Creating persistence for domain models
- **Creating database interaction** - Implementing queries and commands against data stores
- **Implementing persistence** - Storing and retrieving domain entities
- **Need to store/retrieve domain models** - Data access abstraction required

**Trigger phrases:**
- "Create a repository for X"
- "Implement data access for Y"
- "Add persistence layer for Z"
- "Store/retrieve domain model X"

## Quick Start

**User:** "Create a repository for storing search history"

**What happens:**
1. Create Protocol interface in `domain/repositories/search_history_repository.py`
2. Create Neo4j implementation in `infrastructure/neo4j/search_history_repository.py`
3. Implement ManagedResource for lifecycle
4. Use ServiceResult for all operations
5. Add required Cypher queries

**Result:** ✅ Repository with Protocol + Implementation ready for dependency injection

## Instructions

### Step 1: Create Domain Protocol (Interface)

**Location:** `src/project_watch_mcp/domain/repositories/{name}_repository.py`

**Pattern:**
```python
from abc import ABC, abstractmethod
from project_watch_mcp.domain.common import ServiceResult

class {Name}Repository(ABC):
    """Port for {purpose} storage and retrieval.

    This interface defines the contract for {operations}.
    Concrete implementations will be provided in the infrastructure layer.
    """

    @abstractmethod
    async def {operation}(self, param: Type) -> ServiceResult[ReturnType]:
        """Brief description of operation.

        Args:
            param: Description

        Returns:
            ServiceResult[ReturnType]: Success with data or Failure on errors
        """
        pass
```

**Key Requirements:**
- Inherit from `ABC`
- Use `@abstractmethod` decorator
- Return `ServiceResult[T]` for all operations
- Document expected behavior in docstrings
- No implementation details (pure interface)

### Step 2: Create Infrastructure Implementation

**Location:** `src/project_watch_mcp/infrastructure/neo4j/{name}_repository.py`

**Pattern:**
```python
from neo4j import AsyncDriver, RoutingControl
from project_watch_mcp.config.settings import Settings
from project_watch_mcp.domain.common import ServiceResult
from project_watch_mcp.domain.repositories.{name}_repository import {Name}Repository
from project_watch_mcp.domain.services.resource_manager import ManagedResource

class Neo4j{Name}Repository({Name}Repository, ManagedResource):
    """Neo4j adapter implementing {Name}Repository interface."""

    def __init__(self, driver: AsyncDriver, settings: Settings):
        if not driver:
            raise ValueError("Neo4j driver is required")
        if not settings:
            raise ValueError("Settings is required")

        self.driver = driver
        self.settings = settings
        self.database = settings.neo4j.database_name

    async def _execute_with_retry(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
        routing: RoutingControl = RoutingControl.WRITE,
    ) -> ServiceResult[list[dict]]:
        """Execute query with parameter validation and retry logic."""
        # Validate before executing
        validation_result = validate_and_build_query(query, parameters, strict=True)
        if validation_result.is_failure:
            return ServiceResult.fail(f"Validation failed: {validation_result.error}")

        validated_query = validation_result.data

        try:
            records, _, _ = await self.driver.execute_query(
                cast(LiteralString, validated_query.query),
                validated_query.parameters,
                database_=self.database,
                routing_=routing,
            )
            return ServiceResult.ok([dict(record) for record in records])
        except Neo4jError as e:
            return ServiceResult.fail(f"Database error: {str(e)}")

    async def close(self) -> None:
        """Close and cleanup resources (ManagedResource protocol)."""
        # Repository-specific cleanup if needed
        pass
```

**Key Requirements:**
- Implement Protocol interface
- Inherit from `ManagedResource`
- Required constructor params: `driver: AsyncDriver, settings: Settings`
- Validate parameters in constructor (`if not driver: raise ValueError`)
- Use `_execute_with_retry()` for all database operations
- Implement `close()` for resource cleanup
- All operations return `ServiceResult[T]`

### Step 3: Add Cypher Queries

**Location:** `src/project_watch_mcp/infrastructure/neo4j/queries.py`

**Pattern:**
```python
class CypherQueries:
    # Existing queries...

    # {Name}Repository Queries
    GET_{ENTITY} = """
    MATCH (e:{Label} {project_name: $project_name, id: $id})
    RETURN e
    """

    SAVE_{ENTITY} = """
    MERGE (e:{Label} {project_name: $project_name, id: $id})
    SET e += $properties
    SET e.updated_at = datetime()
    RETURN e
    """
```

**Key Requirements:**
- Group queries by repository
- Use parameterized queries (prevent injection)
- Use MERGE for upsert operations
- Include timestamp management
- Document query purpose

**See:** [references/query-patterns.md](./references/query-patterns.md) for common patterns

### Step 4: Register in Container

**Location:** `src/project_watch_mcp/infrastructure/container.py`

**Pattern:**
```python
async def {name}_repository(self) -> {Name}Repository:
    """Provide {Name}Repository implementation."""
    driver = await self.neo4j_driver()
    settings = await self.settings()
    return Neo4j{Name}Repository(driver, settings)
```

**Key Requirements:**
- Return type is Protocol (not implementation)
- Inject dependencies (driver, settings)
- Use async/await for resource initialization
- Follow naming convention: `{name}_repository()`

### Step 5: Create Tests

**Unit Tests:** `tests/unit/infrastructure/neo4j/test_{name}_repository.py`
**Integration Tests:** `tests/integration/infrastructure/neo4j/test_{name}_repository.py`

**Pattern:**
```python
@pytest.mark.asyncio
async def test_save_{entity}_success(mock_driver, settings):
    """Test successful {entity} save operation."""
    # Arrange
    repo = Neo4j{Name}Repository(mock_driver, settings)
    mock_driver.execute_query.return_value = (
        [{"e": {"id": "test", "name": "Test"}}],
        None,
        None,
    )

    # Act
    result = await repo.save_{entity}(entity_data)

    # Assert
    assert result.is_success
    assert result.data is not None
```

**Key Requirements:**
- Test both success and failure cases
- Mock driver.execute_query for unit tests
- Test parameter validation
- Test ServiceResult.ok() and ServiceResult.fail() paths
- Integration tests use real Neo4j instance

## Examples

### Example 1: Simple CRUD Repository

**Protocol:**
```python
class SearchHistoryRepository(ABC):
    @abstractmethod
    async def save_query(self, query: str, user_id: str) -> ServiceResult[None]:
        pass

    @abstractmethod
    async def get_recent_queries(self, user_id: str, limit: int) -> ServiceResult[list[str]]:
        pass
```

**Implementation:**
```python
class Neo4jSearchHistoryRepository(SearchHistoryRepository, ManagedResource):
    async def save_query(self, query: str, user_id: str) -> ServiceResult[None]:
        cypher = """
        CREATE (q:SearchQuery {query: $query, user_id: $user_id, timestamp: datetime()})
        """
        result = await self._execute_with_retry(cypher, {"query": query, "user_id": user_id})
        return ServiceResult.ok(None) if result.is_success else result
```

### Example 2: Repository with Complex Domain Model

For advanced patterns, see [references/pattern-guide.md](./references/pattern-guide.md):
- Converting Neo4j records to domain models
- Handling nested relationships
- Batch operations
- Transaction management

### Example 3: Repository with Pagination

For pagination patterns, see [references/pattern-guide.md](./references/pattern-guide.md):
- Cursor-based pagination
- Offset-based pagination
- Performance considerations

## Requirements

**Dependencies:**
- `neo4j>=5.0.0` - Async driver
- `project_watch_mcp.domain.common` - ServiceResult
- `project_watch_mcp.domain.services.resource_manager` - ManagedResource
- `project_watch_mcp.config.settings` - Settings injection

**Project Structure:**
```
src/project_watch_mcp/
├── domain/
│   └── repositories/
│       └── {name}_repository.py     # Protocol (ABC)
├── infrastructure/
│   └── neo4j/
│       ├── {name}_repository.py     # Implementation
│       └── queries.py               # Cypher queries
└── tests/
    ├── unit/infrastructure/neo4j/
    │   └── test_{name}_repository.py
    └── integration/infrastructure/neo4j/
        └── test_{name}_repository.py
```

## Common Patterns

### Pattern 1: Query Parameter Validation

Always validate query parameters before execution:
```python
validation_result = validate_and_build_query(query, parameters, strict=True)
if validation_result.is_failure:
    return ServiceResult.fail(f"Validation failed: {validation_result.error}")
```

### Pattern 2: ServiceResult Propagation

Chain ServiceResult operations:
```python
result = await self._execute_with_retry(query, params)
if result.is_failure:
    return ServiceResult.fail(f"Failed to save: {result.error}")

# Transform data and return success
return ServiceResult.ok(transformed_data)
```

### Pattern 3: Resource Lifecycle

Implement ManagedResource for proper cleanup:
```python
async def close(self) -> None:
    """Cleanup repository-specific resources."""
    # Driver is managed externally by container
    # Only cleanup repository-specific resources here
    logger.debug(f"{self.__class__.__name__} cleanup complete")
```

**See:** [references/pattern-guide.md](./references/pattern-guide.md) for complete pattern catalog

## Red Flags - STOP

If you see any of these, investigate immediately:

1. ❌ Protocol in infrastructure layer → Must be in domain
2. ❌ Return `None` on error → Use `ServiceResult.fail()`
3. ❌ Optional `settings` parameter → Must be required
4. ❌ Direct driver usage → Use `_execute_with_retry()`
5. ❌ Missing parameter validation → Validate in constructor
6. ❌ Raw Cypher in methods → Use `CypherQueries` class
7. ❌ Synchronous methods → All methods must be `async`
8. ❌ Missing `ManagedResource` → Required for lifecycle
9. ❌ Return domain models from Neo4j layer → Convert in repository
10. ❌ Missing tests → Must have unit + integration tests

## Success Checklist

Before marking repository complete:

- [ ] Protocol exists in `domain/repositories/`
- [ ] Implementation exists in `infrastructure/neo4j/`
- [ ] Constructor validates `driver` and `settings`
- [ ] All methods return `ServiceResult[T]`
- [ ] Implements `ManagedResource` with `close()`
- [ ] Uses `_execute_with_retry()` for all operations
- [ ] Queries defined in `CypherQueries`
- [ ] Registered in container
- [ ] Unit tests passing (mocked driver)
- [ ] Integration tests passing (real Neo4j)
- [ ] Quality gates pass (`./scripts/check_all.sh`)
- [ ] Documentation updated (if new pattern)

## See Also

- [templates/protocol-template.py](./templates/protocol-template.py) - Repository protocol skeleton
- [templates/implementation-template.py](./templates/implementation-template.py) - Neo4j implementation skeleton
- [templates/test-template.py](./templates/test-template.py) - Test suite skeleton
- [references/pattern-guide.md](./references/pattern-guide.md) - Complete pattern catalog
- [references/troubleshooting.md](./references/troubleshooting.md) - Common issues and solutions

**Related Skills:**
- `implement-dependency-injection` - For container registration
- `validate-layer-boundaries` - For architecture compliance
- `run-quality-gates` - For validation before commit

**Last Updated:** 2025-10-18
