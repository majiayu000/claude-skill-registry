---
name: expertise-file-design
description: Design YAML expertise file structures for agent experts. Use when creating mental models for domain-specific agents, defining expertise schema, or structuring knowledge for Act-Learn-Reuse workflows.
allowed-tools: Read, Grep, Glob, Write
---

# Expertise File Design

Guide for designing YAML expertise files that serve as mental models for agent experts.

## MANDATORY: Act-Learn-Reuse Context

Expertise files are **mental models**, NOT sources of truth. They:

- Accelerate agent execution by pre-loading domain knowledge
- Are maintained by self-improve prompts, not humans
- Validate against the actual codebase (source of truth)
- Have enforced line limits to protect context windows

## When to Use

- Creating mental models for new domain-specific agents
- Defining expertise schema structures (YAML)
- Structuring knowledge for Act-Learn-Reuse workflows
- Reviewing or auditing existing expertise file designs
- Setting up line limits and section priorities

## Expertise File Structure

### Core Template

```yaml
# {domain}/expertise.yaml
# Mental model for {domain} agent expert
# Last updated: {timestamp}
# Lines: {current}/{max}

overview:
  description: "Brief description of this domain"
  primary_technology: "Main tech/framework"
  architecture_pattern: "Key pattern used"

core_implementation:
  main_module:
    file: "path/to/main/file.ext"
    lines: approximate_line_count
    purpose: "What this module does"
    key_exports:
      - name: "FunctionOrClass"
        type: "function|class|constant"
        purpose: "Brief description"

  supporting_modules:
    - file: "path/to/support.ext"
      purpose: "Supporting functionality"

schema_structure:  # For database/API domains
  entities:
    entity_name:
      fields:
        - name: "field_name"
          type: "data_type"
          constraints: "nullable, unique, etc."
      relationships:
        - target: "other_entity"
          type: "one-to-many|many-to-many"

key_operations:
  operation_category:
    operation_name:
      function: "function_name"
      file: "path/to/file.ext"
      signature: "func(param: Type) -> ReturnType"
      logic: "Brief description of what it does"
      edge_cases:
        - "Important edge case 1"
        - "Important edge case 2"

patterns_and_conventions:
  naming:
    - "Convention description"
  error_handling:
    - "How errors are handled"
  data_flow:
    - "How data moves through system"

best_practices:
  - "Practice 1: Explanation"
  - "Practice 2: Explanation"

known_issues:
  - issue: "Issue description"
    workaround: "How to handle it"
    status: "open|resolved|wontfix"

integration_points:
  - system: "External system name"
    method: "How integration works"
    considerations: "Important notes"

testing_notes:
  - "How to test this domain"
  - "Key test scenarios"
```

## Line Limits

| Domain Complexity | Max Lines | Guidance |
| --- | --- | --- |
| Small/Focused | 300 | Single module, simple operations |
| Medium | 500-600 | Multiple modules, moderate complexity |
| Large/Complex | 800-1000 | Full subsystem, many operations |
| **Absolute Max** | 1000 | Never exceed - split into sub-experts |

## Section Priority

When approaching line limits, prioritize sections in this order:

1. **core_implementation** - Essential for navigation
2. **key_operations** - Critical for task execution
3. **best_practices** - Prevents mistakes
4. **known_issues** - Avoids wasted effort
5. **patterns_and_conventions** - Nice to have
6. **testing_notes** - Can reference external docs

## Domain-Specific Templates

### Database Domain

```yaml
overview:
  database_system: "PostgreSQL|MySQL|MongoDB|etc"
  orm_pattern: "Raw SQL|ORM name|Query builder"
  connection_strategy: "Pooling|Single|Per-request"

schema_structure:
  tables:
    table_name:
      purpose: "What this table stores"
      primary_key: "id (UUID|INT)"
      fields: [...]
      indexes: [...]
      foreign_keys: [...]

key_operations:
  crud:
    create: {function: "", file: "", logic: ""}
    read: {function: "", file: "", logic: ""}
    update: {function: "", file: "", logic: ""}
    delete: {function: "", file: "", logic: ""}

  specialized:
    bulk_insert: {...}
    transaction_handling: {...}
```

### API/Service Domain

```yaml
overview:
  api_style: "REST|GraphQL|gRPC"
  auth_method: "JWT|OAuth|API Key"
  versioning: "URL|Header|None"

endpoints:
  resource_name:
    base_path: "/api/v1/resource"
    operations:
      list: {method: "GET", auth: "required", pagination: "cursor"}
      create: {method: "POST", auth: "required", validation: "..."}

request_response_patterns:
  success_format: {...}
  error_format: {...}
```

### Frontend/UI Domain

```yaml
overview:
  framework: "React|Vue|Angular|etc"
  state_management: "Redux|Zustand|Context|etc"
  styling: "CSS Modules|Tailwind|Styled Components"

component_hierarchy:
  pages:
    - name: "PageName"
      route: "/path"
      children: [...]

  shared:
    - name: "ComponentName"
      purpose: "Reusable for X"

state_structure:
  stores:
    store_name:
      shape: {...}
      actions: [...]
```

## Seeding Strategy

When creating a new expertise file:

1. **Start minimal** - Begin with overview and core_implementation only
2. **Let agent discover** - Run self-improve to populate
3. **Iterate** - Run self-improve until stable (no changes)
4. **Review** - Human validates accuracy
5. **Maintain** - Self-improve after every ACT

## Anti-Patterns

| Pattern | Problem | Solution |
| --- | --- | --- |
| Copy-pasting docs | Duplicates source of truth | Reference files, don't copy |
| Including code | Bloats file, goes stale | Reference by function name |
| No line limits | Context window overflow | Enforce max lines strictly |
| Manual updates | Human time wasted | Self-improve prompt only |
| Flat structure | Hard to navigate | Use nested YAML sections |

## Validation Checklist

Before considering an expertise file complete:

- [ ] Valid YAML syntax (no parse errors)
- [ ] Under line limit for domain complexity
- [ ] All file paths verified to exist
- [ ] All function names verified accurate
- [ ] Overview section complete
- [ ] Key operations documented
- [ ] Best practices included
- [ ] Known issues captured

## Related Skills

- `agent-expert-creation`: Full agent expert workflow
- `self-improve-prompt-design`: Maintaining expertise accuracy
- `meta-agentic-creation`: Building experts that build experts

---

**Last Updated:** 2025-12-15

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
