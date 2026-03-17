---
name: container-scanner
description: Scans containers and Dockerfiles for security issues. Wraps Hadolint for Dockerfile linting and Trivy for container image scanning. Use when user asks to "scan Dockerfile", "lint Dockerfile", "container security", "image scan", "Dockerセキュリティ", "コンテナスキャン".
---

# Container Scanner

Wrapper for Hadolint and Trivy to scan Dockerfiles and container images.

## Prerequisites

```bash
# Hadolint (Dockerfile linting)
brew install hadolint
# or
docker pull hadolint/hadolint

# Trivy (container image scanning)
brew install trivy
# or
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
```

## Usage

```bash
# Lint Dockerfile
npx container-scanner lint Dockerfile

# Scan container image
npx container-scanner image nginx:latest

# Both operations with JSON output
npx container-scanner lint Dockerfile --json
npx container-scanner image myapp:v1 --json

# Check available tools
npx container-scanner --check
```

## Hadolint Rules

Common Dockerfile best practices checked:

| Rule | Description |
|------|-------------|
| DL3000 | Use absolute WORKDIR |
| DL3001 | For some POSIX utilities, you can skip using apt-get |
| DL3002 | Last USER should not be root |
| DL3003 | Use WORKDIR to switch directories |
| DL3006 | Always tag the version of an image explicitly |
| DL3007 | Using latest is prone to errors |
| DL3008 | Pin versions in apt get install |
| DL3009 | Delete apt-get lists after installing |
| DL3018 | Pin versions in apk add |
| DL4006 | Set SHELL option -o pipefail |

## Output Format

### Dockerfile Lint

```json
{
  "tool": "hadolint",
  "scanPath": "Dockerfile",
  "findings": [
    {
      "id": "DL3007",
      "severity": "warning",
      "line": 1,
      "message": "Using latest is prone to errors...",
      "file": "Dockerfile"
    }
  ],
  "summary": { "total": 1, "error": 0, "warning": 1, "info": 0 }
}
```

### Image Scan

```json
{
  "tool": "trivy",
  "image": "nginx:latest",
  "findings": [
    {
      "id": "CVE-2024-1234",
      "severity": "critical",
      "package": "openssl",
      "installedVersion": "1.1.1",
      "fixedVersion": "1.1.2",
      "title": "Buffer Overflow"
    }
  ],
  "summary": { "total": 5, "critical": 1, "high": 2, "medium": 2 }
}
```

## Exit Codes

- `0`: No issues found
- `1`: Issues detected
- `2`: Tool not installed or error
