---
name: architect-phase
description: Takes user stories and enriches them with implementation details, patterns, and file references. Spawns architect to add API endpoints, database models, component names, and cross-cutting concerns. Use when converting high-level stories to architecture-annotated specifications ready for execution.
---

# Architect Phase Skill

> **ROOT AGENT ONLY** - Spawns architect agent, runs only from root Claude Code agent.

**Purpose:** Enrich user stories with implementation architecture details
**Trigger:** After design-phase completes (stories extracted and PR approved)
**Input:** `storiesFolder` (string), `projectFolder` (string), `complexity` (int), `scope` (object), `tools` (string[])
**Output:** `{enrichedStories, architectureNotes, patternReferences}`

---

## Workflow

**1. Spawn architect agent (enrichment mode)**

- Read all story files from `storiesFolder`
- For each story:
  - Identify story requirements and acceptance criteria
  - Check multi-mono for existing solutions (if applicable)
  - Find example files in reference repos (from scope)
  - Validate patterns against Context7 docs (if external libraries used)
  - Add "Architecture Details" section with:
    - **API Endpoints:** Routes and methods (e.g., `POST /api/users`)
    - **Files to Create/Modify:** Exact paths (e.g., `services/auth/routes.ts`)
    - **Import Statements:** Key dependencies needed
    - **Database Models:** Schemas or ORM definitions
    - **Component Names:** React/UI component references
    - **Patterns:** Reference existing patterns from codebase
- Save updated story files
- Return paths to all enriched stories

**2. Generate cross-cutting concerns document (if needed)**

- If stories have complex interdependencies:
  - Create `architecture-notes.md` in project folder
  - Document shared patterns, middleware, utilities
  - Add dependency graph or integration points
- Complexity ≥30 → deeper analysis mode

**3. Output enriched stories**

- Return list of enriched story file paths
- Return architecture notes path (if created)
- Return list of pattern references found

---

## Architecture Annotation Pattern

**Story File (before):**

```markdown
# User Story: Admin Dashboard Setup

**As a** system administrator
**I want to** view a dashboard showing system metrics
**So that** I can monitor application health

## Acceptance Criteria

- Dashboard displays CPU usage, memory, and response times
- Data refreshes every 10 seconds
- Show metrics for last 24 hours
```

**Story File (after architect annotation):**

````markdown
# User Story: Admin Dashboard Setup

**As a** system administrator
**I want to** view a dashboard showing system metrics
**So that** I can monitor application health

## Acceptance Criteria

- Dashboard displays CPU usage, memory, and response times
- Data refreshes every 10 seconds
- Show metrics for last 24 hours

## Architecture Details

- **API Endpoints:**
  - `GET /api/admin/metrics` - Returns system metrics
  - `GET /api/admin/metrics/history?range=24h` - Historical data

- **Files to Create/Modify:**
  - `services/admin/routes/metrics.routes.ts`
  - `services/admin/controllers/metrics.controller.ts`
  - `web/src/pages/AdminDashboard.tsx`
  - `web/src/components/MetricsCard.tsx`

- **Import Statements:**
  ```typescript
  import { metricsService } from "@shared/services/metrics";
  import { formatMetrics } from "@shared/utils/formatting";
  ```
````

- **Database Models:**
  - `MetricsSnapshot` - stores timestamp, cpu, memory, responseTime
  - Index on `createdAt` for range queries

- **Component Names:**
  - `AdminDashboard` - main page
  - `MetricsCard` - metric display card
  - `RefreshButton` - 10s auto-refresh trigger

- **Patterns:**
  - Real-time updates: WebSocket with fallback to polling (see `rugby-crm` for similar pattern)
  - Data formatting: Use `@shared/utils/formatting` (consistent with existing code)
  - API error handling: Standard error middleware (see `services/common/middleware`)

````

---

## Input Specification

```json
{
  "storiesFolder": "docs/epics/in-progress/msm-feature/user-stories/",
  "projectFolder": "docs/epics/in-progress/msm-feature/",
  "complexity": 26,
  "scope": {
    "targets": ["/home/user/code/metasaver-com"],
    "references": ["/home/user/code/rugby-crm"]
  },
  "tools": ["serena"]
}
````

---

## Output Specification

```json
{
  "enrichedStories": ["user-stories/msm-feat-001-database-schema.md", "user-stories/msm-feat-002-contracts-types.md", "user-stories/msm-feat-003-workflow-scaffolding.md"],
  "architectureNotes": "architecture-notes.md",
  "patternReferences": [
    {
      "story": "msm-feat-003",
      "pattern": "Real-time updates",
      "reference": "rugby-crm/src/features/notifications",
      "reason": "Similar WebSocket + polling pattern"
    }
  ]
}
```

---

## Key Guidelines

**1. Pattern Discovery:**

- Always check scope.references for existing implementations
- Reference file paths explicitly (helps execution phase locate code)
- Call out shared utilities and middleware

**2. File Organization:**

- Follow existing project structure
- Use established naming conventions (services/, controllers/, components/)
- Group related files by feature

**3. Import Statements:**

- Include enough detail to guide code generation
- Use actual import paths from codebase
- Call out shared packages or internal utilities

**4. Database Modeling:**

- Include ORM-specific syntax if applicable (Prisma, TypeORM, etc.)
- Specify indexes for performance-critical queries
- Document relationships between models

**5. Conciseness:**

- Total architect work: 50-100 lines max
- Point to reference repos instead of duplicating patterns
- Use tables/lists, not prose

---

## Integration

**Called by:**

- `/build` command (after design-phase approval)
- `/ms` command (complexity ≥15, after design-phase approval)

**Calls:**

- `architect` agent (enrichment mode, complexity-aware model)

**Next step:** execution-phase (workers read enriched stories and implement)

---

## Example Workflow

```
Design Phase Output:
  stories/
    msm-feat-001-database-schema.md
    msm-feat-002-contracts-types.md
    msm-feat-003-workflow-scaffolding.md

Architect Phase (this skill):
  → Read scope: targets=[metasaver-com], references=[rugby-crm]
  → For each story:
    - Check rugby-crm for similar patterns
    - Add API endpoints
    - List files to create/modify
    - Add import statements
    - Specify database models
    - Reference components
  → Save enriched stories
  → Create architecture-notes.md for cross-cutting concerns

Output:
  {
    enrichedStories: [msm-feat-001-enriched.md, msm-feat-002-enriched.md, ...],
    architectureNotes: "architecture-notes.md",
    patternReferences: [...]
  }

Execution Phase:
  → Workers read enriched stories
  → Execute story-by-story with full architecture context
  → Create/modify files listed in Architecture Details
```

---

## Common Patterns to Enrich

| Pattern                   | Details to Add                                        |
| ------------------------- | ----------------------------------------------------- |
| REST API                  | Endpoint, method, request/response format, validation |
| Database Schema           | Models, fields, indexes, relationships                |
| React Component           | Component name, props, state, child components        |
| Service Layer             | Service class, methods, error handling                |
| Middleware                | Integration point, purpose, parameters                |
| Utility Functions         | Function signature, usage examples, performance notes |
| Cross-service Integration | API contract, error handling, retry logic             |

---

## Checklist for Architect

- [ ] All stories have Architecture Details section
- [ ] API endpoints match project conventions
- [ ] Files paths use correct directory structure
- [ ] Import statements are accurate and complete
- [ ] Database models include required fields and indexes
- [ ] Component names follow naming conventions
- [ ] Pattern references point to actual code locations
- [ ] Cross-cutting concerns documented (if complex)
- [ ] No duplication of patterns (reference instead)
