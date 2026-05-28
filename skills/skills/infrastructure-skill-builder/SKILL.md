---
name: infrastructure-skill-builder
description: Transform infrastructure documentation, runbooks, and operational knowledge into reusable Claude Code skills. Convert Proxmox configs, Docker setups, Kubernetes deployments, and cloud infrastructure patterns into structured, actionable skills.
license: MIT
tags: [infrastructure, documentation, skill-creation, knowledge-capture, iac]
---

# Infrastructure Skill Builder

Convert your infrastructure documentation into powerful, reusable Claude Code skills.

## Overview

Infrastructure knowledge is often scattered across:
- README files
- Runbooks and wiki pages
- Configuration files
- Troubleshooting guides
- Team Slack/Discord history
- Mental models of senior engineers

This skill helps you systematically capture that knowledge as Claude Code skills for:
- Faster onboarding
- Consistent operations
- Disaster recovery
- Knowledge preservation
- Team scaling

## When to Use

Use this skill when:
- Documenting complex infrastructure setups
- Creating runbooks for operations teams
- Onboarding new team members to infrastructure
- Preserving expert knowledge before team changes
- Standardizing infrastructure operations
- Building organizational infrastructure library
- Migrating from manual to automated operations

## Skill Extraction Process

### Step 1: Identify Infrastructure Domains

**Common domains:**
- **Container Orchestration**: Docker, Kubernetes, Proxmox LXC
- **Cloud Platforms**: AWS, GCP, Azure, DigitalOcean
- **Databases**: PostgreSQL, MongoDB, Redis, MySQL
- **Web Servers**: Nginx, Apache, Caddy, Traefik
- **Monitoring**: Prometheus, Grafana, ELK Stack
- **CI/CD**: Jenkins, GitLab CI, GitHub Actions
- **Networking**: VPNs, Load Balancers, DNS, Firewalls
- **Storage**: S3, MinIO, NFS, Ceph
- **Security**: Authentication, SSL/TLS, Firewalls

### Step 2: Extract Core Operations

For each domain, document:

1. **Setup/Provisioning**: How to create new instances
2. **Configuration**: How to configure for different use cases
3. **Operations**: Day-to-day management tasks
4. **Troubleshooting**: Common issues and resolutions
5. **Scaling**: How to scale up/down
6. **Backup/Recovery**: Disaster recovery procedures
7. **Monitoring**: Health checks and alerts
8. **Security**: Security best practices

## Infrastructure Skill Template

```markdown
---
name: [infrastructure-component]-manager
description: Expert guidance for [component] management, provisioning, troubleshooting, and operations
license: MIT
tags: [infrastructure, [component], operations, troubleshooting]
---

# [Component] Manager

Expert knowledge for managing [component] infrastructure.

## Authentication & Access

### Access Methods
```bash
# How to access the infrastructure component
ssh user@host
# or
kubectl config use-context cluster-name
```

### Credentials & Configuration
- Where credentials are stored
- How to configure access
- Common authentication issues

## Architecture Overview

### Component Topology
- How components are organized
- Network topology
- Resource allocation
- Redundancy setup

### Key Resources
- Resource 1: Purpose and specs
- Resource 2: Purpose and specs
- Resource 3: Purpose and specs

## Common Operations

### Operation 1: [e.g., Create New Instance]
```bash
# Step-by-step commands
command1 --flags
command2 --flags

# Verification
verify-command
```

### Operation 2: [e.g., Update Configuration]
```bash
# Commands and explanations
```

### Operation 3: [e.g., Scale Resources]
```bash
# Commands and explanations
```

## Monitoring & Health Checks

### Check System Status
```bash
# Health check commands
status-command

