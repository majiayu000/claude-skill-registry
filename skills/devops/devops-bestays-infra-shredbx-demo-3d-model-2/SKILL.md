---
name: devops-bestays-infra
description: Manages Bestays infrastructure including Docker Compose, Dockerfile creation, Makefile workflows, service orchestration, production migrations, and backups. Use when managing containers, adding services, deploying to VPS, running migrations, or setting up infrastructure. Acts as a self-updating knowledge index that points to authoritative sources.
---

# DevOps Bestays Infrastructure

## Overview

Orchestrate and manage the Bestays Real Estate Platform development environment. This skill provides workflows for starting services, debugging issues, checking system health, and locating component information across the codebase.

**Core Principle**: This skill is a **pointer system**, not a knowledge base. It knows WHERE information lives (specs, configs, code), not WHAT the information is. This keeps it lightweight, accurate, and self-maintaining.

## When to Use This Skill

**Primary Triggers**:

- Starting or restarting the development environment
- Debugging service failures or integration issues
- Checking system health or component status
- Finding information about system components
- Adding new services to docker-compose
- Understanding how subsystems connect
- Troubleshooting environment setup

**User Patterns**:

- "How do I start the dev environment?"
- "The backend isn't starting"
- "What ports does the system use?"
- "Where is the chat API documented?"
- "How do I add a new service?"
- "Check system health"

## Core Capabilities

### 1. Environment Orchestration

**Start Development Environment**:

```bash
make dev
```

**What Happens**:

1. Checks for running containers → Stops if found
2. Runs preflight validation (`.sdlc-workflow/scripts/preflight.sh`)
3. Starts all services (docker-compose up -d)
4. Verifies health checks

**Preflight Validates**:

- Docker daemon running
- Ports available (8011, 5183, 5433, 6379)
- .env file exists
- Required env vars set (CLERK_SECRET_KEY, OPENROUTER_API_KEY)
- Docker Compose file valid
- Required directories present

**Spec Reference**: `.pattern-book/specifications/tech/preflight-validation.md`

**Stop Environment**:

```bash
make dev-stop
# or
make down
```

**Full Rebuild** (after Dockerfile changes):

```bash
make rebuild
```

Performs: down → build → up → migrate

### 2. System Health Monitoring

**Check All Services**:

```bash
make check
```

**What It Checks**:

- Backend health: `curl http://localhost:8011/api/health`
- Database: `pg_isready`
- Frontend: `curl http://localhost:5183`

**View Logs**:

```bash
make logs              # All services
make logs-server       # Backend only
make logs-frontend     # Frontend only
make logs-db           # Database only
```

**Service Status**:

```bash
make status
# or
docker ps --filter "name=bestays"
```

### 3. Component Information Lookup

**When You Need Information**:

**Step 1**: Identify component category

- Infrastructure? → Docker Compose, Makefile
- Backend? → FastAPI server, PostgreSQL, Redis
- Frontend? → SvelteKit app
- External? → OpenRouter, Clerk
- Pattern-Book? → Discussions, specs

**Step 2**: Consult component map

```
Read: references/component-map.md
```

**Component Map Provides**:

- Definitive source file paths
- What information is available there
- Related specs
- Quick access patterns

**Example Lookup**:

- **Q**: "What ports does the system use?"
- **A**: Component map → Docker Compose section → Points to `docker-compose.dev.yml` → Read ports sections

**Pattern**: Always read definitive source, never rely on cached knowledge

### 4. Troubleshooting

**When Something Breaks**:

**Step 1**: Identify issue category

- Environment startup?
- Service-specific (backend, frontend, db)?
- Application-level (chat, auth)?
- Docker/container?
- Integration/API?

**Step 2**: Consult troubleshooting index

```
Read: references/troubleshooting-index.md
```

**Index Provides**:

- Symptoms → Troubleshooting path
- Common causes
- Pointer to definitive solution

**Example Troubleshooting**:

