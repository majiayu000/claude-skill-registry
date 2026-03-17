---
name: troubleshoot
description: Investigate runtime or production issues from logs, errors, or unexpected behavior (Marcus + Alex workflow)
disable-model-invocation: true
---

Troubleshoot: $ARGUMENTS

Unlike `/fix-issue` (code-level bugs), `/troubleshoot` investigates runtime/production problems from symptoms.

## Step 1 — Gather Symptoms
Identify what's happening:
- What errors are users seeing? (status codes, error messages)
- When did it start? (after a deploy, config change, or spontaneously?)
- Is it affecting all requests or specific endpoints?
- Is the health endpoint responding? What status?

## Step 2 — Check Infrastructure
```bash
# Is the process running? Hit the health endpoint (see project config for URL)
# Check external resource connectivity via device/info endpoint
# Check recent logs — look for ERROR and WARNING entries
```

### Common infrastructure issues:
See the Troubleshooting table in the project config for common symptoms, likely causes, and checks.

## Step 3 — Check Configuration
Read the config file and verify env vars are set correctly.
See the Environment Variables table in the project config for all settings and their defaults.
Common misconfigurations:
- Mock mode accidentally enabled in production
- Resource identifiers don't match actual hardware
- API key not set when it should be
- Rate limit too restrictive

## Step 4 — Check Application Logs
Look for patterns in log output:
- Audit logger entries — are state changes being logged?
- `WARNING` level — resource disconnection, degraded mode
- `ERROR` level — communication failures, unhandled exceptions
- Startup messages — did all components initialize?

## Step 5 — Reproduce Locally
```bash
# Start in mock/dev mode to isolate hardware vs software issues (see dev run command in project config)
# Hit the failing endpoint
```
- If it works in mock mode → hardware/external resource issue
- If it fails in mock mode → software bug → switch to `/fix-issue`

## Step 6 — Resolution
- If config issue → fix env vars, restart
- If hardware/resource issue → check connection, permissions, drivers
- If software bug → use `/fix-issue` to fix the code
- If performance issue → use `/optimize` to profile and fix

## Step 7 — Document
Log the incident:
- What happened, when, how long it lasted
- Root cause identified
- Fix applied
- Prevention steps (monitoring, alerting, tests)