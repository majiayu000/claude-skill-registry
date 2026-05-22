---
name: ln-110-project-docs-coordinator
description: "Coordinates project documentation creation with single context gathering and project type detection. Use when generating project docs subset."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Project Documentation Coordinator

**Type:** L2 Coordinator
**Category:** 1XX Documentation Pipeline

Runtime-backed docs coordinator. The runtime owns context assembly checkpoints, conditional worker fan-out, and docs-generation summary aggregation.

## Purpose & Scope
- **Single context gathering** — analyzes project once, builds Context Store
- **Project type detection** — determines hasBackend, hasDatabase, hasFrontend, hasDocker
- **Delegates to 5 workers** — passes Context Store to each worker
- **Aggregates results** — collects status from all workers, returns summary
- Solves the "context loss" problem by gathering data once and passing explicitly
- Builds the routing table used by `ln-100` docs-quality repair loop

## Runtime Contract

**MANDATORY READ:** Load `references/coordinator_runtime_contract.md`, `references/docs_runtime_contract.md`, `references/docs_generation_summary_contract.md`

Runtime family: `docs-runtime`

Identifier:
- `project-docs`

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_CONTEXT_ASSEMBLY`
3. `PHASE_2_DETECTION`
4. `PHASE_3_DELEGATE`
5. `PHASE_4_AGGREGATE`
6. `PHASE_5_SELF_CHECK`

Worker summary contract:
- `ln-111..115` may receive `summaryArtifactPath`
- each worker writes or returns `docs-generation` summary envelope
- ln-110 consumes worker summaries, not free-text worker prose

## Invocation (who/when)
- **ln-100-documents-pipeline:** Invoked as first L2 coordinator in documentation pipeline
- Never called directly by users

## Inputs

**From ln-100 (optional source cleanup phase):**
```json
{
  "SOURCE_DOC_NOTES": {
    "architecture_notes": { "sections": [...], "diagrams": [...] },
    "requirements_notes": { "functional": [...] },
    "principles_notes": { "principles": [...], "anti_patterns": [...] },
    "tech_stack_notes": { "frontend": "...", "backend": "...", "versions": {} },
    "api_notes": { "endpoints": [...], "authentication": "..." },
    "database_notes": { "tables": [...], "relationships": [...] },
    "runbook_notes": { "prerequisites": [...], "install_steps": [...], "env_vars": [...] },
    "infrastructure_notes": { "servers": [...], "domains": [...], "ports": {} }
  }
}
```

`SOURCE_DOC_NOTES` enriches the standard context store before worker dispatch. Workers consume normalized context fields only; there is no legacy-specific override branch.

**MANDATORY READ:** Load `references/docs_quality_contract.md`.

## Architecture

```
ln-110-project-docs-coordinator (this skill)
├── Phase 1: Context Gathering (ONE TIME)
├── Phase 2: Delegate to Workers
│   ├── ln-111-root-docs-creator → 4 root docs (ALWAYS)
│   ├── ln-112-project-core-creator → 3 core docs (ALWAYS)
│   ├── ln-113-backend-docs-creator → 2 docs (if hasBackend/hasDatabase)
│   ├── ln-114-frontend-docs-creator → 1 doc (if hasFrontend)
│   └── ln-115-devops-docs-creator → 2 docs (1 always + 1 if hasDocker)
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
| ~/.ssh/config, deploy targets | SSH aliases, hostnames, IPs | SERVER_INVENTORY |
| docker-compose VIRTUAL_HOST vars | domain routing | DOMAIN_DNS |
| .env.example registry URLs, .npmrc | artifact repos | ARTIFACT_REPOSITORY |
| docker-compose deploy.resources | resource limits | HOST_REQUIREMENTS |

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
  "SERVER_INVENTORY": [],
  "DOMAIN_DNS": [],
  "ARTIFACT_REPOSITORY": {},
  "HOST_REQUIREMENTS": {},
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

**1.6 Merge Normalized Source Notes (if provided by ln-100):**
- Check if `SOURCE_DOC_NOTES` was passed from ln-100 cleanup phase
- If present, merge supporting facts into the standard Context Store:
  ```
  contextStore.SOURCE_DOC_NOTES = input.SOURCE_DOC_NOTES
  ```
- Enrichment intent:
  - architecture notes strengthen architecture evidence
  - requirement notes strengthen requirements evidence
  - tech-stack notes clarify versions and rationale
  - principles, API, database, runbook, and infrastructure notes provide supplemental factual input
- Workers always generate from normalized context + current project sources
- If no `SOURCE_DOC_NOTES` are present: rely on direct auto-discovery + current canonical docs

### Phase 2: Delegate to Workers

> **MANDATORY:** All applicable workers MUST be invoked. Workers run in parallel via Agent tool for context isolation.

