---
name: ops-devops-platform
description: "Production-grade DevOps and platform engineering patterns: Kubernetes, Terraform, containers, GitOps, CI/CD, observability, incident response, security hardening, and cloud-native operations (AWS, GCP, Azure, Kafka)."
---

# DevOps Engineering — Quick Reference

This skill equips teams with actionable templates, checklists, and patterns for building self-service platforms, automating infrastructure with GitOps, deploying securely with DevSecOps, scaling with Kubernetes, ensuring reliability through SRE practices, and operating production systems with strong observability.

**Modern Best Practices (Jan 2026)**: Kubernetes 1.33+ (supported releases + version skew policy), Docker Engine v27, Terraform 1.x (current stable in 1.14.x), GitOps with Argo CD v3 and Flux v2, OpenTelemetry for traces/metrics/logs, and eBPF-based observability where it meaningfully reduces operational overhead.

---

## Quick Reference

| Task | Tool/Framework | Command | When to Use |
|------|----------------|---------|-------------|
| Infrastructure as Code | Terraform 1.x | `terraform plan && terraform apply` | Provision cloud resources declaratively |
| GitOps Deployment | Argo CD / Flux | `argocd app sync myapp` | Continuous reconciliation, declarative deployments |
| Container Build | Docker Engine v27 | `docker build -t app:v1 .` | Package applications with dependencies |
| Kubernetes Deployment | kubectl / Helm (Kubernetes) | `kubectl apply -f deploy.yaml` / `helm upgrade app ./chart` | Deploy to K8s cluster, manage releases |
| CI/CD Pipeline | GitHub Actions | Define workflow in `.github/workflows/ci.yml` | Automated testing, building, deploying |
| Security Scanning | Trivy / Falco | `trivy image myapp:latest` | Vulnerability scanning, runtime security |
| Monitoring & Alerts | Prometheus + Grafana | Configure ServiceMonitor and AlertManager | Observability, SLO tracking, incident alerts |
| Load Testing | k6 / Locust | `k6 run load-test.js` | Performance validation, capacity planning |
| Incident Response | PagerDuty / Opsgenie | Configure escalation policies | On-call management, automated escalation |
| Platform Engineering | Backstage / Port | Deploy internal developer portal | Self-service infrastructure, golden paths |

---

## Decision Tree: Choosing DevOps Approach

```text
What do you need to accomplish?
    ├─ Infrastructure provisioning?
    │   ├─ Cloud-agnostic → Terraform (multi-cloud support)
    │   ├─ AWS-specific → CloudFormation or Terraform
    │   ├─ GCP-specific → Deployment Manager or Terraform
    │   └─ Azure-specific → ARM templates or Terraform
    │
    ├─ Application deployment?
    │   ├─ Kubernetes cluster?
    │   │   ├─ Simple deploy → kubectl apply -f manifests/
    │   │   ├─ Complex app → Helm charts
    │   │   └─ GitOps workflow → ArgoCD or FluxCD
    │   └─ Serverless?
    │       ├─ AWS → Lambda + SAM/Serverless Framework
    │       ├─ GCP → Cloud Functions
    │       └─ Azure → Azure Functions
    │
    ├─ CI/CD pipeline setup?
    │   ├─ GitHub-based → GitHub Actions (template-github-actions.md)
    │   ├─ GitLab-based → GitLab CI
    │   ├─ Enterprise → Jenkins or Tekton
    │   └─ Security-first → Add SAST/DAST/SCA scans (template-ci-cd.md)
    │
    ├─ Observability & monitoring?
    │   ├─ Metrics → Prometheus + Grafana
    │   ├─ Distributed tracing → Jaeger or OpenTelemetry
    │   ├─ Logs → Loki or ELK stack
    │   ├─ eBPF-based → Cilium + Hubble (sidecarless)
    │   └─ Unified platform → Datadog or New Relic
    │
    ├─ Incident management?
    │   ├─ On-call rotation → PagerDuty or Opsgenie
    │   ├─ Postmortem → template-postmortem.md
    │   └─ Communication → template-incident-comm.md
    │
    ├─ Platform engineering?
    │   ├─ Self-service → Backstage or Port (internal developer portal)
    │   ├─ Policy enforcement → OPA/Gatekeeper
    │   └─ Golden paths → Template repositories + automation
    │
    └─ Security hardening?
        ├─ Container scanning → Trivy or Grype
        ├─ Runtime security → Falco or Sysdig
        ├─ Secrets management → HashiCorp Vault or cloud-native KMS
        └─ Compliance → CIS Benchmarks, template-security-hardening.md
```

