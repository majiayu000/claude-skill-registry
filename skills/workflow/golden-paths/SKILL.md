---
name: golden-paths
description: Use when designing standardized development workflows, paved roads, or opinionated defaults. Covers golden path patterns, template design, developer workflow optimization, and guardrails.
allowed-tools: Read, Glob, Grep
---

# Golden Paths

Patterns for designing standardized, opinionated development workflows that make the right way the easy way.

## When to Use This Skill

- Designing standardized developer workflows
- Creating paved roads for common patterns
- Building template-based service creation
- Implementing guardrails with flexibility
- Optimizing developer onboarding
- Reducing cognitive load for developers

## Golden Path Fundamentals

### What is a Golden Path?

```text
Golden Path Definition:
An opinionated, well-supported workflow that makes best practices
the path of least resistance while not blocking alternatives.

Key Characteristics:
┌─────────────────────────────────────────────────────────────┐
│                    GOLDEN PATH                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✓ Opinionated:  Clear decisions made for you               │
│  ✓ Supported:    First-class documentation and tooling      │
│  ✓ Optimized:    Fastest path to production                 │
│  ✓ Maintained:   Kept up-to-date by platform team           │
│  ✓ Escapable:    Can deviate when needed                    │
│                                                              │
│  "Make the right way the easy way"                          │
│                                                              │
│  Golden Path ≠ The Only Path                                │
│  Golden Path = The Recommended Path                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘

vs Paved Road vs Rails:
├── Golden Path: Recommended workflow with alternatives
├── Paved Road: Same concept, Spotify terminology
├── Rails: More rigid, harder to deviate (often negative)
```

### Golden Path vs Custom

```text
Golden Path Benefits:

Developer Time:
├── New service: 15 min (golden) vs 2 days (custom)
├── Setup CI/CD: Automatic vs 4-8 hours
├── Observability: Built-in vs manual integration
└── Security: Automatic vs checklist review

Platform Support:
├── Golden path: Full support, rapid fixes
├── Custom: Best-effort support, lower priority
├── Hybrid: Support for platform components only

Example Journey:

Golden Path:
┌─────────────────────────────────────────────────────────────┐
│ 1. Choose template     → node-api-template                  │
│ 2. Answer questions    → name, team, database?             │
│ 3. Generate repo       → automatic                         │
│ 4. First deployment    → automatic via CI                  │
│ 5. Start coding        → focus on business logic           │
│                                                              │
│ Time: ~15 minutes                                           │
│ Result: Production-ready service                            │
└─────────────────────────────────────────────────────────────┘

Custom Path:
┌─────────────────────────────────────────────────────────────┐
│ 1. Create repo         → manual setup                       │
│ 2. Choose framework    → research options                   │
│ 3. Setup build         → configure bundler/compiler         │
│ 4. Add observability   → integrate logging, metrics         │
│ 5. Security review     → checklist, manual fixes            │
│ 6. Setup CI/CD         → write pipeline config              │
│ 7. Deploy pipeline     → debug issues                       │
│ 8. Documentation       → write from scratch                 │
│                                                              │
│ Time: 2-5 days                                              │
│ Result: May miss best practices                             │
└─────────────────────────────────────────────────────────────┘
```

## Designing Golden Paths

### Identifying Candidates

```text
Golden Path Selection Criteria:

High-Value Candidates:
├── Frequent: Done by many teams regularly
├── Complex: Easy to get wrong
├── Critical: Security/compliance implications
├── Costly: Takes significant time manually
└── Standardizable: Common pattern across teams

Assessment Matrix:
┌────────────────────────────────────────────────────────────┐
│               Frequency                                     │
│            Low          High                                │
│         ┌─────────────┬─────────────┐                      │
│  High   │ Custom      │ GOLDEN PATH │ ← High Impact        │
│         │ Solution    │ PRIORITY    │                      │
│ Impact  ├─────────────┼─────────────┤                      │
│  Low    │ Ignore      │ Document/   │                      │
│         │             │ Automate    │                      │
│         └─────────────┴─────────────┘                      │
└────────────────────────────────────────────────────────────┘

Common Golden Paths:
1. New service creation (by service type)
2. Database provisioning
3. CI/CD pipeline setup
4. Security scanning integration
5. Observability setup
6. Environment creation
7. API development workflow
8. Frontend application setup
```

### Template Design Principles

