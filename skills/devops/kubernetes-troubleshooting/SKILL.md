---
name: kubernetes-troubleshooting
description: |
  Comprehensive Kubernetes and OpenShift cluster health analysis and troubleshooting. Use this skill when:
  (1) Proactive cluster health assessment and security analysis
  (2) Analyzing pod/container logs for errors or issues
  (3) Interpreting cluster events (kubectl get events)
  (4) Debugging pod failures: CrashLoopBackOff, ImagePullBackOff, OOMKilled
  (5) Diagnosing networking issues: DNS, Service connectivity, Ingress/Route problems
  (6) Investigating storage issues: PVC pending, mount failures
  (7) Analyzing node problems: NotReady, resource pressure, taints
  (8) Troubleshooting OCP-specific issues: SCCs, Routes, Operators, Builds
  (9) Performance analysis and resource optimization
  (10) Security vulnerability assessment and RBAC validation
metadata:
  author: cluster-skills
  version: "1.0.0"
---

# Kubernetes / OpenShift Troubleshooting Guide

Systematic approach to diagnosing and resolving cluster issues through event analysis, log interpretation, and Popeye-style health scoring.

## Current Versions & Tools (January 2026)

| Platform | Version | Key Changes |
|----------|---------|-------------|
| **Kubernetes** | 1.31.x | Sidecar containers GA, Pod lifecycle improvements |
| **OpenShift** | 4.17.x | OVN-Kubernetes default, enhanced web terminal |
| **EKS** | 1.31 | Pod Identity, Auto Mode, Karpenter 1.x |
| **AKS** | 1.31 | Cilium CNI, Workload Identity GA |
| **GKE** | 1.31 | Autopilot improvements, Gateway API GA |

### Troubleshooting Tools

| Tool | Install | Purpose |
|------|---------|---------|
| **k9s** | `brew install k9s` | Terminal UI |
| **stern** | `brew install stern` | Multi-pod log tailing |
| **kubectx/kubens** | `brew install kubectx` | Context switching |
| **kubectl-node-shell** | `kubectl krew install node-shell` | Node access |

## Command Usage Convention

**IMPORTANT**: This skill uses `kubectl` as the primary command. When working with:
- **OpenShift/ARO clusters**: Replace `kubectl` with `oc`
- **Standard Kubernetes (AKS, EKS, GKE)**: Use `kubectl` as shown

## Cluster Health Scoring (Popeye-Style)

Health scores range from 0-100. Issues reduce the score based on severity:

- **BOOM (Critical)**: -50 points - Security vulnerabilities, resource exhaustion, failed services
- **WARN (Warning)**: -20 points - Configuration inefficiencies, best practice violations
- **INFO (Informational)**: -5 points - Non-critical issues, optimization opportunities

### Quick Cluster Health Assessment

```bash
#!/bin/bash
# cluster-health-check.sh
echo "=== CLUSTER HEALTH ASSESSMENT ==="

# 1. Node Health (Critical)
echo "### NODE HEALTH ###"
kubectl get nodes -o wide | grep -E "NotReady|Unknown" && \
  echo "BOOM: Unhealthy nodes detected!" || echo "✓ All nodes healthy"

# 2. Pod Issues (Critical)
echo -e "\n### POD HEALTH ###"
POD_ISSUES=$(kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded --no-headers | wc -l)
if [ $POD_ISSUES -gt 0 ]; then
    echo "WARN: $POD_ISSUES pods not running"
    kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded
else
    echo "✓ All pods running"
fi

# 3. Security (Critical)
echo -e "\n### SECURITY ASSESSMENT ###"
PRIVILEGED=$(kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].securityContext.privileged == true) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
[ $PRIVILEGED -gt 0 ] && echo "BOOM: $PRIVILEGED privileged containers!" || echo "✓ No privileged containers"

# 4. Resource Configuration (Warning)
echo -e "\n### RESOURCE CONFIGURATION ###"
NO_LIMITS=$(kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].resources.limits == null) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
[ $NO_LIMITS -gt 0 ] && echo "WARN: $NO_LIMITS containers without limits" || echo "✓ All have limits"

# 5. Storage (Warning)
echo -e "\n### STORAGE HEALTH ###"
PENDING_PVC=$(kubectl get pvc -A --field-selector=status.phase!=Bound --no-headers | wc -l)
[ $PENDING_PVC -gt 0 ] && echo "WARN: $PENDING_PVC PVCs not bound" || echo "✓ All PVCs bound"

# OpenShift: Cluster Operators
if command -v oc &> /dev/null; then
    echo -e "\n### OPENSHIFT OPERATORS ###"
    DEGRADED=$(oc get clusteroperators --no-headers | grep -c -E "False.*True|False.*False")
    [ $DEGRADED -gt 0 ] && echo "BOOM: $DEGRADED operators degraded!" || echo "✓ All operators healthy"
fi
```

