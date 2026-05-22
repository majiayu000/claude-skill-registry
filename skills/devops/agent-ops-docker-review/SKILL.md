---
name: agent-ops-docker-review
description: "Docker image reviews, optimization, and step-building guidance. Analyzes Dockerfiles for best practices, security issues, and anti-patterns."
license: MIT
compatibility: [opencode, claude, cursor]

metadata:
  category: analysis
  related: [agent-ops-state]

---

# Docker Review Skill

Analyze Dockerfiles for best practices, security issues, and optimization opportunities.

## Modes

| Mode | Command | Purpose |
|------|---------|---------|
| Review | `/docker-review` | Analyze existing Dockerfile, produce findings report |
| Optimize | `/docker-optimize` | Suggest specific changes with before/after comparison |
| Build | `/docker-build` | Interactive step-by-step Dockerfile creation |
| Scan | `/docker-scan` | Run security scanners on built images (requires Docker) |

## Review Mode

### Trigger

```
/docker-review [path/to/Dockerfile]
```

If no path provided, search for `Dockerfile` in project root.

### Procedure

1. **Locate Dockerfile**
   - Check provided path or search common locations
   - If not found, offer to create one (switches to Build mode)

2. **Static Analysis**
   - Parse Dockerfile instructions
   - Check against best practices rules (see below)
   - Identify anti-patterns and security issues

3. **Generate Report**
   - Output to `.agent/docker-review.md`
   - Categorize findings by severity
   - Provide fix suggestions for each finding

### Output Format

```markdown
# Docker Review Report

**File:** Dockerfile
**Date:** YYYY-MM-DD
**Base Image:** python:3.11-slim

## Summary

| Severity | Count |
|----------|-------|
| 🔴 Error | 2 |
| 🟡 Warning | 5 |
| 🔵 Info | 3 |

## Findings

### 🔴 Error: Running as root user

**Line 1-end**
No USER instruction found. Container will run as root.

**Fix:**
```dockerfile
# Add before CMD/ENTRYPOINT
RUN useradd -r -s /bin/false appuser
USER appuser
```

### 🟡 Warning: Unpinned base image version
...
```

## Best Practices Rules

### Security (🔴 Error level)

| ID | Rule | Description |
|----|------|-------------|
| SEC001 | Non-root user | Container must not run as root |
| SEC002 | No secrets in build | No passwords, API keys, or tokens in Dockerfile |
| SEC003 | COPY over ADD | Use COPY unless ADD features needed (URL, tar extraction) |
| SEC004 | Minimal base | Prefer alpine, slim, or distroless images |

### Optimization (🟡 Warning level)

| ID | Rule | Description |
|----|------|-------------|
| OPT001 | Pin versions | Pin base image and package versions |
| OPT002 | Combine RUN | Chain RUN commands to reduce layers |
| OPT003 | Clean in same layer | Remove caches in same RUN as install |
| OPT004 | Order by change frequency | Put least-changing instructions first |
| OPT005 | Use .dockerignore | Exclude unnecessary files from context |
| OPT006 | Multi-stage builds | Separate build and runtime stages |

### Maintainability (🔵 Info level)

| ID | Rule | Description |
|----|------|-------------|
| MNT001 | Use LABEL | Add maintainer, version, description labels |
| MNT002 | HEALTHCHECK | Define health check for orchestrators |
| MNT003 | Explicit EXPOSE | Document exposed ports |
| MNT004 | ARG for versions | Use build args for version pinning |

## Optimize Mode

### Trigger

```
/docker-optimize [path/to/Dockerfile]
```

### Procedure

1. Run Review mode analysis
2. Generate optimized Dockerfile with all fixes applied
3. Show before/after comparison
4. Estimate size reduction (if possible)

### Output

Creates `.agent/references/dockerfile-optimized.md`:

```markdown
# Optimized Dockerfile

## Changes Applied

1. ✅ SEC001: Added non-root user
2. ✅ OPT002: Combined 5 RUN commands into 2
3. ✅ OPT006: Converted to multi-stage build

## Estimated Impact

- Layers: 12 → 6 (50% reduction)
- Size: ~450MB → ~120MB (estimated, multi-stage)

## Original

```dockerfile
FROM python:3.11
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

