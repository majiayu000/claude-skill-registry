---
name: pipeline-design
description: Use when designing CI/CD pipelines, selecting deployment strategies, or architecting continuous delivery workflows. Covers platform decisions (GitHub Actions vs GitLab CI), build pipeline structure, deployment strategies (rolling/canary/blue-green), approval gates, and DORA metrics.
---

# Pipeline Design

## Platform Selection

| Factor | GitHub Actions | GitLab CI |
|--------|---------------|-----------|
| **Best for** | OSS, GitHub-native repos | Self-hosted, mono-repos, complex workflows |
| **Reuse model** | Reusable workflows + composite actions | YAML anchors + `include` templates, dynamic child pipelines |
| **Container builds** | docker/build-push-action with GHA cache | DinD service (slower) or Kaniko |
| **Security scanning** | Third-party (Trivy, Snyk, CodeQL) | Built-in templates (SAST, container, dependency) |
| **Secrets** | Environment-scoped, OIDC for cloud | CI/CD variables, group-level inheritance |
| **Approval gates** | Environment protection rules | `when: manual` + protected environments |

**Decision**: GitHub for smaller teams + cloud-native, GitLab for self-hosted + complex orchestration.

## Build Pipeline Structure

**Minimum stages** (never skip lint):
1. **Lint** → unit tests (fail fast)
2. **Build** → containerize, tag with `$COMMIT_SHA`
3. **Security scan** → Trivy/CodeQL
4. **Staging deploy** → auto-deploy from main
5. **Production deploy** → manual approval + tag-triggered

### Parallelism
- Run lint + unit tests parallel (independent)
- Matrix builds for multi-version/multi-OS testing
- Docker layer caching: `cache-from: type=gha` + `cache-to: type=gha,mode=max`

### Artifacts & Caching
- **GitHub**: Use `actions/setup-*` built-in caching (`cache:` parameter), `hashFiles('**/package-lock.json')`
- **GitLab**: Cache key `${CI_COMMIT_REF_SLUG}`, use `policy: pull-push`, prefer `artifacts` for stage handoff
- **Expire artifacts**: 1h intermediates, 1d deploy artifacts (unbounded artifacts = storage waste)

## Deployment Strategy Selection

| Strategy | Use When | Rollback Time | Risk |
|----------|----------|---------------|------|
| **Rolling update** | Low-traffic services, no state migration | 5-10m | Medium (partial outage if fails) |
| **Blue-green** | Stateless APIs, need instant rollback | <1m | Low (switch load balancer) |
| **Canary** | High-traffic services, catch bugs early | 15-30m | Low (gradual rollout) |
| **Feature flags** | Complex business logic, team gating | Instant | Lowest (conditional logic) |

**Guardrails**: Always use one strategy consistently per environment. Never mix.

## Approval Gates

| Pattern | Best For | Key Setting |
|---------|----------|-------------|
| **Manual approval** | Production deploys, compliance | Environment protection rules (GitHub) / `when: manual` (GitLab) |
| **Tag-triggered** | Release trains, semantic versioning | Only deploy on `refs: tags/v*` |
| **Time-based** | Scheduled maintenance windows | GitLab `when: delayed` + `start_in: 30m` |
| **Multi-approver** | Enterprise compliance | Azure Pipelines `ManualValidation@0` + email notifiers |

**Rule**: Never auto-deploy to production. Always require manual gate OR tag-triggered release.

## Security Scanning

**Non-negotiable**: Every pipeline must include dependency scanning + SAST.

### GitHub Actions
- Pin action versions to SHA (not tags): `uses: actions/checkout@abc123...` not `@v4`
- Trivy for filesystem + container scanning → output SARIF → GitHub Security tab
- CodeQL for deep SAST analysis
- Set `permissions:` block explicitly per job (default token has limited perms)

### GitLab CI
- Use built-in `include`: `Security/SAST.gitlab-ci.yml`, `Security/Dependency-Scanning.gitlab-ci.yml`, `Security/Container-Scanning.gitlab-ci.yml`
- Start with `allow_failure: true`, tighten to `false` once baseline clean
- Use `rules:` syntax (deprecated `only/except`)

### Container Registry Security
- Tag immutably with `$COMMIT_SHA`, convenience tag with `latest` + semver on releases
- Never embed secrets in Docker build → use `--secret` flag or build args
- Use `docker/metadata-action` for consistent tagging across images

## Post-Deployment Verification

- **Readiness**: `kubectl rollout status deployment/my-app --timeout=5m`
- **Health checks**: Hit `/health` endpoint 10x with 10s backoff
- **Error rate**: Query Prometheus, rollback if error_rate > 1%
- **Metrics window**: Wait 60s post-deploy before sampling metrics (startup noise)

## Automated Rollback

```yaml
deploy:
  steps:
    - run: kubectl apply -f k8s/
    - run: kubectl rollout status deployment/my-app --timeout=5m
    - run: curl -f https://app.example.com/health

    - if: failure()
      run: kubectl rollout undo deployment/my-app
```

## DORA Metrics

| Metric | Target | How to Track |
|--------|--------|-------------|
| **Deployment Frequency** | ≥daily | Count deployments/day |
| **Lead Time** | <1h (elite) | Merge commit → production |
| **Change Failure Rate** | <15% | Failed deployments / total |
| **MTTR** | <1h | Rollback completion time |

**Dashboard**: Export from CI/CD platform (GitHub Actions: jobs API, GitLab: CI metrics API).

## Gotchas

- **GitHub**: `GITHUB_TOKEN` has limited permissions → explicitly set `permissions:` block
- **GitHub**: `actions/checkout@v4` fetches 1 commit by default → add `fetch-depth: 0` for full history (changelogs, version bumps)
- **GitLab**: DinD (`docker:24-dind` service) requires `DOCKER_TLS_CERTDIR: "/certs"` (TLS errors otherwise)
- **Both**: Never store secrets in YAML → use platform secret management
- **Both**: Pin all third-party actions/images to specific versions (not `latest` or `master`)
- **Both**: Coverage reports need explicit format → `cobertura` for GitLab MR display, `lcov` for Codecov
- **Both**: Unbounded artifacts/cache destroy pipeline speed → set expiration policies
- **Kubernetes**: Prefer GitOps (ArgoCD/Flux) over direct kubectl from CI for production

## Cross-References

- **devops:github-actions-patterns** -- deep GitHub Actions patterns: reusable workflows, OIDC, matrix strategies
- **devops:docker-patterns** -- container build optimization, multi-stage builds for CI
- **devops:gitops-workflow** -- ArgoCD/Flux deployment patterns, GitOps pipeline integration
