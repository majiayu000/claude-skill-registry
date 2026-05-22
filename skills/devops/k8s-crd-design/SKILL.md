---
name: k8s-crd-design
description: Design CRD schemas, webhooks, reconcile loops, status models, and RBAC for Kubernetes operators. Use when Codex needs to define or review the API shape and control-plane behavior of a Kubebuilder-style operator.
---

# Kubernetes CRD Design Patterns

Use these patterns when designing and implementing CRDs, webhooks, controllers, and RBAC for Kubernetes operators.

## Problem Framing

Before writing code:

- Summarize the user problem in one sentence.
- List the CRD's top three responsibilities.
- Identify safety risks if the controller misbehaves.

## CRD Schema Design

Propose:

- `spec` fields with types, validation markers, and requiredness
- `status` fields for observed state, conditions, and generation tracking
- default markers for safe optional fields
- validation markers for enum, minimum, pattern, and cross-field rules
- printer columns for useful `kubectl get` output

Enable the status subresource when the CR reports status.

## Webhook Design

### Validating Webhook

- Block invalid creates and updates.
- Enforce immutable fields on update.
- Validate cross-field constraints.
- Return clear, user-facing error messages.

### Mutating Webhook

- Default only safe, optional fields.
- Do not overwrite explicit user input.
- Add only predictable labels or annotations the controller depends on.

### Failure Policy

- Use `Ignore` in local dev if availability matters more than strict enforcement.
- Use `Fail` when the environment requires safety over availability.

## Reconcile Loop

Follow this sequence:

1. Fetch the CR.
2. Handle deletion and finalizers.
3. Compute desired state from the spec.
4. Create, update, or delete owned resources.
5. Update status and conditions.
6. Requeue only when needed.

Keep the reconcile function idempotent and level-triggered.

## RBAC Minimization

Grant only the verbs and resources the controller needs:

- CRD: `get`, `list`, `watch`, `patch`, `update` on status if used
- owned resources: the minimal CRUD verbs actually exercised
- events: `create` and `patch`

Avoid wildcards and cluster-wide scope unless the resource model requires it.

## Test Outline

Minimum coverage:

- table-driven unit tests for reconcile logic
- envtest or equivalent integration tests for webhook validation
- valid and invalid sample CRs for manual verification
