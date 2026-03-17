---
name: clean-code
description: Enforce SOLID, DRY, KISS principles during implementation.
  Auto-activated when writing or modifying code.
---

# Clean Code Skill

## Purpose
Ensure all code follows clean code principles.

## Core Principles

### SOLID
Reference: [principles/solid.md](principles/solid.md)

### DRY (Don't Repeat Yourself)
Reference: [principles/dry.md](principles/dry.md)
- Extract common logic to functions
- Use constants for magic values
- Create shared utilities

### KISS (Keep It Simple, Stupid)
Reference: [principles/kiss.md](principles/kiss.md)
- Favor readability over cleverness
- One thing per function
- Obvious over implicit

### YAGNI (You Aren't Gonna Need It)
Reference: [principles/yagni.md](principles/yagni.md)
- Implement only what's needed now
- No speculative generalization
- Add complexity when required

## Code Quality Checklist
Use before committing: [checklists/pre-commit.md](checklists/pre-commit.md)

### Naming
- [ ] Variables describe content
- [ ] Functions describe action
- [ ] Classes describe entity
- [ ] No abbreviations (except common ones)

### Functions
- [ ] Single responsibility
- [ ] < 20 lines preferred
- [ ] < 5 parameters
- [ ] No side effects where possible

### Comments
- [ ] Explain why, not what
- [ ] Update when code changes
- [ ] Remove commented-out code

### Error Handling
- [ ] Specific error types
- [ ] Meaningful messages
- [ ] Proper logging
- [ ] Recovery or fail gracefully

## Auto-Checks
When implementing, verify:
```bash
npm run lint
npm run typecheck
```
