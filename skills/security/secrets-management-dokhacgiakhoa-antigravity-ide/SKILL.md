---
version: 4.1.0-fractal
name: secrets-management
description: Implement secure secrets management for CI/CD pipelines using Vault, AWS Secrets Manager, or native platform solutions. Use when handling sensitive credentials, rotating secrets, or securing CI/CD environments.
---

# Secrets Management

Secure secrets management practices for CI/CD pipelines using Vault, AWS Secrets Manager, and other tools.

## Purpose

Implement secure secrets management in CI/CD pipelines without hardcoding sensitive information.

## Use this skill when

- Store API keys and credentials
- Manage database passwords
- Handle TLS certificates
- Rotate secrets automatically
- Implement least-privilege access

## Do not use this skill when

- You plan to hardcode secrets in source control
- You cannot secure access to the secrets backend
- You only need local development values without sharing

## Instructions

1. Identify secret types, owners, and rotation requirements.
2. Choose a secrets backend and access model.
3. Integrate CI/CD or runtime retrieval with least privilege.
4. Validate rotation and audit logging.

## Safety

- Never commit secrets to source control.
- Limit access and log secret usage for auditing.

## Secrets Management Tools

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [HashiCorp Vault](./sub-skills/hashicorp-vault.md)
### 2. [AWS Secrets Manager](./sub-skills/aws-secrets-manager.md)
### 3. [Azure Key Vault](./sub-skills/azure-key-vault.md)
### 4. [Google Secret Manager](./sub-skills/google-secret-manager.md)
### 5. [Setup Vault](./sub-skills/setup-vault.md)
### 6. [GitHub Actions with Vault](./sub-skills/github-actions-with-vault.md)
### 7. [GitLab CI with Vault](./sub-skills/gitlab-ci-with-vault.md)
### 8. [Store Secret](./sub-skills/store-secret.md)
### 9. [Retrieve in GitHub Actions](./sub-skills/retrieve-in-github-actions.md)
### 10. [Terraform with AWS Secrets Manager](./sub-skills/terraform-with-aws-secrets-manager.md)
### 11. [Organization/Repository Secrets](./sub-skills/organizationrepository-secrets.md)
### 12. [Environment Secrets](./sub-skills/environment-secrets.md)
### 13. [Project Variables](./sub-skills/project-variables.md)
### 14. [Protected and Masked Variables](./sub-skills/protected-and-masked-variables.md)
### 15. [Automated Rotation with AWS](./sub-skills/automated-rotation-with-aws.md)
### 16. [Manual Rotation Process](./sub-skills/manual-rotation-process.md)
### 17. [Kubernetes Integration](./sub-skills/kubernetes-integration.md)
### 18. [Pre-commit Hook](./sub-skills/pre-commit-hook.md)
### 19. [CI/CD Secret Scanning](./sub-skills/cicd-secret-scanning.md)
