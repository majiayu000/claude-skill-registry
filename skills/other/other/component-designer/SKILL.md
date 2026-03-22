---
name: component-designer
description: Use when designing a specific module component - creates architecture/component_name.md with purpose, interface, dependencies, and pattern references
version: 1.1.0
---

# Component Designer

Design individual components (services, forms, entities, plugins) and document them.

## Activation

Activate when you detect:
- "Design X component" or "Design the service"
- "Create spec for the form"
- Breaking down architecture into pieces
- Need detailed design for a single component

## Workflow

### 1. Identify Component Type

Ask if unclear:
```
What type of component is this?
1. Service (business logic)
2. Form (user input)
3. Entity (data storage)
4. Plugin (extensible behavior)
5. Controller (routing)
```

### 2. Gather Component Details

Ask based on type:

**For Services:**
```
1. What operations does this service perform?
2. What other services does it need?
3. Should it dispatch events?
```

**For Forms:**
```
1. What type? (ConfigFormBase, FormBase, ConfirmFormBase)
2. What fields are needed?
3. What validation?
4. What happens on submit?
```

**For Entities:**
```
1. Content entity or config entity?
2. What fields/properties?
3. What relationships to other entities?
4. Access control needs?
```

**For Plugins:**
```
1. What plugin type?
2. What does each plugin variation do?
3. What configuration does it need?
```

### 3. Find Pattern Reference

Use `core-pattern-finder` skill to locate a reference implementation in core.

### 4. Create Component Document

Use `Write` tool to create `{project_path}/architecture/{component_name}.md`:

```markdown
# Component: {ComponentName}

## Type
{Service | Form | Entity | Plugin | Controller}

## Purpose
{One paragraph from user input}

## Interface

### Public Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| methodName() | $param: Type | ReturnType | What it does |

### Events (if service)
| Event | When Dispatched |
|-------|-----------------|
| event.name | Condition |

## Dependencies

| Service | Purpose |
|---------|---------|
| entity_type.manager | {why needed} |

## Pattern Reference
Based on: `{path from core-pattern-finder}`

Apply from reference:
- {what to copy}

Adapt for our needs:
- {what to change}

## File Locations
- Class: `src/{Type}/{ComponentName}.php`
- Service definition: `my_module.services.yml`
- Routing: `my_module.routing.yml` (if controller)

## Acceptance Criteria
- [ ] {criterion 1}
- [ ] {criterion 2}
- [ ] {criterion 3}
```

### 5. Update Main Architecture

Use `Edit` tool to add component reference to `architecture/main.md`:

```markdown
## Components

### {ComponentName}
Type: {type}
Purpose: {one line}
Design: See `architecture/{component_name}.md`
```

### 6. Confirm

Show user:
```
Component designed: {ComponentName}

Files created:
- architecture/{component_name}.md

Based on core pattern:
- {pattern_reference}

Ready for implementation in Phase 3.
Review the design? (yes/no)
```

## Stop Points

STOP and wait for user:
- After asking component type
- After asking for details
- Before creating files
- After showing confirmation