**2.1 Always invoke (parallel):**
- `ln-111-root-docs-creator` with Context Store
- `ln-112-project-core-creator` with full Context Store
- `ln-115-devops-docs-creator` with Context Store (infrastructure.md always; runbook.md internally conditional on hasDocker)

**2.2 Conditionally invoke:**
- `ln-113-backend-docs-creator` if hasBackend OR hasDatabase
- `ln-114-frontend-docs-creator` if hasFrontend

**Invocation (parallel via Agent tool):**
```
Agent(description: "{doc_type} docs via {worker}",
     prompt: "Invoke Skill(skill: \"{worker}\") with context below.\n\nCONTEXT: {contextStore}",
     subagent_type: "general-purpose")
```

**Delegation Rules:**
- Pass Context Store and flags to workers via Agent+Skill pattern
- Wait for all Agent completions
- Collect normalized result (`created_files`, `skipped_files`, `quality_inputs`, `validation_status`)

### Phase 3: Aggregate Results

1. Collect status from all workers
2. Sum totals: created files, skipped files
3. Report any validation warnings
4. Return aggregated summary to ln-100
5. **Include Context Store** for subsequent workers (ln-120 needs TECH_STACK)
6. Merge `quality_inputs.owners` from all workers into one repair-routing table

**Output:**
```json
{
  "workers_invoked": 5,
  "total_created": 11,
  "total_skipped": 0,
  "validation_status": "passed",
  "created_files": [
    "AGENTS.md",
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
    "docs/project/infrastructure.md",
    "docs/project/runbook.md"
  ],
  "quality_inputs": {
    "doc_paths": ["AGENTS.md", "CLAUDE.md", "docs/README.md", "docs/project/architecture.md"],
    "owners": {
      "AGENTS.md": "ln-111-root-docs-creator",
      "CLAUDE.md": "ln-111-root-docs-creator",
      "docs/project/architecture.md": "ln-112-project-core-creator"
    }
  },
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
- **Repair routing table required** — every created doc path must map to one owning creator


## Worker Invocation (MANDATORY)

**Host Skill Invocation:** `Skill(skill: "...", args: "...")` is mandatory delegation.
- Claude: call the Skill tool exactly as shown.
- Codex: if no Skill tool exists, locate the named skill in available skills, read its `SKILL.md`, treat `args` as `$ARGUMENTS`, execute that skill workflow, then return here with its result/artifact.
- Do not inline worker logic or mark the worker complete without executing the target skill.

| Phase | Worker | Context | Condition |
|-------|--------|--------|-----------|
| 2 | ln-111-root-docs-creator | Agent (parallel) — root docs | ALWAYS |
| 2 | ln-112-project-core-creator | Agent (parallel) — core project docs | ALWAYS |
| 2 | ln-115-devops-docs-creator | Agent (parallel) — infrastructure + runbook | ALWAYS |
| 2 | ln-113-backend-docs-creator | Agent (parallel) — API spec + DB schema | hasBackend OR hasDatabase |
| 2 | ln-114-frontend-docs-creator | Agent (parallel) — design guidelines | hasFrontend |

**All workers:** Invoke via Agent tool with Skill — workers get Context Store.

## TodoWrite format (mandatory)
```
- Build Context Store (pending)
- Invoke ln-111-root-docs-creator (pending)
- Invoke ln-112-project-core-creator (pending)
- Invoke ln-115-devops-docs-creator (pending)
- Invoke ln-113-backend-docs-creator [conditional] (pending)
- Invoke ln-114-frontend-docs-creator [conditional] (pending)
- Aggregate results (pending)
```

**Anti-Patterns:**
- ❌ Creating documentation files directly instead of invoking workers
- ❌ Marking worker steps done without Agent+Skill invocation
- ❌ Skipping conditional workers without checking flags

### Documentation Standards (passed to workers)
- **NO_CODE Rule:** Documents describe contracts, not implementations
- **Stack Adaptation:** Links must match TECH_STACK (Context Store)
- **Format Priority:** Tables/ASCII > Lists > Text

## Definition of Done
- [ ] Context Store built with all discovered data
- [ ] Project type flags determined
- [ ] All applicable workers invoked
- [ ] Results aggregated
- [ ] **Actuality verified:** all document facts match current code (paths, functions, APIs, configs exist and are accurate)
- [ ] Summary returned to ln-100

## Phase 4: Meta-Analysis

Optional reference: load `references/meta_analysis_protocol.md` only when the user asks for post-run meta-analysis or protocol-formatted run reflection.

Skill type: `planning-coordinator`. When requested, run after all phases complete. Output to chat using the `planning-coordinator` format.

## Reference Files
- Guides: `references/guides/automatic_analysis_guide.md`, `critical_questions.md`, `troubleshooting.md`

---
**Version:** 2.1.0
**Last Updated:** 2025-01-12
