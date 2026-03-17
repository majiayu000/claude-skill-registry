---
name: speckit
description: Use when user wants to work with specifications or create feature requirements following the spec-driven development workflow
---

# Speckit: Spec-Driven Development Workflow

## Overview

Speckit is a complete specification-driven development workflow that ensures features are well-defined before implementation. It guides you through creating specifications, technical plans, and actionable tasks.

**Core Principle:** Define WHAT and WHY before HOW. Specifications describe user needs and business value, plans describe technical approach, tasks describe execution steps.

## Template Locations

All speckit sub-skills use standardized templates located in the `.github/skills/` directory:

- **Constitution Template**: `.github/skills/speckit-constitution/constitution-template.md`
- **Specification Template**: `.github/skills/speckit-specify/spec-template.md`
- **Plan Template**: `.github/skills/speckit-plan/plan-template.md`
- **Tasks Template**: `.github/skills/speckit-tasks/tasks-template.md`

Each sub-skill MUST load and use its respective template as the base structure.

## When to Use

Use this skill when:
- Starting a new feature or project
- User requests "spec-driven development"
- User wants to create detailed requirements before coding
- You need to ensure feature is well-understood before implementation
- User mentions "specifications", "spec format", or "speckit"

## The Workflow

The speckit workflow has 4 main phases:

```
1. Brainstorming → 2. Specify → 3. Plan → 4. Tasks → (5. Implement)
```

### Phase 1: Brainstorming (Understanding)

**Skill:** `brainstorming`

**Purpose:** Deeply understand user intent, requirements, and design before creating the specification.

**When:** User presents their goal and wants to work in the specs format

**What happens:**
- Explore user intent through targeted questions
- Identify requirements, constraints, and success criteria
- Clarify ambiguities and edge cases
- Document assumptions and design decisions
- Create shared understanding of what will be built

**Output:** Clear understanding of feature requirements, ready to be formalized

### Phase 2: Specify (WHAT & WHY)

**Skill:** `speckit-specify`

**Purpose:** Create a formal, technology-agnostic specification that describes user needs and business value.

**Prerequisites:** Completed brainstorming session

**What happens:**
- Generate feature branch and directory structure
- Create `spec.md` with:
  - Feature overview and context
  - Functional requirements (user capabilities)
  - Non-functional requirements (quality attributes)
  - User scenarios and acceptance criteria
  - Success metrics (technology-agnostic)
  - Edge cases and constraints
- Validate specification quality
- Resolve any remaining clarifications

**Key Principles:**
- Focus on WHAT users need and WHY
- Avoid HOW to implement (no tech stack, APIs, code structure)
- Written for business stakeholders, not developers
- Technology-agnostic success criteria

**Output:** `specs/N-feature-name/spec.md` - Complete feature specification

### Phase 3: Plan (HOW - Technical Design)

**Skill:** `speckit-plan`

**Purpose:** Create technical implementation plan that describes HOW to build the feature.

**Prerequisites:** Completed specification

**What happens:**
- Load specification and project context
- Research technical approaches and best practices
- Design system architecture
- Create data models and API contracts
- Document technology choices and rationale
- Generate quickstart scenarios
- Update agent context with new technologies

**Output:** 
- `specs/N-feature-name/plan.md` - Implementation plan
- `specs/N-feature-name/data-model.md` - Entity relationships
- `specs/N-feature-name/contracts/` - API specifications
- `specs/N-feature-name/quickstart.md` - Integration scenarios
- `specs/N-feature-name/research.md` - Technical decisions

### Phase 4: Tasks (Execution Plan)

**Skill:** `speckit-tasks`

**Purpose:** Break down the plan into actionable, dependency-ordered tasks.

**Prerequisites:** Completed technical plan

**What happens:**
- Load spec, plan, and design artifacts
- Map requirements to tasks
- Organize tasks by user story
- Identify dependencies and parallel opportunities
- Create execution phases (Setup → Foundation → User Stories → Polish)
- Generate task checklist with file paths

