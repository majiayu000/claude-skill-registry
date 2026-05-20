---
name: ln-115-devops-docs-creator
description: "Creates infrastructure.md and runbook.md (Docker-conditional). Use for DevOps documentation in any project."
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# DevOps Documentation Creator

**Type:** L3 Worker

L3 Worker that creates infrastructure.md and runbook.md. Infrastructure inventory is always created; runbook is conditional on Docker presence.

## Purpose & Scope
- Creates infrastructure.md (always) — declarative inventory: WHAT is deployed WHERE
- Creates runbook.md (if hasDocker) — procedural guide: HOW to deploy/restart/troubleshoot
- Receives Context Store from ln-110-project-docs-coordinator
- Never gathers context itself; uses coordinator input

## Invocation (who/when)
- **ln-110-project-docs-coordinator:** ALWAYS invoked (infrastructure.md is unconditional)
- Never called directly by users

## Inputs
From coordinator:
- `contextStore`: Context Store with DevOps-specific data
  - DOCKER_COMPOSE_DEV (development setup)
  - DOCKER_COMPOSE_PROD (production setup)
  - ENV_VARIABLES (from .env.example)
  - STARTUP_SEQUENCE (services order)
  - DEPLOYMENT_TARGET (AWS, Vercel, Heroku)
  - CI_CD_PIPELINE (from .github/workflows)
  - DOCKER_SERVICES (parsed from docker-compose.yml services)
  - DEPLOYMENT_SCALE ("single" | "multi" | "auto-scaling" | "gpu-based")
  - DEVOPS_CONTACTS (from CODEOWNERS, package.json author, git log)
  - HAS_GPU (detected from docker-compose nvidia runtime)
  - SERVER_INVENTORY (from SSH config, deploy targets)
  - DOMAIN_DNS (from docker-compose VIRTUAL_HOST vars, nginx configs)
  - ARTIFACT_REPOSITORY (from .env registry URLs, .npmrc, pip.conf)
  - HOST_REQUIREMENTS (from docker-compose deploy.resources.limits)
- `targetDir`: Project root directory
- `flags`: { hasDocker }

**MANDATORY READ:** Load `shared/references/docs_quality_contract.md`, `shared/references/docs_quality_rules.json`, and `shared/references/markdown_read_protocol.md`.

## Documents Created (2: 1 always + 1 conditional)

| File | Condition | Questions | Auto-Discovery |
|------|-----------|-----------|----------------|
| docs/project/infrastructure.md | Always | Q52-Q55 | Medium |
| docs/project/runbook.md | hasDocker | Q46-Q51 | High |

## Workflow

### Phase 1: Check Conditions
1. Parse flags from coordinator
2. infrastructure.md: ALWAYS proceeds (no condition check)
3. runbook.md: Create ONLY if `hasDocker=true`
4. If target file already exists: skip that file (idempotent)

### Phase 2a: Create infrastructure.md (unconditional)
1. Check if `docs/project/infrastructure.md` exists
2. If exists: skip with log
3. If not exists:
   - Copy `references/templates/infrastructure_template.md`
   - Replace placeholders with Context Store values
   - Preserve the shared opening contract and standard top sections from the template
   - Populate Server Inventory from SERVER_INVENTORY
   - Populate Port Allocation from DOCKER_SERVICES port mappings
   - Populate Deployed Services from DOCKER_SERVICES
   - Populate CI/CD Pipeline from CI_CD_PIPELINE
   - Never leave template markers in published infrastructure docs
   - If data is missing: omit the claim or use a concise neutral fallback, but do NOT emit `[TBD: ...]`
4. **Conditional Section Pruning:**
   - If no CI/CD detected: replace with concise empty-state note, not `[TBD: ...]`
   - If no ARTIFACT_REPOSITORY: replace with concise empty-state note, not `[TBD: ...]`
   - If single server / no SERVER_INVENTORY: simplify to single-column table
   - If !HAS_GPU: remove GPU column from Server Inventory and Deployed Services
   - Populate Deployed Services ONLY from DOCKER_SERVICES (no generic examples)

### Phase 2b: Create runbook.md (conditional)
1. If `!hasDocker`: skip entirely
2. Check if `docs/project/runbook.md` exists
3. If exists: skip with log
4. If not exists:
   - Copy `references/templates/runbook_template.md`
   - Replace placeholders with Context Store values
   - Preserve the shared opening contract and standard top sections from the template
   - Populate setup steps from package.json scripts
   - Extract env vars from .env.example
   - Never leave template markers in published runbooks
   - If data is missing: omit the claim or use a concise neutral fallback, but do NOT emit `[TBD: ...]`
