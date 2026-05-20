---
name: codewiki
description: >
  Generate a structured product knowledge base from codebase scanning.
  Creates a codewiki/ folder with architecture docs, user flows, API reference,
  service maps, and more. Also generates CLAUDE.md. Handles single repos,
  monorepos, and multi-repo microservices. Use when asked to document a project,
  generate a knowledge base, map architecture, create onboarding docs, or
  set up CLAUDE.md for a codebase.
user-invocable: true
---

# CodeWiki — Product Knowledge Base Generator

Scan code, fetch product context, discover user flows, and generate a structured `codewiki/` knowledge base.

Output templates are in this skill's `templates/` directory. Read each template only when generating that specific file — do NOT load all templates at once.

## HARD RULES

1. **Phase 1 is not optional.** Product context is the difference between a useful wiki and a mechanical code listing. Complete it before scanning. If user can't answer, use the code-first fallback.
2. **Multi-repo workspace must be verified before scanning.** If repos aren't in a shared parent folder, stop and help the user set it up.
3. **Never scan all repos simultaneously.** Use Scan → Write to `_scratch/` → Carry 30-line summary → Next. This is how you survive large multi-repo projects.
4. **Never skip a service in microservices.** User flows that touch 5 services are useless if one is undocumented. Every service gets at least a lightweight scan.
5. **Scan in priority order.** Infrastructure/contracts → gateway → frontends → core business services → supporting services.
6. **Report progress between repos.** Tell the user what you found and which repo is next. Do not ask for permission between repos — just continue. Only pause on errors or contradictions.
7. **On startup, check if `codewiki/_scratch/` exists.** If it does, offer to resume from previous scan data.
8. **Always use `codewiki/` (no dot prefix).** Ensures visibility in file explorers and default git tracking.
9. **Adaptive detection.** If hardcoded grep patterns don't match anything for a component, read the entry point file and trace outward. Don't report "no endpoints found" without trying alternative approaches.
10. **WebFetch failures.** Report the specific error (401, 404, timeout) and continue. Never silently skip a URL.

---

## Phase 1: Product Context Gathering (MANDATORY — DO NOT SKIP)

> **STOP. You MUST complete Phase 1 before scanning any code.**
> Do not run `ls`, `grep`, or read any files until Phase 1 is done.
> If the user says "just scan the code" or tries to skip, explain that
> the wiki quality depends heavily on product context and ask them to
> answer at least questions 1–3 before proceeding.

### Step 1a: Ask the User

Ask all of these in a single message. Mark which are required vs. optional:

1. **Product name** *(required)* — What is this product called?
2. **One-liner** *(required)* — Describe it in one sentence. What does it do and for whom?
3. **Target users** *(required)* — Who uses this? (e.g., developers, marketers, internal ops team)
4. **Product URLs** *(optional but strongly recommended)* — Provide any of:
   - Marketing website / landing page
   - Documentation site
   - API docs URL
   - App Store / Play Store listing
   - README or repo URL (if different from the working directory)
5. **Repo list** *(required for multi-repo)* — If this is a multi-repo product:
   - List all repos (backend, frontend, mobile app, comms, infra, etc.)
   - Are they all cloned into a single parent folder? If not, I'll ask you to set that up.
   - Provide git clone URLs for any not yet cloned.
6. **Anything the code won't tell me?** *(optional)* — Business context, upcoming changes, non-obvious terminology, areas of tech debt, inter-service communication patterns, etc.

**Code-first fallback:** If user says they can't answer 1–3, say: "No problem — I'll scan the code first and come back with my best guess for you to correct." Infer product name from package.json `name` field or README title, one-liner from package.json `description` or README first paragraph, users from UI/API patterns (admin dashboard = internal ops, public signup = consumers, API-only = developers). Present guesses for confirmation before continuing to Phase 2.

### Step 1b: Multi-Repo Workspace Setup

> **For multi-repo products, all repos MUST be cloned into a single parent folder.**
> This is how CodeWiki discovers cross-repo relationships.

Expected structure:
```
<product-name>/              ← master folder
├── backend/                 ← git clone <backend-url>
├── frontend/                ← git clone <frontend-url>
├── mobile-app/              ← git clone <mobile-url>
├── comms-service/           ← git clone <comms-url>
├── shared-libs/             ← git clone <shared-url>
└── infra/                   ← git clone <infra-url>
```

**If repos are not yet organized this way**, give the user exact commands:
```bash
mkdir -p ~/projects/<product-name> && cd ~/projects/<product-name>
git clone <url-1> <folder-name-1>
git clone <url-2> <folder-name-2>
# ... etc
```

