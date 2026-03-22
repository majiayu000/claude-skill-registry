---
name: convert
description: (ePost) Use when user says "convert this prototype", "migrate this code", "make this match our design system", or "port from external source" — transforms external or prototype code into production-ready, system-consistent code
user-invocable: true
context: fork
agent: epost-fullstack-developer
metadata:
  argument-hint: "[path/to/prototype or repo URL]"
  connections:
    requires: [web-prototype]
---

# Convert Command

Convert external prototypes, mockups, or inconsistent code into production-ready code with your design system components and proper module structure.

## Usage

```
/convert /path/to/prototype
/convert https://github.com/user/prototype-repo
/convert ./my-mockup --module smart-send
```

## Your Process

1. **Scout** the prototype — read all components, styles, data sources
2. **Inventory** — list all components, their styles, and data patterns
3. **Map** each component to klara-theme equivalent using `prototype-conversion` skill
4. **Map** hardcoded styles to semantic token classes
5. **Map** mock data to real API patterns from `module-integration` skill
6. **Create** phased conversion plan
7. **Review** plan with user before implementing
8. **Implement** with proper klara-theme tokens, module structure, API binding

## Skills Activated

- `web-prototype-conversion` — Component and token mapping
- `web/module-integration` — API binding and module patterns
- `domain-b2b` — Target module knowledge
- `web-ui-lib` — klara-theme component reference
- `web-rag` — Search for existing implementations

## Quality Checks

- All hardcoded colors replaced with semantic tokens
- All components use your design system imports
- Module file structure follows `_components/`, `_hooks/`, `_services/` pattern
- Data flow follows Component -> Hook -> Action -> Service -> API
- TypeScript strict mode compliance
- Build successful