**Key Principles:**
- Tasks organized by user story (independent implementation)
- Each task has specific file path
- Clear dependencies marked
- Parallel opportunities identified ([P] marker)
- Each user story independently testable

**Output:** `specs/N-feature-name/tasks.md` - Complete task breakdown

### Phase 5: Implementation (Execute)

**Skills:** `executing-plans` OR `test-driven-development` (user choice)

**Purpose:** Execute the tasks and build the feature.

**Prerequisites:** Completed task breakdown

**User Choice:**
- **Option A - Executing Plans:** Sequential execution of all tasks with checkpoints
- **Option B - Test-Driven Development:** TDD approach with failing tests first

**What happens:**
- Check checklist completion status
- Execute tasks phase-by-phase
- Respect dependencies and parallel opportunities
- Validate at checkpoints
- Track progress

**Output:** Implemented feature matching specification

## Supporting Skills

### Speckit-Checklist

**Skill:** `speckit-checklist`

**Purpose:** Generate custom requirement quality checklists ("unit tests for requirements")

**When:** After specification or plan, when you need domain-specific validation

**Output:** `specs/N-feature-name/checklists/[domain].md` - Quality checklist

### Speckit-Constitution

**Skill:** `speckit-constitution`

**Purpose:** Create or update project constitution (principles and standards)

**When:** Establishing project principles or updating standards

**Output:** `.specify/memory/constitution.md` - Project constitution

## Quick Start Guide

### Starting a New Feature

1. **Brainstorm the feature:**
   ```
   Use brainstorming skill to explore feature requirements
   ```

2. **Create specification:**
   ```
   Use speckit-specify skill with feature description
   ```

3. **Build technical plan:**
   ```
   Use speckit-plan skill to design implementation
   ```

4. **Generate tasks:**
   ```
   Use speckit-tasks skill to create task breakdown
   ```

5. **Implement (choose one):**
   ```
   Use executing-plans skill for sequential execution
   OR
   Use test-driven-development skill for TDD approach
   ```

### Example Workflow

**User says:** "I want to build a user authentication system with OAuth2"

**Agent does:**
1. Invoke `brainstorming` skill
   - Ask about requirements, constraints, security needs
   - Document design decisions
   - Clarify scope and edge cases

2. Invoke `speckit-specify` skill
   - Create specification describing WHAT users need (login, logout, session management)
   - Define success criteria (user can authenticate in <3 minutes, sessions persist for 24h)
   - No mention of specific OAuth libraries or frameworks

3. Invoke `speckit-plan` skill
   - Research OAuth2 best practices
   - Choose specific libraries and frameworks
   - Design data model (User, Session, Token entities)
   - Create API contracts (POST /auth/login, POST /auth/logout, etc.)
   - Document architecture decisions

4. Invoke `speckit-tasks` skill
   - Generate task list organized by user story
   - Mark parallel opportunities
   - Include file paths for each task

5. Offer implementation options:
   - "Ready to implement! Choose approach:"
   - "A) Use executing-plans for sequential task execution"
   - "B) Use test-driven-development for TDD approach"

## Iron Laws

### Specification Phase
- **No implementation details** in spec.md (no languages, frameworks, APIs)
- **Technology-agnostic success criteria** (user-facing metrics only)
- **Written for business stakeholders** (avoid technical jargon)
- **Focus on user value** (WHAT and WHY, not HOW)

