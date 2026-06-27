---
name: security-threat-model
description: Threat-model product features, APIs, data flows, secrets, permissions, supply-chain changes, auth boundaries, and risky code paths before or during implementation. Use when touching authentication, authorization, payments, secrets, user data, uploads, webhooks, admin tools, innerHTML/eval/exec, dependency upgrades, or cross-tenant access.
---

# Security Threat Model

## Purpose

Use this skill before implementing or approving security-sensitive changes. It complements `auth-security` and `server-security` by mapping assets, attackers, trust boundaries, and concrete controls.

## Scope First

Identify:

1. Assets: credentials, tokens, user data, tenant data, money movement, admin actions.
2. Actors: anonymous user, authenticated user, tenant admin, internal operator, compromised dependency.
3. Trust boundaries: browser/server, service/service, tenant/tenant, CI/runtime, third-party callbacks.
4. Entry points: API routes, CLI commands, jobs, webhooks, uploads, config files.
5. Existing controls: validation, authz, rate limits, audit logs, secret storage.

## Threat Checklist

Check at least:

- Spoofing: can an identity, tenant, callback, or service be forged?
- Tampering: can payloads, configs, migrations, artifacts, or logs be altered?
- Repudiation: is there an audit trail for sensitive actions?
- Information disclosure: can secrets, PII, logs, or tenant data leak?
- Denial of service: can expensive paths be amplified?
- Elevation of privilege: can user or service permissions expand?
- Supply chain: can dependencies, scripts, CI, or generated files introduce risk?

## Required Controls

Every finding needs one of:

- preventive control in production code,
- detective control with alerting,
- compensating manual control with owner and expiry,
- explicit accepted risk with rationale.

Do not accept "warn and continue" for authz, secrets, tenant isolation, injection, or payment/security-critical failures.

## Output Shape

```text
scope:
assets:
trust_boundaries:
entry_points:
threats:
required_controls:
tests_or_probes:
residual_risks:
review_gate:
```

For implementation work, include exact files and verification commands that prove the controls are active.
