---
name: infrastructure-validation
description: Use when working with Terraform (.tf, .tfvars), Ansible (playbooks, roles, inventory), Docker (Dockerfile, docker-compose.yml), CloudFormation, or any infrastructure-as-code files — provides validation workflows, tool chains, and common mistake prevention
---

<!-- TOKEN BUDGET: 130 lines / ~390 tokens -->

# Infrastructure Validation

## Activation Triggers
- Files matching: `*.tf`, `*.tfvars`, `Dockerfile`, `docker-compose.yml`, `playbook*.yml`, `roles/`, `inventory/`
- Config: `.shipyard/config.json` has `iac_validation` set to `"auto"` or `true`

## Overview

IaC mistakes don't cause test failures — they cause outages, breaches, and cost overruns. Validate before every change.

**Core principle:** Never apply without plan review. Like TDD requires tests before code, IaC requires validation before apply.

## File Detection

| Files Present | Workflow |
|--------------|----------|
| `*.tf` | Terraform |
| `playbook*.yml`, `roles/`, `inventory/` | Ansible |
| `Dockerfile`, `docker-compose.yml` | Docker |
| Templates with `AWSTemplateFormatVersion` | CloudFormation |
| YAML with `apiVersion:` | Kubernetes |

## Terraform Workflow

Run in order. Each step must pass before proceeding.

```
terraform fmt -check          # 1. Format (auto-fix with fmt if needed)
terraform validate            # 2. Syntax validation
terraform plan -out=tfplan    # 3. Review every change — NEVER skip
tflint --recursive            # 4. Lint (if installed)
tfsec . OR checkov -d .       # 5. Security scan (if installed)
```

**Drift detection:** `terraform plan -detailed-exitcode` — exit code 2 means drift. Document what drifted and why before overwriting.

## Ansible Workflow

```
yamllint .                              # 1. YAML syntax
ansible-lint                            # 2. Best practices
ansible-playbook --syntax-check *.yml   # 3. Playbook syntax
ansible-playbook --check *.yml          # 4. Dry run (where supported)
molecule test                           # 5. Role tests (if configured)
```

## Docker Workflow

```
hadolint Dockerfile                     # 1. Lint (if installed)
docker build -t test-build .            # 2. Build
trivy image test-build                  # 3. Security scan (if installed)
docker compose config                   # 4. Validate compose (if applicable)
```

## Common Mistakes

### Terraform
| Mistake | Fix |
|---------|-----|
| Local state file | Use remote backend (S3+DynamoDB, GCS) |
| No state locking | Enable lock table |
| Hardcoded secrets | Use variables + secret manager |
| `*` in security groups | Restrict to specific CIDRs |
| Unpinned provider version | Pin in `required_providers` |
| Missing tags | Require via policy or module defaults |

### Ansible
| Mistake | Fix |
|---------|-----|
| Plaintext secrets | `ansible-vault encrypt` |
| `shell` instead of modules | Use native modules (apt, copy, etc.) |
| Everything as root | `become: false` by default, escalate only when needed |

### Docker
| Mistake | Fix |
|---------|-----|
| `FROM ubuntu:latest` | Pin to digest: `FROM ubuntu:22.04@sha256:...` |
| Running as root | Add `USER nonroot` |
| `COPY . .` | Use `.dockerignore`, copy specific files |
| Secrets in ENV/ARG | Use build secrets or runtime injection |
| No health check | Add `HEALTHCHECK` instruction |
| Single-stage build | Use multi-stage builds |

## Red Flags — STOP

- `terraform apply -auto-approve` without prior plan review
- Security group with `0.0.0.0/0` on non-HTTP ports
- IAM policy with `*` action or `*` resource
- Secrets in `.tf`, `.yml`, or `Dockerfile`
- State file committed to git
- `latest` tag on any base image
- Container running as root in production

## Integration

**Referenced by:** `shipyard:builder` (detects IaC files, follows appropriate workflow), `shipyard:verifier` (IaC validation mode), `shipyard:auditor` (IaC security checks)

**Pairs with:** `shipyard:security-audit` (security lens for IaC), `shipyard:shipyard-verification` (IaC claims need validation evidence)