# Expected output
# What healthy output looks like
```

### Common Metrics
- Metric 1: What it means, normal range
- Metric 2: What it means, normal range
- Metric 3: What it means, normal range

## Troubleshooting

### Issue 1: [Common Problem]
**Symptoms**: What you observe
**Cause**: Why it happens
**Fix**: Step-by-step resolution
```bash
# Fix commands
```

### Issue 2: [Another Problem]
**Symptoms**:
**Cause**:
**Fix**:
```bash
# Fix commands
```

## Backup & Recovery

### Backup Procedures
```bash
# How to backup
backup-command

# Verification
verify-backup
```

### Recovery Procedures
```bash
# How to restore
restore-command

# Verification
verify-restore
```

## Security Best Practices

- Security practice 1
- Security practice 2
- Security practice 3

## Quick Reference

| Task | Command |
|------|---------|
| Task 1 | `command1` |
| Task 2 | `command2` |
| Task 3 | `command3` |

## Additional Resources

- Official documentation links
- Related skills
- External references
```

## Real-World Example: Proxmox Skill

Based on the proxmox-auth skill in this repository:

### Extracted Knowledge

**From**: Proxmox VE cluster documentation + operational experience

**Structured as**:
1. **Authentication**: SSH access patterns, node IPs
2. **Architecture**: Cluster topology (2 nodes, resources)
3. **Operations**: Container/VM management commands
4. **Troubleshooting**: Common errors and fixes
5. **Networking**: Bridge configuration, IP management
6. **GPU Passthrough**: Special container configurations

**Result**: Comprehensive skill covering:
- Quick access to any node
- Container lifecycle management
- GPU-accelerated containers
- Network troubleshooting
- Backup procedures
- Common gotchas and solutions

## Extraction Scripts

### Extract from Runbooks

```bash
#!/bin/bash
# extract-from-runbook.sh - Convert runbook to skill

RUNBOOK_FILE="$1"
SKILL_NAME="$2"

if [ -z "$RUNBOOK_FILE" ] || [ -z "$SKILL_NAME" ]; then
    echo "Usage: $0 <runbook.md> <skill-name>"
    exit 1
fi

SKILL_DIR="skills/$SKILL_NAME"
mkdir -p "$SKILL_DIR"

# Extract sections from runbook
cat > "$SKILL_DIR/SKILL.md" << EOF
---
name: $SKILL_NAME
description: $(head -5 "$RUNBOOK_FILE" | grep -v "^#" | head -1 | xargs)
license: MIT
extracted-from: $RUNBOOK_FILE
---

# ${SKILL_NAME^}

$(cat "$RUNBOOK_FILE")

---

**Note**: This skill was auto-extracted from runbook documentation.
Review and refine before use.
EOF

echo "✓ Created skill: $SKILL_DIR/SKILL.md"
echo "Review and edit to add:"
echo "  - Metadata and tags"
echo "  - Troubleshooting section"
echo "  - Quick reference"
echo "  - Examples"
```

### Extract from Docker Compose

