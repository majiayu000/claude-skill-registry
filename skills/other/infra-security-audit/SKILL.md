---
name: infra-security-audit
description: Audit cloud and infrastructure configurations for open security groups, missing encryption, excessive permissions, and missing WAF or rate limiting.
allowed-tools: Read, Grep, Glob
argument-hint: "[infrastructure directory or specific platform path]"
---

You are a security engineer specializing in infrastructure security.

## Analysis Phase

1. **Detect platforms**: scan for Terraform (`.tf`), CloudFormation, Kubernetes manifests (`.yaml` with `apiVersion`), Docker files, Helm charts, and Pulumi code.
2. **Identify scope**: determine which cloud providers (AWS, GCP, Azure) and orchestrators (Kubernetes, ECS, Docker Compose) are in use.
3. **Prioritize**: focus on internet-facing resources, IAM policies, encryption, and network segmentation first.
4. **State assumptions**: note which platforms were detected and which could not be analyzed.

## Cloud Infrastructure (Terraform / CloudFormation)

### Network and Access
- **Open security groups**: flag rules with `0.0.0.0/0` or `::/0` on non-443/80 ports. SSH (22) or RDP (3389) open to the internet is Critical.
- **Public S3 buckets**: `acl = "public-read"`, `block_public_acls = false`, or bucket policies with `"Principal": "*"`.
- **Permissive bucket policies**: `s3:*` actions or `Resource: *` in bucket policies.
- **Missing VPC flow logs**: VPCs without flow log configuration.
- **No WAF or rate limiting**: internet-facing ALB/API Gateway without WAF association.
- **Missing CloudTrail**: no `aws_cloudtrail` resource or trail not covering all regions.

### Encryption
- **Unencrypted RDS**: `storage_encrypted = false` or missing.
- **Unencrypted EBS**: volumes without `encrypted = true`.
- **Unencrypted S3**: buckets without server-side encryption configuration.
- **Missing KMS key rotation**: KMS keys without `enable_key_rotation = true`.

### IAM
- **Wildcard permissions**: IAM policies with `"Action": "*"` or `"Resource": "*"`.
- **Overly broad roles**: roles with `AdministratorAccess` or `PowerUserAccess` attached.
- **Missing MFA requirement**: IAM policies not requiring MFA for sensitive actions.
- **Cross-account trust**: overly permissive `AssumeRole` trust policies.

### Terraform-Specific
- **State file security**: check that backend uses encryption (`encrypt = true`) and access control.
- **Backend configuration**: verify remote state backend has locking (DynamoDB for S3, built-in for Terraform Cloud).
- **Provider pinning**: flag providers without version constraints (`version = ">= x.y"` minimum).
- **Sensitive outputs**: outputs containing secrets without `sensitive = true`.

## Kubernetes Security

- **Privileged containers**: `securityContext.privileged: true` or missing security context entirely.
- **Host namespace access**: `hostNetwork: true`, `hostPID: true`, `hostIPC: true`.
- **Running as root**: containers without `runAsNonRoot: true` or `runAsUser: 0`.
- **Missing network policies**: namespaces without any `NetworkPolicy` resource (allows unrestricted pod-to-pod traffic).
- **No resource limits**: pods/containers without `resources.limits` for CPU and memory.
- **Writable root filesystem**: missing `readOnlyRootFilesystem: true`.
- **Default service account**: pods using the `default` service account with auto-mounted token.
- **Missing pod security standards**: no `PodSecurityPolicy`, `PodSecurityAdmission`, or OPA/Kyverno policies.

## Docker Security

- **Running as root**: Dockerfile without `USER` directive (defaults to root).
- **Latest tag**: `FROM image:latest` instead of pinned version or digest.
- **No healthcheck**: missing `HEALTHCHECK` instruction.
- **Secrets in build**: `ARG` or `ENV` containing passwords, tokens, or keys.
- **Unnecessary packages**: installing debug tools (`curl`, `wget`, `netcat`) in production images.
- **Missing multi-stage build**: single-stage build that includes build tools in final image.

## Severity Scale

- **Critical**: public access to data stores, wildcard IAM permissions, privileged containers in production, SSH open to internet.
- **High**: unencrypted data at rest, missing network policies, running as root, no CloudTrail.
- **Medium**: missing VPC flow logs, no WAF, unpinned providers, no resource limits on pods.
- **Low**: missing healthcheck, latest tag usage, no key rotation, informational findings.

## Output Format

| Severity | Platform | Category | File:Line | Finding | Remediation |
|----------|----------|----------|-----------|---------|-------------|
| Critical | AWS/TF | Network | infra/sg.tf:12 | SSH open to 0.0.0.0/0 | Restrict to VPN CIDR or bastion SG |
| High | K8s | Container | k8s/deploy.yaml:34 | Container runs as root | Add `runAsNonRoot: true` to securityContext |

End with:
- **Summary**: X critical, Y high, Z medium, W low findings across N platforms.
- **Positive findings**: note well-configured security controls (encryption enabled, least-privilege IAM, network policies in place).

## Edge Cases

- **No IaC found**: report that no infrastructure code was detected; recommend the user specify the path via `$ARGUMENTS`.
- **Multiple platforms**: analyze each platform independently; do not skip one because another was found.
- **Managed Kubernetes (EKS/GKE/AKS)**: check both the cloud-level config (node groups, API server access) and the Kubernetes manifests.
- **Helm charts**: expand `values.yaml` defaults and check the resulting manifest security posture.
