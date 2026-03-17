---
name: when-building-backend-api-orchestrate-api-development
type: sop-workflow
description: |
  Use when building a production-ready REST API from requirements through deployment.
  Orchestrates 8-12 specialist agents across 5 phases using Test-Driven Development methodology.
  Covers planning, architecture, TDD implementation, comprehensive testing, documentation, and
  blue-green deployment over a 2-week timeline with emphasis on quality and reliability.
agents:
  - product-manager
  - system-architect
  - database-architect
  - qa-engineer
  - backend-developer
  - security-specialist
  - performance-analyst
  - api-documentation-specialist
  - devops-engineer
  - production-validator
  - performance-monitor
  - code-reviewer
phases: 5
memory_pattern: "api-development/{api-id}/phase-{N}/{agent}/{deliverable}"
---

# API Development Orchestration Workflow

Complete REST API development workflow using Test-Driven Development and multi-agent coordination. Orchestrates 8-12 specialist agents across planning, architecture design, TDD implementation, testing, documentation, and production deployment in a systematic 2-week process.

## Overview

This SOP implements a comprehensive API development workflow emphasizing quality through Test-Driven Development (TDD). The workflow balances speed with thoroughness, using hierarchical coordination for planning phases and parallel execution for development and testing. Each phase produces validated deliverables that subsequent phases consume, ensuring continuity and traceability.

The TDD approach ensures high test coverage (>90%), reduces bugs, and produces well-designed, maintainable code. Parallel execution of specialized reviews accelerates quality validation while maintaining comprehensive coverage of security, performance, and architectural concerns.

## Trigger Conditions

Use this workflow when:
- Building a new REST API or microservice from scratch
- Migrating existing API to modern architecture with comprehensive testing
- Need systematic TDD approach with documented test coverage
- Require production-ready API with security, performance, and scalability validation
- Timeline is 2-4 weeks with clear milestones and deliverables
- Quality gates (testing, security, performance) are non-negotiable
- Need comprehensive API documentation and operational runbooks

## Orchestrated Agents (12 Total)

### Planning & Architecture Agents
- **`product-manager`** - Requirements gathering, endpoint definition, API contracts, success criteria
- **`system-architect`** - API architecture design, RESTful patterns, versioning, error handling strategy
- **`database-architect`** - Schema design, query optimization, indexing, migration planning
- **`qa-engineer`** - Test planning, TDD strategy, coverage targets, performance benchmarks

### Development Agents (TDD Cycle)
- **`tester`** - Write tests first (red phase), integration tests, E2E scenarios
- **`backend-developer`** - Implement to pass tests (green phase), refactor for quality
- **`code-reviewer`** - Code quality review, refactoring suggestions, best practices validation

### Quality & Validation Agents
- **`security-specialist`** - Security architecture, OWASP validation, penetration testing
- **`performance-analyst`** - Load testing, stress testing, bottleneck identification, optimization
- **`api-documentation-specialist`** - OpenAPI specs, developer guides, code examples

### Deployment & Operations Agents
- **`devops-engineer`** - CI/CD pipeline, Docker/K8s deployment, infrastructure as code
- **`production-validator`** - Pre-production validation, go/no-go decision, smoke testing
- **`performance-monitor`** - Production monitoring, logging, alerting, SLO tracking

## Workflow Phases

### Phase 1: Planning & Design (Days 1-2, Sequential)

**Duration**: 2 days
**Execution Mode**: Sequential analysis and design
**Agents**: `product-manager`, `system-architect`, `database-architect`, `qa-engineer`

**Process**:

1. **Gather API Requirements** (Day 1 Morning)
   ```bash
   npx claude-flow hooks pre-task --description "API Development: ${API_NAME}"
   npx claude-flow swarm init --topology hierarchical --max-agents 12 --strategy specialized
   npx claude-flow agent spawn --type planner
   ```

   **Product Manager** defines:
   - Complete endpoint list with HTTP methods (GET, POST, PUT, DELETE, PATCH)
   - Data models and relationships (entities, attributes, cardinality)
   - Authentication and authorization requirements (OAuth, JWT, RBAC)
   - Rate limiting and quota specifications
   - Third-party integrations and external dependencies
   - API versioning strategy (URL path, header, content negotiation)
   - Success metrics and SLAs (response time, uptime, throughput)

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-1/product-manager/requirements" \
     --value "${REQUIREMENTS_JSON}"
   ```

2. **Design API Architecture** (Day 1 Afternoon)
   ```bash
   npx claude-flow memory retrieve --key "api-development/${API_ID}/phase-1/product-manager/requirements"
   npx claude-flow agent spawn --type system-architect
   ```

   **System Architect** designs:
   - RESTful API structure following Richardson Maturity Model
   - URL patterns and resource naming conventions
   - Request/response formats with JSON schemas
   - Error handling patterns (error codes, messages, stack traces)
   - Pagination, filtering, sorting, and search strategies
   - Caching strategy (ETags, cache-control headers)
   - API security architecture (authentication flow, token management)
   - Versioning and backward compatibility approach

   Generate OpenAPI 3.0 specification:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-1/system-architect/openapi-spec" \
     --value "${OPENAPI_YAML}"
   ```

