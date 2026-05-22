---
name: sentry-monitoring
description: Sentry error tracking and performance monitoring for real-time visibility into application errors, performance issues, and release health
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read, WebFetch]
best_practices:
  - Never expose auth tokens in output
  - Require confirmation for destructive operations
  - Use environment variables for credentials
error_handling: graceful
streaming: supported
---

# Sentry Monitoring Skill

## Overview

Provides 90%+ context savings vs raw Sentry API calls. Progressive disclosure by feature category: error tracking, performance monitoring, release management, and project configuration.

## Requirements

- Sentry account with project configured
- `SENTRY_AUTH_TOKEN` environment variable (optional, for authenticated API calls)
- `SENTRY_ORG` environment variable (optional, defaults to first organization)
- `SENTRY_PROJECT` environment variable (optional, defaults to first project)

## Tools (Progressive Disclosure)

### Error Tracking

| Tool          | Description               | Confirmation |
| ------------- | ------------------------- | ------------ |
| list-issues   | List recent issues/errors | No           |
| issue-details | Get detailed issue info   | No           |
| resolve-issue | Mark issue as resolved    | Yes          |
| ignore-issue  | Ignore/snooze issue       | Yes          |

### Performance Monitoring

| Tool                | Description                       | Confirmation |
| ------------------- | --------------------------------- | ------------ |
| list-transactions   | List performance transactions     | No           |
| transaction-summary | Get transaction performance stats | No           |
| slow-queries        | Identify slow database queries    | No           |

### Release Management

| Tool           | Description                    | Confirmation |
| -------------- | ------------------------------ | ------------ |
| list-releases  | List releases                  | No           |
| create-release | Create new release             | Yes          |
| set-commits    | Associate commits with release | Yes          |

### Project Configuration

| Tool             | Description           | Confirmation |
| ---------------- | --------------------- | ------------ |
| list-projects    | List Sentry projects  | No           |
| project-settings | View project settings | No           |
| list-alerts      | List alert rules      | No           |

## Quick Reference

```bash
# List recent issues
curl -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  "https://sentry.io/api/0/projects/$SENTRY_ORG/$SENTRY_PROJECT/issues/?query=is:unresolved"

# Get issue details
curl -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  "https://sentry.io/api/0/issues/{issue_id}/"

# Resolve issue
curl -X PUT -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  "https://sentry.io/api/0/issues/{issue_id}/" \
  -d '{"status": "resolved"}'

# List transactions
curl -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  "https://sentry.io/api/0/organizations/$SENTRY_ORG/events/?field=transaction"

# Create release
curl -X POST -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  "https://sentry.io/api/0/organizations/$SENTRY_ORG/releases/" \
  -d '{"version": "1.0.0", "projects": ["project-slug"]}'

# List projects
curl -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  "https://sentry.io/api/0/organizations/$SENTRY_ORG/projects/"
```

## Configuration

### Environment Variables

| Variable            | Required | Description                                  |
| ------------------- | -------- | -------------------------------------------- |
| `SENTRY_AUTH_TOKEN` | Optional | Sentry authentication token for API calls    |
| `SENTRY_ORG`        | Optional | Organization slug (defaults to first org)    |
| `SENTRY_PROJECT`    | Optional | Project slug (defaults to first project)     |
| `SENTRY_DSN`        | No       | For SDK integration (not used by this skill) |

### Getting Auth Token

1. Navigate to Sentry Settings → Account → API → Auth Tokens
2. Create new token with scopes: `project:read`, `project:write`, `event:read`
3. Set as environment variable: `export SENTRY_AUTH_TOKEN=your_token_here`

## Security

⚠️ **Never expose auth tokens in output**
⚠️ **Destructive operations (resolve-issue, ignore-issue, create-release, set-commits) require confirmation**
⚠️ **Use environment variables for credentials, never hardcode**

## Agent Integration

- **devops** (primary): Production monitoring, incident response
- **incident-responder** (primary): Error triage, issue resolution
- **developer** (secondary): Debugging, performance optimization
- **qa** (secondary): Test environment monitoring

## Error Handling

If tool execution fails:

1. Verify `SENTRY_AUTH_TOKEN` is set: `echo $SENTRY_AUTH_TOKEN`
2. Check token permissions include required scopes
3. Verify organization and project slugs are correct
4. Review Sentry API rate limits (default: 3000 requests/minute)

## Common Workflows

### Incident Response

1. `list-issues` - Get recent unresolved errors
2. `issue-details` - Investigate specific issue
3. `resolve-issue` - Mark as resolved after fix deployed

### Performance Optimization

1. `list-transactions` - Identify slow endpoints
2. `transaction-summary` - Analyze performance patterns
3. `slow-queries` - Find database bottlenecks

### Release Management

1. `create-release` - Create new release version
2. `set-commits` - Associate commits with release
3. `list-releases` - Track release health

## Troubleshooting

| Issue               | Solution                                                                   |
| ------------------- | -------------------------------------------------------------------------- |
| 401 Unauthorized    | Check `SENTRY_AUTH_TOKEN` is valid and not expired                         |
| 403 Forbidden       | Verify token has required scopes (project:read, project:write, event:read) |
| 404 Not Found       | Verify `SENTRY_ORG` and `SENTRY_PROJECT` are correct slugs                 |
| Rate limit exceeded | Wait 1 minute, reduce request frequency                                    |

## Related

- Sentry API Documentation: https://docs.sentry.io/api/
- Sentry Error Tracking: https://docs.sentry.io/product/issues/
- Sentry Performance: https://docs.sentry.io/product/performance/
- Sentry Releases: https://docs.sentry.io/product/releases/

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
