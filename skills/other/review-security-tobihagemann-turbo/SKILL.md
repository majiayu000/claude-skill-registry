---
name: review-security
description: "Analyze code for security vulnerabilities, insecure patterns, and security regressions using strict determination criteria. References the project threat model when available. Returns structured findings without applying fixes. Use when the user asks to \"review security\", \"check for security issues\", \"find vulnerabilities in my changes\", \"run a security review\", \"analyze my code for security\", \"security audit\", or \"security scan\"."
---

# Review Security

Analyze code for security vulnerabilities, insecure patterns, and security regressions. Return structured findings.

## Step 1: Determine the Scope

Determine what to review:

- If a specific **diff command** was provided (e.g., `git diff --cached`, `git diff main...HEAD`), use that.
- If a **file list or directory** was provided, review those files directly (read the full files, not a diff).
- If **neither** was provided, default to diffing against the repository's default branch (detect via `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`).

## Step 2: Load Threat Model Context

Check if `.turbo/threat-model.md` exists at the repository root. If it does, read sections 2 (Trust Boundaries and Assumptions) and 3 (Attack Surface, Mitigations and Attacker Stories) to understand:

- **Assets** at risk and their trust boundaries
- **Attack surfaces** already identified, with their existing mitigations
- **Attacker stories** describing known threat scenarios

Use this context to prioritize findings. Changes that touch identified attack surfaces or weaken documented mitigations deserve heightened scrutiny. Changes that introduce new trust boundary crossings not covered by the threat model are especially important to flag.

If no threat model exists, proceed without it. Do not create one.

## Step 3: Review

1. For diff scope: run the diff command to obtain the changes. For file scope: read the specified files.
2. For each file, read enough surrounding context to understand the code
3. Apply the vulnerability determination criteria and return findings in the output format below

### Review Mindset

Do not treat the existence of a check, sanitizer, or authorization guard as proof of safety. When a defense exists, reason about whether it actually constrains the value or state as intended across the full transformation and execution chain. A regex that validates a URL before decoding does not constrain the decoded URL. A permission check in one handler does not protect a second handler that skips it. Start from what the code is trying to guarantee, then look for ways that guarantee can fail.

### What to Look For

- **Injection** — SQL, command, template, LDAP, XPath, header injection via unsanitized input
- **Authentication and authorization** — missing or weakened auth checks, hardcoded credentials, insecure token handling, privilege escalation
- **Cryptographic misuse** — weak algorithms, hardcoded keys/IVs, nonce reuse, missing authentication (e.g., AES-CBC without HMAC)
- **Data exposure** — secrets in logs, error messages leaking internals, sensitive data in URLs or query params
- **Input validation** — missing or insufficient validation at trust boundaries, path traversal, open redirects
- **Insecure defaults** — debug mode, permissive CORS, disabled TLS verification, fail-open behavior
- **Deserialization** — untrusted data deserialization without type constraints
- **Dependency risks** — new dependencies with known CVEs, removed security-related dependencies
- **Race conditions** — TOCTOU bugs, unprotected shared state in security-critical paths
- **Transformation chain bypasses** — validation or sanitization that runs before encoding, decoding, normalization, or type coercion, allowing the constrained value to diverge after transformation (validate-then-decode, partial normalization, parsing ambiguities between components)
- **State and invariant violations** — workflow bypasses where security-critical operations proceed without required preconditions, missing state guards on multi-step processes, assumptions about execution order that concurrent or out-of-order requests can violate
- **Resource management** — unbounded allocations from attacker-controlled input, missing rate limiting on sensitive endpoints

## Vulnerability Determination Criteria

Flag an issue only when ALL of these hold:

1. It is a concrete security weakness, not a theoretical concern or defense-in-depth suggestion
2. The vulnerability is discrete and actionable (not a general architecture issue)
3. In diff mode: the issue was introduced or worsened by the changeset (do not flag pre-existing issues unless the change removes a mitigation). In file scope mode: this criterion does not apply
4. The vulnerable code path is reachable with attacker-controlled input or attacker-influenced state
5. The author would likely fix the issue if aware of the security implications
6. The issue is demonstrable through a specific attack scenario, not speculation

## Comment Standards

1. Name the vulnerability class (e.g., "SQL injection", "path traversal")
2. Describe the attack scenario: what an attacker controls, what they achieve
3. Keep the body to one paragraph maximum
4. No code chunks longer than 3 lines
5. Reference the trust boundary being crossed when applicable
6. If a threat model exists, note when a finding relates to an identified attack surface
7. Use a matter-of-fact tone

## Priority Levels

- **P0** — Exploitable by remote unauthenticated attacker with immediate impact (RCE, auth bypass, credential theft)
- **P1** — Exploitable with preconditions (authenticated attacker, specific configuration, race condition)
- **P2** — Security weakness that increases attack surface or weakens defense-in-depth
- **P3** — Minor security hygiene issue with minimal direct impact

## What to Ignore

- Style and naming unless it creates a security-relevant ambiguity
- In diff mode: pre-existing vulnerabilities not affected by this changeset
- Defense-in-depth suggestions when the primary defense demonstrably holds (not just exists)
- Vulnerabilities in test code that cannot be reached in production

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, ≤80 chars)>

**File:** `<file path>` (lines <start>-<end>)
**Category:** <vulnerability class>

<one paragraph describing the attack scenario: what input an attacker controls, what code path is triggered, and what the impact is>
```

After all findings, add:

```
## Overall Verdict

**Security:** <secure | concerns found>

<1-3 sentence summary. If a threat model was consulted, note whether the changes affect any identified attack surfaces.>
```

If there are no qualifying findings, state that no security issues were found and explain briefly.