---

## When to Use This Skill

Claude should invoke this skill when users request:

- Platform engineering patterns (self-service developer platforms, internal tools)
- GitOps workflows (ArgoCD, FluxCD, declarative infrastructure management)
- Infrastructure as Code patterns (Terraform, K8s manifests, policy as code)
- CI/CD pipelines with DevSecOps (GitHub Actions, security scanning, SAST/DAST/SCA)
- SRE incident management, escalation, and postmortem templates
- eBPF-based observability (Cilium, Hubble, kernel-level insights, OpenTelemetry)
- Kubernetes operational patterns (day-2 operations, resource management, workload placement)
- Cloud-native monitoring (Prometheus, Grafana, unified observability platforms)
- Team workflow, communication, handover guides, and runbooks

---

## Resources (Best Practices Guides)

Operational best practices by domain:

- **DevOps/SRE Operations**: [resources/devops-best-practices.md](resources/devops-best-practices.md) - Core patterns for safe infrastructure changes, deployments, and incident response
- **Platform Engineering**: [resources/platform-engineering-patterns.md](resources/platform-engineering-patterns.md) - Self-service platforms, golden paths, internal developer portals, policy as code
- **GitOps Workflows**: [resources/gitops-workflows.md](resources/gitops-workflows.md) - Continuous reconciliation, multi-environment promotion, ArgoCD/FluxCD patterns, progressive delivery
- **SRE Incident Management**: [resources/sre-incident-management.md](resources/sre-incident-management.md) - Severity classification, escalation procedures, blameless postmortems, alert correlation, and runbooks
- **Operational Standards**: [resources/operational-patterns.md](resources/operational-patterns.md) - Platform engineering blueprints, CI/CD safety, SLOs, and reliability drills

Each guide includes:
- Checklists for completeness and safety
- Common anti-patterns and remediations
- Step-by-step patterns for safe rollout, rollback, and verification
- Decision matrices (e.g., deployment, escalation, monitoring strategy)
- Real-world examples and edge case handling

---

## Templates (Copy-Paste Ready)

Production templates organized by tech stack (27 templates total):

### AWS Cloud
- [templates/aws/template-aws-ops.md](templates/aws/template-aws-ops.md) - AWS service operations and best practices
- [templates/aws/template-aws-terraform.md](templates/aws/template-aws-terraform.md) - Terraform modules for AWS infrastructure
- [templates/aws/template-cost-optimization.md](templates/aws/template-cost-optimization.md) - AWS cost optimization strategies

### GCP Cloud
- [templates/gcp/template-gcp-ops.md](templates/gcp/template-gcp-ops.md) - GCP service operations
- [templates/gcp/template-gcp-terraform.md](templates/gcp/template-gcp-terraform.md) - Terraform modules for GCP

### Azure Cloud
- [templates/azure/template-azure-ops.md](templates/azure/template-azure-ops.md) - Azure service operations

### Kubernetes
- [templates/kubernetes/template-kubernetes-ops.md](templates/kubernetes/template-kubernetes-ops.md) - Day-to-day K8s operations
- [templates/kubernetes/template-ha-dr.md](templates/kubernetes/template-ha-dr.md) - High availability and disaster recovery
- [templates/kubernetes/template-platform-api.md](templates/kubernetes/template-platform-api.md) - Platform API patterns
- [templates/kubernetes/template-k8s-deploy.yaml](templates/kubernetes/template-k8s-deploy.yaml) - Deployment manifests

