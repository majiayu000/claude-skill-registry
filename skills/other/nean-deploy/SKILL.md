---
name: nean-deploy
description: Deployment checklist and setup for NEAN projects targeting Docker, AWS, or Kubernetes.
argument-hint: "[--target docker|aws|k8s] [--check-only]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Prepare a NEAN project for production deployment with proper configuration, security hardening, and monitoring setup.

## Arguments
- `--target <platform>` — Deployment target (default: `docker`)
  - `docker` — Docker Compose (self-hosted, simplest)
  - `aws` — AWS (ECS, RDS, ALB)
  - `k8s` — Kubernetes (Helm charts)
- `--check-only` — Run pre-deployment checklist without creating files

## Pre-deployment checklist (always runs)

### Environment
- [ ] All env vars documented in `.env.example`
- [ ] Production env vars set in deployment platform
- [ ] `JWT_SECRET` is unique 64+ char string
- [ ] `NODE_ENV=production` in production
- [ ] No secrets in code or committed files

### Database
- [ ] PostgreSQL instance provisioned
- [ ] Connection string configured
- [ ] Migrations tested and ready
- [ ] Database user has minimal required permissions
- [ ] Backups configured

### Security
- [ ] Helmet middleware configured
- [ ] CORS configured for production domain
- [ ] Rate limiting enabled
- [ ] Auth secrets rotated from development
- [ ] CSP headers configured
- [ ] HTTPS enforced

### Performance
- [ ] Build succeeds: `npm run build`
- [ ] No TypeScript errors
- [ ] Angular bundle size reasonable (check with `npm run build -- --stats-json`)
- [ ] API response times acceptable
- [ ] Database indexes in place

### Monitoring
- [ ] Error tracking configured (Sentry, etc.)
- [ ] Logging configured for production (structured JSON)
- [ ] Health check endpoints working: `/api/health`, `/api/health/ready`
- [ ] Metrics collection configured (optional)

## What gets created (per target)

### Docker
```
docker/
├── Dockerfile.api           # Multi-stage NestJS build
├── Dockerfile.web           # Multi-stage Angular build + Nginx
├── docker-compose.yml       # Full stack
├── docker-compose.prod.yml  # Production overrides
└── nginx.conf               # Nginx configuration
```

### AWS
```
infrastructure/
├── terraform/               # Infrastructure as code
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── ecs/
│   └── task-definition.json
└── scripts/
    └── deploy.sh            # Deployment script
```

### Kubernetes
```
k8s/
├── helm/
│   └── myapp/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values.prod.yaml
│       └── templates/
│           ├── api-deployment.yaml
│           ├── web-deployment.yaml
│           ├── service.yaml
│           ├── ingress.yaml
│           ├── configmap.yaml
│           └── secrets.yaml
└── skaffold.yaml            # Local development
```

## Docker deployment (recommended for self-hosted)

### Build and run
```bash
# Build images
docker compose -f docker/docker-compose.yml build

# Run locally
docker compose -f docker/docker-compose.yml up -d

# Production with overrides
docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d
```

### Production docker-compose.prod.yml
```yaml
version: '3.8'

services:
  api:
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
    restart: always

  web:
    deploy:
      replicas: 2
    restart: always

  db:
    volumes:
      - /data/postgres:/var/lib/postgresql/data
    restart: always
```

## Environment-specific configuration

### API environment
```bash
# Production .env for API
NODE_ENV=production
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_USERNAME=myapp
DATABASE_PASSWORD=${DB_PASSWORD}  # From secrets
DATABASE_NAME=myapp_prod
JWT_SECRET=${JWT_SECRET}          # From secrets
JWT_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d
CORS_ORIGINS=https://myapp.com
API_PORT=3000
LOG_LEVEL=info
```

### Angular environment
```typescript
// environment.prod.ts
export const environment = {
  production: true,
  apiUrl: '/api',  // Relative, goes through Nginx
};
```

## Workflow
1. Run pre-deployment checklist
2. Fix any blockers found
3. Create deployment configuration for target
4. Verify builds succeed
5. Test in staging environment
6. Document deployment steps
7. Set up monitoring and alerts

## Output
- Checklist results (pass/fail)
- Files created
- Next steps for deployment
- Environment variables needed in production
- Monitoring setup instructions

## Reference
For platform-specific configurations, see `reference/nean-deploy-reference.md`
