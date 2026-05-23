---
name: cfn-epic-creator
description: "Creates comprehensive epic definitions with sequential reviews from 10 key personas. Use when you need to analyze requirements from multiple perspectives and generate structured epic documentation with cost estimates and risk assessments."
version: 1.0.0
tags: [epic, creator, personas, analysis, cost-estimation, requirements]
status: production
---

# CFN Epic Creator

## Overview

The cfn-epic-creator skill provides orchestration for creating comprehensive epic definitions through sequential reviews from eleven persona reviews: Simplifier (initial scope reduction), Product Manager, Architect, Security Specialist, Backend Developer, Frontend Developer, DevOps Engineer, Test Specialist, Code Standards Reviewer, Strategic Alignment Reviewer, and Simplifier (final complexity check).

## Usage

The epic creator is a **main chat workflow** - not a standalone script. Main chat:
1. Creates base JSON
2. Spawns Simplifier for initial scope reduction (review only - returns recommendations)
3. User approves initial simplifications
4. Spawns 9 persona agents sequentially (each edits epic directly)
5. Spawns Simplifier for final complexity review (review only - returns recommendations)
6. User approves final simplifications

See **Main Chat Execution Process** below for details.

## Output Structure

The generated JSON follows this structure:

```json
{
  "epic": {
    "id": "EPIC-XXXXXX",
    "title": "Extracted from description",
    "description": "Full epic description",
    "status": "in-review",
    "priority": "high",
    "estimatedDuration": "TBD",
    "budget": "TBD",
    "owner": "TBD",
    "metadata": {
      "createdAt": "2024-01-01T00:00:00.000Z",
      "reviewMode": "standard|enterprise|mvp",
      "devopsEnforced": true|false
    },
    "personas": [
      {
        "name": "product-owner",
        "reviewOrder": 1,
        "status": "completed",
        "insights": [
          "Strategic insight 1",
          "Strategic insight 2"
        ],
        "recommendations": [
          {
            "id": "PO-001",
            "title": "Recommendation title",
            "type": "blocking|suggested",
            "priority": "critical|high|medium|low",
            "estimatedCost": "$X,XXX",
            "description": "Detailed description"
          }
        ],
        "costAnalysis": {
          "category1": "$X,XXX",
          "category2": "$X,XXX"
        }
      },
      {
        "name": "architect",
        "reviewOrder": 2,
        "...": "..."
      },
      {
        "name": "security-specialist",
        "reviewOrder": 3,
        "...": "..."
      },
      {
        "name": "test-specialist",
        "reviewOrder": 4,
        "...": "..."
      },
      {
        "name": "strategic-alignment-reviewer",
        "reviewOrder": 5,
        "...": "..."
      },
      {
        "name": "code-standards-reviewer",
        "reviewOrder": 6,
        "...": "..."
      },
      {
        "name": "devops-engineer",
        "reviewOrder": 7,
        "...": "..."
      },
      {
        "name": "backend-developer",
        "reviewOrder": 8,
        "...": "..."
      },
      {
        "name": "frontend-developer",
        "reviewOrder": 9,
        "...": "..."
      }
    ],
    "technicalRequirements": {
      "components": [
        {"name": "ComponentA", "responsibility": "Handles X", "dependencies": ["ComponentB"]},
        {"name": "ComponentB", "responsibility": "Handles Y", "dependencies": []}
      ],
      "interfaces": [
        {"name": "IService", "methods": ["getData(): Promise<Data>", "setData(d: Data): void"]}
      ],
      "dependencies": {
        "internal": ["shared-utils", "auth-service"],
        "external": ["react", "axios"]
      },
      "architecture": "modular-monolith"
    },
    "implementationRoadmap": [
      {"phase": 1, "name": "Core Infrastructure", "tasks": ["task1", "task2"]},
      {"phase": 2, "name": "Feature Implementation", "tasks": ["task3", "task4"]}
    ],
    "totalCostBreakdown": {},
    "riskAssessment": {
      "technical": [{"risk": "API breaking changes", "mitigation": "Version API endpoints"}],
      "operational": [{"risk": "Deployment downtime", "mitigation": "Blue-green deployment"}]
    }
  }
}
```

## Persona Review Order

