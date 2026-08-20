---
name: prd-v06-environment-setup
description: Document development environment requirements for team consistency and AI agent understanding during PRD v0.6 Architecture. Triggers on requests to define environment setup, document tooling, create dev setup guide, or when user asks "what tools do I need?", "environment setup", "dev environment", "CLI requirements", "project setup", "onboarding setup". Consumes TECH- (stack selections), ARC- (architecture decisions). Outputs ENV- entries for development, CI/CD, and infrastructure environments. Feeds v0.7 Build Execution.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Environment Setup

Position in workflow: v0.6 Architecture Design / Technical Specification → **v0.6 Environment Setup** → v0.7 Build Execution

Environment setup documents the **tools, packages, and configurations** developers need to work on the project. This eliminates environment drift and speeds up onboarding.

## Consumes

This skill requires prior work from v0.5-v0.6:

- **TECH-\* technology decisions** (from v0.5 Technical Stack Selection) — Choices for frontend/backend/database/CI/CD determine which tools, languages, and package managers developers need
- **ARC-\* architecture decisions** (from v0.6 Architecture Design) — Architectural patterns (monolith vs microservices, container strategy, deployment topology) inform infrastructure and scripting needs

This skill assumes v0.5 Technical Stack Selection is complete with TECH- entries specifying the tech stack.

## Produces

This skill creates/updates:

- **ENV-001: Development Environment** — Local setup specification with CLIs (global), packages (per-project), config files, verification steps. Enables consistent development experience across team
- **ENV-002: CI/CD Pipeline** (optional) — Automated testing and deployment workflow specifications with required secrets and pipeline stages
- **ENV-003: Production Infrastructure** (optional) — Production hosting, environment variables, services, and deployment topology

