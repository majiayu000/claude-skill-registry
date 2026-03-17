---
name: ln-110-project-docs-coordinator
description: Coordinates project documentation creation. Gathers context once, detects project type, delegates to 5 L3 workers (ln-111-115). L2 Coordinator invoked by ln-100.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Project Documentation Coordinator

L2 Coordinator that gathers project context once and delegates document creation to specialized L3 workers.

## Purpose & Scope
- **Single context gathering** — analyzes project once, builds Context Store
- **Project type detection** — determines hasBackend, hasDatabase, hasFrontend, hasDocker
- **Delegates to 5 workers** — passes Context Store to each worker
- **Aggregates results** — collects status from all workers, returns summary
- Solves the "context loss" problem by gathering data once and passing explicitly

## Invocation (who/when)
- **ln-100-documents-pipeline:** Invoked as first L2 coordinator in documentation pipeline
- Never called directly by users

## Inputs

**From ln-100 (via Phase 0 Legacy Migration):**
```json
{
  "LEGACY_CONTENT": {
    "legacy_architecture": { "sections": [...], "diagrams": [...] },
    "legacy_requirements": { "functional": [...] },
    "legacy_principles": { "principles": [...], "anti_patterns": [...] },
    "legacy_tech_stack": { "frontend": "...", "backend": "...", "versions": {} },
    "legacy_api": { "endpoints": [...], "authentication": "..." },
    "legacy_database": { "tables": [...], "relationships": [...] },
    "legacy_runbook": { "prerequisites": [...], "install_steps": [...], "env_vars": [...] }
  }
}
```

**LEGACY_CONTENT** is passed to workers as base content. Priority: **Legacy > Auto-discovery > Template defaults**.

## Architecture

```
ln-110-project-docs-coordinator (this skill)
├── Phase 1: Context Gathering (ONE TIME)
├── Phase 2: Delegate to Workers
│   ├── ln-111-root-docs-creator → 4 root docs (ALWAYS)
│   ├── ln-112-project-core-creator → 3 core docs (ALWAYS)
│   ├── ln-113-backend-docs-creator → 2 docs (if hasBackend/hasDatabase)
│   ├── ln-114-frontend-docs-creator → 1 doc (if hasFrontend)
│   └── ln-115-devops-docs-creator → 1 doc (if hasDocker)
└── Phase 3: Aggregate Results
```

## Workflow

### Phase 1: Context Gathering (ONE TIME)

**1.1 Auto-Discovery (scan project files):**

| Source | Data Extracted | Context Store Keys |
|--------|----------------|-------------------|
| package.json | name, description, dependencies, scripts, engines, author, contributors | PROJECT_NAME, PROJECT_DESCRIPTION, DEPENDENCIES, DEV_COMMANDS, DEVOPS_CONTACTS |
| docker-compose.yml | services, ports, deploy.replicas, runtime:nvidia | DOCKER_SERVICES, DEPLOYMENT_SCALE, HAS_GPU |
| Dockerfile | runtime version | RUNTIME_VERSION |
| src/ structure | folders, patterns | SRC_STRUCTURE, ARCHITECTURE_PATTERN |
| migrations/ | table definitions | SCHEMA_OVERVIEW |
| .env.example | environment variables | ENV_VARIABLES |
| tsconfig.json, .eslintrc | conventions | CODE_CONVENTIONS |
| README.md | project description, scaling mentions | PROJECT_DESCRIPTION (fallback), DEPLOYMENT_SCALE (fallback) |
| CODEOWNERS | maintainers | DEVOPS_CONTACTS |
| git log | frequent committers | DEVOPS_CONTACTS (fallback) |

**1.2 Detect Project Type:**

| Flag | Detection Rule |
|------|----------------|
| hasBackend | express/fastify/nestjs/fastapi/django in dependencies |
| hasDatabase | pg/mongoose/prisma/sequelize in dependencies OR postgres/mongo in docker-compose |
| hasFrontend | react/vue/angular/svelte in dependencies |
| hasDocker | Dockerfile exists OR docker-compose.yml exists |

**1.3 User Materials Request:**
- Ask: "Do you have existing materials (requirements, designs, docs)?"
- If provided: Extract answers for Context Store

**1.4 MCP Research (for detected technologies):**
- Use Context7/Ref for best practices
- Store in Context Store for workers

**1.5 Build Context Store:**
```json
{
  "PROJECT_NAME": "my-project",
  "PROJECT_DESCRIPTION": "...",
  "TECH_STACK": { "frontend": "React 18", "backend": "Express 4.18", "database": "PostgreSQL 15" },
  "DEPENDENCIES": [...],
  "SRC_STRUCTURE": { "controllers": [...], "services": [...] },
  "ENV_VARIABLES": ["DATABASE_URL", "JWT_SECRET"],
  "DEV_COMMANDS": { "dev": "npm run dev", "test": "npm test" },
  "DOCKER_SERVICES": ["app", "db"],
  "DEPLOYMENT_SCALE": "single",
  "DEVOPS_CONTACTS": [],
  "HAS_GPU": false,
  "flags": { "hasBackend": true, "hasDatabase": true, "hasFrontend": true, "hasDocker": true }
}
```