```text
Template Design:

1. Opinionated Defaults
   ├── Make decisions so developers don't have to
   ├── Choose proven technologies
   ├── Use sensible configurations
   └── Document why choices were made

2. Minimal Required Input
   ├── Service name
   ├── Team/owner
   ├── 1-3 key configuration choices
   └── Everything else has defaults

3. Complete Package
   ┌─────────────────────────────────────────────────────────┐
   │ Template Contents:                                       │
   │                                                          │
   │ Application Layer:                                       │
   │ ├── Application code skeleton                            │
   │ ├── Configuration management                             │
   │ ├── Health check endpoints                               │
   │ └── API documentation setup                              │
   │                                                          │
   │ Quality Layer:                                           │
   │ ├── Unit test framework                                  │
   │ ├── Integration test setup                               │
   │ ├── Linting and formatting                               │
   │ └── Pre-commit hooks                                     │
   │                                                          │
   │ Operations Layer:                                        │
   │ ├── Dockerfile                                           │
   │ ├── Kubernetes manifests                                 │
   │ ├── CI/CD pipeline                                       │
   │ └── Infrastructure as Code                               │
   │                                                          │
   │ Observability Layer:                                     │
   │ ├── Structured logging                                   │
   │ ├── Metrics instrumentation                              │
   │ ├── Distributed tracing                                  │
   │ └── Dashboard templates                                  │
   │                                                          │
   │ Documentation Layer:                                     │
   │ ├── README template                                      │
   │ ├── ADR templates                                        │
   │ ├── Runbook templates                                    │
   │ └── API specification                                    │
   └─────────────────────────────────────────────────────────┘

4. Clear Extension Points
   ├── Where to add business logic
   ├── How to add new endpoints
   ├── How to integrate dependencies
   └── How to customize behavior
```

### Template Architecture

```text
Template Implementation Patterns:

1. Scaffolding/Generation (Backstage, Yeoman)
   Input → Template + Variables → Generated Repo

   Pros: Simple, full control
   Cons: Generated code diverges over time

2. Cookiecutter/Copier
   Template repo → Variable substitution → New repo

   Pros: Easy to maintain templates
   Cons: Post-generation updates hard

3. Base Image/Library Pattern
   ┌─────────────────────────────────────────────────────────┐
   │                Application Code                          │
   │                      │                                   │
   │                      ▼                                   │
   │  ┌─────────────────────────────────────────────────┐    │
   │  │           Company Base Library                   │    │
   │  │  ├── Logging (preconfigured)                    │    │
   │  │  ├── Metrics (preconfigured)                    │    │
   │  │  ├── Tracing (preconfigured)                    │    │
   │  │  ├── HTTP client (with retry)                   │    │
   │  │  └── Health checks (standard)                   │    │
   │  └─────────────────────────────────────────────────┘    │
   │                      │                                   │
   │                      ▼                                   │
   │  ┌─────────────────────────────────────────────────┐    │
   │  │           Company Base Image                     │    │
   │  │  ├── Runtime (Node, Go, .NET)                   │    │
   │  │  ├── Security patches                           │    │
   │  │  └── Standard tooling                           │    │
   │  └─────────────────────────────────────────────────┘    │
   └─────────────────────────────────────────────────────────┘

   Pros: Updates propagate automatically
   Cons: Requires versioning strategy

4. Mono-Repo with Generators
   Centralized templates → Generated into mono-repo

   Pros: Consistency, shared tooling
   Cons: Mono-repo complexity
```

## Guardrails and Flexibility

### Guardrail Design

```text
Guardrails: Automatic enforcement of standards without blocking.

Types of Guardrails:

1. Preventive (Block before it happens)
   ├── Pre-commit hooks
   ├── PR checks
   ├── Template validation
   └── Infrastructure policies

2. Detective (Alert after it happens)
   ├── Compliance scans
   ├── Drift detection
   ├── Audit logs
   └── Security scanning

3. Corrective (Auto-fix issues)
   ├── Auto-formatting
   ├── Auto-remediation
   ├── Self-healing infrastructure
   └── Automated rollbacks

Guardrail Implementation:
┌─────────────────────────────────────────────────────────────┐
│                 DEVELOPMENT LIFECYCLE                        │
│                                                              │
│  Code ──► Commit ──► PR ──► Merge ──► Deploy ──► Production │
│    │        │        │        │         │           │       │
│    ▼        ▼        ▼        ▼         ▼           ▼       │
│ [Lint]  [Pre-    [PR      [Build   [Deploy    [Runtime     │
│ [Format] commit]  checks]  gates]   policies]  monitoring] │
│                                                              │
│  Guardrails at each stage:                                  │
│  ├── IDE: Real-time feedback, auto-fix                      │
│  ├── Commit: Secrets scan, lint                             │
│  ├── PR: Tests, security scan, approval                     │
│  ├── Build: Vulnerability scan, compliance                  │
│  ├── Deploy: Canary, health checks                          │
│  └── Runtime: Anomaly detection, auto-scale                 │
└─────────────────────────────────────────────────────────────┘
```

