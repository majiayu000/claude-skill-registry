---
name: arch-orchestrator
description: Use when the user says "create architecture plan/specs", "turn this brief into docs", "generate frontend/backend/api specs", or "write the spec markdown files". Triggers on requests for end-to-end software architecture documentation from a product brief.
---

# Architecture Orchestrator

## Overview

Turn a raw product brief into a consistent, implementation-ready spec pack under `specs/` by coordinating specialist agents **and** enforcing a project's preferred stack (frontend, backend, and AI).

## When to Use

- User provides a software brief and wants full project architecture/spec docs
- User wants "screen-by-screen + backend + API + AI" markdown files
- User says "create architecture", "generate specs", "turn my brief into documentation"
- User wants an **opinionated** stack (design system + deployment platform) applied consistently across the whole spec pack

## When NOT to Use

- Simple one-off questions about architecture patterns
- When user already has spec files and just needs edits
- Code implementation tasks (use after specs are approved)

---

## Preference System (SOURCE OF TRUTH)

### 1) Preference File Search Order

1. `specs/preferences.yaml` (recommended)
2. `specs/preferences.json`
3. `.arch-orchestrator/preferences.yaml`
4. `.arch-orchestrator/preferences.json`

If none exist, **create** `specs/preferences.yaml` using the default template (see `templates/preferences.example.yaml`), and record this in `specs/decisions.md`.

### 2) Design System Sources Search Order

1. `design-system/` folder (any of: `README.md`, `tokens.*`, `components.*`, `patterns.*`, `a11y.*`)
2. `specs/design-system-source.md`
3. `docs/design-system.md`

If none exist, generate `specs/design-system.md` as a "Design system not provided" doc.

### 3) How Preferences Are Applied

- Treat preferences as **hard constraints** unless explicitly marked as optional
- Every generated spec must include:
  - The chosen packages/libraries and *why* they exist in the architecture
  - How they are wired into the repo
  - Any constraints they impose (build/deploy/runtime limits)
- Subagents must be instructed to **read and comply** with `specs/preferences.yaml` first, then the brief

---

## Output Contract (MUST)

Create (or update) these files in `specs/`:

| File | Purpose |
|------|---------|
| `specs/index.md` | Navigation hub with links to all specs |
| `specs/brief-normalized.md` | Structured extraction of the product brief |
| `specs/preferences.yaml` | Stack preferences (create if missing) |
| `specs/design-system.md` | Design tokens, components, a11y rules |
| `specs/frontend-specs.md` | Screen-by-screen UI specifications |
| `specs/backend-specs.md` | Domain model, services, database schema |
| `specs/api-docs.md` | Endpoint documentation with schemas |
| `specs/ai-services.md` | AI/LLM features (or "Not in scope") |
| `specs/decisions.md` | Architectural decisions and rationale |
| `specs/open-questions.md` | Uncertainties needing clarification |

---

## Workflow

### Phase 0: Load Preferences + Design System

1. **Load preferences**
   - Find and parse a preference file using the search order above
   - If missing, create `specs/preferences.yaml` using the default template
   - Normalize into a short "Stack Summary" section for all specs

2. **Load design system sources**
   - If `design-system/` exists, summarize it into `specs/design-system.md`
   - If only a doc exists, consolidate it
   - If nothing exists, produce a default DS doc matching chosen UI libraries

3. **Propagate constraints**
   - Every Task prompt must include: "Follow `specs/preferences.yaml` as hard constraints."

### Phase 1: Normalize the Brief

1. **Locate the brief**
   - Look for: `brief.md`, `spec.md`, `requirements.md`, `product-brief.md`
   - If not found, ask user where it is

2. **Extract and structure**
   - Project name and purpose
   - Goals and non-goals
   - User roles and personas
   - Key workflows and user journeys
   - Technical constraints (merge with preferences; preferences win)
   - Required integrations
   - Success metrics

3. **Write `specs/brief-normalized.md`**

### Phase 2: Define Shared Foundations (Backend First)

