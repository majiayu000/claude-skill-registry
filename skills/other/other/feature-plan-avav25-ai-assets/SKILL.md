---
name: feature-plan
description: Plan feature implementation across services and roles — parse requirements, understand project architecture (ARCHITECTURE.md, CLAUDE.md), decompose into work packages per service/role, estimate complexity, produce an actionable implementation plan. Part of the umbrella feature workflow.
context: fork
argument-hint: [PRD or feature brief path]
---

# Feature Plan

Plan a feature implementation by understanding the project architecture, decomposing work into service-level and role-level packages, and producing an actionable plan. This is the **planning phase** — no code is written here. Output feeds into `/feature-dev` for execution.

## 1. Receive Feature Requirements

Gather the feature specification from the user:

- **Accepted formats**: PRD, ARD, design doc, implementation plan, ticket/issue, verbal description
- Read every provided document thoroughly
- Extract and organize:
  - **Goal**: What the feature does (1–2 sentences)
  - **Requirements**: Functional (what it does) and non-functional (performance, security, compliance)
  - **Acceptance criteria**: How to verify the feature works
  - **Constraints**: Deadlines, compatibility, dependencies on other teams/services
  - **Out of scope**: What this feature explicitly does NOT cover

If the specification is ambiguous or incomplete — ask before proceeding. Do not assume missing requirements.

## 2. Understand Project Architecture

Read and internalize the project's structure to plan correctly:

### 2a. Read Architecture Documentation

Read the following files (if they exist):

1. **`ARCHITECTURE.md`** — system overview, component boundaries, data flow, service map
2. **`CLAUDE.md`** (root) — tech stack declaration, project structure, conventions
3. **Subdirectory `CLAUDE.md` files** — per-service/module context and stack info

**Extract**:
- Service/module boundaries (monolith modules, microservices, frontend/backend split)
- Tech stack per service (language, framework, database, messaging)
- Communication patterns (REST, gRPC, events, shared DB)
- Data flow relevant to the feature
- Deployment topology (monorepo vs polyrepo, shared vs independent deploys)

### 2b. Scan Project Structure

If documentation is incomplete or absent, scan the filesystem:

```
// turbo
ls -la (or dir for Windows)
```

Look for:
- **Monorepo signals**: `packages/`, `services/`, `apps/`, root `package.json` with workspaces, Nx/Turborepo config
- **Polyrepo signals**: Single service, one `CLAUDE.md`, one tech stack
- **Infrastructure**: `terraform/`, `infra/`, `k8s/`, `helm/`, `docker-compose.yml`
- **Dependency files**: `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, `*.csproj` per service

### 2c. Build Service Map

Create a map of services/modules the feature touches:

```
## Service Map

| Service/Module | Tech Stack | Role | Affected by Feature |
|---|---|---|---|
| [name] | [lang + framework] | @[role] | [yes/no — how] |
| [name] | [lang + framework] | @[role] | [yes/no — how] |
| infrastructure | Terraform / K8s | Agent(devops-engineer) | [yes/no — how] |
```

## 3. Decompose into Work Packages

Break the feature into **work packages** — each package is a self-contained unit of work scoped to one service/module and one role.

### 3a. Identify Work Streams

Group changes by responsibility:

| Work Stream | Role | Scope |
|---|---|---|
| **Frontend** | `Agent(frontend-engineer)` | UI components, pages, client-side logic, API integration |
| **Backend API** | `Agent(java-engineer)` / `Agent(python-engineer)` | Endpoints, business logic, data access, validation |
| **Data Layer** | `Agent(db-engineer)` | Database schema, migrations, queries, indexing, optimization |
| **Infrastructure** | `Agent(devops-engineer)` | Terraform, Docker, K8s, config, secrets |
| **Cloud Architecture** | `Agent(cloud-architect)` | Cloud platform design, landing zones, networking, cost optimization |
| **CI/CD Architecture** | `Agent(devops-architect)` | Pipeline design, deployment strategy, GitHub org governance, platform engineering |
| **ML / Data** | `Agent(ml-engineer)` | Models, pipelines, feature engineering. For LLM/RAG/agent features also consult `context-engineering` skill |
| **Data Pipelines** | `Agent(data-engineer)` | ETL/ELT, data warehousing, Spark, dbt, Airflow |
| **Mobile** | `Agent(mobile-engineer)` | React Native, Flutter, iOS, Android apps |
| **Marketing Content** | `Agent(marketing-strategist)` | Positioning, messaging, GTM, landing pages |
| **Architecture** | `Agent(system-architect)` | System design, ARCHITECTURE.md, component boundaries, tech selection |
| **Cross-cutting** | `Agent(software-engineer)` | Shared libraries, contracts, API specs |

Only include work streams that the feature actually requires. Do not add empty streams.

### 3b. Define Work Packages

For each work stream, create ordered work packages:

```
### [Work Stream]: [Service Name] — @[role]

