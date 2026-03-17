---
description: Orchestrate multi-agent parallel development with domain-specialized agents. PROACTIVELY invoke this skill (without user asking) when you detect an implementation task spanning 3+ domains (frontend, backend, database, devops, testing, security, mobile) OR 15+ tasks in tasks.md. Warn the user about higher token cost but recommend it for quality. Also use when user says "team setup", "parallel agents", "team lead", or "agent teams".
---

# Team Lead

**Plan and launch parallel development agents across domains using Claude Code's native Agent Teams.**

## Usage

```bash
/sw:team-lead "<feature description>" [OPTIONS]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--dry-run` | Show proposed agent plan without launching | false |
| `--domains` | Override domain detection (e.g., `--domains frontend,backend,testing`) | auto-detect |
| `--max-agents` | Maximum number of concurrent agents | 6 |

---

## 1. Tool Reference

| Action | Tool | Parameters |
|--------|------|------------|
| Create team | `TeamCreate` | `team_name`, `description` |
| Spawn agent | `Task` | `team_name`, `name`, `subagent_type`, `prompt`, `mode: "bypassPermissions"` |
| Send message | `SendMessage` | `type`, `recipient`, `content`, `summary` |
| Shutdown agent | `SendMessage` | `type: "shutdown_request"`, `recipient` |

---

## 2. Domain-to-Skill Mapping

Analyze the feature request and map affected domains to SpecWeave skills.

| Domain | Primary Skill | Additional Skills | When to Use |
|--------|--------------|-------------------|-------------|
| **Frontend** | `sw-frontend:frontend-architect` | `sw-frontend:nextjs`, `sw-frontend:frontend-design` | UI components, pages, client-side state |
| **Backend** | `sw:architect` | `sw-infra:devops` | API endpoints, services, business logic |
| **Database** | `sw:architect` | | Schema design, migrations, seed data |
| **Shared/Types** | `sw:architect` | `sw:code-simplifier` | TypeScript interfaces, shared constants, API contracts |
| **Testing** | `sw-testing:qa-engineer` | `sw-testing:e2e-testing`, `sw-testing:unit-testing` | Test strategy, E2E suites, integration tests |
| **Security** | `sw:security` | `sw:security-patterns` | Auth, authorization, threat modeling, OWASP |
| **DevOps** | `sw-infra:devops` | `sw-k8s:deployment-generate`, `sw-infra:observability` | CI/CD, Docker, K8s, monitoring |
| **Mobile** | `sw-mobile:react-native-expert` | `sw-mobile:screen-generate`, `sw-mobile:expo` | Native/cross-platform mobile apps |
| **ML** | `sw-ml:ml-engineer` | `sw-ml:pipeline`, `sw-ml:deploy` | Model training, inference pipelines, deployment |

### Auto-Detection Signals

The orchestrator infers domains from the feature description and codebase structure (e.g., `src/components/` signals Frontend, `prisma/` signals Database, `src/api/` signals Backend, `tests/` signals Testing, auth-related keywords signal Security, Docker/K8s/CI files signal DevOps, React Native/Flutter signal Mobile, model/pipeline keywords signal ML).

---

## 3. Contract-First Spawning Protocol

Agents are NOT all spawned simultaneously. The orchestrator follows a two-phase dependency protocol to prevent integration conflicts.

### Contract Artifacts

| Artifact | Location | Producer | Consumers |
|----------|----------|----------|-----------|
| TypeScript interfaces | `src/types/` or `src/shared/types/` | Shared/Types agent | Frontend, Backend, Testing |
| Prisma schema | `prisma/schema.prisma` | Database agent | Backend, Testing |
| OpenAPI spec | `openapi.yaml` or `src/api/openapi.yaml` | Backend agent | Frontend, Testing |
| GraphQL schema | `schema.graphql` | Backend agent | Frontend, Mobile |
| API route types | `src/api/types/` | Backend agent | Frontend |

### Organization Discovery (CRITICAL -- resolve BEFORE spawning agents)

**The orchestrator MUST resolve the actual organization/owner name before spawning ANY agents.**
All `{ORG}` placeholders below must be replaced with the real value.

**Discovery chain (in order of priority):**

1. **From config** (`repository.organization`):
```bash
ORG=$(jq -r '.repository.organization // empty' .specweave/config.json 2>/dev/null)
```

