---
name: ln-115-devops-docs-creator
description: Creates runbook.md for DevOps setup. L3 Worker invoked CONDITIONALLY when hasDocker detected.
---

# DevOps Documentation Creator

L3 Worker that creates runbook.md. CONDITIONAL - only invoked when project has Docker or deployment config.

## Purpose & Scope
- Creates runbook.md (if hasDocker)
- Receives Context Store from ln-110-project-docs-coordinator
- Step-by-step setup and deployment instructions
- Troubleshooting guide
- Never gathers context itself; uses coordinator input

## Invocation (who/when)
- **ln-110-project-docs-coordinator:** CONDITIONALLY invoked when:
  - `hasDocker=true` (Dockerfile or docker-compose.yml detected)
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
- `targetDir`: Project root directory
- `flags`: { hasDocker }

## Documents Created (1, conditional)

| File | Condition | Questions | Auto-Discovery |
|------|-----------|-----------|----------------|
| docs/project/runbook.md | hasDocker | Q46-Q51 | High |

## Workflow

### Phase 1: Check Conditions
1. Parse flags from coordinator
2. If `!hasDocker`: return early with empty result

### Phase 2: Create Document
1. Check if file exists (idempotent)
2. If exists: skip with log
3. If not exists:
   - Copy template
   - Replace placeholders with Context Store values
   - Populate setup steps from package.json scripts
   - Extract env vars from .env.example
   - Mark `[TBD: X]` for missing data
4. **Conditional Section Pruning:**
   - If DEPLOYMENT_SCALE != "multi" or "auto-scaling": Remove scaling/load balancer sections
   - If !HAS_GPU: Remove GPU-related sections (nvidia runtime, CUDA)
   - If service not in DOCKER_SERVICES: Remove that service's examples (e.g., no Redis = no Redis commands)
   - If DEVOPS_CONTACTS empty: Mark {{KEY_CONTACTS}} as `[TBD: Provide DevOps team contacts via Q50]`
   - Populate {{SERVICE_DEPENDENCIES}} ONLY from DOCKER_SERVICES (no generic examples)
   - Populate {{PORT_MAPPING}} ONLY from docker-compose.yml ports section

### Phase 3: Self-Validate
1. Check SCOPE tag
2. Validate sections:
   - Local Development Setup (prerequisites, install, run)
   - Deployment (platform, build, deploy steps)
   - Troubleshooting (common errors, debugging)
3. Check env vars documented
4. Check Maintenance section

### Phase 4: Return Status
```json
{
  "created": ["docs/project/runbook.md"],
  "skipped": [],
  "tbd_count": 0,
  "validation": "OK"
}
```

## Critical Notes

### Core Rules
- **Conditional:** Skip entirely if no Docker detected
- **Heavy auto-discovery:** Most data from docker-compose.yml, .env.example, package.json
- **Reproducible:** Setup steps must be testable and repeatable
- **Idempotent:** Never overwrite existing files

### NO_CODE_EXAMPLES Rule (MANDATORY)
Runbook documents **procedures**, NOT implementations:
- **FORBIDDEN:** Full Docker configs, CI/CD pipelines (>5 lines)
- **ALLOWED:** Command examples (1-3 lines), env var tables, step lists
- **INSTEAD OF CODE:** "See [docker-compose.yml](../docker-compose.yml)"

### Stack Adaptation Rule (MANDATORY)
- Commands must match project stack (npm vs pip vs go)
- Link to correct cloud provider docs (AWS/Azure/GCP)
- Never mix stack references (no npm commands in Python project)

### Format Priority (MANDATORY)
Tables (env vars, ports, services) > Lists (setup steps) > Text

## Definition of Done
- Condition checked (hasDocker)
- Document created if applicable
- Setup steps, deployment, troubleshooting documented
- All env vars from .env.example included
- Status returned to coordinator

## Reference Files
- Templates: `references/templates/runbook_template.md`
- Questions: `references/questions_devops.md` (Q46-Q51)

---
**Version:** 1.1.0 (Added NO_CODE, Stack Adaptation, Format Priority rules)
**Last Updated:** 2025-01-12