Then ask the user to `cd` into the master folder and run CodeWiki from there.

**Verify the setup:**
```bash
ls -la
for dir in */; do echo "$dir: $(git -C "$dir" remote get-url origin 2>/dev/null || echo 'not a git repo')"; done
```

If any repos are missing, tell the user which ones and provide the clone command. Do NOT proceed to Phase 2 until the workspace is verified.

### Step 1c: Fetch External Context

For each URL provided, use WebFetch to extract product context.

**Error handling:** If a URL fails (auth wall, 404, timeout), tell the user which URL failed and why, then continue with the rest. Do not silently skip.

For each successful fetch, extract:
- Landing page copy, feature descriptions, value propositions
- App store descriptions and key metadata
- Documentation structure (table of contents, section names)
- API documentation overview (auth method, base URL, resource groups)

### Step 1d: Summarize Before Proceeding

Present a short summary back to the user:
> "Here's what I understand about [Product Name] before I look at the code: ..."

Ask: **"Is this accurate? Anything to correct or add?"**

Only after the user confirms, proceed to Phase 2.

After confirmation, estimate scope:
> "Based on [N repos/components], this will take [several phases]. I'll report progress after each repo/component."

---

## Context Window Management (Multi-Repo Strategy)

> **CRITICAL: Do NOT scan all repos at once.** Scanning multiple repos simultaneously
> will exhaust the context window. Instead, use the Scan → Summarize → Flush → Next
> pattern described below.

### Scan Priority Order

Scan in this order. The goal is top-down: infrastructure first (the "map"), then entry points, then services behind them.

**Priority 1 — Infrastructure & contracts (scan first)**
- `infra/`, `deploy/`, `platform/` — docker-compose, k8s manifests, terraform
- Shared proto/OpenAPI/AsyncAPI specs
- Shared libraries / type packages

*Why first:* Gives you the full service map, ports, dependencies, and contracts before any individual service. It's the table of contents.

**Priority 2 — API gateway / BFF (Backend-for-Frontend)**
- The service that receives external traffic and routes it internally
- Often named: `gateway`, `api-gateway`, `bff`, `proxy`

*Why second:* Shows all user-facing endpoints and which internal service handles each one.

**Priority 3 — Frontend(s)**
- Web frontend, mobile app, admin dashboard
- Scan routes/screens, API client configuration, state management

*Why third:* Now you can map screens → gateway endpoints → internal services.

**Priority 4 — Core business services**
- Services that own primary business data (users, orders, payments, etc.)
- Prioritize by: how many user flows touch this service

**Priority 5 — Supporting services**
- Notifications, analytics, logging, search, file storage
- These are consumed by other services but rarely initiate flows

### The Scan → Summarize → Flush → Next Pattern

For each repo/service, follow this cycle:

```
1. SCAN      Read the repo: tech stack, endpoints, models, events, env vars
2. WRITE     Write findings to codewiki/_scratch/<repo-name>.md (on disk)
3. SUMMARIZE Create a compact summary (max 30 lines) of:
             - What this service does (1-2 sentences)
             - Endpoints it exposes (list)
             - Events it produces/consumes (list)
             - Data models it owns (list)
             - How it connects to other services (list)
4. CARRY     Keep ONLY the compact summary in working memory
5. NEXT      Move to the next repo — raw scan data is on disk, not in context
```

**The `_scratch/` folder:**
```
codewiki/
├── _scratch/                  ← temporary, per-repo scan notes
│   ├── backend.md
│   ├── frontend.md
│   ├── comms-service.md
│   └── ...
├── overview.md                ← final output files (generated in Phase 5)
├── architecture.md
└── ...
```

**Compact summary format** (carried between repo scans):
```markdown
## <service-name> | <tech stack> | <port>
Purpose: <one sentence>
Endpoints: GET /users, POST /users, GET /users/:id, ...
Produces: user.created, user.updated
Consumes: payment.completed
Models: User, Role, Session
Calls: payment-service (gRPC), notification-service (HTTP)
DB: postgres (users, roles, sessions tables)
```

### Progress Reporting

After scanning each repo, tell the user:
> "✓ Scanned **backend** (3/6 repos done). Found 14 endpoints, 3 event topics, 5 models.
> Next up: **comms-service**. Continuing..."

Do NOT ask for permission between each repo — just report progress and continue.

---

## Phase 2: Codebase Analysis

