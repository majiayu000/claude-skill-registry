---
name: platform-engineering
description: Provides platform engineering best practices for Internal Developer Platforms (IDPs), golden paths, service catalogs, and developer experience. Use when building developer platforms, configuring Backstage, designing self-service workflows, or when user mentions 'platform engineering', 'backstage', 'golden path', 'IDP', 'developer portal', 'service catalog', 'DevEx', 'platform team', 'self-service'.
---

# Platform Engineering

Best practices for building Internal Developer Platforms (IDPs) that reduce cognitive load, accelerate delivery, and create golden paths for development teams.

## IDP Architecture Layers

A well-designed IDP separates concerns into distinct layers. Each layer abstracts complexity from the one above it.

```
Developer Interface (Portal / CLI / API)
        |
  Orchestration Layer (Workflows, Templates, Scaffolding)
        |
  Integration Layer (APIs, Plugins, Connectors)
        |
  Resource Layer (Infrastructure, Services, Tools)
```

| Layer | Purpose | Components | Owned By |
|-------|---------|------------|----------|
| Developer Interface | Self-service entry point | Backstage portal, CLI tools, API gateway | Platform team |
| Orchestration | Workflow automation, templating | Scaffolder, Terraform modules, Crossplane | Platform team |
| Integration | Connect tools and services | Backstage plugins, API adapters, webhooks | Platform + tool owners |
| Resource | Actual infrastructure and services | Kubernetes, databases, CI/CD, monitoring | Infrastructure team |
| Governance | Policy enforcement and compliance | OPA, Kyverno, cost policies, security scans | Security + platform team |

## Platform Team Topology and Responsibilities

### Team Structure

| Role | Responsibility | Focus Area |
|------|---------------|------------|
| Platform Product Manager | Roadmap, prioritization, user research | Developer needs, adoption metrics |
| Platform Engineer | IDP core, golden paths, automation | Infrastructure abstraction, tooling |
| Developer Advocate | Documentation, onboarding, feedback loops | DevEx, training, communication |
| SRE/Reliability Lead | Platform reliability, SLOs, incident response | Uptime, performance, observability |
| Security Engineer | Policy-as-code, compliance automation | Guardrails, scanning, access control |

### Interaction Model

```
Stream-Aligned Teams (consumers)
        |
        | self-service requests
        v
Platform Team (enablers)
        |
        | golden paths, templates, APIs
        v
Infrastructure / Cloud (resources)
```

Platform teams operate as **enabling teams** (Team Topologies model). They reduce cognitive load on stream-aligned teams by providing curated, opinionated abstractions.

## Backstage: Service Catalog and Developer Portal

### catalog-info.yaml -- Service Registration

Every service registers itself in the catalog via a `catalog-info.yaml` at the repo root.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: Handles payment processing and refunds
  annotations:
    github.com/project-slug: acme-corp/payment-service
    backstage.io/techdocs-ref: dir:.
    pagerduty.com/service-id: P1234ABC
    grafana/dashboard-selector: "payment-service"
  tags:
    - java
    - spring-boot
    - payments
  links:
    - url: https://grafana.internal/d/payments
      title: Dashboard
      icon: dashboard
    - url: https://runbooks.internal/payments
      title: Runbook
      icon: docs
spec:
  type: service
  lifecycle: production
  owner: team-payments
  system: checkout-system
  providesApis:
    - payment-api
  consumesApis:
    - inventory-api
    - notification-api
  dependsOn:
    - resource:payments-db
    - component:auth-service

---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: payment-api
  description: Payment processing REST API
spec:
  type: openapi
  lifecycle: production
  owner: team-payments
  system: checkout-system
  definition:
    $text: ./openapi.yaml
```

### Service Catalog API -- Querying Components

```bash
# List all components owned by a team
curl -s "https://backstage.internal/api/catalog/entities?filter=kind=component,spec.owner=team-payments" \
  -H "Authorization: Bearer $BACKSTAGE_TOKEN" | jq '.[] | {name: .metadata.name, lifecycle: .spec.lifecycle}'

# Find all services consuming a specific API
curl -s "https://backstage.internal/api/catalog/entities?filter=kind=component,spec.consumesApis=payment-api" \
  -H "Authorization: Bearer $BACKSTAGE_TOKEN" | jq '.[] | .metadata.name'

# Get component details with relations
curl -s "https://backstage.internal/api/catalog/entities/by-name/component/default/payment-service" \
  -H "Authorization: Bearer $BACKSTAGE_TOKEN" | jq '{
    name: .metadata.name,
    owner: .spec.owner,
    apis: .spec.providesApis,
    dependencies: .spec.dependsOn
  }'