### Planning Phase
- **Specification is immutable** during planning (don't change WHAT while designing HOW)
- **All technical decisions documented** in research.md with rationale
- **Constitution principles enforced** (non-negotiable constraints)
- **Design artifacts generated** before tasks (data model, contracts, quickstart)

### Task Phase
- **Organize by user story** (enable independent implementation)
- **Every task has file path** (specific, not vague)
- **Dependencies explicit** (clear execution order)
- **Each story independently testable** (complete vertical slices)

### Implementation Phase
- **Constitution check before start** (validate checklist completion)
- **Halt on failed checklists** (unless user explicitly proceeds)
- **Track progress** (mark tasks completed in tasks.md)
- **Validate at checkpoints** (don't continue with broken state)

## Common Patterns

### Pattern: Exploratory Spike
If requirements are unclear, use brainstorming first to explore the problem space.

### Pattern: Iterative Refinement
After generating spec, use speckit-checklist to validate quality, then refine if needed.

### Pattern: Multiple Implementation Approaches
Generate tasks.md once, then choose between executing-plans (sequential) or test-driven-development (TDD).

### Pattern: Constitution-Driven Development
Define project constitution first, then all specs/plans automatically enforce those principles.

## Anti-Patterns

### ❌ Skip Brainstorming
**Wrong:** Jump directly to speckit-specify without understanding requirements
**Right:** Use brainstorming to deeply explore user needs first

### ❌ Mix Spec and Implementation
**Wrong:** Include framework choices, API endpoints, database schemas in spec.md
**Right:** Spec describes user needs, plan describes technical approach

### ❌ Tasks Before Plan
**Wrong:** Generate tasks directly from specification
**Right:** Create technical plan first, then generate tasks from plan

### ❌ Ignore Checklists
**Wrong:** Proceed with implementation when checklists fail
**Right:** Complete checklists or explicitly acknowledge risk

### ❌ Vague Tasks
**Wrong:** "Create user model" (no file path, unclear scope)
**Right:** "Create User entity in src/models/user.py with fields from data-model.md" [US1]

## Success Indicators

You're using speckit correctly when:
- ✅ Specifications contain zero implementation details
- ✅ Success criteria are measurable and technology-agnostic
- ✅ Plans reference specifications and don't change WHAT
- ✅ Tasks map clearly to user stories
- ✅ Each user story is independently testable
- ✅ Constitution principles are enforced throughout
- ✅ Brainstorming precedes specification
- ✅ Implementation follows completed task breakdown

## Files Created

```
specs/N-feature-name/
├── spec.md                    # WHAT & WHY (from speckit-specify)
├── plan.md                    # HOW (from speckit-plan)
├── tasks.md                   # Execution plan (from speckit-tasks)
├── data-model.md              # Entities (from speckit-plan)
├── research.md                # Technical decisions (from speckit-plan)
├── quickstart.md              # Integration scenarios (from speckit-plan)
├── contracts/                 # API specs (from speckit-plan)
│   ├── openapi.yaml
│   └── ...
└── checklists/                # Quality validation (from speckit-checklist)
    ├── ux.md
    ├── security.md
    └── ...
```

## Related Skills

- **brainstorming** - Explore requirements before specification (REQUIRED first step)
- **speckit-specify** - Create feature specification
- **speckit-plan** - Create technical plan
- **speckit-tasks** - Generate task breakdown
- **speckit-checklist** - Generate quality checklists
- **speckit-constitution** - Manage project constitution
- **executing-plans** - Sequential task execution (implementation option A)
- **test-driven-development** - TDD approach (implementation option B)
- **systematic-debugging** - Debug issues during implementation
- **verification-before-completion** - Verify work before claiming complete

## Workflow Entry Points

### New Feature (Full Workflow)
1. brainstorming → 2. speckit-specify → 3. speckit-plan → 4. speckit-tasks → 5. Choose: executing-plans OR test-driven-development

### Existing Spec (Continue from Plan)
1. speckit-plan → 2. speckit-tasks → 3. Choose: executing-plans OR test-driven-development

### Existing Plan (Continue from Tasks)
1. speckit-tasks → 2. Choose: executing-plans OR test-driven-development

### Quality Check (Any Phase)
- speckit-checklist (generate domain-specific quality checklist)

## Notes

- **Replaced skills:** speckit-analyze and speckit-clarify are replaced by brainstorming skill
- **Implementation choice:** speckit-implement is replaced by offering both executing-plans and test-driven-development
- **Brainstorming first:** Always use brainstorming skill before speckit-specify
- **Constitution authority:** Project constitution (.specify/memory/constitution.md) is non-negotiable
- **Quality gates:** Checklists validate requirements quality before implementation
