---
name: analyze-architecture
description: Comprehensive brownfield architecture analysis for existing codebases. Discovers structure, identifies patterns, assesses quality, calculates production readiness, and provides actionable recommendations. Use when analyzing existing codebases to understand architecture, assess quality, or prepare for modernization.
acceptance:
  - codebase_structure_analyzed: "Codebase structure discovered and documented"
  - project_type_detected: "Project type identified (frontend/backend/fullstack/monorepo)"
  - architecture_patterns_identified: "Architectural patterns recognized and documented"
  - tech_stack_documented: "Technology stack analyzed with versions"
  - quality_scores_calculated: "Quality scores computed across 8 dimensions"
  - production_readiness_scored: "Production readiness score calculated (0-100)"
  - recommendations_provided: "Actionable recommendations prioritized by impact"
  - report_generated: "Comprehensive analysis report generated"
inputs:
  codebase_path:
    type: string
    required: false
    description: "Path to codebase root (default: current directory)"
  output_format:
    type: string
    required: false
    description: "markdown | json | both (default: markdown)"
  focus_area:
    type: string
    required: false
    description: "architecture | security | performance | scalability | tech-debt | all (default: all)"
  depth:
    type: string
    required: false
    description: "quick | standard | comprehensive (default: standard)"
  token_budget:
    type: number
    required: false
    description: "Maximum tokens to use (default: 100000)"
outputs:
  report_file:
    type: string
    description: "Path to generated analysis report"
  project_type:
    type: string
    description: "Detected project type"
  architecture_patterns:
    type: array
    description: "List of identified architectural patterns"
  production_readiness_score:
    type: number
    description: "Overall production readiness score (0-100)"
  quality_scores:
    type: object
    description: "Quality scores per dimension"
  tech_debt_items:
    type: array
    description: "Identified technical debt items"
  recommendations:
    type: array
    description: "Prioritized recommendations"
telemetry:
  emit: "skill.analyze-architecture.completed"
  track:
    - project_type
    - architecture_patterns
    - production_readiness_score
    - tech_debt_count
    - recommendations_count
    - duration_ms
    - focus_area
---

# Analyze Architecture (Brownfield)

## Purpose

Perform comprehensive, production-ready architecture analysis of existing codebases. Designed for brownfield projects where formal architecture documentation may not exist. Discovers structure, identifies patterns, assesses quality across 8 dimensions, and provides actionable recommendations.

**Core Principles:**
- **Discovery-first:** Understand what exists before judging
- **Pattern recognition:** Identify architectural patterns in use
- **Multi-dimensional:** Quality assessment across 8 key areas
- **Actionable insights:** Prioritized recommendations with effort estimates
- **Production focus:** Calculate readiness for production deployment
- **Brownfield-optimized:** Works without existing documentation

---

## Prerequisites

- Codebase accessible on filesystem
- Read access to all source files
- Build configuration files present (package.json, etc.)
- Database schema files accessible (if applicable)

---

## Workflow Modes

Choose the analysis depth based on time constraints and requirements:

### Quick Mode (`--depth quick`)
**Duration:** 5-7 minutes
**Token Usage:** ~50,000 tokens
**Steps:** 1-8 only
**Output:** Executive summary + key metrics

**Best For:**
- Initial assessments
- Time-sensitive decisions
- High-level overviews
- Quick health checks

**Steps Included:**
1. Discover Codebase Structure
2. Detect Project Type
3. Analyze Technology Stack
4. Identify Architectural Patterns
5. Calculate Quality Scores (simplified)
6. Identify Critical Technical Debt
7. Generate Quick Report
8. Emit Telemetry

---

### Standard Mode (`--depth standard`) [DEFAULT]
**Duration:** 10-12 minutes
**Token Usage:** ~80,000 tokens
**Steps:** 1-12
**Output:** Comprehensive analysis without deep-dives

**Best For:**
- Regular assessments
- Pre-production reviews
- Architecture validation
- Team presentations

**Steps Included:**
1-11 from full workflow (excludes integration analysis, deep testing review, and extended report sections)

---

### Comprehensive Mode (`--depth comprehensive`)
**Duration:** 15-20 minutes
**Token Usage:** ~120,000 tokens
**Steps:** All 15 steps
**Output:** Complete analysis with all sections

**Best For:**
- Production readiness assessments
- Architecture audits
- Documentation creation
- Detailed planning

**Steps Included:**
All 15 steps with deep analysis, complete recommendations, risk assessment, and extended report

---

## Adaptive Workflow

The skill automatically adapts based on available information:

**Early Exit Conditions:**
- If `docs/architecture.md` exists and is recent (<30 days): Reference existing documentation, skip redundant discovery
- If all package.json files parsed successfully: Skip manual tech stack discovery
- If documentation is comprehensive: Validate metrics instead of rediscovering

