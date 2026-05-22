---
name: Container Security
description: Comprehensive container security guidance including vulnerability scanning with Trivy, image hardening, secrets management, and CIS benchmark compliance. Activates when working with "container security", "image scanning", "CVE", "vulnerability", "docker security", "hardening", or "CIS benchmark".
version: 1.0.0
---

# Container Security Skill

## Overview

Implement defense-in-depth security practices for containerized applications. Master vulnerability scanning, image hardening, secrets management, runtime security, and compliance with CIS Docker Benchmark to build secure, production-ready containers.

## Vulnerability Scanning

### Use Trivy for Comprehensive Scanning

**Scan Images for Vulnerabilities:**

Install and run Trivy to detect CVEs in container images:

```bash
# Install Trivy
brew install aquasecurity/trivy/trivy

# Scan image for vulnerabilities
trivy image myapp:latest

# Filter by severity
trivy image --severity HIGH,CRITICAL myapp:latest

# Output JSON for automation
trivy image --format json --output results.json myapp:latest

# Scan with exit code on findings
trivy image --exit-code 1 --severity CRITICAL myapp:latest
```

**Scan Dockerfiles for Misconfigurations:**

Detect security issues in Dockerfiles:

```bash
# Scan Dockerfile
trivy config Dockerfile

# Scan with specific policies
trivy config --policy ./policies Dockerfile

# Output in table format
trivy config --format table Dockerfile
```

**Integrate Scanning into CI/CD:**

Add Trivy scanning to GitHub Actions:

```yaml
name: Container Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
```

### Implement Continuous Monitoring

**Schedule Regular Scans:**

Set up automated scanning for deployed images:

```bash
# Scan all images in registry
trivy image --severity HIGH,CRITICAL \
  $(docker images --format "{{.Repository}}:{{.Tag}}")

# Scan specific registry
trivy image ghcr.io/org/app:latest

# Generate SBOM (Software Bill of Materials)
trivy image --format cyclonedx myapp:latest > sbom.json
```

**Configure Scanning Policies:**

Create custom policies with .trivyignore:

```
# .trivyignore
# Ignore specific CVEs (with justification)
CVE-2023-12345  # Fixed in runtime, not exploitable in our context
CVE-2023-67890  # Mitigation applied via network policies

# Ignore low severity in specific packages
CVE-2023-11111 package=curl
```

## Image Hardening

### Use Non-Root Users

**Run Containers as Unprivileged Users:**

Never run containers as root:

```dockerfile
FROM node:20-alpine

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001 -G appuser

# Set up application directory
WORKDIR /app
COPY --chown=appuser:appuser . .

# Install dependencies
RUN npm ci --only=production

# Switch to non-root user
USER appuser

EXPOSE 3000
CMD ["node", "server.js"]
```

**Verify User in Runtime:**

Check effective user in running container:

```bash
docker run --rm myapp:latest id
# Expected output: uid=1001(appuser) gid=1001(appuser)
```

### Implement Read-Only Root Filesystem

**Make Filesystem Immutable:**

Run containers with read-only root:

```dockerfile
FROM python:3.11-slim

RUN useradd -m -u 1001 appuser

WORKDIR /app
COPY --chown=appuser:appuser . .

RUN pip install --no-cache-dir -r requirements.txt

USER appuser

# Create writable temp directory
RUN mkdir -p /tmp/app && chown appuser:appuser /tmp/app

ENV TMPDIR=/tmp/app

CMD ["python", "app.py"]
```

Run with read-only filesystem:

```bash
docker run --read-only --tmpfs /tmp myapp:latest
```

Kubernetes configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        securityContext:
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1001
        volumeMounts:
        - name: tmp
          mountPath: /tmp
      volumes:
      - name: tmp
        emptyDir: {}
```

### Minimize Attack Surface

**Use Minimal Base Images:**

Choose distroless or scratch images:

```dockerfile
# Option 1: Distroless (no shell, no package manager)
FROM gcr.io/distroless/python3-debian12

COPY --chown=nonroot:nonroot app/ /app/
WORKDIR /app

USER nonroot
CMD ["main.py"]

# Option 2: Scratch (for static binaries)
FROM golang:1.21 AS builder
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o app

