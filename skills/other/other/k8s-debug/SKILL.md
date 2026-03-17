---
name: k8s-debug
type: complex
depth: extended
description: >-
  Diagnoses Kubernetes pod failures, network connectivity, deployment rollouts,
  HPA scaling, and EKS cluster issues. Use when debugging CrashLoopBackOff,
  ImagePullBackOff, Pending pods, service endpoints, ingress/Gateway API routing,
  sidecar containers, in-place resize, node pressure, VPC CNI, IRSA, or observability
  stack. Covers K8s 1.32-1.35 GA features: sidecars, DRA, ValidatingAdmissionPolicy.
---

# [H1][K8S-DEBUG]
>**Dictum:** *Systematic diagnosis eliminates guesswork.*

<br>

Cloud mode (EKS/K8s 1.32+) only. Selfhosted uses Docker containers -- see docker-gen/docker-val skills.

**K8s:** 1.32-1.35 | Stable APIs: sidecar containers GA (1.33), DRA GA (1.33), in-place pod resize GA (1.35), fine-grained supplemental groups GA (1.35), topology-aware routing GA (1.34), VolumeAttributesClass GA (1.34), `kubectl events --for` (1.32+), `kubectl debug --copy-to` (1.32+), ValidatingAdmissionPolicy GA (1.30+), Gateway API v1.4 (1.35+) | **Canonical:** `infrastructure/src/deploy.ts` (207 LOC)

**Tasks:**
1. Identify pod status from decision tree below.
2. Follow the matching workflow branch.
3. Read `references/troubleshooting_pods.md` for pod/networking workflows or `references/troubleshooting_cluster.md` for cluster/operational workflows.
4. Read `references/common_issues.md` for detailed diagnostic tables.
5. Use scripts for automated data collection (see Scripts section).
6. Follow escalation checklist if unresolved.

---
## [1][RESOURCE_MAP]
>**Dictum:** *deploy.ts resources are the debugging targets.*

<br>

| [INDEX] | [CATEGORY]    | [RESOURCE]        | [KIND]                | [KEY_DETAILS]                                            |
| :-----: | ------------- | ----------------- | --------------------- | -------------------------------------------------------- |
|   [1]   | **Namespace** | `parametric-ns`   | Namespace             | `metadata.name: parametric`.                             |
|   [2]   | **Compute**   | `compute-deploy`  | Deployment            | Container `api`, label `app: parametric-api`, port 4000. |
|   [3]   | **Compute**   | `compute-svc`     | Service (ClusterIP)   | Port 4000/TCP, selector `app: parametric-api`.           |
|   [4]   | **Compute**   | `compute-hpa`     | HPA (autoscaling/v2)  | CPU + memory targets, env-driven min/max.                |
|   [5]   | **Compute**   | `compute-ingress` | Ingress (nginx class) | TLS `compute-tls`, ssl-redirect, proxy-body-size 50m.    |
|   [6]   | **Compute**   | `compute-config`  | ConfigMap             | API_BASE_URL, POSTGRES_HOST, REDIS_HOST, OTEL_*.         |
|   [7]   | **Compute**   | `compute-secret`  | Secret                | POSTGRES_PASSWORD, REDIS_PASSWORD.                       |
|   [8]   | **Observe**   | `observe-alloy`   | DaemonSet             | Alloy OTLP: gRPC :4317, HTTP :4318, metrics :12345.      |
|   [9]   | **Observe**   | `prometheus`      | Deployment            | Port 9090, PVC `/prometheus`, scrape interval 15s.       |
|  [10]   | **Observe**   | `grafana`         | Deployment            | Port 3000, PVC `/var/lib/grafana`.                       |

**Probes** (`_CONFIG.k8s.probes`, deploy.ts:19): Startup 150s window (5s x 30), Liveness 30s (10s x 3), Readiness 15s (5s x 3). `terminationGracePeriodSeconds: 30`.

**Labels:** Compute: `app: parametric-api`. Observe: `app: <name>, stack: parametric, tier: observe`. Metadata: `component: <name>, stack: parametric, tier: observe`.

```bash
# Quick status for all project resources
kubectl get deploy,ds,svc,hpa,ingress,configmap,secret -n parametric
kubectl get pods -n parametric -o wide
kubectl top pods -n parametric --containers
```

---
## [2][DECISION_TREE]
>**Dictum:** *Pod status determines the diagnostic path.*

<br>