**Token Budget Management:**
- Track token usage per step
- Warn at 80% of budget
- Switch to quick mode if budget exceeded
- Prioritize critical findings if limited budget

---

## Workflow

### 1. Discover Codebase Structure

**Action:** Analyze directory structure and identify key components

**Early Exit Condition:**
If `docs/architecture.md` or `docs/ARCHITECTURE.md` exists and is recent (<30 days):
- Read existing architecture documentation
- Extract project structure from docs
- Validate structure still matches (quick check)
- Skip to Step 4 (Architectural Patterns)

**Execute:**
```bash
# Check for existing architecture docs
find {codebase_path}/docs -name "*architecture*.md" -mtime -30 2>/dev/null

# If no recent docs, discover structure
# Find all major directories and files
find {codebase_path} -maxdepth 3 -type d | head -50
find {codebase_path} -name "package.json" -o -name "*.config.*" -o -name "tsconfig.json"
```

**Identify:**
- **Monorepo detection:** Multiple package.json files, workspaces config
- **Package structure:** packages/, apps/, libs/, src/ directories
- **Configuration files:** tsconfig.json, .eslintrc, vite.config.ts, etc.
- **Documentation:** README.md, docs/ folder, ARCHITECTURE.md
- **Build artifacts:** dist/, build/, node_modules/

**Classification:**
- **Monorepo:** Multiple packages with shared configuration
- **Standalone:** Single package with unified source
- **Microservices:** Multiple independent services
- **Modular monolith:** Single codebase with clear module boundaries

**See:** `references/codebase-discovery-guide.md` for detection heuristics

---

### 2. Detect Project Type

**Action:** Determine primary domain (frontend, backend, fullstack, monorepo)

**Frontend indicators:**
- React, Vue, Angular, Svelte dependencies
- Component directories (components/, pages/, views/)
- State management (Redux, Zustand, Pinia)
- UI libraries (Material-UI, TailwindCSS, shadcn)
- Build tools (Vite, Webpack, Next.js)

**Backend indicators:**
- Express, Fastify, NestJS, Koa dependencies
- API routes (routes/, controllers/, endpoints/)
- Database ORM (Prisma, TypeORM, Sequelize)
- Service layers (services/, handlers/, use-cases/)
- Middleware (auth, validation, error handling)

**Fullstack indicators:**
- Next.js, Remix, SvelteKit, Nuxt
- Both frontend and backend patterns present
- API routes within same codebase
- Shared types between client/server

**Monorepo indicators:**
- Workspaces in package.json (npm, yarn, pnpm)
- Turborepo, Nx, Lerna configuration
- Multiple packages with dependencies
- Shared libraries and utilities

**Output:** `project_type` = frontend | backend | fullstack | monorepo

---

### 3. Analyze Technology Stack

**Action:** Extract and document all technologies with versions

**Early Exit Condition:**
If all package.json files found and successfully parsed:
- Extract dependencies and devDependencies
- Parse versions directly from package.json
- Skip manual grep-based discovery
- Proceed to Step 4

**Execute:**
```bash
# Read all package.json files
find {codebase_path} -name "package.json" -not -path "*/node_modules/*" -exec cat {} \;

# Extract tech stack using primitive (preferred)
python .claude/skills/bmad-commands/scripts/extract_tech_stack.py \
  --codebase {codebase_path} \
  --output json

# Read Prisma schema if exists
find {codebase_path} -name "schema.prisma" -exec cat {} \;
```

**Extract:**

**Backend Stack:**
- Runtime (Node.js version from .nvmrc or package.json)
- Framework (Express, NestJS, Fastify, etc.)
- ORM/Database (Prisma, TypeORM, Mongoose, etc.)
- Caching (Redis, Memcached)
- Job queues (Bull, Inngest, Agenda)
- Auth (Passport, JWT, Clerk, Auth0)
- Validation (Zod, Joi, Yup)
- Testing (Jest, Vitest, Mocha)

**Frontend Stack:**
- Framework (React, Vue, Angular, Svelte)
- UI Library (Material-UI, Ant Design, Chakra)
- State Management (Redux, Zustand, Recoil, Context)
- Data Fetching (React Query, SWR, Apollo)
- Routing (React Router, Vue Router)
- Styling (CSS-in-JS, Tailwind, CSS Modules)
- Build Tool (Vite, Webpack, Rollup)
- Testing (Vitest, Jest, Playwright, Cypress)

**Database & Infrastructure:**
- Database (PostgreSQL, MongoDB, MySQL, etc.)
- Caching layer (Redis, Memcached)
- Search (Elasticsearch, Algolia)
- File storage (S3, Cloudinary, Supabase)
- Real-time (WebSocket, SSE, Socket.io)