**DEPLOYMENT_SCALE detection rules:**
- `"single"` (default): No deploy.replicas, no scaling keywords in README
- `"multi"`: deploy.replicas > 1 OR load balancer mentioned
- `"auto-scaling"`: auto-scaling keywords in README/docker-compose
- `"gpu-based"`: runtime: nvidia in docker-compose

**DEVOPS_CONTACTS fallback chain:**
1. CODEOWNERS file → extract maintainers
2. package.json author/contributors → extract names/emails
3. git log → top 3 frequent committers
4. If all empty → `[TBD: Provide DevOps team contacts]`

**1.6 Merge Legacy Content (if provided by ln-100):**
- Check if `LEGACY_CONTENT` was passed from ln-100 Phase 0
- If exists, merge into Context Store:
  ```
  contextStore.LEGACY_CONTENT = input.LEGACY_CONTENT
  ```
- Merge priority for workers:
  - `LEGACY_CONTENT.legacy_architecture` → used by ln-112 for architecture.md
  - `LEGACY_CONTENT.legacy_requirements` → used by ln-112 for requirements.md
  - `LEGACY_CONTENT.legacy_tech_stack` → merged with auto-discovered TECH_STACK
  - `LEGACY_CONTENT.legacy_principles` → used by ln-111 for principles.md
  - `LEGACY_CONTENT.legacy_api` → used by ln-113 for api_spec.md
  - `LEGACY_CONTENT.legacy_database` → used by ln-113 for database_schema.md
  - `LEGACY_CONTENT.legacy_runbook` → used by ln-115 for runbook.md
- If no LEGACY_CONTENT: workers use auto-discovery + template defaults

### Phase 2: Delegate to Workers

**2.1 Always invoke (parallel):**
- `ln-111-root-docs-creator` with Context Store
- `ln-112-project-core-creator` with full Context Store

**2.2 Conditionally invoke:**
- `ln-113-backend-docs-creator` if hasBackend OR hasDatabase
- `ln-114-frontend-docs-creator` if hasFrontend
- `ln-115-devops-docs-creator` if hasDocker

**Delegation Pattern:**
- Pass Context Store and flags to workers via direct Skill tool invocation
- Wait for completion
- Collect result (created, skipped, tbd_count, validation)

### Phase 3: Aggregate Results

1. Collect status from all workers
2. Sum totals: created files, skipped files, TBD markers
3. Report any validation warnings
4. Return aggregated summary to ln-100
5. **Include Context Store** for subsequent workers (ln-120 needs TECH_STACK)

**Output:**
```json
{
  "workers_invoked": 5,
  "total_created": 11,
  "total_skipped": 0,
  "total_tbd": 8,
  "validation_status": "OK",
  "files": [
    "CLAUDE.md",
    "docs/README.md",
    "docs/documentation_standards.md",
    "docs/principles.md",
    "docs/project/requirements.md",
    "docs/project/architecture.md",
    "docs/project/tech_stack.md",
    "docs/project/api_spec.md",
    "docs/project/database_schema.md",
    "docs/project/design_guidelines.md",
    "docs/project/runbook.md"
  ],
  "context_store": {
    "PROJECT_NAME": "...",
    "TECH_STACK": { "frontend": "React 18", "backend": "Express 4.18", "database": "PostgreSQL 15" },
    "DEPENDENCIES": [...],
    "flags": { "hasBackend": true, "hasDatabase": true, "hasFrontend": true, "hasDocker": true }
  }
}
```

## Critical Notes
- **Context gathered ONCE** — never duplicated in workers
- **Context Store passed explicitly** — no implicit state
- **Workers self-validate** — coordinator only aggregates
- **Idempotent** — workers skip existing files
- **Parallel where possible** — ln-111 and ln-112 can run in parallel

### Documentation Standards (passed to workers)
- **NO_CODE Rule:** Documents describe contracts, not implementations
- **Stack Adaptation:** Links must match TECH_STACK (Context Store)
- **Format Priority:** Tables/ASCII > Lists > Text

## Definition of Done
- Context Store built with all discovered data
- Project type flags determined
- All applicable workers invoked
- Results aggregated
- **Actuality verified:** all document facts match current code (paths, functions, APIs, configs exist and are accurate)
- Summary returned to ln-100

## Reference Files
- Guides: `references/guides/automatic_analysis_guide.md`, `critical_questions.md`, `troubleshooting.md`

---
**Version:** 2.1.0
**Last Updated:** 2025-01-12
