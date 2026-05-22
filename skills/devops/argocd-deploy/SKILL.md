---
name: argocd-deploy
description: Deploy to Kubernetes via ArgoCD GitOps
argument-hint: "<app-name> [--sync] [--prune]"
tags: [deploy, argocd, gitops, kubernetes]
user-invocable: true
---

# ArgoCD GitOps Deployment

Deploy and manage Kubernetes applications via ArgoCD.

## What To Do

1. **CLI commands**:
   ```bash
   argocd app sync matching-engine
   argocd app get matching-engine
   argocd app diff matching-engine
   argocd app rollback matching-engine <revision>
   ```

2. **Create ArgoCD Application manifest** (deploy/argocd-app.yaml)

3. **Sync policies**: automated prune + selfHeal for production

## Arguments
- `<app-name>`: ArgoCD application name
- `--sync`: Force sync now
- `--prune`: Remove orphaned resources