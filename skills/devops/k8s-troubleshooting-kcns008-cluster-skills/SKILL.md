---
name: k8s-troubleshooting
description: |
  Comprehensive Kubernetes and OpenShift cluster health analysis and troubleshooting based on Popeye's issue detection patterns. Use this skill when:
  (1) Proactive cluster health assessment and security analysis
  (2) Analyzing pod/container logs for errors or issues
  (3) Interpreting cluster events (kubectl get events)
  (4) Debugging pod failures: CrashLoopBackOff, ImagePullBackOff, OOMKilled, etc.
  (5) Diagnosing networking issues: DNS, Service connectivity, Ingress/Route problems
  (6) Investigating storage issues: PVC pending, mount failures
  (7) Analyzing node problems: NotReady, resource pressure, taints
  (8) Troubleshooting OCP-specific issues: SCCs, Routes, Operators, Builds
  (9) Performance analysis and resource optimization
  (10) Security vulnerability assessment and RBAC validation
  (11) Configuration best practices validation
  (12) Reliability and high availability analysis
---

# Kubernetes / OpenShift Troubleshooting Guide

## Current Versions & Troubleshooting Tools (January 2026)

| Platform | Version | Key Changes |
|----------|---------|-------------|
| **Kubernetes** | 1.31.x | Sidecar containers GA, Pod lifecycle improvements |
| **OpenShift** | 4.17.x | OVN-Kubernetes default, enhanced web terminal |
| **EKS** | 1.31 | Pod Identity, Auto Mode, Karpenter 1.x |
| **AKS** | 1.31 | Cilium CNI, Workload Identity GA |
| **GKE** | 1.31 | Autopilot improvements, Gateway API GA |

### Troubleshooting Tools & CLIs

| Tool | Version | Install | Purpose |
|------|---------|---------|--------|
| **kubectl** | 1.31.x | `brew install kubectl` | Cluster operations |
| **oc** | 4.17.x | `brew install openshift-cli` | OpenShift operations |
| **k9s** | 0.32.x | `brew install k9s` | Terminal UI |
| **stern** | 1.30.x | `brew install stern` | Multi-pod log tailing |
| **kubectx/kubens** | 0.9.x | `brew install kubectx` | Context/namespace switching |
| **krew** | 0.4.x | kubectl plugin manager | Plugin ecosystem |
| **kubectl-node-shell** | - | `kubectl krew install node-shell` | Node access |
| **kubectl-neat** | - | `kubectl krew install neat` | Clean YAML output |
| **kubectl-tree** | - | `kubectl krew install tree` | Resource hierarchy |

```bash
# Essential CLI tool installation
brew install kubectl kubectx k9s stern

# Install krew (kubectl plugin manager)
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/arm64/arm64/')" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/krew-${OS}_${ARCH}.tar.gz" &&
  tar zxvf krew-${OS}_${ARCH}.tar.gz &&
  KREW=./krew-${OS}_${ARCH} && "$KREW" install krew
)

# Install useful kubectl plugins
kubectl krew install ctx ns neat tree node-shell images lineage

# Multi-pod log streaming with stern
stern -n ${NAMESPACE} ${POD_PREFIX}
stern -A -l app=${APP_NAME} --since 1h

# Interactive cluster navigation with k9s
k9s -n ${NAMESPACE}
k9s --context ${CONTEXT}
```

## Command Usage Convention

**IMPORTANT**: This skill uses `kubectl` as the primary command in all examples. When working with:
- **OpenShift/ARO clusters**: Replace all `kubectl` commands with `oc`
- **Standard Kubernetes clusters (AKS, EKS, GKE, etc.)**: Use `kubectl` as shown

The agent will automatically detect the cluster type and use the appropriate command.

Systematic approach to diagnosing and resolving cluster issues through event analysis, log interpretation, and root cause identification.

## Proactive Cluster Health Analysis (Popeye-Style)

### Cluster Scoring Framework

Popeye uses a health scoring system (0-100) to assess cluster health. Critical issues reduce the score significantly:

- **BOOM (Critical)**: -50 points - Security vulnerabilities, resource exhaustion, failed services
- **WARN (Warning)**: -20 points - Configuration inefficiencies, best practice violations
- **INFO (Informational)**: -5 points - Non-critical issues, optimization opportunities

### Quick Cluster Health Assessment

```bash
#!/bin/bash
# Comprehensive cluster health check based on Popeye patterns
echo "=== POPEYE-STYLE CLUSTER HEALTH ASSESSMENT ==="

# 1. Node Health Check
echo "### NODE HEALTH (Critical Weight: 1.0) ###"
kubectl get nodes -o wide | grep -E "NotReady|Unknown" && echo "BOOM: Unhealthy nodes detected!" || echo "✓ All nodes healthy"

# 2. Pod Issues Check
echo -e "\n### POD HEALTH (Critical Weight: 1.0) ###"
POD_ISSUES=$(kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded --no-headers | wc -l)
if [ $POD_ISSUES -gt 0 ]; then
    echo "WARN: $POD_ISSUES pods not running"
    kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded
else
    echo "✓ All pods running"
fi

# 3. Security Issues Check
echo -e "\n### SECURITY ASSESSMENT (Critical Weight: 1.0) ###"
# Check for privileged containers
PRIVILEGED=$(kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].securityContext.privileged == true) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $PRIVILEGED -gt 0 ]; then
    echo "BOOM: $PRIVILEGED privileged containers detected (Security Risk!)"
else
    echo "✓ No privileged containers found"
fi

# Check for containers running as root
ROOT_CONTAINERS=$(kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].securityContext.runAsUser == 0) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $ROOT_CONTAINERS -gt 0 ]; then
    echo "WARN: $ROOT_CONTAINERS containers running as root"
else
    echo "✓ No containers running as root"
fi

# 4. Resource Configuration Check
echo -e "\n### RESOURCE CONFIGURATION (Warning Weight: 0.8) ###"
NO_LIMITS=$(kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].resources.limits == null) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $NO_LIMITS -gt 0 ]; then
    echo "WARN: $NO_LIMITS containers without resource limits"
else
    echo "✓ All containers have resource limits"
fi

# 5. Storage Issues Check
echo -e "\n### STORAGE HEALTH (Warning Weight: 0.5) ###"
PENDING_PVC=$(kubectl get pvc -A --field-selector=status.phase!=Bound --no-headers | wc -l)
if [ $PENDING_PVC -gt 0 ]; then
    echo "WARN: $PENDING_PVC PVCs not bound"
    kubectl get pvc -A --field-selector=status.phase!=Bound
else
    echo "✓ All PVCs bound"
fi

# 6. Network Issues Check
echo -e "\n### NETWORKING (Warning Weight: 0.5) ###"
# Check services without endpoints
EMPTY_ENDPOINTS=$(kubectl get svc -A -o json | jq -r '.items[] | select(.spec.clusterIP != "None") | select(.status.loadBalancer.ingress == null) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $EMPTY_ENDPOINTS -gt 0 ]; then
    echo "WARN: $EMPTY_ENDPOINTS services may have endpoint issues"
else
    echo "✓ Services appear healthy"
fi

# OpenShift specific checks
if command -v oc &> /dev/null; then
    echo -e "\n### OPENSHIFT CLUSTER OPERATORS (Critical Weight: 1.0) ###"
    DEGRADED=$(oc get clusteroperators --no-headers | grep -c -E "False.*True|False.*False")
    if [ $DEGRADED -gt 0 ]; then
        echo "BOOM: $DEGRADED cluster operators degraded/unavailable"
        oc get clusteroperators | grep -E "False.*True|False.*False"
    else
        echo "✓ All cluster operators healthy"
    fi
fi
```

