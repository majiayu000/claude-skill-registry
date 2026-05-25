---
name: platform-engineering
description: Design and implement Internal Developer Platforms (IDPs) with self-service capabilities, golden paths, and developer experience optimization. Covers platform strategy, IDP architecture (Backstage, Port), infrastructure orchestration (Crossplane), GitOps (Argo CD), and adoption patterns. Use when building developer platforms, improving DevEx, or establishing platform teams.
---

# Platform Engineering

## Purpose

Build Internal Developer Platforms (IDPs) that provide self-service infrastructure, reduce cognitive load, and accelerate developer productivity through golden paths and platform-as-product thinking.

Platform engineering represents the evolution beyond traditional DevOps, focusing on creating product-quality internal platforms that treat developers as customers. The discipline addresses the developer productivity crisis where engineers spend 30-40% of time on infrastructure and tooling instead of features.

## When to Use This Skill

Trigger this skill when:
- Building or improving an internal developer platform
- Designing a developer portal (Backstage, Port, or commercial IDP)
- Implementing golden paths and software templates
- Establishing or restructuring a platform engineering team
- Measuring and improving developer experience (DevEx)
- Integrating IDP with infrastructure, CI/CD, observability, or security tools
- Driving platform adoption across an engineering organization
- Assessing platform maturity and identifying capability gaps

## Core Concepts

### Platform as Product

Treat internal platforms with the same rigor as customer-facing products:

**Product Management Approach:**
- Define platform vision, strategy, and roadmap
- Identify developer "customers" and their pain points
- Measure success via adoption metrics, satisfaction surveys, and business impact
- Iterate based on feedback loops and usage analytics
- Balance new capabilities with platform reliability and support

**Key Differences from Traditional DevOps:**
- DevOps focuses on delivery pipelines; platform engineering builds comprehensive developer experiences
- Platform teams operate as product teams (product managers, UX designers, engineers)
- Success measured by developer productivity and satisfaction, not just infrastructure metrics
- Self-service is the primary interface, not ticket queues

### Internal Developer Platform (IDP) Architecture

**Three-Layer Architecture:**

**1. Developer Portal (Frontend)**
- Service catalog: Inventory of services with ownership, dependencies, health status
- Software templates: Project scaffolding with best practices baked in
- Documentation hub: Centralized, searchable, version-controlled docs
- Self-service workflows: Environment provisioning, deployments, access requests

**2. Platform Orchestration (Backend)**
- Infrastructure provisioning: Multi-cloud resource management
- Environment management: Dev, staging, production lifecycle
- Deployment automation: GitOps-based continuous delivery
- Configuration management: Separation of app and infrastructure concerns

**3. Integration Layer (Glue)**
- CI/CD integration: Pipeline visibility and triggering
- Observability: Metrics, logs, traces surfaced in portal
- Security: Vulnerability scanning, policy enforcement, secrets management
- FinOps: Cost visibility, budgets, optimization recommendations

For detailed architecture patterns and component breakdowns, see `references/idp-architecture.md`.

### Golden Paths and Scaffolding

**Golden Path Principle:**
Provide opinionated templates that handle 80% of use cases while allowing escape hatches for the remaining 20%.

**Template Components:**
- Repository structure and boilerplate code
- Infrastructure as code (Kubernetes manifests, Terraform)
- CI/CD pipeline configurations
- Observability instrumentation (metrics, logging, tracing)
- Security configurations (RBAC, network policies, secrets)
- Documentation templates (README, runbooks, architecture diagrams)

**Constraint Mechanisms:**
- Policy-as-code enforcement (OPA, Kyverno) for security and compliance
- Resource limits and quotas to prevent over-provisioning
- Required health checks and observability instrumentation
- Approved base images and dependency scanning

For template design patterns and examples, see `references/golden-paths.md`.

### Developer Experience (DevEx) Optimization

**Cognitive Load Reduction:**
- Abstract infrastructure complexity without hiding necessary details
- Provide sensible defaults with clear override mechanisms
- Use progressive disclosure (simple for common cases, advanced options available)
- Consolidate tooling (single developer portal vs. 15+ separate tools)