```

## Golden Path Templates

Golden paths are opinionated, pre-configured templates that encode best practices. They give teams a paved road to production.

### Backstage Software Template

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: spring-boot-service
  title: Spring Boot Microservice
  description: Creates a production-ready Spring Boot service with CI/CD, monitoring, and database
  tags:
    - java
    - spring-boot
    - recommended
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Service Details
      required:
        - name
        - owner
        - description
      properties:
        name:
          title: Service Name
          type: string
          pattern: '^[a-z][a-z0-9-]*$'
          ui:autofocus: true
        owner:
          title: Owner Team
          type: string
          ui:field: OwnerPicker
          ui:options:
            catalogFilter:
              kind: Group
        description:
          title: Description
          type: string
        javaVersion:
          title: Java Version
          type: string
          default: '21'
          enum: ['17', '21']

    - title: Infrastructure
      properties:
        database:
          title: Database
          type: string
          default: postgresql
          enum: [postgresql, mysql, none]
        cacheLayer:
          title: Cache Layer
          type: string
          default: none
          enum: [redis, none]
        messageBroker:
          title: Message Broker
          type: string
          default: none
          enum: [kafka, rabbitmq, none]

  steps:
    - id: fetch-template
      name: Fetch Skeleton
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}
          description: ${{ parameters.description }}
          javaVersion: ${{ parameters.javaVersion }}
          database: ${{ parameters.database }}

    - id: create-repo
      name: Create Repository
      action: publish:github
      input:
        repoUrl: github.com?owner=acme-corp&repo=${{ parameters.name }}
        description: ${{ parameters.description }}
        defaultBranch: main
        protectDefaultBranch: true
        requireCodeOwnerReviews: true

    - id: register-catalog
      name: Register in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps['create-repo'].output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml

    - id: create-argocd-app
      name: Create ArgoCD Application
      action: argocd:create-resources
      input:
        appName: ${{ parameters.name }}
        repoUrl: ${{ steps['create-repo'].output.remoteUrl }}

  output:
    links:
      - title: Repository
        url: ${{ steps['create-repo'].output.remoteUrl }}
      - title: Service in Catalog
        url: ${{ steps['register-catalog'].output.entityRef }}
      - title: CI/CD Pipeline
        url: ${{ steps['create-repo'].output.remoteUrl }}/actions
```

### Golden Path Coverage Matrix

| Category | What the Golden Path Provides | Without Golden Path |
|----------|------------------------------|---------------------|
| Repository | Pre-configured with CI/CD, linting, CODEOWNERS | Manual setup, inconsistent configs |
| CI/CD | Working pipeline from day one | Copy-paste from other repos, broken configs |
| Observability | Dashboards, alerts, SLOs pre-configured | No monitoring until first incident |
| Security | Dependency scanning, SAST, secrets detection | Added retroactively (if at all) |
| Documentation | ADR template, README structure, API docs | Empty README, no docs |
| Infrastructure | Terraform modules, Kubernetes manifests | Hand-crafted YAML, drift between envs |
| Testing | Test framework, coverage gates, fixtures | Ad-hoc test setup, no coverage requirements |

## Developer Experience Metrics (SPACE Framework)

Measure platform effectiveness using the SPACE framework. Never rely on a single dimension.

| Dimension | What It Measures | Example Metrics | Collection Method |
|-----------|-----------------|-----------------|-------------------|
| **S**atisfaction | How developers feel about the platform | NPS score, satisfaction survey (1-5) | Quarterly survey |
| **P**erformance | Outcome of developer work | Deployment frequency, change failure rate | DORA metrics pipeline |
| **A**ctivity | Volume of actions | Scaffolding requests, API calls, portal visits | Platform telemetry |
| **C**ommunication | Quality of collaboration | Time to first response on platform support | Ticketing system |
| **E**fficiency | Flow and minimal friction | Time from commit to deploy, onboarding time | Pipeline metrics |

### Key DevEx Metrics Dashboard

```yaml
# Platform DevEx Metrics -- collected via platform telemetry
metrics:
  onboarding:
    time_to_first_deploy:
      target: "< 2 hours"
      description: "Time from new hire to first successful deployment"
      source: "scaffolder + pipeline timestamps"

    time_to_first_commit:
      target: "< 4 hours"
      description: "Time from repo creation to first merged commit"
      source: "github events"

  self_service:
    template_adoption_rate:
      target: "> 80%"
      description: "Percentage of new services using golden path templates"
      source: "backstage scaffolder logs"

    self_service_resolution_rate:
      target: "> 70%"
      description: "Percentage of requests resolved without platform team intervention"
      source: "support tickets vs portal actions"

  reliability:
    platform_availability:
      target: "99.9%"
      description: "Uptime of developer portal, CI/CD, and artifact registry"
      source: "synthetic monitoring"

    mean_time_to_recovery:
      target: "< 30 minutes"
      description: "Time to restore platform services after incident"
      source: "incident management system"

  delivery:
    deployment_frequency:
      target: "multiple per day per team"
      description: "How often teams deploy to production"
      source: "deployment pipeline events"

    lead_time_for_changes:
      target: "< 1 day"
      description: "Time from commit to production"
      source: "git + pipeline timestamps"
```

## Self-Service Portal Workflow

### Request Flow Architecture

