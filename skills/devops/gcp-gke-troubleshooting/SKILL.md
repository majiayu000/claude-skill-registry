---
name: gcp-gke-troubleshooting
description: |
  Systematically diagnoses and resolves common GKE issues including pod failures,
  networking problems, database connection errors, and Pub/Sub issues. Use when pods
  are stuck in Pending, CrashLoopBackOff, ImagePullBackOff, experiencing DNS failures,
  Cloud SQL connection timeouts, or Pub/Sub message processing problems. Provides
  systematic debugging workflows and solution patterns for Spring Boot applications.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# GKE Troubleshooting

## Purpose

Systematically diagnose and resolve common GKE issues. This skill provides structured debugging workflows, common causes, and proven solutions for the most frequent problems encountered in production deployments.

## When to Use

Use this skill when you need to:
- Debug pods stuck in Pending, CrashLoopBackOff, or ImagePullBackOff status
- Troubleshoot networking issues (DNS failures, service connectivity)
- Fix Cloud SQL connection problems or IAM authentication errors
- Resolve Pub/Sub message processing issues
- Investigate resource exhaustion or scheduling failures
- Debug health probe failures
- Diagnose application crashes or startup issues

Trigger phrases: "pod not starting", "CrashLoopBackOff", "debug GKE issue", "Cloud SQL connection failed", "Pub/Sub not working", "pod pending"

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Identify the Pod Status](#step-1-identify-the-pod-status)
  - [Step 2: Investigate Based on Status](#step-2-investigate-based-on-status)
  - [Step 3: Network and Connectivity Issues](#step-3-network-and-connectivity-issues)
  - [Step 4: Database Connection Issues](#step-4-database-connection-issues)
  - [Step 5: Pub/Sub Issues](#step-5-pubsub-issues)
- [Examples](#examples)
- [Requirements](#requirements)
- [See Also](#see-also)

## Quick Start

Quick diagnostic flow for any pod issue:

```bash
# 1. Check pod status
kubectl get pods -n wtr-supplier-charges

# 2. View detailed pod information
kubectl describe pod <pod-name> -n wtr-supplier-charges

# 3. Check logs
kubectl logs <pod-name> -n wtr-supplier-charges

# 4. Check previous logs if crashed
kubectl logs <pod-name> -n wtr-supplier-charges --previous

# 5. Check events for scheduling issues
kubectl get events -n wtr-supplier-charges --sort-by='.lastTimestamp'

# 6. Check resource availability
kubectl top nodes
kubectl top pods -n wtr-supplier-charges
```

## Instructions

### Step 1: Identify the Pod Status

Understand what the pod status means:

```bash
kubectl get pods -n wtr-supplier-charges -o wide
```

| Status | Meaning | Action |
|--------|---------|--------|
| **Running** | Pod is executing | Check logs if issues |
| **Pending** | Waiting to be scheduled | Check events, node resources |
| **CrashLoopBackOff** | App crashes repeatedly | Check logs, configuration |
| **ImagePullBackOff** | Can't pull image | Verify image, permissions |
| **Completed** | Pod ran successfully and exited | Normal for batch jobs |
| **Error** | Pod exited with error | Check logs |

### Step 2: Investigate Based on Status

#### Pod Status: ImagePullBackOff

**Diagnose:**
```bash
# Get detailed error
kubectl describe pod <pod-name> -n wtr-supplier-charges

# Look for "Failed to pull image" in Events section
# Example: "Failed to pull image ... access denied"

# Check if image exists in registry
gcloud artifacts docker images list \
  europe-west2-docker.pkg.dev/ecp-artifact-registry/wtr-supplier-charges-container-images
```

**Solutions:**

1. **Image doesn't exist:**
```bash
# Verify image tag is correct
kubectl get deployment supplier-charges-hub -n wtr-supplier-charges \
  -o jsonpath='{.spec.template.spec.containers[0].image}'
```

2. **Missing Artifact Registry permissions:**
```bash
# Grant Artifact Registry Reader role
gcloud artifacts repositories add-iam-policy-binding \
  wtr-supplier-charges-container-images \
  --location=europe-west2 \
  --member="serviceAccount:app-runtime@project.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
```

3. **Private image registry authentication:**
```bash
# Create image pull secret
kubectl create secret docker-registry regcred \
  --docker-server=europe-west2-docker.pkg.dev \
  --docker-username=_json_key \
  --docker-password="$(cat key.json)" \
  -n wtr-supplier-charges

# Add to deployment
spec:
  imagePullSecrets:
  - name: regcred
```

#### Pod Status: CrashLoopBackOff

**Diagnose:**
```bash
# Check current logs
kubectl logs <pod-name> -n wtr-supplier-charges

# Check logs from previous container (if crashed)
kubectl logs <pod-name> -n wtr-supplier-charges --previous

# Check liveness probe configuration
kubectl describe pod <pod-name> -n wtr-supplier-charges | grep -A 10 "Liveness"
```

**Common Causes:**

1. **Application exits immediately:**
```bash
# Check startup logs for Java/Spring Boot errors
kubectl logs <pod-name> -n wtr-supplier-charges | head -50

# Look for: ClassNotFoundException, ConfigurationException, connection errors
```

2. **Liveness probe fails too early:**
```bash
# Increase initialDelaySeconds from 20 to 60
kubectl patch deployment supplier-charges-hub -n wtr-supplier-charges \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"supplier-charges-hub-container","livenessProbe":{"initialDelaySeconds":60}}]}}}}'
```

3. **Out of memory:**
```bash
# Check memory usage
kubectl top pods <pod-name> -n wtr-supplier-charges

# Increase memory limits
kubectl patch deployment supplier-charges-hub -n wtr-supplier-charges \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"supplier-charges-hub-container","resources":{"limits":{"memory":"4Gi"}}}]}}}}'
```

4. **Missing environment variables:**
```bash
# Check what env vars are set
kubectl exec <pod-name> -n wtr-supplier-charges -- env | sort

# Verify ConfigMap/Secret values
kubectl get configmap supplier-charges-hub-config -n wtr-supplier-charges -o yaml
kubectl get secret db-credentials -n wtr-supplier-charges -o yaml
```

#### Pod Status: Pending (Unschedulable)

**Diagnose:**
```bash
# Check events for scheduling messages
kubectl describe pod <pod-name> -n wtr-supplier-charges

# Look for: "Insufficient memory", "Insufficient cpu", "PersistentVolumeClaim"

# Check node capacity
kubectl top nodes
kubectl describe nodes
```

**Solutions:**

1. **Insufficient cluster resources:**
```bash
# Scale deployment down
kubectl scale deployment supplier-charges-hub --replicas=1 -n wtr-supplier-charges

# Or trigger autoscaling (if available)
# GKE Autopilot automatically provisions capacity
```

2. **Node affinity/taints preventing scheduling:**
```bash
# Check node taints
kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints

# View pod's node affinity/tolerations
kubectl get pod <pod-name> -n wtr-supplier-charges -o yaml | grep -A 10 -B 2 "affinity\|toleration"

# Add toleration to deployment if needed
spec:
  tolerations:
  - key: "dedicated"
    operator: "Equal"
    value: "compute"
    effect: "NoSchedule"
```

3. **PersistentVolumeClaim not bound:**
```bash
# Check PVC status
kubectl get pvc -n wtr-supplier-charges

# If Pending, check storage class
kubectl get storageclass
```

### Step 3: Network and Connectivity Issues

#### DNS Resolution Failures

**Diagnose:**
```bash
# Test DNS from pod
kubectl exec <pod-name> -n wtr-supplier-charges -- nslookup postgres

# Test connectivity to service
kubectl exec <pod-name> -n wtr-supplier-charges -- curl -v http://postgres:5432
```

**Solutions:**

1. **CoreDNS pods not running:**
```bash
# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Restart CoreDNS if needed
kubectl rollout restart deployment coredns -n kube-system
```

2. **Service doesn't exist or wrong namespace:**
```bash
# Verify service exists
kubectl get svc postgres -n wtr-supplier-charges

# Use fully qualified DNS name if in different namespace
service-name.namespace.svc.cluster.local
```

#### Service Not Accessible

**Diagnose:**
```bash
# Check service endpoints
kubectl get endpoints supplier-charges-hub -n wtr-supplier-charges

# If empty, no pods match the selector
kubectl get svc supplier-charges-hub -n wtr-supplier-charges -o yaml | grep selector
kubectl get pods -n wtr-supplier-charges --show-labels
```

**Solutions:**

1. **Pod labels don't match service selector:**
```bash
# Add/update labels on deployment
kubectl patch deployment supplier-charges-hub -n wtr-supplier-charges \
  -p '{"spec":{"template":{"metadata":{"labels":{"app":"supplier-charges-hub"}}}}}'
```

2. **Pods not in Ready state:**
```bash
# Check readiness probe
kubectl describe pod <pod-name> -n wtr-supplier-charges | grep -A 10 "Readiness"

# Check health endpoint
kubectl exec <pod-name> -n wtr-supplier-charges -- \
  curl localhost:8080/actuator/health/readiness
```

### Step 4: Database Connection Issues

**Diagnose:**
```bash
# Test connectivity to Cloud SQL Proxy
kubectl exec <pod-name> -n wtr-supplier-charges -- nc -zv localhost 5432

# Check Cloud SQL Proxy logs
kubectl logs <pod-name> -c cloud-sql-proxy -n wtr-supplier-charges

# Check application startup logs for DB connection errors
kubectl logs <pod-name> -c supplier-charges-hub-container -n wtr-supplier-charges | grep -i "database\|connection"
```

**Solutions:**

1. **IAM Authentication fails:**
```bash
# Verify Workload Identity binding
kubectl get sa app-runtime -n wtr-supplier-charges -o yaml | grep iam.gke.io

# Grant cloudsql.client role
gcloud projects add-iam-policy-binding project-id \
  --member="serviceAccount:app-runtime@project.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

# Check service account email format (must be {name}@{project}.iam)
```

2. **Wrong connection string:**
```bash
# Verify DB_CONNECTION_NAME format: project:region:instance
kubectl get configmap db-config -n wtr-supplier-charges -o yaml

# Should be something like: ecp-wtr-supplier-charges-labs:europe-west2:supplier-charges-hub
```

3. **Cloud SQL Proxy not running:**
```bash
# Check sidecar logs
kubectl logs <pod-name> -c cloud-sql-proxy -n wtr-supplier-charges

# Check sidecar resources
kubectl describe pod <pod-name> -n wtr-supplier-charges | grep -A 15 "cloud-sql-proxy"
```

### Step 5: Pub/Sub Issues

**Diagnose:**
```bash
# Check subscription backlog
gcloud pubsub subscriptions describe supplier-charges-incoming-sub \
  --project=ecp-wtr-supplier-charges-labs

# Check application Pub/Sub logs
kubectl logs <pod-name> -c supplier-charges-hub-container \
  -n wtr-supplier-charges | grep -i "pubsub\|subscription"

# Test pub/sub connectivity from pod
kubectl exec <pod-name> -n wtr-supplier-charges -- \
  gcloud pubsub topics list --project=ecp-wtr-supplier-charges-labs
```

**Solutions:**

1. **Missing Pub/Sub permissions:**
```bash
# Grant Pub/Sub roles
gcloud projects add-iam-policy-binding project-id \
  --member="serviceAccount:app-runtime@project.iam.gserviceaccount.com" \
  --role="roles/pubsub.subscriber"

gcloud projects add-iam-policy-binding project-id \
  --member="serviceAccount:app-runtime@project.iam.gserviceaccount.com" \
  --role="roles/pubsub.publisher"
```

2. **High subscription backlog (messages not being consumed):**
```bash
# Check if pod is running
kubectl get pods -n wtr-supplier-charges

# Check application logs for processing errors
kubectl logs -f <pod-name> -c supplier-charges-hub-container \
  -n wtr-supplier-charges | grep -i "error\|exception"

# Increase message processing timeout
# In application.yaml:
# spring.cloud.gcp.pubsub.subscriber.max-ack-extension-period: 600
```

3. **Message processing failures:**
```bash
# Check for poison messages (causing repeated failures)
# Review DLQ (Dead Letter Queue) if configured

# Implement retry logic with exponential backoff
# See Spring Cloud GCP documentation for retry configuration
```

## Examples

See [examples/examples.md](examples/examples.md) for comprehensive examples including:
- Complete troubleshooting workflow
- Database connectivity debugging
- Pub/Sub debugging

## Requirements

- `kubectl` access to the cluster
- `gcloud` CLI configured
- Permissions to view pod logs and describe resources
- For database debugging: access to view Cloud SQL configuration
- For Pub/Sub debugging: access to view subscription details

## See Also

- [gcp-gke-deployment-strategies](../gcp-gke-deployment-strategies/SKILL.md) - Understand deployment health checks
- [gcp-gke-monitoring-observability](../gcp-gke-monitoring-observability/SKILL.md) - Monitor applications
- [gcp-gke-workload-identity](../gcp-gke-workload-identity/SKILL.md) - Debug IAM/Workload Identity issues