- **Issue**: "make dev fails"
- **Action**: Read troubleshooting-index.md → Environment Issues → Points to preflight validation
- **Next**: Run `bash .sdlc-workflow/scripts/preflight.sh` to see specific failure

**Debugging Workflow**:

1. Check service logs (`make logs-[service]`)
2. Verify service health (`make check`)
3. Access service shell (`make shell-[service]`)
4. Consult infrastructure discussion for detailed workflows
5. Update troubleshooting index with new learnings

**Infrastructure Discussion**: `.pattern-book/discussions/20251027-2321-infrastructure-setup-deployment-testing-/`

### 5. Adding New Components

**To Add a New Service to Docker Compose**:

**Step 1**: Update `docker-compose.dev.yml`

```yaml
services:
  new-service:
    image: ...
    ports:
      - "XXXX:YYYY"
    environment:
      - VAR=value
    depends_on:
      - existing-service
    networks:
      - bestays-network
```

**Step 2**: Update preflight validation (if ports added)

- Edit `.sdlc-workflow/scripts/preflight.sh`
- Add port check in `check_ports_available()`

**Step 3**: Update Makefile (if special commands needed)

```makefile
logs-newservice:
    $(COMPOSE) logs -f new-service

shell-newservice:
    $(COMPOSE) exec new-service /bin/sh
```

**Step 4**: Update this skill

- Add entry to `references/component-map.md`
- Document in relevant section (Infrastructure, Backend, etc.)
- Add troubleshooting patterns if known

**Step 5**: Create/update specs

- Create URS if user-facing feature
- Create tech spec for implementation details
- Create integration contract for API boundaries

### 6. Self-Update Protocol

**When This Skill Is Missing Information**:

**Detect**: Encounter question skill can't answer with current pointers

**Analyze**: Determine what information is missing and where it should be documented

**Update**:

1. If it's configuration → Already documented in config files, add pointer to component map
2. If it's a process → Document in relevant spec or discussion, add pointer
3. If it's troubleshooting → Add to troubleshooting index
4. If it's new component → Add to component map

**Pattern to Follow**:

In `references/component-map.md`:

```markdown
### [Component Name]

**Definitive Source**: [file path]

**What's There**: [list of available information]

**Spec** (if applicable): [path to spec]

**Key Details**: [critical locating information]
```

In `references/troubleshooting-index.md`:

```markdown
### "[Issue Title]"

**Symptoms**: [observable problems]

**Troubleshooting Path**: [step-by-step diagnosis]

**Common Causes**: [typical root causes]

**Definitive Source**: [where solution documented]
```

**Commit Updates**: After updating, commit changes to skill so future sessions benefit

## Quick Reference Commands

### Daily Workflow

```bash
# Start development (smart restart)
make dev

# View logs (all services)
make logs

# Check health
make check

# Stop everything
make dev-stop
```

### Debugging

```bash
# Service-specific logs
make logs-server
make logs-frontend
make logs-db

# Access service shells
make shell-server      # Backend Python shell
make shell-frontend    # Frontend Node shell
make shell-db          # PostgreSQL psql
```

### Maintenance

```bash
# Full rebuild (after Dockerfile changes)
make rebuild

# Run preflight checks
bash .sdlc-workflow/scripts/preflight.sh

# Validate environment
make dev-validate
```

### Status Checks

```bash
# Container status
make status

# Comprehensive status
make dev-status

# Health checks
make health
```

## Service Endpoints

**Local Development URLs**:

- Backend API: http://localhost:8011
- API Documentation: http://localhost:8011/docs
- Frontend: http://localhost:5183
- PostgreSQL: localhost:5433
- Redis: localhost:6379

**Container-to-Container URLs** (within Docker network):

- Backend: http://server:8011
- PostgreSQL: postgresql://postgres:5432
- Redis: redis://redis:6379

**Note**: Always check `docker-compose.dev.yml` for current configuration

## Integration with Other Skills

**Works With**:

- **skill-pb-spec**: When creating specs for new components, use this skill to understand system context
- **skill-pb-discuss**: Use this skill to provide system details during requirements gathering
- **backend-architect**: Use component map to understand existing architecture before designing new features
- **debugger**: Use troubleshooting index as starting point for investigation

