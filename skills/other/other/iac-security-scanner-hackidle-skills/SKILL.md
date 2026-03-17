---
name: iac-security-scanner
description: Scan Terraform, Kubernetes, CloudFormation, ARM templates, and Dockerfiles for security misconfigurations using 790 Terrascan-derived policies with NIST 800-53 control mappings. Use when users need to review IaC for security issues, audit cloud configurations, check compliance posture, harden infrastructure code, or identify misconfigurations across AWS, Azure, GCP, and Kubernetes before deployment.
license: MIT
metadata:
  author: hackIDLE
  version: "1.0.0"
---

# IaC Security Scanner

Scan infrastructure code for security misconfigurations using 790 policies extracted from Terrascan.

## Capabilities

- **Terraform** (HCL2): AWS, Azure, GCP resources
- **Kubernetes**: Pods, Deployments, Services, RBAC
- **CloudFormation**: AWS resources (JSON/YAML)
- **Dockerfiles**: Image security best practices
- **Compliance Mapping**: NIST 800-53 controls
  - **HCL Normalization Helper**: `scripts/normalize_hcl.py` uses `python-hcl2`

## Prerequisites (Optional)

- For HCL normalization: `pip install python-hcl2`

## Scan Workflow

### 1. Identify IaC Type and Provider

Determine from file extensions and content:
- `.tf` → Terraform HCL
- `.yaml/.yml` with `apiVersion` → Kubernetes
- `.yaml/.yml` or `.json` with `AWSTemplateFormatVersion` → CloudFormation
- `Dockerfile` → Docker
- `.json` with `$schema.*deploymentTemplate` → ARM

### 2. Load Relevant Reference Files

Based on detected provider, load policies from:
- AWS: `references/aws/README.md` then specific resource files
- Azure: `references/azure/README.md`
- GCP: `references/gcp/README.md`
- K8s: `references/k8s/README.md`
- Docker: `references/docker/README.md`

For control mapping: `references/nist-mapping.md`

### 3. Extract Resources

Parse the IaC to identify:
- Resource types (e.g., `aws_s3_bucket`, `kubernetes_pod`)
- Resource configurations
- Resource relationships

### 4. Apply Security Checks

For each resource:
1. Load the corresponding policy file (e.g., `references/aws/aws_s3_bucket.md`)
2. Check each policy's conditions against the resource config
3. Record violations with severity and remediation

### 5. Generate Report

Output format:

```text
## Security Scan Results

**File**: main.tf
**IaC Type**: Terraform (AWS)
**Resources Scanned**: 12
**Findings**: 5 (🔴 2 HIGH, 🟡 2 MEDIUM, 🟢 1 LOW)

### 🔴 HIGH: AC_AWS_0132 - S3 bucket missing public access block
- **Resource**: aws_s3_bucket.data_lake (line 45)
- **Category**: Network Security
- **NIST Controls**: SC-7, AC-3
- **Issue**: No `aws_s3_bucket_public_access_block` resource found
- **Remediation**:
  ```hcl
  resource "aws_s3_bucket_public_access_block" "data_lake" {
    bucket                  = aws_s3_bucket.data_lake.id
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
  }
  ```
```

## Reference File Format

Each resource policy file contains:
- Policy ID and name
- Severity level (HIGH/MEDIUM/LOW)
- Category
- Description of the security issue
- What to check
- NIST 800-53 control mapping (where applicable)

## Severity Definitions

- 🔴 **HIGH**: Immediate security risk, public exposure, data breach potential
- 🟡 **MEDIUM**: Security weakness, defense-in-depth gap, compliance issue
- 🟢 **LOW**: Best practice deviation, hardening recommendation

## Common Scan Scenarios

### Full Repository Scan

Scan all `.tf` files recursively, aggregate findings by severity.

### Pre-Commit Check

Quick scan of staged files, fail on HIGH severity.

### Compliance Audit

Scan with NIST control mapping, group findings by control family.