Write `specs/backend-specs.md` first with:

1. **Canonical domain model** (SOURCE OF TRUTH)
   - Core entities with fields, types, constraints
   - Relationships between entities

2. **Platform blueprint** (from preferences)
   - Compute layer selection rationale
   - Storage selection (D1 vs KV vs R2 vs Durable Objects)
   - Deployment model and environment separation

3. **Auth/authz model** (from preferences)
   - Authentication approach (JWT, session, OAuth)
   - Authorization model (RBAC, ABAC)
   - Multi-tenancy strategy

4. **Error conventions**
   - Standard error envelope format
   - HTTP status code usage
   - Error code taxonomy

5. **Observability + operations** (from preferences)
   - Logging, error tracking, metrics
   - Analytics approach

6. **Complete the backend spec**
   - Services architecture
   - Database schema with indexes
   - Background jobs and queues
   - Security and rate limiting

### Phase 3: Spawn Specialist Agents (Preference-Aware)

Use the Task tool to spawn agents in parallel:

**API Documentation Agent:**
```
Task tool with:
- subagent_type: "general-purpose"
- prompt: "Create comprehensive API documentation in specs/api-docs.md.
          HARD CONSTRAINTS: Follow specs/preferences.yaml.
          Reference the canonical domain model from specs/backend-specs.md.
          Include all endpoints with request/response schemas, auth requirements,
          error handling, and pagination conventions."
```

**Frontend Specs Agent:**
```
Task tool with:
- subagent_type: "general-purpose"
- prompt: "Create granular frontend specifications in specs/frontend-specs.md.
          HARD CONSTRAINTS: Follow specs/preferences.yaml and specs/design-system.md.
          Use the preferred UI component source and icon strategy.
          Reference entities from specs/backend-specs.md and endpoints from specs/api-docs.md.
          Provide screen-by-screen breakdown with component-level detail."
```

**AI Services Agent** (ONLY if AI features mentioned or ai.enabled=true):
```
Task tool with:
- subagent_type: "general-purpose"
- prompt: "Create AI services architecture in specs/ai-services.md.
          HARD CONSTRAINTS: Follow specs/preferences.yaml.
          Include AI feature inventory, model gateway, prompt management, RAG strategy,
          safety guardrails, evaluation framework, and cost controls."
```

### Phase 4: Create Index and Decision Logs

1. **Index** (`specs/index.md`)
   - Navigation hub with links to all specs
   - One-paragraph summary per document
   - "Stack Summary" pulled from preferences

2. **Decisions** (`specs/decisions.md`)
   - All assumptions made
   - Rationale for key architectural choices
   - Stack choices (must match preferences)

3. **Open questions** (`specs/open-questions.md`)
   - Uncertainties needing clarification
   - Trade-offs to discuss with team

### Phase 5: Consistency Validation

Before finishing, verify:

- [ ] Preferences applied across FE/BE/API/AI specs
- [ ] Entity names identical across all specs
- [ ] API routes in frontend-specs.md exist in api-docs.md
- [ ] Permissions consistent (screen access = endpoint access)
- [ ] Data schemas match between FE/BE/API
- [ ] All agent tasks completed successfully
- [ ] All open questions captured

---

## Assumptions + Questions

Ask at most **5 critical questions** only if blockers exist:
- Must choose between fundamentally different approaches (e.g., session vs jwt)
- Must know tenancy model for multi-tenant apps
- Must clarify data residency / compliance requirements

Otherwise, proceed with explicit assumptions and document in `specs/decisions.md`.

---

## Error Handling

| Condition | Action |
|-----------|--------|
| Preferences missing | Create defaults, record in decisions.md |
| Design system missing | Generate default DS doc, record assumptions |
| Brief missing | Ask user where it is |
| Brief vague | Proceed with assumptions, document in decisions.md |
| AI features unclear | Default to ai.enabled preference; otherwise "not in scope" |
| Agent fails | Document issue in open-questions.md, continue with other specs |
