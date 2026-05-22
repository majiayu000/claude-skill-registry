# Config Scan

Security review of configuration files and infrastructure as code.

---
description: Detect security misconfigurations in config files, Docker, and IaC
version: 1.0.0
tags: [security, configuration, docker, iac, terraform, kubernetes]
---

## Quick Start

```
/config-scan                      # Scan all config files
/config-scan --docker             # Docker files only
/config-scan --k8s                # Kubernetes manifests
/config-scan --terraform          # Terraform files
/config-scan --env                # Environment files
```

## What This Skill Detects

### Environment Files
- Secrets in `.env` files
- Insecure default values
- Missing required security variables

### Docker Security
- Running as root
- Exposed sensitive ports
- Insecure base images
- Missing security options

### Kubernetes Security
- Privileged containers
- Missing resource limits
- Insecure service accounts
- Network policy gaps

### Infrastructure as Code
- Overly permissive IAM policies
- Public S3 buckets
- Unencrypted storage
- Missing security groups

### Application Config
- Debug mode enabled
- Verbose error messages
- Insecure defaults

## Scan Categories

### Environment Files

**Files scanned**: `.env`, `.env.*`, `*.env`

| Issue | Severity | Description |
|-------|----------|-------------|
| Secrets in .env | HIGH | Credentials should use secrets manager |
| .env committed | CRITICAL | Should be in .gitignore |
| DEBUG=true | HIGH | Debug mode in production config |
| Weak secrets | MEDIUM | Short or simple values |

**Detection patterns**:
```
# Committed .env files
git ls-files | grep -E '\.env$|\.env\.'

# Secrets in env files
(PASSWORD|SECRET|KEY|TOKEN|CREDENTIAL)=.+

# Debug flags
DEBUG=(true|1|yes)
NODE_ENV=development
```

### Docker Security

**Files scanned**: `Dockerfile`, `docker-compose.yml`

| Issue | Severity | Description |
|-------|----------|-------------|
| USER root | HIGH | Container runs as root |
| COPY secrets | CRITICAL | Secrets copied into image |
| Latest tag | MEDIUM | Unpinned base image |
| Exposed ports | LOW | Wide port exposure |
| No healthcheck | LOW | Missing health monitoring |

**Detection patterns**:

```dockerfile
# Running as root (no USER directive)
FROM.*\n(?!.*USER)

# Copying secrets
COPY.*\.(pem|key|crt|env)
COPY.*secret
COPY.*password

# Unpinned images
FROM\s+\w+:latest
FROM\s+\w+\s*$

# Dangerous capabilities
--privileged
--cap-add
```

**docker-compose.yml issues**:

```yaml
# Privileged mode
privileged: true

# All capabilities
cap_add:
  - ALL

# Host network
network_mode: host

# Sensitive mounts
volumes:
  - /:/host
  - /var/run/docker.sock
```

### Kubernetes Security

**Files scanned**: `*.yaml`, `*.yml` (k8s manifests)

| Issue | Severity | Description |
|-------|----------|-------------|
| privileged: true | CRITICAL | Full host access |
| runAsRoot | HIGH | Container runs as root |
| No resource limits | MEDIUM | DoS risk |
| hostNetwork | HIGH | Pod uses host network |
| No securityContext | MEDIUM | Missing security settings |

**Detection patterns**:

```yaml
# Privileged containers
securityContext:
  privileged: true

# Running as root
securityContext:
  runAsUser: 0
runAsNonRoot: false

# Host access
hostNetwork: true
hostPID: true
hostIPC: true

# Dangerous volume mounts
volumes:
  - hostPath:
      path: /

# Missing limits
# (absence of resources.limits)

# Wildcard RBAC
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["*"]
```

### Terraform/IaC

**Files scanned**: `*.tf`, `*.tfvars`

| Issue | Severity | Description |
|-------|----------|-------------|
| Public S3 bucket | CRITICAL | Data exposure |
| * in IAM policy | HIGH | Overly permissive |
| No encryption | HIGH | Data at rest unencrypted |
| 0.0.0.0/0 ingress | HIGH | Open to internet |
| Hardcoded secrets | CRITICAL | Credentials in TF |

**Detection patterns**:

