---
name: deploying-applications
description: Deployment patterns from Kubernetes to serverless and edge functions. Use when deploying applications, setting up CI/CD, or managing infrastructure. Covers Kubernetes (Helm, ArgoCD), serverless (Vercel, Lambda), edge (Cloudflare Workers, Deno), IaC (Pulumi, OpenTofu, SST), and GitOps patterns.
---

# Deploying Applications

Production deployment patterns from Kubernetes to serverless and edge functions. Bridges the gap from application assembly to production infrastructure.

## Purpose

This skill provides clear guidance for:
- Selecting the right deployment strategy (Kubernetes, serverless, containers, edge)
- Implementing Infrastructure as Code with Pulumi or OpenTofu
- Setting up GitOps automation with ArgoCD or Flux
- Choosing serverless databases (Neon, Turso, PlanetScale)
- Deploying edge functions (Cloudflare Workers, Deno Deploy)

## When to Use This Skill

Use this skill when:
- Deploying applications to production infrastructure
- Setting up CI/CD pipelines and GitOps workflows
- Choosing between Kubernetes, serverless, or edge deployment
- Implementing Infrastructure as Code (Pulumi, OpenTofu, SST)
- Migrating from manual deployment to automated infrastructure
- Integrating with `assembling-components` for complete deployment flow

## Deployment Strategy Decision Tree

```
WORKLOAD TYPE?

├── COMPLEX MICROSERVICES (10+ services)
│   └─ Kubernetes + ArgoCD/Flux (GitOps)
│       ├─ Helm 4.0 for packaging
│       ├─ Service mesh: Linkerd (5-10% overhead) or Istio (25-35%)
│       └─ See references/kubernetes-patterns.md

├── VARIABLE TRAFFIC / COST-SENSITIVE
│   └─ Serverless
│       ├─ Database: Neon/Turso (scale-to-zero)
│       ├─ Compute: Vercel, AWS Lambda, Cloud Functions
│       ├─ Edge: Cloudflare Workers (<5ms cold start)
│       └─ See references/serverless-dbs.md and references/edge-functions.md

├── CONSISTENT LOAD / PREDICTABLE TRAFFIC
│   └─ Containers (ECS, Cloud Run, Fly.io)
│       ├─ ECS Fargate: AWS-native, serverless containers
│       ├─ Cloud Run: GCP, scale-to-zero containers
│       └─ Fly.io: Global edge, multi-region

├── GLOBAL LOW-LATENCY (<50ms)
│   └─ Edge Functions + Edge Database
│       ├─ Cloudflare Workers + D1 (SQLite)
│       ├─ Deno Deploy + Turso (libSQL)
│       └─ See references/edge-functions.md

└── RAPID PROTOTYPING / STARTUP MVP
    └─ Managed Platform as a Service
        ├─ Vercel (Next.js, zero-config)
        ├─ Railway (any framework)
        └─ Render (auto-deploy from Git)

IaC CHOICE?

├─ TypeScript-first → Pulumi (Apache 2.0, multi-cloud)
├─ HCL-based → OpenTofu (CNCF, Terraform-compatible)
└─ Serverless TypeScript → SST v3 (built on Pulumi)
```

## Core Concepts

### Infrastructure as Code (IaC)

Define infrastructure using code instead of manual configuration.

**Primary: Pulumi (TypeScript)**
- Context7 ID: `/pulumi/docs` (Trust: 94.6/100, 9,525 snippets)
- TypeScript-first (same language as React/Next.js)
- Multi-cloud support (AWS, GCP, Azure, Cloudflare)
- See references/pulumi-guide.md for patterns and examples

**Alternative: OpenTofu (HCL)**
- CNCF project, Terraform-compatible
- MPL-2.0 license (open governance)
- Drop-in Terraform replacement
- See references/opentofu-guide.md for migration

**Serverless: SST v3 (TypeScript)**
- Built on Pulumi
- Optimized for AWS Lambda, API Gateway
- Live Lambda development

### GitOps Deployment

Declarative infrastructure with Git as source of truth.

**ArgoCD** (Recommended for platform teams):
- Rich web UI
- Built-in RBAC and multi-tenancy
- Self-healing deployments
- See references/gitops-argocd.md

**Flux** (Recommended for DevOps automation):
- Kubernetes-native
- CLI-focused
- Simpler architecture
- See references/gitops-argocd.md

### Service Mesh

Optional layer for microservices communication, security, and observability.

