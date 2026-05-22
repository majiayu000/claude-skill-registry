---
name: ln-115-devops-docs-creator
description: "Creates infrastructure.md and runbook.md (Docker-conditional). Use for DevOps documentation in any project."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# DevOps Documentation Creator

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
   - Populate Server Inventory from SERVER_INVENTORY
   - Populate Port Allocation from DOCKER_SERVICES port mappings
   - Populate Deployed Services from DOCKER_SERVICES
   - Populate CI/CD Pipeline from CI_CD_PIPELINE
   - Mark `[TBD: X]` for missing data
4. **Conditional Section Pruning:**
   - If no CI/CD detected: mark CI/CD Pipeline section as `[TBD: Configure CI/CD]`
   - If no ARTIFACT_REPOSITORY: mark Artifact Repository as `[TBD: Configure registry]`
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
   - Populate setup steps from package.json scripts
   - Extract env vars from .env.example
   - Mark `[TBD: X]` for missing data
5. **Conditional Section Pruning:**
   - If DEPLOYMENT_SCALE != "multi" or "auto-scaling": Remove scaling/load balancer sections
   - If !HAS_GPU: Remove GPU-related sections (nvidia runtime, CUDA)
   - If service not in DOCKER_SERVICES: Remove that service's examples
   - If DEVOPS_CONTACTS empty: Mark as `[TBD: Provide DevOps team contacts via Q50]`
   - Populate service dependencies ONLY from DOCKER_SERVICES
   - Populate port mapping ONLY from docker-compose.yml ports section

### Phase 3: Self-Validate
**For infrastructure.md:**
1. Check SCOPE tag
2. Validate sections: Server Inventory, Port Allocation, Deployed Services
3. Check no procedural content leaked (belongs in runbook.md)
4. Check Maintenance section

**For runbook.md (if created):**
1. Check SCOPE tag
2. Validate sections: Local Development Setup, Deployment, Troubleshooting
3. Check env vars documented
4. Check Maintenance section

### Phase 4: Return Status
```json
{
  "created": ["docs/project/infrastructure.md", "docs/project/runbook.md"],
  "skipped": [],
  "tbd_count": 3,
  "validation": "OK"
}
```

## Critical Notes

### Core Rules
- **infrastructure.md:** Always created, no condition
- **runbook.md:** Conditional on hasDocker
- **Heavy auto-discovery:** Most data from docker-compose.yml, .env.example, package.json, SSH config
- **Reproducible:** Setup steps must be testable and repeatable
- **Idempotent:** Never overwrite existing files

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

## Definition of Done
- [ ] infrastructure.md created (always)
- [ ] runbook.md created if hasDocker
- [ ] Infrastructure: server inventory, ports, services documented
- [ ] Runbook: setup steps, deployment, troubleshooting documented
- [ ] All env vars from .env.example included in runbook
- [ ] **Actuality verified:** all document facts match current code (paths, functions, APIs, configs exist and are accurate)
- [ ] Status returned to coordinator

## Reference Files
- Templates: `references/templates/infrastructure_template.md`, `references/templates/runbook_template.md`
- Questions: `references/questions_devops.md` (Q46-Q51 runbook, Q52-Q55 infrastructure)

---
**Version:** 2.0.0
**Last Updated:** 2025-01-12
