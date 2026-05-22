---
name: architect-role-skill
version: 1.0.0
category: architecture
complexity: high
status: active
created: 2025-12-12
author: claude-command-and-control

description: |
  Professional software architecture skill for analyzing existing codebases,
  designing new systems, creating comprehensive planning documents, and guiding
  technical decision-making through structured architectural workflows.

triggers:
  - "design system"
  - "create architecture"
  - "analyze codebase"
  - "evaluate technology stack"
  - "architectural review"

dependencies: []

tags:
  - architecture
  - system-design
  - planning
  - technical-decisions
  - documentation
---

# Architect Role Skill

## Description

Analyze existing codebases for architectural improvements or guide greenfield projects through comprehensive software planning and system design. This skill implements professional architecture practices including requirements gathering, system design, technology selection, and comprehensive planning document generation.

## When to Use This Skill

- Designing new systems or applications (greenfield projects)
- Analyzing existing codebases for architectural improvements
- Evaluating and recommending technology stack changes
- Creating comprehensive planning and architecture documents
- Assessing scalability, maintainability, and performance
- Documenting architectural decisions and trade-offs
- Developing phased implementation roadmaps

## When NOT to Use This Skill

- For code implementation (use builder-role-skill)
- For infrastructure deployment (use devops-role-skill)
- For testing and validation (use validator-role-skill)
- For documentation writing (use scribe-role-skill)

## Prerequisites

- Project requirements or existing codebase to analyze
- Access to stakeholder requirements (for greenfield)
- Git repository with project history (for analysis)
- Understanding of target deployment environment

---

## Workflow

### Phase 1: Greenfield Project Initialization

Design new systems from requirements through comprehensive planning.

**Step 1.1: Requirements Discovery**

Engage stakeholders with structured questions:

```markdown
## Requirements Discovery Questionnaire

### Business Goals
- What problem does this application solve?
- Who are the target users?
- What are the critical features?
- What are the success metrics?

### Technical Requirements
- What are the performance requirements?
- What are the scalability expectations?
- What are the security requirements?
- What compliance standards must be met?

### Constraints
- What are the budget constraints?
- What are the timeline constraints?
- What technologies are you familiar with?
- What deployment environment (cloud, on-premise, hybrid)?

### Integration
- What existing systems must integrate with this?
- What third-party services are required?
- What data sources need to be connected?
```

**Step 1.2: Planning Document Generation**

Create the following artifacts in project root:

**1. DEVELOPMENT_PLAN.md**

```markdown
# Development Plan: [Project Name]

## Executive Summary
[1-2 paragraph overview of the project, its goals, and approach]

## System Architecture Overview
[High-level description of system components and their relationships]

## Technology Stack Justification

### Frontend
- Framework: [Choice]
- Rationale: [Why this was selected]
- Alternatives Considered: [What was rejected and why]

### Backend
- Framework: [Choice]
- Rationale: [Why this was selected]
- Alternatives Considered: [What was rejected and why]

### Database
- System: [Choice]
- Rationale: [Why this was selected]
- Schema Strategy: [Relational/Document/Graph]

### Infrastructure
- Hosting: [Cloud provider/On-premise]
- Container Orchestration: [If applicable]
- CI/CD: [Tools selected]

## Component Breakdown

### Component 1: [Name]
- Purpose: [What it does]
- Responsibilities: [Key functions]
- Dependencies: [What it depends on]
- API Surface: [Public interfaces]

### Component 2: [Name]
[Same structure...]

## Data Model Design

### Entity: [Name]
```
{
  field1: type,
  field2: type,
  relationships: [...]
}
```

## API Specifications

### Endpoint: [Method] [Path]
- Purpose: [What it does]
- Request: [Schema]
- Response: [Schema]
- Authentication: [Requirements]
- Rate Limiting: [Policy]

## Security Architecture
- Authentication Strategy: [JWT/Session/OAuth/etc]
- Authorization Model: [RBAC/ABAC/etc]
- Data Encryption: [At rest/In transit]
- Secrets Management: [Vault/KMS/etc]
- Security Testing: [SAST/DAST/Penetration testing]

## Deployment Strategy
- Environments: [Dev/Staging/Production]
- Deployment Method: [Blue-green/Canary/Rolling]
- Rollback Strategy: [How to recover from failures]
- Monitoring: [What to monitor]
- Alerting: [When to alert]

## Development Phases

### Phase 1: Foundation (Weeks 1-2)
- [ ] Database schema implementation
- [ ] Authentication service
- [ ] Basic API structure
- [ ] Development environment setup

### Phase 2: Core Features (Weeks 3-5)
- [ ] Feature 1 implementation
- [ ] Feature 2 implementation
- [ ] Integration testing

### Phase 3: Integration & Polish (Weeks 6-8)
- [ ] Third-party integrations
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Documentation

### Phase 4: Launch (Week 9)
- [ ] Production deployment
- [ ] Monitoring setup
- [ ] Post-launch support plan

## Success Metrics
- Performance: [Specific targets]
- Reliability: [Uptime targets]
- User Adoption: [Metrics]
- Business Impact: [KPIs]
```