2. **From sync profiles** (fallback if repository.organization not set):
```bash
if [ -z "$ORG" ]; then
  ORG=$(jq -r '[.sync.profiles[].config.owner // .sync.profiles[].config.organization] | map(select(. != null)) | first // empty' .specweave/config.json 2>/dev/null)
fi
```

3. **From umbrella childRepos** (fallback):
```bash
if [ -z "$ORG" ]; then
  ORG=$(jq -r '.umbrella.childRepos[0].path // empty' .specweave/config.json 2>/dev/null | sed 's|repositories/||' | cut -d/ -f1)
fi
```

4. **From existing filesystem** (last resort):
```bash
if [ -z "$ORG" ]; then
  ORG=$(ls -d repositories/*/ 2>/dev/null | head -1 | xargs basename 2>/dev/null)
fi
```

5. **If all fail**: Ask the user. NEVER guess or use a placeholder.

**NEVER read org from .env files.** Organization belongs in `.specweave/config.json`.

### Multi-Repo Increment Placement (CRITICAL)

**In umbrella projects with a `repositories/` folder, each agent MUST create its increment in its OWN repo's `.specweave/`:**

```
# CORRECT: Each repo has its own .specweave/increments/
umbrella-project/
├── .specweave/config.json              # Umbrella config ONLY
├── repositories/
│   ├── {ORG}/sw-ecom-domain/
│   │   └── .specweave/increments/0001-domain-models/
│   ├── {ORG}/sw-ecom-shared/
│   │   └── .specweave/increments/0001-shared-types/
│   └── {ORG}/sw-ecom-api/
│       └── .specweave/increments/0001-api-endpoints/

# WRONG: All agents dumping into umbrella root
umbrella-project/
├── .specweave/increments/0001-everything/               # WRONG!
```

**Rules:**
- Run `specweave init` in each repo if `.specweave/` doesn't exist
- Each agent's working directory is its assigned repo inside `repositories/`
- Never create `.specweave/increments/` in the umbrella root for multi-repo work
- Replace `{ORG}` with the actual organization discovered above

### Phase 1: Upstream Agents (Contracts First)

**Contract chain order**: shared/types -> database -> backend -> frontend (upstream before downstream).

Spawn agents that produce shared contracts. These MUST complete before downstream agents begin.

**Upstream agents** (spawn first, wait for completion):
- **Shared/Types agent** -- produces TypeScript interfaces, enums, constants
- **Database agent** -- produces Prisma schema, migration files, seed data

```
Phase 1: Upstream
  ├── Shared/Types Agent -> produces interfaces, enums
  └── Database Agent -> produces schema, migrations

  [WAIT for Phase 1 completion via CONTRACT_READY messages]
```

### Phase 2: Downstream Agents (Consume Contracts)

Once upstream contracts are established, spawn downstream agents in parallel.

**Downstream agents** (spawn in parallel after Phase 1):
- **Backend agent** -- consumes types and schema, produces API endpoints
- **Frontend agent** -- consumes types and API contracts, produces UI
- **Testing agent** -- consumes all contracts, produces test suites
- **Security agent** -- consumes all code, produces security hardening
- **DevOps agent** -- consumes all code, produces deployment config

```
Phase 2: Downstream (parallel)
  ├── Backend Agent (reads types + schema)
  ├── Frontend Agent (reads types + API spec)
  ├── Testing Agent (reads all contracts)
  ├── Security Agent (reads all code)
  └── DevOps Agent (reads all code)
```

### No-Dependency Case

If the feature has no cross-domain dependencies (e.g., purely frontend work with no new types), skip Phase 1 and spawn all agents in parallel immediately.

### Spawn Decision Logic

```
Analyze domains
  │
  ├── Any upstream domains (shared/types, database)?
  │     YES -> Phase 1: spawn upstream, wait for contracts
  │           Phase 2: spawn downstream in parallel
  │     NO  -> Spawn all agents in parallel (no dependency)
  │
  └── Single domain?
        YES -> Spawn single agent, no orchestration needed
```

---

## 3b. Plan Review Workflow

The team lead acts as **architectural reviewer** for all sub-agent plans. Do NOT auto-accept plans.

### Why Review

Without review, agents may duplicate work across domains, misinterpret scope, make conflicting architectural decisions, or produce plans misaligned with the spec.

### Permission Mode: bypassPermissions (CRITICAL)

