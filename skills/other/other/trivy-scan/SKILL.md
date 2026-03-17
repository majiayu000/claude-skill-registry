---
name: trivy-scan
description: Scan containers and dependencies for vulnerabilities with Trivy
argument-hint: "[<image-or-path>] [--severity=HIGH,CRITICAL]"
tags: [security, container, trivy, devsecops]
user-invocable: true
---

# Trivy Vulnerability Scanner

Scan container images, filesystems, and dependencies for vulnerabilities.

## What To Do

1. **Install**: `choco install trivy` or `brew install trivy`

2. **Scan container image**:
   ```bash
   trivy image --severity HIGH,CRITICAL --format json -o trivy-report.json myapp:latest
   ```

3. **Scan filesystem (NuGet/npm)**:
   ```bash
   trivy fs --severity HIGH,CRITICAL --scanners vuln .
   ```

4. **Scan IaC (Terraform, Helm, Dockerfile)**:
   ```bash
   trivy config --severity HIGH,CRITICAL .
   ```

5. **CI Integration**:
   ```yaml
   - script: trivy image --exit-code 1 --severity CRITICAL $(ACR_NAME).azurecr.io/$(IMAGE):$(TAG)
     displayName: "Container Scan"
   ```

## Arguments
- `<image-or-path>`: Container image or filesystem path
- `--severity=<levels>`: Filter (LOW, MEDIUM, HIGH, CRITICAL)