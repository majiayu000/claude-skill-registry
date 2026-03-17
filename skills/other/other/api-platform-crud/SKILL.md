---
name: api-platform-crud
description: Create complete REST API CRUD operations using API Platform 4 with DDD and CQRS patterns. Use when adding new API resources, implementing CRUD endpoints, creating DTOs, configuring operations, or setting up state processors. Follows the repository's hexagonal architecture with YAML resource configuration and command bus pattern.
---

# API Platform CRUD Skill

## Context (Input)

- Need to create new API resource with REST endpoints
- Implementing CRUD operations (Create, Read, Update, Delete)
- Adding DTOs for input/output transformation
- Configuring API Platform operations, filters, or pagination
- Working with state processors following CQRS pattern

## Task (Function)

Implement production-ready REST API CRUD operations following DDD, CQRS, and hexagonal architecture patterns.

**Success Criteria**:

- All CRUD operations functional (POST, GET, PUT, PATCH, DELETE)
- DTOs properly validated
- Domain entities remain framework-agnostic
- Command bus pattern used for write operations
- `make ci` outputs "✅ CI checks successfully passed!"

> Template examples reference MongoDB/Doctrine ODM. In this service, use Doctrine ORM with MySQL (`.orm.xml` mappings, `EntityManagerInterface`) while keeping the same layering and DTO/processor patterns.

---

## Quick Start: Complete CRUD in 10 Steps

> **Full Implementation Example**: See [examples/complete-customer-crud.md](examples/complete-customer-crud.md) for detailed code.

### Step 1: Create Domain Entity

Create pure PHP entity in `src/Core/{Context}/Domain/Entity/{Entity}.php`

- ❌ NO Doctrine annotations/attributes
- ❌ NO Symfony imports
- ❌ NO API Platform attributes
- ✅ Pure business logic only

### Step 2: Create Doctrine XML Mapping

Create `config/doctrine/{Entity}.mongodb.xml` with field mappings and indexes.

**See**: [database-migrations](../database-migrations/SKILL.md) skill for XML mapping patterns.

### Step 3: Create Input DTOs

Create three DTOs in `src/Core/{Context}/Application/DTO/`:

- `{Entity}Create` - For POST requests
- `{Entity}Put` - For PUT requests (full update)
- `{Entity}Patch` - For PATCH requests (partial update)

**See**: [reference/dto-validation-patterns.md](reference/dto-validation-patterns.md)

### Step 4: Configure Validation

Create `config/validator/{Entity}.yaml` with validation rules for each DTO.

### Step 5: Create API Platform Resource Configuration

Create `config/api_platform/resources/{entity}.yaml`:

```yaml
App\Core\{Context}\Domain\Entity\{Entity}:
  shortName: { Entity }
  operations:
    ApiPlatform\Metadata\GetCollection: ~
    ApiPlatform\Metadata\Get: ~
    ApiPlatform\Metadata\Post:
      input: App\Core\{Context}\Application\DTO\{Entity}Create
      processor: App\Core\{Context}\Application\Processor\Create{Entity}Processor
    ApiPlatform\Metadata\Put:
      input: App\Core\{Context}\Application\DTO\{Entity}Put
      processor: App\Core\{Context}\Application\Processor\Update{Entity}Processor
    ApiPlatform\Metadata\Patch:
      input: App\Core\{Context}\Application\DTO\{Entity}Patch
      processor: App\Core\{Context}\Application\Processor\Patch{Entity}Processor
    ApiPlatform\Metadata\Delete: ~
```

**See**: [reference/configuration-patterns.md](reference/configuration-patterns.md) for detailed patterns.

### Step 6: Configure Serialization Groups

Create `config/serialization/{Entity}.yaml` to control which fields are exposed.

### Step 7: Create State Processors

Create processors in `src/Core/{Context}/Application/Processor/`:

- `Create{Entity}Processor` - Handles POST
- `Update{Entity}Processor` - Handles PUT
- `Patch{Entity}Processor` - Handles PATCH

Each processor:

1. Receives DTO
2. Transforms to Command
3. Dispatches via Command Bus
4. Returns resulting Entity

### Step 8: Create Command and Handler

Create:

- Command in `Application/Command/{Action}{Entity}Command.php`
- Handler in `Application/CommandHandler/{Action}{Entity}CommandHandler.php`

Handler contains business logic and calls repository.

**See**: [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) for CQRS patterns.

### Step 9: Create Repository

Create:

