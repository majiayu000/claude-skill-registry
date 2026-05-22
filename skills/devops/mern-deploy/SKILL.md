---
name: mern-deploy
description: Deployment checklist and setup for MERN projects targeting Vercel, AWS, or Docker.
argument-hint: "[--target vercel|aws|docker] [--check-only]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Prepare a MERN project for production deployment with proper configuration, security hardening, and monitoring setup.

## Arguments
- `--target <platform>` — Deployment target (default: `vercel`)
  - `vercel` — Vercel (recommended for Next.js)
  - `aws` — AWS (Lambda + API Gateway or ECS)
  - `docker` — Docker container (self-hosted)
- `--check-only` — Run pre-deployment checklist without creating files

## Pre-deployment checklist (always runs)

### Environment
- [ ] All env vars documented in `.env.example`
- [ ] Production env vars set in deployment platform
- [ ] `NEXTAUTH_SECRET` is unique 32+ char string
- [ ] `NODE_ENV=production` in production
- [ ] No secrets in code or committed files

### Database
- [ ] MongoDB Atlas cluster created (or production DB ready)
- [ ] Connection string uses `mongodb+srv://`
- [ ] IP whitelist configured (or `0.0.0.0/0` for serverless)
- [ ] Database user has minimal required permissions

### Security
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Rate limiting enabled
- [ ] CORS configured for production domain
- [ ] Auth secrets rotated from development

### Performance
- [ ] Build succeeds: `pnpm build`
- [ ] No TypeScript errors
- [ ] Bundle size reasonable (check `.next/analyze` if concerned)
- [ ] Images optimized

### Monitoring
- [ ] Error tracking configured (Sentry, etc.)
- [ ] Logging configured for production
- [ ] Health check endpoint working: `/api/health`

## What gets created (per target)

### Vercel
```
vercel.json           # Vercel configuration
```

### AWS
```
serverless.yml        # Serverless Framework config
  or
Dockerfile           # For ECS deployment
buildspec.yml        # CodeBuild config
```

### Docker
```
Dockerfile           # Multi-stage build
docker-compose.yml   # Local testing
.dockerignore        # Ignore patterns
```

## Workflow
1. Run pre-deployment checklist
2. Fix any blockers found
3. Create deployment configuration for target
4. Verify build succeeds
5. Document deployment steps

## Output
- Checklist results (pass/fail)
- Files created
- Next steps for deployment
- Environment variables needed in production

## Reference
For platform-specific configurations, see `reference/mern-deploy-reference.md`