```bash
#!/bin/bash
# docker-compose-to-skill.sh - Extract skill from docker-compose.yaml

COMPOSE_FILE="${1:-docker-compose.yaml}"
PROJECT_NAME=$(basename $(pwd))

SKILL_DIR="skills/docker-$PROJECT_NAME"
mkdir -p "$SKILL_DIR"

# Extract services
SERVICES=$(yq eval '.services | keys | .[]' "$COMPOSE_FILE")

cat > "$SKILL_DIR/SKILL.md" << EOF
---
name: docker-$PROJECT_NAME
description: Docker Compose configuration and management for $PROJECT_NAME
license: MIT
---

# Docker $PROJECT_NAME

Manage Docker Compose stack for $PROJECT_NAME.

## Services

$(yq eval '.services | to_entries | .[] | "### " + .key + "\n" + (.value.image // "custom") + "\n"' "$COMPOSE_FILE")

## Quick Start

\`\`\`bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
\`\`\`

## Service Details

### Ports

$(yq eval '.services | to_entries | .[] | select(.value.ports) | "- **" + .key + "**: " + (.value.ports | join(", "))' "$COMPOSE_FILE")

### Volumes

$(yq eval '.services | to_entries | .[] | select(.value.volumes) | "- **" + .key + "**: " + (.value.volumes | join(", "))' "$COMPOSE_FILE")

## Configuration

See \`$COMPOSE_FILE\` for full configuration.

## Common Operations

### Restart Service

\`\`\`bash
docker-compose restart SERVICE_NAME
\`\`\`

### Update Service

\`\`\`bash
docker-compose pull SERVICE_NAME
docker-compose up -d SERVICE_NAME
\`\`\`

### View Service Logs

\`\`\`bash
docker-compose logs -f SERVICE_NAME
\`\`\`

## Troubleshooting

### Service Won't Start

1. Check logs: \`docker-compose logs SERVICE_NAME\`
2. Verify ports not in use: \`netstat -tulpn | grep PORT\`
3. Check disk space: \`df -h\`

### Network Issues

\`\`\`bash
# Recreate network
docker-compose down
docker network prune
docker-compose up -d
\`\`\`
EOF

echo "✓ Created skill from docker-compose.yaml"
```

### Extract from Kubernetes Manifests

```bash
#!/bin/bash
# k8s-to-skill.sh - Extract skill from Kubernetes manifests

K8S_DIR="${1:-.}"
APP_NAME="${2:-$(basename $(pwd))}"

SKILL_DIR="skills/k8s-$APP_NAME"
mkdir -p "$SKILL_DIR"

cat > "$SKILL_DIR/SKILL.md" << EOF
---
name: k8s-$APP_NAME
description: Kubernetes deployment and management for $APP_NAME
license: MIT
---

# Kubernetes $APP_NAME

Manage Kubernetes resources for $APP_NAME.

## Resources

$(find "$K8S_DIR" -name "*.yaml" -o -name "*.yml" | while read file; do
    KIND=$(yq eval '.kind' "$file" 2>/dev/null)
    NAME=$(yq eval '.metadata.name' "$file" 2>/dev/null)
    echo "- **$KIND**: $NAME ($(basename $file))"
done)

## Deployment

### Apply All Resources

\`\`\`bash
kubectl apply -f $K8S_DIR/
\`\`\`

### Check Status

\`\`\`bash
# Pods
kubectl get pods -l app=$APP_NAME

# Services
kubectl get svc -l app=$APP_NAME

# Deployments
kubectl get deploy -l app=$APP_NAME
\`\`\`

## Common Operations

### Scale Deployment

\`\`\`bash
kubectl scale deployment $APP_NAME --replicas=3
\`\`\`

### Update Image

\`\`\`bash
kubectl set image deployment/$APP_NAME container=new-image:tag
\`\`\`

### View Logs

\`\`\`bash
kubectl logs -f deployment/$APP_NAME
\`\`\`

### Port Forward

\`\`\`bash
kubectl port-forward svc/$APP_NAME 8080:80
\`\`\`

## Troubleshooting

### Pod Not Starting

\`\`\`bash
# Check pod events
kubectl describe pod POD_NAME

# Check logs
kubectl logs POD_NAME

# Previous instance logs
kubectl logs POD_NAME --previous
\`\`\`

### Service Not Reachable

\`\`\`bash
# Check endpoints
kubectl get endpoints $APP_NAME

# Check service
kubectl describe svc $APP_NAME

# Test from another pod
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://$APP_NAME
\`\`\`

## Quick Reference

| Task | Command |
|------|---------|
| Apply | \`kubectl apply -f $K8S_DIR/\` |
| Status | \`kubectl get all -l app=$APP_NAME\` |
| Logs | \`kubectl logs -f deployment/$APP_NAME\` |
| Scale | \`kubectl scale deployment $APP_NAME --replicas=N\` |
| Delete | \`kubectl delete -f $K8S_DIR/\` |
EOF

echo "✓ Created Kubernetes skill"
```