**Key Metrics:**

**DORA Metrics:**
- Deployment frequency (how often code reaches production)
- Lead time for changes (commit to production duration)
- Mean time to recovery (MTTR for incidents)
- Change failure rate (percentage of deployments causing incidents)

**SPACE Framework:**
- Satisfaction: Developer happiness via surveys and NPS
- Performance: Throughput and efficiency of work completed
- Activity: Code commits, PRs, deployments (context, not raw counts)
- Communication: Collaboration quality, discoverability
- Efficiency: Minimize interruptions, reduce toil

**Platform-Specific Metrics:**
- Platform adoption rate (percentage of teams using platform)
- Self-service rate (actions completed without platform team tickets)
- Onboarding time (new developer to first production deployment)
- Template usage (which golden paths are adopted)
- Support ticket volume and resolution time

## Platform Maturity Assessment

Assess current platform capabilities using a 5-level maturity model:

**Level 0: Ad-Hoc** - Manual provisioning, no standardization
**Level 1: Basic Automation** - Some IaC and CI/CD, limited self-service
**Level 2: Paved Paths** - Golden path templates, early portal, limited coverage
**Level 3: Self-Service Platform** - Comprehensive portal, 80%+ self-service
**Level 4: Product-Driven Platform** - Data-driven, product team structure, FinOps integration
**Level 5: AI-Augmented Platform** - AI-assisted troubleshooting, predictive optimization

For detailed assessment framework, gap analysis, and improvement roadmap, see `references/maturity-model.md`.

## Decision Frameworks

### Build vs. Buy IDP

**Choose Open Source (Backstage) when:**
- Large enterprise (1000+ engineers)
- Dedicated platform team available (5-10 engineers)
- Deep customization required
- Open-source ecosystem preferred
- Long-term investment (3+ year horizon)

**Choose Commercial IDP (Port, Humanitec, Cortex) when:**
- Mid-size organization (100-1000 engineers)
- Faster time-to-value needed (3-6 months vs. 6-12 months)
- Prefer managed solution with vendor support
- Limited platform engineering resources (<5 engineers)
- Standard use cases (web apps, microservices, CI/CD)

**Choose Hybrid Approach when:**
- Large organization needing both flexibility and speed
- Complex infrastructure requiring orchestration backend
- Want best-in-class portal + orchestration components
- Willing to integrate multiple systems (e.g., Backstage + Humanitec)

For complete decision tree, selection criteria, and ROI calculations, see `references/decision-frameworks.md`.

### Golden Path Design: Flexibility vs. Standardization

**Spectrum of Control:**

**High Standardization (Regulated Industries):**
- Limited technology choices, mandatory templates
- Policy enforcement via admission controllers (OPA, Kyverno)
- Escape hatches require approval process

**Balanced Approach (Recommended for Most):**
- Recommended golden paths (easy, well-documented, supported)
- Alternatives allowed with documentation
- Soft enforcement (defaults + education, not hard blocks)
- Clear ownership for deviations ("deviate and own")

**High Flexibility (Innovative Organizations):**
- Golden paths as suggestions (not requirements)
- Minimal policy enforcement (only critical security)
- "Build it, run it" ownership model

For detailed guidance on choosing the right balance and enforcement strategies, see `references/decision-frameworks.md`.

### Platform Team Structure

**Centralized Model:**
- Single platform team (5-20 engineers) serving entire organization
- Best for: Small to mid-size orgs (100-500 engineers)

**Federated Model:**
- Central team (5-10 engineers) + embedded engineers (1-2 per business unit)
- Best for: Large orgs (500-2000+ engineers), multiple business units

**Hub-and-Spoke Model:**
- Central "hub" team (3-5 engineers) + "spoke" teams contributing plugins
- Best for: Organizations with strong open-source culture

For team sizing, roles, responsibilities, and governance models, see `references/decision-frameworks.md`.

## Tool Recommendations

### Developer Portals

**Backstage** (Open Source, CNCF)
- Trust Score: 78.7/100, 8,876 code snippets
- Software catalog, scaffolder, TechDocs, plugin ecosystem
- Recommended for: Enterprises with platform teams

