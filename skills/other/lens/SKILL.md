---
name: lens
description: Lens Kubernetes IDE. Use for K8s management.
---

# Lens Desktop

Lens is a graphical IDE for Kubernetes. 2025 adds **Lens Prism** (Agent Mode) to reason about cluster issues.

## When to Use

- **Visualization**: Accessing Prometheus metrics (built-in) alongside Pods.
- **Multi-Cluster**: Managing 10+ clusters with easy context switching.
- **Helm**: Visual Helm chart management (upgrade/rollback).

## Core Concepts

### Hotbar

Quick access to different clusters.

### Metrics Integration

Detects Prometheus automatically and adds graphs to Pod/Node views.

### Terminal

Opens a terminal with `kubectl` context pre-set to the active cluster.

## Best Practices (2025)

**Do**:

- **Use Lens Prism**: Ask "Why is this pod pending?" to get AI diagnosis.
- **Use Port Forwarding**: The UI manages port forwards visually.
- **Share Catalogs**: Sync cluster lists with team members.

**Don't**:

- **Don't ignore RBAC**: Lens respects your kubeconfig permissions.

## References

- [Lens Documentation](https://docs.k8slens.dev/)
