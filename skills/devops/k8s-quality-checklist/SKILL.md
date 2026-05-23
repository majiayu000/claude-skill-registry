---
name: k8s-quality-checklist
description: Review Kubernetes operators for safety, CRD quality, webhook correctness, RBAC scope, controller behavior, and local dev-loop readiness. Use when Codex is auditing an operator implementation or deciding whether a change is ready for testing or release.
---

# Kubernetes Operator Quality Checklist

Use this checklist before major iterations, demos, releases, or code review sign-off.

## Safety

- Target cluster is `kind-*` or another explicitly approved dev cluster.
- Leader election is disabled in the dev overlay.
- The dev manager runs a single replica.
- Webhook timeouts are short in dev.
- Mutations are limited to owned or explicitly allowed resources.
- Destructive operations require explicit confirmation.

## CRD Quality

- Structural schema is valid and complete.
- Required fields are marked correctly.
- Sensible defaults exist for optional fields.
- Status subresource is enabled when status is used.
- Printer columns and categories improve operability.
- Validation markers enforce the stated invariants.

## Webhook Quality

- Validating webhook covers invariants and immutable fields.
- Mutating webhook only defaults safe optional fields.
- Cross-field validation exists where needed.
- Error messages are clear.
- Failure policy matches the environment.
- Certificates, mounts, services, and endpoints are present.

## RBAC Quality

- Verbs are minimal.
- Resources are minimal.
- Cluster-wide permissions are justified.
- Service accounts are dedicated.

## Controller Quality

- Reconcile logic is idempotent.
- Owner references are set correctly.
- Finalizers exist for cleanup paths.
- Status conditions use standard concepts such as `Ready`, `Progressing`, and `Degraded`.
- Events are recorded for meaningful state changes.
- Transient failures requeue with backoff.

## Fast Loop Quality

- `make dev` or `tilt up` starts cleanly.
- Local compile succeeds.
- Binary sync and restart work reliably.
- Logs reflect fresh code after edits.
- CRD and webhook changes are applied correctly.

## Test Quality

- Reconcile logic has unit tests.
- Webhooks have envtest or integration coverage.
- Example CR manifests exist for manual checks.
- Error paths and edge cases are covered.