### Docker
- [templates/docker/template-docker-ops.md](templates/docker/template-docker-ops.md) - Container build, security, and operations

### Kafka
- [templates/kafka/template-kafka-ops.md](templates/kafka/template-kafka-ops.md) - Kafka cluster operations and streaming

### Terraform & IaC
- [templates/terraform-iac/template-iac-terraform.md](templates/terraform-iac/template-iac-terraform.md) - Infrastructure as Code patterns
- [templates/terraform-iac/template-module.md](templates/terraform-iac/template-module.md) - Reusable Terraform modules
- [templates/terraform-iac/template-env-promotion.md](templates/terraform-iac/template-env-promotion.md) - Environment promotion strategies

### CI/CD Pipelines
- [templates/cicd-pipelines/template-ci-cd.md](templates/cicd-pipelines/template-ci-cd.md) - General CI/CD patterns
- [templates/cicd-pipelines/template-github-actions.md](templates/cicd-pipelines/template-github-actions.md) - GitHub Actions workflows
- [templates/cicd-pipelines/template-gitops.md](templates/cicd-pipelines/template-gitops.md) - GitOps deployment patterns
- [templates/cicd-pipelines/template-release-safety.md](templates/cicd-pipelines/template-release-safety.md) - Safe release practices

### Monitoring & Observability
- [templates/monitoring-observability/template-slo.md](templates/monitoring-observability/template-slo.md) - Service level objectives
- [templates/monitoring-observability/template-alert-rules.md](templates/monitoring-observability/template-alert-rules.md) - Alert configuration
- [templates/monitoring-observability/template-observability-slo.md](templates/monitoring-observability/template-observability-slo.md) - Observability patterns
- [templates/monitoring-observability/template-loadtest-perf.md](templates/monitoring-observability/template-loadtest-perf.md) - Load testing and performance

### Incident Response
- [templates/incident-response/template-postmortem.md](templates/incident-response/template-postmortem.md) - Incident postmortems
- [templates/incident-response/template-runbook-starter.md](templates/incident-response/template-runbook-starter.md) - Runbook starter template
- [templates/incident-response/template-incident-comm.md](templates/incident-response/template-incident-comm.md) - Incident communication
- [templates/incident-response/template-incident-response.md](templates/incident-response/template-incident-response.md) - Incident response procedures

### Security
- [templates/security/template-security-hardening.md](templates/security/template-security-hardening.md) - Security hardening checklists

---

## Navigation

**Resources**
- [resources/operational-patterns.md](resources/operational-patterns.md)
- [resources/sre-incident-management.md](resources/sre-incident-management.md)
- [resources/devops-best-practices.md](resources/devops-best-practices.md)
- [resources/platform-engineering-patterns.md](resources/platform-engineering-patterns.md)
- [resources/gitops-workflows.md](resources/gitops-workflows.md)

