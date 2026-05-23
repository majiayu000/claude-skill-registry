---
name: convex-self-hosting
description: Guides self-hosted Convex deployment, authentication setup, environment configuration, troubleshooting, and production deployment considerations.
---

# Convex Self-Hosting

Expert guidance for deploying and managing self-hosted Convex instances.

## Quick Start

> **IMPORTANT CLI LIMITATION**: The Convex CLI (`npx convex`) is designed primarily for Convex Cloud and has **limited support for self-hosted backends**. Many CLI commands may not work correctly with self-hosted deployments. Environment-based configuration and direct API interaction is often required instead.

```bash
# Docker deployment (recommended)
git clone https://github.com/get-convex/convex-backend
cd convex-backend/self-hosted
docker compose up
docker compose exec backend ./generate_admin_key.sh

# Configure environment
export CONVEX_SELF_HOSTED_URL=http://127.0.0.1:3210
export CONVEX_SELF_HOSTED_ADMIN_KEY=<your-key>

# Deploy your functions (may have limited functionality with self-hosted)
npx convex deploy
```

## Core Concepts

### What is Self-Hosted Convex?

- **Same code** as Convex Cloud (open-sourced February 2025)
- **Full operational responsibility** (scaling, migrations, backups, security)
- **Single-node by default** (horizontal scaling requires code modifications)
- **FSL Apache 2.0 License** (converts to standard Apache 2.0 after 4 years)

### When to Self-Host

**Use self-hosting for:**
- Data sovereignty/compliance requirements
- Private network/VPC deployment
- Specific geographic data residency
- Unlimited testing environments
- Integration with existing infrastructure

**Use Convex Cloud for:**
- Automatic scaling
- Managed migrations
- Professional support
- Reduced operational overhead

## Essential Environment Variables

### Required

| Variable | Purpose | Example |
|----------|---------|---------|
| `CONVEX_SELF_HOSTED_URL` | Backend API URL | `http://127.0.0.1:3210` |
| `CONVEX_SELF_HOSTED_ADMIN_KEY` | Admin authentication | Generated via script |

### Platform-Specific (PaaS)

| Variable | Purpose | Example |
|----------|---------|---------|
| `CONVEX_CLOUD_ORIGIN` | Backend API endpoint | `https://your-app.fly.dev` |
| `CONVEX_SITE_ORIGIN` | HTTP actions endpoint | `https://your-site.fly.dev` |

### Database

| Variable | Purpose | Example |
|----------|---------|---------|
| `POSTGRES_URL` | Postgres connection (preferred) | `postgres://user:pass@host:5432?sslmode=require` |
| `DATABASE_URL` | Alternative connection string | `postgresql://user:pass@host/dbname` |

> **Gotcha**: Use `POSTGRES_URL` instead of `DATABASE_URL` for better compatibility. Remove database name from URL - Convex adds it based on `INSTANCE_NAME`.

### Security

| Variable | Purpose | Example |
|----------|---------|---------|
| `INSTANCE_SECRET` | Instance authentication | Generate with `openssl rand -hex 32` |
| `DISABLE_BEACON` | Disable telemetry | `true` |

## Authentication (@convex-dev/auth)

> **Critical**: The CLI does not support self-hosted deployments for Convex Auth. Manual setup required.

### Required Environment Variables

#### JWT_PRIVATE_KEY

**Format**: Must be **PKCS#8** format (NOT PKCS#1/RSAPrivateKey).

**Generate**:
```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out jwt_private_key.pem
```

**Verify**: File should start with `-----BEGIN PRIVATE KEY-----` (NOT `-----BEGIN RSA PRIVATE KEY-----`).

#### JWKS

**Purpose**: Public key set for verifying JWT signatures.

**Required Format**:
```json
{
  "keys": [{
    "kty": "RSA",
    "e": "AQAB",
    "n": "...",
    "alg": "RS256",
    "kid": "unique-key-id",
    "use": "sig"
  }]
}
```

#### JWT_ISSUER

**Purpose**: The issuer URL for JWT tokens. Must match your Convex deployment URL.

```bash
JWT_ISSUER=https://your-convex-url.com
```

## Common Gotchas

| Issue | Solution |
|-------|----------|
| **Multi-line env vars fail** | CLI doesn't support multi-line values (like PEM keys). Use base64 encoding or dashboard UI. |
| **POSTGRES_URL vs DATABASE_URL** | Use `POSTGRES_URL` without database name. Convex adds it based on `INSTANCE_NAME`. |
| **Database name required** | Must create database named `convex_self_hosted` for Postgres setups. |
| **Single-node scaling** | Self-hosted is single-node by default. Horizontal scaling requires Rust codebase modifications. |
| **Never use `latest` tag** | Pin to specific versions in production to avoid breaking changes. |
| **Beacon telemetry** | Self-hosted instances send anonymous telemetry. Disable with `DISABLE_BEACON=true`. |

## Platform-Specific Deployments

### Fly.io

```toml
[env]
  CONVEX_CLOUD_ORIGIN = "https://your-app.fly.dev"
  CONVEX_SITE_ORIGIN = "https://your-app.fly.dev"
```