```hcl
# Public S3
acl = "public-read"
acl = "public-read-write"

# Overly permissive IAM
"Action": "*"
"Resource": "*"
"Principal": "*"

# Open security groups
cidr_blocks = ["0.0.0.0/0"]
ingress {
  from_port = 0
  to_port   = 65535

# Missing encryption
encrypted = false
# (or absence of encryption settings)

# Hardcoded secrets
password = "..."
secret_key = "..."
```

### Application Config

**Files scanned**: `config/*.json`, `*.config.js`, `application.yml`

| Issue | Severity | Description |
|-------|----------|-------------|
| DEBUG=true | HIGH | Debug in production |
| Verbose errors | MEDIUM | Stack traces exposed |
| CORS * | HIGH | All origins allowed |
| No HTTPS | MEDIUM | Unencrypted transport |

**Detection patterns**:

```javascript
// Debug mode
debug: true,
DEBUG: true,
NODE_ENV: 'development'

// Verbose errors
showStackTrace: true
detailedErrors: true

// CORS
origin: '*'
origin: true
Access-Control-Allow-Origin: *

// Session security
secure: false  // cookies
httpOnly: false
sameSite: 'none'
```

## Output Format

```
CONFIG SCAN RESULTS
===================

Files scanned: 23
Issues found: 15

CRITICAL (2)
------------
[!] Dockerfile:1 - Running as root
    No USER directive found
    Fix: Add "USER node" or similar non-root user

[!] terraform/s3.tf:12 - Public S3 bucket
    acl = "public-read"
    Fix: Remove public ACL, use bucket policies

HIGH (5)
--------
[H] docker-compose.yml:15 - Privileged container
    privileged: true
    Fix: Remove privileged flag, use specific capabilities

[H] k8s/deployment.yaml:34 - Missing resource limits
    No CPU/memory limits defined
    Fix: Add resources.limits section

...

MEDIUM (8)
----------
...
```

## Configuration

### Ignore Rules

Create `.config-scan-ignore`:

```yaml
# Ignore specific files
files:
  - "docker-compose.dev.yml"
  - "terraform/modules/test/**"

# Ignore specific rules
rules:
  - id: "docker-root-user"
    files: ["Dockerfile.dev"]
    reason: "Development only"

  - id: "k8s-no-limits"
    reason: "Handled by LimitRange"
```

### Scan Profiles

```yaml
# .config-scan.yaml
profile: production  # or: development, strict

# Custom thresholds
thresholds:
  fail_on: high
  warn_on: medium

# Specific scanners
scanners:
  docker: true
  kubernetes: true
  terraform: true
  env_files: true
  app_config: true
```

## Best Practices Checked

### Docker
- [ ] Non-root user specified
- [ ] Base image pinned to digest
- [ ] No secrets in build
- [ ] Multi-stage build used
- [ ] Health check defined
- [ ] Read-only root filesystem

### Kubernetes
- [ ] Non-root security context
- [ ] Resource limits defined
- [ ] Network policies in place
- [ ] No privileged containers
- [ ] Service accounts scoped
- [ ] Secrets encrypted at rest

### Terraform
- [ ] State file encrypted
- [ ] No hardcoded secrets
- [ ] Least privilege IAM
- [ ] Encryption enabled
- [ ] Logging enabled
- [ ] No public access by default

## Remediation Examples

### Docker: Run as Non-Root
```dockerfile
# Before
FROM node:18

# After
FROM node:18
RUN groupadd -r app && useradd -r -g app app
USER app
```

### Kubernetes: Security Context
```yaml
# Before
containers:
  - name: app
    image: myapp

# After
containers:
  - name: app
    image: myapp
    securityContext:
      runAsNonRoot: true
      runAsUser: 1000
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
```

### Terraform: Private S3
```hcl
# Before
resource "aws_s3_bucket" "data" {
  acl = "public-read"
}

# After
resource "aws_s3_bucket" "data" {
  # No ACL (private by default)
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

## CI/CD Integration

```yaml
# GitHub Actions
- name: Config Security Scan
  run: |
    /config-scan --fail-on high

- name: Docker Scan
  run: |
    /config-scan --docker --fail-on critical
```

## Related Skills

- `/security-scan` - Full security analysis
- `/secrets-scan` - Credential detection
- `/dependency-scan` - Package vulnerabilities