All ENV- entries are **specifications, not confidence-based**. They are:
- **Concrete and verifiable** (each CLI/package has an install command; each config file has a purpose)
- **Preferring CLIs over MCPs** (standard tools work in CI/CD; MCPs don't scale)
- **Per-project, not global** (package managers install dependencies in the project, not globally)

Example ENV-001 entry (Development Environment):
```markdown
ENV-001: Development Environment
Category: Development Setup
Status: Approved | Date: 2026-02-26
Owner: Engineering Team

Purpose:
Local development setup for team consistency and AI agent understanding.

CLIs (Global, install once):
- Node.js 20.x: https://nodejs.org — Language runtime
  Install: `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && nvm install 20`
  Verify: `node --version`
- mise: https://mise.jdx.dev — Version manager
  Install: `curl https://mise.jdx.dev/install.sh | sh`
  Verify: `mise --version`

Packages (Per-Project):
- typescript: Type checking (devDependency)
- eslint, prettier: Code quality (devDependencies)
- jest: Testing framework (devDependency)
- Listed in package.json, installed via: `npm install`

Configuration Files:
| File | Purpose |
|------|---------|
| package.json | Dependencies, scripts, project metadata |
| tsconfig.json | TypeScript compiler options |
| .eslintrc.json | Linting rules |
| .prettierrc | Code formatting rules |
| .env.example | Template for environment variables |

Scripts:
{
  "validate": "npm run lint && npm run type-check",
  "lint": "eslint src/",
  "fix": "eslint src/ --fix && prettier --write src/",
  "type-check": "tsc --noEmit",
  "test": "jest",
  "dev": "next dev",
  "build": "next build"
}

Verification:
# 1. Check global CLIs
node --version
mise --version

# 2. Check per-project packages
npm list | head -20

# 3. Run validation
npm run validate

# 4. Run tests
npm run test

Related IDs: TECH-001 (Next.js), TECH-002 (TypeScript), ARC-001 (monolith structure)
```

Example ENV-002 entry (CI/CD):
```markdown
ENV-002: CI/CD Pipeline
Category: Automation
Status: Approved | Date: 2026-02-26

Purpose:
Automated testing and deployment configuration.

Workflow Files:
- .github/workflows/test.yml: Run tests on push to any branch
- .github/workflows/deploy.yml: Deploy main branch to production on merge

Required Secrets (set in GitHub Settings → Secrets):
| Secret | Purpose |
|--------|---------|
| VERCEL_TOKEN | Authentication for Vercel deployment |
| DATABASE_URL | Production database connection string |
| API_KEY | Third-party API credentials |

Pipeline Stages:
1. Install: `npm install`
2. Lint: `npm run validate` (must pass)
3. Test: `npm run test` (must pass)
4. Build: `npm run build` (must succeed)
5. Deploy: Push to Vercel (main branch only)

Related IDs: ENV-001, TECH-002 (Node.js), ARC-001 (monolith deployment)
```

## Environment Types

| Type | What It Defines | When Required |
|------|-----------------|---------------|
| **ENV-001** | Development environment (local setup) | Always |
| **ENV-002** | CI/CD pipeline configuration | When using automated testing/deployment |
| **ENV-003** | Production infrastructure | When deploying to production |

**Rule**: ENV-001 (Development Environment) is required for every project. ENV-002 and ENV-003 are optional based on project needs.

## Design Principles

### 1. Prefer CLIs Over MCPs

**Rule**: Use CLIs for operations, MCPs only when CLIs are insufficient.

| Factor | CLI | MCP |
|--------|-----|-----|
| Works in CI/CD | Yes | No |
| Works locally | Yes | Yes (limited contexts) |
| Structured output | JSON, exit codes | Varies |
| Debugging | Standard tools | Harder |

**Decision**: Default to CLI. Only document MCPs for operations where CLIs don't exist.

### 2. Per-Project Over Global

**Rule**: Language-specific packages installed per-project, not globally.

**Global (OK):**
- Version managers (mise, asdf, nvm)
- System tools (jq, ripgrep)
- Platform CLIs (gh, aws-cli)

**Per-Project (Required):**
- Linters/formatters (eslint, prettier)
- Type checkers (typescript)
- Testing frameworks (jest, pytest)

### 3. Structured Over Prose

**Rule**: ENV- specs use structured data (tables, code blocks), not narrative.

**Why**:
- AI agents can parse and execute
- Humans can scan quickly
- Diff-friendly in version control

### 4. Verification Required

**Rule**: Every ENV- spec includes verification commands.

**Why**:
- Confirms setup succeeded
- Debugging aid
- Onboarding confidence

## Setup Process

1. **Pull TECH- decisions** — What technologies are we using?
2. **Pull ARC- decisions** — What architecture patterns apply?
3. **Inventory tooling needs** — What do developers need installed?
4. **Categorize by scope** — Global vs per-project
5. **Define configuration files** — What configs are needed?
6. **Create verification steps** — How to confirm setup works?
7. **Document in ENV- entries** — Record in SoT.TECHNICAL_DECISIONS.md

## ENV-001 Output Template (Development Environment)

```
ENV-001: Development Environment
Category: Development Setup
Status: Approved | Date: YYYY-MM-DD
Owner: {Team/Person}

Purpose:
Document local development requirements for team consistency.

CLIs (Global):
- {tool}: {purpose} — {install command}

Packages (Per-Project):
- {package}: {purpose}

Configuration Files:
| File | Purpose |
|------|---------|
| {file} | {purpose} |

Scripts:
{
  "validate": "{quality check command}",
  "fix": "{auto-fix command}",
  "test": "{test command}"
}

Verification:
# 1. Check tools
{tool} --version

# 2. Check packages
{package manager list command}

# 3. Run validation
npm run validate

Related IDs: TECH-XXX, ARC-XXX
```

## ENV-002 Output Template (CI/CD Pipeline)

```
ENV-002: CI/CD Pipeline
Category: Automation
Status: Approved | Date: YYYY-MM-DD

Purpose:
Document automated testing and deployment configuration.

Workflow Files:
- {path}: {purpose}

Required Secrets:
| Secret | Purpose | Where to Set |
|--------|---------|--------------|
| {name} | {purpose} | {location} |

Pipeline Stages:
1. {Stage}: {What happens}
2. {Stage}: {What happens}

Related IDs: ENV-001, DEP-XXX
```

## ENV-003 Output Template (Production Infrastructure)

```
ENV-003: Production Infrastructure
Category: Infrastructure
Status: Approved | Date: YYYY-MM-DD

Purpose:
Document production hosting and services configuration.

Hosting Platform:
{Platform and configuration details}

Environment Variables:
| Variable | Purpose | Required |
|----------|---------|----------|
| {name} | {purpose} | {yes/no} |

Services:
| Service | Purpose | Connection |
|---------|---------|------------|
| {service} | {purpose} | {how connected} |

Related IDs: DEP-XXX, MON-XXX
```

## Common Tool Categories

### Version/Environment Managers
- `mise`, `asdf`, `nvm`, `pyenv`, `rbenv`
- **Purpose**: Manage language versions per-project

### Code Quality
- **JavaScript/TypeScript**: `eslint`, `prettier`, `biome`
- **Python**: `ruff`, `black`, `pylint`
- **Go**: `golangci-lint`

### Type Checking
- **JavaScript/TypeScript**: `typescript`
- **Python**: `mypy`, `pyright`

### Data Processing
- `jq` (JSON), `yq` (YAML)

### API Testing
- `httpie`, `curl`, `bruno-cli`

### Git Workflows
- `gh` (GitHub CLI), `glab` (GitLab CLI)

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Global package pollution** | `npm install -g` for project packages | Use devDependencies |
| **Missing verification** | No way to confirm setup | Add verification commands |
| **Prose instead of structure** | Long paragraphs describing setup | Use tables and code blocks |
| **MCP over CLI** | Using MCP when CLI exists | Prefer CLI for portability |
| **Undocumented config** | Config files without explanation | Document purpose of each file |
| **Implicit dependencies** | Setup fails without warning | List all dependencies explicitly |

## Quality Gates

Before proceeding to Build Execution:

- [ ] ENV-001 documents all development tools
- [ ] All tools have install commands
- [ ] All packages are in package manifest
- [ ] Configuration files are listed with purpose
- [ ] Standard scripts defined (validate, fix, test)
- [ ] Verification commands work
- [ ] CLI preferred over MCP documented

## Downstream Connections

ENV- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.7 Build Execution** | ENV-001 defines dev setup | Developer follows ENV-001 to set up |
| **Onboarding** | ENV-001 as setup guide | New dev uses ENV-001 for first day |
| **CI/CD** | ENV-002 defines pipeline | GitHub Actions mirrors ENV-002 |
| **Deployment** | ENV-003 defines infrastructure | DEP- references ENV-003 |

## Detailed References

- **ENV- entry template**: See `assets/env.md`
- **Environment examples**: See `references/examples.md`
