---
name: architecture-planner
description: Design component architecture and module structure using established
  architectural patterns for clean, maintainable, and scalable systems.
allowed-tools: Read, Write, Edit
---

## Purpose

The architecture-planner skill provides comprehensive guidance for designing component architecture and module structure in feature implementations. This skill helps the Architecture Designer agent plan clean, layered architectures following established patterns such as Layered Architecture, Hexagonal Architecture (Ports and Adapters), and Clean Architecture principles.

This skill emphasizes:
- **Clear component boundaries** with single responsibilities
- **Layer separation** between interfaces, business logic, and data access
- **Dependency injection** for testability and flexibility
- **Extension points** for future enhancements
- **Design patterns** that improve maintainability

The architecture-planner skill is essential for creating implementations that are easy to test, maintain, and extend over time.

## When to Use

This skill auto-activates when the agent describes:
- "Plan component architecture for..."
- "Design module structure with..."
- "Separate concerns into layers..."
- "Structure the codebase with..."
- "Organize components using..."
- "Define interfaces between..."
- "Create extension points for..."
- "Apply architectural pattern..."

## Provided Capabilities

### 1. Component Identification and Boundaries

**What it provides:**
- Identification of distinct components based on responsibilities
- Clear component boundaries following Single Responsibility Principle
- Component naming conventions and file organization
- Determination of component granularity (not too large, not too small)

**Guidance:**
- Each component should have ONE primary responsibility
- Components should be independently testable
- Components should have minimal coupling with others
- Use descriptive names that reflect the component's purpose

**Example:**
```python
# Good: Clear, focused components
components = [
    {
        "name": "FeatureProcessor",
        "responsibility": "Process feature requests according to business rules",
        "file": "src/core/processor.py"
    },
    {
        "name": "DataValidator",
        "responsibility": "Validate input data against schemas",
        "file": "src/core/validator.py"
    },
    {
        "name": "ResultFormatter",
        "responsibility": "Format processing results for output",
        "file": "src/core/formatter.py"
    }
]

# Bad: Too broad, multiple responsibilities
components = [
    {
        "name": "FeatureHandler",
        "responsibility": "Process, validate, format, store, and log features",
        "file": "src/feature_handler.py"  # Too many responsibilities!
    }
]
```

### 2. Layer Separation (Presentation, Business, Data)

**What it provides:**
- Three-layer architecture design
- Clear separation between concerns
- Dependencies flow from outer layers (presentation) to inner layers (business logic)
- Data layer abstraction through repositories or adapters

**Layer Definitions:**

**Presentation Layer (Interfaces):**
- CLI interfaces
- REST API endpoints
- GraphQL resolvers
- Event handlers
- External system interfaces

**Business Layer (Core):**
- Business logic and rules
- Domain models and entities
- Service orchestration
- Use cases and workflows
- Validation logic

**Data Layer (Implementations):**
- Database adapters
- External service clients
- File system operations
- Caching mechanisms
- Data access repositories

**Example:**
```python
# Layered Architecture Structure
architecture = {
    "presentation_layer": {
        "location": "src/interfaces/",
        "components": [
            "src/interfaces/cli/commands.py",
            "src/interfaces/api/routes.py",
            "src/interfaces/api/schemas.py"
        ],
        "dependencies": ["business_layer"]
    },
    "business_layer": {
        "location": "src/core/",
        "components": [
            "src/core/processor.py",
            "src/core/validator.py",
            "src/core/models.py",
            "src/core/services.py"
        ],
        "dependencies": ["data_layer (via interfaces)"]
    },
    "data_layer": {
        "location": "src/adapters/",
        "components": [
            "src/adapters/database.py",
            "src/adapters/external_api.py",
            "src/adapters/file_storage.py"
        ],
        "dependencies": ["external systems"]
    }
}
```

### 3. Dependency Injection Patterns

**What it provides:**
- Constructor injection for required dependencies
- Property injection for optional dependencies
- Interface-based dependency injection
- Dependency inversion principle application
- Mock-friendly architecture for testing

**Benefits:**
- Testability: Easy to inject mocks and test doubles
- Flexibility: Change implementations without modifying client code
- Decoupling: Components depend on abstractions, not concretions