### Step 2a: Project Layout & Scoping

**Single-repo projects:**
```bash
ls -la
find . -maxdepth 2 -type f -name "*.json" -o -name "*.toml" -o -name "*.yaml" -o -name "*.yml" -o -name "*.mod" -o -name "*.lock" | head -50
```

**Multi-repo master folder:**
```bash
ls -la
for dir in */; do
  echo "=== $dir ==="
  ls "$dir"/*.json "$dir"/*.toml "$dir"/*.yaml "$dir"/*.yml "$dir"/*.mod "$dir"/Dockerfile 2>/dev/null
  echo ""
done
```

Identify:
- **Single repo:** Project type (monorepo, single app, library, CLI tool, etc.)
- **Multi-repo:** Map each folder to its role (backend, frontend, mobile, comms, infra, shared libs, etc.)

For multi-repo, present the inventory:
> "I found [N] repos in this workspace:
> | Folder | Likely role | Stack signals |
> |--------|------------|---------------|
> | backend/ | API server | go.mod, Dockerfile |
> | frontend/ | Web app | package.json (next), tsconfig.json |
> | ...
>
> I'll scan them in this order: [list in priority order]. Starting now."

#### Architecture Classification

Classify the project:
- **Single app** — one deployable unit (e.g., a Rails app, a Next.js full-stack app)
- **Modular monolith** — one deployable unit with clearly separated internal modules
- **Microservices** — multiple independently deployable services
- **Monorepo with shared packages** — multiple apps/services sharing code via a package manager workspace

Detection signals for **microservices**:
- `docker-compose.yml` defining multiple services with separate build contexts
- Multiple directories each with their own `Dockerfile`
- Multiple directories each with their own dependency files (separate `go.mod`, `package.json`, `requirements.txt`)
- Presence of API gateway, service mesh config, or message broker config
- Proto/OpenAPI/AsyncAPI spec files defining service contracts
- Kubernetes manifests or Helm charts with multiple deployments

State your classification to the user before proceeding.

#### Scoping Gate

**If microservices or multi-service architecture:**
Do NOT ask the user to skip services. Instead, use a two-tier scan:

> "This is a microservices project with [N] services. I found: [list them].
> I'll do a **lightweight scan** of all services first to map the full topology,
> then a **deep scan** of the [3–4] most critical ones.
> Which services are most critical to document in depth?"

**Lightweight scan** (ALL services): tech stack, exposed endpoints/topics/events, data models owned, env vars, Dockerfile/deployment config.
**Deep scan** (user-selected): internal code structure, handler logic, error handling, full file mapping, test coverage.

**If monolith or single app with many modules:**
> "This is a large project with [N] components. I found: [list them].
> Which ones should I focus on? I recommend starting with [top 3–4 by importance],
> and I can document the rest in a follow-up pass."

Wait for user to confirm scope before continuing.

#### Infrastructure-as-Architecture (Microservices only)

Before scanning individual services, read the infrastructure layer — it IS the architecture map:

```bash
# Docker compose — shows service dependencies, ports, networks
cat docker-compose*.yml 2>/dev/null

# Kubernetes — shows deployments, services, ingress
find . -path "*/k8s/*" -o -path "*/helm/*" -o -path "*/kubernetes/*" | head -30

# API gateway config
find . -name "nginx.conf" -o -name "kong.yml" -o -name "traefik.*" -o -name "envoy.*" | head -10

# Message broker config
find . -name "*.proto" -o -name "asyncapi.*" -o -name "*.avsc" | head -20
```

From this, build an initial **service topology** before looking at any service code:
- Which services exist and their ports
- Which services depend on which (links, depends_on, network policies)
- What shared infrastructure exists (databases, message brokers, caches, object storage)
- What the external entry points are (API gateway, load balancer, CDN)

Present this topology to the user for confirmation before deep-scanning individual services.

### Step 2b: Per-Component Analysis

For each component **in scope**, analyze:

**Tech stack** — Read dependency/config files:
- package.json, tsconfig.json (Node/TS)
- go.mod, go.sum (Go)
- requirements.txt, pyproject.toml, setup.py (Python)
- Cargo.toml (Rust)
- pubspec.yaml (Flutter/Dart)

If none of the above exist, check for other indicators (Gemfile, pom.xml, build.gradle, mix.exs, etc.) and adapt accordingly. Don't assume a fixed set of languages.

**Entry points** — Find main files:
- Look for `main.*`, `index.*`, `app.*`, `server.*` in src/ or root
- Check package.json `main`/`bin` fields, or `[tool.poetry.scripts]`, etc.

