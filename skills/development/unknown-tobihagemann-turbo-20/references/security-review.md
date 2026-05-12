# Security Review Reference

## Review Instructions

Check if `.turbo/threat-model.md` exists at the repository root. If it does, read sections 2 (Trust Boundaries and Assumptions) and 3 (Attack Surface, Mitigations and Attacker Stories) to understand assets at risk, identified attack surfaces with existing mitigations, and attacker stories. Use this context to prioritize findings. If no threat model exists, proceed without it.

### Review Mindset

Do not treat the existence of a check, sanitizer, or authorization guard as proof of safety. When a defense exists, reason about whether it actually constrains the value or state as intended across the full transformation and execution chain. A regex that validates a URL before decoding does not constrain the decoded URL. A permission check in one handler does not protect a second handler that skips it. Start from what the code is trying to guarantee, then look for ways that guarantee can fail.

## What to Review

- **Injection** — SQL, command, template, LDAP, XPath, header injection via unsanitized input
- **Authentication and authorization** — missing or weakened auth checks, hardcoded credentials, insecure token handling, privilege escalation
- **Cryptographic misuse** — weak algorithms, hardcoded keys/IVs, nonce reuse, missing authentication (e.g., AES-CBC without HMAC)
- **Data exposure** — secrets in logs, error messages leaking internals, sensitive data in URLs or query params
- **Input validation** — missing or insufficient validation at trust boundaries, path traversal, open redirects
- **Insecure defaults** — debug mode, permissive CORS, disabled TLS verification, fail-open behavior
- **Deserialization** — untrusted data deserialization without type constraints
- **Dependency risks** — new dependencies with known CVEs, removed security-related dependencies
- **Race conditions** — TOCTOU bugs, unprotected shared state in security-critical paths
- **Transformation chain bypasses** — validation or sanitization that runs before encoding, decoding, normalization, or type coercion, allowing the constrained value to diverge after transformation
- **State and invariant violations** — workflow bypasses where security-critical operations proceed without required preconditions, missing state guards on multi-step processes
- **Resource management** — unbounded allocations from attacker-controlled input, missing rate limiting on sensitive endpoints

## Determination Criteria

Flag an issue only when ALL of these hold:

1. It is a concrete security weakness, not a theoretical concern or defense-in-depth suggestion
2. The vulnerability is discrete and actionable (not a general architecture issue)
3. The vulnerable code path is reachable with attacker-controlled input or attacker-influenced state
4. The author would likely fix the issue if aware of the security implications
5. The issue is demonstrable through a specific attack scenario, not speculation

## Priority Levels

- **P0** — Exploitable by remote unauthenticated attacker with immediate impact (RCE, auth bypass, credential theft)
- **P1** — Exploitable with preconditions (authenticated attacker, specific configuration, race condition)
- **P2** — Security weakness that increases attack surface or weakens defense-in-depth
- **P3** — Minor security hygiene issue with minimal direct impact

## What to Ignore

- Style and naming unless it creates a security-relevant ambiguity
- Defense-in-depth suggestions when the primary defense demonstrably holds (not just exists)
- Vulnerabilities in test code that cannot be reached in production

**Extra metadata:** `**Category:** <vulnerability class>`

**Verdict label:** `Security: <secure | concerns found>`