1. **Simplifier (Initial)** - Early scope reduction, feature elimination, YAGNI enforcement (REVIEW ONLY - returns recommendations)
2. **Product Manager** - Business value, user stories, market fit (on refined scope)
3. **Architect** - System design, technology choices, scalability, feasibility
4. **Security Specialist** - Security posture, vulnerabilities, compliance, threat modeling
5. **Backend Developer** - API design, data structures, business logic (defines API contract)
6. **Frontend Developer** - User interface, experience, client-side logic (depends on backend API)
7. **DevOps Engineer** - Deployment, operations, infrastructure (knows full stack)
8. **Test Specialist** - Production readiness, test coverage, quality gates, integration verification
9. **Code Standards Reviewer** - Type alignment, naming conventions, API contract consistency
10. **Strategic Alignment Reviewer** - High-level coherence, plan consistency, integration completeness, dead code detection
11. **Simplifier (Final)** - Complexity reduction, scope creep detection, over-engineering prevention (REVIEW ONLY - returns recommendations)

## Main Chat Execution Process

The epic creator uses a sequential persona review process. Main chat spawns each persona agent one at a time, and each agent edits the epic file directly.

### Step 1: Create Base Epic JSON

Main chat creates the base JSON directly:

```json
{
  "epic_id": "unique-id",
  "description": "Your epic description",
  "mode": "standard",
  "created_at": "2025-01-01T00:00:00Z",
  "personas": [
    {"name": "Simplifier (Initial)", "focus": "scope reduction, feature elimination"},
    {"name": "Product Manager", "focus": "business value, user stories"},
    {"name": "Architect", "focus": "system design, scalability, feasibility"},
    {"name": "Security Specialist", "focus": "threats, compliance, threat modeling"},
    {"name": "Backend Developer", "focus": "APIs, data models (defines API contract)"},
    {"name": "Frontend Developer", "focus": "UI/UX, components (depends on backend)"},
    {"name": "DevOps Engineer", "focus": "deployment, monitoring, infrastructure"},
    {"name": "Test Specialist", "focus": "test strategy, coverage, quality gates"},
    {"name": "Code Standards Reviewer", "focus": "types, naming, contracts"},
    {"name": "Strategic Alignment Reviewer", "focus": "integration gaps, coherence"},
    {"name": "Simplifier (Final)", "focus": "scope creep detection, complexity review"}
  ],
  "reviews": [],
  "userStories": [],
  "technicalRequirements": {},
  "implementationRoadmap": [],
  "riskAssessment": {}
}
```

Write this to a file (e.g., `docs/epics/my-epic.json`).

### Step 2: Spawn Personas Sequentially

For each persona, spawn a Task agent that reads the epic, analyzes it, and adds their review:

| Order | Agent | Focus |
|-------|-------|-------|
| 1 | `simplifier` | Initial scope reduction, feature elimination (REVIEW ONLY - returns recommendations to user) |
| 2 | `product-owner` | Business value, user stories, market fit (on refined scope) |
| 3 | `system-architect` | System design, scalability, feasibility, technical constraints |
| 4 | `security-specialist` | Threats, vulnerabilities, compliance, threat modeling |
| 5 | `backend-developer` | API design, data models, services (defines API contract first) |
| 6 | `react-frontend-engineer` | UI/UX, client architecture (depends on backend API) |
| 7 | `devops-engineer` | Deployment, monitoring, infrastructure (knows full stack) |
| 8 | `tester` | Test strategy, coverage, production readiness **[MUST ALIGN WITH EXISTING FRAMEWORK - vitest/jest]** |
| 9 | `code-standards-reviewer` | Types, naming, API contracts, consistency |
| 10 | `strategic-alignment-reviewer` | Integration gaps, dead code, misalignments, coherence |
| 11 | `simplifier` | Final complexity review, scope creep detection (REVIEW ONLY - returns recommendations to user) |

### Step 3: Persona Task Template

Each persona agent receives this task - they both review AND contribute to the epic:

