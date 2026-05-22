---
name: Deployment Advisor
description: Choose deployment strategy and infrastructure. Use when deciding where to deploy applications, setting up CI/CD, or configuring production environments. Covers Vercel, Railway, AWS, Cloudflare Workers, and Docker.
version: 1.0.0
---

# Deployment Advisor

Choose the right deployment strategy for your application scale and requirements.

## Core Principle

**Start simple, scale when needed.** Don't over-engineer infrastructure for 10 users that won't arrive for months.

## Deployment Tiers

### Tier 1: MVP / Small Projects (<1,000 users)

**Cost**: $0-$20/month
**Time to Deploy**: 5-15 minutes
**Best for**: MVPs, prototypes, side projects, marketing sites

**Recommended Platforms**:

**Vercel** (Next.js, React, static sites):

- Push to GitHub → auto deploy
- Edge functions, image optimization
- Free SSL, global CDN
- $0 for hobby, $20/mo for team

**Netlify** (Static sites, Jamstack):

- Similar to Vercel, better for non-Next.js
- Form handling, split testing
- Serverless functions

**Railway** (Full-stack, databases):

- Deploys anything (Node, Python, Go, Rust)
- Integrated PostgreSQL, Redis, MongoDB
- $5/mo for 512MB RAM + usage

**Cloudflare Pages** (Static + Workers):

- Free unlimited bandwidth
- Edge functions (Workers)
- Fastest CDN globally

---

### Tier 2: Growing Products (1K-100K users)

**Cost**: $20-$500/month
**Time to Deploy**: 1-4 hours
**Best for**: Validated products, growing startups, paid customers

**Recommended Platforms**:

**AWS Amplify** (Full-stack web apps):

- Managed hosting + backend
- Authentication, APIs, databases
- Auto-scaling, monitoring
- $50-200/mo typical

**Google Cloud Run** (Containerized apps):

- Pay only for actual usage
- Scales to zero
- Automatic HTTPS
- $20-100/mo for small traffic

**Fly.io** (Distributed apps):

- Global deployment (closer to users)
- PostgreSQL, Redis included
- Docker-based
- $50-200/mo

**Render** (Simpler alternative to AWS):

- Auto-deploy from Git
- PostgreSQL, Redis, cron jobs
- Free tier available
- $50-150/mo for production

---

### Tier 3: Scale / Enterprise (100K+ users)

**Cost**: $500-$5,000+/month
**Time to Deploy**: 1-4 weeks
**Best for**: High traffic, enterprise, compliance requirements

**Recommended Platforms**:

**AWS ECS** (Containers, no Kubernetes complexity):

- Fargate (serverless containers)
- Full AWS ecosystem
- Fine-grained control
- $500-2000/mo typical

**AWS EKS / Google GKE** (Kubernetes):

- Full orchestration
- Multi-region, auto-scaling
- Complex but powerful
- $1000-5000+/mo

**DigitalOcean App Platform** (Mid-tier simplicity):

- Kubernetes-powered, no K8s knowledge needed
- Cheaper than AWS
- Good middle ground
- $200-1000/mo

---

## Decision Framework

### Question 1: What are you deploying?

**Static site (HTML, CSS, JS)**:
→ Vercel, Netlify, Cloudflare Pages

**Next.js app**:
→ Vercel (best integration), Netlify

**React/Vue/Angular SPA**:
→ Vercel, Netlify, Cloudflare Pages

**Node.js API**:
→ Railway, Render, Fly.io, AWS Amplify

**Python API (FastAPI, Flask, Django)**:
→ Railway, Render, Fly.io, Google Cloud Run

**Go/Rust API**:
→ Fly.io, Railway, Google Cloud Run

**Full-stack (Frontend + Backend + DB)**:
→ Railway, Render, AWS Amplify

**Microservices**:
→ Fly.io, Google Cloud Run, AWS ECS

### Question 2: Do you need a database?

**No database**:
→ Vercel, Netlify, Cloudflare Pages

**Serverless database (PostgreSQL, MySQL)**:
→ Railway, Render (integrated), AWS RDS, Supabase

**Redis/caching**:
→ Railway, Render, AWS ElastiCache, Upstash

**MongoDB**:
→ MongoDB Atlas, Railway, AWS DocumentDB

### Question 3: How many users?

**<100 users (MVP)**:
→ Free/cheap tiers: Vercel free, Railway $5

**100-1,000 users**:
→ Vercel Pro ($20), Railway ($20-50), Render

**1K-10K users**:
→ Railway ($50-100), AWS Amplify, Cloud Run

**10K-100K users**:
→ AWS Amplify, Cloud Run, Fly.io ($100-500)

**100K-1M users**:
→ AWS ECS, GKE, dedicated servers ($500-5000)

### Question 4: Geographic distribution?

**Single region (US/Europe)**:
→ Any platform

**Global (low latency worldwide)**:
→ Cloudflare Pages/Workers, Vercel Edge, Fly.io (multi-region)

**China/Asia**:
→ Cloudflare, Fly.io Hong Kong, Alibaba Cloud

### Question 5: Special requirements?

**Compliance (HIPAA, SOC 2, GDPR)**:
→ AWS, Google Cloud, Azure (compliance certifications)

**Long-running jobs (>15 min)**:
→ Railway, Render Background Workers, AWS ECS

**WebSockets/real-time**:
→ Railway, Render, Fly.io, AWS ECS

**High compute (video processing, ML)**:
→ AWS ECS/EKS, Google Cloud Run, dedicated GPUs

---

## CI/CD Pipeline Setup

### Tier 1: Git Push Auto-Deploy

**Platforms**: Vercel, Netlify, Railway, Render

**Setup** (5 minutes):