**DevOps & Tools:**
- Package manager (npm, yarn, pnpm)
- Monorepo tool (Turborepo, Nx, Lerna)
- CI/CD (GitHub Actions, CircleCI, etc.)
- Linting (ESLint, Prettier)
- Type checking (TypeScript)

**Output:** Complete technology inventory with versions

**See:** `references/tech-stack-catalog.md` for common patterns

---

### 4. Identify Architectural Patterns

**Action:** Recognize and document architectural patterns in use

**Search for pattern indicators:**

**Domain-Driven Design (DDD):**
```bash
# Look for DDD structure
grep -r "domain/entities" {codebase_path}/src
grep -r "domain/value-objects" {codebase_path}/src
grep -r "AggregateRoot" {codebase_path}/src
grep -r "DomainEvent" {codebase_path}/src
```

**CQRS (Command Query Responsibility Segregation):**
```bash
# Use metric validation primitive for accuracy (RECOMMENDED)
python .claude/skills/bmad-commands/scripts/validate_metrics.py \
  --codebase {codebase_path}/src \
  --metric cqrs \
  --output json

# Alternative: Manual discovery (less accurate)
# grep -r "CommandHandler" {codebase_path}/src
# grep -r "QueryHandler" {codebase_path}/src
# find {codebase_path}/src -path "*/commands/*" -o -path "*/queries/*"
```

**Expected Output:**
```json
{
  "command_files": 92,
  "query_files": 119,
  "command_handlers": 65,
  "query_handlers": 87,
  "total_handlers": 152,
  "total_files": 211
}
```

**Layered Architecture:**
```bash
# Look for layers
find {codebase_path}/src -type d -name "presentation" -o -name "application" -o -name "domain" -o -name "infrastructure"
find {codebase_path}/src -type d -name "controllers" -o -name "services" -o -name "repositories"
```

**Microservices:**
```bash
# Look for service boundaries
find {codebase_path} -name "docker-compose.yml" -o -name "Dockerfile"
find {codebase_path}/services -type d -maxdepth 1
```

**Event-Driven:**
```bash
# Look for event patterns
grep -r "EventEmitter" {codebase_path}/src
grep -r "EventBus" {codebase_path}/src
find {codebase_path}/src -path "*/events/*"
```

**Hexagonal/Ports & Adapters:**
```bash
# Look for ports and adapters
find {codebase_path}/src -path "*/ports/*" -o -path "*/adapters/*"
grep -r "interface.*Port" {codebase_path}/src
```

**Repository Pattern:**
```bash
# Look for repositories
find {codebase_path}/src -path "*/repositories/*"
grep -r "Repository" {codebase_path}/src | grep -E "(class|interface)"
```

**Output:** Array of identified patterns with evidence

**Pattern Confidence Scoring:**
- Strong evidence: 5+ files matching pattern
- Moderate evidence: 3-4 files matching pattern
- Weak evidence: 1-2 files matching pattern

**See:** `references/architectural-patterns-catalog.md` for complete list

---

### 5. Evaluate Domain Model (if DDD/CQRS)

**Action:** Analyze domain entities, services, and events

**Discover Entities:**
```bash
# Find entity files
find {codebase_path}/src -path "*/domain/entities/*" -o -path "*/entities/*"
grep -r "class.*Entity" {codebase_path}/src
```

**Discover Value Objects:**
```bash
# Find value objects
find {codebase_path}/src -path "*/domain/value-objects/*" -o -path "*/value-objects/*"
```

**Discover Aggregates:**
```bash
# Find aggregate roots
grep -r "AggregateRoot" {codebase_path}/src
```

**Discover Domain Events:**
```bash
# Find domain events
find {codebase_path}/src -path "*/domain/events/*" -o -path "*/events/*"
grep -r "DomainEvent" {codebase_path}/src
```

**Discover Application Services:**
```bash
# Find services
find {codebase_path}/src -path "*/application/services/*" -o -path "*/services/*"
grep -r "class.*Service" {codebase_path}/src | head -20
```

**Discover Command/Query Handlers:**
```bash
# Find CQRS handlers
find {codebase_path}/src -path "*/handlers/commands/*" -o -path "*/handlers/queries/*"
grep -r "CommandHandler\|QueryHandler" {codebase_path}/src | wc -l
```

**Output:**
- Entity count and list
- Value object count
- Aggregate roots identified
- Domain events count
- Service count
- Command handler count
- Query handler count

**Domain Model Quality Indicators:**
- **Excellent:** Clear separation, proper aggregates, rich domain logic
- **Good:** Entities present, some business logic in domain
- **Fair:** Anemic domain model, logic in services
- **Poor:** No domain layer, data structures only

---

### 6. Assess API Architecture

**Action:** Analyze API design, endpoints, and middleware

