---
name: speckit-plan
description: Execute implementation planning workflow using the plan template to generate design artifacts
---

# Speckit-Plan: Technical Implementation Planning

## Purpose

Create technical implementation plan that describes **HOW** to build the feature defined in the specification, including architecture, technology choices, data models, and API contracts.

## Prerequisites

- Completed specification (`spec.md` exists)
- Project constitution loaded (`.specify/memory/constitution.md`)

## What This Skill Does

1. Loads specification and project context
2. Researches technical approaches and best practices
3. Designs system architecture and technology stack
4. Creates data models and API contracts
5. Documents technology choices with rationale
6. Generates integration scenarios (quickstart)
7. Updates agent context with new technologies

## Key Principles

### Specification is Immutable
- Don't change WHAT while designing HOW
- Technical decisions must serve specification requirements
- If spec gaps found, note them but don't modify spec

### Constitution Authority
- Project constitution principles are non-negotiable
- Validate all choices against constitution
- Document compliance in Constitution Check section

### Design Before Tasks
- Complete all design artifacts before task generation
- Data models, contracts, and research must be finished
- Provides foundation for accurate task breakdown

## Template Location

**IMPORTANT:** The plan template is located at:
`.github/skills/speckit-plan/plan-template.md`

This template MUST be loaded and used as the base structure for all technical planning.

## Execution Flow

All execution logic is now contained within this skill. The skill handles:
- Setup script execution
- Context loading
- Planning workflow execution
- Artifact generation

### Quick Summary

1. **Setup:** Run `setup-plan.sh` to get feature paths
2. **Load template** from `.github/skills/speckit-plan/plan-template.md`
3. **Load context:** Read spec.md and constitution.md
4. **Execute planning workflow:**
   - **Phase 0: Research & Outline**
     - Identify unknowns and research needs
     - Dispatch research agents for each unknown
     - Consolidate findings in `research.md`
   - **Phase 1: Design & Contracts**
     - Extract entities → `data-model.md`
     - Generate API contracts → `contracts/`
     - Create integration scenarios → `quickstart.md`
     - Update agent context (copilot-specific files)
5. **Constitution check:** Validate design against principles
6. **Report completion:** List all generated artifacts

## Phase 0: Research & Outline

**Goal:** Resolve all technical unknowns before design

### What Happens

1. **Extract unknowns** from Technical Context:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Dispatch research agents:**
   - "Research {unknown} for {feature context}"
   - "Find best practices for {tech} in {domain}"

3. **Consolidate findings** in `research.md`:
   ```markdown
   ## Decision: [what was chosen]
   
   **Rationale:** [why chosen]
   
   **Alternatives Considered:**
   - Option A: [pros/cons]
   - Option B: [pros/cons]
   
   **Selected:** Option A because...
   ```

**Output:** `research.md` with all unknowns resolved

## Phase 1: Design & Contracts

**Prerequisites:** research.md complete

### What Happens

1. **Data Model** (`data-model.md`):
   - Extract entities from specification
   - Define fields, types, relationships
   - Document validation rules
   - Describe state transitions

2. **API Contracts** (`contracts/`):
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Generate OpenAPI or GraphQL schema
   - Include request/response examples

3. **Quickstart** (`quickstart.md`):
   - End-to-end integration scenarios
   - Setup instructions
   - Sample requests/responses
   - Common troubleshooting

4. **Agent Context Update:**
   - Run `update-agent-context.sh copilot`
   - Add new technologies from plan
   - Preserve manual additions between markers

**Output:** 
- `data-model.md`
- `contracts/*.yaml` (OpenAPI/GraphQL)
- `quickstart.md`
- Updated agent context files

## Constitution Check

Validate design against project principles:

1. **Load constitution** from `.specify/memory/constitution.md`
2. **Check each principle:**
   - Does design violate any MUST rules?
   - Are SHOULD rules followed or justified?
3. **Document compliance** in Constitution Check section
4. **ERROR if violations unjustified**

## Success Indicators

Plan is ready when:
- ✅ All research decisions documented with rationale
- ✅ Data model covers all entities from specification
- ✅ API contracts map to all user actions
- ✅ Quickstart provides working integration example
- ✅ Constitution check passes (or violations justified)
- ✅ Agent context updated with new technologies
- ✅ No NEEDS CLARIFICATION markers remain

## Output

```
specs/N-feature-name/
├── plan.md                    # Technical implementation plan (HOW)
├── data-model.md              # Entity definitions and relationships
├── research.md                # Technical decisions and rationale
├── quickstart.md              # Integration scenarios
└── contracts/                 # API specifications
    ├── openapi.yaml
    └── schema.graphql
```

## Next Step

After plan is complete:
- Use `speckit-tasks` to generate task breakdown

## Common Mistakes

### ❌ Changing Specification During Planning
**Wrong:** "Spec says OAuth2, but I'll use API keys instead" (changing WHAT)
**Right:** "Spec requires OAuth2, planning OAuth2 implementation" (serving WHAT)

### ❌ Ignoring Constitution
**Wrong:** Skip constitution check, violate principles
**Right:** Validate against constitution, justify any exceptions

### ❌ Incomplete Research
**Wrong:** Jump to design with unresolved unknowns
**Right:** Research all unknowns first, document decisions

### ❌ Vague Data Models
**Wrong:** "User entity has some fields"
**Right:** "User entity: id (UUID), email (string, unique), createdAt (timestamp)"

### ❌ Missing Contracts
**Wrong:** "We'll figure out API structure during implementation"
**Right:** Complete OpenAPI spec with all endpoints, schemas, examples

## Related Skills

- **speckit-specify** - Previous step (create specification)
- **speckit-tasks** - Next step (generate task breakdown)
- **speckit-checklist** - Generate domain-specific quality checks
