---
name: security-review
description: Adversarial security audit — STRIDE threat modeling, OWASP Top 10 mapping, supply-chain (CVE/SBOM) review, secrets scanning, auth/authz analysis. Use when reviewing changes that touch authentication, authorization, input parsing, deserialization, network I/O, dependencies, secrets, or before any production release / external-surface PR.
---

Threat modeling is hypothesis generation for an adversary. Walk the change set as the attacker would: where does untrusted input enter, what trust boundary does it cross, what does it gain on the other side. Every unaudited path is a free move for the attacker.

## When to Apply / NOT

Apply: new external surface (HTTP route, RPC method, file upload); AuthN/AuthZ change; deserialization / parsing of untrusted input; new dependency or major-version upgrade; cryptographic change; pre-release of public-facing service; incident postmortem.

NOT apply: internal refactor with no trust-boundary delta; pure performance work; documentation-only changes; internal-only experimental code.

## Anti-patterns

- **Allowlist-by-omission**: treating "no obvious issue" as "secure".
- **Crypto improvisation**: hand-rolling primitives.
- **Trust the client**: validating only client-side.
- **Logging secrets**: tokens, PII, session cookies in logs.
- **Default-permit ACL**: authorization checks on opt-in basis.
- **Magic-string config**: secrets in source / env files.
- **Outdated SBOM**: stale dependency snapshots.
- **Skipping the threat model**: jumping to checklist without naming assets/actors/boundaries.

## STRIDE Question Template

Apply each prompt to every component touched by the change.

| Letter | Threat | Required questions |
|---|---|---|
| **S** | Spoofing | Who is the principal? How is identity proven? Can the credential be forged, replayed, or stolen? Is MFA / mutual-auth enforced? |
| **T** | Tampering | What inputs cross the trust boundary? Are they validated against an explicit schema (Zod / Pydantic / serde)? Are messages integrity-protected (HMAC / signature / TLS)? |
| **R** | Repudiation | Are security-relevant actions logged with actor + timestamp + outcome? Are logs append-only / tamper-evident? |
| **I** | Information Disclosure | What data is returned in error paths, logs, telemetry? Are PII / secrets ever serialized? Are timing side-channels addressed (constant-time compare)? |
| **D** | Denial of Service | Are inputs bounded (size, count, depth)? Is parsing resource-limited (zip-bomb, billion-laughs, ReDoS)? Are external calls rate-limited? |
| **E** | Elevation of Privilege | What privilege does the new code execute under? Is least privilege honored? Can input alter privilege (path traversal, SQL injection, deserialization gadget)? |

For each "yes" / "unclear" answer, file a finding with severity and remediation owner.

## OWASP Top 10 (2021) Walkthrough

1. **Broken Access Control** — `git grep -n -C 3 'authorize\|@PreAuthorize\|require_role'` then trace policy.
2. **Cryptographic Failures** — `git grep -n -E 'MD5|SHA1|DES|Random\(\)'` for weak primitives. Use `-E` (extended regex) for alternation; `-F` (fixed-string) breaks the pipe-as-OR. Add ecosystem patterns as needed: `Math.random`, `secrets.choice`, `Mersenne` constants.
3. **Injection** — `ast-grep` patterns for unparameterized queries / shell concat / template eval.
4. **Insecure Design** — threat model walk; cross-check STRIDE.
5. **Security Misconfiguration** — TLS / CORS / CSP / cookie flags / debug toggles.
6. **Vulnerable & Outdated Components** — language-family CVE scanner.
7. **Identification & Authentication Failures** — token TTL, refresh, session fixation, MFA.
8. **Software & Data Integrity Failures** — lockfile pinned; signature-verified artifacts; CI provenance.
9. **Security Logging & Monitoring Failures** — audit log coverage; alert on auth-fail / privilege-escalation.
10. **Server-Side Request Forgery** — egress allowlist; SSRF guard on URL inputs.

## Parallel Dep-Audit Tooling

| Family | CVE scanner | Secrets / history | SBOM |
|---|---|---|---|
| Rust | `cargo audit`, `cargo deny check advisories` | `gitleaks`, `trufflehog` | `cargo cyclonedx`, `syft` |
| Python | `pip-audit`, `safety check` | `gitleaks`, `detect-secrets` | `cyclonedx-py`, `syft` |
| JavaScript/TypeScript | `npm audit`, `pnpm audit`, `bun audit` | `gitleaks`, `trufflehog` | `cyclonedx-bom`, `syft` |
| Go | `govulncheck`, `nancy` | `gitleaks`, `trufflehog` | `cyclonedx-gomod`, `syft` |
| Java/Kotlin | OWASP Dependency-Check, `gradle dependencyCheckAnalyze` | `gitleaks`, `trufflehog` | CycloneDX Gradle/Maven, `syft` |
| OCaml | `opam audit`, opam-repository advisory feed | `gitleaks`, `detect-secrets` | `syft` (filesystem) |

Use `fd -e <ext>` (not `find`). Use `git grep -n -F 'literal'` (not `grep`). Use `bat -P -p -n` (not `cat`).

## Constitutional Rules

1. **Default deny**.
2. **Validate at the trust boundary** — schema-validate every input.
3. **Never roll your own crypto**.
4. **No secrets in source** — vault-only; enforce via `gitleaks`.
5. **Pin and verify** — lockfiles checked in, integrity hashes enforced.
6. **Log security events** — every AuthN/AuthZ outcome.
7. **Severity is a contract** — Critical/high block merge.