### Security Vulnerability Detection

#### Container Security Analysis
```bash
# Security Context Validation
echo "=== CONTAINER SECURITY ANALYSIS ==="

# 1. Privileged Containers (Critical)
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{range .spec.containers[*]}{.name}{"\t"}{.securityContext.privileged}{"\n"}{end}{end}' | grep "true" && echo "BOOM: Privileged containers found!" || echo "✓ No privileged containers"

# 2. Host Namespace Access (Critical)
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.hostNetwork}{"\t"}{.spec.hostPID}{"\t"}{.spec.hostIPC}{"\n"}' | grep -E "true.*true|true$|true\s" && echo "BOOM: Host namespace access detected!" || echo "✓ No host namespace access"

# 3. Capabilities Check (Warning)
kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].securityContext.capabilities.add != null) | "\(.metadata.namespace)/\(.metadata.name): \(.spec.containers[].securityContext.capabilities.add[])"'

# 4. Read-Only Root Filesystem (Warning)
READONLY_ISSUES=$(kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].securityContext.readOnlyRootFilesystem == false) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
echo "INFO: $READONLY_ISSUES containers without read-only root filesystem"
```

#### RBAC Security Analysis
```bash
echo "=== RBAC SECURITY ANALYSIS ==="

# Check for overly permissive roles
kubectl get clusterroles -o json | jq -r '.items[] | select(.rules[].verbs[] == "*") | "\(.metadata.name): Wildcard permissions detected"'

# Check service account permissions
kubectl get serviceaccounts -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name)"'
```

### Performance Issues Detection

#### Resource Utilization Analysis
```bash
echo "=== PERFORMANCE ANALYSIS ==="

# Find pods approaching memory limits
kubectl top pods -A --no-headers | awk '{print $4}' | sed 's/Mi//' | while read mem; do
    if [ "$mem" -gt 900 ]; then
        echo "WARN: Pod using high memory: ${mem}Mi"
    fi
done

# CPU throttling detection
kubectl top pods -A --no-headers | awk '{print $3}' | sed 's/m//' | while read cpu; do
    if [ "$cpu" -gt 900 ]; then
        echo "WARN: Pod using high CPU: ${cpu}m"
    fi
done
```

### Configuration Best Practices Validation

#### Deployment Health Checks
```bash
echo "=== DEPLOYMENT BEST PRACTICES ==="

# Check for liveness/readiness probes
NO_PROBES=$(kubectl get deployments -A -o json | jq -r '.items[] | select(.spec.template.spec.containers[].livenessProbe == null or .spec.template.spec.containers[].readinessProbe == null) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
echo "INFO: $NO_PROBES deployments missing health probes"

# Check for pod disruption budgets
PDB_COUNT=$(kubectl get pdb -A --no-headers | wc -l)
DEPLOY_COUNT=$(kubectl get deployments -A --no-headers | wc -l)
echo "INFO: $PDB_COUNT pod disruption budgets for $DEPLOY_COUNT deployments"

# Rolling update strategy
NO_STRATEGY=$(kubectl get deployments -A -o json | jq -r '.items[] | select(.spec.strategy.type != "RollingUpdate") | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
echo "INFO: $NO_STRATEGY deployments not using RollingUpdate"
```

## Troubleshooting Workflow

1. **Identify Scope**: Pod, Node, Namespace, or Cluster-wide issue?
2. **Gather Context**: Events, logs, resource status, recent changes
3. **Analyze Symptoms**: Match patterns to known issues
4. **Determine Root Cause**: Follow diagnostic tree
5. **Remediate**: Apply fix and verify resolution
6. **Document**: Record findings for future reference

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

# Node status
kubectl get nodes -o wide
kubectl describe node ${NODE_NAME}

# Resource usage
kubectl top pods -n ${NAMESPACE}
kubectl top nodes

# OpenShift specific
oc get events -n ${NAMESPACE}
oc adm top pods -n ${NAMESPACE}
oc get clusteroperators
oc adm node-logs ${NODE_NAME} -u kubelet
```

### Cloud Provider Specific Commands

```bash
# EKS Troubleshooting (AWS)
aws eks describe-cluster --name ${CLUSTER} --query 'cluster.status'
aws eks describe-addon --cluster-name ${CLUSTER} --addon-name vpc-cni --query 'addon.status'
eksctl utils describe-stacks --cluster ${CLUSTER}
exportctl get nodegroup --cluster ${CLUSTER}