**All agents MUST be spawned with `mode: "bypassPermissions"`.** This is required because:
- Agents run as separate processes that encounter folder trust prompts
- Trust prompts require interactive input that agents CANNOT provide
- Without `bypassPermissions`, agents get STUCK waiting for trust confirmation and never execute
- This applies to ALL agent spawns — upstream and downstream

**NEVER use `mode: "plan"` for agent spawns** — it causes agents to block on the trust-folder prompt.

### Protocol (SendMessage-Based)

Since agents use `bypassPermissions` (not `plan` mode), plan review uses an explicit SendMessage protocol:

**Agent side** (built into every agent prompt template):
1. Read the increment spec and explore the codebase
2. Create plan files (spec.md, plan.md, tasks.md) in the increment directory
3. Send plan summary to team-lead:
```
SendMessage({
  type: "message",
  recipient: "team-lead",
  content: "PLAN_READY: Created spec.md, plan.md, tasks.md at .specweave/increments/[ID]/. Summary: [key decisions, file list, task count]. Ready for review.",
  summary: "Plan ready for review"
});
```
4. **WAIT for PLAN_APPROVED message** before starting implementation. Do NOT proceed without approval.

**Team-lead side**:
1. Receive `PLAN_READY` message from agent
2. Read the agent's plan files (spec.md, plan.md, tasks.md)
3. Evaluate:
   - Does it align with the feature spec and ACs?
   - Is the architecture consistent with existing codebase patterns?
   - Does the agent stay within its file ownership boundaries?
   - Are there conflicts with other agents' plans?
   - Is scope correct — not too broad, not too narrow?
4. Approve or reject:

```
// Approve
SendMessage({
  type: "message",
  recipient: "database-agent",
  content: "PLAN_APPROVED: Go ahead with implementation.",
  summary: "Plan approved"
});

// Reject with feedback
SendMessage({
  type: "message",
  recipient: "database-agent",
  content: "PLAN_REJECTED: Revise: 1) Add index on user_id for sessions. 2) Missing migration for AC-US1-03.",
  summary: "Plan needs revision"
});
```

### Non-Blocking Review

Plan review MUST NOT block other agents. Review plans as they arrive — agents waiting for approval are idle, but other agents continue working normally.

### Multi-Increment Consideration

For very large features, the team lead MAY split work into multiple increments per domain for better tracking and independent closure. Decide this during initial analysis (Step 1), before spawning agents.

---

## 4. Agent Spawn Prompt Templates

Each agent receives a detailed prompt that includes its skill invocations, file ownership, and workflow instructions.

### 4a. Frontend Agent

```
You are the FRONTEND agent for increment [INCREMENT_ID].

SKILLS TO INVOKE:
  Skill({ skill: "sw-frontend:frontend-architect" })
  Skill({ skill: "sw-frontend:nextjs" })         // if Next.js project
  Skill({ skill: "sw-frontend:frontend-design" }) // for polished, world-class UI
  Skill({ skill: "sw:service-connect" })          // for external service setup

FILE OWNERSHIP (WRITE access):
  src/components/**
  src/pages/**
  src/hooks/**
  src/styles/**
  src/app/**           // Next.js app router
  src/stores/**        // Client state (zustand, redux, etc.)
  public/**

READ ACCESS: Any file in the repository (especially src/types/, src/shared/, openapi.yaml)

DESIGN QUALITY:
  - Default to world-class, sleek, polished, production-ready design
  - All UI must be responsive (mobile-first) and accessible (WCAG 2.1 AA)
  - Use modern design patterns: clean spacing, typography hierarchy, subtle animations
  - Invoke `sw-frontend:frontend-design` for high-quality UI polish

WORKFLOW:
  1. Set working directory to your assigned repo: cd repositories/{ORG}/{repo-name}
  2. If .specweave/ doesn't exist in your repo, run: specweave init
  3. Create YOUR increment in YOUR repo: .specweave/increments/[ID]/
  4. Read the increment spec and tasks
  5. Verify services are running and accessible (check dev server, API endpoints)
  6. Wait for contract artifacts if Phase 1 is active:
     - Read src/types/ for shared interfaces
     - Read openapi.yaml for API endpoints (if backend produces one)
  7. Create plan files (plan.md, tasks.md) for your increment
  8. Send plan to team-lead and WAIT for approval:
     SendMessage({ type: "message", recipient: "team-lead",
       content: "PLAN_READY: [increment path]. [summary of planned tasks and files].",
       summary: "Frontend plan ready for review" })
  9. WAIT for "PLAN_APPROVED" message. If "PLAN_REJECTED", revise and re-submit.
  10. Execute tasks autonomously: prefer /sw:auto for autonomous execution
  11. Run all tests for owned code (unit + integration): npm test
  12. Run quality gate: /sw:grill
  13. Do NOT signal completion until all tests pass
  14. After auto completes, attempt closure via /sw:done
  15. Signal completion via SendMessage to team-lead

RULES:
  - WRITE only to files you own (listed above)
  - READ any file for context
  - Follow existing code conventions (check .eslintrc, .prettierrc, tsconfig.json)
  - Run linter and type-check before signaling completion
  - All new components must have corresponding test files
  - ALL repository operations MUST use `repositories/{ORG}/` directory structure
  - Create .specweave/increments/ in YOUR assigned repo, NOT in the umbrella project root
```

