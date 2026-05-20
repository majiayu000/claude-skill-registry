---
name: gke-workload-security
description: Workflows for auditing and hardening the security of GKE workloads.
---

# GKE Workload Security

This skill provides workflows and best practices for securing GKE workloads. It
covers security auditing, Identity and Access Management (Workload Identity),
Network Security (Network Policies), and Node Security.

## Workflows

### 1. Security Audit

Assess the current security posture of your cluster using the provided audit
script.

**Capabilities:**

- Checks for Workload Identity.
- Verifies Network Policy is enabled.
- Checks if Shielded Nodes are enabled.
- Checks if Binary Authorization is enabled.
- Checks for Private Cluster configuration.

**Command:**

```bash
./.agent/skills/gke-workload-security/scripts/audit_cluster.sh <cluster-name> <region> <project-id>
```

### 2. Configure Workload Identity

Workload Identity allows Kubernetes Service Accounts (KSAs) to impersonate
Google Service Accounts (GSAs). This is the recommended method for workloads to
access Google Cloud APIs.

**Steps:**

1. **Create Namespace and KSA:**

   ```bash
   kubectl create namespace workload-identity-test-ns
   kubectl create serviceaccount <ksa-name> \
       --namespace workload-identity-test-ns
   ```

2. **Bind KSA to GSA:**

   ```bash
   gcloud iam service-accounts add-iam-policy-binding <gsa-name>@<project-id>.iam.gserviceaccount.com \
       --role roles/iam.workloadIdentityUser \
       --member "serviceAccount:<project-id>.svc.id.goog[workload-identity-test-ns/<ksa-name>]"
   ```

3. **Annotate KSA:**

   ```bash
   kubectl annotate serviceaccount <ksa-name> \
       --namespace workload-identity-test-ns \
       iam.gke.io/gcp-service-account=<gsa-name>@<project-id>.iam.gserviceaccount.com
   ```

4. **Verify Example Pod:**
   Use existing asset `assets/workload-identity-pod.yaml` to test the
   configuration. Update the `<ksa-name>` in the file first.

   ```bash
   kubectl apply -f .agent/skills/gke-workload-security/assets/workload-identity-pod.yaml
   ```

### 3. Implement Network Policies

Control traffic flow between Pods using Network Policies. By default, all
traffic is allowed.

**Enable Network Policy Enforcement:**

```bash
gcloud container clusters update <cluster-name> \
    --update-addons=NetworkPolicy=ENABLED \
    --region <region>
```

> [!NOTE]
> If your cluster uses Dataplane V2 (`--enable-dataplane-v2`), Network Policy enforcement is built-in and this step is not required (and may fail).

**Apply Default Deny Policy:**
Isolate namespaces by denying all ingress and egress traffic by default.

**Replace <target-namespace> with the namespace you want to isolate.**

kubectl apply -f .agent/skills/gke-workload-security/assets/default-deny-netpol.yaml -n <target-namespace>

### 4. Enable Shielded Nodes

Ensure nodes are running with verifiable integrity.

**Command:**

```bash
gcloud container clusters update <cluster-name> \
    --enable-shielded-nodes \
    --region <region>
```

### 5. GKE Sandbox (gVisor)

Run untrusted workloads in a sandbox for extra isolation.

**Enable GKE Sandbox:**

```bash
gcloud container clusters update <cluster-name> \
    --enable-gke-sandbox \
    --region <region>
```

**Run a Sandboxed Pod:**
Add `runtimeClassName: gvisor` to your Pod spec.

## Best Practices

1. **Least Privilege:** Always use Workload Identity with minimal IAM roles.
   Avoid using Node default service accounts.
2. **Network Isolation:** Use Network Policies to restrict Pod-to-Pod
   communication.
3. **Image Security:** Use Binary Authorization to ensure only trusted images
   are deployed.
4. **Regular Audits:** Run the audit script periodically to check for
   configuration drift.
5. **Private Clusters:** Prefer Private Clusters to limit public exposure of the
   control plane and nodes.
