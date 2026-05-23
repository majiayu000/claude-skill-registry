---
name: flow-nexus-platform
title: Flow Nexus Platform Management
version: 2.0.0
category: platform
description: Comprehensive Flow Nexus platform management - authentication, sandboxes, app deployment, payments, and challenges
author: Flow Nexus
tags:
  - authentication
  - sandboxes
  - deployment
  - payments
  - gamification
  - cloud
difficulty: intermediate
prerequisites:
  - Flow Nexus MCP server configured
  - Valid Flow Nexus account
tools_required:
  - mcp__flow-nexus__*
related_skills:
  - flow-nexus-swarm
  - flow-nexus-neural
  - flow-nexus-workflow
---

# Flow Nexus Platform Management

## Behavioral Classification

**Type**: Autonomous Execution

This skill provides commands that execute immediately when invoked. No interactive decisions required.

**Command Categories**:
- Authentication: Login, register, profile management
- Sandboxes: Create, execute, manage isolated environments
- App Store: Browse, publish, deploy applications
- Payments: Credits, billing, subscriptions
- Challenges: Coding challenges, achievements, leaderboards
- Storage: File storage, real-time subscriptions

---

## Overview

Comprehensive platform management for Flow Nexus - covering authentication, sandbox execution, app deployment, credit management, and coding challenges. This skill consolidates 6 Flow Nexus command modules into a single interface.

---

## Quick Start

### Step 1: Authenticate

```javascript
// Register new account
mcp__flow-nexus__user_register({
  email: "dev@example.com",
  password: "SecurePass123!",
  full_name: "Developer Name"
})

// Or login to existing account
mcp__flow-nexus__user_login({
  email: "dev@example.com",
  password: "SecurePass123!"
})
```

### Step 2: Create a Sandbox

```javascript
mcp__flow-nexus__sandbox_create({
  template: "node",
  name: "dev-environment",
  install_packages: ["express", "dotenv"],
  env_vars: { NODE_ENV: "development" }
})
```

### Step 3: Execute Code

```javascript
mcp__flow-nexus__sandbox_execute({
  sandbox_id: "your_sandbox_id",
  code: 'console.log("Hello Flow Nexus!")',
  language: "javascript"
})
```

### Step 4: Deploy an App

```javascript
mcp__flow-nexus__template_deploy({
  template_name: "express-api-starter",
  deployment_name: "my-api",
  variables: { database_url: "postgres://..." }
})
```

---

## Sub-Documentation

For detailed information, see the following files:

| Document | Contents |
|----------|----------|
| [Authentication](./auth.md) | Registration, login, password management, profile |
| [Sandbox Management](./sandbox.md) | Create sandboxes, execute code, templates, patterns |
| [App Store](./app-store.md) | Browse, publish, deploy applications |
| [Payments](./payments.md) | Credits, billing, subscriptions, cost optimization |
| [Challenges](./challenges.md) | Coding challenges, leaderboards, achievements |
| [Storage](./storage.md) | File storage, real-time subscriptions, system utilities |

---

## Quick Reference

### Core Commands

| Command | Description |
|---------|-------------|
| `user_login` | Authenticate with email/password |
| `auth_status` | Check authentication status |
| `sandbox_create` | Create new sandbox environment |
| `sandbox_execute` | Run code in sandbox |
| `app_search` | Search app store |
| `template_deploy` | Deploy app template |
| `check_balance` | View credit balance |
| `challenges_list` | Browse coding challenges |

### Sandbox Templates

| Template | Description |
|----------|-------------|
| `node` | Node.js with npm |
| `python` | Python 3.x with pip |
| `react` | React development setup |
| `nextjs` | Next.js full-stack |
| `vanilla` | Basic HTML/CSS/JS |
| `base` | Minimal Linux environment |
| `claude-code` | Claude Code integrated |

### Subscription Tiers

| Tier | Credits/Month | Concurrent Sandboxes | Price |
|------|---------------|---------------------|-------|
| Free | 100 | 2 | $0 |
| Pro | 1,000 | 10 | $29/mo |
| Enterprise | Unlimited | Unlimited | Custom |

---

## Best Practices

### Security
- Never hardcode API keys - use environment variables
- Use private buckets for sensitive data
- Review audit logs periodically

### Performance
- Clean up unused sandboxes to save credits
- Use smaller sandbox templates when possible
- Batch operations to reduce API calls

### Cost Management
- Complete daily challenges for bonus credits
- Publish templates to earn passive credits
- Monitor usage via `user_stats`

---

## Troubleshooting

### Authentication Issues
- **Login Failed**: Check email/password, verify email first
- **Token Expired**: Re-login to get fresh tokens
- **Permission Denied**: Check tier limits

### Sandbox Issues
- **Sandbox Won't Start**: Check template compatibility, verify credits
- **Execution Timeout**: Increase timeout or optimize code
- **Package Install Failed**: Check package name availability

### Payment Issues
- **Credits Not Applied**: Allow 5-10 minutes for processing
- **Auto-refill Not Working**: Verify payment method on file

---

## Support & Resources

- **Documentation**: https://docs.flow-nexus.ruv.io
- **API Reference**: https://api.flow-nexus.ruv.io/docs
- **Status Page**: https://status.flow-nexus.ruv.io
- **Community Forum**: https://community.flow-nexus.ruv.io
- **GitHub Issues**: https://github.com/ruvnet/flow-nexus/issues

---

## Related Skills

- `flow-nexus-swarm` - AI swarm orchestration
- `flow-nexus-neural` - Neural network training
- `flow-nexus-workflow` - Workflow automation

---

**Version**: 2.0.0
**Last Updated**: 2025-01-24