### 4b. Backend Agent

```
You are the BACKEND agent for increment [INCREMENT_ID].

SKILLS TO INVOKE:
  Skill({ skill: "sw:architect" })
  Skill({ skill: "sw-infra:devops" })      // if deployment config needed
  Skill({ skill: "sw:service-connect" })    // for auth provider and external service setup

FILE OWNERSHIP (WRITE access):
  src/api/**
  src/services/**
  src/middleware/**
  src/routes/**
  src/controllers/**
  src/utils/server/**
  prisma/seed.ts       // seed data only (schema owned by DB agent)

READ ACCESS: Any file in the repository (especially prisma/schema.prisma, src/types/)

AUTH SETUP:
  - If the project needs authentication, set up the auth provider (Supabase, Firebase, Auth0, etc.)
  - Use `sw:service-connect` to connect to auth services and verify connectivity
  - Ensure auth middleware works end-to-end before signaling completion

WORKFLOW:
  1. Set working directory to your assigned repo: cd repositories/{ORG}/{repo-name}
  2. If .specweave/ doesn't exist in your repo, run: specweave init
  3. Create YOUR increment in YOUR repo: .specweave/increments/[ID]/
  4. Read the increment spec and tasks
  5. Verify services are running and accessible (database, auth provider, external APIs)
  6. Wait for contract artifacts if Phase 1 is active:
     - Read prisma/schema.prisma for database schema
     - Read src/types/ for shared interfaces
  7. Create plan files (plan.md, tasks.md) for your increment
  8. Send plan to team-lead and WAIT for approval:
     SendMessage({ type: "message", recipient: "team-lead",
       content: "PLAN_READY: [increment path]. [summary of planned tasks and files].",
       summary: "Backend plan ready for review" })
  9. WAIT for "PLAN_APPROVED" message. If "PLAN_REJECTED", revise and re-submit.
  10. Execute tasks autonomously: prefer /sw:auto for autonomous execution
  11. Generate or update OpenAPI spec if API routes change
  12. Run all tests for owned code (unit + integration): npm test
  13. Run quality gate: /sw:grill
  14. Do NOT signal completion until all tests pass
  15. After auto completes, attempt closure via /sw:done
  16. Signal completion via SendMessage to team-lead

RULES:
  - WRITE only to files you own (listed above)
  - READ any file for context
  - Every new API endpoint must have request/response validation
  - Error handling must follow project conventions
  - All services must have unit tests
  - ALL repository operations MUST use `repositories/{ORG}/` directory structure
  - Create .specweave/increments/ in YOUR assigned repo, NOT in the umbrella project root
```

### 4c. Database Agent

