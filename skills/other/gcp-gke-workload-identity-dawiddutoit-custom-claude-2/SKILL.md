---
name: gcp-gke-workload-identity
description: |
  Implements Workload Identity for secure, keyless authentication between GKE pods
  and Google Cloud services. Use when setting up pod authentication to Pub/Sub,
  Cloud SQL, Secret Manager, or other GCP services. Eliminates service account key
  management, reduces security blast radius, and implements least privilege access
  patterns. Works with Spring Boot applications and IAM bindings.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# GKE Workload Identity

## Purpose

Workload Identity enables GKE pods to authenticate to Google Cloud services without managing service account keys. Pods use short-lived, automatically rotated credentials based on IAM bindings between Kubernetes and GCP service accounts.

## When to Use

Use this skill when you need to:
- Set up secure authentication from GKE pods to GCP services (Pub/Sub, Cloud SQL, Secret Manager)
- Eliminate service account key management and rotation
- Implement least privilege access with IAM bindings
- Authenticate Spring Boot applications to Google Cloud APIs
- Reduce security blast radius by avoiding static credentials
- Enable Cloud SQL Proxy or Pub/Sub client libraries to authenticate automatically

Trigger phrases: "set up Workload Identity", "GKE authentication", "pod to GCP service auth", "keyless authentication", "Cloud SQL IAM auth"

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Create Google Cloud Service Account](#step-1-create-google-cloud-service-account)
  - [Step 2: Create Kubernetes Service Account with Annotation](#step-2-create-kubernetes-service-account-with-annotation)
  - [Step 3: Bind KSA to GSA](#step-3-bind-ksa-to-gsa-one-time-iam-setup)
  - [Step 4: Grant Service Account Required IAM Roles](#step-4-grant-service-account-required-iam-roles)
  - [Step 5: Update Deployment to Use Service Account](#step-5-update-deployment-to-use-service-account)
  - [Step 6: Verify Workload Identity Configuration](#step-6-verify-workload-identity-configuration)
- [Examples](#examples)
- [Requirements](#requirements)
- [See Also](#see-also)

## Quick Start

Three simple steps to enable Workload Identity for your application:

```bash
# 1. Create Kubernetes Service Account
kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-runtime
  namespace: wtr-supplier-charges
  annotations:
    iam.gke.io/gcp-service-account: app-runtime@project.iam.gserviceaccount.com
EOF

# 2. Bind GSA to KSA (one-time setup)
gcloud iam service-accounts add-iam-policy-binding \
  app-runtime@project.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:project.svc.id.goog[wtr-supplier-charges/app-runtime]"

# 3. Use in deployment
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supplier-charges-hub
spec:
  template:
    spec:
      serviceAccountName: app-runtime
      containers:
      - name: app
        image: ...
EOF
```

Spring Boot automatically detects and uses the pod's credentials (no code changes needed).

## Instructions

### Step 1: Create Google Cloud Service Account

Create a service account for your application in the GCP project:

```bash
# Create service account
gcloud iam service-accounts create app-runtime \
  --project=ecp-wtr-supplier-charges-labs \
  --display-name="Supplier Charges Hub Runtime"

# Verify creation
gcloud iam service-accounts list --project=ecp-wtr-supplier-charges-labs
```

**Naming Convention:** Use `{app}-runtime` for clarity. For Supplier Charges Hub: `app-runtime@ecp-wtr-supplier-charges-labs.iam.gserviceaccount.com`

### Step 2: Create Kubernetes Service Account with Annotation

Create a Kubernetes Service Account (KSA) in your namespace with the annotation linking it to the GSA:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-runtime
  namespace: wtr-supplier-charges
  annotations:
    iam.gke.io/gcp-service-account: app-runtime@ecp-wtr-supplier-charges-labs.iam.gserviceaccount.com
```

Apply it:
```bash
kubectl apply -f service-account.yaml
```

**Key Points:**
- KSA name can differ from GSA name, but matching helps clarity
- Namespace must be correct in annotation
- The full GSA email (with `.iam.gserviceaccount.com`) is required

### Step 3: Bind KSA to GSA (One-Time IAM Setup)

Create the IAM binding that allows the KSA to impersonate the GSA:

```bash
gcloud iam service-accounts add-iam-policy-binding \
  app-runtime@ecp-wtr-supplier-charges-labs.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:ecp-wtr-supplier-charges-labs.svc.id.goog[wtr-supplier-charges/app-runtime]"
```

**Syntax:** `project.svc.id.goog[namespace/ksa-name]` is the principal that gets the role.

**Verify:**
```bash
gcloud iam service-accounts get-iam-policy \
  app-runtime@ecp-wtr-supplier-charges-labs.iam.gserviceaccount.com
```

### Step 4: Grant Service Account Required IAM Roles

Give the service account permissions to access the resources your application needs:

```bash
# For Pub/Sub publishing
gcloud projects add-iam-policy-binding ecp-wtr-supplier-charges-labs \
  --member="serviceAccount:app-runtime@ecp-wtr-supplier-charges-labs.iam.gserviceaccount.com" \
  --role="roles/pubsub.publisher"

# For Pub/Sub subscribing
gcloud projects add-iam-policy-binding ecp-wtr-supplier-charges-labs \
  --member="serviceAccount:app-runtime@ecp-wtr-supplier-charges-labs.iam.gserviceaccount.com" \
  --role="roles/pubsub.subscriber"

# For Cloud SQL connections
gcloud projects add-iam-policy-binding ecp-wtr-supplier-charges-labs \
  --member="serviceAccount:app-runtime@ecp-wtr-supplier-charges-labs.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

# For Secret Manager access
gcloud projects add-iam-policy-binding ecp-wtr-supplier-charges-labs \
  --member="serviceAccount:app-runtime@ecp-wtr-supplier-charges-labs.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Step 5: Update Deployment to Use Service Account

Specify the KSA in your deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supplier-charges-hub
  namespace: wtr-supplier-charges
spec:
  template:
    spec:
      serviceAccountName: app-runtime  # Use the KSA
      containers:
      - name: supplier-charges-hub-container
        image: europe-west2-docker.pkg.dev/.../supplier-charges-hub:latest
        # No credential configuration needed!
      - name: cloud-sql-proxy
        image: gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.11.4
        # Cloud SQL Proxy also uses pod's credentials
```

### Step 6: Verify Workload Identity Configuration

Test that the pod can access GCP services:

```bash
# Get a pod
POD_NAME=$(kubectl get pods -n wtr-supplier-charges -o name | head -1)

# Check the pod's Workload Identity binding
kubectl describe pod $POD_NAME -n wtr-supplier-charges | grep -A 5 "Annotations"

# Test access to Pub/Sub
kubectl exec $POD_NAME -n wtr-supplier-charges -- \
  gcloud pubsub topics list --project=ecp-wtr-supplier-charges-labs

# Test access to Cloud SQL
kubectl exec $POD_NAME -c cloud-sql-proxy -n wtr-supplier-charges -- \
  cloud-sql-proxy --version
```

## Examples

### Example 1: Complete Workload Identity Setup for Pub/Sub

```bash
#!/bin/bash
# Full setup for Supplier Charges Hub with Pub/Sub access

PROJECT_ID="ecp-wtr-supplier-charges-labs"
GSA_NAME="app-runtime"
GSA_EMAIL="${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
NAMESPACE="wtr-supplier-charges"
KSA_NAME="app-runtime"

# Step 1: Create Google Cloud Service Account
gcloud iam service-accounts create $GSA_NAME \
  --project=$PROJECT_ID \
  --display-name="Supplier Charges Hub Runtime"

# Step 2: Grant IAM roles for Pub/Sub
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$GSA_EMAIL" \
  --role="roles/pubsub.publisher"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$GSA_EMAIL" \
  --role="roles/pubsub.subscriber"

# Step 3: Create Kubernetes Service Account
kubectl create serviceaccount $KSA_NAME -n $NAMESPACE --dry-run=client -o yaml | \
  kubectl annotate -f - \
    iam.gke.io/gcp-service-account=$GSA_EMAIL \
    --overwrite \
    --local \
  | kubectl apply -f -

# Step 4: Bind KSA to GSA
gcloud iam service-accounts add-iam-policy-binding $GSA_EMAIL \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:${PROJECT_ID}.svc.id.goog[${NAMESPACE}/${KSA_NAME}]"

# Verify
echo "Workload Identity setup complete!"
gcloud iam service-accounts get-iam-policy $GSA_EMAIL
```

### Example 2: Spring Boot Application Using Workload Identity

```java
// No special configuration needed!
// Spring Cloud GCP automatically detects pod credentials

@Service
public class SupplierChargesPublisher {

    @Autowired
    private PubSubTemplate pubSubTemplate;

    public void publishCharge(SupplierCharge charge) {
        // Credentials come from Workload Identity automatically
        pubSubTemplate.publish("supplier-charges-topic",
            objectMapper.writeValueAsString(charge));
    }
}

// For Cloud SQL, IAM authentication is used:
// JDBC URL: jdbc:postgresql://localhost:5432/supplier_charges_hub
// Username: app-runtime@project.iam (GSA email)
// Cloud SQL Proxy handles IAM auth automatically
```

### Example 3: Verify Workload Identity is Working

```bash
#!/bin/bash
# Test script to verify Workload Identity

POD=$(kubectl get pods -n wtr-supplier-charges -o jsonpath='{.items[0].metadata.name}')
NAMESPACE="wtr-supplier-charges"

echo "Testing Workload Identity for pod: $POD"

# Check the bound service account
echo ""
echo "=== Service Account Binding ==="
kubectl get pod $POD -n $NAMESPACE -o jsonpath='{.spec.serviceAccountName}'
echo ""

# Check pod annotations
echo ""
echo "=== Pod Workload Identity Annotation ==="
kubectl get pod $POD -n $NAMESPACE -o jsonpath='{.metadata.annotations.iam\.gke\.io/gcp-service-account}'
echo ""

# Test Pub/Sub access
echo ""
echo "=== Testing Pub/Sub Access ==="
kubectl exec $POD -n $NAMESPACE -- \
  gcloud pubsub topics list --project=ecp-wtr-supplier-charges-labs || \
  echo "Pub/Sub access test failed!"

# Test Cloud SQL connection
echo ""
echo "=== Testing Cloud SQL Proxy ==="
kubectl exec $POD -c cloud-sql-proxy -n $NAMESPACE -- \
  nc -zv localhost 5432 || \
  echo "Cloud SQL Proxy connection test failed!"

echo ""
echo "Workload Identity verification complete!"
```

## Requirements

- GKE cluster with Workload Identity enabled (enabled by default in Autopilot)
- `gcloud` CLI with appropriate IAM permissions
- `kubectl` access to the cluster
- KSA and GSA created in their respective systems
- IAM role: `roles/iam.securityAdmin` to create IAM bindings

## See Also

- [gcp-gke-cluster-setup](../gcp-gke-cluster-setup/SKILL.md) - Ensure Workload Identity is enabled
- [gcp-gke-troubleshooting](../gcp-gke-troubleshooting/SKILL.md) - Diagnose Workload Identity issues
- [gcp-pubsub](../gcp-pubsub/SKILL.md) - Configure Pub/Sub integration