- Interface in `Domain/Repository/{Entity}RepositoryInterface.php`
- Implementation in `Infrastructure/Repository/{Entity}Repository.php`
- Register in `config/services.yaml`

**See**: [database-migrations](../database-migrations/SKILL.md) skill for repository patterns.

### Step 10: Configure Filters (Optional)

Add filters in `config/services.yaml` for search, ordering, etc.

**See**: [reference/filters-and-pagination.md](reference/filters-and-pagination.md)

---

## Architecture Flow

```
REST Request → API Platform
            ↓
        Processor (Application)
            ↓
        DTO → Transformer → Command
            ↓
        Command Bus
            ↓
        Handler (Application)
            ↓
        Entity (Domain) ← Repository (Infrastructure)
            ↓
        MongoDB
```

**See**: [reference/configuration-patterns.md](reference/configuration-patterns.md) for detailed architecture.

---

## Constraints (Parameters)

### NEVER

- Add framework annotations/attributes to Domain entities
- Put business logic in Processors (use Handlers)
- Skip validation configuration
- Use PHP attributes for API Platform config (use YAML)
- Violate layer boundaries (check with `make deptrac`)
- Skip DTO transformation (direct Entity manipulation)

### ALWAYS

- Keep Domain entities framework-agnostic
- Use YAML for all configuration (validation, serialization, resources)
- Dispatch Commands via Command Bus for write operations
- Create separate DTOs for Create, Put, and Patch
- Follow IRI pattern for entity references
- Run `make ci` before committing

---

## Format (Output)

### Expected API Endpoints

```
GET    /api/{entities}           # List all
GET    /api/{entities}/{id}      # Get one
POST   /api/{entities}           # Create
PUT    /api/{entities}/{id}      # Full update
PATCH  /api/{entities}/{id}      # Partial update
DELETE /api/{entities}/{id}      # Delete
```

### Expected OpenAPI Spec

```bash
make generate-openapi-spec
# Generates .github/openapi-spec/spec.yaml
```

### Expected CI Result

```
✅ CI checks successfully passed!
```

---

## Verification Checklist

After implementation:

- [ ] Domain entity created (no framework imports)
- [ ] Doctrine XML mapping configured
- [ ] Three DTOs created (Create, Put, Patch)
- [ ] Validation rules configured in YAML
- [ ] API Platform resource YAML created
- [ ] Serialization groups configured
- [ ] State Processors created for write operations
- [ ] Commands and Handlers implemented
- [ ] Repository interface and implementation created
- [ ] Filters configured (if needed)
- [ ] Resource directory registered in `api_platform.yaml`
- [ ] All endpoints respond correctly (test with Postman/Behat)
- [ ] Validation works (test invalid inputs)
- [ ] `make deptrac` passes (no violations)
- [ ] `make ci` passes (all checks green)
- [ ] OpenAPI spec generated successfully

---

## Related Skills

- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) - DDD patterns and CQRS
- [deptrac-fixer](../deptrac-fixer/SKILL.md) - Fix architectural violations
- [database-migrations](../database-migrations/SKILL.md) - MongoDB entity management
- [openapi-development](../openapi-development/SKILL.md) - OpenAPI documentation
- [testing-workflow](../testing-workflow/SKILL.md) - Write E2E tests for endpoints

---

## Quick Commands

```bash
# Clear cache after config changes
make cache-clear

# Generate OpenAPI spec
make generate-openapi-spec

# Validate architecture
make deptrac

# Run E2E tests
make behat

# Full CI check
make ci
```

---

## Reference Documentation

For detailed patterns and examples:

- **[Configuration Patterns](reference/configuration-patterns.md)** - YAML config, operations, pagination, IRI resolution
- **[DTO & Validation Patterns](reference/dto-validation-patterns.md)** - DTO design, validation rules, exception handling
- **[Filters & Pagination](reference/filters-and-pagination.md)** - Search filters, sorting, pagination config
- **[Troubleshooting](reference/troubleshooting.md)** - Common issues and solutions
- **[Complete Example](examples/complete-customer-crud.md)** - Full Customer CRUD implementation

---

## Template Syntax

Throughout documentation, placeholders follow these conventions:

| Placeholder  | Example            | Usage                         |
| ------------ | ------------------ | ----------------------------- |
| `{Entity}`   | `Customer`         | PascalCase class name         |
| `{Context}`  | `Customer`         | Bounded context/module name   |
| `{entity}`   | `customer`         | Lowercase for configs/filters |
| `{entities}` | `customers`        | Plural for collection names   |
| `{Action}`   | `Create`, `Update` | Command action verb           |