**Provides Context For**:

- System architecture understanding
- Component boundaries and responsibilities
- Integration points between subsystems
- Current implementation state

## Resources

### references/component-map.md

Complete index of all system components and where their information lives.

**When to Read**: Looking for information about a specific component

**Provides**:

- File path to definitive source
- List of available information
- Related specifications
- Quick access patterns

**Covers**:

- Infrastructure (Docker, Makefile, preflight)
- Backend (FastAPI, PostgreSQL, Redis)
- Frontend (SvelteKit)
- External services (OpenRouter, Clerk)
- Pattern-Book system
- Configuration files

### references/troubleshooting-index.md

Index of common issues and where to find solutions.

**When to Read**: Debugging a problem

**Provides**:

- Symptoms → troubleshooting path
- Common causes
- Pointers to definitive solutions

**Covers**:

- Environment & startup issues
- Service-specific issues (backend, frontend, db, redis)
- Application-level issues (chat, auth)
- Docker & container issues
- Performance issues
- Development workflow issues
- Integration & API issues

## Best Practices

### Always Use Pointers

**Good** ✅:

```
"Port configuration is in docker-compose.dev.yml → services → [service] → ports"
```

**Bad** ❌:

```
"Backend uses port 8011, frontend uses 5183..."
```

### Read Definitive Sources

When user asks "What ports does the system use?":

1. Point to docker-compose.dev.yml
2. Read the file
3. Extract current configuration
4. Provide answer

**Never** answer from memory - config may have changed.

### Update After Learning

When you solve a problem not documented:

1. Document solution in appropriate spec
2. Update troubleshooting index with pointer
3. Update component map if new component
4. Commit update

### Maintain Single Source of Truth

- Config lives in config files
- Specs live in .pattern-book/specifications/
- This skill provides POINTERS only
- No duplication of information

## Workflow Examples

### Example 1: Starting Development

**User**: "Start the development environment"

**Actions**:

1. Run `make dev`
2. Monitor output for preflight validation
3. If validation fails, read error and guide user
4. Once services start, verify health with `make check`
5. Provide service URLs

### Example 2: Debugging Backend Failure

**User**: "Backend isn't starting"

**Actions**:

1. Read `references/troubleshooting-index.md` → "Backend Not Starting"
2. Follow troubleshooting path:
   - Check logs: `make logs-server`
   - Check container: `docker ps -a | grep bestays-server`
   - Identify error in logs
3. If database connection issue → Check postgres health
4. If migration issue → Run `make migrate`
5. Document new issue if not in index

### Example 3: Finding API Specification

**User**: "Where is the chat API documented?"

**Actions**:

1. Read `references/component-map.md` → Backend section
2. Find: "Specs: .pattern-book/specifications/integration/openrouter-chat.md"
3. Read integration spec for API contract
4. Also point to API docs: http://localhost:8011/docs

### Example 4: Adding New Environment Variable

**User**: "How do I add a new environment variable?"

**Actions**:

1. Read `references/component-map.md` → Configuration Files → Environment Variables
2. Guide through process:
   - Add to `.env` file
   - Add to `docker-compose.dev.yml` → service → environment
   - Document in relevant spec
3. Restart services: `make dev`
4. Update component map if it's a significant new config

## Validation & Quality

**Skill Health Indicators**:

- ✅ All pointers in component map are valid file paths
- ✅ Troubleshooting index covers known issues
- ✅ Can answer "where is X documented?" questions
- ✅ No duplicated information (everything points to source)
- ✅ Self-update protocol is followed when gaps found

**Regular Maintenance**:

- After new components added → Update component map
- After solving new issues → Update troubleshooting index
- After specs created → Update pointers
- After config changes → Verify pointers still valid

---

**Last Updated**: 2025-10-28
**Maintainer**: Self-updating skill (updates itself when gaps discovered)
**Version**: 1.0.0
