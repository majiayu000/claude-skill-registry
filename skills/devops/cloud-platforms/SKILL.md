---
name: cloud-platforms
description: Cloud platform reference modules for GCP, Azure, and AWS. Use when working with cloud infrastructure, Kubernetes, managed databases, networking, IAM, or production diagnostics. Detect the target platform from AGENTS.md and repository context.
user-invocable: false
---

# Cloud Platforms

Load the provider-specific reference file that matches the repository context.

## Workflow

1. Read root `AGENTS.md` and relevant infrastructure files.
2. Detect the platform from concrete signals in the repo.
3. Load only the matching provider reference file.
4. Apply platform-specific CLI commands and operational patterns from that file.

## Detection Signals

| Signal in `AGENTS.md` or repo | Platform | Resource |
|---|---|---|
| GCP, GKE, Cloud SQL, Cloud Build, Artifact Registry | GCP | `gcp-reference.md` |
| Azure, AKS, Azure Database for PostgreSQL, Azure Monitor, ACR | Azure | `azure-reference.md` |
| AWS, EKS, RDS, CloudWatch, ECR | AWS | `aws-reference.md` |

If multiple platforms are present, scope the reference by service.

## Integration

- Used by: `analyze-prod`, `bugfix`, `infra-change`, `deploy-production`, `deploy-to-production`
