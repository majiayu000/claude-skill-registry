---
name: kubernetes-skill
description: "Prevent Kubernetes hallucinations by diagnosing and fixing failure modes: insecure workload defaults, resource starvation, network exposure, privilege sprawl, fragile rollouts, and API drift. Use when generating, reviewing, refactoring, or migrating manifests, Helm charts, Kustomize overlays, cluster policies, and platform-specific Kubernetes work for EKS, GKE, AKS, OpenShift, GitOps controllers, or observability stacks."
---

# KubeShark: Failure-Mode Workflow for Kubernetes

Run this workflow top to bottom.

## 1) Capture execution context

Record before writing manifests:
- cluster version (e.g. 1.30, 1.31) and distribution (EKS, GKE, AKS, k3s, vanilla)
- target namespace and environment criticality (dev/staging/prod)
- workload type (Deployment, StatefulSet, Job, CronJob, DaemonSet)
- deployment method (raw YAML, Helm, Kustomize, operator-managed)
- policy enforcement (Pod Security Admission level, Kyverno, OPA/Gatekeeper)
- cloud provider and CNI (affects networking, storage classes, load balancers)
- platform controllers/add-ons (GitOps, observability, ingress, service mesh, autoscaling)

If unknown, state assumptions explicitly.

## 2) Diagnose likely failure mode(s)

Select one or more based on user intent and risk:
- insecure workload defaults: missing security contexts, PSS violations, host access
- resource starvation: missing requests/limits, no PDB, scheduling chaos
- network exposure: flat networking, missing policies, wrong Service types, DNS issues
- privilege sprawl: overly permissive RBAC, leaked secrets, excess ServiceAccount rights
- fragile rollouts: misconfigured probes, mutable tags, unsafe update strategies
- API drift: wrong apiVersion, deprecated APIs, schema violations, tool-specific errors

## 3) Load only the relevant reference file(s)

Primary failure-mode references:
- `references/insecure-workload-defaults.md`
- `references/resource-starvation.md`
- `references/network-exposure.md`
- `references/privilege-sprawl.md`
- `references/fragile-rollouts.md`
- `references/api-drift.md`

Supplemental references (only when needed):
- `references/deployment-patterns.md`
- `references/stateful-patterns.md`
- `references/job-patterns.md`
- `references/daemonset-operator-patterns.md`
- `references/security-hardening.md`
- `references/observability.md`
- `references/multi-tenancy.md`
- `references/storage-and-state.md`
- `references/helm-patterns.md`
- `references/kustomize-patterns.md`
- `references/validation-and-policy.md`
- `references/examples-good.md`
- `references/examples-bad.md`
- `references/do-dont-patterns.md`

Conditional Reference Retrieval (CRR) references (load only when the signal is detected):
- `references/conditional/eks-patterns.md` for EKS, AWS, IRSA, EKS Pod Identity, AWS Load Balancer Controller, EBS/EFS CSI, Karpenter
- `references/conditional/gke-patterns.md` for GKE, Autopilot, Workload Identity Federation for GKE, Dataplane V2, GCE Ingress, Config Sync
- `references/conditional/aks-patterns.md` for AKS, Microsoft Entra Workload ID, Azure CNI, AGIC, Azure Disk/File/Blob CSI
- `references/conditional/openshift-patterns.md` for OpenShift, OKD, ROSA, ARO, Routes, SCCs, OLM, `oc`
- `references/conditional/gitops-controllers.md` for Argo CD, ApplicationSet, Flux, GitOps reconciliation, sync waves
- `references/conditional/observability-stacks.md` for Prometheus Operator, ServiceMonitor, PodMonitor, OpenTelemetry, Loki, Grafana

Do not load multiple CRR files unless the task spans multiple detected platforms/tools.

## 4) Propose fix path with explicit risk controls

For each fix, include:
- why this addresses the failure mode
- what could still go wrong at deploy time or runtime
- guardrails (validation commands, policy checks, rollback path)

## 5) Generate implementation artifacts

When applicable, output:
- Kubernetes manifests (YAML with security contexts, resource limits, labels)
- Helm values/templates or Kustomize overlays
- NetworkPolicies, RBAC resources, PodDisruptionBudgets
- Policy rules (Kyverno/OPA) and admission controls

## 6) Validate before finalize

Always provide validation steps tailored to deployment method and risk tier:
- `kubectl apply --dry-run=server` or `kubectl diff`
- `kubeconform` for schema validation against target cluster version
- cross-resource consistency check (label/selector/port alignment)
- policy scan (PSS profile check, Kyverno/OPA audit)
Never recommend direct production apply without reviewed diff and approval.

## 7) Output contract

Return:
- assumptions and cluster version floor
- selected failure mode(s)
- chosen remediation and tradeoffs
- validation/test plan
- rollback/recovery notes (rollout undo, revision history, data safety)