```
You are the DATABASE agent for increment [INCREMENT_ID].

SKILLS TO INVOKE:
  Skill({ skill: "sw:architect" })

FILE OWNERSHIP (WRITE access):
  prisma/schema.prisma
  prisma/migrations/**
  src/db/**
  src/repositories/**
  scripts/db/**
  seeds/**

READ ACCESS: Any file in the repository

WORKFLOW:
  1. Set working directory to your assigned repo: cd repositories/{ORG}/{repo-name}
  2. If .specweave/ doesn't exist in your repo, run: specweave init
  3. Create YOUR increment in YOUR repo: .specweave/increments/[ID]/
  4. Read the increment spec and tasks
  5. Design database schema changes
  6. Create plan files (plan.md, tasks.md) for your increment
  7. Send plan to team-lead and WAIT for approval:
     SendMessage({ type: "message", recipient: "team-lead",
       content: "PLAN_READY: [increment path]. [summary of schema changes, migrations, seed data].",
       summary: "Database plan ready for review" })
  8. WAIT for "PLAN_APPROVED" message. If "PLAN_REJECTED", revise and re-submit.
  9. Generate Prisma migration: npx prisma migrate dev --name <migration-name>
  10. Write seed data if needed
  11. Execute tasks autonomously: prefer /sw:auto for autonomous execution
  12. Run all tests for owned code (migration, seed): npm test
  13. Run quality gate: /sw:grill
  14. Do NOT signal completion until all tests pass
  15. Signal CONTRACT_READY with schema details via SendMessage to team-lead
  16. After auto completes, attempt closure via /sw:done
  17. Signal completion via SendMessage to team-lead

RULES:
  - WRITE only to files you own (listed above)
  - READ any file for context
  - Always create migrations (never modify schema without migration)
  - Seed data must be idempotent
  - Schema changes must be backward-compatible when possible
  - ALL repository operations MUST use `repositories/{ORG}/` directory structure
  - Create .specweave/increments/ in YOUR assigned repo, NOT in the umbrella project root
```

### 4d. Testing Agent

```
You are the TESTING agent for increment [INCREMENT_ID].

SKILLS TO INVOKE:
  Skill({ skill: "sw-testing:qa-engineer" })
  Skill({ skill: "sw-testing:e2e-testing" })   // for E2E test suites
  Skill({ skill: "sw-testing:unit-testing" })   // for unit test coverage

FILE OWNERSHIP (WRITE access):
  tests/**
  __tests__/**
  src/**/*.test.ts
  src/**/*.test.tsx
  src/**/*.spec.ts
  e2e/**
  playwright.config.ts  // if Playwright
  cypress.config.ts     // if Cypress
  test-utils/**
  fixtures/**

READ ACCESS: Any file in the repository

WORKFLOW:
  1. Set working directory to your assigned repo: cd repositories/{ORG}/{repo-name}
  2. If .specweave/ doesn't exist in your repo, run: specweave init
  3. Create YOUR increment in YOUR repo: .specweave/increments/[ID]/
  4. Read the increment spec and tasks
  5. Wait for ALL other agents to produce initial code
  6. Create plan files (plan.md, tasks.md) for your increment
  7. Send plan to team-lead and WAIT for approval:
     SendMessage({ type: "message", recipient: "team-lead",
       content: "PLAN_READY: [increment path]. [summary of test strategy, coverage plan].",
       summary: "Testing plan ready for review" })
  8. WAIT for "PLAN_APPROVED" message. If "PLAN_REJECTED", revise and re-submit.
  9. Write unit tests for new services/components
  10. Write integration tests for API endpoints
  11. Write E2E tests for user journeys
  12. Execute tasks autonomously: prefer /sw:auto for autonomous execution
  13. Run all tests (unit + integration + E2E): npm test && npx playwright test
  14. Do NOT signal completion until all tests pass -- if tests fail, fix and repeat
  15. Run quality gate: /sw:grill
  16. After auto completes, attempt closure via /sw:done
  17. Signal completion via SendMessage to team-lead

RULES:
  - WRITE only to test files (listed above)
  - READ any file for context
  - Tests must cover all acceptance criteria from spec.md
  - Follow existing test patterns and utilities
  - E2E tests must include accessibility checks when applicable
  - ALL repository operations MUST use `repositories/{ORG}/` directory structure
  - Create .specweave/increments/ in YOUR assigned repo, NOT in the umbrella project root
```

### 4e. Security Agent