```
Developer submits request via Portal UI
        |
        v
Request Validation (schema check, policy check)
        |
        v
Approval Gate (if required by policy)
        |           |
        | auto      | manual
        v           v
Orchestration Engine (executes workflow)
        |
        +---> Provision Infrastructure (Terraform/Crossplane)
        +---> Configure CI/CD (GitHub Actions / ArgoCD)
        +---> Register in Catalog (Backstage)
        +---> Set Up Monitoring (Grafana / PagerDuty)
        +---> Notify Team (Slack / Email)
        |
        v
Verification (health checks, smoke tests)
        |
        v
Developer notified -- ready to use
```

### Self-Service Capability Matrix

| Capability | Automation Level | Approval Required | Typical Time |
|------------|-----------------|-------------------|--------------|
| Create new service | Fully automated | No | 5 minutes |
| Provision database | Fully automated | No (dev/staging), Yes (prod) | 10 minutes |
| Add CI/CD pipeline | Fully automated | No | 2 minutes |
| Request cloud credentials | Semi-automated | Yes (security review) | 1 hour |
| Create new environment | Fully automated | No (non-prod), Yes (prod) | 15 minutes |
| Add monitoring/alerts | Fully automated | No | 5 minutes |
| Resize infrastructure | Semi-automated | Yes (cost review > threshold) | 30 minutes |
| Decommission service | Automated with safeguards | Yes (owner confirmation) | 10 minutes |

## Platform Engineering Maturity Model

| Level | Name | Characteristics | Capabilities |
|-------|------|----------------|--------------|
| 0 | Ad Hoc | No platform, tribal knowledge | Teams manage their own infra |
| 1 | Reactive | Shared scripts, wiki docs | Basic CI/CD, manual provisioning |
| 2 | Standardized | Golden paths, basic portal | Service templates, catalog, basic self-service |
| 3 | Optimized | Full IDP, metrics-driven | Self-service everything, DevEx metrics, policy-as-code |
| 4 | Strategic | Platform as product, innovation | API-first platform, marketplace, continuous feedback |

### Maturity Assessment Checklist

```
Level 1 --> Level 2:
  [x] Service catalog exists and is maintained
  [x] At least 3 golden path templates available
  [x] Basic developer portal deployed
  [x] CI/CD standardized across teams

Level 2 --> Level 3:
  [x] Self-service for >80% of common requests
  [x] SPACE metrics collected and reviewed monthly
  [x] Policy-as-code enforced (not advisory)
  [x] Platform team has dedicated product manager
  [x] Internal SLOs defined for platform services

Level 3 --> Level 4:
  [x] API-first platform (all capabilities programmable)
  [x] Internal developer marketplace for plugins/extensions
  [x] Continuous developer experience research program
  [x] Platform economics model (cost attribution per team)
  [x] Platform contributes to organizational strategy
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Build it and they will come | No adoption without developer input | Treat platform as product; user research before building |
| Ticket-ops disguised as platform | Self-service portal that just creates tickets | Automate end-to-end; tickets are a smell, not a solution |
| Mandating platform use | Forced adoption breeds resentment and workarounds | Make the golden path the easiest path, not the only path |
| One-size-fits-all templates | Overly rigid templates that don't fit team needs | Composable templates with sensible defaults and escape hatches |
| No feedback loops | Platform team builds in isolation | Regular surveys, office hours, embedded rotations with teams |
| Ignoring developer experience | Technically correct but painful to use | Measure DevEx metrics, optimize for developer happiness |
| Platform team as bottleneck | All changes go through platform team | Self-service with guardrails; teams should not wait on platform |
| Over-abstracting too early | Complex abstraction layers before understanding needs | Start with concrete solutions, abstract when patterns emerge |
| Neglecting documentation | Powerful platform nobody knows how to use | Docs-as-code, TechDocs in Backstage, examples for everything |
| No platform SLOs | Platform reliability treated as best-effort | Define and publish SLOs; platform is a product with SLAs |
| Shadow platforms | Teams build their own tooling around the platform | Understand why and address gaps; shadow platforms reveal unmet needs |
| Gold plating the portal | Spending months on portal UI before delivering value | Ship incrementally; a working CLI beats a beautiful but empty portal |

## Platform Engineering Checklist

- [ ] Platform team established with clear product ownership
- [ ] Developer portal deployed (Backstage or equivalent)
- [ ] Service catalog populated with all production services
- [ ] At least 3 golden path templates available and documented
- [ ] Self-service provisioning for common infrastructure (databases, queues, caches)
- [ ] CI/CD pipelines standardized and available via templates
- [ ] Observability stack integrated (dashboards auto-created with new services)
- [ ] Security scanning built into golden paths (not bolted on after)
- [ ] DevEx metrics defined and collected (SPACE framework dimensions)
- [ ] Feedback mechanism active (surveys, office hours, Slack channel)
- [ ] Platform SLOs defined and monitored
- [ ] Documentation maintained in developer portal (TechDocs)
- [ ] Onboarding time measured and optimized (target: first deploy < 2 hours)
- [ ] Cost visibility per team/service available through platform
- [ ] Platform roadmap published and informed by developer feedback
- [ ] Escape hatches documented for when golden paths don't fit
- [ ] Platform reliability meets or exceeds published SLOs
