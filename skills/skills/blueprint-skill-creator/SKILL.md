---
name: blueprint-skill-creator
description: Creates blueprint-driven skills for infrastructure and deployment tasks. This skill should be used when creating new skills that require templates, patterns, or reference configurations (e.g., Dockerfiles, Helm charts, Kubernetes manifests, CI/CD pipelines). It enforces impact analysis before containerization, identifies environment requirements, network topology changes, and auth/CORS implications. Use this skill when building deployment-related skills or when containerizing applications.
---

# Blueprint Skill Creator

## Overview

This skill creates infrastructure skills that bundle **blueprints** (reusable templates and patterns) with **impact analysis** (understanding what changes when containerizing/deploying). It ensures deployment skills don't just generate configs—they understand and document the full impact.

## Core Principle: Impact-Aware Blueprints

Traditional approach (fragile):
```
Request: "Create a Dockerfile"
Result: Generic Dockerfile that breaks in production
```

Blueprint-driven approach (robust):
```
Request: "Create a Dockerfile"
Process:
1. Analyze project for containerization requirements
2. Identify environment variables (build-time vs runtime)
3. Map localhost references → Docker service names
4. Check auth/CORS origins for container network
5. Generate Dockerfile with documented gotchas
6. Create docker-compose with proper networking
```

## Workflow: Creating Blueprint-Driven Skills

### Step 1: Define the Skill's Domain

Identify what infrastructure domain the skill covers:

| Domain | Examples | Key Concerns |
|--------|----------|--------------|
| Containerization | Dockerfiles, docker-compose | Env vars, networking, multi-stage builds |
| Orchestration | Helm, Kubernetes manifests | Service discovery, secrets, resource limits |
| CI/CD | GitHub Actions, pipelines | Build vs deploy stages, secrets injection |
| Event Systems | Kafka, Dapr | Topics, schemas, authentication |

### Step 2: Conduct Impact Analysis

Before creating any blueprint, analyze the target project:

#### 2.1 Environment Analysis
```
Scan for:
├── .env files → What variables exist?
├── process.env / os.environ usage → What's expected at runtime?
├── Build-time variables → NEXT_PUBLIC_*, ARG in Dockerfiles
└── Sensitive values → API keys, secrets, connection strings
```

#### 2.2 Network Topology Analysis
```
Identify:
├── localhost references → Must become service names
├── Port bindings → What ports are exposed?
├── Service dependencies → What talks to what?
└── External services → Databases, APIs, auth providers
```

#### 2.3 Auth/CORS Impact Analysis

**Critical for SSO/Better Auth:**
```
Check auth configuration for:
├── Allowed origins → Must include Docker service names
├── Callback URLs → localhost:3000 → web:3000
├── API URLs → localhost:8000 → api:8000
└── NODE_ENV behavior → Some features disabled in production
```

**Common gotcha:**
```typescript
// better-auth config - WILL BREAK in Docker if not updated
trustedOrigins: [
  "http://localhost:3000",     // Works locally
  // MISSING: "http://web:3000"  // Needed for Docker
  // MISSING: "http://frontend:3000"  // Needed for K8s
]
```

### Step 3: Create Skill Structure

Initialize using skill-creator:
```bash
python3 .claude/skills/engineering/skill-creator/scripts/init_skill.py \
  <skill-name> --path .claude/skills/engineering/
```

Organize with blueprints:
```
.claude/skills/engineering/<skill-name>/
├── SKILL.md                    # Instructions + impact analysis guidance
├── references/                 # Blueprint documentation
│   ├── patterns.md             # Common patterns and when to use them
│   ├── impact-checklist.md     # What to check before containerizing
│   └── gotchas.md              # Known issues and solutions
└── assets/                     # Template files
    ├── Dockerfile.template     # Base template
    ├── docker-compose.template # Compose template
    └── .env.example            # Environment template
```

### Step 4: Write Blueprint References

Each reference file should include:

**Pattern documentation (`references/patterns.md`):**
```markdown
# Pattern: Multi-Stage Build

## When to Use
- Production deployments
- When image size matters
- When build dependencies differ from runtime

## Template
[Include actual template code]

## Variables to Replace
- `{{BASE_IMAGE}}` - Base image (e.g., python:3.13-slim)
- `{{APP_MODULE}}` - Entry point (e.g., main:app)
- `{{PORT}}` - Exposed port

## Impact Notes
- Build-time ARGs are baked in - cannot change at runtime
- Use ENV for runtime configuration
```