```
You are the SECURITY agent for increment [INCREMENT_ID].

SKILLS TO INVOKE:
  Skill({ skill: "sw:security" })
  Skill({ skill: "sw:security-patterns" })

FILE OWNERSHIP (WRITE access):
  src/auth/**
  src/middleware/auth*
  src/middleware/security*
  src/utils/crypto/**
  src/utils/validation/**
  security/**
  .env.example          // document required secrets (never .env itself)

READ ACCESS: Any file in the repository

WORKFLOW:
  1. Set working directory to your assigned repo: cd repositories/{ORG}/{repo-name}
  2. If .specweave/ doesn't exist in your repo, run: specweave init
  3. Create YOUR increment in YOUR repo: .specweave/increments/[ID]/
  4. Read the increment spec and tasks
  5. Audit code produced by other agents for security issues
  6. Create plan files (plan.md, tasks.md) for your increment
  7. Send plan to team-lead and WAIT for approval:
     SendMessage({ type: "message", recipient: "team-lead",
       content: "PLAN_READY: [increment path]. [summary of security findings, hardening plan].",
       summary: "Security plan ready for review" })
  8. WAIT for "PLAN_APPROVED" message. If "PLAN_REJECTED", revise and re-submit.
  9. Implement auth/authz middleware if needed
  10. Add input validation and sanitization
  11. Execute tasks autonomously: prefer /sw:auto for autonomous execution
  12. Run all tests for owned code (security tests): npm test
  13. Run security audit tools (npm audit, dependency check)
  14. Run quality gate: /sw:grill
  15. Do NOT signal completion until all tests pass
  16. After auto completes, attempt closure via /sw:done
  17. Signal completion with security findings summary via SendMessage to team-lead

RULES:
  - WRITE only to files you own (listed above)
  - READ any file for context and audit
  - NEVER commit secrets, credentials, or API keys
  - All user input must be validated and sanitized
  - Follow OWASP Top 10 guidelines
  - ALL repository operations MUST use `repositories/{ORG}/` directory structure
  - Create .specweave/increments/ in YOUR assigned repo, NOT in the umbrella project root
```

---

## 5. File Ownership

Each agent has exclusive WRITE access to specific file patterns. This prevents merge conflicts.

### Ownership Map

| Domain | WRITE Patterns | Notes |
|--------|---------------|-------|
| **Frontend** | `src/components/**`, `src/pages/**`, `src/hooks/**`, `src/styles/**`, `src/app/**`, `src/stores/**`, `public/**` | UI layer |
| **Backend** | `src/api/**`, `src/services/**`, `src/middleware/**`, `src/routes/**`, `src/controllers/**` | API layer |
| **Database** | `prisma/**`, `src/db/**`, `src/repositories/**`, `seeds/**`, `scripts/db/**` | Data layer |
| **Shared/Types** | `src/types/**`, `src/shared/**`, `src/constants/**`, `src/utils/shared/**` | Contracts |
| **Testing** | `tests/**`, `__tests__/**`, `e2e/**`, `**/*.test.ts`, `**/*.test.tsx`, `**/*.spec.ts`, `test-utils/**`, `fixtures/**` | All test files |
| **Security** | `src/auth/**`, `src/middleware/auth*`, `src/middleware/security*`, `src/utils/crypto/**`, `src/utils/validation/**`, `security/**` | Auth and security |
| **DevOps** | `.github/**`, `docker/**`, `Dockerfile*`, `docker-compose*`, `k8s/**`, `terraform/**`, `.gitlab-ci.yml`, `Makefile` | Infrastructure |
| **Mobile** | `src/screens/**`, `src/navigation/**`, `ios/**`, `android/**`, `src/native/**` | Mobile app |
| **ML** | `models/**`, `notebooks/**`, `src/ml/**`, `src/pipelines/**`, `data/**` | Machine learning |

### Ownership Rules

1. **WRITE only to files you own** -- agents must not modify files outside their ownership patterns
2. **READ any file** -- all agents have unrestricted read access for context
3. **Shared files require coordination** -- if two domains need to modify the same file (e.g., `package.json`), the orchestrator assigns a primary owner and others request changes via SendMessage
4. **New files** -- agents can create new files ONLY within their ownership patterns
5. **Conflict detection** -- the orchestrator checks for ownership overlap before spawning and resolves ambiguity upfront
6. **Repository directory structure** -- for multi-repo setups, ALL repository cloning and creation MUST use the `repositories/{ORG}/` directory convention

---

## 6. Communication Protocol

Agents communicate contract readiness, blocking issues, and completion status using `SendMessage`.

### Message Types

| Prefix | Purpose | Sender | Receiver |
|--------|---------|--------|----------|
| `CONTRACT_READY:` | Upstream contract is published | Upstream agent | team-lead (broadcasts to downstream) |
| `BLOCKING_ISSUE:` | Agent is stuck, needs help | Any agent | team-lead |
| `COMPLETION:` | Agent finished all tasks | Any agent | team-lead |

