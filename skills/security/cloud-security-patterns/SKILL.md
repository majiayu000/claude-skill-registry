---
name: cloud-security-patterns
description: Cloud infrastructure security patterns for IaC and cloud services. Use when writing or reviewing Terraform, CDK, CloudFormation, Kubernetes manifests, or cloud infrastructure configuration. Do NOT use for application code security -- use security-patterns instead.
durability: encoded-preference
---

# Cloud Security Patterns

Cloud infrastructure security principles. For application code security (OWASP, input validation, authentication), see security-patterns skill.

## IAM

- No wildcard permissions (`*`) on actions or resources
- Service accounts scoped to minimum required actions
- Prefer IAM roles over long-lived access keys
- Review IAM policies for overly broad resource access (`Resource: "*"`)
- Separate IAM roles per service/function (no shared "admin" roles)

## Network Segmentation

- Databases and internal services not exposed to public internet
- Security groups and network policies follow deny-by-default
- Service-to-service communication restricted to required paths only
- Public-facing resources isolated in separate subnets/VPCs
- Egress rules restrict outbound traffic to known destinations

## Secrets Management

- No secrets in environment variables, config files, source code, or IaC templates
- Use dedicated secrets managers (Vault, AWS Secrets Manager, GCP Secret Manager)
- Secrets rotated on a defined schedule
- Secret references in IaC use dynamic lookups (not hardcoded values)
- CI/CD pipeline secrets scoped to the minimum required stage

## Container Security

- Base images from trusted registries only
- Images pinned by digest, not mutable tags
- Containers run as non-root user
- Read-only root filesystem where possible
- No privileged mode unless explicitly justified

## IaC Security Scanning

For pipeline integration of security scanning (SAST, secrets detection, dependency scanning), see cicd-patterns skill. The following are IaC-specific scanning concerns:

- Terraform/CDK/CloudFormation templates scanned for misconfigurations before apply
- Security group rules reviewed for overly permissive access (0.0.0.0/0)
- Encryption at rest enabled for all data stores
- Logging enabled for all services (CloudTrail, VPC Flow Logs, access logs)

## Review Checklist

- [ ] No wildcard IAM permissions
- [ ] No secrets in IaC templates or environment variables
- [ ] Databases not publicly accessible
- [ ] Containers run as non-root
- [ ] Base images pinned by digest
- [ ] Encryption at rest enabled
- [ ] Logging and audit trails enabled