1. Connect GitHub/GitLab repo
2. Configure build command: `npm run build`
3. Configure output directory: `dist` or `.next`
4. Push to main branch → auto deploy

**Environment Variables**:

```bash
DATABASE_URL=postgresql://...
API_KEY=secret_key
NODE_ENV=production
```

**Preview Deployments**:

- Every pull request gets preview URL
- Test before merging to production

---

### Tier 2: GitHub Actions CI/CD

**Use when**: Custom tests, security scans, multi-stage deploys

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - run: npm run lint

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
```

---

### Tier 3: Enterprise CI/CD

**Features**:

- Multi-environment (dev, staging, prod)
- Blue-green deployments
- Canary releases
- Automated rollbacks
- Security scanning (SAST, DAST)

**Pipeline Stages**:

```
Build → Test → Security Scan → Stage Deploy → Integration Tests → Prod Deploy
```

**Tools**:

- GitHub Actions, GitLab CI, CircleCI
- ArgoCD (GitOps for Kubernetes)
- Terraform (Infrastructure as Code)

---

## Deployment Checklist

### Pre-Launch

- [ ] Environment variables configured
- [ ] Database migrations tested
- [ ] SSL/HTTPS enabled
- [ ] Custom domain connected
- [ ] Error monitoring set up (Sentry, Rollbar)
- [ ] Analytics configured
- [ ] Backup strategy defined

### Launch Day

- [ ] Deploy to production
- [ ] Verify all pages load
- [ ] Test critical user flows
- [ ] Check error monitoring dashboard
- [ ] Monitor performance metrics
- [ ] Have rollback plan ready

### Post-Launch

- [ ] Monitor logs for errors
- [ ] Check performance (response times)
- [ ] Verify analytics tracking
- [ ] Review cost/usage
- [ ] Document any issues
- [ ] Plan scaling strategy

---

## Common Deployment Patterns

### Pattern 1: Jamstack (Static + API)

**Stack**: Next.js (Vercel) + API (Railway/Supabase)

**Pros**: Fast, cheap, scales easily
**Cons**: Not suitable for real-time or server-heavy apps

```
Frontend (Vercel) → API (Railway) → Database (Supabase)
```

### Pattern 2: Serverless

**Stack**: Vercel Functions + Serverless DB (Supabase/PlanetScale)

**Pros**: Zero server management, pay per use
**Cons**: Cold starts, vendor lock-in

```
Frontend (Vercel) → Edge Functions (Vercel) → Serverless DB
```

### Pattern 3: Traditional Full-Stack

**Stack**: Railway (Node.js + PostgreSQL)

**Pros**: Simple, everything in one place
**Cons**: Single point of failure

```
Railway: Node.js API + PostgreSQL + Redis
```

### Pattern 4: Microservices

**Stack**: Multiple Cloud Run services + Cloud SQL

**Pros**: Independent scaling, fault isolation
**Cons**: Complex, higher cost

```
Frontend (Vercel) → Service 1 (Cloud Run) → Database
                 → Service 2 (Cloud Run) → Queue
```

---

## Cost Optimization

### Free Tier Strategy

- Vercel: Free for personal projects
- Supabase: 500MB DB, 50K API requests/day
- Railway: $5 credit/month (enough for small API)
- Cloudflare: Unlimited bandwidth free

**Total**: $0-5/month for MVP

### Production Cost Optimization

- Use caching (Redis, CDN) to reduce compute
- Optimize images (Next.js Image, Cloudinary)
- Database connection pooling (PgBouncer)
- Monitor and right-size resources
- Use spot instances for non-critical workloads

---

## Security Best Practices

### Must-Haves

- ✅ HTTPS only (automatic on most platforms)
- ✅ Environment variables for secrets (never commit)
- ✅ Database encryption at rest
- ✅ Regular dependency updates
- ✅ Rate limiting on APIs

### Recommended

- Security headers (helmet.js for Node)
- DDoS protection (Cloudflare)
- Automated vulnerability scanning
- Audit logs for sensitive operations
- Backup and disaster recovery plan

---

## Monitoring & Observability

### Tier 1: Basic Monitoring

- Platform dashboards (Vercel Analytics, Railway Metrics)
- Error tracking: Sentry ($0-26/mo)
- Uptime monitoring: UptimeRobot (free), Better Uptime

### Tier 2: Enhanced Monitoring

- APM: New Relic, Datadog ($15-100/mo)
- Log aggregation: LogTail, Papertrail
- Custom metrics and alerting

### Tier 3: Enterprise Observability

- Full stack: Datadog, New Relic ($300-1000+/mo)
- Distributed tracing (OpenTelemetry)
- Custom dashboards (Grafana)
- PagerDuty for incidents

---

## Quick Start Recommendations

**Simple marketing site**:
→ Vercel + Contentful CMS

**SaaS MVP**:
→ Next.js (Vercel) + Supabase (DB + Auth) + Stripe

**Internal tool**:
→ React (Netlify) + FastAPI (Railway) + PostgreSQL (Railway)

**Mobile app backend**:
→ FastAPI (Cloud Run) + Cloud SQL + Firebase Auth

**E-commerce**:
→ Next.js (Vercel) + Shopify/Stripe + PostgreSQL (Supabase)

---

## Related Resources

**Related Skills**:

- `frontend-builder` - For building apps to deploy
- `api-designer` - For API architecture
- `performance-optimizer` - For optimizing deployed apps

**Related Patterns**:

- `META/DECISION-FRAMEWORK.md` - Platform selection guidance
- `STANDARDS/architecture-patterns/deployment-patterns.md` - Deployment architectures (when created)

**Related Playbooks**:

- `PLAYBOOKS/deploy-to-vercel.md` - Vercel deployment guide (when created)
- `PLAYBOOKS/setup-cicd.md` - CI/CD setup procedure (when created)