# EKS Pod Identity issues
aws eks describe-pod-identity-association --cluster-name ${CLUSTER} --association-id ${ASSOC_ID}

# EKS CloudWatch Logs Insights query for control plane logs
aws logs filter-log-events --log-group-name /aws/eks/${CLUSTER}/cluster \
  --filter-pattern "ERROR" --start-time ${TIMESTAMP}

# AKS Troubleshooting (Azure)
az aks show --resource-group ${RG} --name ${CLUSTER} --query provisioningState
az aks get-credentials --resource-group ${RG} --name ${CLUSTER} --admin
az aks browse --resource-group ${RG} --name ${CLUSTER}  # Opens dashboard

# AKS diagnostic logs
az aks kollect --resource-group ${RG} --name ${CLUSTER} --storage-account ${STORAGE}
az aks check-network outbound --resource-group ${RG} --name ${CLUSTER}

# AKS Workload Identity issues
az aks show --resource-group ${RG} --name ${CLUSTER} --query 'oidcIssuerProfile'

# GKE Troubleshooting (Google Cloud)
gcloud container clusters describe ${CLUSTER} --region ${REGION} --format='value(status)'
gcloud container clusters get-credentials ${CLUSTER} --region ${REGION}

# GKE operations and errors
gcloud container operations list --filter="targetLink:${CLUSTER}" --sort-by="~startTime" --limit=10
gcloud container operations describe ${OPERATION_ID} --region ${REGION}

# GKE Workload Identity issues
gcloud iam service-accounts get-iam-policy ${GSA_EMAIL}

# GKE node pool issues
gcloud container node-pools describe ${POOL} --cluster ${CLUSTER} --region ${REGION}

# ARO Troubleshooting (Azure Red Hat OpenShift)
az aro show --resource-group ${RG} --name ${CLUSTER} --query provisioningState
az aro list-credentials --resource-group ${RG} --name ${CLUSTER}
az aro show --resource-group ${RG} --name ${CLUSTER} --query 'networkProfile'

# ROSA Troubleshooting (Red Hat OpenShift on AWS)
rosa describe cluster --cluster ${CLUSTER}
rosa logs install --cluster ${CLUSTER}
rosa logs uninstall --cluster ${CLUSTER}
rosa list machinepools --cluster ${CLUSTER}
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

### Container State Analysis

#### Waiting States

| Reason | Cause | Resolution |
|--------|-------|------------|
| `ContainerCreating` | Setting up container | Check events for errors, volume mounts |
| `ImagePullBackOff` | Cannot pull image | Verify image name, registry access, credentials |
| `ErrImagePull` | Image pull failed | Check image exists, network, ImagePullSecrets |
| `CreateContainerConfigError` | Config error | Check ConfigMaps, Secrets exist and mounted correctly |
| `InvalidImageName` | Malformed image reference | Fix image name in spec |
| `CrashLoopBackOff` | Container repeatedly crashing | Check logs --previous, fix application |

#### Terminated States

| Reason | Exit Code | Cause | Resolution |
|--------|-----------|-------|------------|
| `OOMKilled` | 137 | Memory limit exceeded | Increase memory limit, fix memory leak |
| `Error` | 1 | Application error | Check logs for stack trace |
| `Error` | 126 | Command not executable | Fix command/entrypoint permissions |
| `Error` | 127 | Command not found | Fix command path, verify image contents |
| `Error` | 128 | Invalid exit code | Application bug |
| `Error` | 130 | SIGINT (Ctrl+C) | Normal if manual termination |
| `Error` | 137 | SIGKILL | OOM or forced termination |
| `Error` | 143 | SIGTERM | Graceful shutdown requested |
| `Completed` | 0 | Normal exit | Expected for Jobs/init containers |

## Event Analysis

### Event Types and Severity

```
Type: Normal   → Informational, typically no action needed
Type: Warning  → Potential issue, investigate
```

### Critical Events to Monitor

#### Pod Scheduling Events

| Event Reason | Meaning | Resolution |
|--------------|---------|------------|
| `FailedScheduling` | Cannot place pod | Check node resources, taints, affinity |
| `Unschedulable` | No suitable node | Add nodes, adjust requirements |
| `NodeNotReady` | Target node unavailable | Check node status |
| `TaintManagerEviction` | Pod evicted due to taint | Check node taints, add tolerations |

**FailedScheduling Analysis:**
```
# Common messages and fixes:
"Insufficient cpu"           → Reduce requests or add capacity
"Insufficient memory"        → Reduce requests or add capacity  
"node(s) had taint"          → Add toleration or remove taint
"node(s) didn't match selector" → Fix nodeSelector/affinity
"persistentvolumeclaim not found" → Create PVC or fix name
"0/3 nodes available"        → All nodes have issues, check each
```

#### Image Events

| Event Reason | Meaning | Resolution |
|--------------|---------|------------|
| `Pulling` | Downloading image | Normal, wait |
| `Pulled` | Image downloaded | Normal |
| `Failed` | Pull failed | Check image name, registry, auth |
| `BackOff` | Repeated pull failures | Fix underlying issue |
| `ErrImageNeverPull` | Image not local with Never policy | Change imagePullPolicy or pre-pull |

**ImagePullBackOff Diagnosis:**
```bash
# Check image name is correct
kubectl get pod ${POD} -o jsonpath='{.spec.containers[*].image}'

# Verify ImagePullSecrets
kubectl get pod ${POD} -o jsonpath='{.spec.imagePullSecrets}'
kubectl get secret ${SECRET} -n ${NAMESPACE}

# Test registry access
kubectl run test --image=${IMAGE} --restart=Never --rm -it -- /bin/sh
```

#### Volume Events

| Event Reason | Meaning | Resolution |
|--------------|---------|------------|
| `FailedMount` | Cannot mount volume | Check PVC, storage class, permissions |
| `FailedAttachVolume` | Cannot attach volume | Check cloud provider, volume exists |
| `VolumeResizeFailed` | Cannot expand volume | Check storage class allows expansion |
| `ProvisioningFailed` | Cannot create volume | Check storage class, quotas |