## Quick Diagnostic Commands

```bash
# Pod status overview
kubectl get pods -n ${NAMESPACE} -o wide

# Recent events (sorted by time)
kubectl get events -n ${NAMESPACE} --sort-by='.lastTimestamp'

# Pod details and events
kubectl describe pod ${POD_NAME} -n ${NAMESPACE}

# Container logs (current)
kubectl logs ${POD_NAME} -n ${NAMESPACE} -c ${CONTAINER}

# Container logs (previous crashed instance)
kubectl logs ${POD_NAME} -n ${NAMESPACE} -c ${CONTAINER} --previous

# Multi-pod log streaming
stern -n ${NAMESPACE} ${POD_PREFIX}
stern -A -l app=${APP_NAME} --since 1h

# Node status
kubectl get nodes -o wide
kubectl describe node ${NODE_NAME}

# Resource usage
kubectl top pods -n ${NAMESPACE}
kubectl top nodes
```

## Pod Status Interpretation

### Pod Phase States

| Phase | Meaning | Action |
|-------|---------|--------|
| `Pending` | Not scheduled or pulling images | Check events, node resources, PVC status |
| `Running` | At least one container running | Check container statuses if issues |
| `Succeeded` | All containers completed successfully | Normal for Jobs |
| `Failed` | All containers terminated, at least one failed | Check logs, exit codes |
| `Unknown` | Cannot determine state | Node communication issue |

### Container Waiting States

| Reason | Cause | Resolution |
|--------|-------|------------|
| `ContainerCreating` | Setting up container | Check events, volume mounts |
| `ImagePullBackOff` | Cannot pull image | Verify image name, registry access, credentials |
| `ErrImagePull` | Image pull failed | Check image exists, network, ImagePullSecrets |
| `CreateContainerConfigError` | Config error | Check ConfigMaps, Secrets exist |
| `CrashLoopBackOff` | Container repeatedly crashing | Check `logs --previous`, fix application |

### Container Exit Codes

| Exit Code | Signal | Cause | Resolution |
|-----------|--------|-------|------------|
| 0 | - | Normal exit | Expected for Jobs |
| 1 | - | Application error | Check logs for stack trace |
| 126 | - | Command not executable | Fix permissions |
| 127 | - | Command not found | Fix command path |
| 137 | SIGKILL | OOM or forced termination | Increase memory limit |
| 143 | SIGTERM | Graceful shutdown | Normal during updates |

## Event Analysis

### Critical Events to Monitor

#### Scheduling Events

| Event | Meaning | Resolution |
|-------|---------|------------|
| `FailedScheduling` | Cannot place pod | Check node resources, taints, affinity |
| `Unschedulable` | No suitable node | Add nodes, adjust requirements |

**FailedScheduling Messages:**
```
"Insufficient cpu"           → Reduce requests or add capacity
"Insufficient memory"        → Reduce requests or add capacity
"node(s) had taint"          → Add toleration or remove taint
"node(s) didn't match selector" → Fix nodeSelector/affinity
"persistentvolumeclaim not found" → Create PVC or fix name
```

#### Image Events

| Event | Meaning | Resolution |
|-------|---------|------------|
| `BackOff` | Repeated pull failures | Check image name, registry, auth |
| `ErrImageNeverPull` | Image not local | Change imagePullPolicy or pre-pull |

**ImagePullBackOff Diagnosis:**
```bash
# Check image name
kubectl get pod ${POD} -o jsonpath='{.spec.containers[*].image}'

# Verify ImagePullSecrets
kubectl get pod ${POD} -o jsonpath='{.spec.imagePullSecrets}'
kubectl get secret ${SECRET} -n ${NAMESPACE}
```

#### Volume Events

| Event | Meaning | Resolution |
|-------|---------|------------|
| `FailedMount` | Cannot mount volume | Check PVC, storage class |
| `FailedAttachVolume` | Cannot attach | Check cloud provider, volume exists |

**PVC Pending Diagnosis:**
```bash
kubectl describe pvc ${PVC_NAME} -n ${NAMESPACE}
kubectl get storageclass
kubectl get pv
```

## Log Analysis Patterns

### Common Error Patterns

```bash
# Search for errors
kubectl logs ${POD} -n ${NS} | grep -iE "(error|exception|fatal|panic)"

# Java OOM
java.lang.OutOfMemoryError → Increase memory, tune JVM heap

# Connection refused
ECONNREFUSED, Connection refused → Dependency not available

# DNS failure
ENOTFOUND, getaddrinfo → DNS resolution failed, check service name

# Permission denied
Permission denied → Check securityContext, runAsUser, fsGroup
```

### Memory Issues (OOMKilled)

```
Last State: Terminated
Reason: OOMKilled
Exit Code: 137

→ Solutions:
1. Increase memory limit
2. Profile application memory usage
3. For JVM: Set -Xmx < container limit (leave ~25% headroom)
```