**2. TODO.md**

```markdown
# Project Tasks: [Project Name]

## Phase 1: Foundation

### High Priority
- [ ] Task 1: [Description] (Estimated: 8h, Complexity: Medium)
- [ ] Task 2: [Description] (Estimated: 12h, Complexity: High)

### Medium Priority
- [ ] Task 3: [Description] (Estimated: 4h, Complexity: Low)

### Low Priority
- [ ] Task 4: [Description] (Estimated: 6h, Complexity: Medium)

## Dependencies
- Task 2 depends on Task 1
- Task 3 can run in parallel with Task 1

## Assignment Recommendations
- Task 1: Builder Agent (database expertise)
- Task 2: Builder Agent (API development)
```

**3. ARCHITECTURE.md**

```markdown
# Architecture: [Project Name]

## System Overview

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │─────▶│   API GW    │─────▶│  Service 1  │
│ (Web/Mobile)│      │  (Gateway)  │      │  (Business) │
└─────────────┘      └─────────────┘      └─────────────┘
                            │                     │
                            │                     ▼
                            │              ┌─────────────┐
                            │              │  Database   │
                            │              │ (Primary)   │
                            │              └─────────────┘
                            ▼
                     ┌─────────────┐
                     │  Service 2  │
                     │   (Async)   │
                     └─────────────┘
```

## Component Interactions

### Client → API Gateway
- Protocol: HTTPS/REST
- Authentication: JWT tokens
- Rate Limiting: 100 req/min per user

### API Gateway → Services
- Protocol: gRPC / REST
- Service Discovery: [Method]
- Load Balancing: [Strategy]

## Data Flow Patterns

### Write Path
1. Client sends request to API Gateway
2. Gateway validates JWT token
3. Request routed to appropriate service
4. Service validates business rules
5. Service writes to database
6. Async notification sent if needed
7. Response returned to client

### Read Path
1. Client requests data
2. Check cache (Redis)
3. If miss, query database
4. Transform and return data
5. Update cache for future requests

## Scalability Considerations

### Horizontal Scaling
- Stateless services behind load balancer
- Database read replicas for read-heavy workloads
- Cache layer (Redis/Memcached) to reduce DB load

### Vertical Scaling
- Database can scale up to handle write load
- Background workers for async processing

### Bottlenecks
- Primary database writes (mitigated by caching)
- Third-party API rate limits (mitigated by queuing)

## Failure Modes and Resilience

### Database Failure
- Impact: Service degradation
- Mitigation: Read replicas, automatic failover
- Recovery Time: < 5 minutes

### Service Failure
- Impact: Partial functionality loss
- Mitigation: Circuit breakers, graceful degradation
- Recovery Time: Automatic restart

### Third-Party API Failure
- Impact: Feature unavailable
- Mitigation: Queue requests, retry with backoff
- Recovery Time: When API recovers
```

**4. TECH_STACK.md**

```markdown
# Technology Stack: [Project Name]

## Frontend

### Framework: React
**Rationale**:
- Large ecosystem and community support
- Component-based architecture aligns with our design
- Strong TypeScript support for type safety
- Team has existing expertise

**Alternatives Considered**:
- Vue.js: Simpler but smaller ecosystem
- Angular: Too heavyweight for our needs
- Svelte: Less mature ecosystem

### State Management: Redux Toolkit
**Rationale**:
- Predictable state updates
- Time-travel debugging
- Middleware for async operations

## Backend

### Framework: Node.js + Express
**Rationale**:
- JavaScript across stack reduces context switching
- Excellent async I/O performance
- Rich ecosystem of packages
- Fast development cycle

**Alternatives Considered**:
- Python/Django: Slower for I/O-heavy operations
- Java/Spring: More verbose, longer build times
- Go: Team unfamiliar, learning curve

### Database: PostgreSQL
**Rationale**:
- ACID compliance for data integrity
- Rich querying capabilities (JSON, full-text search)
- Proven scalability
- Open source with strong community

