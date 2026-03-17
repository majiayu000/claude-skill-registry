---
description: Generates comprehensive specifications (spec.md, plan.md, tasks.md with embedded tests) for SpecWeave increments. Use when creating new increments, planning features, or converting ideas into actionable specs. Produces structured documentation with proven templates and context-aware organization.
---

# Spec Generator - Flexible Increment Documentation

**Purpose**: Automatically generate comprehensive specification documentation (spec.md, plan.md, tasks.md with embedded tests) for SpecWeave increments using proven templates and flexible, context-aware structure.

**When to Use**:
- Creating new increments (`/sw:inc`)
- Planning features or products
- Generating structured documentation
- Converting ideas into actionable specs

**Based On**: Flexible Spec Generator (V2) - context-aware, non-rigid templates

---

## How Spec Generator Works

### 1. Flexible Spec Generation (spec.md)

**Adapts to Context**:
- **New Product**: Full PRD with market analysis, user personas, competitive landscape
- **Feature Addition**: Focused user stories, acceptance criteria, integration points
- **Bug Fix**: Problem statement, root cause, solution, impact analysis
- **Refactoring**: Current state, proposed changes, benefits, migration plan

**YAML Frontmatter**:
```yaml
---
increment: 0001-feature-name
title: "Feature Title"
type: feature
priority: P1
status: planned
created: 2025-12-04
# NOTE: project: and board: fields REMOVED from frontmatter!
# Use per-US **Project**: and **Board**: fields instead (see below)
---
```

**⛔ CRITICAL RULE: Every User Story MUST have `**Project**:` field!**

This is MANDATORY in BOTH single-project AND multi-project modes.

