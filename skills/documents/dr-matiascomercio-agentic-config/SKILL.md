---
name: dr
description: 'Alias skill that invokes /dry-run with all arguments passed through.
  Provides shorthand for dry-run mode. Triggers on keywords: dr, dry run shorthand,
  alias'
---

---
name: dr
description: Alias skill that invokes /dry-run with all arguments passed through. Provides shorthand for dry-run mode. Triggers on keywords: dr, dry run shorthand, alias
project-agnostic: true
allowed-tools: []
---

# DR Alias Skill

Simple alias that delegates to `/dry-run` with all arguments.

## Usage

```
/dr <any command or prompt>
```

## Behavior

Executes `/dry-run` with all arguments passed through unchanged:

- `/dr /po_spec path/to/spec.md` → `/dry-run /po_spec path/to/spec.md`
- `/dr /spec IMPLEMENT path/to/spec.md` → `/dry-run /spec IMPLEMENT path/to/spec.md`
- `/dr <question>` → `/dry-run <question>`

## Implementation

Execute: `/dry-run $ARGUMENTS`
