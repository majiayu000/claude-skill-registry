---
name: k9s
description: k9s terminal UI for Kubernetes. Use for K8s management.
---

# K9s

K9s is a terminal UI (TUI) for Kubernetes. It is faster than clicking in a web dashboard and morediscoverable than raw `kubectl`.

## When to Use

- **Cluster Management**: Viewing Pods, Logs, and YAML in real-time.
- **Debugging**: Shell into a pod (`s`), view logs (`l`), delete pod (`Ctrl+d`).
- **Safety**: Read-only mode prevents accidental deletions in Prod.

## Core Concepts

### Views

Navigate by resource type (`:pods`, `:svc`, `:deploy`).

### XRay

`:xray RESOURCE` creates a dependency tree view (e.g., Service -> Pod -> Node).

### Pulses

`:pulse` gives a high-level health dashboard.

## Best Practices (2025)

**Do**:

- **Use Aliases**: Define aliases for commonly used CRDs.
- **Use Plugins**: Extend K9s with custom scripts (e.g., `kubectl neat` to clean YAML).
- **Context Awareness**: Use skins to color-code Prod (Red) vs Dev (Blue).

**Don't**:

- **Don't rely solely on it**: Know your `kubectl` commands for scripting/automation.

## References

- [K9s Documentation](https://k9scli.io/)