```
START: What is the pod status?
|
+-- Pending --------> [SCHEDULING]
|   +-- "Insufficient cpu/memory" --> kubectl top nodes --> add nodes or free resources
|   +-- "didn't match node affinity" --> check nodeSelector --> adjust constraint
|   +-- Taints block scheduling --> add tolerations or remove taint
|   +-- "unbound PersistentVolumeClaims" --> kubectl get pvc -n parametric --> fix PVC binding
|
+-- CrashLoopBackOff --> [APPLICATION CRASH]
|   +-- kubectl logs <pod> -n parametric -c api --previous
|   |   +-- Stack trace --> fix app code, redeploy
|   |   +-- "Error: connect ECONNREFUSED" --> verify DB/Redis/deps running
|   |   +-- Missing env var --> check compute-config and compute-secret
|   +-- kubectl describe pod <pod> -n parametric
|       +-- "OOMKilled" (exit 137) --> increase memory limits (deploy.ts:168)
|       +-- "Startup probe failed" --> boot > 150s; increase failureThreshold
|       +-- "Liveness probe failed" --> app hung; check /api/health/liveness
|
+-- ImagePullBackOff --> [IMAGE PULL]
|   +-- "manifest unknown" --> verify image:tag exists in registry
|   +-- "unauthorized" --> create/update imagePullSecrets
|
+-- Running but broken --> [SERVICE/NETWORK]
|   +-- kubectl get endpoints compute-svc -n parametric
|   |   +-- ENDPOINTS empty --> selector mismatch (must be app: parametric-api)
|   |   +-- ENDPOINTS has IPs --> test connectivity from debug pod
|   +-- Ingress 502/503 --> check pod readiness + ingress controller
|   +-- TLS handshake error --> check compute-tls secret + cert expiry
|
+-- Error / Unknown --> [NODE/CLUSTER]
    +-- kubectl describe node <node>
    +-- MemoryPressure/DiskPressure --> evict pods, clean disk, add nodes
    +-- NetworkUnavailable --> check CNI plugin (aws-node on EKS)
```

---
## [3][ESSENTIAL_COMMANDS]
>**Dictum:** *Structured queries replace grep-based debugging.*

<br>

```bash
# --- Pod Lifecycle ---
kubectl get pods -n parametric -o wide
kubectl describe pod <pod> -n parametric
kubectl logs <pod> -n parametric -c api [--previous] [--tail=100]
kubectl exec <pod> -n parametric -c api -it -- /bin/sh
kubectl top pod <pod> -n parametric --containers
kubectl events --for pod/<pod> -n parametric

# --- Structured Queries (jsonpath) ---
kubectl get pod <pod> -n parametric -o jsonpath='{.status.containerStatuses[*].state}'
kubectl get pod <pod> -n parametric -o jsonpath='{.status.containerStatuses[?(@.name=="api")].restartCount}'
kubectl get deploy compute-deploy -n parametric -o jsonpath='{.status.conditions[?(@.type=="Available")].status}'

# --- Service / Network ---
kubectl get svc,endpoints -n parametric
kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- /bin/bash
kubectl exec <pod> -n parametric -- nslookup compute-svc.parametric.svc.cluster.local

# --- Ingress (nginx) / Gateway API ---
kubectl describe ingress compute-ingress -n parametric
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --tail=50
kubectl get gateways,httproutes,grpcroutes -n parametric
kubectl get httproute <route> -n parametric -o jsonpath='{.status.parents[*].conditions}'

# --- HPA / Observability ---
kubectl describe hpa compute-hpa -n parametric
kubectl get pods -n parametric -l tier=observe
kubectl logs -n parametric -l app=alloy --tail=50

# --- Debug Containers (stable 1.25+) ---
kubectl debug <pod> -n parametric -it --image=nicolaka/netshoot --target=api
kubectl debug <pod> -it --copy-to=debug-pod --share-processes --container=api -- /bin/sh
kubectl debug node/<node> -it --image=ubuntu

# --- Sidecar Containers (GA 1.33+) ---
kubectl get pod <pod> -n parametric -o jsonpath='{.spec.initContainers[?(@.restartPolicy=="Always")]}'
kubectl get pod <pod> -n parametric -o jsonpath='{.status.initContainerStatuses[*].name}'

# --- In-Place Pod Resize (GA 1.35+) ---
kubectl patch pod <pod> -n parametric --subresource resize --type merge -p \
  '{"spec":{"containers":[{"name":"api","resources":{"requests":{"cpu":"500m","memory":"512Mi"},"limits":{"cpu":"1000m","memory":"1Gi"}}}]}}'
# > [IMPORTANT] kubectl patch --subresource resize is temporary. Update deploy.ts resource specs + pulumi up.
kubectl get pod <pod> -n parametric -o jsonpath='{.status.resize}'

# --- ValidatingAdmissionPolicy (GA 1.30+) ---
kubectl get validatingadmissionpolicies
kubectl get events --field-selector reason=ValidatingAdmissionPolicyRejection -n parametric

# --- Wait / Condition-Based ---
kubectl wait --for=condition=ready pod -l app=parametric-api -n parametric --timeout=120s
kubectl wait --for=condition=available deployment/compute-deploy -n parametric --timeout=300s

# --- ConfigMap / Secret Verification ---
kubectl get configmap compute-config -n parametric -o yaml
kubectl get secret compute-secret -n parametric -o jsonpath='{.data}' | jq 'keys'

# --- EKS-Specific ---
aws eks describe-cluster --name <cluster>
kubectl get pods -n kube-system -l k8s-app=aws-node
kubectl logs -n kube-system -l k8s-app=aws-node --tail=50

# --- Emergency (IaC-first: all state-modifying commands below are temporary) ---
kubectl rollout restart deployment/compute-deploy -n parametric
# > [IMPORTANT] Temporary fix. Update deploy.ts image tag or config for permanent resolution via pulumi up.
kubectl rollout undo deployment/compute-deploy -n parametric
# > [IMPORTANT] Temporary rollback. Fix root cause in deploy.ts and redeploy via pulumi up.
kubectl delete pod <pod> -n parametric --force --grace-period=0
# > [IMPORTANT] Temporary. Investigate root cause in deployment config (deploy.ts).
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
# > [CRITICAL] Bypasses Pulumi state. Coordinate with Pulumi node group config. Run pulumi refresh after.
kubectl scale deployment/compute-deploy -n parametric --replicas=N
# > [IMPORTANT] Temporary. Update HPA/deployment replica specs in Pulumi for permanent resolution via pulumi up.
kubectl taint nodes <node> <key>:<effect>-
# > [CRITICAL] Bypasses Pulumi state. Update deploy.ts toleration/taint config + pulumi up.
```