**Discover API Endpoints:**
```bash
# Find route definitions
find {codebase_path}/src -path "*/routes/*" -o -path "*/controllers/*"
grep -r "router\." {codebase_path}/src | grep -E "(get|post|put|patch|delete)" | wc -l
```

**Identify API Style:**
- **REST:** router.get(), router.post(), /api/v1/ patterns
- **GraphQL:** schema definitions, resolvers, apollo-server
- **tRPC:** .query(), .mutation(), typed procedures
- **gRPC:** .proto files, protobuf definitions

**Discover Middleware:**
```bash
# Find middleware
find {codebase_path}/src -path "*/middleware/*"
grep -r "app.use\|router.use" {codebase_path}/src
```

**Common Middleware to Check:**
- Authentication (JWT verification, OAuth)
- Authorization (RBAC, permissions)
- Validation (request body/params validation)
- Error handling (global error handler)
- Rate limiting (DDoS protection)
- Request logging (audit trail)
- CORS (cross-origin handling)

**API Versioning:**
```bash
# Check for versioning
grep -r "/api/v[0-9]" {codebase_path}/src
```

**Output:**
- API style (REST, GraphQL, tRPC, gRPC)
- Endpoint count
- Middleware stack
- Versioning strategy
- Authentication method
- Authorization approach

**API Quality Indicators:**
- **Excellent:** Versioned, validated, authenticated, documented
- **Good:** Proper middleware, error handling, basic validation
- **Fair:** Basic routes, some middleware missing
- **Poor:** No middleware, no validation, security gaps

---

### 7. Review Data Architecture

**Action:** Analyze database schema, caching, and real-time infrastructure

**Analyze Database Schema:**
```bash
# Find Prisma schema
find {codebase_path} -name "schema.prisma" -exec wc -l {} \;
find {codebase_path} -name "schema.prisma" -exec grep -E "model |enum " {} \; | wc -l

# Find migrations
find {codebase_path} -path "*/prisma/migrations/*" -name "migration.sql" | wc -l
```

**Extract from Schema:**
- Model count (database tables)
- Enum count (type enums)
- Relationship patterns (one-to-many, many-to-many)
- Index count (performance indexes)
- Multi-tenancy patterns (tenantId fields)

**Check Caching Strategy:**
```bash
# Look for caching
grep -r "redis\|cache\|memcache" {codebase_path}/src --include="*.ts" | wc -l
find {codebase_path}/src -path "*/cache/*"
```

**Identify Real-time Architecture:**
```bash
# Look for real-time
grep -r "WebSocket\|SSE\|socket.io\|EventSource" {codebase_path}/src
find {codebase_path}/src -path "*/realtime/*"
```

**Output:**
- Database type (PostgreSQL, MongoDB, etc.)
- Model count
- Index optimization level
- Multi-tenant design (yes/no)
- Caching strategy (Redis, in-memory, none)
- Real-time approach (WebSocket, SSE, polling, none)

**Data Architecture Quality Indicators:**
- **Excellent:** Optimized indexes, caching, multi-tenant, real-time
- **Good:** Proper schema, some indexes, basic caching
- **Fair:** Basic schema, missing indexes, no caching
- **Poor:** Unoptimized schema, no indexes, performance issues

---

### 8. Analyze Security Posture

**Action:** Assess authentication, authorization, and security measures

**Authentication Analysis:**
```bash
# Find auth implementation
grep -r "passport\|jwt\|clerk\|auth0\|supabase" {codebase_path}/src
find {codebase_path}/src -path "*/auth/*"
```

**Authorization Analysis:**
```bash
# Find authorization logic
grep -r "RBAC\|permissions\|roles\|authorize" {codebase_path}/src
grep -r "canAccess\|hasPermission\|checkRole" {codebase_path}/src
```

**Security Measures Check:**
```bash
# Check for security practices
grep -r "helmet\|cors\|csurf\|express-rate-limit" {codebase_path}/src
grep -r "bcrypt\|argon2\|scrypt" {codebase_path}/src
grep -r "sanitize\|escape\|validator" {codebase_path}/src
```

**Secrets Management:**
```bash
# Check for environment variables and secrets
find {codebase_path} -name ".env*" | wc -l
grep -r "process.env" {codebase_path}/src | wc -l
grep -r "AWS_SECRET\|API_KEY\|PASSWORD" {codebase_path}/src
```

**SQL Injection Protection:**
- Prisma (parameterized queries) = Protected
- Raw SQL queries = Vulnerable
- Input validation with Zod/Joi = Protected

**XSS Protection:**
- React (JSX escaping) = Protected
- Helmet CSP headers = Protected
- User input sanitization = Protected

**Output:**
- Authentication method (JWT, OAuth, Clerk, etc.)
- Authorization approach (RBAC, ABAC, etc.)
- Security headers (Helmet, CORS, CSP)
- Password hashing (bcrypt, argon2)
- Input validation (Zod, Joi, Yup)
- SQL injection protection (ORM usage)
- XSS protection (React, sanitization)
- Secrets management (env vars, vault)