**Impact checklist (`references/impact-checklist.md`):**
```markdown
# Pre-Containerization Checklist

## Environment Variables
- [ ] List all env vars used in application
- [ ] Categorize: build-time vs runtime
- [ ] Identify secrets (should use K8s secrets, not ENV)

## Network Changes
- [ ] Find all localhost references
- [ ] Map to Docker service names
- [ ] Update CORS/auth origins

## Auth/SSO Specific
- [ ] Check trustedOrigins includes Docker service names
- [ ] Verify callback URLs work with container networking
- [ ] Test NODE_ENV=production behavior

## Dependencies
- [ ] Identify service startup order
- [ ] Configure health checks
- [ ] Set up proper wait conditions
```

### Step 5: Include Asset Templates

Asset templates should be parameterized and documented:

**Dockerfile.template:**
```dockerfile
# ===== IMPACT NOTES =====
# This template requires:
# - ENV: {{ENV_VARS_LIST}}
# - Network: Service name "{{SERVICE_NAME}}" on port {{PORT}}
# - Auth: Ensure CORS includes http://{{SERVICE_NAME}}:{{PORT}}
# ========================

FROM {{BASE_IMAGE}} AS builder
# ... template content
```

**docker-compose.template:**
```yaml
# ===== NETWORK TOPOLOGY =====
# Services communicate via Docker network using service names:
# - web → api: http://api:8000
# - api → db: postgres://db:5432
# - web → sso: http://sso:3001
# ============================

services:
  {{SERVICE_NAME}}:
    build:
      context: {{CONTEXT_PATH}}
      args:
        - NODE_ENV={{NODE_ENV}}
    environment:
      # Runtime configuration
      - DATABASE_URL=${DATABASE_URL}
      - API_URL=http://api:8000  # Docker service name, not localhost!
```

## Creating Specific Blueprint Skills

### Example: Docker Blueprint Skill

When creating a Docker blueprint skill, include:

**SKILL.md sections:**
1. Impact analysis workflow
2. Environment variable handling
3. Multi-stage build patterns
4. Network configuration for Docker Compose
5. Auth/CORS gotchas

**References:**
- `references/fastapi-patterns.md` - FastAPI-specific patterns
- `references/nextjs-patterns.md` - Next.js-specific patterns
- `references/auth-impact.md` - Better Auth/SSO considerations

**Assets:**
- `assets/Dockerfile.fastapi` - FastAPI template
- `assets/Dockerfile.nextjs` - Next.js template
- `assets/docker-compose.base.yml` - Base compose file

### Example: Helm Blueprint Skill

When creating a Helm blueprint skill, include:

**SKILL.md sections:**
1. Chart structure requirements
2. Values.yaml patterns
3. Secret management (External Secrets Operator)
4. Service discovery in Kubernetes
5. Resource limits by environment

**References:**
- `references/chart-structure.md` - Helm chart anatomy
- `references/security-context.md` - Pod security patterns
- `references/networking.md` - Service/Ingress patterns

**Assets:**
- `assets/base-chart/` - Complete Helm chart template
- `assets/values-dev.yaml` - Development values
- `assets/values-prod.yaml` - Production values

## Validation Checklist

Before finalizing a blueprint skill, verify:

- [ ] SKILL.md includes impact analysis workflow
- [ ] References document all patterns with "when to use"
- [ ] Assets are parameterized with clear variable markers
- [ ] Gotchas and common failures are documented
- [ ] Network topology is explicitly documented
- [ ] Auth/CORS implications are addressed
- [ ] Environment variables are categorized (build vs runtime)
- [ ] Service dependencies and startup order documented

## Anti-Patterns to Avoid

**Don't create blueprints that:**
- Hardcode localhost URLs
- Bake secrets into images
- Ignore NODE_ENV behavior differences
- Skip health checks
- Assume single-container deployment
- Forget about CORS/auth origins

**Do create blueprints that:**
- Use environment variables for all URLs
- Reference secrets from external stores
- Document production vs development differences
- Include comprehensive health checks
- Support both Docker Compose and Kubernetes
- Explicitly list required CORS origin updates

## Resources

### references/
Contains pattern documentation and impact checklists that inform blueprint creation.

### assets/
Contains template files that serve as starting points for generated configurations.

### scripts/
Contains validation scripts for checking blueprint completeness.
