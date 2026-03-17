---
name: documentation-management
description: Keep project documentation accurate when behavior changes. EXCLUSIVE to project-manager agent.
allowed-tools: Read, Edit, Write, Grep
---
# Documentation Management

**Exclusive to:** `project-manager` agent

## Instructions

1. Identify what changed affecting docs
2. Update appropriate file(s) based on change type
3. Keep content concise and actionable
4. Verify README under 300 lines
5. Cross-check links and file paths

## Documentation Structure (Source of Truth)

```
docs/
├── project-overview-pdr.md   # Goals, features, requirements
├── codebase-summary.md       # Structure, models, routes, components
├── code-standards.md         # Conventions and patterns
└── system-architecture.md    # Design and data flow
```

Also: `README.md` (root) — Keep under 300 lines

## Update Triggers

| Change Type | Update |
|-------------|--------|
| New feature | `project-overview-pdr.md`, `codebase-summary.md` |
| New model/controller | `codebase-summary.md` |
| Pattern change | `code-standards.md` |
| Architecture change | `system-architecture.md` |
| Setup change | `README.md` |

## Update Process

1. Identify what changed affecting docs
2. Update appropriate file(s)
3. Keep content concise and actionable
4. Verify README under 300 lines

## Cross-Reference Validation

After updates, verify:
- [ ] Links still work
- [ ] File paths accurate
- [ ] Code examples current
- [ ] No contradictions between docs

## README Constraints

| Section | Max Lines |
|---------|-----------|
| Quick Start | 30 |
| Documentation links | 20 |
| Tech Stack | 15 |
| Commands | 20 |
| **Total** | < 300 |

## Examples
- "Update docs after adding a new model"
- "Document a new design pattern"