**Routes/Screens** — Discover user-facing paths:
- Web: Grep for route definitions in the framework's style (React Router, Next.js pages/app dir, Express `app.get`, etc.)
- Mobile: Look for screen/navigation definitions

**API endpoints** — Find all route/handler definitions:
- REST: Grep for HTTP method decorators/calls (`@Get`, `@Post`, `app.get(`, `router.`, etc.)
- GraphQL: Look for schema files, resolver definitions
- tRPC: Look for router definitions
- If no patterns match, read the main entry point and trace outward

**Data models** — Find schemas and types:
- Database migrations: `migrations/`, `db/migrate/`, `alembic/`
- ORM models: Look for model/entity definition patterns in the detected framework
- TypeScript types/interfaces: key type definition files
- Prisma schema, GraphQL type definitions, protobuf files

**Environment variables** — Find config:
- `.env.example`, `.env.sample`, `.env.template`
- Docker compose files for service-level env vars
- Config files that reference `process.env`, `os.environ`, `os.Getenv`, etc.

**Build/run/test commands** — Find all dev commands:
- package.json scripts section
- Makefile, Taskfile.yml, Justfile
- Docker and docker-compose files
- CI/CD configs (.github/workflows/, .gitlab-ci.yml, etc.)

#### Additional Fields for Microservices

If the project was classified as microservices, also capture for EACH service:

**Service identity:**
- Service name (as defined in docker-compose, k8s manifests, or code)
- Port(s) it listens on
- Whether it's user-facing (external) or internal-only

**Data ownership:**
- Which database(s) does this service own?
- Does it have its own DB, or share with another service?
- What are the primary tables/collections it manages?

**Events & messages (produced and consumed):**
- Message queue topics/channels this service publishes to
- Topics/channels it subscribes to / consumes from
- Look for: RabbitMQ channel/queue definitions, Kafka topic configs, Redis pub/sub, AWS SQS/SNS, NATS subjects, event emitter patterns
- Grep for: `publish(`, `emit(`, `produce(`, `subscribe(`, `consume(`, `on(`, queue/topic name strings in config files

**Synchronous service-to-service calls:**
- gRPC client stubs and proto imports
- HTTP calls to other internal services (look for internal base URLs, service discovery patterns, or hardcoded `localhost:<port>` in dev configs)
- Look in docker-compose for `depends_on` to find call direction

**Service contracts:**
- Proto files (`.proto`) — who defines them, who consumes them
- OpenAPI/Swagger specs generated or consumed by this service
- AsyncAPI specs for event contracts
- Shared type packages imported by this service

### Step 2c: Cross-Component Mapping

Discover how components connect:
- **Frontend-to-backend calls**: Grep for fetch/axios/ky base URLs, API client configs, tRPC client setup, GraphQL client setup
- **Shared types/contracts**: packages shared between components, proto files, OpenAPI generated clients
- **Auth flow**: How authentication works across frontend and backend (JWT, sessions, OAuth providers)
- **Infrastructure**: Docker compose service dependencies, API gateway configs

#### Additional mapping for microservices:

**Service dependency graph** — Build a complete picture of which service calls which:

| Source Service | Target Service | Protocol | Purpose |
|---------------|---------------|----------|---------|
| api-gateway | user-service | REST | Auth, user lookup |
| user-service | notification-service | Kafka | Send welcome email on signup |
| billing-service | user-service | gRPC | Validate user plan |

To build this table:
1. Read each service's outbound client configs and env vars referencing other service URLs
2. Read message broker topic names — match publishers to consumers across services
3. Read proto/OpenAPI imports across services
4. Cross-reference with docker-compose `depends_on` and kubernetes service definitions

**Data ownership map** — Which service owns which data:

| Data Entity | Owner Service | Shared With | Access Method |
|------------|--------------|-------------|---------------|
| User | user-service | all services | REST API / JWT claims |
| Invoice | billing-service | admin-dashboard | REST API |

**Async flow chains** — For event-driven patterns, trace the full chain:
> Example: User signs up → user-service publishes `user.created` → notification-service sends welcome email → billing-service creates free trial

Document every async chain by matching published topics to consumed topics across services. These are invisible in HTTP-only tracing and often the most poorly documented part of any system.

---

## Phase 3: User Flow Discovery (Interactive)

### Step 3a: Present & Identify Flows

