<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: cloud-native-security
description: >-
  Cloud-native security covering service mesh hardening, Kubernetes admission
  controllers, serverless function misconfiguration, IaC security scanning,
  cloud workload protection, container runtime threats, cloud IAM auditing,
  GitOps security, cloud resource drift detection, logging completeness audits,
  secrets management, and cloud lateral movement detection. Spans AWS, GCP,
  Azure, and multi-cloud Kubernetes environments.
domain: cybersecurity
subdomain: cloud-native-security
tags:
  - kubernetes
  - service-mesh
  - admission-controllers
  - serverless
  - infrastructure-as-code
  - cwpp
  - cloud-iam
  - gitops
  - drift-detection
  - cloud-logging
  - secrets-management
  - lateral-movement
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1190", "T1078.004", "T1580", "T1552.007", "T1021.004", "T1538"]
  nist-csf: ["PR.AC-4", "PR.DS-5", "PR.IP-1", "DE.CM-1", "DE.CM-7"]
  frameworks: ["CIS Kubernetes Benchmark", "CIS AWS Foundations", "NIST SP 800-190", "NSA K8s Hardening Guide"]
---

# Cloud-Native Security

## When to Use

Activate when the operator asks about securing cloud-native architectures —
service meshes, Kubernetes admission control, serverless security, IaC scanning,
CWPP, cloud IAM, GitOps pipelines, drift detection, cloud logging, secrets
management, or lateral movement detection across AWS/GCP/Azure/K8s environments.

Mode: `[MODE: RED]` for cloud attack paths; `[MODE: BLUE]` for cloud defense and detection; `[MODE: ARCHITECT]` for secure cloud-native design.

## Prerequisites

- kubectl configured for target cluster
- AWS CLI / gcloud / az CLI authenticated
- Terraform >= 1.5 or OpenTofu for IaC scanning
- Istio/Linkerd CLI for service mesh operations
- OPA/Gatekeeper or Kyverno for admission control
- Falco or Tetragon for runtime detection

## Quick Reference

| Attack / Control | Command | Context |
|-----------------|---------|---------|
| Mesh mTLS bypass | `istioctl analyze --all-namespaces` | Defensive |
| Admission controller test | `kubectl apply --dry-run=server -f pod.yaml` | Defensive |
| Lambda enumeration | `aws lambda list-functions --region us-east-1` | Offensive |
| IaC scan | `tfsec . --format json` | Defensive |
| Cloud workload scan | `trivy k8s --report summary cluster` | Defensive |
| Container runtime alerts | `falco -r /etc/falco/falco_rules.yaml` | Defensive |
| IAM enumeration | `aws iam get-account-authorization-details` | Offensive |
| GitOps drift check | `argocd app diff myapp` | Defensive |
| Resource drift | `terraform plan -detailed-exitcode` | Defensive |
| CloudTrail gaps | `aws cloudtrail get-trail-status --name default` | Defensive |
| Secrets audit | `kubectl get secrets -A -o json \| jq '.items[].type'` | Offensive |
| Lateral movement | `aws ec2 describe-instances --filters "Name=iam-instance-profile.arn,Values=*"` | Offensive |

## Techniques

| Technique | Description |
|-----------|-------------|
| [securing-service-mesh-configurations](techniques/securing-service-mesh-configurations/) | Harden Istio/Linkerd mTLS, authorization policies, and mesh telemetry |
| [implementing-kubernetes-admission-controllers](techniques/implementing-kubernetes-admission-controllers/) | Deploy OPA/Gatekeeper and Kyverno policies for workload admission |
| [detecting-misconfigured-cloud-functions](techniques/detecting-misconfigured-cloud-functions/) | Find over-permissioned Lambda/Cloud Functions/Azure Functions |
| [auditing-infrastructure-as-code-security](techniques/auditing-infrastructure-as-code-security/) | Scan Terraform/CloudFormation/Pulumi for security misconfigurations |
| [implementing-cloud-workload-protection](techniques/implementing-cloud-workload-protection/) | Deploy CWPP across K8s nodes, VMs, and serverless |
| [detecting-container-runtime-threats](techniques/detecting-container-runtime-threats/) | Falco/Tetragon rules for runtime anomaly detection |
| [auditing-cloud-identity-permissions](techniques/auditing-cloud-identity-permissions/) | Audit IAM roles, policies, and privilege escalation paths |
| [implementing-gitops-security](techniques/implementing-gitops-security/) | Secure ArgoCD/Flux pipelines, RBAC, and supply chain |
| [detecting-cloud-resource-drift](techniques/detecting-cloud-resource-drift/) | Detect unmanaged changes to cloud infrastructure |
| [auditing-cloud-logging-completeness](techniques/auditing-cloud-logging-completeness/) | Verify CloudTrail/GCP Audit/Azure Monitor coverage |
| [implementing-cloud-secrets-management](techniques/implementing-cloud-secrets-management/) | Vault, AWS Secrets Manager, K8s CSI driver integration |
| [detecting-cloud-lateral-movement](techniques/detecting-cloud-lateral-movement/) | Detect cross-account/cross-service lateral movement in cloud |

## Workflow

### 1. Assess Cloud-Native Posture

```bash
# Kubernetes cluster scan
trivy k8s --report summary cluster

# AWS account baseline
aws configservice describe-compliance-by-config-rule --output json

# Terraform state audit
terraform plan -detailed-exitcode -out=plan.tfplan
```

### 2. Harden Admission Control

```bash
# Install Gatekeeper
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml

# Apply constraint templates
kubectl apply -f constraint-templates/
kubectl apply -f constraints/
```

### 3. Runtime Detection

```bash
# Deploy Falco
helm install falco falcosecurity/falco --namespace falco --create-namespace

# Verify rules
falco --list | grep -i cloud
```

### 4. Continuous Compliance

```bash
# IaC scanning in CI
tfsec . --format json --out results.json
checkov -d . --output json > checkov-results.json
```

## Verification

- [ ] Service mesh mTLS enforced (STRICT mode, no PERMISSIVE)
- [ ] Admission controllers block privileged pods in production
- [ ] Serverless functions follow least-privilege IAM
- [ ] IaC scanned in CI/CD — zero HIGH+ findings
- [ ] CWPP deployed on all nodes and workloads
- [ ] Runtime detection rules tuned and alerting
- [ ] Cloud IAM follows least privilege — no wildcard policies
- [ ] GitOps pipelines enforce signed commits and image verification
- [ ] Drift detection runs on schedule with alerts
- [ ] All cloud API actions logged (no blind spots)
- [ ] Secrets managed via Vault/CSI — no hardcoded credentials
- [ ] Lateral movement detection rules deployed in SIEM

## Detection Opportunities

- Service mesh telemetry for unauthorized service-to-service calls
- Admission controller audit logs for denied workload deployments
- CloudTrail/GCP Audit Logs for IAM privilege escalation
- Terraform plan diffs for unauthorized infrastructure changes
- Falco alerts for container escape and runtime anomalies
- SIEM correlation for cross-account lateral movement patterns