**Shared Utilities** (Centralized patterns — extract, don't duplicate)
- [../software-clean-code-standard/utilities/config-validation.md](../software-clean-code-standard/utilities/config-validation.md) — Zod 3.24+, secrets management (Vault, 1Password, Doppler)
- [../software-clean-code-standard/utilities/resilience-utilities.md](../software-clean-code-standard/utilities/resilience-utilities.md) — p-retry v6, circuit breaker, OTel spans
- [../software-clean-code-standard/utilities/logging-utilities.md](../software-clean-code-standard/utilities/logging-utilities.md) — pino v9 + OpenTelemetry integration
- [../software-clean-code-standard/utilities/observability-utilities.md](../software-clean-code-standard/utilities/observability-utilities.md) — OpenTelemetry SDK, tracing, metrics
- [../software-clean-code-standard/utilities/testing-utilities.md](../software-clean-code-standard/utilities/testing-utilities.md) — Test factories, fixtures, mocks
- [../software-clean-code-standard/resources/clean-code-standard.md](../software-clean-code-standard/resources/clean-code-standard.md) — Canonical clean code rules (`CC-*`) for citation

**Templates**
- [templates/incident-response/template-postmortem.md](templates/incident-response/template-postmortem.md)
- [templates/incident-response/template-runbook-starter.md](templates/incident-response/template-runbook-starter.md)
- [templates/incident-response/template-incident-comm.md](templates/incident-response/template-incident-comm.md)
- [templates/incident-response/template-incident-response.md](templates/incident-response/template-incident-response.md)
- [templates/docker/template-docker-ops.md](templates/docker/template-docker-ops.md)
- [templates/security/template-security-hardening.md](templates/security/template-security-hardening.md)
- [templates/azure/template-azure-ops.md](templates/azure/template-azure-ops.md)
- [templates/gcp/template-gcp-terraform.md](templates/gcp/template-gcp-terraform.md)
- [templates/gcp/template-gcp-ops.md](templates/gcp/template-gcp-ops.md)
- [templates/cicd-pipelines/template-release-safety.md](templates/cicd-pipelines/template-release-safety.md)
- [templates/cicd-pipelines/template-gitops.md](templates/cicd-pipelines/template-gitops.md)
- [templates/cicd-pipelines/template-ci-cd.md](templates/cicd-pipelines/template-ci-cd.md)
- [templates/cicd-pipelines/template-github-actions.md](templates/cicd-pipelines/template-github-actions.md)
- [templates/kafka/template-kafka-ops.md](templates/kafka/template-kafka-ops.md)
- [templates/aws/template-aws-terraform.md](templates/aws/template-aws-terraform.md)
- [templates/aws/template-aws-ops.md](templates/aws/template-aws-ops.md)
- [templates/aws/template-cost-optimization.md](templates/aws/template-cost-optimization.md)
- [templates/monitoring-observability/template-slo.md](templates/monitoring-observability/template-slo.md)
- [templates/monitoring-observability/template-loadtest-perf.md](templates/monitoring-observability/template-loadtest-perf.md)
- [templates/monitoring-observability/template-alert-rules.md](templates/monitoring-observability/template-alert-rules.md)
- [templates/monitoring-observability/template-observability-slo.md](templates/monitoring-observability/template-observability-slo.md)
- [templates/kubernetes/template-k8s-deploy.yaml](templates/kubernetes/template-k8s-deploy.yaml)
- [templates/kubernetes/template-platform-api.md](templates/kubernetes/template-platform-api.md)
- [templates/kubernetes/template-kubernetes-ops.md](templates/kubernetes/template-kubernetes-ops.md)
- [templates/kubernetes/template-ha-dr.md](templates/kubernetes/template-ha-dr.md)
- [templates/terraform-iac/template-env-promotion.md](templates/terraform-iac/template-env-promotion.md)
- [templates/terraform-iac/template-iac-terraform.md](templates/terraform-iac/template-iac-terraform.md)
- [templates/terraform-iac/template-module.md](templates/terraform-iac/template-module.md)

**Data**
- [data/sources.json](data/sources.json) — Curated external references

---

## Related Skills

**Operations & Infrastructure:**
- [../qa-resilience/SKILL.md](../qa-resilience/SKILL.md) — Resilience, chaos engineering, and failure handling patterns
- [../data-sql-optimization/SKILL.md](../data-sql-optimization/SKILL.md) — Database tuning, high availability, and migrations
- [../qa-observability/SKILL.md](../qa-observability/SKILL.md) — Monitoring, tracing, profiling, and performance optimization
- [../qa-debugging/SKILL.md](../qa-debugging/SKILL.md) — Production debugging, log analysis, and root cause investigation

**Security & Compliance:**
- [../software-security-appsec/SKILL.md](../software-security-appsec/SKILL.md) — Application-layer security patterns and OWASP best practices

**Software Development:**
- [../software-backend/SKILL.md](../software-backend/SKILL.md) — Service-level design and integration patterns
- [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) — System design, scalability, and architectural patterns
- [../dev-api-design/SKILL.md](../dev-api-design/SKILL.md) — RESTful API design and versioning
- [../git-workflow/SKILL.md](../git-workflow/SKILL.md) — Git branching strategies and CI/CD integration

**Optional: AI/Automation (Related Skills):**
- [../ai-mlops/SKILL.md](../ai-mlops/SKILL.md) — ML model deployment, monitoring, and lifecycle management

---

## Cost Governance & Capacity Planning

**[templates/cost-governance/template-cost-governance.md](templates/cost-governance/template-cost-governance.md)** — Production cost control for cloud infrastructure.

### Key Sections

- **Cost Governance Framework** — Tagging strategy, budget alerts, anomaly detection
- **Cloud Cost Optimization** — Right-sizing, reserved capacity, storage tiering
- **Kubernetes Cost Control** — Resource requests/limits, quotas, autoscaler config
- **Capacity Planning** — Utilization baseline, growth projections, scaling triggers
- **FinOps Practices** — Monthly review agenda, optimization workflow

---

## Do / Avoid

### GOOD: Do

- Tag all resources at creation time
- Set budget alerts before hitting limits
- Review right-sizing recommendations monthly
- Use spot/preemptible for fault-tolerant workloads
- Set Kubernetes resource requests on all pods
- Enable cluster autoscaler with scale-down
- Document capacity planning assumptions
- Run postmortems after every incident

### BAD: Avoid

- Deploying without cost tags
- Running dev resources 24/7
- Over-provisioning "just in case"
- Ignoring reserved capacity opportunities
- Disabling scale-down to "avoid disruption"
- Alert fatigue (too many low-priority alerts)
- Snowflake infrastructure (manual, undocumented)
- "Clickops" drift (changes outside IaC)

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **No tagging** | Can't attribute costs | Enforce tags in CI/CD |
| **Dev runs 24/7** | 70% waste | Scheduled shutdown |
| **Over-provisioned** | Paying for unused capacity | Monthly right-sizing |
| **No reservations** | Paying on-demand premium | 60-70% coverage target |
| **Alert fatigue** | Real issues missed | SLO-based alerting, tuned thresholds |
| **Snowflake infra** | Undocumented, unreproducible | Everything in Terraform/IaC |
| **No postmortems** | Same incidents repeat | Blameless postmortem for every SEV1/2 |

---

## Optional: AI/Automation

> **Note**: AI assists with analysis but cost/incident decisions need human approval.

### Automated Operations

- Unused resource detection and notification
- Right-sizing recommendation generation
- Alert summarization and correlation
- Runbook step suggestions

### AI-Assisted Analysis

- Cost trend prediction
- Incident pattern identification
- Post-mortem theme extraction

### Bounded Claims

- AI recommendations need validation before action
- Automated deletions require approval workflow
- Cost predictions are estimates, not guarantees
- Runbook suggestions need SRE verification

---

## Operational Deep Dives

See [resources/operational-patterns.md](resources/operational-patterns.md) for:
- Platform engineering blueprints and GitOps reconciliation checklists
- DevSecOps CI/CD gates, SLO/SLI playbooks, and rollout verification steps
- Observability patterns (eBPF), incident noise reduction, and reliability drills

---

## External Resources

See [data/sources.json](data/sources.json) for 45+ curated sources organized by tech stack:
- **Cloud Platforms**: AWS, GCP, Azure documentation and best practices
- **Container Orchestration**: Kubernetes, Helm, Kustomize, Docker
- **Infrastructure as Code**: Terraform, CloudFormation, ARM templates
- **CI/CD & GitOps**: GitHub Actions, GitLab CI, Jenkins, ArgoCD, FluxCD
- **Streaming**: Apache Kafka, Confluent, Strimzi
- **Monitoring**: Prometheus, Grafana, Datadog, OpenTelemetry, Jaeger
- **SRE**: Google SRE books, incident response patterns
- **Security**: OWASP DevSecOps, CIS Benchmarks, Trivy, Falco
- **Tools**: kubectl, k9s, stern, Cosign, Syft, Terragrunt

---

*Use this skill as a hub for safe, modern, and production-grade DevOps patterns. All templates and patterns are operational—no theory or book summaries.*
