---
name: deployment
description: Build, push, and deploy services via GitOps in this repo. Use when updating images, manifests, or rolling out changes with Argo CD.
---

# Deployment

## Overview

Deploy changes using repo scripts and GitOps manifests in `argocd/`. Scripts build and push images, update manifests, and trigger rollouts.

## When to use

- You changed service code and need a new image.
- You updated manifests or runtime config under `argocd/`.
- You need to roll out or roll back a service quickly and safely.

## Service deploy scripts

Bumba:

```bash
bun run packages/scripts/src/bumba/deploy-service.ts
```

Jangar:

```bash
bun run packages/scripts/src/jangar/deploy-service.ts
```

## Environment overrides

Bumba script supports:

- `BUMBA_IMAGE_REGISTRY`
- `BUMBA_IMAGE_REPOSITORY`
- `BUMBA_IMAGE_TAG`
- `BUMBA_KUSTOMIZE_PATH`
- `BUMBA_K8S_NAMESPACE`
- `BUMBA_K8S_DEPLOYMENT`

Jangar script supports:

- `JANGAR_IMAGE_REGISTRY`
- `JANGAR_IMAGE_REPOSITORY`
- `JANGAR_IMAGE_TAG`
- `JANGAR_KUSTOMIZE_PATH`
- `JANGAR_SERVICE_MANIFEST`

## Rollout verification

```bash
kubectl rollout status deployment/bumba -n jangar
kubectl rollout status deployment/jangar -n jangar
```

## Rollback

- Revert the tag change in `argocd/applications/bumba/kustomization.yaml`.
- Re-apply manifests or let Argo CD reconcile.

## Resources

- Reference: `references/deploy-runbook.md`
- Helper script: `scripts/deploy-service.sh`
- Checklist: `assets/deploy-checklist.md`