```
Read /tmp/epic.json and analyze the epic description from your perspective.

YOUR JOB: Review the epic AND add your contributions to it.

1. ADD YOUR REVIEW to the reviews array:
{
  "persona": "<your-name>",
  "reviewOrder": <number>,
  "status": "completed",
  "insights": ["insight 1", "insight 2", ...],
  "recommendations": [
    {
      "id": "<PERSONA>-001",
      "title": "recommendation title",
      "type": "blocking|suggested",
      "priority": "critical|high|medium|low",
      "description": "details"
    }
  ],
  "risks": ["risk 1", "risk 2"]
}

2. ADD YOUR CONTRIBUTIONS to the epic itself:
   - Simplifier (Initial & Final): **REVIEW ONLY** - returns recommendations, does not edit
   - Product Owner: Add user stories, acceptance criteria, success metrics
   - Architect: **STRUCTURAL OUTPUT REQUIRED** - Add to technicalRequirements:
     * `components` or `modules`: List of components/modules with responsibilities
     * `interfaces` or `api`: Interface definitions, function signatures, contracts
     * `dependencies`: Internal and external dependency mapping
     * `architecture`: High-level architecture pattern (monolith, microservices, etc.)
     * Also add: data models, feasibility analysis, scalability considerations
   - Security: Add security requirements, threat mitigations, compliance needs, threat model
   - Backend: Add API endpoints, services, database schemas (defines API contract)
   - Frontend: Add UI components, user flows, client requirements (uses backend API)
   - DevOps: Add deployment requirements, monitoring needs, infrastructure specs
   - Tester: Add test cases, quality gates, validation criteria **[MUST ALIGN WITH EXISTING FRAMEWORK]**
   - Code Standards: Add naming conventions, type requirements, API contracts
   - Strategic Alignment: Flag integration gaps, add missing connections, coherence validation

3. UPDATE these epic sections based on your expertise:
   - implementationRoadmap: Add phases/tasks from your domain
   - totalCostBreakdown: Add cost estimates for your area
   - riskAssessment: Add risks you've identified

Write the updated JSON back to /tmp/epic.json
```

### Step 4: Simplifier - Initial Scope Reduction

The Simplifier runs FIRST before any other personas. It analyzes the base epic and does NOT edit it. Instead:

```
Read /tmp/epic.json and analyze for unnecessary scope and complexity.

DO NOT edit the epic. Instead:

1. ADD your review to the reviews array only
2. RETURN your findings to main chat for user review:

{
  "persona": "simplifier-initial",
  "phase": "scope-reduction",
  "status": "completed",
  "simplifications": [
    {
      "target": "component/feature",
      "issue": "why it's unnecessary for v1",
      "suggestion": "defer to v2 or eliminate",
      "defer_to_v2": true/false
    }
  ],
  "features_to_remove": ["feature 1", "feature 2"],
  "features_to_defer": ["feature 3", "feature 4"],
  "consolidations": [
    {"merge": ["A", "B"], "into": "single feature"}
  ],
  "complexity_reduction": "estimated % reduction"
}

Write review to /tmp/epic.json reviews array.
Return full findings to main chat - USER DECIDES what to apply.
```

Main chat presents initial Simplifier recommendations to user. User approves scope reduction, then main chat applies changes before spawning other personas.

### Step 5: Core Personas (2-10)

After initial simplification, personas 2-10 analyze the refined epic and add their contributions. Each persona edits the epic directly.

After personas 2-10 complete, `/tmp/epic.json` contains the full epic with contributions and reviews.

### Step 6: Simplifier - Final Complexity Review

The Simplifier runs AGAIN at the end and does NOT edit the epic. Instead:

```
Read /tmp/epic.json and analyze for scope creep and over-engineering.

DO NOT edit the epic. Instead:

1. ADD your review to the reviews array only
2. RETURN your findings to main chat for user review:

{
  "persona": "simplifier-final",
  "phase": "complexity-review",
  "status": "completed",
  "scope_creep_detected": ["feature X added by persona Y", "..."],
  "over_engineering": [
    {
      "target": "component/feature",
      "issue": "why it's over-engineered",
      "suggestion": "simpler alternative",
      "added_by": "persona-name"
    }
  ],
  "features_to_remove": ["feature 1", "feature 2"],
  "features_to_defer": ["feature 3", "feature 4"],
  "consolidations": [
    {"merge": ["A", "B"], "into": "single feature"}
  ],
  "complexity_reduction": "estimated % reduction"
}

Write review to /tmp/epic.json reviews array.
Return full findings to main chat - USER DECIDES what to apply.
```

Main chat presents final Simplifier recommendations to user. User chooses which simplifications to accept, then main chat applies approved changes.

### Example Main Chat Flow