**When to Use Service Mesh**:
- Multi-team microservices (security boundaries)
- Zero-trust networking (mTLS required)
- Advanced traffic management (canary, blue-green)

**When NOT to Use**:
- Simple monolith or 2-3 services (overhead not justified)
- Serverless architectures (incompatible)

**Linkerd** (Performance-focused):
- 5-10% overhead
- Rust-based
- Simple, opinionated

**Istio** (Feature-rich):
- 25-35% overhead
- C++ (Envoy)
- Advanced routing, observability

See references/kubernetes-patterns.md for service mesh patterns.

## Quick Start Workflows

### Workflow 1: Deploy Next.js to Vercel (Zero-Config)

```bash
# Install Vercel CLI
npm i -g vercel

# Link project
vercel link

# Deploy to production
vercel --prod
```

See examples/nextjs-vercel/ for complete example.

### Workflow 2: Deploy to Kubernetes with ArgoCD

1. Create Helm chart
2. Push chart to Git repository
3. Create ArgoCD Application
4. ArgoCD syncs automatically

See examples/k8s-argocd/ for complete GitOps setup.

### Workflow 3: Deploy Serverless with Pulumi

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Create Lambda function
const lambda = new aws.lambda.Function("api", {
    runtime: "nodejs20.x",
    handler: "index.handler",
    role: role.arn,
    code: new pulumi.asset.FileArchive("./dist"),
});

export const apiUrl = lambda.invokeArn;
```

See examples/pulumi-aws/ and references/pulumi-guide.md for patterns.

### Workflow 4: Deploy Edge Function to Cloudflare Workers

```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/api/hello', (c) => {
  return c.json({ message: 'Hello from edge!' })
})