3. **Design Database Schema** (Day 2 Morning)
   ```bash
   npx claude-flow memory retrieve --key "api-development/${API_ID}/phase-1/system-architect/openapi-spec"
   npx claude-flow agent spawn --type code-analyzer
   ```

   **Database Architect** creates:
   - Normalized schema design (3NF) with entity-relationship diagram
   - Table definitions (columns, data types, constraints, defaults)
   - Relationships and foreign key constraints
   - Indexes for query performance (primary, secondary, composite)
   - Migration scripts (up and down migrations)
   - Backup and recovery strategy
   - Scaling strategy (sharding, replication, read replicas)

   Generate SQL schema and migrations:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-1/database-architect/schema" \
     --value "${SCHEMA_SQL}"
   npx claude-flow memory store --key "api-development/${API_ID}/phase-1/database-architect/migrations"
   ```

4. **Create Test Strategy** (Day 2 Afternoon)
   ```bash
   npx claude-flow memory retrieve --pattern "api-development/${API_ID}/phase-1/*"
   npx claude-flow agent spawn --type tester
   ```

   **QA Engineer** plans:
   - Unit test strategy (per endpoint, per function)
   - Integration test scenarios (database, external APIs)
   - End-to-end test workflows (complete user journeys)
   - Performance test targets (load, stress, endurance)
   - Security test cases (OWASP API Security Top 10)
   - Test data management (fixtures, factories, mocks)
   - Coverage targets (>90% for new code)
   - CI/CD test automation strategy

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-1/qa-engineer/test-plan"
   npx claude-flow hooks post-task --task-id "phase-1-planning"
   ```

**Outputs**:
- API requirements document with complete endpoint specifications
- OpenAPI 3.0 specification (machine-readable contract)
- Database schema with ER diagram and migrations
- Comprehensive test plan with coverage targets
- DevOps plan with infrastructure requirements

**Success Criteria**:
- [ ] All API endpoints documented in OpenAPI spec
- [ ] Database schema normalized and indexed for performance
- [ ] Test strategy covers all quality dimensions
- [ ] Architecture approved by technical stakeholders
- [ ] Phase 1 deliverables stored in memory

---

### Phase 2: Foundation Setup (Days 3-4, Parallel)

**Duration**: 2 days
**Execution Mode**: Parallel infrastructure setup
**Agents**: `backend-developer`, `database-architect`, `devops-engineer`

**Process**:

1. **Initialize Development Environment**
   ```bash
   npx claude-flow swarm init --topology mesh --max-agents 3 --strategy adaptive
   npx claude-flow task orchestrate --strategy parallel
   ```

2. **Parallel Setup Execution**

   Spawn all setup agents concurrently:
   ```bash
   # Backend project setup
   npx claude-flow agent spawn --type backend-dev --capabilities "nodejs,typescript,express"

   # Database setup
   npx claude-flow agent spawn --type code-analyzer --capabilities "postgresql,prisma,migrations"

   # CI/CD setup
   npx claude-flow agent spawn --type cicd-engineer --capabilities "github-actions,docker,testing"
   ```

   **Backend Developer** initializes:
   - Node.js/Express (or FastAPI/Flask/Spring Boot) project
   - TypeScript configuration (strict mode, path aliases)
   - ESLint + Prettier (code quality and formatting)
   - Environment variable management (dotenv, validation)
   - Dependency installation (express, prisma, jest, supertest, etc.)
   - Project structure (controllers, services, models, middleware)
   - Logging framework (Winston, Pino) with structured logging
   - Error handling middleware (global error handler)

   **Memory Pattern**: `api-development/${API_ID}/phase-2/backend-developer/project-setup`

   **Database Architect** sets up:
   - PostgreSQL database (or MySQL/MongoDB)
   - Connection pooling configuration (pg-pool, connection limits)
   - Initial migration execution (create tables, indexes)
   - Seed data for development and testing
   - Database backup scripts (pg_dump automation)
   - Performance monitoring queries (slow query log)

   **Memory Pattern**: `api-development/${API_ID}/phase-2/database-architect/db-config`

   **DevOps Engineer** configures:
   - GitHub Actions workflow (or GitLab CI/Jenkins)
   - Docker containers (multi-stage builds for optimization)
   - Docker Compose for local development
   - Environment secrets management (GitHub Secrets, Vault)
   - Automated testing pipeline (run tests on PR)
   - Code quality checks (linting, type checking)
   - Build artifact generation and storage

   **Memory Pattern**: `api-development/${API_ID}/phase-2/devops-engineer/ci-config`

   **Coordination Script**:
   ```bash
   npx claude-flow hooks post-edit --file "package.json" \
     --memory-key "api-development/${API_ID}/phase-2/setup-complete"
   npx claude-flow hooks notify --message "Development environment ready"
   ```

