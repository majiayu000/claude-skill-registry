---
name: review:infra
description: Infrastructure-focused review covering IaC, CI/CD, releases, migrations, logging, and observability. Spawns the senior-review-specialist agent for infrastructure analysis.
---

# Infrastructure Code Review

Run an infrastructure-focused review using 6 infrastructure checklists via the senior-review-specialist agent.

## Instructions

Spawn the `senior-review-specialist` agent to perform this review.

## Checklists to Apply

Load and apply these review checklists:

- `commands/review/infra.md` - Deployment config, least privilege, operational clarity
- `commands/review/ci.md` - Pipeline security, deployment safety
- `commands/review/release.md` - Versioning, rollout, migration, rollback
- `commands/review/migrations.md` - Database migration safety
- `commands/review/logging.md` - Secrets exposure, PII leaks, wide-events
- `commands/review/observability.md` - Logs, metrics, tracing, alertability

## Agent Instructions

The agent should:

1. **Get working tree changes**: Run `git diff` to see all changes
2. **Identify infrastructure files**:
   - Terraform, CloudFormation, Kubernetes manifests
   - CI/CD pipelines (GitHub Actions, GitLab CI, etc.)
   - Migration files, deployment scripts
   - Logging and monitoring configuration
3. **For each changed file**:
   - Read the full file content
   - Go through each diff hunk
   - Apply all 6 infrastructure checklists
   - Look for security misconfigurations and operational risks
4. **Cross-reference related files**: Check environment configs, secrets handling
5. **Assess blast radius**: What could go wrong in production?

## Output Format

Generate an infrastructure review report with:

- **Critical Issues (BLOCKER)**: Security misconfigurations, deployment risks
- **High Priority Issues**: Missing guardrails, cost explosions
- **Medium Priority Issues**: Observability gaps, operational hazards
- **Infrastructure Map**: Components, dependencies, deployment topology
- **Operational Readiness**: Logging, alerting, rollback capabilities
- **File Summary**: Infrastructure issues per file
- **Overall Assessment**: Production readiness recommendation