```
1. Create base JSON and write to docs/epics/my-epic.json
2. Task(simplifier, "Review docs/epics/my-epic.json for initial scope reduction...") → returns recommendations
3. Present initial simplifier recommendations to user
4. Apply approved scope reductions to epic
5. Task(product-owner, "Review docs/epics/my-epic.json from business perspective...")
6. Task(system-architect, "Review docs/epics/my-epic.json from architecture perspective...")
7. Task(security-specialist, "Review docs/epics/my-epic.json from security perspective...")
8. Task(backend-developer, "Review docs/epics/my-epic.json from backend perspective...")
9. Task(react-frontend-engineer, "Review docs/epics/my-epic.json from frontend perspective...")
10. Task(devops-engineer, "Review docs/epics/my-epic.json from operations perspective...")
11. Task(tester, "Review docs/epics/my-epic.json from testing perspective...")
12. Task(code-standards-reviewer, "Review docs/epics/my-epic.json for code consistency...")
13. Task(strategic-alignment-reviewer, "Review docs/epics/my-epic.json for integration gaps...")
14. Task(simplifier, "Review docs/epics/my-epic.json for scope creep and complexity...") → returns recommendations
15. Present final simplifier recommendations to user
16. Apply approved simplifications
```

## Selective Agent Validation

Instead of running all 11 personas, you can declare specific agents in your preferred order.

### Usage

```bash
# Run specific agents in order
cfn-epic-creator "Build dashboard" --agents=typescript-specialist,tester,integration-tester,react-frontend-engineer

# Run agents within each sprint context (keeps context close to execution)
cfn-epic-creator "Build feature" --agents=typescript-specialist,tester --per-sprint
```

### Available Agents

| Agent | Focus Area |
|-------|-----------|
| `typescript-specialist` | Cross-file type safety, imports/exports, type contracts |
| `tester` | Test strategy, coverage requirements, quality gates |
| `integration-tester` | End-to-end workflow validation, component wiring |
| `react-frontend-engineer` | UI components, branding, breaking error prevention |
| `backend-developer` | API design, data structures, service contracts |
| `rust-developer` | Systems programming, memory safety, performance optimization |
| `security-specialist` | Security review, vulnerability assessment |
| `code-standards-reviewer` | Naming conventions, type alignment, API consistency |
| `strategic-alignment-reviewer` | Integration gaps, dead code detection |
| `simplifier` | Scope reduction, over-engineering prevention |
| `product-owner` | Business value, user stories, acceptance criteria |
| `system-architect` | System design, scalability, technical constraints |
| `devops-engineer` | Deployment, infrastructure, monitoring |

### Per-Sprint Validation (--per-sprint)

When `--per-sprint` is enabled, validation agents run within each sprint/phase context rather than at the epic level. This:

1. **Keeps context close to execution** - agents see only the files/tasks in that sprint
2. **Catches sprint-specific issues** - type mismatches within a sprint's scope
3. **Reduces cognitive load** - smaller context window for more focused review

**Example workflow with --per-sprint:**

```
Sprint 1: Core Types
├── typescript-specialist reviews Sprint 1 files only
├── tester defines tests for Sprint 1 deliverables
└── Validation report for Sprint 1

Sprint 2: API Layer
├── typescript-specialist reviews Sprint 2 files + Sprint 1 interfaces
├── tester defines integration tests
└── Validation report for Sprint 2

Sprint 3: UI Components
├── react-frontend-engineer reviews Sprint 3 files
├── integration-tester validates full wiring
└── Validation report for Sprint 3
```

### Common Agent Combinations

**TypeScript-First Validation:**
```bash
--agents=typescript-specialist,code-standards-reviewer,tester
```
Sets types/imports/exports consistency, then validates naming conventions, then defines tests.

**Full-Stack Review:**
```bash
--agents=backend-developer,react-frontend-engineer,integration-tester
```
API contracts first, then UI components, then wiring validation.

**Quality Focus:**
```bash
--agents=simplifier,tester,security-specialist,code-standards-reviewer
```
Scope reduction, test strategy, security review, standards enforcement.

**Haiku Model Optimization:**
```bash
--agents=typescript-specialist,tester,integration-tester,react-frontend-engineer --per-sprint
```
Focused agents with per-sprint context for smaller models.

## Test Framework Alignment (MANDATORY)