**PVC Pending Diagnosis:**
```bash
# Check PVC status and events
kubectl describe pvc ${PVC_NAME} -n ${NAMESPACE}

# Verify StorageClass exists and is default
kubectl get storageclass

# Check for available PVs (if not dynamic provisioning)
kubectl get pv

# OpenShift: Check storage operator
oc get clusteroperator storage
```

#### Container Events

| Event Reason | Meaning | Resolution |
|--------------|---------|------------|
| `Created` | Container created | Normal |
| `Started` | Container started | Normal |
| `Killing` | Container being stopped | Normal during updates/scale-down |
| `Unhealthy` | Probe failed | Fix probe or application |
| `ProbeWarning` | Probe returned warning | Check probe configuration |
| `BackOff` | Container crashing | Check logs, fix application |

### Event Patterns

#### Flapping Pod (Repeated restarts)
```
Events:
  Warning  BackOff    Container is in waiting state due to CrashLoopBackOff
  Normal   Pulled     Container image already present
  Normal   Created    Created container
  Normal   Started    Started container
  Warning  BackOff    Back-off restarting failed container
```
**Diagnosis**: Check `kubectl logs --previous`, application is crashing on startup.

#### Resource Starvation
```
Events:
  Warning  FailedScheduling  0/3 nodes are available: 3 Insufficient cpu
```
**Diagnosis**: Cluster needs more capacity or pod requests are too high.

#### Probe Failures
```
Events:
  Warning  Unhealthy  Liveness probe failed: HTTP probe failed with statuscode: 503
  Normal   Killing    Container failed liveness probe, will be restarted
```
**Diagnosis**: Application not responding, check if startup is slow (use startupProbe) or app is unhealthy.

## Log Analysis Patterns

### Common Error Patterns

#### Application Startup Failures
```
# Java
java.lang.OutOfMemoryError: Java heap space
→ Increase memory limit, tune JVM heap (-Xmx)

java.net.ConnectException: Connection refused
→ Dependency not ready, add init container or retry logic

# Python
ModuleNotFoundError: No module named 'xxx'
→ Missing dependency, fix requirements.txt/Dockerfile

# Node.js
Error: Cannot find module 'xxx'
→ Missing dependency, fix package.json or node_modules

# General
ECONNREFUSED, Connection refused
→ Service dependency not available

ENOTFOUND, getaddrinfo ENOTFOUND
→ DNS resolution failed, check service name
```

#### Database Connection Issues
```
# PostgreSQL
FATAL: password authentication failed
→ Wrong credentials, check Secret values

connection refused
→ Database not running or wrong host/port

too many connections
→ Connection pool exhaustion, configure pool size

# MySQL
Access denied for user
→ Wrong credentials or missing grants

Can't connect to MySQL server
→ Database not running or network issue

# MongoDB
MongoNetworkError
→ Connection string wrong or network issue
```

#### Memory Issues
```
# Container OOMKilled
Last State: Terminated
Reason: OOMKilled
Exit Code: 137

→ Solutions:
1. Increase memory limit
2. Profile application memory usage
3. Fix memory leaks
4. For JVM: Set -Xmx < container limit (leave ~25% headroom)
```

#### Permission Issues
```
# File system
Permission denied
mkdir: cannot create directory: Permission denied
→ Check securityContext, runAsUser, fsGroup

# OpenShift SCC
Error: container has runAsNonRoot and image has non-numeric user
→ Add runAsUser to securityContext

pods "xxx" is forbidden: unable to validate against any security context constraint
→ Create appropriate SCC or use service account with SCC access
```

### Log Analysis Commands

```bash
# Search for errors in logs
kubectl logs ${POD} -n ${NS} | grep -iE "(error|exception|fatal|panic)"

# Follow logs in real-time
kubectl logs -f ${POD} -n ${NS}

# Logs from all containers in pod
kubectl logs ${POD} -n ${NS} --all-containers

# Logs from multiple pods (by label)
kubectl logs -l app=${APP_NAME} -n ${NS} --all-containers

# Logs with timestamps
kubectl logs ${POD} -n ${NS} --timestamps

# Logs from last hour
kubectl logs ${POD} -n ${NS} --since=1h

# Logs from last 100 lines
kubectl logs ${POD} -n ${NS} --tail=100

# OpenShift: Node-level logs
oc adm node-logs ${NODE} -u kubelet
oc adm node-logs ${NODE} -u crio
oc adm node-logs ${NODE} --path=journal
```

## Node Troubleshooting

### Node Conditions

| Condition | Status | Meaning |
|-----------|--------|---------|
| `Ready` | True | Node healthy |
| `Ready` | False | Kubelet not healthy |
| `Ready` | Unknown | No heartbeat from node |
| `MemoryPressure` | True | Low memory |
| `DiskPressure` | True | Low disk space |
| `PIDPressure` | True | Too many processes |
| `NetworkUnavailable` | True | Network not configured |

### Node NotReady Diagnosis

```bash
# Check node status
kubectl describe node ${NODE_NAME}

# Check kubelet status (SSH to node or via oc adm)
systemctl status kubelet
journalctl -u kubelet -f

# Check container runtime
systemctl status crio  # or containerd/docker
journalctl -u crio -f

# Check node resources
df -h
free -m
top

# OpenShift: Machine status
oc get machines -n openshift-machine-api
oc describe machine ${MACHINE} -n openshift-machine-api
```

### Node Resource Pressure

```bash
# Check resource allocation vs capacity
kubectl describe node ${NODE} | grep -A 10 "Allocated resources"

# Find pods using most resources
kubectl top pods -A --sort-by=cpu
kubectl top pods -A --sort-by=memory

# Evict pods from node (drain)
kubectl drain ${NODE} --ignore-daemonsets --delete-emptydir-data
```

## Networking Troubleshooting

### DNS Issues

```bash
# Test DNS resolution from a debug pod
kubectl run dns-test --image=busybox:1.28 --rm -it --restart=Never -- nslookup ${SERVICE_NAME}
kubectl run dns-test --image=busybox:1.28 --rm -it --restart=Never -- nslookup ${SERVICE_NAME}.${NAMESPACE}.svc.cluster.local

# Check CoreDNS/DNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns

# Check DNS service
kubectl get svc -n kube-system kube-dns
```