**Outputs**:
- Initialized project with all dependencies
- Database with schema and seed data
- CI/CD pipeline operational
- Development environment fully functional

**Success Criteria**:
- [ ] Project builds without errors
- [ ] Database connections established and tested
- [ ] CI/CD pipeline runs successfully
- [ ] Local development environment documented

---

### Phase 3: TDD Implementation (Days 5-10, Red-Green-Refactor Cycle)

**Duration**: 6 days
**Execution Mode**: Iterative TDD cycles per endpoint
**Agents**: `tester`, `backend-developer`, `code-reviewer`

**Process**:

This phase follows strict Test-Driven Development:
1. **RED**: Write failing tests (tester agent)
2. **GREEN**: Implement code to pass tests (backend-developer agent)
3. **REFACTOR**: Improve code quality (code-reviewer agent)

**TDD Cycle Example** (POST /api/auth/register endpoint):

1. **RED Phase: Write Failing Tests** (30-60 min per endpoint)
   ```bash
   npx claude-flow agent spawn --type tester
   ```

   **Tester Agent** writes:
   ```javascript
   // Unit tests
   describe('POST /api/auth/register', () => {
     test('should register user with valid email and password', async () => {
       const response = await request(app)
         .post('/api/auth/register')
         .send({ email: 'user@example.com', password: 'SecurePass123!' });

       expect(response.status).toBe(201);
       expect(response.body).toHaveProperty('token');
       expect(response.body.user.email).toBe('user@example.com');
     });

     test('should reject duplicate email registration', async () => {
       // Create user first
       await createUser({ email: 'existing@example.com' });

       const response = await request(app)
         .post('/api/auth/register')
         .send({ email: 'existing@example.com', password: 'Pass123!' });

       expect(response.status).toBe(409);
       expect(response.body.error).toContain('Email already exists');
     });

     test('should validate password strength', async () => {
       const response = await request(app)
         .post('/api/auth/register')
         .send({ email: 'user@example.com', password: 'weak' });

       expect(response.status).toBe(400);
       expect(response.body.error).toContain('Password must be at least 8 characters');
     });

     test('should validate email format', async () => {
       const response = await request(app)
         .post('/api/auth/register')
         .send({ email: 'invalid-email', password: 'SecurePass123!' });

       expect(response.status).toBe(400);
       expect(response.body.error).toContain('Invalid email format');
     });
   });

   // Integration tests
   describe('User Registration Integration', () => {
     test('should create user in database', async () => {
       const response = await request(app)
         .post('/api/auth/register')
         .send({ email: 'dbtest@example.com', password: 'Pass123!' });

       const userInDb = await db.user.findUnique({ where: { email: 'dbtest@example.com' } });
       expect(userInDb).toBeDefined();
       expect(userInDb.passwordHash).not.toBe('Pass123!'); // Password should be hashed
     });
   });
   ```

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-3/tester/auth/register-tests" \
     --value "${TEST_FILE_CONTENT}"
   ```

2. **GREEN Phase: Implement to Pass Tests** (1-2 hours per endpoint)
   ```bash
   npx claude-flow memory retrieve --key "api-development/${API_ID}/phase-3/tester/auth/register-tests"
   npx claude-flow agent spawn --type backend-dev
   ```

   **Backend Developer** implements:
   ```javascript
   // POST /api/auth/register implementation
   router.post('/register', async (req, res, next) => {
     try {
       // Validate input
       const { email, password } = req.body;

       if (!isValidEmail(email)) {
         return res.status(400).json({ error: 'Invalid email format' });
       }

       if (password.length < 8) {
         return res.status(400).json({ error: 'Password must be at least 8 characters' });
       }

       // Check for duplicate email
       const existingUser = await db.user.findUnique({ where: { email } });
       if (existingUser) {
         return res.status(409).json({ error: 'Email already exists' });
       }

       // Hash password
       const passwordHash = await bcrypt.hash(password, 10);

       // Create user
       const user = await db.user.create({
         data: { email, passwordHash }
       });

       // Generate JWT token
       const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: '7d' });

       res.status(201).json({
         token,
         user: { id: user.id, email: user.email }
       });
     } catch (error) {
       next(error);
     }
   });
   ```

   Run tests and verify all pass:
   ```bash
   npm test -- auth/register.test.js
   # All tests should pass (GREEN)
   ```

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-3/backend-developer/auth/register-impl"
   ```

