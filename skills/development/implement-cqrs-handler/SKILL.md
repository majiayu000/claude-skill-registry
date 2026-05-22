---
name: implement-cqrs-handler
description: |
  Provides step-by-step implementation guide for creating CQRS command or query handlers
  following project patterns with ServiceResult, dependency injection, and handler
  registration. Use when implementing new use cases, adding features, creating API
  endpoints, or building application layer logic.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

Works with Python handlers in application/commands/ and application/queries/.
# Implement CQRS Handler

## Purpose
Create command or query handlers following the project's CQRS pattern with proper separation of write (command) and read (query) operations, ServiceResult pattern, and dependency injection.

## When to Use

Use this skill when:
- **Implementing new use cases** - Creating new application layer operations
- **Adding features** - Building new functionality that modifies or queries data
- **Creating API endpoints** - Wiring business logic to interface layer
- **Building application layer logic** - Orchestrating domain services and repositories

**Trigger phrases:**
- "Create a command handler for X"
- "Implement a query to retrieve Y"
- "Add a new use case for Z"
- "Build handler for feature X"

## Quick Start

**Command Handler (writes, returns ServiceResult[None]):**
```python
# src/{{PROJECT_NAME}}/application/commands/my_command.py
from {{PROJECT_NAME}}.application.commands.base import CommandHandler
from {{PROJECT_NAME}}.domain.common import ServiceResult

class MyCommandHandler(CommandHandler[MyCommand]):
    def __init__(self, repository: MyRepository):
        self.repository = repository

    async def handle(self, command: MyCommand) -> ServiceResult[None]:
        # Implementation
        return ServiceResult.ok(None)
```

**Query Handler (reads, returns ServiceResult[TResult]):**
```python
# src/{{PROJECT_NAME}}/application/queries/my_query.py
from {{PROJECT_NAME}}.application.queries.base import QueryHandler
from {{PROJECT_NAME}}.application.dto.my_dto import MyDTO
from {{PROJECT_NAME}}.domain.common import ServiceResult

class MyQueryHandler(QueryHandler[MyQuery, list[MyDTO]]):
    def __init__(self, repository: MyRepository):
        self.repository = repository

    async def handle(self, query: MyQuery) -> ServiceResult[list[MyDTO]]:
        # Implementation
        return ServiceResult.ok(results)
```

## Table of Contents