### Escape Hatches

```text
Escape Hatches: How to deviate from golden path when needed.

Principles:
├── Make deviation possible but intentional
├── Require justification, not approval
├── Don't punish teams for legitimate needs
└── Learn from deviations to improve paths

Escape Hatch Patterns:

1. Documented Exception
   # .platform/exceptions.yaml
   exceptions:
     - rule: must-use-company-base-image
       reason: "ML workload requires specific CUDA version"
       approved-by: platform-team
       expires: 2024-12-31
       review-issue: PLAT-1234

2. Tiered Support
   ┌─────────────────────────────────────────────────────────┐
   │ Tier 1: Golden Path                                      │
   │ - Full support                                           │
   │ - Automatic updates                                      │
   │ - Priority bug fixes                                     │
   │                                                          │
   │ Tier 2: Supported Deviation                              │
   │ - Documented exception                                   │
   │ - Best-effort support                                    │
   │ - Manual updates may be needed                           │
   │                                                          │
   │ Tier 3: Custom                                           │
   │ - Self-supported                                         │
   │ - No guarantees                                          │
   │ - Must meet minimum security standards                   │
   └─────────────────────────────────────────────────────────┘

3. Override Mechanism
   # pipeline.yaml
   lint:
     enabled: true
     override: true  # Skip for this repo
     override-reason: "Legacy code, lint fix scheduled for Q2"
```

## Common Golden Paths

### Service Creation Path

```text
Service Creation Golden Path:

┌─────────────────────────────────────────────────────────────┐
│ Step 1: Select Template                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Available Templates:                                        │
│  ○ REST API (Node.js)     - Standard HTTP API               │
│  ○ REST API (Go)          - High-performance API            │
│  ○ REST API (.NET)        - Enterprise API                  │
│  ● GraphQL Service        - Flexible API layer              │
│  ○ Event Consumer         - Kafka/message processing        │
│  ○ Scheduled Job          - Batch/cron workloads            │
│                                                              │
│  [Continue with GraphQL Service]                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Step 2: Configure Service                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Service Name: _________ (kebab-case, e.g., user-service)   │
│  Owner Team:   [▼ Select team ]                             │
│  Description:  _________________________________________     │
│                                                              │
│  Optional Features:                                          │
│  ☑ Database (PostgreSQL)                                    │
│  ☐ Cache (Redis)                                            │
│  ☑ Message Queue (Kafka consumer)                           │
│  ☐ External API Client                                      │
│                                                              │
│  [Create Service]                                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Step 3: Automatic Setup (60 seconds)                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✓ Repository created         github.com/org/user-service   │
│  ✓ CI/CD pipeline configured  Actions workflow created      │
│  ✓ Dev environment ready      user-service.dev.internal     │
│  ✓ Database provisioned       PostgreSQL on RDS             │
│  ✓ Secrets configured         Vault paths created           │
│  ✓ Monitoring setup           Datadog dashboards created    │
│  ✓ Registered in catalog      Backstage entry created       │
│                                                              │
│  [Open Repository] [View in Catalog] [Start Coding]         │
└─────────────────────────────────────────────────────────────┘
```

### Deployment Path

```text
Deployment Golden Path:

Developer Workflow:
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  1. Developer pushes to feature branch                      │
│     └── Automatic: lint, test, build, security scan         │
│                                                              │
│  2. Developer opens PR                                      │
│     └── Automatic: preview environment, E2E tests           │
│                                                              │
│  3. PR approved and merged                                  │
│     └── Automatic: deploy to staging                        │
│                                                              │
│  4. Staging validation (automated + manual)                 │
│     └── Automatic: smoke tests, synthetic monitoring        │
│                                                              │
│  5. Production deployment                                   │
│     └── Automatic: canary → gradual rollout                 │
│                                                              │
│  No manual steps required for standard deployments          │
└─────────────────────────────────────────────────────────────┘

Pipeline Configuration:
# Comes pre-configured in template
# Developers only modify if needed

deploy:
  staging:
    trigger: merge-to-main
    strategy: rolling
    tests: [smoke, integration]

  production:
    trigger: staging-success
    strategy: canary
    canary-percentage: 5
    canary-duration: 15m
    rollback: automatic
```

