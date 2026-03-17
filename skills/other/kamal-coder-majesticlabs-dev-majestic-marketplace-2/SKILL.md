---
name: kamal-coder
description: This skill guides deploying Rails applications with Kamal. Use when configuring deploy.yml, setting up accessories, managing secrets, or preparing servers for container deployment.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Kamal Coder

## Overview

Kamal deploys containerized applications to bare metal or VMs using Docker. It handles zero-downtime deployments with Traefik as reverse proxy.

## Server Requirements

Before Kamal can deploy, servers need:

| Requirement | Purpose |
|-------------|---------|
| Docker | Container runtime |
| SSH access | Kamal connects via SSH |
| Ports 80, 443 open | HTTP/HTTPS traffic |
| Port 22 open | SSH for deployments |

**Provision with:** Ansible (`infra/bin/provision --config`) or cloud-init at boot time.

## Configuration: config/deploy.yml

### Minimal Setup

```yaml
service: myapp
image: username/myapp

servers:
  web:
    hosts:
      - 192.168.1.1
    labels:
      traefik.http.routers.myapp.rule: Host(`myapp.com`)

registry:
  username: username
  password:
    - KAMAL_REGISTRY_PASSWORD

env:
  clear:
    RAILS_ENV: production
    RAILS_LOG_TO_STDOUT: "true"
  secret:
    - RAILS_MASTER_KEY
    - DATABASE_URL
```

### Multi-Role Setup

```yaml
service: myapp
image: username/myapp

servers:
  web:
    hosts:
      - 192.168.1.1
      - 192.168.1.2
    labels:
      traefik.http.routers.myapp.rule: Host(`myapp.com`)
  worker:
    hosts:
      - 192.168.1.3
    cmd: bundle exec sidekiq
    traefik: false  # No HTTP traffic

registry:
  username: username
  password:
    - KAMAL_REGISTRY_PASSWORD

env:
  clear:
    RAILS_ENV: production
  secret:
    - RAILS_MASTER_KEY
    - DATABASE_URL
    - REDIS_URL
```

### With Accessories (Databases, Redis)

```yaml
service: myapp
image: username/myapp

servers:
  web:
    hosts:
      - 192.168.1.1

accessories:
  db:
    image: postgres:16
    host: 192.168.1.1
    port: 5432
    env:
      clear:
        POSTGRES_DB: myapp_production
      secret:
        - POSTGRES_PASSWORD
    directories:
      - data:/var/lib/postgresql/data
    options:
      shm-size: 256m

  redis:
    image: redis:7-alpine
    host: 192.168.1.1
    port: 6379
    directories:
      - data:/data
    cmd: redis-server --appendonly yes
```

## Secrets: .kamal/secrets

Kamal reads secrets from `.kamal/secrets` (git-ignored).

### With 1Password CLI

```bash
# .kamal/secrets
KAMAL_REGISTRY_PASSWORD=$(op read "op://Infrastructure/DockerHub/password")
RAILS_MASTER_KEY=$(op read "op://MyApp/production/master_key")
DATABASE_URL=$(op read "op://MyApp/production/database_url")
POSTGRES_PASSWORD=$(op read "op://MyApp/production-db/password")
```

### With Environment Variables

```bash
# .kamal/secrets
KAMAL_REGISTRY_PASSWORD=$DOCKERHUB_TOKEN
RAILS_MASTER_KEY=$RAILS_MASTER_KEY
DATABASE_URL=$DATABASE_URL
```

### Multi-Environment

```yaml
# config/deploy.yml
<% if ENV["KAMAL_DESTINATION"] == "staging" %>
service: myapp-staging
<% else %>
service: myapp
<% end %>
```

```bash
# .kamal/secrets.staging
RAILS_MASTER_KEY=$(op read "op://MyApp/staging/master_key")
```

## Traefik Configuration

### SSL with Let's Encrypt

