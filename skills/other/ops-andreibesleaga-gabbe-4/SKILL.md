---
name: deployment
description: CI/CD pipeline verification, Docker container security, environment management, and deployment workflow
triggers: [deploy, CI/CD, Docker, pipeline, environment, release, container, staging, production]
context_cost: medium
---

# Deployment Skill

## Goal
Ensure software is deployed safely, securely, and repeatably. Verify CI/CD pipeline health, container security, environment configuration, and rollback readiness before any production deployment.

## Steps

1. **Pre-deployment checklist**
   ```
   [ ] All tests passing (integrity-check.skill completed)
   [ ] SECURITY_CHECKLIST.md completed
   [ ] No critical CVEs in dependencies
   [ ] Environment variables documented and configured
   [ ] Database migrations reviewed and tested
   [ ] Rollback plan documented
   [ ] Monitoring and alerting in place
   ```

2. **Verify CI/CD pipeline**
   ```yaml
   # GitHub Actions example structure to verify:
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - run: [install command]
         - run: [test command]          # Must be here
         - run: [typecheck command]     # Must be here
         - run: [lint command]          # Must be here
         - run: [security scan]        # Must be here

     build:
       needs: [test]  # Build only after tests pass
       steps:
         - run: docker build -t app:${{ github.sha }} .
         - run: trivy image app:${{ github.sha }}  # Container scan

     deploy-staging:
       needs: [build]
       environment: staging  # Requires manual approval in GitHub
   ```

3. **Docker container security check**
   ```dockerfile
   # Verify Dockerfile follows security best practices:
   FROM node:22-alpine AS base     # Use specific version (not :latest)
   WORKDIR /app

   # Security: run as non-root user
   RUN addgroup -S appgroup && adduser -S appuser -G appgroup

   # Security: copy only necessary files
   COPY package*.json ./
   RUN npm ci --only=production     # No dev dependencies in production

   COPY --chown=appuser:appgroup . .

   USER appuser                     # Never run as root

   EXPOSE 3000
   CMD ["node", "dist/server.js"]
   ```

   ```bash
   # Scan container for vulnerabilities
   trivy image app:latest --severity HIGH,CRITICAL
   docker scout cves app:latest  # Docker Scout alternative
   ```

4. **IaC security check** (if applicable)
   ```bash
   # Terraform/Kubernetes manifests
   checkov -d infra/
   tfsec infra/terraform/

   # Kubernetes
   kubesec scan infra/kubernetes/deployment.yaml
   ```

5. **Environment configuration**
   ```bash
   # Verify all required env vars are documented and configured
   # Check: .env.example has all vars without values
   # Check: production env vars set in GitHub Secrets / AWS SSM / Vault

   # Never: env vars with secrets in CI/CD config files
   # Never: docker-compose.yml with hardcoded production secrets
   ```

6. **Database migration execution** (before deploying new code)
   ```bash
   # Run migrations BEFORE deploying new code (backward compatible)
   # This ensures rollback is possible without data issues

   # Prisma
   npx prisma migrate deploy --schema=prisma/schema.prisma

   # Laravel
   php artisan migrate --force --no-interaction

   # Python (Alembic)
   uv run alembic upgrade head
   ```

   **Python Docker Security:**
   ```dockerfile
   FROM python:3.12-slim-bookworm AS base
   WORKDIR /app
   
   # Security: non-root user
   RUN addgroup --system appgroup && adduser --system --group appuser

   # Install uv
   COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

   COPY pyproject.toml uv.lock ./
   RUN uv sync --frozen --no-dev

   COPY --chown=appuser:appgroup . .
   
   USER appuser
   CMD ["uv", "run", "fastapi", "run", "src/main/main.py", "--port", "8000"]
   ```

7. **Deploy to staging first**
   ```bash
   # Blue-Green or rolling deployment
   # Run smoke tests after staging deploy

   # Smoke test examples:
   curl -f https://staging.app.com/health || exit 1
   curl -f https://staging.app.com/api/v1/ping || exit 1
   ```

8. **Smoke tests after deployment**
   ```typescript
   // tests/smoke/health.spec.ts
   test('health check returns 200', async ({ request }) => {
     const response = await request.get('/health');
     expect(response.status()).toBe(200);
     const body = await response.json();
     expect(body.status).toBe('ok');
   });

   test('authentication endpoint accepts requests', async ({ request }) => {
     const response = await request.post('/auth/login', {
       data: { email: 'test@example.com', password: 'wrong' }
     });
     expect(response.status()).toBe(401); // Wrong creds — correct behavior
   });
   ```

9. **Production deployment gate**
   - Requires human approval (configured in CI/CD environment protection rules)
   - Tag the release: `git tag v[semver] -m "Release [version]"`
   - Create GitHub Release with changelog

10. **Post-deployment verification**
    ```bash
    # Verify production health
    curl -f https://app.com/health

    # Check error rates in monitoring (Sentry, Datadog, etc.)
    # Verify no sudden spike in error rate after deploy
    # Verify response times are within baseline

    # If error rate spikes: trigger rollback immediately
    ```

11. **Rollback plan**
    ```bash
    # Document before deploying:
    # 1. Previous stable version: v1.2.3
    # 2. Rollback command: kubectl rollout undo deployment/app
    # 3. Database: were there migrations? Can they be rolled back?
    # 4. Cache: does rollback require cache flush?
    # 5. Decision maker: who approves the rollback call?

    # Kubernetes rollback:
    kubectl rollout undo deployment/app --to-revision=N

    # Docker Compose rollback:
    docker pull app:v1.2.3
    docker compose up -d
    ```

## Constraints
- NEVER deploy to production without first deploying and testing on staging
- NEVER skip container security scan in CI/CD pipeline
- NEVER commit secrets to CI/CD config files
- Production deployment ALWAYS requires human approval
- Always have a tested rollback plan before deploying

## Output Format
Deployment checklist completion + CI/CD pipeline verification + staging test results + production deployment confirmation or rollback if issues found.
