---
name: cyber-security
description: Vulnerability assessment, defensive programming, and attack prevention
category: Security
---

# Skill: cyber-security

## What I do

I provide a defensive mindset for building resilient systems. I focus on identifying potential attack vectors, implementing robust security controls, and ensuring that security is integrated throughout the development lifecycle rather than added as an afterthought.

## When to use me

- During architectural design to model potential threats
- When selecting or updating third-party dependencies
- Before exposing new endpoints or services to the internet
- When implementing authentication or authorisation logic
- During security-focused code reviews

## Core principles

1. **Defence in depth** — Never rely on a single security control. Implement multiple layers of protection.
2. **Least privilege** — Grant only the minimum access required for a component or user to perform its function.
3. **Assume breach** — Design systems under the assumption that an attacker may already have access to part of the network.
4. **Secure by design** — Security should be a fundamental requirement from the start, not a checklist item at the end.

## Patterns & examples

**Threat Modelling (STRIDE):**
- **Spoofing**: Can someone pretend to be another user?
- **Tampering**: Can data be modified in transit or at rest?
- **Repudiation**: Can a user deny performing an action?
- **Information Disclosure**: Can sensitive data be leaked?
- **Denial of Service**: Can the system be overwhelmed?
- **Elevation of Privilege**: Can a user gain unauthorised access levels?

**Defensive Programming Pattern:**
```typescript
// ✅ Correct: Validate all inputs, use secure defaults, and fail securely
async function processSensitiveData(userId: string, payload: unknown) {
  // 1. Validate userId format
  if (!isValidUUID(userId)) throw new SecurityError("Invalid ID");

  // 2. Authorise user action
  const hasAccess = await checkPermissions(userId, 'write');
  if (!hasAccess) throw new ForbiddenError("Unauthorised action");

  // 3. Sanitise and validate payload schema
  const cleanData = Schema.parse(payload);

  // 4. Process securely...
}
```

## Anti-patterns to avoid

- ❌ **Security through obscurity** — Relying on secret algorithms or hidden URLs is not a valid security strategy.
- ❌ **Hardcoding secrets** — API keys and credentials must never be committed to version control.
- ❌ **Trusting user input** — Every piece of data from a client must be treated as malicious until validated.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Security/Cyber Security.md`

## Related skills

- `security` — Core secure coding practices and implementation
- `check-compliance` — Automated security scanning and linting
- `static-analysis` — Identifying logic flaws and vulnerabilities
- `dependency-management` — Managing third-party risk
