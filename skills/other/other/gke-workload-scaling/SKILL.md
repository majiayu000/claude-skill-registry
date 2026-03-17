---
name: gke-workload-scaling
description: Specific workflows for scaling GKE workloads using HPA and VPA, as well as best practices for autoscaling configuration.
---

# GKE Workload Scaling

This skill provides workflows and best practices for scaling applications on Google Kubernetes Engine (GKE). It covers manual scaling, Horizontal Pod Autoscaling (HPA), and Vertical Pod Autoscaling (VPA).

## Workflows

### 1. Manual Scaling

Quickly scale a deployment to a fixed number of replicas. Useful for immediate manual intervention or testing.

**Command:**

```bash
kubectl scale deployment <deployment-name> --replicas=<number> -n <namespace>
```

### 2. Horizontal Pod Autoscaling (HPA)

Automatically scale the number of pods based on observed CPU utilization, memory utilization, or custom metrics.

**Prerequisites:**

- Metrics Server must be running (enabled by default on GKE).
- Containers clearly define resource requests/limits.

**Quick Command:**

```bash
kubectl autoscale deployment <deployment-name> --cpu-percent=50 --min=1 --max=10
```

**Manifest Approach (Recommended):**
Use a YAML manifest for version-controlled configuration.
See [assets/hpa-example.yaml](assets/hpa-example.yaml) for a template.

```bash
kubectl apply -f assets/hpa-example.yaml
```

### 3. Vertical Pod Autoscaling (VPA)

Automatically adjust the CPU and memory reservations for your pods to match actual usage. This is critical for right-sizing workloads.

**Prerequisites:**

- VPA must be enabled on the cluster.
  - **Autopilot:** Enabled by default.
  - **Standard:** Must be enabled manually.

**Enable VPA on Standard Cluster:**

```bash
gcloud container clusters update <cluster-name> --enable-vertical-pod-autoscaling --zone <zone>
```

**Update Modes:**

- `Off`: Calculates recommendations but does not apply them. Good for "dry run" analysis.
- `Initial`: Assigns resources only at pod creation time.
- `Auto`: Updates running pods by restarting them if recommendations differ significantly from requests.
- `InPlaceOrRecreate`: Attempts to update Pod resources without recreating the Pod. If in-place update is not possible, it reverts to `Auto` mode (requires GKE 1.34+).

**Example:**
See [assets/vpa-example.yaml](assets/vpa-example.yaml) for a configuration template.

### 4. Cluster Autoscaler

While not a workload-level scaler, the Cluster Autoscaler is essential for ensuring your cluster has enough nodes to run the scaled pods.

**Enable on a Node Pool:**

```bash
gcloud container clusters update <cluster-name> \
    --enable-autoscaling \
    --node-pool <node-pool-name> \
    --min-nodes <min> \
    --max-nodes <max> \
    --zone <zone>
```

## Best Practices

1. **Define Resource Requests:** HPA and VPA rely on accurate resource requests. Always define them in your container specs.
2. **Avoid Metric Conflicts:** Do not configure HPA and VPA to use the same metric (e.g., both CPU). This causes thrashing.
   - _Typical Pattern:_ HPA on CPU, VPA on Memory.
3. **Pod Disruption Budgets (PDBs):** Define PDBs to ensure application availability during scaling events or node upgrades.
4. **HPA Lag:** HPA has a stabilization window (default 5 mins) to prevent rapid fluctuation.
5. **VPA "Auto" Mode Risks:** In "Auto" mode, VPA restarts pods to change resources. Ensure your application handles restarts gracefully (e.g., handles SIGTERM).
   - _Note:_ By default, VPA requires at least 2 replicas to perform evictions. In GKE 1.22+, you can override this by setting `minReplicas` in `PodUpdatePolicy`.