---
## [4][EKS_DEBUGGING]
>**Dictum:** *EKS-specific issues require AWS-level diagnostics.*

<br>

| [INDEX] | [SYMPTOM]                         | [DIAGNOSTIC]                                                                         | [FIX]                                                                   |
| :-----: | --------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
|   [1]   | **Pod stuck `ContainerCreating`** | `kubectl logs -n kube-system -l k8s-app=aws-node --tail=50`                          | VPC CNI IP exhaustion: scale nodes, prefix delegation, larger instance. |
|   [2]   | **Pod cannot reach AWS APIs**     | `kubectl describe sa <sa> -n parametric`                                             | IRSA: annotate SA with `eks.amazonaws.com/role-arn`.                    |
|   [3]   | **Node cannot join cluster**      | `aws eks describe-nodegroup --cluster-name <c> --nodegroup-name <ng>`                | Attach EKS node IAM policies.                                           |
|   [4]   | **Add-on unhealthy**              | `aws eks describe-addon --cluster-name <c> --addon-name <name>`                      | `aws eks update-addon --addon-version <latest>`.                        |
|   [5]   | **CoreDNS CrashLoop on EKS**      | `kubectl logs -n kube-system -l k8s-app=kube-dns`                                    | Add Fargate profile or patch compute type.                              |
|   [6]   | **ALB not routing**               | `kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller` | Check subnet tags + IAM policy (project uses nginx, not ALB).           |

---
## [5][SCRIPTS]
>**Dictum:** *Automated collection prevents missed diagnostics.*

| [INDEX] | [SCRIPT]                         | [SCOPE]               | [USAGE]                                                                            |
| :-----: | -------------------------------- | --------------------- | ---------------------------------------------------------------------------------- |
|   [1]   | **`scripts/pod_diagnostics.py`** | Single pod deep-dive  | `python3 scripts/pod_diagnostics.py <pod> -n parametric [-c api] [-o report.txt]`. |
|   [2]   | **`scripts/_collectors.py`**     | Diagnostic collectors | Imported by `pod_diagnostics.py` (not run directly).                               |
|   [3]   | **`scripts/cluster_health.sh`**  | Cluster-wide overview | `./scripts/cluster_health.sh`.                                                     |
|   [4]   | **`scripts/network_debug.sh`**   | Network connectivity  | `./scripts/network_debug.sh parametric <pod>`.                                     |

---
## [6][ESCALATION_CHECKLIST]
>**Dictum:** *Systematic escalation prevents missed root causes.*

- [ ] Pod events + current/previous logs.
- [ ] Startup (150s) vs liveness (30s) probe failure distinguished.
- [ ] Node resources: `kubectl top nodes`.
- [ ] Image tag exists in registry.
- [ ] Service selector matches labels (`app: parametric-api`) + DNS resolves.
- [ ] NetworkPolicies not blocking + ConfigMap/Secret/env vars present.
- [ ] HPA status + Ingress/TLS healthy.
- [ ] Sidecar containers (1.33+) + in-place resize status (1.35+).
- [ ] (EKS) VPC CNI health + IRSA annotation.