## Node Troubleshooting

### Node Conditions

| Condition | Status | Meaning |
|-----------|--------|---------|
| `Ready` | True | Node healthy |
| `Ready` | False | Kubelet not healthy |
| `Ready` | Unknown | No heartbeat |
| `MemoryPressure` | True | Low memory |
| `DiskPressure` | True | Low disk space |
| `PIDPressure` | True | Too many processes |

### Node NotReady Diagnosis

```bash
kubectl describe node ${NODE_NAME}

# On the node (SSH or debug)
systemctl status kubelet
journalctl -u kubelet -f

# Check resources
df -h
free -m
top
```

## Networking Troubleshooting

### DNS Issues

```bash
# Test DNS resolution
kubectl run dns-test --image=busybox:1.28 --rm -it --restart=Never -- \
  nslookup ${SERVICE_NAME}.${NAMESPACE}.svc.cluster.local

# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns
```

### Service Connectivity

```bash
# Verify service and endpoints
kubectl get svc ${SERVICE} -n ${NS}
kubectl get endpoints ${SERVICE} -n ${NS}

# Test from debug pod
kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never -- \
  curl -v http://${SERVICE}.${NS}.svc.cluster.local:${PORT}
```

### Ingress/Route Issues

```bash
# Check Ingress
kubectl describe ingress ${INGRESS} -n ${NS}

# Ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# OpenShift Route
oc describe route ${ROUTE} -n ${NS}
oc get pods -n openshift-ingress
```

## OpenShift-Specific Troubleshooting

### Cluster Operators

```bash
# Check overall health
oc get clusteroperators

# Investigate degraded operator
oc describe clusteroperator ${OPERATOR}
oc logs -n openshift-${OPERATOR} -l name=${OPERATOR}-operator
```

### Security Context Constraints (SCC)

```bash
# List SCCs
oc get scc

# Check which SCC a pod is using
oc get pod ${POD} -n ${NS} -o yaml | grep scc

# Common error fix
# "unable to validate against any security context constraint"
oc adm policy add-scc-to-user ${SCC} -z ${SERVICE_ACCOUNT} -n ${NS}
```

### Build Failures

```bash
# Check build status
oc get builds -n ${NS}
oc describe build ${BUILD} -n ${NS}
oc logs build/${BUILD} -n ${NS}
```

## Cloud Provider Troubleshooting

### EKS (AWS)

```bash
aws eks describe-cluster --name ${CLUSTER} --query 'cluster.status'
aws eks describe-addon --cluster-name ${CLUSTER} --addon-name vpc-cni
eksctl get nodegroup --cluster ${CLUSTER}
```

### AKS (Azure)

```bash
az aks show --resource-group ${RG} --name ${CLUSTER} --query provisioningState
az aks check-network outbound --resource-group ${RG} --name ${CLUSTER}
```

### GKE (Google Cloud)

```bash
gcloud container clusters describe ${CLUSTER} --region ${REGION} --format='value(status)'
gcloud container operations list --filter="targetLink:${CLUSTER}" --limit=10
```

## Diagnostic Decision Tree

### Pod Not Starting

```
Pod Phase = Pending?
├── Yes → Check Scheduling
│   ├── "Insufficient cpu/memory" → Add nodes or reduce requests
│   ├── "node(s) had taint" → Add toleration
│   ├── "PVC not found" → Create PVC
│   └── No events → Check API server
│
└── No → Check Container Status
    ├── ImagePullBackOff → Fix image name/auth
    ├── CrashLoopBackOff → Check logs --previous
    ├── CreateContainerConfigError → Fix ConfigMap/Secret
    └── Running but not ready → Check readiness probe
```

### Application Not Responding

```
Can reach Service?
├── No → Check Service
│   ├── No endpoints → Fix selector labels
│   ├── Wrong port → Fix targetPort
│   └── NetworkPolicy blocking → Adjust policy
│
└── Yes → Check Pod
    ├── Probe failing → Fix probe or application
    ├── High latency → Check resources, dependencies
    └── Errors in logs → Fix application
```

## Performance Analysis

### Resource Optimization

```bash
# Compare usage vs requests
kubectl top pods -n ${NS}

kubectl get pods -n ${NS} -o custom-columns=\
NAME:.metadata.name,\
CPU_REQ:.spec.containers[*].resources.requests.cpu,\
MEM_REQ:.spec.containers[*].resources.requests.memory

# Find pods without limits
kubectl get pods -A -o json | jq -r \
  '.items[] | select(.spec.containers[].resources.limits == null) |
   "\(.metadata.namespace)/\(.metadata.name)"'
```

### Right-Sizing Recommendations

| Symptom | Indication | Action |
|---------|------------|--------|
| CPU throttling | CPU limit too low | Increase CPU limit |
| OOMKilled | Memory limit too low | Increase memory limit |
| Low utilization | Over-provisioned | Reduce requests |
