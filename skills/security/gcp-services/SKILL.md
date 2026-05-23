---
name: gcp-services
version: "1.0"
description: >
  Configure GCP IAM, Secret Manager, and VPC networking with security best practices.
  PROACTIVELY activate for: (1) setting up service accounts and IAM permissions, (2) managing secrets in Secret Manager, (3) configuring VPC and firewall rules.
  Triggers: "iam", "secret manager", "vpc"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# GCP Services Skill (IAM, Secret Manager, Networking)

## Metadata (Tier 1)

**Keywords**: iam, service account, secret manager, vpc, firewall, permissions, least privilege, policy, network

**File Patterns**: *.tf (google_project_iam_*, google_secret_*, google_compute_network)

**Modes**: gcp_dev, deployment

---

## Instructions (Tier 2)

### IAM Least Privilege

#### Service Account Creation
```bash
gcloud iam service-accounts create SERVICE-sa \
  --display-name="Service Account for SERVICE"
```

#### Grant Minimal Permissions
```bash
# Secret Manager access
gcloud projects add-iam-policy-binding PROJECT \
  --member="serviceAccount:SERVICE-sa@PROJECT.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Cloud SQL client
gcloud projects add-iam-policy-binding PROJECT \
  --member="serviceAccount:SERVICE-sa@PROJECT.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

#### NEVER Use Basic Roles
- roles/owner
- roles/editor
- roles/viewer (on service accounts)

Use predefined roles (roles/run.invoker)
Use custom roles for specific needs

### Secret Manager

#### Create Secret
```bash
echo -n "SECRET_VALUE" | gcloud secrets create SECRET_NAME --data-file=-
```

#### Grant Access
```bash
gcloud secrets add-iam-policy-binding SECRET_NAME \
  --member="serviceAccount:SA@PROJECT.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

#### Access in Cloud Run
```bash
# As environment variable (less secure)
gcloud run deploy SERVICE --update-secrets=VAR=secret:version

# As mounted file (more secure)
gcloud run deploy SERVICE --update-secrets=/secrets/file=secret:version
```

#### Best Practices
- Pin to specific versions in production (not :latest)
- Enable rotation for sensitive secrets
- Use automatic replication unless data residency required
- Never pass secrets via environment variables in logs

### VPC & Firewall

#### Create Custom VPC
```bash
gcloud compute networks create NETWORK \
  --subnet-mode=custom

gcloud compute networks subnets create SUBNET \
  --network=NETWORK \
  --region=REGION \
  --range=10.0.0.0/24
```

#### Firewall Rules (Deny by Default)
```bash
# Allow HTTPS from anywhere
gcloud compute firewall-rules create allow-https \
  --network=NETWORK \
  --allow=tcp:443 \
  --source-ranges=0.0.0.0/0

# Allow SSH from specific bastion
gcloud compute firewall-rules create allow-ssh-bastion \
  --network=NETWORK \
  --allow=tcp:22 \
  --source-ranges=10.0.1.0/24 \
  --target-tags=ssh-enabled
```

#### VPC Connector for Cloud Run
```bash
gcloud compute networks vpc-access connectors create CONNECTOR \
  --network=NETWORK \
  --region=REGION \
  --range=10.8.0.0/28
```

### Anti-Patterns
- Using default VPC in production
- Overly permissive firewall rules (0.0.0.0/0 on SSH)
- Service account keys (use Workload Identity)
- Secrets in environment variables
- Basic IAM roles on service accounts
