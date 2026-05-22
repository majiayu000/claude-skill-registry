---
name: full-deploy
description: Complete deployment pipeline - test, security audit, deploy, and notify. Use for production deployments.
allowed-tools: Bash(npm:*), Bash(npx:*), Bash(wrangler:*), Read, Glob, Grep, Task, Write
model: sonnet
---

# Full Deployment Pipeline

This compound skill orchestrates a complete deployment with validation.

## Pipeline Steps

### 1. Run Tests
First, ensure all tests pass:

```bash
cd /Users/admin/cursor/agentic-commerce
npm test
```

If tests fail, STOP and report the failures. Do not proceed with deployment.

### 2. Security Audit
Use the security-auditor agent to check for vulnerabilities:

- Check for hardcoded secrets
- Validate input sanitization
- Review authentication flows
- Check OWASP Top 10 compliance

Focus on files changed since the last deployment.

### 3. Build Workers
Build both workers:

```bash
cd workers/main && npm run build:worker
cd ../search-consumer && npm run build:consumer
```

### 4. Deploy to Cloudflare
Deploy in sequence (main first, then search-consumer):

```bash
cd workers/main && npx wrangler deploy
cd ../search-consumer && npx wrangler deploy
```

### 5. Verify Deployment
Tail logs briefly to confirm healthy startup:

```bash
timeout 10 npx wrangler tail workers/main
```

### 6. Report Summary
Provide a deployment summary including:
- Test results (pass/fail counts)
- Security findings (if any)
- Deployment status for each worker
- Any warnings or recommendations

## Rollback Procedure
If deployment verification fails:

```bash
cd workers/main && npx wrangler rollback
cd ../search-consumer && npx wrangler rollback
```
