---
name: aurora-context-generator
description: >
  Generates CONTEXT.md documentation for bounded contexts by exploring existing
  code and YAML definitions. Trigger: When user asks to document a bounded
  context, generate CONTEXT.md, or analyze a domain.
license: MIT
metadata:
  author: aurora
  version: '1.0'
  auto_invoke: 'Generate CONTEXT.md, document bounded context, analyze domain'
allowed-tools: Read, Write, Glob, Grep, Task, AskUserQuestion
---

## When to Use

- User wants to generate/update CONTEXT.md for a bounded context
- User needs to document an existing domain based on code
- Analyzing a bounded context structure

## Critical Patterns

### 1. Exploration First

Before generating, ALWAYS explore the bounded context:

```
1. Find all .aurora.yaml files in cliter/{context}/
2. Read each YAML to extract modules, fields, relationships
3. Explore src/@api/{context}/ for resolvers, controllers, DTOs
4. Explore src/@apps/{context}/ for handlers, services, domain logic
5. Identify business rules from code patterns (guards, validators, handlers)
```

### 2. Information Sources

| Source                                  | What to Extract                            |
| --------------------------------------- | ------------------------------------------ |
| `cliter/{context}/*.aurora.yaml`        | Modules, fields, relationships, aggregates |
| `src/@api/{context}/`                   | API endpoints, resolvers, DTOs             |
| `src/@apps/{context}/*/application/`    | Commands, queries, handlers, use cases     |
| `src/@apps/{context}/*/domain/`         | Value objects, entities, business rules    |
| `src/@apps/{context}/*/infrastructure/` | Repositories, external integrations        |

### 3. Module Discovery from YAML

Read `.aurora.yaml` files and extract:

```yaml
# From the YAML, extract:
boundedContextName: business-partner-portal # Context name
moduleName: partner # Module name
moduleNames: partners # Plural
aggregateName: Partner # Aggregate

# From properties, infer:
# - Field types and relationships
# - Required fields (business rules)
# - Indexes (query patterns)
```

### 4. Business Rules Discovery

Look for patterns in code:

| Code Pattern           | Business Rule Type    |
| ---------------------- | --------------------- |
| `@Guards()` decorators | Access control rules  |
| Validators in handlers | Data validation rules |
| `if/throw` in domain   | Domain invariants     |
| Value Objects          | Data constraints      |
| Saga/Events            | Process rules         |

## Generation Process

1. **Receive bounded context name** from user
2. **Explore code structure**:

   ```bash
   # Find all YAML definitions
   glob: cliter/{context}/*.aurora.yaml

   # Find application handlers
   glob: src/@apps/{context}/**/handlers/**/*.handler.ts

   # Find domain entities and value objects
   glob: src/@apps/{context}/**/domain/**/*.ts
   ```

3. **Read and analyze** each found file
4. **Extract information**:
   - Modules from YAML files
   - Business flows from handlers (commands/queries)
   - Business rules from validators and guards
   - Dependencies from imports
5. **Generate CONTEXT.md** with discovered information
6. **Write to** `cliter/{context}/CONTEXT.md`

## Output Structure

```markdown
# {Bounded Context Name}

## Purpose

{Inferred from module descriptions and aggregate names}

## Modules

| Module   | Responsibility                       |
| -------- | ------------------------------------ |
| {module} | {Inferred from aggregate and fields} |

## Key Business Rules

{Extracted from code analysis}

- Rule from guards/validators
- Rule from domain invariants
- Rule from value object constraints

## Main Flows

{Extracted from command/query handlers}

1. **{CommandName}**: {Description from handler}
2. **{QueryName}**: {Description from handler}

## Dependencies

- **Uses**: {From imports analysis}
- **Used by**: {From reverse dependency search}

## Technical Notes

- Aggregate roots identified
- Event patterns found
- Integration points discovered
```

## Example Exploration

For `business-partner-portal`:

```bash
# Step 1: Find YAMLs
glob: cliter/business-partner-portal/*.aurora.yaml

# Step 2: Read each YAML
read: cliter/business-partner-portal/partner.aurora.yaml

# Step 3: Find handlers
glob: src/@apps/business-partner-portal/**/handlers/**/*.ts

# Step 4: Find domain logic
glob: src/@apps/business-partner-portal/**/domain/**/*.ts

# Step 5: Analyze imports for dependencies
grep: "from '@api/" in src/@apps/business-partner-portal/
```

## Commands

```bash
# Explore bounded context structure
eza -T cliter/{context}/
eza -T src/@apps/{context}/

# Find all modules
fd ".aurora.yaml" cliter/{context}/

# Find all handlers
fd "handler.ts" src/@apps/{context}/
```

## User Interaction

If code exploration reveals ambiguity, ask user:

1. **Purpose clarification**: "Based on the modules found ({list}), is this
   context about {inferred purpose}?"
2. **Missing information**: "I couldn't find business rules in code. Can you
   describe the key constraints?"
3. **Dependencies**: "I found imports from {contexts}. Are there other
   dependencies?"

## Resources

- **Template**: See [assets/CONTEXT-template.md](assets/CONTEXT-template.md)