3. **REFACTOR Phase: Improve Code Quality** (30 min per endpoint)
   ```bash
   npx claude-flow memory retrieve --pattern "api-development/${API_ID}/phase-3/*/auth/register-*"
   npx claude-flow agent spawn --type reviewer
   ```

   **Code Reviewer** evaluates:
   - Code readability and clarity
   - Duplication (extract validation to middleware)
   - Security best practices (password hashing, JWT signing)
   - Error handling completeness
   - Performance optimizations

   Suggests refactoring:
   ```javascript
   // Extracted validation middleware
   const validateRegistration = (req, res, next) => {
     const { email, password } = req.body;

     if (!isValidEmail(email)) {
       return res.status(400).json({ error: 'Invalid email format' });
     }

     if (password.length < 8) {
       return res.status(400).json({ error: 'Password must be at least 8 characters' });
     }

     next();
   };

   // Cleaner route handler
   router.post('/register', validateRegistration, async (req, res, next) => {
     try {
       const user = await authService.registerUser(req.body);
       const token = authService.generateToken(user.id);

       res.status(201).json({ token, user });
     } catch (error) {
       if (error.code === 'DUPLICATE_EMAIL') {
         return res.status(409).json({ error: 'Email already exists' });
       }
       next(error);
     }
   });
   ```

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-3/code-reviewer/auth/register-review"
   npx claude-flow hooks post-edit --file "src/routes/auth.ts"
   ```

4. **Repeat TDD Cycle for All Endpoints** (Days 5-10)

   Apply RED-GREEN-REFACTOR to all endpoints:
   - Authentication (register, login, logout, refresh, reset-password)
   - CRUD operations (create, read, update, delete for all resources)
   - Search and filtering
   - Pagination and sorting
   - File uploads (if applicable)
   - Webhooks (if applicable)

   **Progress Tracking**:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-3/progress" \
     --value '{"completed_endpoints": 12, "total_endpoints": 20, "coverage": 93.5}'
   ```

**Outputs**:
- All API endpoints implemented
- Comprehensive test suite with >90% coverage
- Refactored, clean, maintainable code
- All tests passing (green)

**Success Criteria**:
- [ ] All endpoints functional and tested
- [ ] Test coverage exceeds 90%
- [ ] No code quality violations (ESLint passing)
- [ ] Code review approved for all endpoints
- [ ] TDD cycle completed for entire API surface

---

### Phase 4: Testing & Documentation (Days 11-12, Parallel)

**Duration**: 2 days
**Execution Mode**: Parallel validation across multiple dimensions
**Agents**: `qa-engineer`, `security-specialist`, `performance-analyst`, `api-documentation-specialist`

**Process**:

1. **Initialize Testing Swarm**
   ```bash
   npx claude-flow swarm init --topology star --max-agents 4 --strategy specialized
   npx claude-flow task orchestrate --strategy parallel --priority high
   ```

