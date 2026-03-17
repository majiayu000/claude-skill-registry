---
name: k8s-dev
description: Assistance with Remote Kubernetes Development (Telepresence, Okteto, DevSpace).
context_cost: medium
---
# Kubernetes Dev Skill

## Triggers
- k8s dev
- remote dev
- telepresence
- okteto
- devspace
- tilt
- scaffold
- remote cluster

## Purpose
To develop directly against a remote Kubernetes cluster, enabling access to cloud dependencies and effectively "infinite" resources.

## Capabilities

### 1. Remote Interception (Telepresence)
-   **Intercept**: Route traffic from a remote service to your laptop.
-   **Debug**: Step through code locally while handling live remote requests.
-   **Preview URLs**: Share a specific intercept version with teammates.

### 2. Sync & Hot Reload (Okteto / DevSpace)
-   **File Sync**: Bi-directional sync between local folder and remote pod.
-   **Terminal**: Get a shell inside the remote pod.
-   **Environment**: Spin up ephemeral namespaces for each developer.

### 3. Configuration
-   **DevSpace**: Generate `devspace.yaml` for pipeline + sync.
-   **Okteto**: Generate `okteto.yaml` for hybrid dev.

## Instructions
1.  **When to use**: Recommend Remote Dev when the app is too large for Docker Desktop (RAM/CPU limits) or depends on cloud-only resources (RDS, SQS).
2.  **Isolation**: Ensure developers work in their own Namespaces to avoid stepping on toes.
3.  **Security**: Use RBAC to limit developer permissions in the cluster.

## Deliverables
-   `devspace.yaml` configuration.
-   `telepresence` intercept commands.
-   `okteto.yaml` manifest.
