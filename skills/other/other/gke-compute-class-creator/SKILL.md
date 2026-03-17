---
name: gke-compute-class-creator
description: Guide for creating GKE ComputeClass resources. Use this skill when users want to define custom node configurations, autoscaling priorities, or hardware requirements (e.g., Spot VMs, GPUs, specific machine families) for their GKE workloads.
---

# Creating GKE ComputeClasses

This skill helps you construct `ComputeClass` resources for Google Kubernetes Engine (GKE). ComputeClasses allow for declarative node configuration and sophisticated autoscaling behaviors like fallback priorities and active migration.

## Workflow

1. **Analyze Requirements**: Determine the user's goals (Cost optimization? Specific hardware? High availability?).
2. **Select Strategy**:
   - **Cost Optimization**: Use `spot: true` as a high priority, with `spot: false` as a fallback.
   - **Performance**: Select specific `machineFamily` (e.g., `c3`, `c4`) or `machineType`.
   - **AI/ML**: Configure `gpu` or `tpu` fields.
3. **Construct YAML**: Use the references below to build the `ComputeClass` manifest.
4. **Validate**: Ensure all fields comply with the specification.
5. **Apply**: Provide the user with the `kubectl apply -f <filename>.yaml` command.

## References

- **[Specification](references/compute-class-spec.md)**: Detailed breakdown of the `ComputeClass` CRD fields (`priorities`, `machineFamily`, `gpu`, etc.).
- **[Examples](references/compute-class-examples.md)**: Copy-pasteable YAML patterns for common scenarios (Spot fallback, GPU, Zonal).

## Usage Tips

- **Active Migration**: If the user wants to automatically move back to Spot VMs when they become available, ensure `spec.activeMigration.optimizeRulePriority` is set to `true`.
- **Node Selection**: Remind the user that to use the class, their Pods must specify:
  ```yaml
  nodeSelector:
    cloud.google.com/compute-class: "<class-name>"
  ```
- **Conflict Warning**: Advise against mixing `ComputeClass` selection with other hard node selectors (like `cloud.google.com/gke-spot`) as this can lead to scheduling conflicts.