### Core Sections
- [Purpose](#purpose) - What this skill helps you build
- [Quick Start](#quick-start) - Immediate working examples for commands and queries
- [Instructions](#instructions) - Complete implementation guide
  - [Step 1: Decide Command vs Query](#step-1-decide-command-vs-query) - When to use each pattern
  - [Step 2: Create Request Object](#step-2-create-request-object) - Define command/query data structures
  - [Step 3: Create Handler](#step-3-create-handler) - Implement handler logic with templates
  - [Step 4: Create DTO](#step-4-create-dto-queries-only) - Data transfer objects for queries
  - [Step 5: Register in Container](#step-5-register-in-container) - Dependency injection setup
  - [Step 6: Wire to MCP Tool](#step-6-wire-to-mcp-tool) - Expose handler via MCP interface

### Supporting Resources
- [Templates](templates/) - Handler skeletons and boilerplate code
  - [templates/command_handler.py](templates/command_handler.py) - Command handler skeleton
  - [templates/query_handler.py](templates/query_handler.py) - Query handler skeleton
- [References](references/reference.md) - CQRS pattern deep dive and architecture
- [Requirements](#requirements) - Pattern compliance checklist

### Utility Scripts
- [Generate Handler](./scripts/generate_handler.py) - Auto-generate CQRS handler boilerplate code
- [List Handlers](./scripts/list_handlers.py) - List and inventory all CQRS handlers in the project
- [Validate CQRS Separation](./scripts/validate_cqrs_separation.py) - Validate CQRS pattern separation in handlers

### Related Documentation
- ARCHITECTURE.md - System architecture overview
- CLAUDE.md - Core rules and patterns

## Instructions

### Step 1: Decide Command vs Query

**Use Command when:**
- Writing/modifying data
- Changing system state
- Side effects required
- Examples: IndexFile, DeleteFile, InitializeProject

**Use Query when:**
- Reading data only
- No state changes
- Retrieving information
- Examples: SearchCode, GetStats, FindRelated

### Step 2: Create Request Object

**For Commands:**
```python
# src/{{PROJECT_NAME}}/application/commands/my_command_command.py
from dataclasses import dataclass
from {{PROJECT_NAME}}.application.commands.base import Command

@dataclass
class MyCommand(Command):
    """Command to perform write operation.

    Contains all data needed for the operation.
    """
    param1: str
    param2: int
    force: bool = False
```

**For Queries:**
```python
# src/{{PROJECT_NAME}}/application/queries/my_query.py
from dataclasses import dataclass
from {{PROJECT_NAME}}.application.queries.base import Query

@dataclass
class MyQuery(Query):
    """Query to retrieve data.

    Contains parameters for data retrieval.
    """
    filter_by: str
    limit: int = 10
```

### Step 3: Create Handler

**Command Handler Template:**
```python
from {{PROJECT_NAME}}.application.commands.base import CommandHandler
from {{PROJECT_NAME}}.core.monitoring import get_logger, traced
from {{PROJECT_NAME}}.domain.common import ServiceResult

logger = get_logger(__name__)

class MyCommandHandler(CommandHandler[MyCommand]):
    """Handler for MyCommand.

    Orchestrates the operation using domain services.
    """

    def __init__(
        self,
        repository: MyRepository,
        service: MyService,
    ):
        """Initialize with required dependencies.

        Args:
            repository: Repository for persistence
            service: Service for business logic
        """
        if not repository:
            raise ValueError("Repository required")
        if not service:
            raise ValueError("Service required")
        self.repository = repository
        self.service = service

    @traced
    async def handle(self, command: MyCommand) -> ServiceResult[None]:
        """Execute the command.

        Args:
            command: The command to execute

        Returns:
            ServiceResult indicating success or failure
        """
        try:
            # 1. Validate inputs
            validation = self._validate(command)
            if not validation.success:
                return validation

            # 2. Execute business logic
            result = await self.service.do_work(command.param1)
            if not result.success:
                return ServiceResult.fail(result.error)

            # 3. Persist changes
            save_result = await self.repository.save(result.data)
            if not save_result.success:
                return ServiceResult.fail(f"Save failed: {save_result.error}")

            logger.info(f"Command completed: {command.param1}")
            return ServiceResult.ok(
                None,
                items_processed=1,
                operation="my_command"
            )

        except Exception as e:
            logger.exception(f"Command failed: {str(e)}")
            return ServiceResult.fail(f"Unexpected error: {str(e)}")

    def _validate(self, command: MyCommand) -> ServiceResult[None]:
        """Validate command parameters."""
        if not command.param1:
            return ServiceResult.fail("param1 is required")
        return ServiceResult.ok(None)
```

**Query Handler Template:**
```python
from {{PROJECT_NAME}}.application.queries.base import QueryHandler
from {{PROJECT_NAME}}.application.dto.my_dto import MyDTO
from {{PROJECT_NAME}}.core.monitoring import get_logger, traced
from {{PROJECT_NAME}}.domain.common import ServiceResult

logger = get_logger(__name__)

class MyQueryHandler(QueryHandler[MyQuery, list[MyDTO]]):
    """Handler for MyQuery.

    Retrieves data without modifying system state.
    """

    def __init__(
        self,
        repository: MyRepository,
    ):
        """Initialize with required dependencies.

        Args:
            repository: Repository for data retrieval
        """
        if not repository:
            raise ValueError("Repository required")
        self.repository = repository

    @traced
    async def handle(self, query: MyQuery) -> ServiceResult[list[MyDTO]]:
        """Execute the query.

        Args:
            query: The query to execute

        Returns:
            ServiceResult containing the requested data or error
        """
        try:
            # 1. Validate query
            if query.limit < 1:
                return ServiceResult.fail("Limit must be at least 1")

            # 2. Fetch data
            results = await self.repository.find_by_filter(
                filter_by=query.filter_by,
                limit=query.limit
            )
            if not results.success:
                return ServiceResult.fail(results.error)

            # 3. Convert to DTOs
            dtos = [MyDTO.from_entity(entity) for entity in results.data]

            logger.info(f"Query returned {len(dtos)} results")
            return ServiceResult.ok(
                dtos,
                metadata={"total_results": len(dtos), "filter": query.filter_by}
            )

        except Exception as e:
            logger.exception(f"Query failed: {str(e)}")
            return ServiceResult.fail(f"Unexpected error: {str(e)}")
```

### Step 4: Create DTO (Queries Only)

If query returns complex data, create a DTO:

```python
# src/{{PROJECT_NAME}}/application/dto/my_dto.py
from dataclasses import dataclass
from typing import Any

@dataclass
class MyDTO:
    """Data transfer object for query results.

    Carries data from application layer to interface layer.
    Contains only data, no business logic.
    """
    id: str
    name: str
    value: int
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
            "metadata": self.metadata,
        }

    @classmethod
    def from_entity(cls, entity) -> "MyDTO":
        """Create from domain entity."""
        return cls(
            id=entity.id,
            name=entity.name,
            value=entity.value,
            metadata=entity.metadata,
        )
```

### Step 5: Register in Container

Add handler to `src/{{PROJECT_NAME}}/interfaces/mcp/container.py`:

```python
# 1. Import handler at top
from {{PROJECT_NAME}}.application.commands.my_command import MyCommandHandler

# 2. Add provider in Container class
class Container(containers.DeclarativeContainer):
    # ... existing providers ...

    # Command Handlers
    my_command_handler = providers.Singleton(
        MyCommandHandler,
        repository=code_repository,  # Inject dependencies
        service=my_service,
    )
```

### Step 6: Wire to MCP Tool

Add MCP tool in `src/{{PROJECT_NAME}}/interfaces/mcp/server.py`:

```python
@mcp.tool()
async def my_operation(param1: str, param2: int) -> dict[str, Any]:
    """Perform my operation.

    Args:
        param1: Description
        param2: Description

    Returns:
        Result dictionary
    """
    command = MyCommand(param1=param1, param2=param2)
    result = await container.my_command_handler().handle(command)

    if not result.success:
        return {"success": False, "error": result.error}

    return {"success": True, "message": "Operation completed"}
```

## Pattern Examples

The Quick Start and Instructions sections above provide complete working examples:
- Command handler with validation (Step 3)
- Query handler with DTO conversion (Step 3)
- DTO creation pattern (Step 4)
- Container registration (Step 5)
- MCP tool wiring (Step 6)

## Requirements

- Handler extends `CommandHandler[TCommand]` or `QueryHandler[TQuery, TResult]`
- Request object extends `Command` or `Query`
- Return type is always `ServiceResult[T]`
- Commands return `ServiceResult[None]`
- Queries return `ServiceResult[TResult]` (often DTOs)
- All dependencies injected via constructor
- Constructor validates dependencies (fail-fast)
- Use `@traced` decorator for OpenTelemetry tracing
- Use `get_logger(__name__)` for logging
- No optional dependencies - all required

## See Also

- [templates/command_handler.py](./templates/command_handler.py) - Command handler skeleton
- [templates/query_handler.py](./templates/query_handler.py) - Query handler skeleton
- [references/reference.md](./references/reference.md) - CQRS pattern deep dive
- ARCHITECTURE.md - System architecture overview
- CLAUDE.md - Core rules and patterns