Present a structured summary of what you discovered in Phase 2:
- List all detected routes/screens/pages
- List all detected API endpoints grouped by resource
- List detected data models

Then propose flows you inferred from code:
> "Based on what I found, I think the main user flows are:
> 1. User signup/onboarding
> 2. Create a project
> 3. Invite a teammate
> 4. ...
>
> **Add, remove, or reorder these, then I'll document each one.**"

The user confirms the list in one pass.

### Step 3b: Flow Deep-Dive

For each confirmed flow, generate documentation from code analysis first. Then present your draft and ask:
- "Is this accurate? What am I missing?"
- "What error states or edge cases exist?"
- "Are there different user roles that experience this differently?"

For each flow, also:
- Map the user's description to the routes/endpoints discovered in Phase 2
- Identify the API calls triggered at each step
- Note any gaps between code and user description (ask about them)

#### Multi-Service Flow Tracing (microservices only)

For each step in a flow, trace the full service chain:

1. **Entry point**: Which service receives the initial request? (usually gateway or BFF)
2. **Synchronous chain**: Does that service call others? Map: Service A → Service B → Service C.
3. **Async side-effects**: After the synchronous response, what events get published? Which services consume them?
4. **Data writes**: Which service writes to which database at each step?
5. **Failure modes**: What happens if a mid-chain service is down? Retry logic, DLQ, saga/compensation?

Also ask: "After [step], does anything happen in the background that the user doesn't see? (e.g., emails sent, records synced, jobs queued)"

Confirm traced chains with the user — async flows are the hardest to discover from code alone.

### Step 3c: Generate User Stories

For each flow, generate user stories:
> As a [user type], I want to [action] so that [benefit].

Present all stories for validation.

### Step 3d: Check for More

Ask: "Are there other flows I should document? If not, I'll confirm the architecture and start generating the wiki."

---

## Phase 4: Architecture Checkpoint (BEFORE writing files)

> Before generating any files, present a brief architecture summary to the user:

> "Here's the architecture I'm about to document:
> - **Architecture type**: [single app / microservices / monorepo / etc.]
> - **Components**: [list]
> - **Communication**: [how they connect]
> - **Auth**: [method]
> - **Key data models**: [list]
>
> Does this look right? Any corrections before I generate the wiki?"

**For microservices, also present:**

> **Service dependency summary:**
> | Service | Calls (sync) | Publishes events | Consumes events | Owns DB |
> |---------|-------------|-----------------|----------------|---------|
> | api-gateway | user-svc, payment-svc | — | — | No |
> | user-svc | — | user.created | — | users-db |
> | payment-svc | user-svc | payment.completed | — | payments-db |
> | notification-svc | — | — | user.created, payment.completed | No |
>
> "Does this service map look right? Are there connections I'm missing?"

Wait for confirmation. This prevents errors from propagating across all output files.

---

## Phase 5: Knowledge Base Generation

### Directory Structure

```
codewiki/
├── overview.md
├── architecture.md
├── service-map.md          (microservices only)
├── events.md               (microservices only)
├── user-flows/
│   ├── index.md
│   └── <flow-name>.md    (one per flow)
├── api-reference.md
├── data-models.md
├── frontend-map.md        (skip if no frontend)
├── mobile-map.md          (skip if no mobile app)
├── commands.md
├── env-vars.md
└── glossary.md
```

### Generation Process

For each file:
1. Read the corresponding template from this skill's `templates/` directory
2. Read the relevant `codewiki/_scratch/` files for source data
3. Fill in the template with findings
4. Write to `codewiki/`

Read templates one at a time — do not load all templates simultaneously.

**Glossary detection:** Scan READMEs, doc comments, and UI strings for capitalized multi-word terms that appear to be domain concepts. Also check for existing glossary/terminology sections. Focus on product-specific terms only — not general programming terms.

**Important:** Only generate files that are relevant. Skip `service-map.md` and `events.md` for single apps. Skip `mobile-map.md` if no mobile app. Skip `frontend-map.md` if no frontend.

After all files are generated:
```bash
rm -rf codewiki/_scratch/
```

---

## Phase 6: CLAUDE.md Generation

Check if `CLAUDE.md` exists in the project root.

### If CLAUDE.md does NOT exist:

Read the template from `templates/claude-md.md` and generate. Remove links for any files that were skipped (e.g., mobile-map.md if no mobile app).

### If CLAUDE.md ALREADY exists:

Ask the user:
> "CLAUDE.md already exists. Would you like me to:
> 1. **Fresh scan** — back up the existing file and replace it entirely
> 2. **Rescan & merge** — preserve your manual additions and merge in new findings"