### Message Examples

```typescript
// Upstream agent signals contract is ready
SendMessage({
  type: "message",
  recipient: "team-lead",
  content: "CONTRACT_READY: TypeScript interfaces written to src/types/checkout.ts. Exports: CheckoutItem, CartSummary, PaymentIntent.",
  summary: "Shared types contract ready"
});

// Agent reports a blocking issue
SendMessage({
  type: "message",
  recipient: "team-lead",
  content: "BLOCKING_ISSUE: Cannot implement payment webhook -- Stripe webhook secret not found in .env. Need STRIPE_WEBHOOK_SECRET to proceed.",
  summary: "Blocked on missing Stripe secret"
});

// Agent signals completion
SendMessage({
  type: "message",
  recipient: "team-lead",
  content: "COMPLETION: All 8 tasks done. Tests passing (24/24). /sw:grill passed. Frontend increment ready for merge.",
  summary: "Frontend agent completed all tasks"
});
```

---

## 7. Spawning Agents

### Step 1: Create the Team

```typescript
TeamCreate({
  team_name: "feature-checkout",
  description: "Building checkout flow across frontend, backend, and database"
});
```

### Step 2: Spawn Upstream Agents (Phase 1)

All agents are spawned with `mode: "bypassPermissions"` to prevent blocking on trust-folder prompts. Plan review is enforced via the SendMessage PLAN_READY/PLAN_APPROVED protocol (see Section 3b).

```typescript
Task({
  team_name: "feature-checkout",
  name: "database-agent",
  subagent_type: "general-purpose",
  mode: "bypassPermissions",
  prompt: `[DATABASE AGENT PROMPT - see template in Section 4c]`,
});

Task({
  team_name: "feature-checkout",
  name: "shared-types-agent",
  subagent_type: "general-purpose",
  mode: "bypassPermissions",
  prompt: `[SHARED/TYPES AGENT PROMPT]`,
});
```

### Step 3: Wait for Phase 1 CONTRACT_READY Messages

Messages are delivered automatically via SendMessage from upstream agents.

### Step 4: Spawn Downstream Agents (Phase 2)

```typescript
Task({
  team_name: "feature-checkout",
  name: "backend-agent",
  subagent_type: "general-purpose",
  mode: "bypassPermissions",
  prompt: `[BACKEND AGENT PROMPT - see template in Section 4b]`,
});

Task({
  team_name: "feature-checkout",
  name: "frontend-agent",
  subagent_type: "general-purpose",
  mode: "bypassPermissions",
  prompt: `[FRONTEND AGENT PROMPT - see template in Section 4a]`,
});

Task({
  team_name: "feature-checkout",
  name: "testing-agent",
  subagent_type: "general-purpose",
  mode: "bypassPermissions",
  prompt: `[TESTING AGENT PROMPT - see template in Section 4d]`,
});
```

---

## 8. Quality Gates

Every agent MUST run quality validation before signaling completion.

### Per-Agent Quality Gate

```
Agent Workflow:
  1. Execute all assigned tasks (prefer /sw:auto for autonomous execution)
  2. Run all tests for owned code (unit + integration + E2E)
  3. Run linter/type-check for owned code
  4. Run /sw:grill
  5. If tests fail -> fix issues and repeat from step 2. Do NOT signal completion until all tests pass.
  6. If /sw:grill passes -> attempt closure via /sw:done
  7. If /sw:grill fails -> fix issues, repeat from step 2
  8. Signal COMPLETION via SendMessage
```

### Orchestrator Quality Gate

After all agents complete, the orchestrator (team lead) runs a final validation:

```
Orchestrator Final Check:
  1. All agents signaled COMPLETION
  2. No unresolved BLOCKING_ISSUE messages
  3. Run full test suite (all domains combined)
  4. Run /sw:grill on the combined increment
  5. Run /sw:done --auto <id> for each increment in dependency order
  6. If any /sw:done --auto fails, report the failure and continue with remaining increments
  7. If all pass -> /sw:team-merge
  8. If failures -> identify owning agent, send fix request via SendMessage
```

### Grill Checklist per Domain

