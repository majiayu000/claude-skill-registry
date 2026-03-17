---
name: security-baseline
description: Security requirements, threats, and controls that apply across this system.
---

# Security Baseline

## Threat Model (High Level)

- Primary users: internal analytics users
- Assets to protect:
  - Customer PII (anonymized in demo)
  - Event data integrity
  - Connection strings and secrets

## Required Controls

### Authentication

- Use Azure AD / Entra ID for Fabric workspace access
- Service principals for automated pipelines

### Authorization

- Enforce least privilege on Fabric items
- Separate dev/prod workspaces

### Input Validation & Output Encoding

- Validate all untrusted input at boundaries
- Sanitize or encode output where appropriate

### Secrets Management

- Store secrets in Azure Key Vault, never in code or config files
- Use Fabric-managed connections where possible

### Logging & Auditing

- Log security-relevant events
- Avoid logging sensitive data

## Common Vulnerabilities

- Never embed connection strings in notebooks
- Validate JSON payloads in streaming pipelines