FROM scratch
COPY --from=builder /src/app /app
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
ENTRYPOINT ["/app"]

# Option 3: Alpine (minimal with package manager)
FROM alpine:3.19
RUN apk add --no-cache ca-certificates && \
    adduser -D -u 1001 appuser
COPY --chown=appuser:appuser app /app
USER appuser
CMD ["/app"]
```

**Remove Unnecessary Packages:**

Clean up build dependencies:

```dockerfile
FROM ubuntu:22.04

# Install build dependencies, build, then remove in same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev && \
    # Build application
    pip3 install -r requirements.txt && \
    # Remove build tools
    apt-get purge -y --auto-remove build-essential python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## Secrets Management

### Never Embed Secrets in Images

**Use Environment Variables:**

Pass secrets at runtime:

```dockerfile
FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

USER node

# Don't set secret values in Dockerfile
ENV NODE_ENV=production
# ENV API_KEY=secret123  # NEVER DO THIS

CMD ["node", "server.js"]
```

Run with secrets:

```bash
# Bad: Visible in process list and history
docker run -e API_KEY=secret123 myapp:latest

# Better: Read from file
docker run --env-file .env.production myapp:latest

# Best: Use secrets management
docker run --secret id=api_key,src=./secrets/api_key myapp:latest
```

**Implement Docker Secrets:**

Use BuildKit secrets for build-time secrets:

```dockerfile
# syntax=docker/dockerfile:1.4

FROM python:3.11-slim

WORKDIR /app

# Use secret during build without persisting it
RUN --mount=type=secret,id=pip_token \
    PIP_TOKEN=$(cat /run/secrets/pip_token) && \
    pip install --extra-index-url https://token:${PIP_TOKEN}@private-repo.com/simple/ \
    -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

Build with secrets:

```bash
docker buildx build \
  --secret id=pip_token,src=./secrets/pip_token \
  -t myapp:latest .
```

### Integrate with Secrets Managers

**Use Kubernetes Secrets:**

Reference secrets in pod specs:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  database-url: postgresql://user:pass@db:5432/mydb
  api-key: super-secret-key

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: api-key
```

**Integrate with HashiCorp Vault:**

Use Vault agent injector:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/agent-inject-secret-config: "secret/data/myapp/config"
        vault.hashicorp.com/role: "myapp"
    spec:
      serviceAccountName: myapp
      containers:
      - name: app
        image: myapp:latest
```

## Runtime Security

### Apply Security Contexts

**Configure Pod Security Standards:**

Implement restrictive security contexts:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    fsGroup: 1001
    seccompProfile:
      type: RuntimeDefault

  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1001
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
```

### Limit Container Capabilities

**Drop All Capabilities by Default:**

Only grant necessary capabilities:

```dockerfile
# Dockerfile with minimal capabilities
FROM alpine:3.19
RUN adduser -D -u 1001 appuser
COPY app /app
USER appuser
CMD ["/app"]
```

Docker run with limited capabilities:

```bash
docker run \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --security-opt=no-new-privileges \
  myapp:latest
```

Kubernetes configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        securityContext:
          capabilities:
            drop:
            - ALL
            add:
            - NET_BIND_SERVICE
          allowPrivilegeEscalation: false
```

### Implement Network Policies

**Restrict Network Access:**

Define network policies to limit traffic:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: UDP
      port: 53  # DNS
```

## CIS Benchmark Compliance

### Follow CIS Docker Benchmark

**Implement Key Controls:**

Apply critical CIS recommendations:

1. **Use Trusted Base Images:**

```dockerfile
# Use official images from verified publishers
FROM node:20-alpine

# Verify image signatures
# docker trust inspect node:20-alpine
```

2. **Don't Install Unnecessary Packages:**

```dockerfile
FROM debian:12-slim

# Install only required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

3. **Scan Images for Vulnerabilities (CIS 4.5):**

```bash
# Regular scanning
trivy image --severity HIGH,CRITICAL myapp:latest
```

4. **Use COPY Instead of ADD (CIS 4.9):**

```dockerfile
# Good
COPY app.py /app/