5. **Conditional Section Pruning:**
   - If DEPLOYMENT_SCALE != "multi" or "auto-scaling": Remove scaling/load balancer sections
   - If !HAS_GPU: Remove GPU-related sections (nvidia runtime, CUDA)
   - If service not in DOCKER_SERVICES: Remove that service's examples
   - If DEVOPS_CONTACTS empty: replace with concise empty-state note, not `[TBD: ...]`
   - Populate service dependencies ONLY from DOCKER_SERVICES
   - Populate port mapping ONLY from docker-compose.yml ports section

### Phase 3: Self-Validate
**For infrastructure.md:**
1. Check SCOPE tag and metadata markers
2. Check required top sections (`Quick Navigation`, `Agent Entry`, `Maintenance`)
3. Validate sections: Server Inventory, Port Allocation, Deployed Services
4. Check no procedural content leaked (belongs in runbook.md)
5. Check docs-quality contract compliance (no forbidden placeholders, no leaked template metadata, valid doc kind/role)

**For runbook.md (if created):**
1. Check SCOPE tag and metadata markers
2. Check required top sections (`Quick Navigation`, `Agent Entry`, `Maintenance`)
3. Validate sections: Local Development Setup, Deployment, Troubleshooting
4. Check env vars documented
5. Check docs-quality contract compliance (no forbidden placeholders, no leaked template metadata, valid doc kind/role)

### Phase 4: Return Status
```json
{
  "created_files": ["docs/project/infrastructure.md", "docs/project/runbook.md"],
  "skipped_files": [],
  "quality_inputs": {
    "doc_paths": ["docs/project/infrastructure.md", "docs/project/runbook.md"],
    "owners": {
      "docs/project/infrastructure.md": "ln-115-devops-docs-creator",
      "docs/project/runbook.md": "ln-115-devops-docs-creator"
    }
  },
  "validation_status": "passed"
}
```

## Critical Notes

### Core Rules
- **infrastructure.md:** Always created, no condition
- **runbook.md:** Conditional on hasDocker
- **Heavy auto-discovery:** Most data from docker-compose.yml, .env.example, package.json, SSH config
- **Reproducible:** Setup steps must be testable and repeatable
- **Idempotent:** Never overwrite existing files
- **Publishable output:** No `[TBD: ...]`, `TODO`, or leaked template metadata in DevOps docs

### NO_CODE_EXAMPLES Rule (MANDATORY)
Both documents describe **inventory/procedures**, NOT implementations:
- **FORBIDDEN:** Full Docker configs, CI/CD pipelines (>5 lines), full nginx configs
- **ALLOWED:** Command examples (1-3 lines), env var tables, step lists, verification commands
- **INSTEAD OF CODE:** "See [docker-compose.yml](../docker-compose.yml)"

### Stack Adaptation Rule (MANDATORY)
- Commands must match project stack (npm vs pip vs go)
- Link to correct cloud provider docs (AWS/Azure/GCP)
- Never mix stack references (no npm commands in Python project)

### Format Priority (MANDATORY)
Tables (env vars, ports, services, servers) > Lists (setup steps) > Text

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/docs_generation_summary_contract.md`

Accept optional `summaryArtifactPath`.

Summary kind:
- `docs-generation`

Required payload semantics:
- `worker = "ln-115"`
- `status`
- `created_files`
- `skipped_files`
- `quality_inputs`
- `validation_status`
- `warnings`

Write the summary to the provided artifact path or return the same envelope in structured output.

## Definition of Done
- [ ] infrastructure.md created (always)
- [ ] runbook.md created if hasDocker
- [ ] Infrastructure: server inventory, ports, services documented
- [ ] Runbook: setup steps, deployment, troubleshooting documented
- [ ] All env vars from .env.example included in runbook
- [ ] **Actuality verified:** all document facts match current code (paths, functions, APIs, configs exist and are accurate)
- [ ] Status returned

## Reference Files
- Templates: `references/templates/infrastructure_template.md`, `references/templates/runbook_template.md`
- Questions: `references/questions_devops.md` (Q46-Q51 runbook, Q52-Q55 infrastructure)

---
**Version:** 2.0.0
**Last Updated:** 2025-01-12