2. **Parallel Testing Execution**

   Spawn all testing agents concurrently:
   ```bash
   # E2E testing
   npx claude-flow agent spawn --type tester --focus "end-to-end"

   # Performance testing
   npx claude-flow agent spawn --type perf-analyzer --focus "load-stress-endurance"

   # Security testing
   npx claude-flow agent spawn --type security-manager --focus "owasp-penetration"

   # Documentation
   npx claude-flow agent spawn --type api-docs --focus "openapi-developer-guide"
   ```

   **QA Engineer** conducts:
   - **End-to-End Testing**: Complete user workflows (register → login → CRUD → logout)
   - **Error Scenario Testing**: Invalid inputs, unauthorized access, rate limiting
   - **Edge Case Testing**: Boundary conditions, null values, concurrent requests
   - **Smoke Testing**: Basic functionality across all endpoints

   **Memory Pattern**: `api-development/${API_ID}/phase-4/qa-engineer/e2e-results`

   **Performance Analyst** tests:
   - **Load Testing**: 1000 req/sec sustained for 10 minutes (target)
   - **Stress Testing**: Find breaking point (max throughput)
   - **Endurance Testing**: 24-hour sustained load for memory leaks
   - **Spike Testing**: Sudden traffic spikes (10x normal load)
   - **Bottleneck Identification**: Database queries, API calls, CPU/memory usage

   Tools: k6, Apache JMeter, Gatling

   **Memory Pattern**: `api-development/${API_ID}/phase-4/performance-analyst/benchmarks`

   **Security Specialist** validates:
   - **OWASP API Security Top 10**:
     1. Broken Object Level Authorization (BOLA)
     2. Broken Authentication
     3. Broken Object Property Level Authorization
     4. Unrestricted Resource Consumption
     5. Broken Function Level Authorization (BFLA)
     6. Unrestricted Access to Sensitive Business Flows
     7. Server Side Request Forgery (SSRF)
     8. Security Misconfiguration
     9. Improper Inventory Management
     10. Unsafe Consumption of APIs
   - SQL injection testing (automated + manual)
   - XSS vulnerability scanning
   - Authentication bypass attempts
   - Rate limiting validation
   - Secrets scanning (no hardcoded credentials)

   Tools: OWASP ZAP, Burp Suite, Snyk

   **Memory Pattern**: `api-development/${API_ID}/phase-4/security-specialist/audit-report`

   **API Documentation Specialist** creates:
   - **OpenAPI/Swagger UI**: Interactive API documentation
   - **Authentication Guide**: How to obtain and use tokens
   - **Endpoint Reference**: All endpoints with parameters, responses, errors
   - **Code Examples**: cURL, JavaScript, Python, Java SDK examples
   - **Rate Limiting Guide**: Quota limits and header interpretations
   - **Error Handling Guide**: Error codes, messages, troubleshooting
   - **Developer Getting Started**: Quick start tutorial
   - **Changelog**: Versioning and breaking changes

   **Memory Pattern**: `api-development/${API_ID}/phase-4/api-documentation-specialist/docs`

3. **DevOps Runbook** (Parallel with documentation)
   ```bash
   npx claude-flow agent spawn --type cicd-engineer --focus "operations"
   ```

   **DevOps Engineer** documents:
   - Deployment procedures (step-by-step)
   - Monitoring and alerting setup (Grafana, Prometheus)
   - Troubleshooting guide (common issues, solutions)
   - Performance tuning (database, caching, scaling)
   - Backup and recovery procedures
   - Incident response plan (runbook)
   - Rollback procedures

   **Memory Pattern**: `api-development/${API_ID}/phase-4/devops-engineer/runbook`

**Outputs**:
- E2E test results (all passing)
- Performance benchmark report (meets targets)
- Security audit report (no critical issues)
- Complete API documentation (developer-ready)
- Operations runbook (deployment-ready)

**Success Criteria**:
- [ ] All E2E tests passing
- [ ] Performance targets met (API < 200ms, throughput > 1000 req/sec)
- [ ] Security audit passed (zero critical, zero high issues)
- [ ] Documentation complete and published
- [ ] Operations runbook approved

---

### Phase 5: Deployment & Monitoring (Days 13-14, Sequential → Continuous)

**Duration**: 2 days + ongoing monitoring
**Execution Mode**: Sequential deployment with validation gates
**Agents**: `production-validator`, `devops-engineer`, `performance-monitor`

**Process**:

1. **Pre-Production Validation** (Day 13 Morning)
   ```bash
   npx claude-flow hooks pre-task --description "Final production validation"
   npx claude-flow agent spawn --type production-validator
   ```

   **Production Validator** checks:
   - **All Tests Passing**: 100% of test suite (unit + integration + E2E)
   - **Code Coverage**: >90% verified
   - **Security Audit**: Passed with zero critical/high issues
   - **Performance Benchmarks**: All targets met or exceeded
   - **Documentation**: Complete and published
   - **Monitoring Setup**: Dashboards and alerts configured
   - **Rollback Plan**: Documented and rehearsed

   Generate go/no-go report:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-5/production-validator/go-no-go" \
     --value '{"decision": "GO", "readiness_score": 98, "blockers": []}'
   ```

   If any validation fails:
   ```bash
   # Return to appropriate phase to fix issues
   npx claude-flow hooks notify --message "Production validation FAILED: ${BLOCKER_ISSUES}"
   # Halt deployment until issues resolved
   ```

2. **Staging Deployment** (Day 13 Afternoon)
   ```bash
   npx claude-flow agent spawn --type cicd-engineer
   ```

   **DevOps Engineer** deploys to staging:
   ```bash
   # Deploy API to staging environment
   kubectl apply -f k8s/staging/

   # Run smoke tests
   npm run test:smoke -- --env=staging

   # Validate monitoring
   curl https://api-staging.example.com/health
   ```

   **Staging Validation**:
   - Full test suite execution against staging
   - Data persistence verification
   - Error handling validation
   - Monitoring dashboard validation
   - Load balancer health checks

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-5/devops-engineer/staging-deploy"
   ```

