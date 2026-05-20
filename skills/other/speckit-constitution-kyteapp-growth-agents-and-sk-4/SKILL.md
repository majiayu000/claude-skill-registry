---
name: speckit-constitution
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync
---

# Speckit-Constitution: Project Principles Management

## Purpose

Create or update the project constitution - a set of non-negotiable principles and standards that govern all specifications, plans, and implementations in the project.

## What is a Constitution?

The constitution (`specify/memory/constitution.md`) defines:
- **MUST principles:** Non-negotiable requirements (always enforced)
- **SHOULD principles:** Strong recommendations (justify if violated)
- **Project standards:** Coding style, architecture patterns, quality gates
- **Technical constraints:** Required/forbidden technologies
- **Quality gates:** Review requirements, testing standards, documentation needs

## Prerequisites

- Project repository initialized
- `.specify/` directory structure (created by setup scripts)

## What This Skill Does

1. Loads existing constitution (if exists)
2. Gathers principle inputs from user interactively
3. Creates/updates constitution document
4. Ensures all dependent templates stay in sync
5. Validates principle consistency
6. Reports changes made

## Key Principles

### Constitution Authority

- **Non-negotiable within scope:** All specs and plans must comply
- **Explicit violations:** Must be justified in writing
- **Cannot be silently ignored:** Tools check compliance automatically
- **Change via update:** Modify constitution, don't violate it

### Template Synchronization

When constitution updates:
- Spec template updates to reflect new quality gates
- Plan template updates to enforce new technical constraints
- Task template updates to include new validation steps
- Checklist templates update to check new principles

## Template Location

**IMPORTANT:** The constitution template is located at:
`.github/skills/speckit-constitution/constitution-template.md`

This template MUST be loaded and used as the base structure for all constitution creation/updates.

## Execution Flow

All execution logic is now contained within this skill. The skill handles:
- Constitution loading/creation
- Principle gathering
- Template synchronization

### Quick Summary

1. **Load template** from `.github/skills/speckit-constitution/constitution-template.md`
2. **Load existing constitution** (if exists) from `.specify/memory/constitution.md`
3. **Gather inputs:**
   - User-provided principles
   - Interactive questions if needed
   - Technical constraints
   - Quality standards
4. **Create/update constitution:**
   - Fill template with gathered information
   - Organize principles by category
   - Mark MUST vs SHOULD
   - Document rationale
5. **Sync dependent templates:**
   - Update spec template
   - Update plan template
   - Update task template
   - Update checklist templates
6. **Report changes:** List new/modified principles

## Constitution Structure

### Recommended Sections

```markdown
# Project Constitution

## Core Principles

### Architecture
- [MUST] Use microservices pattern for backend services
- [SHOULD] Prefer REST over GraphQL for public APIs

### Security
- [MUST] All data encrypted at rest and in transit
- [MUST] Authentication required for all protected resources
- [SHOULD] Use OAuth2 for third-party integrations

### Quality
- [MUST] All code must pass linting before commit
- [MUST] Test coverage ≥80% for all new code
- [SHOULD] Performance budgets defined for critical paths

### Technology Constraints
- [MUST] Use TypeScript (no JavaScript)
- [MUST] PostgreSQL for relational data
- [FORBIDDEN] MongoDB, MySQL (use PostgreSQL instead)

### Documentation
- [MUST] All public APIs have OpenAPI specs
- [SHOULD] All components have README files
- [SHOULD] Architecture decisions recorded in ADRs

## Quality Gates

### Specification Phase
- [ ] No implementation details in spec.md
- [ ] All success criteria measurable
- [ ] All user stories have acceptance criteria

### Planning Phase
- [ ] All design decisions documented in research.md
- [ ] Constitution compliance validated
- [ ] Data model complete

### Implementation Phase
- [ ] All tests pass
- [ ] Linting clean
- [ ] Code review approved
```

## Common Constitution Topics

### Architecture Patterns
- Microservices vs monolith
- Layered architecture requirements
- Dependency injection patterns
- Event-driven vs request/response

### Security Standards
- Authentication mechanisms
- Authorization patterns
- Data encryption requirements
- Secret management