**Port** (Commercial)
- Managed platform, modern UI/UX, faster time-to-value
- Recommended for: Mid-size orgs (100-1000 engineers)

**Cortex** (Commercial SaaS)
- Enterprise IDP, compliance focus, engineering standards enforcement
- Recommended for: Regulated industries

### Platform Orchestration

**Crossplane** (Open Source, CNCF)
- Trust Score: 67.4/100, universal control plane for multi-cloud
- Kubernetes-native declarative infrastructure
- Recommended for: Multi-cloud abstractions

**Humanitec** (Commercial)
- Platform Orchestrator backend, environment and deployment management
- Recommended for: Complex infrastructure, complements portals

**Terraform Cloud** (Commercial)
- Mature IaC orchestration, workspace management
- Recommended for: Terraform-heavy organizations

### GitOps Continuous Delivery

**Argo CD** (Open Source, CNCF) - **RECOMMENDED**
- Trust Score: 91.8/100 (HIGHEST)
- Declarative GitOps for Kubernetes, multi-cluster management
- Industry-leading documentation and community

**Flux** (Open Source, CNCF)
- Toolkit approach, Kubernetes-native
- Good for: GitOps-native operations

For detailed tool comparisons, integration patterns, and selection criteria, see `references/tool-recommendations.md`.

## Implementation Guides

### Bootstrapping a Platform

**Foundation Phase (Months 1-3):**
1. Define platform vision and form platform team (3-5 members)
2. Interview developers to identify pain points
3. Set up developer portal (Backstage or commercial)
4. Create initial service catalog and first golden path template

**Pilot Phase (Months 4-6):**
1. Select 2-3 pilot teams for white-glove onboarding
2. Rapid iteration based on feedback
3. Expand to 3-5 golden path templates
4. Integrate key tools (CI/CD, monitoring, secrets)

**Expansion Phase (Months 7-12):**
1. Scale to 20-50% of engineering teams
2. Build self-service documentation and training
3. Establish platform SLOs and on-call rotation
4. Internal evangelization (demos, champions program)

**Maturity Phase (Year 2+):**
1. 80%+ adoption across organization
2. Platform team operates as product team
3. Continuous improvement via metrics and feedback
4. AI-assisted capabilities, policy-as-code expansion

For detailed implementation steps and bootstrapping code, see `references/implementation-backstage.md`.

### Creating Golden Path Templates

**Template Design Process:**
1. Identify most common use case (web app, API, data pipeline)
2. Define opinionated choices (language, framework, deployment pattern)
3. Create repository structure and infrastructure manifests
4. Configure CI/CD pipeline with security scanning
5. Instrument observability and document usage
6. Test with pilot team before broad rollout

**Template Categories:**
- Full-stack web application (backend API + frontend + database)
- Data pipeline (ETL/ELT with orchestration)
- Machine learning service (model serving, monitoring)
- Event-driven microservice (message broker integration)
- Scheduled job (cron jobs, batch processing)

For template examples, scaffolding code, and customization patterns, see `references/golden-paths.md` and `examples/` directory.

### Driving Platform Adoption

**Evangelization Strategies:**
- Showcase pilot team successes (internal blog posts, demos)
- Lunch-and-learns on platform capabilities
- Internal champions program (power users helping peers)
- Office hours and Slack/Teams support channels

**Incentive Alignment:**
- Make platform easier than alternatives (golden paths are "paved roads")
- Integrate with workflows developers already use
- Provide immediate value (faster onboarding, better visibility)
- Celebrate early adopters, showcase their successes

For adoption metrics, tracking dashboards, and success patterns, see `references/maturity-model.md`.

## Quick Reference

### Platform Engineering Checklist

**Strategy and Vision:**
- [ ] Platform vision and charter documented
- [ ] Platform team formed with clear roles
- [ ] Developer pain points identified via interviews
- [ ] Success metrics defined (DORA, SPACE, adoption)

