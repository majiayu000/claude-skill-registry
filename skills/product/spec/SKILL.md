---
name: spec
description: Specification management - creating, organizing, and maintaining spec items with acceptance criteria and traits.
---

# Spec - Specification Management

Specifications define WHAT to build. Tasks track the WORK of building it. This skill covers creating and managing spec items, writing acceptance criteria, and using traits for cross-cutting behaviors.

## Quick Start

```bash
# Explore what exists
kspec item list                      # List all spec items
kspec item types                     # Available item types
kspec trait list                     # Available traits

# Create a spec item
kspec item add --under @parent --title "Feature Name" --type feature --slug my-feature

# Add acceptance criteria
kspec item ac add @my-feature --given "precondition" --when "action" --then "result"

# Apply a trait (if project has traits)
kspec item trait add @my-feature @some-trait

# Validate spec quality
kspec validate
```

## When to Use This Skill

Use `/spec` when you need to:
- Create or update spec items (features, requirements, etc.)
- Write or refine acceptance criteria
- Apply traits to specs
- Understand spec hierarchy and organization
- Validate spec quality

**Not for task management** - use `/kspec` for task workflows.

## Core Concepts

### Item Types

Specs are organized in a hierarchy of typed items:

| Type | Purpose |
|------|---------|
| module | High-level organizational grouping |
| feature | User-facing capability |
| requirement | Specific testable behavior |
| constraint | Limitation or boundary |
| decision | Architectural choice (ADR-style) |
| trait | Reusable AC bundle |

See [docs/item-types.md](docs/item-types.md) for detailed guidance on when to use each type.

### Acceptance Criteria

AC define testable outcomes using Given/When/Then format:

```yaml
given: a registered user
when: they enter valid credentials
then: they are logged in and see their dashboard
```

See [docs/acceptance-criteria.md](docs/acceptance-criteria.md) for writing guidelines.

### Traits

Traits are reusable bundles of acceptance criteria for cross-cutting concerns (e.g., JSON output, confirmation prompts). When a spec implements a trait, it inherits the trait's AC.

```bash
# Discover available traits
kspec trait list

# Apply trait to spec
kspec item trait add @my-command @trait-json-output
```

See [docs/traits.md](docs/traits.md) for the full trait system guide.

## Command Reference

### Item Commands

```bash
# View items
kspec item get <ref>                 # Get item details
kspec item list [--type <type>]      # List items, optionally filtered
kspec item types                     # List available types

# Create items
kspec item add --under <parent> --title "..." --type <type> [--slug <slug>]

# Update items
kspec item set <ref> --title "..."   # Update specific fields
kspec item set <ref> --description "..."
kspec item set <ref> --status <implementation-status>
kspec item patch <ref> --data '{...}'  # Complex updates

# Delete items
kspec item delete <ref> [--force]
```

### Acceptance Criteria Commands

```bash
# View AC
kspec item ac list <ref>             # List AC for an item

# Add AC
kspec item ac add <ref> --given "..." --when "..." --then "..."

# Update AC
kspec item ac set <ref> <ac-id> --then "updated result"

# Remove AC
kspec item ac remove <ref> <ac-id> [--force]
```

### Trait Commands

```bash
# Discover traits
kspec trait list                     # All traits with AC counts
kspec trait get <ref>                # Trait details including AC

# Apply/remove traits from specs
kspec item trait add <spec-ref> <trait-ref>
kspec item trait remove <spec-ref> <trait-ref>

# Create new traits (when needed)
kspec trait add "Trait Name" --description "..." [--slug <slug>]
```

### Validation

```bash
kspec validate                       # Check spec quality
```

Validation reports:
- Missing acceptance criteria
- Broken references
- Missing descriptions
- Orphaned specs (no linked tasks)

## Workflow Patterns

### Creating a New Feature

```bash
# 1. Find the appropriate parent
kspec item list --type module

# 2. Create the feature
kspec item add --under @cli-module --title "JSON Export" --type feature --slug json-export

# 3. Add description
kspec item set @json-export --description "Export data in JSON format for integration with other tools"

# 4. Add acceptance criteria
kspec item ac add @json-export --given "data exists" --when "user runs export --json" --then "valid JSON is written to stdout"
kspec item ac add @json-export --given "no data" --when "user runs export --json" --then "empty array [] is returned"

# 5. Apply relevant traits
kspec item trait add @json-export @trait-json-output

# 6. Validate
kspec validate

# 7. Derive task when ready to implement
kspec derive @json-export
```

### Updating Existing Specs

```bash
# Get current state
kspec item get @existing-feature

# Update fields
kspec item set @existing-feature --description "Updated description"

# Add missing AC
kspec item ac add @existing-feature --given "..." --when "..." --then "..."

# Update implementation status
kspec item set @existing-feature --status implemented
```

### Validating Spec Quality

```bash
# Run validation
kspec validate

# Address issues:
# - Add AC to items without them
# - Fix broken references
# - Add descriptions to items
```

## Key Principles

1. **Spec before task** - Define what to build before tracking the work
2. **AC is required** - Specs without acceptance criteria are incomplete
3. **Use CLI, not YAML** - Commands maintain consistency and auto-commit
4. **Validate regularly** - Run `kspec validate` to catch issues early
5. **Traits for patterns** - If 3+ specs need the same behavior, consider a trait

## Related Skills

- `/kspec` - Task and spec management (primary workflow)
- `/spec-plan` - Translating approved plans to specs
- `/triage` - Processing inbox using spec-first approach