**Security Score Calculation:**
- Auth present: 20 points
- Authorization (RBAC): 15 points
- Security headers: 15 points
- Password hashing: 10 points
- Input validation: 15 points
- SQL injection protected: 10 points
- XSS protection: 10 points
- Secrets properly managed: 5 points
- **Total:** 0-100

---

### 9. Evaluate Performance Characteristics

**Action:** Identify bottlenecks and optimization opportunities

**Database Performance:**
```bash
# Check for indexes
grep -r "@@index\|@@id\|@@unique" {codebase_path}/prisma/schema.prisma | wc -l

# Look for N+1 query patterns
grep -r "findMany\|findFirst" {codebase_path}/src | wc -l
grep -r "include:\|select:" {codebase_path}/src | wc -l
```

**Caching Strategy:**
```bash
# Check caching implementation
grep -r "redis.get\|cache.get" {codebase_path}/src | wc -l
grep -r "redis.set\|cache.set" {codebase_path}/src | wc -l
```

**Frontend Performance:**
```bash
# Check for code splitting
grep -r "React.lazy\|lazy(" {codebase_path}/src
grep -r "dynamic(.*import" {codebase_path}/src

# Check for memoization
grep -r "useMemo\|useCallback\|React.memo" {codebase_path}/src | wc -l
```

**Query Optimization:**
- Proper indexes present: +20 points
- Connection pooling configured: +10 points
- Caching implemented: +20 points
- Code splitting: +10 points
- Memoization used: +10 points

**Output:**
- Database index count
- Caching strategy (Redis, in-memory, none)
- Code splitting (yes/no)
- Memoization usage (high, medium, low)
- Query optimization level (excellent, good, fair, poor)
- Performance score (0-100)

**Performance Quality Indicators:**
- **Excellent (80-100):** Optimized indexes, caching, code splitting, memoization
- **Good (60-79):** Some optimization, basic caching, indexes present
- **Fair (40-59):** Minimal optimization, missing key optimizations
- **Poor (0-39):** No optimization, performance bottlenecks likely

---

### 10. Assess Scalability

**Action:** Evaluate horizontal and vertical scaling capabilities

**Horizontal Scaling Readiness:**
- Stateless API design: +30 points
- Distributed caching (Redis): +20 points
- Database connection pooling: +15 points
- Load balancer ready: +10 points
- Background job processing: +15 points
- No server-side sessions: +10 points

**Vertical Scaling Concerns:**
- Single database instance: -20 points
- No read replicas: -15 points
- Synchronous processing: -10 points
- No queue system: -15 points

**Scalability Checks:**
```bash
# Check for stateless design
grep -r "session\|cookie-session" {codebase_path}/src

# Check for background jobs
grep -r "bull\|inngest\|agenda" {codebase_path}/src

# Check for distributed caching
grep -r "redis\|memcached" {codebase_path}/src
```

**Output:**
- Horizontal scaling readiness (0-100)
- Bottlenecks identified
- Scaling recommendations
- Current limitations

**Scalability Quality Indicators:**
- **Excellent (80-100):** Stateless, distributed cache, job queue, load balancer ready
- **Good (60-79):** Mostly stateless, basic caching, some async processing
- **Fair (40-59):** Some stateful components, limited caching
- **Poor (0-39):** Stateful design, no distributed components, single points of failure

---

### 11. Identify Technical Debt

**Action:** Find type errors, deprecated patterns, missing tests, documentation gaps

**Type Safety Analysis (TypeScript):**
```bash
# Run TypeScript compiler
npx tsc --noEmit 2>&1 | grep "error TS" | wc -l

# Count errors by type
npx tsc --noEmit 2>&1 | grep "error TS" | awk '{print $2}' | sort | uniq -c
```

**Deprecated Patterns:**
```bash
# Look for old patterns
grep -r "componentWillMount\|componentWillReceiveProps" {codebase_path}/src
grep -r "@ts-ignore\|@ts-expect-error" {codebase_path}/src | wc -l
grep -r "any" {codebase_path}/src | grep -v "node_modules" | wc -l
```

**Missing Tests:**
```bash
# Count test files
find {codebase_path}/src -name "*.test.*" -o -name "*.spec.*" | wc -l

# Count source files
find {codebase_path}/src -name "*.ts" -o -name "*.tsx" | grep -v ".test\|.spec" | wc -l

# Calculate rough coverage
# test_files / source_files * 100
```

**Documentation Gaps:**
```bash
# Check for documentation
find {codebase_path} -name "README.md" -o -name "*.md" | wc -l
find {codebase_path}/docs -name "*.md" 2>/dev/null | wc -l
```

