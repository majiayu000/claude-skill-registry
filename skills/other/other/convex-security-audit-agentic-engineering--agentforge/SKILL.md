---
name: convex-security-audit
description: Deep Convex security review patterns for authorization, data boundaries, sensitive operations, and defense in depth.
version: 1.0.0
metadata:
  author: agentforge
  source: waynesutton/convexskills and upstream Convex rules
---

# Convex Security Audit

Use this for a deeper security review than `convex-security-check`.

## Focus areas

- role and permission boundaries,
- resource-level authorization,
- sensitive mutations and actions,
- abuse prevention and rate limiting,
- auditability of destructive or privileged operations.

## Repo fit

- Pay extra attention to API key storage, vault-like flows, channels, and any path that bridges daemon and Convex state.