3. **Production Deployment** (Day 14 Morning - Blue-Green Strategy)
   ```bash
   npx claude-flow workflow create --name "production-deployment" \
     --steps '["blue-green-deploy","canary-rollout","full-rollout","monitor"]'
   ```

   **DevOps Engineer** executes:
   ```bash
   # Step 1: Deploy to green environment (alongside blue)
   kubectl apply -f k8s/production/green/

   # Step 2: Run smoke tests on green
   npm run test:smoke -- --env=production-green

   # Step 3: Gradual traffic shift (canary rollout)
   # 10% traffic to green
   kubectl patch service api-service -p '{"spec":{"selector":{"version":"green","weight":"10"}}}'
   sleep 300  # Monitor for 5 minutes

   # 50% traffic to green
   kubectl patch service api-service -p '{"spec":{"selector":{"version":"green","weight":"50"}}}'
   sleep 600  # Monitor for 10 minutes

   # 100% traffic to green
   kubectl patch service api-service -p '{"spec":{"selector":{"version":"green","weight":"100"}}}'

   # Step 4: Keep blue environment ready for rollback (for 24 hours)
   ```

   **Rollback Procedure** (if issues detected):
   ```bash
   # Instant rollback to blue
   kubectl patch service api-service -p '{"spec":{"selector":{"version":"blue","weight":"100"}}}'
   ```

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-5/devops-engineer/production-deploy" \
     --value '{"status": "SUCCESS", "deployment_time": "2025-01-15T10:00:00Z", "version": "v1.0.0"}'
   ```

4. **Post-Deployment Monitoring** (Day 14 Afternoon + Ongoing)
   ```bash
   npx claude-flow agent spawn --type performance-monitor
   ```

   **Performance Monitor** tracks:
   - **Application Metrics**:
     - API response time (p50, p95, p99)
     - Throughput (requests per second)
     - Error rate (4xx, 5xx errors)
     - Uptime and availability
   - **Infrastructure Metrics**:
     - CPU and memory utilization
     - Database connection pool usage
     - Cache hit ratio
     - Network throughput
   - **Business Metrics**:
     - API usage by endpoint
     - User activity patterns
     - Rate limit violations
     - Authentication success/failure rates

   Generate hourly reports for first 24 hours:
   ```bash
   npx claude-flow hooks post-task --task-id "production-monitoring" --export-metrics true
   npx claude-flow memory store --key "api-development/${API_ID}/phase-5/performance-monitor/metrics/hour-${HOUR}"
   ```

   **Alert Configuration**:
   - Response time > 500ms (p95): WARNING
   - Response time > 1000ms (p95): CRITICAL
   - Error rate > 1%: WARNING
   - Error rate > 5%: CRITICAL
   - Uptime < 99.9%: CRITICAL
   - Database connection pool > 80%: WARNING

5. **Documentation Publication** (Day 14)
   ```bash
   npx claude-flow agent spawn --type api-docs
   ```

   **Update Final Documentation**:
   - Production API URLs and endpoints
   - Authentication endpoints (production)
   - Monitoring dashboards (link to Grafana)
   - Support contact information
   - SLA and uptime guarantees

   Publish to developer portal:
   ```bash
   npm run docs:publish -- --env=production
   ```

6. **Knowledge Transfer** (End of Phase 5)
   ```bash
   npx claude-flow hooks session-end --export-workflow "/tmp/${API_ID}-workflow.json"
   ```

   Create handoff materials:
   - Developer onboarding guide
   - Support team training materials
   - Common issues and troubleshooting
   - Escalation procedures

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "api-development/${API_ID}/phase-5/knowledge-transfer/complete"
   ```

**Outputs**:
- Production API (live and stable)
- Complete documentation (published to developer portal)
- Monitoring dashboards (real-time metrics)
- Trained support team (ready for inquiries)
- Workflow documentation (for future reference)

**Success Criteria**:
- [ ] Production deployment successful with zero downtime
- [ ] All monitoring metrics within acceptable ranges
- [ ] Documentation published and accessible
- [ ] Support team trained and ready
- [ ] Post-deployment validation complete

---

## Memory Coordination

### Namespace Convention

All workflow data follows this hierarchical pattern:

```
api-development/{api-id}/phase-{N}/{agent-type}/{deliverable-type}
```

**Examples**:
- `api-development/user-api-v1/phase-1/product-manager/requirements`
- `api-development/user-api-v1/phase-1/system-architect/openapi-spec`
- `api-development/user-api-v1/phase-2/backend-developer/project-setup`
- `api-development/user-api-v1/phase-3/tester/auth/register-tests`
- `api-development/user-api-v1/phase-4/security-specialist/audit-report`
- `api-development/user-api-v1/phase-5/devops-engineer/production-deploy`