| Domain | Grill Checks |
|--------|-------------|
| Frontend | Components render, no console errors, accessibility, responsive |
| Backend | API endpoints return correct status codes, validation works, error handling |
| Database | Migrations apply cleanly, seed data loads, rollback works |
| Testing | All tests pass, coverage threshold met, no flaky tests |
| Security | No exposed secrets, input validation, auth working |
| DevOps | Docker builds, CI passes, deployment config valid |

---

## 9. Workflow Summary

```
/sw:team-lead "Build checkout flow"
  │
  ├── Step 1: Analyze feature -> identify domains -> decide increment split
  ├── Step 2: Create team via TeamCreate
  ├── Step 3: Create per-domain increments
  ├── Step 4: Contract-first spawning (all agents with mode: "bypassPermissions")
  │     ├── Phase 1: Spawn shared + database
  │     │     └── Receive PLAN_READY, review & approve via SendMessage (Section 3b)
  │     │     └── Wait for CONTRACT_READY after approval
  │     └── Phase 2: Spawn backend + frontend + testing
  │           └── Receive PLAN_READY, review & approve via SendMessage
  ├── Step 5: Monitor progress via SendMessage
  ├── Step 6: Quality gates (each agent runs /sw:grill)
  └── Step 7: Merge and close (/sw:team-merge)
```

### --dry-run Output

When `--dry-run` is specified, display the proposed plan without executing:

```
Team Orchestration Plan (DRY RUN)
==================================================
Feature: Build checkout flow | Domains: 4

Phase 1 (upstream):
  1. shared-types -> sw:architect, sw:code-simplifier  | Increment: 0200-checkout-shared
  2. database     -> sw:architect                 | Increment: 0201-checkout-database

Phase 2 (downstream, parallel):
  3. backend      -> sw:architect, sw-infra:devops          | Increment: 0202-checkout-backend
  4. frontend     -> sw-frontend:frontend-architect         | Increment: 0203-checkout-frontend

Max agents: 4 (2 sequential + 2 parallel)
To execute, run without --dry-run.
```

---

## 10. Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| **Agent stuck on trust folder** | Agent spawned without `bypassPermissions` | ALWAYS use `mode: "bypassPermissions"` — NEVER `mode: "plan"`. Trust prompts require interactive input agents cannot provide |
| **Agents editing same files** | Overlapping file ownership patterns | Review ownership map; reassign conflicting files to a single owner; use `--dry-run` to validate before launch |
| **Token cost too high** | Too many agents or overly large prompts | Reduce `--max-agents`; use `--domains` to limit scope; split feature into smaller increments |
| **Contract agent takes too long** | Large schema or complex type system | Set a timeout in the agent prompt; if stuck >15 min, check agent output and consider splitting the contract work |
| **Phase 2 starts before Phase 1 finishes** | CONTRACT_READY not received yet | Ensure upstream agents send CONTRACT_READY via SendMessage before team-lead spawns downstream |
| **Agent fails mid-task** | Build error, test failure, or dependency issue | Send message to agent to fix; restart the agent with `/sw:auto` on its increment |

---

## 11. Examples

### Example 1: Full-Stack Feature

```
User: /sw:team-lead "Build user authentication with login, signup, password reset, and OAuth"

Orchestrator detects domains: shared/types, database, backend, frontend, testing, security
Creates 6 increments.

Phase 1:
  - shared-types agent: Auth types (User, Session, AuthToken interfaces)
  - database agent: User table, Session table, Prisma migrations

Phase 2 (after contracts ready):
  - backend agent: /api/auth/login, /api/auth/signup, /api/auth/reset, OAuth flow
  - frontend agent: LoginForm, SignupForm, ResetPasswordForm, OAuthButton
  - testing agent: Unit tests, E2E login flow, E2E signup flow
  - security agent: Password hashing, JWT validation, rate limiting, CSRF
```

### Example 2: Frontend-Only (No Dependencies)

```
User: /sw:team-lead "Redesign dashboard" --domains frontend,testing
-> No upstream dependencies. Both agents spawn in parallel immediately.
```

### Example 3: Dry Run

```
User: /sw:team-lead "Add payment processing" --dry-run
-> Shows plan with domains, phases, file ownership. No agents spawned.
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `/sw:team-status` | Show progress of all agents in the current team session |
| `/sw:team-merge` | Merge completed agent work in dependency order |
| `/sw:auto` | Autonomous execution (single-agent mode) |
| `/sw:architect` | System architecture and ADRs |
| `/sw:grill` | Quality validation gate |