#### WP-[N]: [Title]
- **Description**: What to implement
- **Files**: Expected files to create/modify
- **Dependencies**: Which WPs must complete first
- **Acceptance criteria**: How to verify this WP is done
- **Complexity**: S (hours) / M (day) / L (days) / XL (week+)
```

**Rules for decomposition**:
- Each WP is independently testable
- WPs within a stream are ordered by dependency (foundations first)
- Cross-service dependencies are explicitly marked
- Database migrations always come before code that uses them
- API contracts defined before consumer implementation

### 3c. Define Integration Points

For features spanning multiple services, explicitly document:

<integration_points>
- **API contracts**: Request/response schemas for new or modified endpoints
- **Events/messages**: New event types, payload schemas, producers, consumers
- **Shared types**: DTOs, enums, or constants shared across services
- **Database changes**: Schema migrations, new tables/columns, index requirements
- **Configuration**: New env vars, feature flags, secrets needed
</integration_points>

## 4. Dependency Graph

Visualize the execution order:

```
## Dependency Graph

WP-1: [DB migration]
  └─► WP-2: [Backend API]
        ├─► WP-3: [Frontend integration]
        └─► WP-4: [Infrastructure/config]
WP-5: [Tests] ← depends on WP-2, WP-3
```

Identify:
- **Critical path**: Longest chain of dependent WPs — determines minimum timeline
- **Parallelizable**: WPs that can be worked on simultaneously by different roles
- **Blockers**: External dependencies (other teams, third-party APIs, approvals)

## 5. Risk Assessment

Evaluate risks for each work stream:

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| [risk description] | High/Med/Low | High/Med/Low | [mitigation strategy] |

**Common risks to evaluate**:
- Breaking changes to existing APIs (backward compatibility)
- Database migration on large tables (performance, downtime)
- Cross-service coordination (deployment order matters)
- New dependencies or services (operational complexity)
- Security implications (new auth flows, data exposure)

## 6. Present the Plan

Compile the full plan and present to the user:

```
# Feature Plan: [Feature Name]

## Goal
[1–2 sentences]

## Architecture Impact
- Services affected: [list]
- New services: [if any]
- Database changes: [yes/no — summary]
- Infrastructure changes: [yes/no — summary]

## Work Packages

### Stream 1: [name] — @[role]
| WP | Title | Complexity | Dependencies | Status |
|----|-------|------------|--------------|--------|
| WP-1 | [title] | M | — | planned |
| WP-2 | [title] | S | WP-1 | planned |

### Stream 2: [name] — @[role]
| WP | Title | Complexity | Dependencies | Status |
|----|-------|------------|--------------|--------|
| WP-3 | [title] | L | WP-1 | planned |

## Critical Path
WP-1 → WP-2 → WP-5 (estimated: [timeframe])

## Risks
[table from Step 5]

## Next Step
Run `/feature-dev` per work package, applying the designated role.
```

Wait for user approval. The user may reorder, split, merge, or remove work packages.

## 7. Update FEATURES.md

After the plan is approved, **apply `Agent(product-manager)`** and update `FEATURES.md`:

1. If `FEATURES.md` does not exist — create it at the project root
2. Add or update the feature entry with status `planned`
3. If the feature has a PRD or spec — save it in `features/` directory and link from `FEATURES.md`

## 8. Handoff to Implementation

After approval, guide execution:

- **Sequential** (single developer): Execute WPs in dependency order using `/feature-dev` for each
- **Parallel** (multiple developers/sessions): Assign independent WPs to separate sessions, each applying the appropriate role
- Track WP status: `planned` → `in_progress` → `done`
- Update the plan if scope changes during implementation

## Integration

- **Input**: PRD, ARD, design doc, or user request
- **Preceded by**: `/feature-design` (produces PRD), `/architecture` (produces ARD, design docs, API contracts, engineering estimates)
- **Followed by**: `/feature-dev` (implementation per work package)
- **Roles**: `Agent(product-manager)` (requirements), `Agent(solution-architect)` / `Agent(system-architect)` (architecture), `Agent(cloud-architect)` (cloud platform), `Agent(devops-architect)` (CI/CD architecture), stack-specific roles (work packages)
- **Skills**: `context-engineering` skill (context pipeline design, RAG, memory, agent harness — for AI/LLM feature work packages)