### Cross-Phase Data Flow

**Phase 1 → Phase 2**:
```bash
# Phase 2 retrieves design specifications
npx claude-flow memory retrieve --key "api-development/${API_ID}/phase-1/system-architect/openapi-spec"
npx claude-flow memory retrieve --key "api-development/${API_ID}/phase-1/database-architect/schema"
```

**Phase 2 → Phase 3**:
```bash
# Phase 3 retrieves project structure and test plan
npx claude-flow memory retrieve --key "api-development/${API_ID}/phase-2/backend-developer/project-setup"
npx claude-flow memory retrieve --key "api-development/${API_ID}/phase-1/qa-engineer/test-plan"
```

**Phase 3 → Phase 4**:
```bash
# Phase 4 retrieves implementation for testing
npx claude-flow memory retrieve --pattern "api-development/${API_ID}/phase-3/backend-developer/*"
```

**Phase 4 → Phase 5**:
```bash
# Phase 5 retrieves test results and documentation
npx claude-flow memory retrieve --pattern "api-development/${API_ID}/phase-4/*/results"
```

---

## Scripts & Automation

### Pre-Workflow Initialization

```bash
#!/bin/bash
# Initialize API development workflow

API_NAME="$1"
API_ID="${API_NAME}-api-$(date +%Y%m%d)"

# Setup coordination
npx claude-flow hooks pre-task --description "API Development: ${API_NAME}"

# Initialize hierarchical swarm (12 agents max)
npx claude-flow swarm init --topology hierarchical --max-agents 12 --strategy specialized

# Store API metadata
npx claude-flow memory store --key "api-development/${API_ID}/metadata" --value '{
  "api_name": "'"${API_NAME}"'",
  "api_id": "'"${API_ID}"'",
  "start_date": "'"$(date -I)"'",
  "timeline_days": 14,
  "phases": 5,
  "tdd_approach": true
}'

echo "✅ API development initialized: ${API_ID}"
```

### TDD Cycle Script

```bash
#!/bin/bash
# Execute TDD cycle for single endpoint

API_ID="$1"
ENDPOINT_PATH="$2"  # e.g., "POST /api/auth/register"

echo "🔴 RED Phase: Writing tests for ${ENDPOINT_PATH}"
npx claude-flow agent spawn --type tester --task "write-tests:${ENDPOINT_PATH}"

# Wait for tests to be written
npx claude-flow memory retrieve --key "api-development/${API_ID}/phase-3/tester/${ENDPOINT_PATH}/tests"

echo "🟢 GREEN Phase: Implementing ${ENDPOINT_PATH}"
npx claude-flow agent spawn --type backend-dev --task "implement:${ENDPOINT_PATH}"

# Run tests to verify implementation
npm test -- "${ENDPOINT_PATH}.test.js"

echo "🔵 REFACTOR Phase: Code review for ${ENDPOINT_PATH}"
npx claude-flow agent spawn --type reviewer --task "review:${ENDPOINT_PATH}"

# Store completion
npx claude-flow hooks post-edit --file "src/routes/${ENDPOINT_PATH}.ts" \
  --memory-key "api-development/${API_ID}/phase-3/completed/${ENDPOINT_PATH}"
```

### Deployment Script

```bash
#!/bin/bash
# Blue-green deployment to production

API_ID="$1"
VERSION="$2"

echo "🚀 Starting blue-green deployment: ${VERSION}"

# Pre-deployment validation
npx claude-flow agent spawn --type production-validator
VALIDATION=$(npx claude-flow memory retrieve --key "api-development/${API_ID}/phase-5/production-validator/go-no-go")

if [ "$(echo $VALIDATION | jq -r '.decision')" != "GO" ]; then
  echo "❌ Production validation FAILED. Aborting deployment."
  exit 1
fi

# Deploy to green environment
kubectl apply -f k8s/production/green/

# Smoke tests
npm run test:smoke -- --env=production-green

# Gradual traffic shift (canary)
for WEIGHT in 10 50 100; do
  echo "Shifting ${WEIGHT}% traffic to green..."
  kubectl patch service api-service -p "{\"spec\":{\"selector\":{\"version\":\"green\",\"weight\":\"${WEIGHT}\"}}}"

  # Monitor for issues (5-10 minutes per step)
  DURATION=$((WEIGHT == 100 ? 10 : 5))
  sleep $((DURATION * 60))

  # Check error rate
  ERROR_RATE=$(curl -s https://monitoring.example.com/api/error-rate | jq -r '.rate')
  if (( $(echo "$ERROR_RATE > 1.0" | bc -l) )); then
    echo "❌ High error rate detected: ${ERROR_RATE}%. Rolling back."
    kubectl patch service api-service -p '{"spec":{"selector":{"version":"blue","weight":"100"}}}'
    exit 1
  fi
done

echo "✅ Deployment complete: ${VERSION}"
npx claude-flow hooks post-task --task-id "production-deployment" --export-metrics true
```