### Quality Standards
- Test coverage requirements
- Code review policies
- Documentation standards
- Performance budgets

### Technology Stack
- Required languages/frameworks
- Approved libraries
- Forbidden technologies
- Version constraints

### Development Process
- Branching strategy
- Commit message format
- PR requirements
- Release process

## Interactive Constitution Creation

If user doesn't provide full constitution, ask:

1. **Architecture:** "What architectural patterns are required?" (microservices, monolith, serverless, etc.)
2. **Security:** "What security requirements are non-negotiable?" (encryption, auth, compliance, etc.)
3. **Quality:** "What quality gates must pass?" (tests, coverage, reviews, etc.)
4. **Technology:** "Are there required or forbidden technologies?" (languages, frameworks, databases, etc.)
5. **Process:** "What development processes are mandatory?" (reviews, docs, versioning, etc.)

Provide options with recommendations for each.

## Success Indicators

Constitution is ready when:
- ✅ Principles clearly marked as MUST or SHOULD
- ✅ Rationale provided for critical constraints
- ✅ Quality gates explicitly defined
- ✅ Technology constraints documented
- ✅ All dependent templates synced
- ✅ No contradictory principles
- ✅ Enforcement mechanism clear

## Output

```
.specify/memory/
└── constitution.md            # Project constitution

Updated templates:
- .specify/templates/spec-template.md
- .specify/templates/plan-template.md
- .specify/templates/tasks-template.md
- .specify/templates/checklist-template.md
```

## Constitution Enforcement

### During Specification
- Spec template includes constitution-mandated sections
- Quality checklist validates constitution compliance
- No forbidden technologies mentioned

### During Planning
- Plan template includes Constitution Check section
- All MUST principles validated
- Violations require written justification
- Research.md references constitution decisions

### During Implementation
- Task template includes constitution validation steps
- Pre-commit hooks enforce code standards
- CI/CD validates quality gates
- Reviews check compliance

## Common Mistakes

### ❌ Too Many MUST Principles
**Wrong:** 50 MUST requirements (impossible to enforce)
**Right:** 5-10 critical MUST requirements, rest are SHOULD

### ❌ Vague Principles
**Wrong:** "Code should be clean and maintainable"
**Right:** "All functions <50 lines, test coverage ≥80%, ESLint clean"

### ❌ No Rationale
**Wrong:** "MUST use PostgreSQL" (why?)
**Right:** "MUST use PostgreSQL (team expertise, ACID guarantees required, proven scale)"

### ❌ Contradictory Principles
**Wrong:** "MUST use microservices" + "MUST deploy as single binary"
**Right:** Resolve contradiction before finalizing

### ❌ Unenforced Principles
**Wrong:** Constitution exists but never checked
**Right:** All tools validate constitution compliance automatically

## Example Constitution

```markdown
# Kyte Clinics Constitution

## Architecture Principles

- [MUST] Use multi-agent system with OpenAI Agents SDK
- [MUST] Follow Composition Root dependency injection pattern
- [SHOULD] Prefer deterministic flows (low temperature) for sales agents

## Security Principles

- [MUST] Never expose wid, aid, uid to external systems
- [MUST] All secrets in environment variables, never committed
- [MUST] Authentication required for all WhatsApp interactions

## Quality Principles

- [MUST] All code passes `npm test` before commit
- [MUST] All code passes `npm run lint` before commit
- [SHOULD] Test coverage ≥80% for critical paths

## Technology Constraints

- [MUST] TypeScript (no JavaScript)
- [MUST] MongoDB for persistence
- [MUST] OpenAI Agents SDK (no custom routing verbs)
- [FORBIDDEN] Custom SDK abstractions (YAGNI)

## Documentation Standards

- [MUST] All agents documented in README
- [SHOULD] Complex tools include usage examples
- [SHOULD] Architecture decisions in docs/architecture/
```

## Related Skills

- **speckit** - Main workflow (uses constitution throughout)
- **speckit-specify** - Specification creation (validates against constitution)
- **speckit-plan** - Technical planning (validates against constitution)