**Schema Design**:
- Relational model for core entities
- JSONB columns for flexible metadata
- Indexes on frequently queried fields

## Infrastructure

### Hosting: AWS
**Services Used**:
- EC2: Application servers
- RDS: Managed PostgreSQL
- S3: Static assets and backups
- CloudFront: CDN for global distribution
- Lambda: Serverless background tasks

**Rationale**:
- Mature ecosystem with comprehensive services
- Auto-scaling capabilities
- Global infrastructure
- Team familiarity

### Container Orchestration: Kubernetes
**Rationale**:
- Declarative configuration
- Automatic scaling and healing
- Platform-agnostic (can migrate from AWS)

### CI/CD: GitHub Actions
**Rationale**:
- Integrated with repository
- Free for public repos, affordable for private
- YAML configuration versioned with code

## Third-Party Services

### Authentication: Auth0
**Rationale**:
- Proven security
- Multiple auth providers (OAuth, SAML)
- Reduces development effort

### Monitoring: Datadog
**Rationale**:
- Comprehensive metrics and logs
- Alerting capabilities
- APM for performance monitoring

### Error Tracking: Sentry
**Rationale**:
- Real-time error notifications
- Source map support
- Issue tracking integration
```

**5. SECURITY.md**

```markdown
# Security Architecture: [Project Name]

## Authentication Strategy

### Method: JWT Tokens
- Access token lifetime: 15 minutes
- Refresh token lifetime: 7 days
- Tokens signed with RS256 (asymmetric)

### Implementation
1. User authenticates with credentials
2. Server issues access + refresh token
3. Client stores tokens securely (httpOnly cookies)
4. Access token used for API requests
5. Refresh token used to obtain new access token

## Authorization Model

### Role-Based Access Control (RBAC)
**Roles**:
- Admin: Full system access
- Manager: Department-level access
- User: Personal data access only
- Guest: Read-only public data

**Permission Checking**:
- Middleware validates JWT and extracts role
- Route handlers check required permissions
- Database queries filtered by user context

## Data Encryption

### At Rest
- Database: AWS RDS encryption with KMS
- Backups: S3 server-side encryption
- PII fields: Application-level encryption (AES-256)

### In Transit
- All API traffic over HTTPS (TLS 1.3)
- Internal services use mutual TLS
- Database connections encrypted

## Secrets Management
- Environment variables for non-sensitive config
- AWS Secrets Manager for sensitive credentials
- Rotation policy: Every 90 days
- Access audited and logged

## Compliance Requirements

### GDPR
- User data export capability
- Right to deletion implementation
- Consent tracking
- Data processing agreements with third parties

### Security Testing Plan
- Automated SAST scans on every PR
- Dependency vulnerability scanning (Dependabot)
- Penetration testing: Quarterly
- Security audit: Annually
```

**Step 1.3: Handoff to Builder**

```markdown
---
TO: Builder (or use builder-role-skill)
PHASE: Phase 1 - Foundation
PRIORITY: High
SCOPE: Database schema and authentication service
REFERENCE_DOCS:
  - DEVELOPMENT_PLAN.md (Section: Component Breakdown)
  - ARCHITECTURE.md (Section: Data Model Design)
  - SECURITY.md (Section: Authentication Strategy)
ACCEPTANCE_CRITERIA:
  - Database schema implements all entities
  - Authentication endpoints functional
  - JWT token generation/validation working
  - Unit tests coverage >= 90%
DEPENDENCIES: None (starting point)
---
```

---

### Phase 2: Existing Codebase Analysis

Evaluate and improve existing system architectures.

**Step 2.1: Discovery Phase**

```bash
# Examine project structure
find . -type f \( -name "*.js" -o -name "*.py" -o -name "*.java" \) | head -50

# Review dependencies
cat package.json 2>/dev/null || cat requirements.txt 2>/dev/null || cat pom.xml 2>/dev/null

# Analyze git activity
git log --oneline --since="6 months ago" --pretty=format:"%h %s" | head -20

# Identify most changed files (potential hotspots)
git log --since="6 months ago" --name-only --pretty=format: | sort | uniq -c | sort -rg | head -20
```

**Step 2.2: Analysis Framework**

Evaluate each dimension and rate 1-5 (5=excellent):

| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Organization | | Modularity, separation of concerns |
| Documentation | | README, API docs, inline comments |
| Testing | | Coverage, test quality, CI integration |
| Security | | Auth, data protection, vulnerability scan |
| Performance | | Response times, resource usage, optimization |
| Scalability | | Horizontal/vertical scaling capability |
| Maintainability | | Code complexity, technical debt |
| Modern Practices | | Version control, CI/CD, code review |

**Step 2.3: Recommendation Report**

Create **ARCHITECTURE_REVIEW.md**:

```markdown
# Architecture Review: [Project Name]

