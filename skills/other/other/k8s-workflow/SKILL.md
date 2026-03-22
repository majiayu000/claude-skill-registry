---
name: k8s-workflow
description: Guide Kubernetes operator development with Kubebuilder, kind, Tilt, and Kustomize. Use when Codex needs to scaffold or iterate on CRDs, controllers, or webhooks; stand up a safe local kind cluster; run a fast operator dev loop; or verify CRDs, pods, and webhook state.
---

# Kubernetes Operator Workflow

Operate in a dev-only posture. Refuse mutating cluster operations unless the current `kubectl` context starts with `kind-`, unless the user explicitly overrides and accepts the risk.

## Quick Start

- Run `scripts/prereqs.sh` from the target repo root to check or install `kind`, `kubectl`, `kustomize`, `tilt`, `go`, and `kubebuilder`.
- Run `scripts/setup-kind.sh [cluster-name]` to create and select a local kind cluster.
- Run `scripts/deploy-dev.sh [config/dev]` to apply the dev overlay.
- Run `scripts/verify-dev.sh [namespace]` to inspect CRDs, pods, webhooks, and recent events.
- Use `references/command-mapping.md` when translating the original Claude plugin commands into Codex actions.

## Required Discovery

Ask these before writing code:

1. CRD purpose
2. Spec fields with types and requiredness
3. Status fields
4. Webhook type: validating, mutating, or both
5. Defaulting rules
6. Validation invariants
7. RBAC scope: namespaced or cluster-scoped
8. Managed child resources
9. Webhook failure policy
10. Safety gates such as annotations or labels

## Build Workflow

1. Scaffold with Kubebuilder:
   - `kubebuilder init --domain <domain> --repo <module>`
   - `kubebuilder create api --group <group> --version v1 --kind <Kind>`
   - `kubebuilder create webhook --group <group> --version v1 --kind <Kind> --defaulting --programmatic-validation`
2. Implement CRD types in `api/v1/*_types.go`.
3. Run `make generate && make manifests`.
4. Implement reconcile logic in `internal/controller/*_controller.go`.
5. Implement defaulting and validation in `api/v1/*_webhook.go`.
6. Add the local dev loop with `$k8s-templates`.
7. Prefer `tilt up` or `make dev` for normal iteration.

## Manual Fallback Cases

Do a manual build, image load, and apply cycle when:

- CRD schema changed
- Dockerfile or base image changed
- Go dependencies changed in a way that affects the container image
- Tilt is not recovering correctly

## Validation

- Verify CRDs are installed.
- Verify manager and webhook pods are healthy.
- Submit a valid sample CR and confirm reconcile activity.
- Submit an invalid CR and confirm webhook rejection.
- Update the target repo `README.md` with a short runbook covering dev, logs, and sample CR usage.

## Safety Notes

- `scripts/context-guard.sh` is the portable version of the plugin preflight guard. Use it as a reference or wrapper before mutating `kubectl`, `helm`, or `kustomize` commands.
- Codex skills do not provide automatic hooks, so apply these guardrails explicitly.
