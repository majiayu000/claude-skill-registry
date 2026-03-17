---
version: 4.1.0-fractal
name: gitops-workflow
description: Implement GitOps workflows with ArgoCD and Flux for automated, declarative Kubernetes deployments with continuous reconciliation. Use when implementing GitOps practices, automating Kubernetes deployments, or setting up declarative infrastructure management.
---

# GitOps Workflow

Complete guide to implementing GitOps workflows with ArgoCD and Flux for automated Kubernetes deployments.

## Purpose

Implement declarative, Git-based continuous delivery for Kubernetes using ArgoCD or Flux CD, following OpenGitOps principles.

## Use this skill when

- Set up GitOps for Kubernetes clusters
- Automate application deployments from Git
- Implement progressive delivery strategies
- Manage multi-cluster deployments
- Configure automated sync policies
- Set up secret management in GitOps

## Do not use this skill when

- You need a one-off manual deployment
- You cannot manage cluster access or repo permissions
- You are not deploying to Kubernetes

## Instructions

1. Define repo layout and desired-state conventions.
2. Install ArgoCD or Flux and connect clusters.
3. Configure sync policies, environments, and promotion flow.
4. Validate rollbacks and secret handling.

## Safety

- Avoid auto-sync to production without approvals.
- Keep secrets out of Git and use sealed or external secret managers.

## OpenGitOps Principles

1. **Declarative** - Entire system described declaratively
2. **Versioned and Immutable** - Desired state stored in Git
3. **Pulled Automatically** - Software agents pull desired state
4. **Continuously Reconciled** - Agents reconcile actual vs desired state

## ArgoCD Setup

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [1. Installation](./sub-skills/1-installation.md)
### 2. [2. Repository Structure](./sub-skills/2-repository-structure.md)
### 3. [3. Create Application](./sub-skills/3-create-application.md)
### 4. [4. App of Apps Pattern](./sub-skills/4-app-of-apps-pattern.md)
### 5. [1. Installation](./sub-skills/1-installation.md)
### 6. [2. Create GitRepository](./sub-skills/2-create-gitrepository.md)
### 7. [3. Create Kustomization](./sub-skills/3-create-kustomization.md)
### 8. [Auto-Sync Configuration](./sub-skills/auto-sync-configuration.md)
### 9. [Canary Deployment with ArgoCD Rollouts](./sub-skills/canary-deployment-with-argocd-rollouts.md)
### 10. [Blue-Green Deployment](./sub-skills/blue-green-deployment.md)
### 11. [External Secrets Operator](./sub-skills/external-secrets-operator.md)
### 12. [Sealed Secrets](./sub-skills/sealed-secrets.md)
