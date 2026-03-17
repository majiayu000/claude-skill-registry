---
name: structurizr-architecture-sync
description: Maintain Structurizr C4 architecture diagrams in sync with code changes. Use when adding components, modifying relationships, changing architectural boundaries, or implementing new patterns. Ensures workspace.dsl accurately reflects the current system architecture.
---

# Structurizr Architecture Synchronization

## Context (Input)

Use this skill when:

- Adding new components (controllers, handlers, services, repositories)
- Creating new entities or aggregates
- Modifying component relationships or dependencies
- Implementing new architectural patterns (CQRS, events, subscribers)
- Adding infrastructure components (databases, caches, message brokers)
- Refactoring that changes component structure
- After fixing Deptrac violations (may indicate architecture drift)
- Creating new bounded contexts or modules
- Implementing new API endpoints with significant handlers

## Task (Function)

Keep the Structurizr workspace (`workspace.dsl`) synchronized with codebase changes, ensuring C4 model diagrams accurately represent the current system architecture.

**Success Criteria**:

- `workspace.dsl` contains all significant components
- Component relationships match actual code dependencies
- Layer groupings (Application/Domain/Infrastructure) are accurate
- Component descriptions reflect current purpose
- All infrastructure dependencies are documented
- C4 diagrams render without errors (check at `http://localhost:${STRUCTURIZR_PORT:-8080}`)

---

## Quick Start: Update Architecture in 5 Steps

> **Complete Template**: See [reference/workspace-template.md](reference/workspace-template.md) for full workspace.dsl structure.

### Step 1: Identify Architectural Changes

Determine if your code changes are architecturally significant:

**✅ DO update workspace.dsl when adding**:

- Processors (HTTP/GraphQL handlers)
- Command Handlers (CQRS pattern)
- Event Subscribers (event-driven patterns)
- Entities (core domain objects)
- Domain Events (significant business events)
- Repositories (data access)
- Event Bus or infrastructure services
- External dependencies (DB, Cache, Message Broker)

**❌ DON'T update for**:

- Factory classes
- Transformer classes (unless critical)
- Value objects (unless architecturally significant)
- Interface definitions (except hexagonal ports)
- Base classes
- DTOs and input/output objects
- Utility classes and helpers

**Target**: 15-25 components per diagram for clarity.

### Step 2: Add Component to Appropriate Group

Edit `workspace.dsl` and add component in the correct layer group:

```dsl
group "Application" {
    newProcessor = component "NewProcessor" "Handles new requests" "RequestProcessor" {
        tags "Item"
    }
}
```

**Layers**:

- `group "Application"` - Controllers, Processors, Handlers, Subscribers
- `group "Domain"` - Entities, Domain Events
- `group "Infrastructure"` - Repositories, Event Bus, Infrastructure services

**External dependencies** (database, cache, messageBroker) go OUTSIDE groups at container level.

**See**: [reference/dsl-syntax.md](reference/dsl-syntax.md) for complete syntax.

### Step 3: Define Relationships

Add relationships showing how your component interacts:

```dsl
// After all component definitions
newProcessor -> commandHandler "dispatches NewCommand"
commandHandler -> repository "uses"
repository -> database "accesses data"
```

**Common patterns**: See [reference/relationship-patterns.md](reference/relationship-patterns.md)

### Step 4: Verify Diagram Renders

View the updated diagram:

```bash
# Refresh browser (Structurizr Lite auto-reloads)
# Port is configurable via STRUCTURIZR_PORT in .env (default: 8080)
open http://localhost:${STRUCTURIZR_PORT:-8080}
# Navigate to "Diagrams" → "Components_All"
```

**Check for**:

- No syntax errors displayed
- New component appears
- Relationships are visible
- Component is in correct layer group

### Step 5: Position and Commit

1. **Drag components** in the UI to improve layout
2. **Click "Save workspace"** button (saves to `workspace.json`)
3. **Commit both files**:

```bash
git add workspace.dsl workspace.json
git commit -m "feat: update architecture with new processor"
```

---

## Diagram as Code Workflow

### Setup (Already Configured)

**Docker**: Structurizr Lite runs in `docker-compose.override.yml`:

```yaml
structurizr:
  image: structurizr/lite:2024.07.02
  ports:
    - '${STRUCTURIZR_PORT}:8080'
  volumes:
    - ./:/usr/local/structurizr
```

**Access**: `http://localhost:${STRUCTURIZR_PORT:-8080}` (port configurable via `.env`)

### Standard Development Flow

