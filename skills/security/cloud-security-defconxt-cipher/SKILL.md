---
name: cloud-security
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: cloud-security
description: >-
  Defensive cloud security for AWS, Azure, and GCP including cloud security posture
  management (CSPM), cloud workload protection (CWPP), cloud access security broker
  (CASB), security group/NSG hardening, IAM policy review, logging and monitoring
  (CloudTrail/Azure Monitor/GCP Audit), cloud forensics, and multi-cloud security
  architecture.
domain: cybersecurity
subdomain: cloud-security
tags:
  - aws
  - azure
  - gcp
  - cspm
  - cwpp
  - iam-review
  - cloudtrail
  - security-groups
  - cloud-forensics
  - landing-zone
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1078.004", "T1530", "T1537", "T1580", "T1619"]
  nist-csf: ["PR.AC-1", "PR.AC-3", "PR.DS-5", "DE.CM-7"]
  frameworks: ["CIS Cloud Benchmarks", "CSA CCM", "NIST SP 800-144"]
---

# Cloud Security (Defensive)

## When to Use

Activate when the operator asks about cloud security posture, AWS/Azure/GCP hardening,
cloud logging, CSPM tools, cloud IAM review, security group audit, cloud forensics,
or secure landing zone design. For offensive cloud attacks, see `red-team/cloud`.

Mode: `[MODE: BLUE]` for cloud hardening; `[MODE: ARCHITECT]` for landing zone design; `[MODE: INCIDENT]` for cloud forensics.

## Quick Reference

| Control | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Audit logging | CloudTrail (all regions) | Activity Log + Diagnostic Settings | Audit Logs + Data Access Logs |
| CSPM | Security Hub + Config | Defender for Cloud | Security Command Center |
| IAM analyzer | IAM Access Analyzer | Entra ID Access Reviews | IAM Recommender |
| Network security | Security Groups + NACLs | NSGs + Azure Firewall | VPC Firewall Rules |
| Secret management | Secrets Manager / SSM | Key Vault | Secret Manager |
| Encryption | KMS (CMK) | Key Vault (CMK) | Cloud KMS (CMEK) |
| Container security | ECR scanning + GuardDuty | Defender for Containers | Artifact Analysis |
| DLP | Macie | Purview | DLP API |

## Workflow

### 1. Cloud Security Posture Assessment

```bash
# AWS — Security Hub + CIS Benchmark
aws securityhub get-findings --filters '{"SeverityLabel":[{"Value":"CRITICAL","Comparison":"EQUALS"}]}'

# AWS — IAM Access Analyzer (find public/cross-account access)
aws accessanalyzer list-findings --analyzer-arn $ANALYZER_ARN

# AWS — Config compliance
aws configservice get-compliance-summary-by-config-rule

# Prowler (multi-cloud CSPM)
prowler aws --compliance cis_2.0
prowler azure --compliance cis_2.0
prowler gcp --compliance cis_2.0

# ScoutSuite (multi-cloud audit)
scout aws --report-dir ./report/
```

### 2. IAM Security Review

```bash
# AWS — Find overprivileged IAM users/roles
aws iam generate-credential-report
aws iam get-credential-report --output text --query Content | base64 -d

# Find users with console access + no MFA
aws iam list-users | jq -r '.Users[].UserName' | while read user; do
  MFA=$(aws iam list-mfa-devices --user-name "$user" | jq '.MFADevices | length')
  [ "$MFA" -eq 0 ] && echo "NO MFA: $user"
done

# Find inline policies (should use managed policies)
aws iam list-users | jq -r '.Users[].UserName' | while read user; do
  INLINE=$(aws iam list-user-policies --user-name "$user" | jq '.PolicyNames | length')
  [ "$INLINE" -gt 0 ] && echo "INLINE POLICY: $user ($INLINE policies)"
done

# Find unused access keys (>90 days)
aws iam list-users | jq -r '.Users[].UserName' | while read user; do
  aws iam list-access-keys --user-name "$user" | jq -r '.AccessKeyMetadata[] |
    select(.Status=="Active") | "\(.UserName): \(.AccessKeyId) created \(.CreateDate)"'
done

# Azure — PIM eligible vs active assignments
az role assignment list --all --output table
```

### 3. Logging & Monitoring

```bash
# AWS — Verify CloudTrail in all regions
aws cloudtrail describe-trails | jq '.trailList[] | {Name, IsMultiRegionTrail, LogFileValidationEnabled}'

# AWS — GuardDuty findings
aws guardduty list-findings --detector-id $DETECTOR_ID --finding-criteria \
  '{"Criterion":{"severity":{"Gte":7}}}'

# Azure — Diagnostic settings for key resources
az monitor diagnostic-settings list --resource $RESOURCE_ID

# GCP — Verify audit logs enabled
gcloud logging sinks list
gcloud projects get-iam-policy $PROJECT_ID

# Critical logs to centralize:
# AWS: CloudTrail, VPC Flow Logs, GuardDuty, Config, WAF, ALB access logs
# Azure: Activity Log, Sign-in Logs, Diagnostic Settings, NSG Flow Logs
# GCP: Audit Logs, VPC Flow Logs, Cloud Armor, Load Balancer logs
```

### 4. Network Security Hardening

```bash
# AWS — Find security groups with 0.0.0.0/0 ingress
aws ec2 describe-security-groups --filters "Name=ip-permission.cidr,Values=0.0.0.0/0" \
  --query 'SecurityGroups[].{ID:GroupId,Name:GroupName}' --output table

# AWS — Find public S3 buckets
aws s3api list-buckets | jq -r '.Buckets[].Name' | while read bucket; do
  ACL=$(aws s3api get-bucket-acl --bucket "$bucket" 2>/dev/null | jq -r '.Grants[] | select(.Grantee.URI != null) | .Grantee.URI')
  [ -n "$ACL" ] && echo "PUBLIC: $bucket — $ACL"
done

# Azure — Find NSGs with any/any rules
az network nsg list | jq '.[] | select(.securityRules[] | select(.sourceAddressPrefix=="*" and .access=="Allow"))'
```

### 5. Cloud Forensics

See `references/cloud-forensics.md` for evidence collection procedures.

```bash
# AWS — Snapshot compromised EC2 for forensics
aws ec2 create-snapshot --volume-id $VOL_ID --description "IR forensics $(date +%Y%m%d)"

# AWS — CloudTrail query for specific actor
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=Username,AttributeValue=compromised-user \
  --start-time "2026-03-01T00:00:00Z" --max-results 50

# AWS — Isolate compromised instance
aws ec2 modify-instance-attribute --instance-id $INSTANCE_ID --groups $ISOLATION_SG_ID
```

## Verification

- [ ] CloudTrail/Audit Logs enabled in all regions with log validation
- [ ] CSPM tool running with CIS benchmark compliance >90%
- [ ] No security groups/NSGs with 0.0.0.0/0 on non-web ports
- [ ] All IAM users have MFA enabled
- [ ] No unused access keys (>90 days)
- [ ] Encryption at rest enabled for all storage services
- [ ] VPC Flow Logs enabled and forwarded to SIEM
- [ ] GuardDuty/Defender/SCC enabled and alerting