**Output:**
- TypeScript error count
- Error breakdown by type
- Deprecated pattern count
- Test coverage estimate
- Documentation file count
- Technical debt priority list

**Technical Debt Scoring:**
- 0-100 errors: Low debt (90-100 points)
- 101-500 errors: Moderate debt (60-89 points)
- 501-1000 errors: High debt (30-59 points)
- 1000+ errors: Critical debt (0-29 points)

---

### 12. Review Testing Infrastructure

**Action:** Assess unit, integration, and E2E test coverage

**Unit Tests:**
```bash
# Find unit test files
find {codebase_path}/src -name "*.test.*" -o -name "*.spec.*" | wc -l
grep -r "describe\|it\|test(" {codebase_path}/src --include="*.test.*" | wc -l
```

**Integration Tests:**
```bash
# Look for integration test patterns
grep -r "supertest\|request(" {codebase_path}/src | wc -l
find {codebase_path} -path "*/tests/integration/*" -o -path "*/e2e/*"
```

**E2E Tests:**
```bash
# Check for E2E frameworks
find {codebase_path} -name "playwright.config.*" -o -name "cypress.config.*"
find {codebase_path} -path "*/e2e/*" -name "*.spec.*" | wc -l
```

**Test Coverage:**
```bash
# Check for coverage configuration
find {codebase_path} -name "vitest.config.*" -o -name "jest.config.*"
grep -r "coverage" {codebase_path}/package.json
```

**Output:**
- Unit test count
- Integration test count
- E2E test count
- Test framework (Vitest, Jest, Playwright, Cypress)
- Coverage tracking (yes/no)
- Testing score (0-100)

**Testing Quality Indicators:**
- **Excellent (85-100):** High coverage, all test types, automated CI
- **Good (70-84):** Unit + integration tests, some E2E, CI setup
- **Fair (50-69):** Basic unit tests, missing integration/E2E
- **Poor (0-49):** Minimal tests, no automation, no coverage tracking

---

### 13. Analyze External Integrations

**Action:** Identify third-party services and integration methods

**Search for Integration Patterns:**
```bash
# Look for API clients
grep -r "axios\|fetch\|got\|node-fetch" {codebase_path}/src
grep -r "prisma\|supabase\|firebase" {codebase_path}/src

# Look for SDKs
grep -r "@clerk\|@auth0\|stripe\|sendgrid\|twilio" {codebase_path}/package.json
```

**Common Integrations to Check:**
- **Authentication:** Clerk, Auth0, Firebase, Supabase
- **Payments:** Stripe, PayPal, Square
- **Email:** SendGrid, Mailgun, AWS SES
- **SMS:** Twilio, Vonage
- **Storage:** AWS S3, Cloudinary, Supabase Storage
- **Analytics:** Google Analytics, Mixpanel, Segment
- **Monitoring:** Sentry, Datadog, New Relic
- **AI:** OpenAI, Anthropic, Hugging Face
- **Search:** Algolia, Elasticsearch, Typesense
- **Database:** PostgreSQL, MongoDB, Redis

**Integration Method:**
- REST API
- SDK/Client Library
- Webhooks
- Event-driven
- Polling

**Output:**
- Service list with purpose
- Integration method per service
- SDK versions
- Webhook endpoints

---

### 14. Calculate Production Readiness Score

**Action:** Compute weighted score across all quality dimensions

**Quality Dimensions & Weights:**

| Dimension       | Weight | Score (0-100) |
|-----------------|--------|---------------|
| Architecture    | 20%    | Calculated    |
| Code Quality    | 15%    | Calculated    |
| Security        | 15%    | Calculated    |
| Performance     | 10%    | Calculated    |
| Scalability     | 10%    | Calculated    |
| Maintainability | 15%    | Calculated    |
| Testing         | 10%    | Calculated    |
| Monitoring      | 5%     | Calculated    |

**Formula:**
```
Production Readiness Score =
  (Architecture × 0.20) +
  (Code Quality × 0.15) +
  (Security × 0.15) +
  (Performance × 0.10) +
  (Scalability × 0.10) +
  (Maintainability × 0.15) +
  (Testing × 0.10) +
  (Monitoring × 0.05)
```

**Score Interpretation:**
- **90-100:** ⭐⭐⭐⭐⭐ Excellent - Production Ready
- **80-89:** ⭐⭐⭐⭐ Very Good - Minor improvements needed
- **70-79:** ⭐⭐⭐⭐ Good - Moderate improvements needed
- **60-69:** ⭐⭐⭐ Fair - Significant work required
- **50-59:** ⭐⭐ Poor - Major rework needed
- **0-49:** ⭐ Critical - Not production ready

**Output:** Overall production readiness score with breakdown

---

### 15. Generate Comprehensive Analysis Report

**Action:** Create detailed markdown report with all findings

**Report Structure:**