**IDP Foundation:**
- [ ] Developer portal deployed (Backstage, Port, or commercial)
- [ ] Service catalog established (ownership, dependencies, health)
- [ ] First golden path template created and validated
- [ ] Documentation hub accessible to all engineers

**Self-Service Capabilities:**
- [ ] Environment provisioning (dev, staging, production)
- [ ] Deployment automation (GitOps with Argo CD or Flux)
- [ ] CI/CD integration visible in portal
- [ ] Observability dashboards per-service

**Security and Compliance:**
- [ ] Policy-as-code enforcement (OPA, Kyverno)
- [ ] Secrets management integrated (Vault, cloud providers)
- [ ] Vulnerability scanning in pipelines
- [ ] RBAC and access controls configured

**Operations and Support:**
- [ ] Platform SLOs defined and monitored
- [ ] Support channels established (Slack, office hours)
- [ ] Incident response playbooks documented
- [ ] Feedback loops and usage analytics in place

### Common Pitfalls

**Building Too Much Upfront:**
- Start small (1 golden path, pilot team) and iterate
- Avoid "boil the ocean" syndrome

**Ignoring Developer Feedback:**
- Establish continuous feedback loops, not just quarterly surveys

**Over-Standardization:**
- Provide clear escape hatches for advanced use cases

**Under-Measuring Success:**
- Track DORA metrics, satisfaction surveys, self-service rates

**Treating Platform as IT Project:**
- Platform engineering is product development, not infrastructure provisioning
- Requires product managers, UX designers, customer focus

## Integration with Other Skills

**Related Skills:**

- `kubernetes-operations`: Cluster operations, namespace management, RBAC, network policies
- `infrastructure-as-code`: Terraform, Pulumi for infrastructure provisioning integrated with platform
- `gitops-workflows`: GitOps principles, Argo CD / Flux implementation patterns
- `building-ci-pipelines`: CI/CD pipeline design integrated into platform templates
- `security-hardening`: Security best practices enforced through golden paths
- `secret-management`: Secrets management integrated into platform (Vault, cloud providers)
- `observability`: Monitoring, logging, tracing integrated into developer portal

**Cross-Skill Workflows:**

**Platform Bootstrapping:**
1. Use `infrastructure-as-code` to provision platform infrastructure
2. Use `kubernetes-operations` to configure clusters
3. Deploy developer portal (Backstage) on platform infrastructure
4. Integrate `gitops-workflows` (Argo CD) for continuous delivery
5. Add `observability` integrations (Prometheus, Grafana plugins)

**Golden Path Creation:**
1. Design template based on common use case
2. Use `building-ci-pipelines` patterns for CI/CD configuration
3. Apply `security-hardening` best practices (SAST, container scanning)
4. Integrate `secret-management` (Vault, encrypted configs)
5. Add `observability` instrumentation (metrics, logging, tracing)

## Example Use Cases

### Use Case 1: E-Commerce Platform Team

**Context:** 300-engineer e-commerce company, microservices architecture, manual provisioning causing bottlenecks.

**Approach:** Deploy Backstage, create 3 golden paths, integrate Argo CD, pilot with 3 teams, expand to 20 teams over 6 months.

**Results:** Onboarding time 2 days → 2 hours, deployment frequency 2x/week → 10x/day, developer NPS +35.

### Use Case 2: Financial Services Platform

**Context:** 1500-engineer bank, strict compliance, legacy infrastructure, fragmented tooling.

**Approach:** Adopt Port (commercial), high standardization golden paths, OPA Gatekeeper, federated model, Terraform Cloud.

**Results:** Compliance audit prep 3 weeks → 3 days, infrastructure drift incidents 90% reduction, per-service cost attribution.

### Use Case 3: Startup Platform

**Context:** 50-engineer startup, rapid growth, need fast developer onboarding.

**Approach:** Lightweight Backstage (2 engineers), 2 golden paths, GitHub Actions, PaaS infrastructure (Fly.io), documentation focus.

**Results:** New engineer to production 1 day (vs. 2 weeks), 100% self-service, 2 engineers supporting 50 developers.

For code examples and template structures, see `examples/` directory.