### Service Connectivity

```bash
# Verify service exists and has endpoints
kubectl get svc ${SERVICE} -n ${NS}
kubectl get endpoints ${SERVICE} -n ${NS}

# Test service from debug pod
kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never -- \
  curl -v http://${SERVICE}.${NS}.svc.cluster.local:${PORT}

# Check if pods match service selector
kubectl get pods -n ${NS} -l ${SELECTOR} -o wide
```

### Ingress/Route Issues

```bash
# Check Ingress status
kubectl describe ingress ${INGRESS} -n ${NS}

# Check Ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# OpenShift Route
oc describe route ${ROUTE} -n ${NS}
oc get route ${ROUTE} -n ${NS} -o yaml

# Check router pods
oc get pods -n openshift-ingress
oc logs -n openshift-ingress -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default
```

### NetworkPolicy Debugging

```bash
# List NetworkPolicies affecting a pod
kubectl get networkpolicy -n ${NS}

# Test connectivity with ephemeral debug container
kubectl debug ${POD} -n ${NS} --image=nicolaka/netshoot -- \
  curl -v http://${TARGET_SERVICE}:${PORT}

# Check if traffic is blocked (look for drops)
# On node running the pod:
conntrack -L | grep ${POD_IP}
```

## OpenShift-Specific Troubleshooting

### Comprehensive OpenShift Health Assessment (Popeye-Style)

```bash
#!/bin/bash
# OpenShift comprehensive health check
echo "=== OPENSHIFT COMPREHENSIVE HEALTH ASSESSMENT ==="

# 1. Cluster Operators Health (Critical)
echo "### CLUSTER OPERATORS (Critical Weight: 1.0) ###"
oc get clusteroperators
echo ""
DEGRADED_OPERATORS=$(oc get clusteroperators --no-headers | grep -c -E "False.*True|False.*False")
if [ $DEGRADED_OPERATORS -gt 0 ]; then
    echo "BOOM: $DEGRADED_OPERATORS cluster operators in degraded state!"
    oc get clusteroperators | grep -E "False.*True|False.*False"
else
    echo "✓ All cluster operators healthy"
fi

# 2. OpenShift Routes Analysis (Warning)
echo -e "\n### ROUTES ANALYSIS (Warning Weight: 0.5) ###"
ROUTE_ISSUES=$(oc get routes -A -o json | jq -r '.items[] | select(.status.ingress == null) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $ROUTE_ISSUES -gt 0 ]; then
    echo "WARN: $ROUTE_ISSUES routes without endpoints"
else
    echo "✓ All routes have endpoints"
fi

# Check TLS certificate issues
EXPIRED_CERTS=$(oc get routes -A -o json | jq -r '.items[] | select(.spec.tls != null) | select(.status.ingress[].conditions[]?.type == "Admitted" and .status.ingress[].conditions[]?.status == "False") | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $EXPIRED_CERTS -gt 0 ]; then
    echo "WARN: $EXPIRED_CERTS routes with TLS issues"
fi

# 3. BuildConfig Health Analysis (Warning)
echo -e "\n### BUILDCONFIG ANALYSIS (Warning Weight: 0.5) ###"
FAILED_BUILDS=$(oc get builds -A --field-selector=status.phase!=Failed --no-headers | wc -l)
echo "INFO: $FAILED_BUILDS failed builds detected"

# Check BuildConfig strategies
BUILDCONFIGS=$(oc get buildconfigs -A --no-headers | wc -l)
echo "INFO: $BUILDCONFIGS build configurations found"

# 4. Security Context Constraints (Critical)
echo -e "\n### SCC ANALYSIS (Critical Weight: 1.0) ###"
SCC_VIOLATIONS=$(oc get events -A --field-selector=reason=FailedScheduling --no-headers | grep -c "unable to validate against any security context constraint")
if [ $SCC_VIOLATIONS -gt 0 ]; then
    echo "BOOM: $SCC_VIOLATIONS SCC violations detected!"
    oc get events -A --field-selector=reason=FailedScheduling | grep "unable to validate against any security context constraint"
else
    echo "✓ No SCC violations detected"
fi

# 5. ImageStream Health (Warning)
echo -e "\n### IMAGESTREAM ANALYSIS (Warning Weight: 0.3) ###"
STALE_IMAGES=$(oc get imagestreams -A -o json | jq -r '.items[] | select(.status.tags[]?.items? | length == 0) | "\(.metadata.namespace)/\(.metadata.name)"' | wc -l)
if [ $STALE_IMAGES -gt 0 ]; then
    echo "WARN: $STALE_IMAGES ImageStreams without images"
else
    echo "✓ All ImageStreams have images"
fi

# 6. Project Resource Quotas (Warning)
echo -e "\n### PROJECT QUOTAS (Warning Weight: 0.5) ###"
oc get projects -A -o json | jq -r '.items[] | "\(.metadata.name): \(.status.phase)"' | while read project_info; do
    project=$(echo $project_info | cut -d: -f1)
    phase=$(echo $project_info | cut -d: -f2)
    if [ "$phase" == "Active" ]; then
        echo "✓ Project $project is active"
    else
        echo "WARN: Project $project is $phase"
    fi
done
```

### Cluster Operators

```bash
# Check overall cluster health
oc get clusteroperators

# Investigate degraded operator
oc describe clusteroperator ${OPERATOR}

# Check operator logs
oc logs -n openshift-${OPERATOR} -l name=${OPERATOR}-operator

# OpenShift-specific: Check co-reconcile events
oc get events -A --field-selector reason=OperatorStatusChanged
```

### Security Context Constraints (SCC)

```bash
# List SCCs
oc get scc

# Check which SCC a pod is using
oc get pod ${POD} -n ${NS} -o yaml | grep scc

# Check which SCC a serviceaccount can use
oc adm policy who-can use scc restricted-v2

# Add SCC to service account (requires admin)
oc adm policy add-scc-to-user ${SCC} -z ${SERVICE_ACCOUNT} -n ${NS}
```