```yaml
traefik:
  options:
    publish:
      - "443:443"
    volume:
      - /letsencrypt:/letsencrypt
  args:
    entryPoints.web.address: ":80"
    entryPoints.websecure.address: ":443"
    entryPoints.web.http.redirections.entryPoint.to: websecure
    entryPoints.web.http.redirections.entryPoint.scheme: https
    certificatesResolvers.letsencrypt.acme.email: admin@myapp.com
    certificatesResolvers.letsencrypt.acme.storage: /letsencrypt/acme.json
    certificatesResolvers.letsencrypt.acme.httpchallenge.entrypoint: web

servers:
  web:
    hosts:
      - 192.168.1.1
    labels:
      traefik.http.routers.myapp.rule: Host(`myapp.com`)
      traefik.http.routers.myapp.entrypoints: websecure
      traefik.http.routers.myapp.tls.certresolver: letsencrypt
```

### Health Checks

```yaml
healthcheck:
  path: /up
  port: 3000
  interval: 10s
  max_attempts: 30
```

## Common Commands

### First Deployment

```bash
# Bootstrap server (installs Docker, creates directories)
kamal server bootstrap

# Full setup (push config, start traefik, deploy app)
kamal setup
```

### Regular Deployment

```bash
# Deploy latest
kamal deploy

# Deploy specific version
kamal deploy --version=abc123

# Deploy to staging
kamal deploy -d staging
```

### Rollback

```bash
# List available versions
kamal app containers

# Rollback to previous
kamal rollback
```

### Debugging

```bash
# SSH into container
kamal app exec --interactive bash

# View logs
kamal app logs -f

# Rails console
kamal app exec --interactive "bin/rails console"
```

### Accessories

```bash
# Start all accessories
kamal accessory boot all

# Restart specific accessory
kamal accessory reboot db

# Exec into accessory
kamal accessory exec db --interactive psql -U postgres
```

## Provisioning Workflow

### Terraform + Ansible + Kamal Pipeline

```bash
# infra/bin/provision
#!/usr/bin/env bash
set -euo pipefail

# 1. Terraform: Create infrastructure
cd infra && tofu apply

# 2. Ansible: Configure server
SERVER_IP=$(tofu output -raw server_ip)
cd ansible
echo "[web]\n$SERVER_IP ansible_user=root" > hosts.ini
ansible-playbook -i hosts.ini playbook.yml

# 3. Kamal: Bootstrap containers
cd ../..
bundle exec kamal server bootstrap
```

### What Ansible Should Configure

Based on [kamal-ansible-manager](https://github.com/guillaumebriday/kamal-ansible-manager):

| Task | Purpose |
|------|---------|
| Install Docker | Container runtime |
| Configure fail2ban | SSH intrusion prevention |
| Setup UFW | Firewall (22, 80, 443) |
| Enable NTP | Time synchronization |
| Create swap | Memory overflow protection |
| Harden SSH | Disable password auth, root login |
| Kernel tuning | swappiness, somaxconn |

## Builder Configuration

### Native ARM64 Builds (Hetzner CAX)

```yaml
builder:
  arch: arm64
  # OR for multi-arch:
  # multiarch: true
```

### Remote Builder

```yaml
builder:
  remote:
    arch: amd64
    host: ssh://builder@build-server
```

## Hooks

### Pre-Deploy

```bash
# .kamal/hooks/pre-deploy
#!/bin/sh
echo "Running pre-deploy tasks..."
bundle exec rails assets:precompile
```

### Post-Deploy

```bash
# .kamal/hooks/post-deploy
#!/bin/sh
echo "Running migrations..."
kamal app exec "bin/rails db:migrate"
```

## Directory Structure

```
myapp/
├── config/
│   └── deploy.yml        # Main Kamal config
├── .kamal/
│   ├── secrets           # Secret values (git-ignored)
│   ├── secrets.staging   # Staging secrets (git-ignored)
│   └── hooks/
│       ├── pre-deploy
│       └── post-deploy
└── Dockerfile            # Application container
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Connection refused | Docker not running | `kamal server bootstrap` |
| Permission denied | SSH key not authorized | Check server's authorized_keys |
| Health check failing | App not starting | Check `kamal app logs` |
| Registry auth failed | Wrong credentials | Verify `.kamal/secrets` |
| Traefik 502 | Container not healthy | Increase `max_attempts` |