### Railway

One-click deployment with built-in Postgres.

### AWS (EC2/SST)

- **SST** for infrastructure as code
- **EC2** for compute
- **RDS** for database
- **S3** for file storage

### Coder Workspace

For Coder workspaces, use the automatic port-based DNS routing:
```
https://<service>--<workspace>--<owner>.coder.<domain>
```

> **Note**: Replace `<workspace>`, `<owner>`, and `<domain>` with your specific Coder environment values.

**Required Services:**

| Service | Port | URL Pattern | Purpose |
|---------|------|-------------|---------|
| Convex API | 3210 | `https://convex-api--<workspace>--<owner>.coder.<domain>` | Main API endpoint |
| Convex Site Proxy | 3211 | `https://convex-site--<workspace>--<owner>.coder.<domain>` | HTTP actions / auth |
| Convex Dashboard | 6791 | `https://convex--<workspace>--<owner>.coder.<domain>` | Dashboard UI |

**Required Environment Variables for Coder:**
```bash
CONVEX_CLOUD_ORIGIN=https://convex-api--<workspace>--<owner>.coder.<domain>
CONVEX_SITE_ORIGIN=https://convex-site--<workspace>--<owner>.coder.<domain>
JWT_ISSUER=https://convex-site--<workspace>--<owner>.coder.<domain>
```

**JWT Key Handling for Coder:**

For proper authentication in Coder workspaces, use a custom entrypoint script that loads the JWT_PRIVATE_KEY from a mounted file:

1. **Generate PKCS#8 formatted key:**
   ```bash
   openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out jwt_private_key.pem
   ```

2. **Create custom entrypoint** ([convex-backend-entrypoint.sh](convex-backend-entrypoint.sh)):
   ```bash
   #!/bin/bash
   set -e

   # Load JWT_PRIVATE_KEY from mounted file
   if [ -f /jwt_private_key.pem ]; then
     echo "Loading JWT_PRIVATE_KEY from /jwt_private_key.pem..."
     DECODED_KEY=$(cat /jwt_private_key.pem)
     export JWT_PRIVATE_KEY="$DECODED_KEY"
   fi

   # Run Convex backend
   exec env JWT_PRIVATE_KEY="$JWT_PRIVATE_KEY" ./convex-local-backend \
     --instance-name "$INSTANCE_NAME" \
     --instance-secret "$INSTANCE_SECRET" \
     --port 3210 \
     --site-proxy-port 3211 \
     --convex-origin "$CONVEX_CLOUD_ORIGIN" \
     --convex-site "$CONVEX_SITE_ORIGIN" \
     --db postgres-v5 \
     "$POSTGRES_URL"
   ```

3. **Mount in Docker Compose:**
   ```yaml
   services:
     convex-backend:
       image: ghcr.io/get-convex/convex-backend:latest
       volumes:
         - ./jwt_private_key.pem:/jwt_private_key.pem:ro
         - ./convex-backend-entrypoint.sh:/convex-backend-entrypoint.sh:ro
       entrypoint: ["/bin/bash", "/convex-backend-entrypoint.sh"]
   ```

For complete Coder workspace setup, see the `coder-convex-setup` skill.

## Production Checklist

### Pre-Deployment
- [ ] Estimate traffic/load requirements
- [ ] Define data retention requirements
- [ ] Plan backup strategy
- [ ] Choose hosting platform
- [ ] Register domain and configure DNS

### Infrastructure
- [ ] Provision PostgreSQL instance
- [ ] Create `convex_self_hosted` database
- [ ] Configure S3 or S3-compatible storage
- [ ] Generate secure `INSTANCE_SECRET`
- [ ] Configure reverse proxy with SSL (nginx/Caddy)
- [ ] Set up firewall rules
- [ ] Configure rate limiting

### Security
- [ ] Rotate admin keys regularly
- [ ] Use different keys for dev/staging/production
- [ ] Store secrets in secret management systems
- [ ] Disable beacon if required
- [ ] Set up monitoring and alerting

### Backup/DR
- [ ] Set up automated backups
- [ ] Configure off-site backup storage
- [ ] Test restore procedures
- [ ] Document recovery procedures

## Reference Documentation

For detailed information on specific topics, see:

- **[Deployment Methods](reference/deployment.md)** - Docker, build from source, platform-specific guides
- **[Authentication Guide](reference/authentication.md)** - Complete JWT setup, troubleshooting, security best practices
- **[Environment Variables](reference/environment.md)** - Complete reference for all configuration options
- **[Production Configuration](reference/production.md)** - Security, monitoring, backups, scaling
- **[Troubleshooting](reference/troubleshooting.md)** - Common issues and solutions
- **[Platform Guides](reference/platforms.md)** - Fly.io, Railway, AWS, Neon, Kubernetes, Coder workspaces

## Resources

- [Official Self-Hosting Docs](https://docs.convex.dev/self-hosting)
- [GitHub Repository](https://github.com/get-convex/convex-backend)
- [Self-Hosting Blog](https://stack.convex.dev/self-hosted-develop-and-deploy)
- [#self-hosted Discord](https://www.convex.dev/discord)