## Infrastructure Patterns to Capture

### Pattern 1: SSH Access Matrix

```markdown
## SSH Access

| Host | IP | Purpose | Access |
|------|--------|---------|--------|
| node1 | 192.168.1.10 | Primary | `ssh node1` |
| node2 | 192.168.1.11 | Secondary | `ssh node2` |
| bastion | 203.0.113.5 | Jump host | `ssh -J bastion node1` |
```

### Pattern 2: Service Port Mapping

```markdown
## Service Ports

| Service | Internal | External | Protocol |
|---------|----------|----------|----------|
| Web | 8080 | 80 | HTTP |
| API | 3000 | 443 | HTTPS |
| DB | 5432 | - | TCP |
```

### Pattern 3: Configuration Files

```markdown
## Configuration Locations

### Application Config
- Path: `/etc/app/config.yaml`
- Format: YAML
- Requires restart: Yes

### Database Config
- Path: `/var/lib/postgres/postgresql.conf`
- Format: INI
- Requires restart: Yes
```

### Pattern 4: Command Workflows

```markdown
## Deployment Workflow

1. **Backup current state**
   ```bash
   ./backup.sh
   ```

2. **Pull latest code**
   ```bash
   git pull origin main
   ```

3. **Build application**
   ```bash
   docker build -t app:latest .
   ```

4. **Deploy**
   ```bash
   docker-compose up -d
   ```

5. **Verify**
   ```bash
   curl http://localhost/health
   ```
```

## Best Practices

### ✅ DO

1. **Document assumptions** - What's required before operations
2. **Include verification** - How to verify each operation succeeded
3. **Add troubleshooting** - Common issues and fixes
4. **Show outputs** - Expected command outputs
5. **Link resources** - Related documentation and skills
6. **Version information** - Software versions, configurations
7. **Security notes** - Security implications of operations
8. **Update regularly** - Keep skills current with infrastructure

### ❌ DON'T

1. **Don't hardcode secrets** - Use placeholders or env vars
2. **Don't skip context** - Explain why, not just how
3. **Don't assume knowledge** - Explain terminology
4. **Don't omit edge cases** - Document special scenarios
5. **Don't forget cleanup** - Include teardown procedures
6. **Don't ignore dependencies** - Document prerequisites
7. **Don't skip testing** - Verify all commands work
8. **Don't leave TODO** - Complete all sections

## Quality Checklist

- [ ] Clear component description
- [ ] Authentication/access documented
- [ ] Architecture overview provided
- [ ] Common operations with examples
- [ ] Troubleshooting section complete
- [ ] Health checks documented
- [ ] Backup/recovery procedures
- [ ] Security considerations noted
- [ ] Quick reference table
- [ ] All commands tested
- [ ] No hardcoded secrets
- [ ] Links to resources

## Quick Start Workflow

```bash
# 1. Identify infrastructure component
COMPONENT="nginx-reverse-proxy"

# 2. Gather documentation
# - Collect README files
# - Export wiki pages
# - Capture team knowledge
# - Document current setup

# 3. Create skill structure
mkdir -p skills/$COMPONENT

# 4. Fill in template
# Use the Infrastructure Skill Template above

# 5. Test all commands
# Verify every command in skill works

# 6. Review and refine
# Have team review for completeness

# 7. Commit to repository
git add skills/$COMPONENT
git commit -m "docs: Add $COMPONENT infrastructure skill"
```

---

**Version**: 1.0.0
**Author**: Harvested from proxmox-auth skill pattern
**Last Updated**: 2025-11-18
**License**: MIT
**Key Principle**: Convert tribal knowledge into structured, searchable, actionable skills.

## Examples in This Repository

- **proxmox-auth**: Proxmox VE cluster management
- **docker-***: Docker-based infrastructure
- **cloudflare-***: Cloudflare infrastructure services

Transform your infrastructure documentation into skills today! 🏗️