**Common SCC Issues:**
```
Error: pods "xxx" is forbidden: unable to validate against any security context constraint

→ Diagnosis:
1. Check pod securityContext requirements
2. Find compatible SCC: oc get scc
3. Grant SCC to service account or adjust pod spec

Common fixes:
- Add runAsUser to match SCC requirements
- Use less restrictive SCC (not recommended for prod)
- Create custom SCC for specific needs
```

### Build Failures

```bash
# Check build status
oc get builds -n ${NS}
oc describe build ${BUILD} -n ${NS}

# Build logs
oc logs build/${BUILD} -n ${NS}
oc logs -f bc/${BUILDCONFIG} -n ${NS}

# Check builder pod
oc get pods -n ${NS} | grep build
oc describe pod ${BUILD_POD} -n ${NS}
```

**Common Build Issues:**
| Error | Cause | Resolution |
|-------|-------|------------|
| `error: build error: image not found` | Base image missing | Check ImageStream or external registry |
| `AssembleInputError` | S2I assemble failed | Check application dependencies |
| `GenericBuildFailed` | Build command failed | Check build logs for details |
| `PushImageToRegistryFailed` | Cannot push to registry | Check registry access, quotas |

### ImageStream Issues

```bash
# Check ImageStream
oc get is ${IS_NAME} -n ${NS}
oc describe is ${IS_NAME} -n ${NS}

# Import external image
oc import-image ${IS_NAME}:${TAG} --from=${EXTERNAL_IMAGE} --confirm -n ${NS}

# Check image import status
oc get imagestreamtag ${IS_NAME}:${TAG} -n ${NS}
```

## Performance Analysis

### Resource Optimization

```bash
# Get actual resource usage vs requests
kubectl top pods -n ${NS}

# Compare with requests/limits
kubectl get pods -n ${NS} -o custom-columns=\
NAME:.metadata.name,\
CPU_REQ:.spec.containers[*].resources.requests.cpu,\
CPU_LIM:.spec.containers[*].resources.limits.cpu,\
MEM_REQ:.spec.containers[*].resources.requests.memory,\
MEM_LIM:.spec.containers[*].resources.limits.memory

# Find pods without resource limits
kubectl get pods -A -o json | jq -r \
  '.items[] | select(.spec.containers[].resources.limits == null) | 
   "\(.metadata.namespace)/\(.metadata.name)"'
```

### Right-Sizing Recommendations

| Symptom | Indication | Action |
|---------|------------|--------|
| CPU throttling, high latency | CPU limit too low | Increase CPU limit |
| OOMKilled frequently | Memory limit too low | Increase memory limit |
| Low CPU utilization | Over-provisioned | Reduce CPU request |
| Low memory utilization | Over-provisioned | Reduce memory request |
| Pending pods | Cluster capacity full | Add nodes or optimize |

### Latency Investigation

```bash
# Check pod startup time
kubectl get pod ${POD} -n ${NS} -o jsonpath='{.status.conditions}'

# Check container startup
kubectl get pod ${POD} -n ${NS} -o jsonpath='{.status.containerStatuses[*].state}'

# Slow image pulls
kubectl describe pod ${POD} -n ${NS} | grep -A 5 "Events"

# Network latency test
kubectl run nettest --image=nicolaka/netshoot --rm -it --restart=Never -- \
  curl -w "@curl-format.txt" -o /dev/null -s http://${SERVICE}:${PORT}
```

## Popeye-Style Diagnostic Decision Trees

### Comprehensive Cluster Health Assessment Tree

```
Cluster Health Score < 80?
├── Yes → Check Critical Issues (BOOM: -50 points each)
│   ├── Node Health Issues?
│   │   ├── NotReady nodes → kubelet problems, resource pressure
│   │   ├── Unknown nodes → Network connectivity, API server
│   │   └── Resource pressure → CPU/Memory/Disk pressure
│   ├── Security Vulnerabilities?
│   │   ├── Privileged containers → Remove privileged flag
│   │   ├── Host namespace access → Remove hostNetwork/hostPID/hostIPC
│   │   ├── Run as root → Set runAsNonRoot: true, runAsUser > 0
│   │   └── Wildcard RBAC → Create specific roles with minimal permissions
│   ├── Service Failures?
│   │   ├── No endpoints → Fix service selector or pod labels
│   │   ├── Failed load balancers → Check cloud provider quotas
│   │   └── Certificate issues → Renew TLS certificates
│   └── Resource Exhaustion?
│       ├── OOMKilled pods → Increase memory limits
│       ├── CPU throttling → Increase CPU limits
│       └── Storage full → Clean up or expand storage
├── No → Check Warning Issues (WARN: -20 points each)
│   ├── Configuration Issues?
│   │   ├── No resource limits → Add requests/limits
│   │   ├── No health probes → Add liveness/readiness probes
│   │   ├── Missing PDBs → Create PodDisruptionBudgets
│   │   └── No rolling updates → Use RollingUpdate strategy
│   ├── Performance Issues?
│   │   ├── Underutilized resources → Right-size pods
│   │   ├── Large container images → Optimize Dockerfile
│   │   └── Inefficient scheduling → Add affinity/anti-affinity
│   └── Reliability Issues?
│       ├── Single replicas → Increase replica count
│       ├── No backup strategy → Implement backup solution
│       └── Missing monitoring → Add metrics and logging
└── Score >= 80 → Check Info Issues (INFO: -5 points each)
    ├── Best Practice Violations?
    │   ├── Missing labels → Add standard labels
    │   ├── No termination grace → Set terminationGracePeriodSeconds
    │   └── Deprecated APIs → Update to newer API versions
    └── Optimization Opportunities?
        ├── Unused resources → Clean up orphaned resources
        ├── ImagePullPolicy: Always → Use IfNotPresent for production
        └── Large logs → Implement log rotation
```

### Pod Not Starting - Enhanced Diagnostic Tree