**Core Sections** (Always Present):
```markdown
# Product Specification: [Increment Name]

**Increment**: [ID]
**Title**: [Title]
**Status**: Planning
**Priority**: [P0-P3]
**Created**: [Date]

## Executive Summary
[1-2 paragraph overview]

## Problem Statement
### Current State
### User Pain Points
### Target Audience

## User Stories & Acceptance Criteria

<!--
⛔ MANDATORY: **Project**: field on EVERY User Story
- Single-project: Use config.project.name value
- Multi-project: Use one of multiProject.projects keys
NEVER generate a User Story without **Project**: field!
-->

### US-001: [Title]
**Project**: [MANDATORY - use config.project.name or multiProject.projects key]
**Board**: [MANDATORY for 2-level structures only]

**As a** [user type]
**I want** [goal]
**So that** [benefit]

**Acceptance Criteria**:
- [ ] **AC-US1-01**: [Criterion 1]
- [ ] **AC-US1-02**: [Criterion 2]

---

### MANDATORY STEP 0: Get Project Context FIRST

**⛔ YOU CANNOT GENERATE spec.md UNTIL YOU COMPLETE THIS STEP!**

**This step is BLOCKING - do not proceed until you have actual project/board IDs.**

**🧠 ULTRATHINK REQUIRED - ANALYZE ALL AVAILABLE CONTEXT FIRST!**

Before assigning ANY project, you MUST analyze:
1. **Living docs structure**: `ls .specweave/docs/internal/specs/` - what project folders exist?
2. **Recent increments**: `grep -r "^\*\*Project\*\*:" .specweave/increments/*/spec.md | tail -10`
3. **config.json**: Read `project.name` (single-project) or `multiProject.projects` (multi-project)
4. **Feature description**: What does the user want to build? Match to existing projects.

**1. Run the context API command:**
```bash
specweave context projects
```

**2. Parse the JSON output:**
```json
{
  "level": 1,
  "projects": [{"id": "frontend-app", "name": "Frontend App"}],
  "detectionReason": "multiProject configuration"
}
```
For 2-level:
```json
{
  "level": 2,
  "projects": [{"id": "acme-corp", "name": "ACME Corp"}],
  "boardsByProject": {
    "acme-corp": [
      {"id": "digital-ops", "name": "Digital Operations"},
      {"id": "mobile-team", "name": "Mobile Team"}
    ]
  }
}
```

**3. 🧠 ULTRATHINK - SMART PROJECT RESOLUTION:**

**RESOLUTION PRIORITY (MUST FOLLOW THIS ORDER!):**
```
1. ✅ EXACT MATCH: config.project.name or multiProject.projects key → USE IT
2. ✅ LIVING DOCS: Existing folder in specs/ → USE THAT PROJECT ID
3. ✅ RECENT PATTERNS: Same feature type in past increments → USE SAME PROJECT
4. ⚠️  UNCERTAIN: Multiple valid options OR no clear match → ASK USER!
5. 🔄 FALLBACK: If all else fails → USE "default" (NEVER "specweave"!)
```

**⚠️ CRITICAL: IF UNCERTAIN - YOU MUST ASK THE USER!**
```
I found multiple potential projects for this feature:
- frontend-app (keywords: UI, form, React)
- backend-api (keywords: API, endpoint)

Which project should I assign to this feature?
```

**❌ NEVER DO THIS:**
- Silently assign to "specweave" (that's the framework name, not user's project!)
- Guess without analyzing context
- Skip asking when genuinely uncertain

**✅ CORRECT FALLBACK (when no projects configured):**
```
**Project**: default
```

**4. STORE the actual IDs for use in spec.md:**
```
RESOLVED_PROJECT = "frontend-app"  // from projects[].id
RESOLVED_BOARD = "digital-ops"     // from boardsByProject (2-level only)
```

**5. Now generate spec.md using RESOLVED values (NEVER placeholders!)**

---

### Per-US Project Resolution (MANDATORY)

**🧠 USE CONTEXT API OUTPUT + LIVING DOCS TO RESOLVE PROJECT/BOARD:**

After running `specweave context projects`, you have the valid project/board IDs.
Now map each user story to the correct project:

**Resolution Flow:**
```
1. Get valid projects from context API: ["frontend-app", "backend-api", "shared"]
2. Analyze feature description for keywords
3. Map keywords to ACTUAL project IDs (from step 1, NOT generic terms!)
4. Assign each US to its project
```

**Resolution Example:**
```
Context API returned: projects = ["frontend-app", "backend-api", "shared"]

Feature: "Add OAuth login to React frontend"
Detected keywords: "React", "frontend", "login"

Mapping:
- "frontend" keyword → matches "frontend-app" (from context API)
- "login" spans frontend + backend

Result:
  US-001 (Login UI) → **Project**: frontend-app
  US-002 (Auth API) → **Project**: backend-api
```

**VALIDATION RULES:**

```
✅ REQUIRED: Run "specweave context projects" BEFORE generating spec.md
✅ REQUIRED: Use ONLY project IDs from the API response
✅ REQUIRED: Each US has explicit **Project**: field with resolved value
✅ REQUIRED: For 2-level, each US has explicit **Board**: field with resolved value

❌ FORBIDDEN: Generating spec.md without running context API first
❌ FORBIDDEN: Using {{PROJECT_ID}} or {{BOARD_ID}} placeholders
❌ FORBIDDEN: Using generic keywords as project names ("frontend" vs "frontend-app")
❌ FORBIDDEN: Inventing project names not in the API response
```

## Success Metrics
[How we'll measure success]

## Non-Goals (Out of Scope)
[What we're NOT doing in this increment]
```

**Flexible Sections** (Context-Dependent):
- **Competitive Analysis** (if new product)
- **Technical Requirements** (if complex feature)
- **API Design** (if backend API)
- **UI/UX Requirements** (if frontend)
- **Security Considerations** (if auth/data)
- **Migration Plan** (if breaking change)

### 2. Technical Plan Generation (plan.md)

**Adapts to Complexity**:
- **Simple Feature**: Component list, data flow, implementation steps
- **Complex System**: Full architecture, C4 diagrams, sequence diagrams, ER diagrams
- **Infrastructure**: Deployment architecture, scaling strategy, monitoring

**Core Sections**:
```markdown
# Technical Plan: [Increment Name]

## Architecture Overview
[System design, components, interactions]

## Component Architecture
### Component 1
[Purpose, responsibilities, interfaces]

## Data Models
[Entities, relationships, schemas]

## Implementation Strategy
### Phase 1: [Name]
### Phase 2: [Name]

## Testing Strategy
[Unit, integration, E2E approach]

## Deployment Plan
[How we'll roll this out]

## Risks & Mitigations
```

### 3. Task Breakdown Generation (tasks.md)

**Smart Task Creation**:
```markdown
# Implementation Tasks: [Increment Name]

## Task Overview
**Total Tasks**: [N]
**Estimated Duration**: [X weeks]
**Priority**: [P0]

---

## Phase 1: Foundation (Week 1) - X tasks

### T-001: [Task Title]
**Priority**: P0
**Estimate**: [X hours]
**Status**: pending

**Description**:
[What needs to be done]

**Files to Create/Modify**:
- `path/to/file.ts`

**Implementation**:
```[language]
[Code example or approach]
```

**Acceptance Criteria**:
- ✅ [Criterion 1]
- ✅ [Criterion 2]

---

[Repeat for all tasks]

## Task Dependencies
[Dependency graph if complex]
```

### 4. Test Strategy Generation (tests.md)

**Comprehensive Test Coverage**:
```markdown
# Test Strategy: [Increment Name]

## Test Overview
**Total Test Cases**: [N]
**Test Levels**: [Unit, Integration, E2E, Performance]
**Coverage Target**: 80%+ overall, 90%+ critical

---

## Unit Tests (X test cases)

### TC-001: [Test Name]
```[language]
describe('[Component]', () => {
  it('[should do something]', async () => {
    // Arrange
    // Act
    // Assert
  });
});
```

## Integration Tests (X test cases)
## E2E Tests (X test cases)
## Performance Tests (X test cases)

## Coverage Requirements
- Critical paths: 90%+
- Overall: 80%+
```

---

## Spec Generator Templates

### Template Selection Logic

**Input Analysis**:
1. Analyze increment description (keywords, complexity)
2. Detect domain (frontend, backend, infra, ML, etc.)
3. Determine scope (feature, product, bug fix, refactor)
4. Assess technical complexity (simple, moderate, complex)

**Template Selection**:
```
IF new_product THEN
  spec_template = "Full PRD"
  plan_template = "System Architecture"
ELSE IF feature_addition THEN
  spec_template = "User Stories Focused"
  plan_template = "Component Design"
ELSE IF bug_fix THEN
  spec_template = "Problem-Solution"
  plan_template = "Implementation Steps"
ELSE IF refactoring THEN
  spec_template = "Current-Proposed"
  plan_template = "Migration Strategy"
END IF
```

### Context-Aware Sections

**Auto-Include Based On**:
- **"authentication"** → Security Considerations, JWT/OAuth design
- **"API"** → API Design, OpenAPI spec, rate limiting
- **"database"** → ER diagrams, migration scripts, indexes
- **"frontend"** → Component hierarchy, state management, UI/UX
- **"deployment"** → CI/CD, infrastructure, monitoring
- **"ML"** → Model architecture, training pipeline, evaluation metrics

---

## Usage Examples

### Example 1: Simple Feature
```
User: /sw:inc "Add dark mode toggle to settings"

Spec Generator:
✓ Detected: Frontend feature (UI component)
✓ Complexity: Simple
✓ Template: User Stories + Component Design

Generating specifications...
✓ spec.md: 3 user stories, UI mockups section
✓ plan.md: Component design, state management, CSS-in-JS
✓ tasks.md: 8 tasks (component, styles, state, tests)
✓ tests.md: Unit tests for component, E2E for toggle
```

### Example 2: Complex System
```
User: /sw:inc "Multi-tenant SaaS platform with billing"

Spec Generator:
✓ Detected: New product (SaaS, multi-tenant, payments)
✓ Complexity: High
✓ Template: Full PRD + System Architecture

Generating specifications...
✓ spec.md: Market analysis, personas, competitive landscape, 15 user stories
✓ plan.md: Multi-tenant architecture, database per tenant, Stripe integration, C4 diagrams
✓ tasks.md: 40 tasks across 4 weeks (auth, tenancy, billing, UI)
✓ tests.md: 100+ test cases (unit, integration, E2E, load testing)
```

### Example 3: Bug Fix
```
User: /sw:inc "Fix race condition in user session handling"

Spec Generator:
✓ Detected: Bug fix (concurrency issue)
✓ Complexity: Moderate
✓ Template: Problem-Solution

Generating specifications...
✓ spec.md: Problem statement, root cause analysis, impact, solution
✓ plan.md: Current implementation, proposed fix, Redis locking
✓ tasks.md: 5 tasks (analysis, fix, tests, rollout, monitoring)
✓ tests.md: Concurrency tests, stress tests
```

---

## Integration with /sw:inc

The Spec Generator is automatically invoked by `/sw:inc`:

1. **User Intent Analysis**:
   - Analyze increment description
   - Detect keywords, domain, complexity

2. **Template Selection**:
   - Choose appropriate templates
   - Auto-include relevant sections

3. **Specification Generation**:
   - Generate spec.md with PM context
   - Generate plan.md with Architect context
   - Generate tasks.md with breakdown
   - Generate tests.md with coverage strategy

4. **User Review**:
   - Show generated structure
   - Allow refinement
   - Confirm before creating files

---

## Advantages Over Rigid Templates

**Flexible (V2) Approach**:
- ✅ Adapts to increment type (product, feature, bug fix, refactor)
- ✅ Includes only relevant sections
- ✅ Scales complexity up/down
- ✅ Domain-aware (frontend, backend, ML, infra)
- ✅ Faster for simple increments
- ✅ Comprehensive for complex products

**Rigid (V1) Approach**:
- ❌ Same template for everything
- ❌ Many irrelevant sections
- ❌ Wastes time on simple features
- ❌ Insufficient for complex products
- ❌ One-size-fits-none

---

## Configuration

Users can customize spec generation in `.specweave/config.yaml`:

```yaml
spec_generator:
  # Default complexity level
  default_complexity: moderate  # simple | moderate | complex

  # Always include sections
  always_include:
    - executive_summary
    - user_stories
    - success_metrics

  # Never include sections
  never_include:
    - competitive_analysis  # We're not doing market research

  # Domain defaults
  domain_defaults:
    frontend:
      include: [ui_mockups, component_hierarchy, state_management]
    backend:
      include: [api_design, database_schema, authentication]
```

---

## 🔀 Multi-Project User Story Generation

**CRITICAL**: When umbrella/multi-project mode is detected, user stories MUST be generated per-project!

### Detection (MANDATORY FIRST STEP)

**Automated Detection**: Use `detectMultiProjectMode(projectRoot)` from `src/utils/multi-project-detector.ts`. This utility checks ALL config formats automatically.

**Manual check (for agents)**: Read `.specweave/config.json` and check:
- `umbrella.enabled` + `childRepos[]`
- `multiProject.enabled` + `projects{}`
- `sync.profiles[].config.boardMapping`
- Multiple folders in `.specweave/docs/internal/specs/`

**If ANY of these conditions are TRUE → Multi-project mode ACTIVE:**
- `umbrella.enabled: true` in config.json
- `umbrella.childRepos` has entries
- Multiple project folders exist in `specs/` (e.g., `sw-app-fe/`, `sw-app-be/`, `sw-app-shared/`)
- User prompt mentions: "3 repos", "frontend repo", "backend API", "shared library"

### Per-User-Story Project Targeting (PREFERRED)

Each user story specifies its target project inline:

```markdown
## User Stories

### US-001: Thumbnail Upload & Comparison (P1)
**Project**: frontend-app
**Board**: ui-team        <!-- 2-level structures only -->
**As a** content creator
**I want** to upload multiple thumbnail variants
**So that** I can visually evaluate my options

**Acceptance Criteria**:
- [ ] **AC-US1-01**: User can drag-and-drop up to 5 images

---

### US-002: CTR Prediction API (P1)
**Project**: backend-api
**Board**: ml-team        <!-- 2-level structures only -->
**As a** frontend application
**I want** to call POST /predict-ctr endpoint
**So that** I can get AI-powered predictions

**Acceptance Criteria**:
- [ ] **AC-US2-01**: POST /predict-ctr accepts thumbnail image
```

**Benefits of per-US targeting:**
- Each US syncs to correct project/repo
- Single increment can span multiple projects
- Living docs auto-grouped by project
- External tools (GitHub/JIRA/ADO) receive issues in correct project

### Multi-Project User Story Format (with **Project**: per US)

**✅ CORRECT Format - Every US has `**Project**:`:**
```markdown
## User Stories

### US-001: Thumbnail Upload
**Project**: frontend-app       # ← MANDATORY!
**As a** content creator
**I want** to upload thumbnails
**So that** I can test different versions

**Acceptance Criteria**:
- [ ] **AC-US1-01**: User can drag-and-drop images
- [ ] **AC-US1-02**: Images validated for YouTube specs

### US-002: Thumbnail Analysis API
**Project**: backend-api        # ← MANDATORY! Different project = different folder
**As a** frontend application
**I want** to call POST /predict-ctr endpoint
**So that** I can get AI-powered predictions

**Acceptance Criteria**:
- [ ] **AC-US2-01**: POST /predict-ctr endpoint accepts thumbnail image
- [ ] **AC-US2-02**: ML model returns prediction score
```

### Project Classification Rules

When analyzing user descriptions, classify each user story by keywords:

| Keywords | Project | Prefix |
|----------|---------|--------|
| UI, component, page, form, view, drag-drop, theme, builder, menu display | Frontend | FE |
| API, endpoint, CRUD, webhook, analytics, database, service, ML model | Backend | BE |
| types, schemas, validators, utilities, localization, common | Shared | SHARED |
| iOS, Android, mobile app, push notification | Mobile | MOBILE |
| Terraform, K8s, Docker, CI/CD, deployment | Infrastructure | INFRA |

### AC-ID Format by Project

```
AC-{PROJECT}-US{story}-{number}

Examples:
- AC-FE-US1-01 (Frontend, User Story 1, AC #1)
- AC-BE-US1-01 (Backend, User Story 1, AC #1)
- AC-SHARED-US1-01 (Shared, User Story 1, AC #1)
- AC-MOBILE-US1-01 (Mobile, User Story 1, AC #1)
```

### tasks.md Must Reference Project-Scoped User Stories

```markdown
### T-001: Create Thumbnail Upload Component
**User Story**: US-FE-001           ← MUST reference project-scoped ID!
**Satisfies ACs**: AC-FE-US1-01, AC-FE-US1-02
**Status**: [ ] Not Started

### T-004: Database Schema & Migrations
**User Story**: US-BE-001, US-BE-002   ← Backend stories only!
**Satisfies ACs**: AC-BE-US1-01, AC-BE-US2-01
**Status**: [ ] Not Started
```

### Workflow Summary

```
1. DETECT multi-project mode (check config.json, folder structure)
   ↓
2. If multi-project → Group user stories by project (FE/BE/SHARED/MOBILE/INFRA)
   ↓
3. Generate prefixed user stories: US-FE-001, US-BE-001, US-SHARED-001
   ↓
4. Generate prefixed ACs: AC-FE-US1-01, AC-BE-US1-01
   ↓
5. Generate tasks referencing correct project user stories
   ↓
6. Each project folder gets its own filtered spec
```

### Why This Matters

Without project-scoped stories:
- ❌ All issues created in ONE repo (wrong!)
- ❌ No clarity which team owns what
- ❌ Tasks reference wrong user stories
- ❌ GitHub sync broken across repos

With project-scoped stories:
- ✅ Each repo gets only its user stories
- ✅ Clear ownership per team/repo
- ✅ GitHub issues in correct repo
- ✅ Clean separation of concerns

---

## Related Skills

- **Planning workflow**: Guides increment planning (uses Spec Generator internally)
- **Context loading**: Loads relevant context for specification generation
- **Quality validation**: Validates generated specifications for completeness
- **multi-project-spec-mapper**: Splits specs into project-specific files
- **umbrella-repo-detector**: Detects multi-repo architecture

---

---

Based on: Flexible Spec Generator (V2) - context-aware, non-rigid templates

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/spec-generator.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

