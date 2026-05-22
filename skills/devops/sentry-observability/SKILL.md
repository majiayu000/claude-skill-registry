---
name: sentry-observability
description: |
  Sentry error tracking and production observability. Invoke when:
  - New Next.js project without error tracking → Suggest setup
  - Deploying to Vercel → "Add observability before deploying"
  - Discussing error handling, try/catch → "Track these in production"
  - Production bug, users reporting errors → Triage with scripts
  - Setting up monitoring, configuring alerts, reviewing PII handling
  Scripts: detect_sentry.sh, init_sentry.sh, list_issues.sh, triage_score.sh
  Keywords: Sentry, production errors, error tracking, triage, alerts,
  observability, Session Replay, PII redaction, source maps, monitoring
---

# Sentry Observability

Production error tracking with two modes: **Setup** (add Sentry) and **Operations** (use Sentry).

## Quick Detection

```bash
# Check if Sentry is configured in current project
~/.claude/skills/sentry-observability/scripts/detect_sentry.sh
```

## Setup Mode

For projects **without** Sentry. Proactively suggest when:
- New Next.js project detected (no @sentry/* in package.json)
- User mentions deploying to production
- Discussing error handling patterns

```bash
# Initialize Sentry in current project
~/.claude/skills/sentry-observability/scripts/init_sentry.sh

# Verify setup after installation
~/.claude/skills/sentry-observability/scripts/verify_setup.sh
```

## Operations Mode

For projects **with** Sentry. Use for triage and monitoring.

```bash
# List unresolved issues (powers /triage)
~/.claude/skills/sentry-observability/scripts/list_issues.sh --env production

# Get priority-scored issues (triage algorithm)
~/.claude/skills/sentry-observability/scripts/triage_score.sh --json

# Get full context for an issue
~/.claude/skills/sentry-observability/scripts/issue_detail.sh PROJ-123

# Create alert rule
~/.claude/skills/sentry-observability/scripts/create_alert.sh --name "New Errors" --type issue

# Mark issue resolved
~/.claude/skills/sentry-observability/scripts/resolve_issue.sh PROJ-123
```

## Core Principles

1. **Vercel Integration First** - Use marketplace, not manual tokens
2. **Clean Environments** - "production" not "vercel-production"
3. **Security by Default** - PII redaction, hide source maps
4. **CLI Automation** - Version-controlled alerts
5. **Cost Awareness** - Free tier = 5k errors/month

## Environment Variables

```bash
# Required (in ~/.secrets or project .env.local)
SENTRY_AUTH_TOKEN / SENTRY_MASTER_TOKEN  # API access
SENTRY_ORG                                # Organization slug
SENTRY_DSN                                # Project DSN

# Auto-detected per project
SENTRY_PROJECT  # From .sentryclirc or .env.local
```

## Decision Trees

### Should I Set Up Sentry?
```
Is this a production application?
├─ YES → Is Sentry already configured?
│   ├─ NO → Run init_sentry.sh
│   └─ YES → Run verify_setup.sh to check health
└─ NO → Skip (development/prototype only)
```

### Triage Priority (from /triage)
```
Score = Events(1x) + Users(5x) + Severity(3x) + Recency(2x) + Env(4x)
Higher score = Higher priority
```

## References

- [Setup Guide](references/setup-guide.md) - Full setup walkthrough
- [Configuration](references/configuration.md) - Advanced config patterns
- [PII Redaction](references/pii-redaction.md) - Security patterns
- [Session Replay](references/session-replay.md) - Visual debugging
- [Troubleshooting](references/troubleshooting.md) - Common issues
- [Anti-Patterns](references/anti-patterns.md) - What NOT to do

## Philosophy

**Observability Is Not Optional**: Production errors without monitoring = invisible failures.

**Proactive Setup**: Suggest Sentry when starting new projects. Don't wait for the first production incident.

**Security First**: PII redaction is non-negotiable. Privacy violations >> lost debugging info.

**Cost Awareness**: Free tier (5k errors/month) is enough for most projects.