```
Pod Phase = Pending?
├── Yes → Check Scheduling Issues
│   ├── Events: FailedScheduling?
│   │   ├── "Insufficient cpu/memory" →
│   │   │   ├── Add nodes OR
│   │   │   ├── Reduce resource requests OR
│   │   │   └── Enable cluster autoscaler
│   │   ├── "node(s) had taint" →
│   │   │   ├── Add toleration to pod OR
│   │   │   └── Remove taint from node
│   │   ├── "node(s) didn't match nodeSelector" →
│   │   │   ├── Fix nodeSelector labels OR
│   │   │   └── Update node labels
│   │   ├── "persistentvolumeclaim not found" →
│   │   │   ├── Create PVC with correct name OR
│   │   │   └── Fix PVC reference in pod
│   │   └── "0/X nodes available" → Check all nodes for issues
│   └── No FailedScheduling events?
│       ├── Check ResourceQuota → Quota exceeded?
│       ├── Check LimitRange → Requests too small/large?
│       └── Check Namespace → Namespace exists and not terminating?
└── No → Pod Phase = Running with issues?
    ├── ContainerCreating > 5min?
    │   ├── Events: ImagePullBackOff?
    │   │   ├── Check image name/registry → Fix image reference
    │   │   ├── Check ImagePullSecrets → Create/update secrets
    │   │   └── Test registry access → kubectl run test-pod --image=xxx
    │   ├── Events: FailedMount?
    │   │   ├── PVC not bound → Create PV or fix StorageClass
    │   │   ├── Secret/ConfigMap not found → Create missing resources
    │   │   └── Permission denied → Fix securityContext, fsgroup
    │   └── Events: CreateContainerConfigError?
    │       ├── Missing ConfigMap → Create ConfigMap
    │       ├── Invalid volume mount → Fix volumeMount path
    │       └── Security context violation → Adjust SCC or securityContext
    └── Container status: Waiting/CrashLoopBackOff?
        ├── Exit code analysis:
        │   ├── 137 (OOMKilled) → Increase memory limit
        │   ├── 1 (General error) → Check application logs
        │   ├── 125/126/127 (Command issues) → Fix entrypoint/command
        │   └── 143 (SIGTERM) → Graceful shutdown issue
        └── No previous logs?
            ├── Application starts too slowly → Add startupProbe
            ├── Entrypoint command not found → Fix Dockerfile CMD/ENTRYPOINT
            └── Permission denied → Fix file permissions in image
```

### Security Issues Diagnostic Tree

```
Security Issues Detected?
├── Privileged Containers (Critical)?
│   ├── Find: kubectl get pods -A -o json | jq 'select(.spec.containers[].securityContext.privileged == true)'
│   ├── Why: Dangerous escape from container isolation
│   └── Fix: Set privileged: false or use least privileged SCC
├── Host Namespace Access (Critical)?
│   ├── Check: hostNetwork, hostPID, hostIPC = true
│   ├── Why: Access to host system resources
│   └── Fix: Remove host namespace access, use specific alternatives
├── Root User Execution (Warning)?
│   ├── Check: runAsUser = 0 or no runAsNonRoot
│   ├── Why: Root access in container
│   └── Fix: Set runAsNonRoot: true, runAsUser: 1000+
├── Wildcard RBAC Permissions (Critical)?
│   ├── Check: verbs: ["*"] or resources: ["*"]
│   ├── Why: Over-privileged service accounts
│   └── Fix: Create specific roles with minimal permissions
├── Missing Security Context (Warning)?
│   ├── Check: No securityContext at pod or container level
│   ├── Why: Default settings may not be secure enough
│   └── Fix: Add securityContext with appropriate settings
└── Sensitive Data in Environment Variables (Critical)?
    ├── Check: Passwords, tokens, keys in env
    ├── Why: Visible via kubectl describe, logs
    └── Fix: Use Secrets, consider external secret management
```

### Performance Issues Diagnostic Tree

```
Performance Issues Detected?
├── Resource Utilization Issues?
│   ├── High CPU Usage?
│   │   ├── Symptoms: High latency, throttling
│   │   ├── Diagnose: kubectl top pods, kubectl describe node
│   │   └── Solutions: Increase limits, optimize code, add replicas
│   ├── Memory Pressure?
│   │   ├── Symptoms: OOMKilled, swapping, slow performance
│   │   ├── Diagnose: kubectl top pods, check events for OOM
│   │   └── Solutions: Increase limits, fix memory leaks, add nodes
│   └── Storage Issues?
│       ├── Symptoms: Failed writes, slow I/O, PVC pending
│       ├── Diagnose: kubectl get pv/pvc, df -h on nodes
│       └── Solutions: Expand PVs, add storage, optimize I/O patterns
├── Networking Performance?
│   ├── DNS Resolution Delays?
│   │   ├── Check: CoreDNS pods, node DNS config
│   │   ├── Test: nslookup from debug pod
│   │   └── Fix: Scale CoreDNS, optimize DNS config
│   ├── Service Connectivity Issues?
│   │   ├── Check: Service endpoints, NetworkPolicies
│   │   ├── Test: curl to service.cluster.local
│   │   └── Fix: Fix selectors, adjust NetworkPolicies
│   └── Ingress/Route Performance?
│       ├── Check: Ingress controller resources, TLS config
│       ├── Test: Load test with hey/wrk
│       └── Fix: Scale ingress, optimize TLS, add caching
└── Application-Specific Issues?
    ├── Slow Startup Times?
    │   ├── Check: Image size, initialization steps
    │   ├── Fix: Multi-stage builds, optimize startup
    │   └── Configure: startupProbe with appropriate values
    ├── Database Connection Pool Issues?
    │   ├── Check: Connection limits, timeout settings
    │   ├── Monitor: Active connections, wait time
    │   └── Fix: Adjust pool size, add connection retry logic
    └── Cache Inefficiency?
        ├── Check: Hit ratios, cache size
        ├── Monitor: Memory usage, eviction rates
        └── Fix: Optimize cache strategy, add external cache
```

### OpenShift-Specific Issues Tree

