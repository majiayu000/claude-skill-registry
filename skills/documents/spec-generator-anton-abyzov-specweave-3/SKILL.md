---
description: Generates comprehensive specifications (spec.md, plan.md, tasks.md with embedded tests) for SpecWeave increments. Use when creating new increments, planning features, or converting ideas into actionable specs. Produces structured documentation with proven templates and context-aware organization.
---

# Spec Generator - Flexible Increment Documentation

**Purpose**: Generate spec.md, plan.md, tasks.md with embedded tests for SpecWeave increments.

**When to Use**: Creating increments (`/sw:inc`), planning features, converting ideas into specs.

---

## MANDATORY STEP 0: Get Project Context FIRST

**This step is BLOCKING — do not proceed until you have actual project/board IDs.**

1. **Run**: `specweave context projects`
2. **Parse** the JSON output for project IDs and (if 2-level) board IDs
3. **Resolve** each user story to correct project using this priority:
   - EXACT MATCH from config → use it
   - LIVING DOCS folder match → use it
   - RECENT PATTERNS in past increments → use same
   - UNCERTAIN → ASK USER (never guess!)
   - FALLBACK → use "default" (never "specweave")

**VALIDATION**: Every US MUST have `**Project**:` field with resolved value. Never use placeholders.

---

## 1. Spec Generation (spec.md)

**Adapts to Context**: New Product (full PRD) | Feature Addition (focused stories) | Bug Fix (problem-solution) | Refactoring (current-proposed)

**YAML Frontmatter**:
```yaml
---
increment: 0001-feature-name
title: "Feature Title"
type: feature
priority: P1
status: planned
created: 2025-12-04
---
```

**Core Sections**: Executive Summary, Problem Statement, User Stories & Acceptance Criteria, Success Metrics, Non-Goals.

**Per-US Format**:
```markdown
### US-001: [Title]
**Project**: [MANDATORY - resolved from Step 0]
**Board**: [MANDATORY for 2-level only]

**As a** [user type]
**I want** [goal]
**So that** [benefit]

**Acceptance Criteria**:
- [ ] **AC-US1-01**: [Criterion]
```

**Flexible Sections** (auto-include by context): Competitive Analysis, Technical Requirements, API Design, UI/UX, Security, Migration Plan.

## 2. Technical Plan (plan.md)

Core sections: Architecture Overview, Component Architecture, Data Models, Implementation Strategy (phased), Testing Strategy, Deployment Plan, Risks & Mitigations.

## 3. Task Breakdown (tasks.md)

```markdown
### T-001: [Task Title]
**User Story**: US-001 | **Satisfies ACs**: AC-US1-01
**Status**: [ ] Not Started
**Test**: Given [X] → When [Y] → Then [Z]
```

## Multi-Project User Story Generation

When multi-project mode detected (config `multiProject.enabled`, multiple `specs/` folders, or user mentions multiple repos):

- Group user stories by project (FE/BE/SHARED/MOBILE/INFRA)
- Use prefixed IDs: `US-FE-001`, `AC-FE-US1-01`
- Each US specifies `**Project**:` inline
- Tasks reference project-scoped story IDs

| Keywords | Project |
|----------|---------|
| UI, component, page, form, view | Frontend |
| API, endpoint, CRUD, webhook, service | Backend |
| types, schemas, validators, utilities | Shared |
| iOS, Android, mobile, push notification | Mobile |
| Terraform, K8s, Docker, CI/CD | Infrastructure |