# Avoid unless needed
ADD https://example.com/file.tar.gz /tmp/
```

5. **Configure Health Checks (CIS 4.6):**

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD curl -f http://localhost:8080/health || exit 1
```

6. **Set Filesystem to Read-Only (CIS 5.12):**

```bash
docker run --read-only --tmpfs /tmp myapp:latest
```

7. **Limit Container Resources (CIS 5.10, 5.11):**

```bash
docker run \
  --memory="512m" \
  --memory-swap="512m" \
  --cpus="0.5" \
  myapp:latest
```

### Audit with Docker Bench Security

**Run Automated CIS Checks:**

Use Docker Bench Security:

```bash
# Clone Docker Bench Security
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security

# Run audit
sudo sh docker-bench-security.sh

# Run specific checks
sudo sh docker-bench-security.sh -c container_images

# Output to file
sudo sh docker-bench-security.sh -l /tmp/docker-bench.log
```

**Address Common Findings:**

Fix typical CIS violations:

```dockerfile
# Before (non-compliant)
FROM node:latest
COPY . /app
WORKDIR /app
RUN npm install
CMD npm start

# After (CIS compliant)
FROM node:20.11.1-alpine3.19

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy dependency manifests
COPY --chown=nodejs:nodejs package*.json ./

# Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy application
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node healthcheck.js

EXPOSE 3000
CMD ["node", "server.js"]
```

## Vulnerability Remediation

### Prioritize Fixes by Severity

**Triage Vulnerability Findings:**

Address vulnerabilities systematically:

1. **Critical**: Immediate remediation required
2. **High**: Fix within 7 days
3. **Medium**: Fix within 30 days
4. **Low**: Fix during routine updates

**Update Base Images:**

Keep base images current:

```dockerfile
# Check for updates regularly
FROM node:20-alpine  # Update from 20.10.0 to 20.11.1

# Pin specific version for reproducibility
FROM node:20.11.1-alpine3.19

# Rebuild images monthly to get security patches
```

**Patch Application Dependencies:**

Update vulnerable packages:

```bash
# Check for outdated packages
npm audit

# Fix vulnerabilities
npm audit fix

# Force fix (may introduce breaking changes)
npm audit fix --force

# Update specific package
npm update package-name
```

### Implement Defense in Depth

**Layer Security Controls:**

Apply multiple security measures:

1. **Build Time:**
   - Scan images with Trivy
   - Use minimal base images
   - Remove build dependencies

2. **Registry:**
   - Sign images with Docker Content Trust
   - Scan on push to registry
   - Implement RBAC for registry access

3. **Runtime:**
   - Apply security contexts
   - Use network policies
   - Enable runtime security monitoring

```yaml
# Complete secure deployment example
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: app
        image: ghcr.io/org/app:v1.2.3@sha256:abc123...
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "250m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url

      volumes:
      - name: tmp
        emptyDir: {}

      serviceAccountName: app-sa
      automountServiceAccountToken: false
```

## Compliance and Auditing

### Generate SBOMs

**Create Software Bill of Materials:**

Track dependencies for compliance:

```bash
# Generate SBOM with Trivy
trivy image --format cyclonedx --output sbom.json myapp:latest

# Generate SBOM with Syft
syft myapp:latest -o cyclonedx-json > sbom.json

# Attest SBOM to image
cosign attest --predicate sbom.json --type cyclonedx myapp:latest
```

### Sign Container Images

**Implement Image Signing:**

Use Cosign for signing:

```bash
# Generate key pair
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key myapp:latest

# Verify signature
cosign verify --key cosign.pub myapp:latest

# Sign with keyless (OIDC)
cosign sign myapp:latest
```

## Official References

- **Trivy Documentation**: https://aquasecurity.github.io/trivy/
- **CIS Docker Benchmark**: https://www.cisecurity.org/benchmark/docker
- **Docker Security Best Practices**: https://docs.docker.com/develop/security-best-practices/
- **OWASP Docker Security Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
- **Kubernetes Security Best Practices**: https://kubernetes.io/docs/concepts/security/

## Related Skills

- **Container Best Practices** - Dockerfile optimization and build efficiency
- **Kubernetes Skill** - Runtime security in orchestrated environments
- **DevOps Practices** - Security integration in CI/CD pipelines