## Optimized

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
RUN useradd -r -s /bin/false appuser
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "app.py"]
```
```

## Build Mode (Interactive)

### Trigger

```
/docker-build
```

### Procedure

1. **Interview** (one question at a time):
   - What language/runtime? (Python, Node, Go, .NET, Java, Rust, other)
   - What is the entry point? (main.py, npm start, ./app, etc.)
   - What port(s) to expose?
   - Any build steps needed? (compile, bundle, etc.)
   - Any system dependencies? (apt packages, etc.)

2. **Generate Dockerfile** using language-specific template
3. **Generate .dockerignore** if not exists
4. **Review** the generated files with user

### Language Templates

#### Python Template

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Security: non-root user
RUN useradd -r -s /bin/false appuser && \
    chown -R appuser:appuser /app
    
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --chown=appuser:appuser . .

USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "-m", "{{entry_point}}"]
```

#### Node.js Template

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
WORKDIR /app

# Security: non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S appuser -u 1001 -G nodejs

COPY --from=builder /app/node_modules ./node_modules
COPY --chown=appuser:nodejs . .

USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "{{entry_point}}"]
```

#### Go Template

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/main .

FROM scratch
COPY --from=builder /app/main /main
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65534:65534
EXPOSE 8080
ENTRYPOINT ["/main"]
```

#### .NET Template

```dockerfile
# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS builder

WORKDIR /app
COPY *.csproj ./
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /out --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app

# Security: non-root user
RUN useradd -r -s /bin/false appuser
COPY --from=builder /out .

USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8080/health || exit 1
ENTRYPOINT ["dotnet", "{{assembly}}.dll"]
```

## Scan Mode

### Trigger

```
/docker-scan [image-name]
```

### Prerequisites

- Docker installed and running
- Image must be built locally or pullable

### Procedure

1. **Check tool availability**:
   - `trivy` (preferred) — vulnerability scanner
   - `grype` (alternative) — vulnerability scanner
   - `dockle` — CIS benchmark linter
   - `dive` — layer analysis

2. **Run available scanners**:
   ```bash
   # Trivy
   trivy image --severity HIGH,CRITICAL {{image}}
   
   # Grype
   grype {{image}} --only-fixed
   
   # Dockle
   dockle {{image}}
   
   # Dive
   dive {{image}} --ci
   ```

3. **Aggregate results** into report

### Output

```markdown
# Docker Security Scan Report

**Image:** myapp:latest
**Date:** YYYY-MM-DD

## Vulnerability Summary

| Severity | Count | Fixed Available |
|----------|-------|-----------------|
| Critical | 2 | 2 |
| High | 5 | 3 |
| Medium | 12 | 8 |

## Critical Vulnerabilities

### CVE-2024-1234 — OpenSSL Buffer Overflow

- **Package:** openssl 1.1.1k
- **Fixed in:** 1.1.1l
- **Action:** Update base image or add `RUN apt-get update && apt-get install -y openssl`

## CIS Benchmark Results

- ✅ CIS-DI-0001: Create user for container
- ❌ CIS-DI-0005: Content trust not enabled
- ✅ CIS-DI-0006: HEALTHCHECK instruction defined

## Layer Efficiency

- Total size: 245MB
- Wasted space: 12MB (4.9%)
- Largest layers:
  1. /usr/lib (89MB) — system libraries
  2. /app/node_modules (67MB) — dependencies
```

## External Tool Integration

### Hadolint (if available)

```bash
# Check if hadolint is available
hadolint --version

# Run hadolint
hadolint Dockerfile --format json
```

Parse hadolint output and merge with built-in rules. Hadolint rules take precedence when available.

### Tool Detection

At skill start, check for available tools:

```
🔧 Tool Detection:
- hadolint: ✅ v2.12.0 (enhanced linting)
- trivy: ✅ v0.48.0 (vulnerability scanning)
- dive: ❌ not found
- dockle: ❌ not found

Running with: hadolint + trivy
```

## Forbidden Behaviors

- Never run `docker build` without user confirmation
- Never push images to registries
- Never modify Dockerfile without showing diff first
- Never store secrets in generated Dockerfiles