**The tester persona MUST detect and align with existing test frameworks before defining test strategies.**

```bash
# Detect existing framework FIRST
grep -q "vitest" package.json && echo "USE VITEST"
grep -q "jest" package.json && echo "USE JEST"
ls vitest.config.* 2>/dev/null && echo "USE VITEST"
ls jest.config.* 2>/dev/null && echo "USE JEST"
```

| If Found | Use |
|----------|-----|
| `vitest` in package.json | `vi.fn()`, `vi.mock()`, `import { describe, it, expect } from 'vitest'` |
| `jest` in package.json | `jest.fn()`, `jest.mock()`, `import { describe, it, expect } from '@jest/globals'` |
| `vitest.config.ts` | vitest patterns |
| `jest.config.js` | jest patterns |

**NEVER mix vitest and jest in the same project. This causes compilation errors.**

---

## Structural Validation Requirements

Before an epic proceeds to implementation, it must pass **structural validation**. This ensures the epic has sufficient architectural detail for agents to implement without design ambiguity.

### When Validation Runs

Structural validation is a **gate between epic creation and implementation**:

```
Epic Creation Workflow:
───────────────────────────────────────────────────────────────
Step 1-2:   Main Chat creates JSON, Simplifier reviews scope
Step 3-12:  9 Personas review (Architect adds structural data)
Step 13-14: Final Simplifier review, user approves
Step 15:    ⬇️ STRUCTURAL VALIDATION GATE ⬇️
            ./.claude/skills/cfn-epic-creator/validate-epic.sh $EPIC -v

            ├─ PASS (≥71%): Proceed to implementation
            └─ FAIL (<71%): Loop back to Architect for structural review
───────────────────────────────────────────────────────────────
```

### Required Structural Elements

| Element | Location | Required Content | Responsible Persona |
|---------|----------|-----------------|---------------------|
| **Module Breakdown** | `technicalRequirements.components` or `.modules` | List of modules with responsibilities | **Architect** |
| **Interfaces** | `technicalRequirements.interfaces` or `.api` | Function signatures, type contracts | **Architect** |
| **Dependencies** | `technicalRequirements.dependencies` | Internal and external dependency map | **Architect** |
| **Roadmap** | `implementationRoadmap` | Ordered phases with tasks | All personas contribute |
| **Risks** | `riskAssessment` | Identified risks with mitigations | All personas contribute |

### Validation Checks (7 total)

1. `technicalRequirements` exists and non-empty
2. `implementationRoadmap` has phases
3. Architect provided ≥3 insights
4. Module/component breakdown defined
5. Interface/API contracts defined
6. Dependency mapping exists
7. Risk assessment populated

### Structural Completeness Score

Score = (passed_checks / 7) × 100%

| Score | Status | Action |
|-------|--------|--------|
| 100% (7/7) | ✅ Ready | Proceed to implementation |
| 71-99% (5-6/7) | ⚠️ Minor gaps | User decides: proceed or enhance |
| <71% (≤4/7) | ⚠️ Significant gaps | Architect review required |

### Running Validation

```bash
# Standard validation (warnings only)
./.claude/skills/cfn-epic-creator/validate-epic.sh epic.json -v

# Strict mode (>2 warnings = FAIL, blocks implementation)
./.claude/skills/cfn-epic-creator/validate-epic.sh epic.json -v -s
```

### Strict Mode (`-s` flag)

In strict mode, epics with >2 structural warnings fail validation (exit code 1). Use for production epics where implementation quality is critical.

---

## Best Practices

1. **Clear Epic Descriptions**: Provide detailed, specific descriptions including:
   - Business objectives
   - Technical requirements
   - Target users/stakeholders
   - Success criteria
   - Constraints and assumptions

2. **Review Simplifier Recommendations**: The Simplifier runs TWICE:

   **Initial Pass (before other personas):**
   - Early scope reduction
   - Feature elimination
   - YAGNI enforcement
   - Defer non-essential features to v2
   - Saves other personas from analyzing unnecessary scope

   **Final Pass (after all personas):**
   - Scope creep detection
   - Over-engineering prevention
   - Consolidation opportunities
   - Simpler alternatives
   - AI/LLM opportunities

3. **Iterate Based on Feedback**: After reviewing, you can:
   - Accept all simplifications
   - Accept some, reject others
   - Ask personas to revise based on new constraints