```
OpenShift Issues Detected?
├── Cluster Operator Degraded?
│   ├── Check: oc get clusteroperators
│   ├── Investigate: oc describe clusteroperator <name>
│   ├── Logs: oc logs -n openshift-<operator>
│   └── Common fixes:
│       ├── authentication/oauth → Check cert rotation
│       ├── ingress → Check router pods, certificates
│       ├── storage → Check storage class, provisioner
│       └── network → Check CNI configuration
├── SCC Violations?
│   ├── Check: Events for "unable to validate against any security context constraint"
│   ├── Diagnose: oc get scc, oc adm policy who-can use scc
│   └── Fix:
│       ├── Grant appropriate SCC to service account
│       ├── Adjust pod securityContext to match SCC
│       └── Create custom SCC for specific needs
├── BuildConfig Failures?
│   ├── Check: oc get builds, oc logs build/<build-name>
│   ├── Common issues:
│       │   ├── Source code access → Git credentials, webhook
│       │   ├── Base image not found → ImageStream, registry
│       │   ├── Build timeouts → Increase timeout, optimize build
│       │   └── Registry push failures → Permissions, quotas
│   └── Fix: Address specific build error, retry build
├── Route Issues?
│   ├── Check: oc get routes, oc describe route <name>
│   ├── Common issues:
│       │   ├── No endpoints → Service selector, pod health
│       │   ├── TLS certificate expired → Renew cert
│       │   ├── Wrong host/path → Update route spec
│       │   └── Router not responding → Check router pods
│   └── Fix: Fix underlying service or update route config
└── ImageStream Issues?
    ├── Check: oc get imagestreams, oc describe is <name>
    ├── Common issues:
    │   ├── No tags/images → Trigger import, fix image reference
    │   ├── Import failures → Registry access, credentials
    │   └── Tag not found → Fix tag reference, re-tag image
    └── Fix: Re-import image, fix registry connection
```

### Application Not Reachable - Enhanced Tree

```
Application Connectivity Issue?
├── Service Level Issues?
│   ├── Service has no endpoints?
│   │   ├── Check: kubectl get endpoints <service>
│   │   ├── Verify: Service selector matches pod labels
│   │   ├── Check: Pod health and readiness
│   │   └── Fix: Update selector or fix pod issues
│   ├── Service wrong type?
│   │   ├── ClusterIP but expecting external → Use LoadBalancer/NodePort
│   │   ├── LoadBalancer not getting IP → Check cloud provider
│   │   └── NodePort not accessible → Check firewall, node ports
│   └── Service port wrong?
│       ├── Check: targetPort vs containerPort
│       ├── Verify: Protocol (TCP/UDP) matches
│       └── Fix: Update service port configuration
├── Ingress/Route Issues?
│   ├── Ingress not found or misconfigured?
│   │   ├── Check: kubectl get ingress, describe ingress
│   │   ├── Verify: Host, path, backend service
│   │   └── Fix: Update ingress configuration
│   ├── TLS Certificate Issues?
│   │   ├── Check: Certificate expiration, validity
│       ├── Verify: Secret exists and contains cert/key
│       │   └── Fix: Renew certificate, update secret
│   ├── Ingress Controller Issues?
│   │   ├── Check: Controller pod health
│       ├── Verify: Controller service endpoints
│       │   └── Fix: Restart controller, fix configuration
│   └── Route-specific (OpenShift)?
│       ├── Check: oc get routes, describe route
│       ├── Verify: Router health, certificates
│       └── Fix: Update route, check router pods
├── NetworkPolicy Blocking?
│   ├── Check: kubectl get networkpolicy
│   ├── Verify: Policy allows traffic flow
│   ├── Test: Temporarily disable policy for debugging
│   └── Fix: Add appropriate ingress/egress rules
└── Application Level Issues?
    ├── Application not binding to right port?
    │   ├── Check: Listen address (0.0.0.0 vs 127.0.0.1)
    │   ├── Verify: Port number matches containerPort
    │   └── Fix: Update application bind configuration
    ├── Health check failures?
    │   ├── Check: Liveness/readiness probe paths
    │   ├── Verify: Application responds to probes
    │   └── Fix: Update probe configuration or application
    └── Application errors?
        ├── Check: Application logs for errors
        ├── Verify: Database connections, dependencies
        └── Fix: Address application-specific issues
```

## Health Check Scripts

### Cluster Health Summary

```bash
#!/bin/bash
# cluster-health.sh - Quick cluster health check

echo "=== Node Status ==="
kubectl get nodes -o wide

echo -e "\n=== Pods Not Running ==="
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded

echo -e "\n=== Recent Warning Events ==="
kubectl get events -A --field-selector type=Warning --sort-by='.lastTimestamp' | tail -20

echo -e "\n=== Resource Pressure ==="
kubectl top nodes

echo -e "\n=== PVCs Not Bound ==="
kubectl get pvc -A --field-selector=status.phase!=Bound

# OpenShift specific
if command -v oc &> /dev/null; then
    echo -e "\n=== Cluster Operators ==="
    oc get clusteroperators | grep -v "True.*False.*False"
fi
```

### Namespace Health Check

```bash
#!/bin/bash
# namespace-health.sh ${NAMESPACE}

NS=${1:-default}

echo "=== Pods in $NS ==="
kubectl get pods -n $NS -o wide

echo -e "\n=== Recent Events ==="
kubectl get events -n $NS --sort-by='.lastTimestamp' | tail -15

echo -e "\n=== Resource Usage ==="
kubectl top pods -n $NS 2>/dev/null || echo "Metrics not available"

echo -e "\n=== Services ==="
kubectl get svc -n $NS

echo -e "\n=== Deployments ==="
kubectl get deploy -n $NS

echo -e "\n=== PVCs ==="
kubectl get pvc -n $NS
```

## Quick Reference: Exit Codes

| Code | Signal | Meaning |
|------|--------|---------|
| 0 | - | Success |
| 1 | - | General error |
| 2 | - | Misuse of command |
| 126 | - | Command not executable |
| 127 | - | Command not found |
| 128 | - | Invalid exit argument |
| 130 | SIGINT | Keyboard interrupt |
| 137 | SIGKILL | Kill signal (OOM or forced) |
| 143 | SIGTERM | Termination signal |
| 255 | - | Exit status out of range |