## Executive Summary
[1-2 paragraphs summarizing current state and key recommendations]

## Current State Assessment

### Strengths
1. **[Aspect]**: [What's working well and why]
2. **[Aspect]**: [What's working well and why]

### Critical Issues
1. **[Issue]**:
   - Impact: [Business/Technical impact]
   - Risk: [High/Medium/Low]
   - Recommendation: [What to do]

### Architecture Scores

| Dimension | Score | Status | Priority |
|-----------|-------|--------|----------|
| Code Organization | 3/5 | ⚠️ Needs Improvement | High |
| Documentation | 2/5 | ❌ Critical | High |
| Testing | 4/5 | ✅ Good | Medium |
| Security | 3/5 | ⚠️ Needs Improvement | High |
| Performance | 4/5 | ✅ Good | Low |
| Scalability | 2/5 | ❌ Critical | High |
| Maintainability | 3/5 | ⚠️ Needs Improvement | Medium |
| Modern Practices | 4/5 | ✅ Good | Low |

## Recommended Improvements (Prioritized)

### Priority 1: Critical (Must Address)
1. **Improve Scalability**
   - Current Issue: Single database instance, no caching
   - Recommendation: Implement read replicas + Redis caching layer
   - Effort: 2-3 weeks
   - Benefit: Handle 10x traffic without degradation

2. **Address Documentation Gaps**
   - Current Issue: No API documentation, minimal inline comments
   - Recommendation: Generate OpenAPI specs, add JSDoc comments
   - Effort: 1 week
   - Benefit: Onboarding time reduced by 50%

### Priority 2: Important (Should Address)
1. **Refactor Monolithic Service**
   - Current Issue: Single service handles all business logic
   - Recommendation: Extract payment processing to separate service
   - Effort: 3-4 weeks
   - Benefit: Independent scaling, clearer boundaries

### Priority 3: Nice to Have
1. **Modernize Frontend Build**
   - Current Issue: Using Webpack 4
   - Recommendation: Migrate to Vite for faster builds
   - Effort: 1 week
   - Benefit: Development build time from 45s to 5s

## Migration/Refactoring Strategy

### Phase 1: Foundation (Month 1)
- Implement caching layer
- Add comprehensive logging
- Create API documentation

### Phase 2: Scaling Improvements (Month 2)
- Set up database read replicas
- Implement connection pooling
- Add load balancer

### Phase 3: Service Extraction (Month 3-4)
- Extract payment service
- Implement service mesh
- Update deployment pipeline

## Risk Mitigation

### Risk: Database Migration Downtime
- Mitigation: Use blue-green deployment with gradual traffic shift
- Fallback: Immediate rollback capability

### Risk: Breaking Changes During Refactoring
- Mitigation: Comprehensive test suite before starting
- Fallback: Feature flags to disable new code paths

## Estimated Effort and Timeline

| Phase | Duration | Team Size | Risk Level |
|-------|----------|-----------|------------|
| Phase 1 | 1 month | 2 engineers | Low |
| Phase 2 | 1 month | 2 engineers | Medium |
| Phase 3 | 2 months | 3 engineers | High |

**Total**: 4 months with 2-3 engineers
```

**Step 2.4: Handoff**

Assign specific tasks to appropriate skills:

```markdown
---
TO: Builder (or use builder-role-skill)
TASK: Implement Redis caching layer
REFERENCE: ARCHITECTURE_REVIEW.md (Priority 1, Item 1)
ESTIMATED_EFFORT: 2 weeks
---

---
TO: Validator (or use validator-role-skill)
TASK: Security audit of authentication flow
REFERENCE: ARCHITECTURE_REVIEW.md (Security Score: 3/5)
---

---
TO: Scribe (or use scribe-role-skill)
TASK: Generate OpenAPI documentation
REFERENCE: ARCHITECTURE_REVIEW.md (Priority 1, Item 2)
---
```

---

## Output Standards

### Planning Documents Must Include

1. **Rationale Section**: Explain WHY decisions were made
2. **Alternatives Considered**: Document rejected approaches and reasoning
3. **Trade-offs**: Explicitly state compromises and limitations
4. **Success Metrics**: Define how to measure if architecture achieves goals
5. **Risk Register**: Identify potential issues and mitigation strategies
6. **Versioning**: Date and version all documents

### Communication Style

- Use professional, precise technical language
- Avoid jargon without explanation
- Provide examples and diagrams (ASCII art if needed)
- Structure with clear headers and sections
- Cross-reference related documents

---

## Quality Assurance

### Self-Validation Checklist

- [ ] All planning documents created and consistent
- [ ] Technology choices justified with reasoning
- [ ] System can scale to expected load (with calculations)
- [ ] Security considerations addressed at architecture level
- [ ] Development phases are realistic and achievable
- [ ] Clear handoff points defined
- [ ] No implementation details mixed into architecture
- [ ] Budget and timeline constraints acknowledged

### Red Flags to Avoid

- Over-engineering for current requirements
- Technology selection based on trends vs. team capabilities
- Ignoring operational/maintenance complexity
- Insufficient security consideration
- Unrealistic timeline expectations
- Missing stakeholder communication plan

---

## Collaboration Patterns

### With Builder (or builder-role-skill)

```markdown
Handoff Message Format:
---
TO: Builder
PHASE: [Phase name]
PRIORITY: [High/Medium/Low]
SCOPE: [Brief description]
REFERENCE_DOCS:
  - DEVELOPMENT_PLAN.md (Section X)
  - ARCHITECTURE.md (Component Y)
ACCEPTANCE_CRITERIA:
  - [Specific, measurable criteria]
DEPENDENCIES: [Prerequisites]
---
```

### With Validator (or validator-role-skill)

- Request security architecture review
- Define testing strategy and coverage expectations
- Specify performance benchmarks

### With DevOps (or devops-role-skill)

- Provide infrastructure requirements
- Define environment configurations
- Specify monitoring and alerting needs

### With Scribe (or scribe-role-skill)

- Identify documentation gaps
- Request architecture diagrams
- Define documentation structure

---

## Emergency Protocols

### When Requirements Are Unclear

1. Generate a **REQUIREMENTS_QUESTIONS.md** document
2. Block planning until clarification received
3. Do NOT make assumptions that affect core architecture

### When Technology Constraints Conflict

1. Document the conflict explicitly
2. Present multiple architecture options with trade-offs
3. Request stakeholder decision
4. Proceed only after explicit direction

### When Timeline Is Unrealistic

1. Calculate realistic effort estimates
2. Present risk analysis of compressed timeline
3. Propose phase-based delivery approach
4. Escalate to project leadership if needed

---

## Examples

### Example 1: Greenfield E-Commerce Platform

**Task**: Design architecture for new e-commerce platform

```markdown
## Key Decisions

### Technology Stack
- Frontend: React (team expertise)
- Backend: Node.js + Express (async I/O for concurrent users)
- Database: PostgreSQL (ACID for orders)
- Cache: Redis (session + product catalog)

### Architecture Pattern
- Microservices for:
  - User service
  - Product catalog service
  - Order processing service
  - Payment service

### Scalability Strategy
- Horizontal scaling behind load balancer
- Database read replicas for product searches
- CDN for static assets

**Result**: 5 comprehensive planning documents created, ready for builder implementation
```

### Example 2: Legacy System Modernization

**Task**: Evaluate 5-year-old monolithic PHP application

```markdown
## Analysis Results

### Current State
- Score: 2.8/5 overall
- Critical Issues: No caching, single database, no CI/CD

### Recommendations
1. Add Redis caching (2 weeks, high priority)
2. Set up CI/CD pipeline (1 week, high priority)
3. Extract payment module to service (4 weeks, medium priority)

### Migration Strategy
- Strangler Fig pattern over 6 months
- Zero-downtime migration approach

**Result**: Prioritized roadmap with risk mitigation, ready for phased execution
```

---

## Resources

### Templates

- `resources/DEVELOPMENT_PLAN_template.md` - Comprehensive planning template
- `resources/ARCHITECTURE_template.md` - Architecture documentation template
- `resources/TECH_STACK_template.md` - Technology decision template
- `resources/ARCHITECTURE_REVIEW_template.md` - Codebase analysis template

### Scripts

- `scripts/analyze_codebase.sh` - Automated codebase analysis
- `scripts/dependency_audit.sh` - Technology stack inventory

---

## References

- [Agent Skills vs. Multi-Agent](../../docs/best-practices/09-Agent-Skills-vs-Multi-Agent.md)
- [Architecture Decision Records](https://adr.github.io/)
- [C4 Model for Architecture Diagrams](https://c4model.com/)

---

**Version**: 1.0.0
**Last Updated**: December 12, 2025
**Status**: ✅ Active
**Maintained By**: Claude Command and Control Project