**Example:**
```python
# Good: Dependency Injection
from abc import ABC, abstractmethod
from typing import Protocol

# Define interface (abstraction)
class IDataRepository(Protocol):
    async def save(self, data: dict) -> bool:
        ...

    async def retrieve(self, id: str) -> dict:
        ...

# Business logic depends on interface
class FeatureProcessor:
    def __init__(self, repository: IDataRepository):
        """Inject repository dependency via constructor."""
        self.repository = repository

    async def process(self, feature_data: dict) -> dict:
        # Process data
        result = self._apply_business_rules(feature_data)

        # Save using injected repository
        await self.repository.save(result)

        return result

# Implementation can be swapped
class PostgresRepository:
    async def save(self, data: dict) -> bool:
        # PostgreSQL implementation
        pass

    async def retrieve(self, id: str) -> dict:
        # PostgreSQL implementation
        pass

class MongoRepository:
    async def save(self, data: dict) -> bool:
        # MongoDB implementation
        pass

    async def retrieve(self, id: str) -> dict:
        # MongoDB implementation
        pass

# Usage: Inject different implementations
processor_postgres = FeatureProcessor(PostgresRepository())
processor_mongo = FeatureProcessor(MongoRepository())

# Testing: Inject mock
class MockRepository:
    async def save(self, data: dict) -> bool:
        return True

    async def retrieve(self, id: str) -> dict:
        return {"id": id, "status": "test"}

processor_test = FeatureProcessor(MockRepository())
```

### 4. Module Organization and File Structure

**What it provides:**
- Directory structure recommendations
- File naming conventions
- Module boundaries and dependencies
- Import organization

**Standard Structure:**
```
src/
├── interfaces/          # Presentation layer
│   ├── cli/
│   │   └── commands.py
│   └── api/
│       ├── routes.py
│       └── schemas.py
├── core/                # Business layer
│   ├── models.py        # Domain models
│   ├── services.py      # Business services
│   ├── processor.py     # Core processing logic
│   └── validator.py     # Validation logic
├── adapters/            # Data layer
│   ├── database.py      # Database adapter
│   ├── external_api.py  # External API client
│   └── cache.py         # Cache adapter
├── config/              # Configuration
│   └── settings.py
└── utils/               # Shared utilities
    └── helpers.py

tests/
├── unit/                # Unit tests (mirror src structure)
│   ├── core/
│   └── adapters/
└── integration/         # Integration tests
    └── api/
```

### 5. Extension Points and Plugin Architecture

**What it provides:**
- Strategy pattern for pluggable algorithms
- Observer pattern for event handling
- Factory pattern for object creation
- Plugin registration mechanisms

**Example:**
```python
# Extension point using Strategy Pattern
from abc import ABC, abstractmethod
from typing import Dict

class ProcessingStrategy(ABC):
    """Base class for processing strategies (extension point)."""

    @abstractmethod
    async def process(self, data: dict) -> dict:
        """Process data using specific strategy."""
        pass

class FastProcessingStrategy(ProcessingStrategy):
    """Fast processing with lower accuracy."""

    async def process(self, data: dict) -> dict:
        # Fast implementation
        return {"result": "fast"}

class AccurateProcessingStrategy(ProcessingStrategy):
    """Slower processing with higher accuracy."""

    async def process(self, data: dict) -> dict:
        # Accurate implementation
        return {"result": "accurate"}

# Plugin registration
class ProcessorFactory:
    _strategies: Dict[str, ProcessingStrategy] = {}

    @classmethod
    def register_strategy(cls, name: str, strategy: ProcessingStrategy):
        """Register new processing strategy (plugin)."""
        cls._strategies[name] = strategy

    @classmethod
    def get_strategy(cls, name: str) -> ProcessingStrategy:
        """Retrieve registered strategy."""
        return cls._strategies.get(name)

# Register built-in strategies
ProcessorFactory.register_strategy("fast", FastProcessingStrategy())
ProcessorFactory.register_strategy("accurate", AccurateProcessingStrategy())

# Users can register custom strategies
class CustomStrategy(ProcessingStrategy):
    async def process(self, data: dict) -> dict:
        return {"result": "custom"}

ProcessorFactory.register_strategy("custom", CustomStrategy())
```

### 6. Design Pattern Application

**What it provides:**
- Repository Pattern for data access abstraction
- Strategy Pattern for algorithm selection
- Factory Pattern for object creation
- Observer Pattern for event handling
- Adapter Pattern for external system integration

**Pattern Selection Guide:**
- **Repository:** Abstract data access logic
- **Strategy:** Multiple algorithms for same operation
- **Factory:** Complex object creation
- **Observer:** Event-driven communication
- **Adapter:** Integrate with external systems

## Usage Guide

### Step 1: Identify Core Functionality
```
Analyze requirements → Extract core features → Define boundaries
```

### Step 2: Determine Layers
```
Identify interfaces (CLI, API) → Core logic → Data access
```

### Step 3: Define Components
```
For each layer → List components → Define responsibilities
```

### Step 4: Establish Dependencies
```
Map dependencies → Apply dependency injection → Define interfaces
```

### Step 5: Select Patterns
```
Identify needs → Choose patterns → Document rationale
```

### Step 6: Plan Extension Points
```
Identify future needs → Design plugin mechanisms → Document APIs
```