## Adoption Strategy

### Rolling Out Golden Paths

```text
Adoption Phases:

Phase 1: Pilot (1-2 teams, 1-2 months)
├── Partner with friendly teams
├── Gather intensive feedback
├── Iterate rapidly
├── Build success stories
└── Document learnings

Phase 2: Early Adopters (5-10 teams, 2-3 months)
├── Expand to interested teams
├── Refine based on feedback
├── Build champions network
├── Create training materials
└── Measure adoption metrics

Phase 3: Early Majority (30-50% teams, 3-6 months)
├── Marketing and communication
├── Training sessions
├── Self-service documentation
├── Deprecate old paths
└── Track DORA metrics

Phase 4: Late Majority (70-90% teams, 6-12 months)
├── Mandate for new services
├── Migration support for existing
├── Advanced features
├── Refinement and optimization
└── Continuous improvement

Adoption Tactics:
├── Make golden path faster than alternatives
├── Provide migration tooling
├── Celebrate early adopters
├── Address blockers quickly
├── Don't force premature adoption
└── Listen to resistors (they find real issues)
```

### Measuring Success

```text
Golden Path Metrics:

Adoption Metrics:
├── % new services using templates
├── % teams with at least one golden path service
├── Template usage by type
├── Deviation rate (why teams don't use)
└── Migration rate (legacy to golden path)

Efficiency Metrics:
├── Time to first deployment (new service)
├── Time to production change
├── PR cycle time
├── Incident resolution time
└── Developer time saved

Quality Metrics:
├── Deployment success rate
├── Security scan pass rate
├── Change failure rate
├── Incident rate (golden vs custom)
└── Compliance audit findings

Satisfaction Metrics:
├── Developer NPS for platform
├── Template satisfaction surveys
├── Support ticket volume
├── Documentation effectiveness
└── Onboarding experience rating
```

## Anti-Patterns

```text
Golden Path Anti-Patterns:

1. "One Golden Path for All"
   ❌ Same template for microservices and ML workloads
   ✓ Multiple paths for different use cases

2. "Rails, Not Paths"
   ❌ Making deviation impossible or punished
   ✓ Deviation possible with justification

3. "Technical Purity Over Practicality"
   ❌ Choosing trendy tech that teams struggle with
   ✓ Use tech teams can actually use

4. "Set and Forget"
   ❌ Creating path once and never updating
   ✓ Continuous improvement based on feedback

5. "Mandate Without Value"
   ❌ Forcing adoption before path is good
   ✓ Make path so good teams want to use it

6. "Complexity Hiding"
   ❌ Hiding all complexity, no learning opportunity
   ✓ Progressive disclosure of complexity

7. "No Escape Hatch"
   ❌ Blocking legitimate deviations
   ✓ Clear process for exceptions
```

## Best Practices

```text
Golden Path Best Practices:

1. Start with Pain Points
   ├── Interview developers about friction
   ├── Measure current time-to-production
   ├── Identify most common tasks
   └── Focus on highest-impact paths first

2. Make Right Way Easy
   ├── Golden path should be faster than alternatives
   ├── Defaults should be secure and compliant
   ├── Documentation integrated into workflow
   └── Errors should guide to solutions

3. Iterate Based on Feedback
   ├── Regular user research
   ├── Fast iteration cycles
   ├── A/B test improvements
   └── Deprecate gracefully

4. Balance Opinionation and Flexibility
   ├── Strong defaults with clear rationale
   ├── Document why choices were made
   ├── Allow overrides with justification
   └── Learn from deviations

5. Invest in Documentation
   ├── Getting started guides
   ├── Decision explanations
   ├── Troubleshooting guides
   └── Migration guides

6. Build Community
   ├── Champions in each team
   ├── Regular office hours
   ├── Contribution guidelines
   └── Celebrate successes
```

## Related Skills

- `internal-developer-platform` - Platform engineering overview
- `self-service-infrastructure` - Infrastructure provisioning patterns
- `design-interview-methodology` - Interview preparation
- `quality-attributes-taxonomy` - Understanding quality requirements
