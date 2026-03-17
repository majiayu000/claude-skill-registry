---
name: AWS Penetration Testing
description: This skill should be used when the user asks to "pentest AWS", "test AWS security", "enumerate IAM", "exploit cloud infrastructure", "AWS privilege escalation", "S3 bucket testing", "metadata SSRF", "Lambda exploitation", or needs guidance on Amazon Web Services security assessment.
metadata:
  author: zebbern
  version: 4.1.0-fractal
---

# AWS Penetration Testing

## Purpose

Provide comprehensive techniques for penetration testing AWS cloud environments. Covers IAM enumeration, privilege escalation, SSRF to metadata endpoint, S3 bucket exploitation, Lambda code extraction, and persistence techniques for red team operations.

## Inputs/Prerequisites

- AWS CLI configured with credentials
- Valid AWS credentials (even low-privilege)
- Understanding of AWS IAM model
- Python 3, boto3 library
- Tools: Pacu, Prowler, ScoutSuite, SkyArk

## Outputs/Deliverables

- IAM privilege escalation paths
- Extracted credentials and secrets
- Compromised EC2/Lambda/S3 resources
- Persistence mechanisms
- Security audit findings

---

## Essential Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| Pacu | AWS exploitation framework | `git clone https://github.com/RhinoSecurityLabs/pacu` |
| SkyArk | Shadow Admin discovery | `Import-Module .\SkyArk.ps1` |
| Prowler | Security auditing | `pip install prowler` |
| ScoutSuite | Multi-cloud auditing | `pip install scoutsuite` |
| enumerate-iam | Permission enumeration | `git clone https://github.com/andresriancho/enumerate-iam` |
| Principal Mapper | IAM analysis | `pip install principalmapper` |

---

## Core Workflow

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Step 1: Initial Enumeration](./sub-skills/step-1-initial-enumeration.md)
### 2. [Step 2: IAM Enumeration](./sub-skills/step-2-iam-enumeration.md)
### 3. [Step 3: Metadata SSRF (EC2)](./sub-skills/step-3-metadata-ssrf-ec2.md)
### 4. [Shadow Admin Permissions](./sub-skills/shadow-admin-permissions.md)
### 5. [Create Access Key for Another User](./sub-skills/create-access-key-for-another-user.md)
### 6. [Attach Admin Policy](./sub-skills/attach-admin-policy.md)
### 7. [Add Inline Admin Policy](./sub-skills/add-inline-admin-policy.md)
### 8. [Lambda Privilege Escalation](./sub-skills/lambda-privilege-escalation.md)
### 9. [Bucket Discovery](./sub-skills/bucket-discovery.md)
### 10. [Bucket Enumeration](./sub-skills/bucket-enumeration.md)
### 11. [Public Bucket Search](./sub-skills/public-bucket-search.md)
### 12. [Mount EBS Volume](./sub-skills/mount-ebs-volume.md)
### 13. [Shadow Copy Attack (Windows DC)](./sub-skills/shadow-copy-attack-windows-dc.md)
### 14. [Disable CloudTrail](./sub-skills/disable-cloudtrail.md)
### 15. [Example 1: SSRF to Admin](./sub-skills/example-1-ssrf-to-admin.md)