---

## Success Metrics

### Technical Metrics
- **Test Coverage**: > 90% (code coverage report)
- **API Response Time**: < 200ms (p95)
- **Uptime**: 99.9%+ (production SLA)
- **Error Rate**: < 0.1% (4xx + 5xx errors)
- **Code Quality Score**: A rating (SonarQube/CodeClimate)
- **Security Audit**: Zero critical, zero high issues

### Performance Metrics
- **Throughput**: > 1000 req/sec sustained
- **Database Query Time**: < 50ms (p95)
- **Memory Usage**: < 512MB per instance
- **CPU Usage**: < 70% under normal load

### Quality Metrics
- **TDD Adherence**: 100% (all endpoints test-first)
- **Documentation Coverage**: 100% of endpoints documented
- **API Compliance**: OpenAPI 3.0 valid (no errors)
- **Code Review Approval**: 100% (all code reviewed)

---

## Usage Examples

### Example 1: User Management API

```bash
# Initialize workflow
API_ID="user-management-api-20250115"
npx claude-flow hooks pre-task --description "User Management API Development"

# Phase 1: Planning (Day 1-2)
npx claude-flow agent spawn --type planner
# Output: 15 endpoints defined, authentication strategy established

# Phase 3: TDD Implementation (Day 5-10)
for endpoint in "POST /api/users/register" "POST /api/users/login" "GET /api/users/:id"; do
  ./tdd-cycle.sh "${API_ID}" "${endpoint}"
done
# Output: All endpoints implemented with 94% test coverage

# Phase 5: Production Deployment (Day 14)
./deploy-production.sh "${API_ID}" "v1.0.0"
# Output: Deployed successfully, handling 1500 req/sec with 99.95% uptime
```

### Example 2: Payment Gateway API

```bash
# High-security API with PCI compliance
API_ID="payment-gateway-api-20250120"

# Phase 1: Enhanced security planning
npx claude-flow agent spawn --type system-architect --focus "pci-compliance"
npx claude-flow agent spawn --type security-specialist --focus "payment-security"
# Output: PCI DSS compliant architecture designed

# Phase 4: Enhanced security testing
npx claude-flow agent spawn --type security-manager --focus "penetration-testing-comprehensive"
# Output: Zero vulnerabilities, PCI DSS validation passed
```

### Example 3: Microservice API (Event-Driven)

```bash
# Microservice with message queue integration
API_ID="order-service-api-20250125"

# Phase 2: Message queue setup
npx claude-flow agent spawn --type backend-dev --capabilities "rabbitmq,events"
# Output: Event-driven architecture with pub/sub patterns

# Phase 3: Event handler TDD
./tdd-cycle.sh "${API_ID}" "POST /api/orders/create"
./tdd-cycle.sh "${API_ID}" "EVENT order.created"
# Output: Synchronous API + asynchronous event processing
```

---

## GraphViz Process Diagram

See `when-building-backend-api-orchestrate-api-development-process.dot` for visual workflow representation showing:
- 5 phases with TDD cycle details
- 12 agent interactions and coordination
- Memory flow between phases
- Blue-green deployment strategy
- Validation gates and decision points

---

## Quality Checklist

Before considering API development complete, verify:

- [ ] **Phase 1**: Requirements documented, OpenAPI spec complete, database schema designed
- [ ] **Phase 2**: Development environment operational, CI/CD pipeline functional
- [ ] **Phase 3**: All endpoints implemented following TDD, test coverage > 90%
- [ ] **Phase 4**: E2E tests passing, security audit passed, performance benchmarks met
- [ ] **Phase 5**: Production deployment successful, monitoring active, documentation published

**Memory Verification**:
- [ ] `api-development/${API_ID}/phase-1/*` - Planning artifacts
- [ ] `api-development/${API_ID}/phase-2/*` - Setup configurations
- [ ] `api-development/${API_ID}/phase-3/*` - TDD implementation + tests
- [ ] `api-development/${API_ID}/phase-4/*` - Test results + documentation
- [ ] `api-development/${API_ID}/phase-5/*` - Deployment logs + metrics

---

**Workflow Complexity**: Medium (12 agents, 14 days, 5 phases)
**Coordination Pattern**: Hierarchical with TDD cycle iteration
**Memory Footprint**: ~30-50 memory entries per API
**Typical Use Case**: Production-ready REST API with comprehensive testing and quality gates