### Step 7: Document Architecture
```
Create diagrams → Document decisions → Provide examples
```

### Step 8: Validate Design
```
Check SOLID principles → Verify testability → Review maintainability
```

## Best Practices

1. **Follow SOLID Principles**
   - Single Responsibility: Each component has one reason to change
   - Open/Closed: Open for extension, closed for modification
   - Liskov Substitution: Subtypes must be substitutable for base types
   - Interface Segregation: Many specific interfaces better than one general
   - Dependency Inversion: Depend on abstractions, not concretions

2. **Keep Components Small and Focused**
   - Maximum 500 lines per file
   - Single responsibility per component
   - Clear, descriptive names
   - Minimal coupling

3. **Use Dependency Injection**
   - Constructor injection for required dependencies
   - Avoid global state and singletons
   - Enable easy testing with mocks

4. **Design for Testability**
   - Inject dependencies
   - Use interfaces/protocols
   - Avoid static methods and global state
   - Keep business logic pure (no side effects)

5. **Document Architectural Decisions**
   - Explain pattern choices
   - Document trade-offs
   - Provide usage examples
   - Include diagrams

6. **Plan for Extension**
   - Identify likely future changes
   - Create extension points
   - Use plugin architectures
   - Version APIs

## Resources

### architecture-patterns.md
Comprehensive guide to architectural patterns including:
- Layered Architecture (presentation, business, data layers)
- Hexagonal Architecture (ports and adapters)
- Event-Driven Architecture
- Microservices patterns
- Clean Architecture principles
- Pattern selection criteria and trade-offs

### component-design-guide.md
Detailed component design guidelines including:
- Single Responsibility Principle application
- Dependency Injection patterns and examples
- Interface design best practices
- Module boundary definition
- Extension point design
- Component interaction patterns

## Example Usage

### Input (from Architecture Designer agent):
```
"Design component architecture for a feature that processes user uploads, validates content, stores files, and sends notifications."
```

### Output (architecture-planner skill provides):
```python
architecture = {
    "layers": {
        "interfaces": [
            "src/interfaces/api/upload_routes.py - REST API endpoints",
            "src/interfaces/api/schemas.py - Request/response schemas"
        ],
        "core": [
            "src/core/upload_processor.py - Main processing orchestration",
            "src/core/content_validator.py - Content validation logic",
            "src/core/notification_service.py - Notification business logic",
            "src/core/models.py - Domain models"
        ],
        "adapters": [
            "src/adapters/file_storage.py - File storage adapter (S3/local)",
            "src/adapters/notification_client.py - Notification service client"
        ]
    },
    "components": [
        {
            "name": "UploadProcessor",
            "file": "src/core/upload_processor.py",
            "responsibility": "Orchestrate upload processing workflow",
            "dependencies": ["ContentValidator", "IFileStorage", "INotificationClient"],
            "interface": None,
            "pattern": "Service layer with dependency injection"
        },
        {
            "name": "ContentValidator",
            "file": "src/core/content_validator.py",
            "responsibility": "Validate uploaded content (size, type, malware scan)",
            "dependencies": [],
            "interface": None,
            "pattern": "Pure function (stateless validation)"
        },
        {
            "name": "IFileStorage",
            "file": "src/adapters/file_storage.py",
            "responsibility": "Abstract file storage operations",
            "dependencies": [],
            "interface": "Protocol/ABC",
            "pattern": "Repository pattern for file storage"
        }
    ],
    "patterns_applied": [
        "Dependency Injection: All services receive dependencies via constructor",
        "Repository Pattern: File storage abstraction through IFileStorage",
        "Strategy Pattern: Pluggable validators for different content types",
        "Adapter Pattern: External notification service wrapped in adapter"
    ],
    "extension_points": [
        "IFileStorage can support S3, Azure Blob, local filesystem",
        "ContentValidator can add new validation strategies",
        "INotificationClient can support email, SMS, push notifications"
    ]
}
```

## Integration

### Used By:
- **@architecture-designer** (Primary) - Phase 2 sub-agent for architecture design

### Integrates With:
- **data-modeler** skill - Data models designed after component structure
- **api-designer** skill - API contracts defined after component interfaces
- **sequential-thinking-mcp** - Deep reasoning for pattern selection

### Workflow Position:
1. Analysis Specialist completes requirements analysis
2. Architecture Designer receives analysis
3. **architecture-planner skill** designs component structure (Step 3)
4. data-modeler skill designs data models (Step 4)
5. api-designer skill designs API contracts (Step 5)
6. Results synthesized into PRP

---

**Version:** 2.0.0
**Auto-Activation:** Yes
**Phase:** 2 - Design & Planning
**Created:** 2025-10-29