export default app
```

Deploy with Wrangler:
```bash
wrangler deploy
```

See examples/cloudflare-workers-hono/ and references/edge-functions.md.

## Integration with assembling-components

After building an application with `assembling-components`, this skill provides deployment patterns:

**Frontend (Next.js/Vite) → Deployment**:
1. Review deployment decision tree
2. Choose platform: Vercel (Next.js), Cloudflare Pages (static), or custom (Pulumi)
3. Set up environment variables
4. Deploy using chosen method

**Backend (FastAPI/Axum) → Deployment**:
1. Containerize application (Dockerfile)
2. Choose platform: ECS Fargate, Cloud Run, or Kubernetes
3. Set up IaC (Pulumi or OpenTofu)
4. Deploy with GitOps (ArgoCD/Flux) or CI/CD

See references/pulumi-guide.md for integration examples.

## Reference Files

### Kubernetes Deployment
- **references/kubernetes-patterns.md** - Helm 4.0, service mesh, autoscaling
- **references/gitops-argocd.md** - ArgoCD/Flux GitOps workflows

### Serverless & Edge
- **references/serverless-dbs.md** - Neon, Turso, PlanetScale (scale-to-zero)
- **references/edge-functions.md** - Cloudflare Workers, Deno Deploy (<5ms cold starts)

### Infrastructure as Code
- **references/pulumi-guide.md** - Pulumi TypeScript patterns, component model
- **references/opentofu-guide.md** - OpenTofu/Terraform migration

## Utility Scripts

Scripts in `scripts/` are executed without loading into context (token-free).

**Generate Kubernetes Manifests**:
```bash
python scripts/generate_k8s_manifests.py --app-name my-app --replicas 3
```

**Validate Deployment Configuration**:
```bash
python scripts/validate_deployment.py --config deployment.yaml
```

See script files for full usage documentation.

## Examples

Complete, runnable examples in `examples/`:

- **pulumi-aws/** - ECS Fargate deployment with Pulumi
- **k8s-argocd/** - Kubernetes + ArgoCD GitOps
- **sst-serverless/** - SST v3 serverless TypeScript

Each example includes:
- README.md with setup instructions
- Complete source code
- Environment variable configuration
- Deployment commands

## Library Recommendations

### Infrastructure as Code (2025)

**Primary: Pulumi**
- Context7: `/pulumi/docs` (Trust: 94.6, 9,525 snippets)
- TypeScript-first, multi-cloud
- Apache 2.0 license

**Alternative: OpenTofu**
- CNCF project, MPL-2.0
- Terraform-compatible
- HCL syntax

**Serverless: SST v3**
- Built on Pulumi
- AWS Lambda optimized
- TypeScript-native

### Serverless Databases

**Neon PostgreSQL**:
- Database branching (like Git)
- Scale-to-zero compute
- Full PostgreSQL compatibility

**Turso SQLite**:
- Edge deployment (200+ locations)
- Sub-millisecond reads
- libSQL (SQLite fork)

**PlanetScale MySQL**:
- Non-blocking schema changes
- Vitess-powered
- Per-row pricing

See references/serverless-dbs.md for comparison and integration.

### Edge Functions

**Cloudflare Workers**:
- <5ms cold starts (V8 isolates)
- 200+ edge locations
- 128MB memory per request

**Deno Deploy**:
- TypeScript-native
- Web Standard APIs
- Global edge (<50ms)

**Hono Framework**:
- Runs on all edge runtimes
- 14KB bundle size
- TypeScript-first

See references/edge-functions.md for patterns.

## Best Practices

### Security
- Use secrets management (AWS Secrets Manager, Vault)
- Enable mTLS for service-to-service communication
- Implement least-privilege IAM roles
- Scan container images for vulnerabilities

### Cost Optimization
- Use serverless databases for variable traffic (scale-to-zero)
- Enable horizontal pod autoscaling (HPA) in Kubernetes
- Right-size compute resources (CPU/memory)
- Use spot instances for non-critical workloads

### Performance
- Deploy close to users (edge functions for global apps)
- Use CDN for static assets (CloudFront, Cloudflare)
- Implement caching strategies (Redis, CloudFront)
- Monitor cold start times for serverless

### Reliability
- Implement health checks (Kubernetes liveness/readiness probes)
- Set up auto-scaling (HPA, Lambda concurrency)
- Use multi-region deployments for critical services
- Implement circuit breakers and retries

## Troubleshooting

### Deployment Failures

**Kubernetes pod fails to start**:
1. Check pod logs: `kubectl logs <pod-name>`
2. Describe pod: `kubectl describe pod <pod-name>`
3. Verify resource limits and requests
4. Check image pull errors (imagePullSecrets)

**Serverless cold starts too slow**:
1. Reduce bundle size (tree-shaking, code splitting)
2. Use provisioned concurrency (AWS Lambda)
3. Consider edge functions (Cloudflare Workers)
4. Optimize initialization code

**GitOps sync errors (ArgoCD/Flux)**:
1. Verify Git repository access
2. Check manifest validity (`kubectl apply --dry-run`)
3. Review sync policies (prune, selfHeal)
4. Check ArgoCD/Flux logs

### Performance Issues

**High service mesh overhead**:
1. Consider switching to Linkerd (5-10% vs Istio 25-35%)
2. Disable unnecessary features
3. Evaluate if service mesh is needed

**Database connection pool exhaustion**:
1. Increase connection pool size
2. Use serverless databases (Neon scale-to-zero)
3. Implement connection pooling (PgBouncer)

See references/ files for detailed troubleshooting guides.

## Migration Patterns

### From Manual to IaC

1. Inventory existing infrastructure
2. Start with non-critical environments (dev, staging)
3. Use Pulumi/OpenTofu to codify infrastructure
4. Test in staging before production
5. Gradual migration (one service at a time)

### From Terraform to OpenTofu

```bash
# Install OpenTofu
brew install opentofu

# Migrate state
terraform state pull > terraform.tfstate.backup
tofu init -migrate-state
tofu plan
tofu apply
```

See references/opentofu-guide.md for complete migration.

### From EC2 to Containers

1. Containerize application (create Dockerfile)
2. Test locally (Docker Compose)
3. Deploy to staging (ECS/Cloud Run/Kubernetes)
4. Monitor performance and costs
5. Cutover production traffic (blue-green deployment)

### From Containers to Serverless

1. Identify stateless services
2. Refactor to serverless-friendly patterns
3. Use serverless databases (Neon/Turso)
4. Deploy to Lambda/Cloud Functions
5. Monitor cold starts and costs

## Next Steps

After deploying applications:
- Set up observability (metrics, logs, traces)
- Implement CI/CD pipelines (GitHub Actions, GitLab CI)
- Configure auto-scaling and resource limits
- Set up disaster recovery and backups
- Document runbooks for incident response

## Additional Resources

- Pulumi documentation: https://www.pulumi.com/docs/
- OpenTofu documentation: https://opentofu.org/docs/
- ArgoCD documentation: https://argo-cd.readthedocs.io/
- Cloudflare Workers docs: https://developers.cloudflare.com/workers/
- Neon documentation: https://neon.tech/docs/
