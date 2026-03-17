---
name: si
description: "Short alias for /subsection-implementation. Implements a single subsection from docs/implementation-plan.md with full automation. Usage: /si 5.1.1"
license: MIT
metadata:
  version: "1.0.0"
  alias_for: "subsection-implementation"
---

# Subsection Implementation (Short Alias)

**This is a short alias for `/subsection-implementation`**

## Usage

```
/si 5.1.1
```

Equivalent to:
```
/subsection-implementation 5.1.1
```

## What It Does

Implements a complete subsection from `docs/implementation-plan.md` with full automation:

1. Clear context (fresh start)
2. Read subsection requirements
3. Create task tracking
4. Implement code (follow project patterns)
5. Write tests (all subsection tests)
6. Run quality checks (must pass!)
7. Update documentation (mark ✅)
8. Commit and push (proper format)

## Examples

```
/si 5.1.1                           # Implement subsection 5.1.1
/si 5.1.1 --branch feature/scout    # On specific branch
/si 5.1.1 --dry-run                 # Show plan without executing
```

## Full Documentation

For complete workflow details, see:
- **Main skill**: `@skills/subsection-implementation/SKILL.md`
- **All skills**: `@skills/README.md`
- **Implementation plan**: `docs/implementation-plan.md`