```markdown
# {Project Name} - Architecture Analysis Report

## Executive Summary
- Project overview
- Overall assessment
- Production readiness score
- Key verdict

## 1. Architecture Overview
- Project structure
- Architecture pattern
- Key characteristics

## 2. Technology Stack
- Backend stack (with versions)
- Frontend stack (with versions)
- Database & infrastructure

## 3. Domain Model Analysis (if applicable)
- Domain entities
- Value objects
- Aggregates
- Domain events
- Application services
- CQRS handlers

## 4. CQRS Implementation (if applicable)
- Command side
- Query side
- Application services

## 5. Infrastructure Layer Analysis
- Database (schema stats)
- Real-time infrastructure
- Caching strategy
- Queue system

## 6. API Architecture
- REST API structure
- Middleware stack
- API versioning

## 7. Multi-Tenant Architecture (if applicable)
- Tenant isolation strategy
- Data isolation
- Security enforcement

## 8. Quality Assessment
- 8.1 Architecture Quality (score/100)
- 8.2 Code Quality (score/100)
- 8.3 Security (score/100)
- 8.4 Performance (score/100)
- 8.5 Scalability (score/100)
- 8.6 Maintainability (score/100)
- 8.7 Testing (score/100)
- 8.8 Monitoring (score/100)

## 9. Technical Debt Analysis
- Current technical debt items
- Priority breakdown (high/medium/low)
- Effort estimates

## 10. External Integrations
- Integration points table
- Integration methods

## 11. Key Recommendations
- 🔴 HIGH PRIORITY (with effort estimates)
- 🟡 MEDIUM PRIORITY (with effort estimates)
- 🟢 LOW PRIORITY (with effort estimates)

## 12. Risk Assessment
- Technical risks table
- Operational risks table

## 13. Production Readiness Checklist
- ✅ Already Complete (%)
- 🔧 Needs Completion (%)

## 14. Final Verdict
- Overall Score: X/100 ⭐⭐⭐⭐
- Category Breakdown (table)
- Success Probability

## 15. Conclusion
- Key achievements
- Critical path to production
- Bottom line recommendation
```

**Output Formats:**

**Markdown (Default):**
- Save to `docs/architecture-analysis-{timestamp}.md`
- Include emoji indicators (✅, ⚠️, ❌, 🔴, 🟡, 🟢)
- Tables for structured data
- Code blocks for examples

**JSON (if requested):**
```json
{
  "timestamp": "2025-11-04T...",
  "project_name": "...",
  "project_type": "fullstack",
  "production_readiness_score": 85,
  "quality_scores": {
    "architecture": 95,
    "code_quality": 90,
    "security": 88,
    "performance": 78,
    "scalability": 82,
    "maintainability": 95,
    "testing": 85,
    "monitoring": 60
  },
  "architecture_patterns": ["DDD", "CQRS", "Layered"],
  "tech_stack": {...},
  "tech_debt": [...],
  "recommendations": [...],
  "risks": [...]
}
```

---

## Success Criteria

An architecture analysis is complete when:

**Analysis Coverage:**
- ✅ Codebase structure discovered and documented
- ✅ Project type detected (frontend/backend/fullstack/monorepo)
- ✅ Architecture patterns identified (3+ if present)
- ✅ Technology stack documented with versions
- ✅ Domain model analyzed (if DDD/CQRS)
- ✅ API architecture assessed
- ✅ Security posture reviewed

**Quality Assessment:**
- ✅ Quality scores calculated for all 8 dimensions
- ✅ Production readiness score computed (0-100)
- ✅ Technical debt identified and prioritized
- ✅ Performance bottlenecks identified
- ✅ Scalability limitations documented

**Recommendations:**
- ✅ Recommendations provided (high/medium/low priority)
- ✅ Effort estimates included for each recommendation
- ✅ Risk assessment completed (technical + operational)
- ✅ Production readiness checklist generated

**Report Quality:**
- ✅ Comprehensive report generated (markdown and/or JSON)
- ✅ Report saved to docs/ directory
- ✅ Report includes all 15 sections
- ✅ Actionable insights provided

---

## Example Usage

### Example 1: Full Analysis (Current Directory)

