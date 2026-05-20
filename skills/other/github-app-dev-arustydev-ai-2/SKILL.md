---
name: github-app-dev
description: GitHub App development guide for building custom integrations. Use this skill when creating a GitHub App, building webhook handlers, implementing GitHub API integrations, developing PR/Issue automation apps, or deploying GitHub Apps to Cloudflare Workers.
---

# GitHub App Development

Build custom GitHub Apps for automation, integrations, and workflow management using best practices for scalable, maintainable applications.

## Getting Started

GitHub Apps are first-class integrations that act on their own behalf, providing granular permissions and webhook subscriptions for specific repositories.

**Quick wins:**
- [Create your first app in 15 minutes](examples/README.md#quick-start)
- [Deploy to Cloudflare Workers](examples/cloudflare-workers-minimal.ts)
- [Use Probot for rapid development](examples/probot-simple.ts)

**This skill covers:**
- App registration and authentication
- Webhook handling and API integration
- Best practices and anti-patterns
- Deployment strategies
- Security and error handling

**This skill does NOT cover:**
- GitHub Actions development (see `github-actions` skill)
- OAuth apps for user authentication
- App marketplace strategy

## Quick Reference

### App Types

| Type | Acts As | Use Case |
|------|---------|----------|
| GitHub App | Itself or user | Automation, integrations, bots |
| OAuth App | User only | "Sign in with GitHub", user-facing tools |

### Authentication

GitHub Apps use a three-tier authentication model:

1. **JWT tokens** - Authenticate the app itself (signed with your private key)
2. **Installation tokens** - Scoped access to specific repositories (exchanged from JWT)
3. **User tokens** - Optional user-delegated permissions (OAuth flow)

Most apps only need installation tokens. See [examples/auth-patterns.ts](examples/auth-patterns.ts) for implementation details.

### Authentication Best Practices

**Essential security patterns:**
- Generate fresh JWT tokens (expire in 10 minutes)
- Cache and refresh installation tokens (expire in 1 hour)
- Scope operations to specific installations
- Handle 401/403 errors gracefully

See [references/authentication.md](references/authentication.md) for advanced patterns and [examples/auth-patterns.ts](examples/auth-patterns.ts) for implementation examples.

### Permission Categories

| Category | Examples | When to Use |
|----------|----------|-------------|
| Repository | contents, pull_requests, issues | Most apps |
| Organization | members, teams | Org-level automation |

See [references/permissions.md](references/permissions.md) for complete permission matrix.

## Example Use Cases & Configurations

### Common App Types with Ready-to-Use Configs

**🚀 PR Automation Bot**
*Auto-label PRs, assign reviewers, enforce quality gates*
- **Config**: [app-configuration.yaml#pr-automation-bot](examples/app-configuration.yaml#L9)
- **Implementation**: [patterns/auto-labeling.ts](examples/patterns/auto-labeling.ts) + [patterns/reviewer-assignment.ts](examples/patterns/reviewer-assignment.ts)
- **Permissions needed**: `contents:read`, `pull_requests:write`, `issues:write`

**🔒 Security Scanner**
*Scan for secrets, vulnerabilities, license compliance*
- **Config**: [app-configuration.yaml#security-scanner-bot](examples/app-configuration.yaml#L66)
- **Implementation**: [webhook-security.ts](examples/webhook-security.ts)
- **Permissions needed**: `contents:read`, `security_events:write`, `vulnerability_alerts:read`

**📋 Issue Triage Assistant**
*Route issues to teams, auto-label by content*
- **Config**: [app-configuration.yaml#issue-triage-bot](examples/app-configuration.yaml#L86)
- **Implementation**: [production-app.ts](examples/production-app.ts)
- **Permissions needed**: `issues:write`, `metadata:read`

**🚢 Release Manager**
*Generate changelogs, manage releases, close issues*
- **Config**: [app-configuration.yaml#release-bot](examples/app-configuration.yaml#L105)
- **Implementation**: [production-app.ts](examples/production-app.ts)
- **Permissions needed**: `contents:write`, `issues:write`, `pull_requests:read`

### Framework-Specific Examples

**⚡ Cloudflare Workers (Edge-First)**
*Best for: Low latency, global deployment, simple logic*
```typescript
// Minimal viable app in <100 lines
export default { async fetch(request, env) { ... } }
```
- **Example**: [cloudflare-workers-minimal.ts](examples/cloudflare-workers-minimal.ts)
- **Deploy guide**: [deployment/cloudflare-workers.md](examples/deployment/cloudflare-workers.md)

**🤖 Probot Framework (Rapid Development)**
*Best for: Prototyping, complex logic, multiple integrations*
```typescript
export = (app) => {
  app.on('pull_request.opened', async (context) => { ... })
}
```
- **Example**: [probot-simple.ts](examples/probot-simple.ts)
- **Setup guide**: [setup-guide.md](examples/setup-guide.md)

**☁️ Serverless Functions (Auto-scaling)**
*Best for: Variable load, complex processing, existing infrastructure*
- **AWS Lambda**: [deployment/aws-lambda.md](examples/deployment/aws-lambda.md)
- **Vercel**: [deployment/vercel.md](examples/deployment/vercel.md)

### Configuration Examples

✅ **Best practice examples:**
- **Minimal permissions**: [app-configuration.yaml#permission-patterns](examples/app-configuration.yaml#L229)
- **Complete event coverage**: [app-configuration.yaml#event-patterns](examples/app-configuration.yaml#L260)
- **Security checklist**: [best-practices.md](examples/best-practices.md)

## Best Practices & Anti-patterns

### Essential Best Practices

**🔒 Security First**
- **Verify all webhook signatures** - Never process unverified webhooks
- **Request minimal permissions** - Use principle of least privilege
- **Secure secret management** - Use dedicated secret managers, not env vars
- **Validate all inputs** - Sanitize webhook payloads and user data

**⚡ Performance & Reliability**
- **Acknowledge webhooks quickly** - Respond within 30 seconds, process async
- **Implement circuit breakers** - Graceful degradation when GitHub API is slow
- **Cache installation tokens** - Refresh before expiry, batch API calls
- **Monitor rate limits proactively** - Check remaining quota before operations

**🏗️ Architecture & Maintainability**
- **Separate concerns** - Dedicated modules for auth, webhooks, services
- **Make operations idempotent** - Handle duplicate webhook deliveries gracefully
- **Use structured logging** - Include context (repo, PR number, installation)
- **Test with realistic payloads** - Use actual GitHub webhook examples

See [examples/best-practices.md](examples/best-practices.md) for comprehensive implementation examples and security checklists.

### Common Anti-patterns to Avoid

**❌ Security Anti-patterns**
- **Skipping signature verification** - "Just for development" becomes production
  ```typescript
  // DON'T: Skip verification
  app.post('/webhook', (req, res) => {
    // Process without verifying req.headers['x-hub-signature-256']
  })
  ```
- **Over-privileged permissions** - Requesting `admin` when `read` suffices
  ```yaml
  # DON'T: Request excessive permissions
  permissions:
    administration: write  # Dangerous! Almost never needed
    contents: write        # Do you really need to modify files?
  ```
- **Logging sensitive data** - Tokens in error messages or debug logs
- **Hardcoded secrets** - Credentials in source code or config files

**❌ Performance Anti-patterns**
- **Synchronous webhook processing** - Blocking responses while making API calls
- **Unbounded API requests** - Making 100+ calls without rate limit checks
- **Memory leaks in long-running apps** - Not cleaning up event listeners
- **Missing error boundaries** - One failed operation breaks entire workflow

**❌ Integration Anti-patterns**
- **Polling instead of webhooks** - Inefficient API usage patterns
- **Not handling app uninstalls** - Continuing to process events after removal
- **Ignoring GitHub API deprecations** - Using outdated endpoints or parameters
- **Assuming webhook order** - Events may arrive out of sequence
- **Under-configured webhooks** - Missing critical events for your use case
  ```yaml
  # DON'T: Miss critical events for PR bot
  events: [issues]  # Forgot pull_request events!
  ```

### Framework Selection Guidelines

| Scale | Complexity | Recommended Approach | When to Use |
|-------|------------|---------------------|-------------|
| **Small** (< 100 repos) | Simple automation | **Probot** | Learning, prototyping, simple bots |
| **Medium** (100-1000 repos) | Custom logic | **Hono + Octokit** | Production apps, edge deployment |
| **Large** (1000+ repos) | Enterprise features | **Custom framework** | Event streaming, multi-tenant |

See [references/implementation-patterns.md](references/implementation-patterns.md) for detailed architecture guidance and [references/anti-patterns.md](references/anti-patterns.md) for comprehensive anti-pattern examples and recovery strategies.

## Error Handling & Rate Limiting

### Quick Error Response Guide

**Key error handling patterns:**
- **403 (Rate Limited)**: Wait for reset time, implement backoff
- **5xx (Server Errors)**: Retry with exponential backoff
- **401/403**: Check credentials/permissions, refresh tokens
- **400/404**: Validate request parameters, verify resource exists

### Rate Limit Essentials

**Key principles:**
- Monitor usage before hitting limits
- Implement graceful degradation strategies
- Use exponential backoff for retries

See [examples/webhook-security.ts](examples/webhook-security.ts) for rate limit monitoring implementation and [references/error-handling.md](references/error-handling.md) for comprehensive patterns.

## Observability & Monitoring

### Essential Monitoring Targets

**Application health:** Response times, error rates, resource usage
**GitHub API integration:** Rate limits, authentication failures, API errors
**Business metrics:** Installations, active repositories, feature usage

### Quick OpenTelemetry Setup

Key trace targets for GitHub Apps:
- `webhook.{event_type}` - Processing time and errors
- `github.api.{operation}` - API performance and rate limits
- `auth.installation_token` - Authentication overhead

See [references/observability.md](references/observability.md) for complete OpenTelemetry setup, alerting strategies, health checks, and dashboard configurations.

## Architecture & Patterns

### Framework Decision Matrix

| Scale | Framework | Architecture |
|-------|-----------|-------------|
| **Small (< 100 repos)** | Probot | Single instance, simple |
| **Medium (100-1000 repos)** | Probot or Hono | Load balanced, cached |
| **Large (1000+ repos)** | Custom Octokit | Event streaming, queues |

### Core Design Principles

**✅ Essential patterns:**
- Event-driven architecture with dedicated handlers
- Stateless operations (no in-memory state)
- Background processing for heavy operations
- Idempotent webhook handling

**❌ Avoid these anti-patterns:**
- Monolithic webhook handlers processing all events
- Synchronous processing of heavy operations
- Direct database access from webhook handlers

See [references/probot.md](references/probot.md) for framework comparisons and [references/hosting/](references/hosting/) for platform-specific patterns.

## Testing & Quality

### Test Strategy Overview

Follow the **70/20/10 test pyramid:**
- **70% Unit Tests** - Business logic and utilities
- **20% Integration Tests** - Webhook processing with mocked API
- **10% End-to-End Tests** - Full flow with test repositories

### Critical Test Scenarios

**Authentication:** Token expiration, app uninstalls, permission changes
**Webhooks:** Duplicate delivery, signature verification, malformed payloads
**Rate limits:** Graceful degradation, retry logic, secondary limits

See [references/testing.md](references/testing.md) for complete testing frameworks, patterns, and automation strategies.

## Production Deployment

### Pre-deploy Checklist

**Security essentials:**
- Webhook signature verification enabled
- Private key in secure vault (not env vars)
- Minimum required permissions only

**Reliability essentials:**
- Health checks responding
- Error monitoring configured
- Response times < 10s (GitHub timeout)

### Configuration

**Required environment variables:**
- `GITHUB_APP_ID` - Your app's unique identifier
- `GITHUB_PRIVATE_KEY` - App authentication key
- `GITHUB_WEBHOOK_SECRET` - Webhook signature verification

See [references/hosting/](references/hosting/) for platform-specific deployment guides and [examples/deployment/](examples/deployment/) for complete configuration examples.

## Performance & Optimization

### Critical Performance Targets

**Response times:** Acknowledge webhooks within 30 seconds
**Async processing:** Queue non-critical operations
**Resource management:** Stream large payloads, monitor memory

### Common Bottlenecks

**Avoid these performance killers:**
- Synchronous GitHub API calls in webhook handlers
- Database queries blocking webhook responses
- Loading large payloads into memory
- CPU-intensive tasks blocking the main thread

See [references/observability.md](references/observability.md) for detailed performance monitoring and optimization strategies.


## Implementation Guides

### Quick Setup (15 minutes)

1. **Register app** - GitHub Settings → Developer settings → GitHub Apps
2. **Choose framework** - Probot for rapid development, raw Octokit for Workers
3. **Deploy** - Start with examples, customize for your needs

See [examples/README.md](examples/README.md) for step-by-step setup guides.

### Development Workflow

**Three-phase approach:**
1. **Setup** - Register app, configure permissions, download key
2. **Development** - Clone templates, implement handlers, test locally
3. **Deployment** - Configure secrets, deploy, install on repos

See [examples/setup-guide.md](examples/setup-guide.md) for detailed step-by-step instructions.

### Advanced Configuration Examples

**🏢 Enterprise Apps** - Multi-tenant, organization-scoped with SAML/SSO integration
**🔄 Multi-Repository Orchestration** - Coordinate changes across multiple repositories
**📊 Analytics & Reporting** - Read-only apps that collect metrics without making changes

See [references/advanced-configuration.md](references/advanced-configuration.md) for complete enterprise patterns, deployment scenarios by scale, and configuration examples.

### Integration Examples

Connect GitHub Apps with external systems using proven integration patterns:

**🔗 External API Integration** - Slack, Jira, CI/CD systems
**📝 Custom Workflow Automation** - Repository-specific business logic
**🔐 Security Integration** - Automated security scanning and policies

See [references/integration-patterns.md](references/integration-patterns.md) for implementation details, authentication patterns, and resilience strategies.

## Common Implementation Patterns

### Essential App Patterns

**Auto-labeling** - Label PRs based on conventional commit titles
**Reviewer assignment** - Route to team members based on file paths
**Quality gates** - Enforce checks based on repository settings
**Welcome automation** - Greet first-time contributors
**Configuration-based logic** - Use repository properties for behavior

See [references/implementation-patterns.md](references/implementation-patterns.md) for complete code examples, event processing patterns, and state management strategies.

### Hosting Platforms

Choose the right platform based on your scale and requirements. See [references/hosting/](references/hosting/) for detailed deployment guides and platform comparisons.

## API Reference

### Core Operations

**Essential API categories:**
- **Pull Requests** - Reviews, comments, status updates
- **Issues & Comments** - Create, label, assign, respond
- **Checks & Status** - CI integration, status reporting
- **Repository** - Files, branches, webhooks, settings

See [references/octokit.md](references/octokit.md) for complete API reference and [examples/production-app.ts](examples/production-app.ts) for real-world usage patterns.

### Webhook Events

**Most common events:**
- `pull_request.opened` - New PR created
- `issues.opened` - New issue created
- `issue_comment.created` - Comment added
- `check_run.completed` - CI check finished

See [references/webhooks.md](references/webhooks.md) for complete event reference.

## Security & Operations

### Security Checklist

✅ **Essential security measures:**
- Verify webhook signatures before processing
- Request minimum necessary permissions
- Store private key securely (use secrets manager)
- Validate all webhook payload input
- Use HTTPS for all communication

### Common Issues

**Authentication problems:**
- Check private key format (PEM) and app ID
- Verify token hasn't expired
- Confirm app is installed on target repository

**Webhook delivery issues:**
- Verify webhook URL is accessible
- Check webhook secret matches
- Confirm app subscribes to necessary events

See [references/error-handling.md](references/error-handling.md) for detailed troubleshooting guides.

## See Also

- [examples/README.md](examples/README.md) - Complete starter projects and runnable code samples
- [examples/best-practices.md](examples/best-practices.md) - Comprehensive implementation examples and security checklists
- [references/anti-patterns.md](references/anti-patterns.md) - Common mistakes and recovery strategies
- [references/testing.md](references/testing.md) - Comprehensive testing strategies and patterns
- [references/error-handling.md](references/error-handling.md) - Advanced error handling and rate limit management
- [references/observability.md](references/observability.md) - OpenTelemetry setup and monitoring best practices
- [references/webhooks.md](references/webhooks.md) - Complete webhook event reference
- [references/permissions.md](references/permissions.md) - Permission matrix and runtime validation
- [references/octokit.md](references/octokit.md) - Octokit SDK patterns
- `cloudflare-workers` skill - Detailed CF Workers patterns
- `github-actions` skill - Building custom Actions (different from Apps)

## External Resources

- [GitHub Apps Documentation](https://docs.github.com/en/apps)
- [Octokit.js](https://github.com/octokit/octokit.js)
- [Probot](https://probot.github.io/)
- [GitHub Webhooks](https://docs.github.com/en/webhooks)
