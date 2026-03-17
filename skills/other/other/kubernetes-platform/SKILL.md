---
id: SKL-kubernetes-KUBERNETESPLATFORM
name: Kubernetes Platform
description: 'Platform engineering on Kubernetes is about making the "golden path"
  easy: secure-by-default workloads, consistent delivery via GitOps, and predictable
  operations (capacity, upgrades, incident respons'
version: 1.0.0
status: active
owner: '@cerebra-team'
last_updated: '2026-02-22'
category: Backend
tags:
- api
- backend
- server
- database
stack:
- Python
- Node.js
- REST API
- GraphQL
difficulty: Intermediate
---

# Kubernetes Platform

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Platform engineering on Kubernetes is about making the "golden path" easy: secure-by-default workloads, consistent delivery via GitOps, and predictable operations (capacity, upgrades, incident response).

## Why This Matters
- **Reliability**: self-healing + controlled rollouts reduce incidents
- **Security**: least privilege and isolation by default
- **Developer velocity**: standard templates + paved roads
- **Cost control**: right-sizing and autoscaling without surprises

## Core Concepts & Rules

### 1. Core Principles
- Follow established patterns and conventions
- Maintain consistency across codebase
- Document decisions and trade-offs

### 2. Implementation Guidelines
- Start with the simplest viable solution
- Iterate based on feedback and requirements
- Test thoroughly before deployment


## Inputs / Outputs / Contracts
* **Inputs**:
  - <e.g., env vars, request payload, file paths, schema>
* **Entry Conditions**:
  - <Pre-requisites: e.g., Repo initialized, DB running, specific branch checked out>
* **Outputs**:
  - <e.g., artifacts (PR diff, docs, tests, dashboard JSON)>
* **Artifacts Required (Deliverables)**:
  - <e.g., Code Diff, Unit Tests, Migration Script, API Docs>
* **Acceptance Evidence**:
  - <e.g., Test Report (screenshot/log), Benchmark Result, Security Scan Report>
* **Success Criteria**:
  - <e.g., p95 < 300ms, coverage ≥ 80%>

## Skill Composition
* **Depends on**: None
* **Compatible with**: None
* **Conflicts with**: None
* **Related Skills**: None

## Quick Start
#

## Assumptions
- Kubernetes cluster is already provisioned (EKS, GKE, AKS, or self-hosted)
- GitOps controller (Argo CD or Flux) is installed and configured
- Basic understanding of Kubernetes concepts (pods, services, deployments)
- Access to cloud provider resources (load balancers, block storage, IAM)
- Team has access to container registry for image storage

## Compatibility
- **Kubernetes**: 1.24+ (Pod Security admission, stable APIs)
- **Argo CD**: 2.5+
- **Flux**: 2.0+
- **Helm**: 3.0+
- **Prometheus**: 2.40+
- **Cloud Providers**: AWS (EKS), GCP (GKE), Azure (AKS)

## Test Scenario Matrix
| Scenario | Input | Expected Output | Verification |
|----------|-------|-----------------|--------------|
| Deploy stateless app | Deployment manifest | Pods running, healthy | `kubectl get pods` |
| Scale deployment | HPA config | Autoscales on load | Load test + metrics |
| Network policy enforcement | NetworkPolicy | Traffic blocked/allowed | `kubectl exec` + curl |
| Secret injection | ExternalSecret | Secrets mounted | `kubectl describe pod` |
| GitOps sync | Git commit | Cluster reconciles | Argo CD UI |
| Pod disruption | Node drain | Pods reschedule | `kubectl cordon` + drain |

## Technical Guardrails
#

## Agent Directives & Error Recovery
*(ข้อกำหนดสำหรับ AI Agent ในการคิดและแก้ปัญหาเมื่อเกิดข้อผิดพลาด)*

- **Thinking Process**: Analyze root cause before fixing. Do not brute-force.
- **Fallback Strategy**: Stop after 3 failed test attempts. Output root cause and ask for human intervention/clarification.
- **Self-Review**: Check against Guardrails & Anti-patterns before finalizing.
- **Output Constraints**: Output ONLY the modified code block. Do not explain unless asked.


## Definition of Done
A Kubernetes platform change is complete when:

- [ ] All manifests are committed to Git with proper versioning
- [ ] GitOps reconciliation shows synced status
- [ ] All pods are running and healthy
- [ ] Health checks (readiness/liveness) are passing
- [ ] Metrics are being collected and visible in dashboards
- [ ] Logs are being aggregated with trace correlation
- [ ] Security policies are in compliance
- [ ] Resource utilization is within expected bounds
- [ ] SLOs are being met or error budget is healthy
- [ ] Runbooks are updated for operational procedures

## Anti-patterns
1. **No requests/limits**: unpredictable scheduling and noisy-neighbor incidents
2. **Hand-applied changes**: `kubectl apply` drift instead of GitOps reconciliation
3. **Flat network**: no NetworkPolicies; lateral movement is trivial
4. **Single replica**: planned/unplanned disruption becomes downtime
5. **Running as root**: wider blast radius on container compromise
6. **Unbounded egress**: data exfiltration paths and surprise costs
7. **Missing probes**: traffic hits pods before they're ready
8. **Treating cluster as product**: no SLOs, no runbooks, no ownership

## Reference Links
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Production Best Practices](https://learnk8s.io/production-best-practices)
- [Kubernetes Patterns](https://k8spatterns.io/)
- [Argo CD Documentation](https://argoproj.github.io/argo-cd/)
- [Flux Documentation](https://fluxcd.io/docs/)
- [Kyverno Policies](https://kyverno.io/policies/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)

## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