1. **Implement code changes** → Add handler, entity, repository
2. **Update workspace.dsl** → Add component + relationships
3. **View locally** → Refresh browser at configured port
4. **Position components** → Drag in UI, click "Save workspace"
5. **Commit together** → Code + workspace.dsl + workspace.json in same PR

### Manual Positioning in UI

**Automatic layout doesn't work well** - use manual positioning:

1. Open Structurizr UI in browser
2. Navigate to "Diagrams" → "Components_All"
3. Drag components to arrange (left-to-right flow recommended)
4. Click "Save workspace" button in top-right
5. Positions saved to `workspace.json` in project root
6. Commit `workspace.json` with `workspace.dsl`

**Layout best practices**:

- Processors/Controllers on the left (entry points)
- Command Handlers in the middle (business logic)
- Repositories to the right of handlers
- Database/Cache/Message Broker on far right (external)

**Common mistakes**: See [reference/common-mistakes.md](reference/common-mistakes.md) for complete guide.

---

## Reference Documentation

### Detailed Guides

- [C4 Model Fundamentals](reference/c4-model-guide.md) - Understanding C4 modeling
- [DSL Syntax Reference](reference/dsl-syntax.md) - Complete Structurizr DSL syntax
- [Component Identification](reference/component-identification.md) - What to document
- [Relationship Patterns](reference/relationship-patterns.md) - Common relationship types
- [Workspace Template](reference/workspace-template.md) - Complete workspace.dsl template
- [Common Mistakes](reference/common-mistakes.md) - Pitfalls and solutions

### Examples

- [Adding CQRS Pattern](examples/cqrs-pattern.md) - Command handlers, events, subscribers
- [Adding API Endpoint](examples/api-endpoint.md) - Controllers, processors, transformers
- [Adding Domain Entity](examples/domain-entity.md) - Entities, value objects, factories
- [Refactoring Components](examples/refactoring.md) - Updating relationships during refactoring

---

## Critical Principles

### What Makes a Good Architecture Diagram

**Clarity over Completeness**:

- 15-25 components (optimal readability)
- Focus on architectural significance
- Clear left-to-right or top-to-bottom flow
- External dependencies clearly visible

**Layer Separation**:

- Application: Entry points and orchestration
- Domain: Business logic and entities
- Infrastructure: Technical implementation

**Meaningful Relationships**:

- Show actual code dependencies
- Use descriptive labels
- Avoid circular dependencies

### Alignment with Deptrac

Layer groupings in workspace.dsl MUST match Deptrac configuration:

```dsl
group "Application"     ↔  Application layer in deptrac.yaml
group "Domain"          ↔  Domain layer in deptrac.yaml
group "Infrastructure"  ↔  Infrastructure layer in deptrac.yaml
```

This ensures architecture documentation matches enforced boundaries.

---

## Integration with Other Skills

Use this skill **after**:

- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) - After creating domain model
- [api-platform-crud](../api-platform-crud/SKILL.md) - After adding API endpoints
- [deptrac-fixer](../deptrac-fixer/SKILL.md) - After fixing layer violations

Use this skill **before**:

- [documentation-sync](../documentation-sync/SKILL.md) - Update docs with architecture
- [ci-workflow](../ci-workflow/SKILL.md) - Validate all changes

---

## Troubleshooting

### Common Issues

**Issue**: Structurizr UI shows "Element does not exist" error

**Solution**: Check component variable names in relationships match the component definitions exactly. See [common-mistakes.md](reference/common-mistakes.md#1-filtered-views-causing-element-does-not-exist-errors).

---

**Issue**: Diagram shows components in wrong positions after pull

**Solution**: Ensure `workspace.json` is committed along with `workspace.dsl`. The JSON file stores manual positions.

---

**Issue**: DSL syntax validation fails

**Solution**:

1. Check balanced braces `{}`
2. Verify all components are defined before relationships
3. Ensure no duplicate variable names
4. Compare with [workspace-template.md](reference/workspace-template.md)

---

**Issue**: Too many components (30+), diagram is cluttered

**Solution**: Follow [component-identification.md](reference/component-identification.md) - aim for 15-25 components. Omit DTOs, utilities, and factories.

---

**Issue**: Can't determine if component should be documented

**Solution**: Use the decision matrix in [component-identification.md](reference/component-identification.md#decision-matrix) or the TL;DR section.

## External Resources

- **Structurizr DSL Documentation**: <https://docs.structurizr.com/dsl>
- **C4 Model**: <https://c4model.com/>
- **Structurizr Lite**: <https://docs.structurizr.com/lite>
- **User Service Example** (VilnaCRM organization reference): <https://github.com/VilnaCRM-Org/user-service/wiki/Design-and-Architecture-Documentation>
