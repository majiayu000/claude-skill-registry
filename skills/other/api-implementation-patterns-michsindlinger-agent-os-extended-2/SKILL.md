---
name: [PROJECT]-api-patterns
description: [PROJECT] REST API implementation patterns and conventions
globs: ["**/*.{java,ts,js,py,rb,go}"]
---

# API Implementation Patterns

> **Template for project-specific API implementation skill**
> Fill in [CUSTOMIZE] sections with your project's detected or chosen patterns

**Project**: [PROJECT NAME]
**Framework**: [CUSTOMIZE: Spring Boot / Express.js / FastAPI / Django / Ruby on Rails / Gin]
**Language**: [CUSTOMIZE: Java / TypeScript / Python / Ruby / Go]
**Last Updated**: [DATE]

---

## Controller/Route Layer

### File Organization

**Location**: [CUSTOMIZE: src/main/java/controllers / src/controllers / app/routers]

**Naming Convention**: [CUSTOMIZE: UserController / UsersController / user_controller / user.routes]

**Pattern Type**: [CUSTOMIZE: Class-based / Function-based / Decorator-based]

### Endpoint Definition Pattern

**[CUSTOMIZE WITH YOUR PROJECT'S ACTUAL PATTERN]**

**Example - GET Endpoint**:
```[language]
[CUSTOMIZE: Show actual code pattern from your project]

Example patterns:
- Spring Boot: @GetMapping("/users")
- Express: router.get('/users', async (req, res) => {...})
- FastAPI: @router.get("/users")
- Django: viewsets.ModelViewSet
- Rails: resources :users
```

**Example - POST Endpoint with Validation**:
```[language]
[CUSTOMIZE: Show create/post pattern]
```

**Example - PUT/PATCH Endpoint**:
```[language]
[CUSTOMIZE: Show update pattern]
```

**Example - DELETE Endpoint**:
```[language]
[CUSTOMIZE: Show delete pattern]
```

### Request/Response Handling

**Request Body Parsing**: [CUSTOMIZE: @RequestBody / req.body / Request / request.data]

**Response Format**: [CUSTOMIZE: ResponseEntity / res.json() / JSONResponse / render]

**Status Codes**: [CUSTOMIZE: Which codes used - 200, 201, 204, 400, 404, 500]

---

## Service Layer

### File Organization

**Location**: [CUSTOMIZE: src/main/java/services / src/services / app/services]

**Naming**: [CUSTOMIZE: UserService / UsersService / user_service / UserService.ts]

**Pattern**: [CUSTOMIZE: Class-based / Function-based / Module-based]

### Business Logic Pattern

**[CUSTOMIZE WITH ACTUAL PATTERN]**

**Example - CRUD Operations**:
```[language]
[CUSTOMIZE: Show service class/module structure]

Example:
- Create: createUser(data) → validates, saves, returns
- Read: getUserById(id) → finds, throws if not found
- Update: updateUser(id, data) → finds, validates, updates
- Delete: deleteUser(id) → checks dependencies, deletes
```

### Transaction Management

**Approach**: [CUSTOMIZE: @Transactional / BEGIN/COMMIT / context manager / transaction.atomic]

**Isolation Level**: [CUSTOMIZE: READ_COMMITTED / Default / Custom]

---

## Data Access Layer

### File Organization

**Location**: [CUSTOMIZE: src/main/java/repositories / src/repositories / app/models]

**Naming**: [CUSTOMIZE: UserRepository / UsersRepository / user_repository]

**Pattern**: [CUSTOMIZE: Spring Data JPA / Prisma / SQLAlchemy / ActiveRecord / Raw SQL]

### Query Pattern

**[CUSTOMIZE WITH ACTUAL PATTERN]**

**Standard Queries**:
```[language]
[CUSTOMIZE: Show query methods]

Examples:
- findById(id)
- findAll()
- save(entity)
- delete(id)
```

**Custom Queries**:
```[language]
[CUSTOMIZE: How custom queries are defined]

Examples:
- Spring Data: findByEmail(email)
- Prisma: findMany({ where: {...}})
- SQLAlchemy: query.filter_by(email=email)
```

### N+1 Query Prevention

**Strategy**: [CUSTOMIZE: @EntityGraph / .include() / select_related() / eager loading]

---

## Data Models / Entities

### File Organization

**Location**: [CUSTOMIZE: src/main/java/entities / src/models / app/models]

**Naming**: [CUSTOMIZE: User / UserEntity / user.model / User.java]

### Field Naming

**Convention**: [CUSTOMIZE: camelCase / snake_case / PascalCase]

**Examples**:
- User ID: [userId / user_id / id]
- Email: [email / emailAddress / email_address]
- Created timestamp: [createdAt / created_at / dateCreated]

### Relationships

**Pattern**: [CUSTOMIZE: @OneToMany / hasMany / ForeignKey / references]

**Example**:
```[language]
[CUSTOMIZE: How relationships are defined]
```

### Validation

**Location**: [CUSTOMIZE: Entity level / DTO level / Separate validators]

**Approach**: [CUSTOMIZE: Annotations / Decorators / Validator classes / Schemas]

---

## DTOs / Serializers

### File Organization

**Location**: [CUSTOMIZE: src/main/java/dto / src/dto / app/serializers]

**Naming Convention**: [CUSTOMIZE: UserDTO / UserResponse / CreateUserDTO / user_schema]

### Request DTOs

**Pattern**: [CUSTOMIZE: Records / Classes / Interfaces / Pydantic models]

**Example**:
```[language]
[CUSTOMIZE: Show CreateRequest pattern]
```

**Validation**: [CUSTOMIZE: @Valid / class-validator / Pydantic / Rails validations]

### Response DTOs

**Pattern**: [CUSTOMIZE: Same as request / Separate / ViewModels]

**Example**:
```[language]
[CUSTOMIZE: Show Response DTO]
```

### Mapping

**Approach**: [CUSTOMIZE: Manual / MapStruct / class-transformer / Serializer]

---

## Exception Handling

### Custom Exceptions

**Location**: [CUSTOMIZE: src/exceptions / src/errors / app/exceptions]

**Naming**: [CUSTOMIZE: ResourceNotFoundException / NotFoundError / ResourceNotFound]

**Example**:
```[language]
[CUSTOMIZE: Show custom exception]
```

### Global Handler

**Pattern**: [CUSTOMIZE: @ControllerAdvice / middleware / exception_handler / rescue_from]

**Error Response Format**:
```json
[CUSTOMIZE: Show your error response structure]
{
  "status": 404,
  "message": "User not found",
  "timestamp": "2025-12-30T10:00:00Z"
}
```

---

## Testing Patterns

### Unit Tests

**Framework**: [CUSTOMIZE: JUnit 5 / Jest / Pytest / RSpec]

**Mocking**: [CUSTOMIZE: Mockito / sinon / unittest.mock / RSpec mocks]

**Test Structure**: [CUSTOMIZE: AAA / Given-When-Then / Arrange-Act-Assert]

**Example**:
```[language]
[CUSTOMIZE: Show unit test pattern]
```

### Integration Tests

**Framework**: [CUSTOMIZE: Spring Test / Supertest / TestContainers / Django TestCase]

**Database**: [CUSTOMIZE: TestContainers / In-memory / Rollback / Fixtures]

**Example**:
```[language]
[CUSTOMIZE: Show integration test]
```

---

## API Documentation

### Format

**Approach**: [CUSTOMIZE: OpenAPI/Swagger / JSDoc / Docstrings / YARD / Inline comments]

### Mock Generation

**Location**: [CUSTOMIZE: api-mocks/ / mocks/ / fixtures/]

**Format**:
```json
[CUSTOMIZE: Show mock structure]
```

---

## Security Patterns

### Input Validation

**Where**: [CUSTOMIZE: Controller / DTO / Middleware / Before filter]

**How**: [CUSTOMIZE: Annotations / Decorators / Manual checks / Validators]

### SQL Injection Prevention

**Approach**: [CUSTOMIZE: Parameterized queries / ORM only / Prepared statements]

### Authentication

**Pattern**: [CUSTOMIZE: JWT / Session / OAuth / API Keys]

---

## Code Generation Checklist

When generating API code, always include:

- [ ] Controller with all endpoints (GET, POST, PUT, DELETE)
- [ ] Service layer with business logic
- [ ] Repository/Data access layer
- [ ] Entity/Model with proper fields
- [ ] Request DTOs with validation
- [ ] Response DTOs
- [ ] Custom exceptions for domain errors
- [ ] Global exception handler
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests (API endpoints)
- [ ] API mocks for frontend
- [ ] [PROJECT-SPECIFIC ITEM]

---

## Project-Specific Conventions

**[CUSTOMIZE - ADD PROJECT GOTCHAS AND PREFERENCES]**

### Naming Conventions
- [e.g., Controllers always plural: UsersController not UserController]
- [e.g., Services always singular: UserService]

### Code Review Requirements
- [e.g., All public methods must have JavaDoc]
- [e.g., Complex logic needs inline comments]

### Performance Considerations
- [e.g., Always paginate list endpoints]
- [e.g., Use database indexes on foreign keys]

---

**Customization Complete**: Replace all [CUSTOMIZE] sections with project-detected or chosen patterns.

**Auto-generated by**: `/add-skill api-implementation-patterns` command (with code analysis)