```bash
User: /analyze-architecture

Winston: Analyzing architecture of current codebase...

[Discovers monorepo structure]
Project Type: Monorepo (backend + dashboard + chat-widget + shared packages)
Architecture: Pure 4-Layer DDD with CQRS

[Analyzes technology stack]
Backend: Node.js 20, TypeScript 5.8, Express 4.18, Prisma 6.9, PostgreSQL
Frontend: React 19, Material-UI 7.1, TanStack Query 5.81, Zustand 4.5

[Identifies patterns]
Patterns: Domain-Driven Design, CQRS, Layered Architecture, Event-Driven, Repository Pattern

[Calculates scores]
Architecture Quality: 95/100 ⭐⭐⭐⭐⭐
Code Quality: 90/100 ⭐⭐⭐⭐
Security: 88/100 ⭐⭐⭐⭐
Performance: 78/100 ⭐⭐⭐⭐
Scalability: 82/100 ⭐⭐⭐⭐
Maintainability: 95/100 ⭐⭐⭐⭐⭐
Testing: 85/100 ⭐⭐⭐⭐
Monitoring: 60/100 ⭐⭐⭐

Production Readiness Score: 85/100 ⭐⭐⭐⭐

✅ Report generated: docs/architecture-analysis-2025-11-04.md
```

### Example 2: Focused Security Analysis

```bash
User: /analyze-architecture . --focus security

Winston: Analyzing security posture of codebase...

[Security analysis only]
✅ Authentication: Clerk-based JWT (Strong)
✅ Authorization: RBAC with permissions (Strong)
✅ Multi-tenant RLS: Row-level security enforced (Excellent)
✅ Input Validation: Zod schemas (Strong)
✅ SQL Injection: Protected by Prisma ORM (Strong)
✅ XSS Protection: React JSX escaping (Strong)
⚠️  Secrets: .env files (Needs secret manager)
⚠️  DDoS Protection: Basic rate limiting (Needs enhancement)
❌ Security Monitoring: No SIEM (Critical gap)

Security Score: 88/100 ⭐⭐⭐⭐

🔴 HIGH PRIORITY Recommendations:
1. Migrate secrets to AWS Secrets Manager or Vault
2. Implement comprehensive security monitoring (SIEM)
3. Add DDoS protection (Cloudflare, AWS Shield)

✅ Report generated: docs/security-analysis-2025-11-04.md
```

### Example 3: JSON Output

```bash
User: /analyze-architecture . --output json

Winston: Analyzing architecture and generating JSON output...

✅ Analysis complete
✅ JSON report: docs/architecture-analysis-2025-11-04.json
✅ Markdown report: docs/architecture-analysis-2025-11-04.md

JSON output includes:
- production_readiness_score
- quality_scores (8 dimensions)
- architecture_patterns
- tech_stack
- tech_debt
- recommendations
- risks
```

---

## Integration with Other Skills

**Prerequisites:**
- No formal architecture document required
- Works with brownfield codebases
- Discovers structure dynamically

**Outputs used by:**
- **create-architecture:** Use analysis to document existing architecture
- **validate-architecture:** Use findings to validate quality
- **review-architecture:** Use as input for peer review
- **Implementation skills:** Use recommendations to prioritize work

**Workflow:**
```bash
# Step 1: Analyze existing codebase
/analyze-architecture

# Step 2: Document architecture (if needed)
/design-architecture docs/prd.md --existing docs/architecture-analysis.md

# Step 3: Review and validate
/review-architecture docs/architecture.md

# Step 4: Implement recommendations
@james *implement <recommendation-from-analysis>
```

---

## Telemetry

Track analysis metrics for continuous improvement:

```json
{
  "skill": "analyze-architecture",
  "timestamp": "2025-11-04T...",
  "project_type": "monorepo",
  "architecture_patterns": ["DDD", "CQRS", "Layered"],
  "production_readiness_score": 85,
  "quality_scores": {
    "architecture": 95,
    "code_quality": 90,
    "security": 88,
    "performance": 78,
    "scalability": 82,
    "maintainability": 95,
    "testing": 85,
    "monitoring": 60
  },
  "tech_debt_count": 283,
  "recommendations_count": 10,
  "duration_ms": 180000,
  "focus_area": "all",
  "output_format": "markdown"
}
```

---

## Quality Gates

**Minimum Requirements for Complete Analysis:**
- ✅ Codebase structure analyzed (directory tree, package.json files)
- ✅ Project type detected (with confidence score)
- ✅ Technology stack documented (with versions from package.json)
- ✅ At least 1 architectural pattern identified
- ✅ All 8 quality dimensions scored (0-100)
- ✅ Production readiness score calculated
- ✅ At least 3 recommendations provided
- ✅ Report generated in requested format

**Escalation Triggers:**
- Unable to detect project type (no package.json, no recognizable patterns)
- Zero architectural patterns identified
- Critical security vulnerabilities found (exposed secrets, SQL injection)
- Production readiness score < 50

---

## References

- `references/codebase-discovery-guide.md` - Techniques for discovering structure
- `references/architectural-patterns-catalog.md` - Complete pattern reference
- `references/tech-stack-catalog.md` - Technology identification guide
- `references/quality-scoring-rubrics.md` - Scoring methodology for each dimension
- `references/production-readiness-checklist.md` - Complete checklist template

---

*Analyze Architecture skill is ready to provide deep, comprehensive analysis of existing codebases.* 🔍