- **Fresh**: Copy existing to `CLAUDE.md.bak`, then generate new.
- **Merge**: Read existing CLAUDE.md, identify sections that are manually written (not matching codewiki template), preserve those, and update/add generated sections around them. Show the user a diff summary of what changed.

---

## Phase 7: Git & Repository Setup

> Always run this phase — do not skip.

### Step 7a: Clean Up Scratch Files

```bash
rm -rf codewiki/_scratch/
```

### Step 7b: Ask User for Repo Preferences

Ask all in a single message:

> "The knowledge base is ready. Let me set up the repo:
>
> 1. **Where should the wiki live?**
>    - a) Inside this project repo (add `codewiki/` folder here)
>    - b) Its own dedicated repo (I'll create a new folder next to this project)
>
> 2. **Want me to create a GitHub repo for it?**
>    - If yes: What should the repo be named? (default: `<product-name>-codewiki`)
>    - Should it be **public** or **private**?
>    - Which GitHub org/account? (default: your personal account)
>
> 3. **Any custom repo description?** (default: 'Product knowledge base for <Product Name>')"

### Step 7c: Commit Locally

**Option A — Inside project repo:**
```bash
git add codewiki/ CLAUDE.md
git commit -m "docs: add codewiki product knowledge base

Generated by CodeWiki. Contains:
- Product overview and architecture docs
- User flow documentation
- API reference and data models
- Service map and environment variable reference"
```

**Option B — Dedicated repo:**
```bash
mkdir -p ../<repo-name>
cp -r codewiki/ ../<repo-name>/codewiki/
cp CLAUDE.md ../<repo-name>/

cd ../<repo-name>
git init
git add -A
git commit -m "Initial codewiki generation"
```

For Option B, also generate `README.md` using the template from `templates/readme.md`. Only include rows/sections for files that were actually generated.

### Step 7d: Create Remote GitHub Repo (if user opted in)

Check if `gh` CLI is available and authenticated:
```bash
gh auth status 2>/dev/null
```

**If `gh` is available and authenticated:**
```bash
cd ../<repo-name>
gh repo create <org-or-user>/<repo-name> \
  --description "<repo description>" \
  --<public|private> \
  --source . \
  --push
```

**If `gh` is not available:**
Tell the user:
> "I can't create the GitHub repo automatically because the `gh` CLI isn't
> installed or authenticated. Here's what to do:
>
> 1. Go to https://github.com/new
> 2. Create a repo named `<repo-name>` (<public/private>)
> 3. Then run:
> ```bash
> cd ../<repo-name>
> git remote add origin git@github.com:<org>/<repo-name>.git
> git push -u origin main
> ```"

### Step 7e: Final Summary

Present to the user:

> **CodeWiki generation complete!**
>
> **Files created:**
> <list all files in codewiki/>
>
> **CLAUDE.md:** <created new / merged / replaced>
>
> **Repo:** <committed to project repo / created at ../<repo-name>/>
> <if GitHub: "Pushed to https://github.com/<org>/<repo-name>">
>
> **Repos scanned:**
> | Repo | Endpoints | Models | Events | Scan depth |
> |------|-----------|--------|--------|------------|
> | backend | 14 | 5 | 3 | deep |
> | frontend | 12 routes | — | — | deep |
> | comms-service | 4 | 2 | 6 | lightweight |
>
> **Next steps:**
> - Share the repo URL with your team
> - Copy `CLAUDE.md` into whichever repo you're working in for Claude Code context
> - Run CodeWiki again anytime to update — I'll detect existing files and offer to merge

---

## Behavioral Guidelines

- Be thorough in scanning but batch related questions. Don't overwhelm with one question per message.
- When scanning code, read actual file contents — don't just list filenames. Understand what the code does.
- Use Task subagents to parallelize scanning when possible (e.g., scan frontend and backend simultaneously) — but only if context window allows. For multi-repo, sequential is safer.
- If you encounter very large files (>1000 lines), read strategically — focus on exports, route definitions, model definitions, and config sections.
- Keep generated documentation concise and scannable. Use tables where appropriate. Avoid walls of text.
- Use relative paths in all documentation so it works regardless of where the repo is cloned.
- If the user interrupts or wants to skip a phase, accommodate gracefully — but always note what was skipped so they can come back to it.
- For microservices: prioritize understanding contracts (protos, event schemas, API specs) over internal implementation. When tracing flows, always confirm async chains with the user.
