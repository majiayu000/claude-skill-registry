---
name: crypto-compliance
description: The banned-primitive gate. Routed to when changed code hashes, signs, encrypts, derives keys, generates security-relevant randomness, configures TLS, or imports a crypto library. Rejects broken primitives, disabled TLS verification, and home-rolled crypto; the approved-primitive list lives in security-controls.md. The auth-crypto-reviewer agent is dispatched as the reviewer.
---

# crypto-compliance

The banned-primitive gate. Routed to when changed code uses cryptography, hashing, signing, key derivation, security-relevant random generation, or TLS configuration.

## Pre-flight

Read these, or STOP and surface the gap — never guess the policy:

- `<project-root>/.codearbiter/security-controls.md` — the project's approved and forbidden primitives, key requirements, and TLS minimum. If this file is unreadable, BLOCK; do not infer the policy.

## Phase 1 — Banned-primitive scan · gate: BLOCK

Scan every crypto operation in the changed code against `security-controls.md`. Apply the project's forbidden list; where it is silent, the following BLOCK unconditionally:

- **Broken primitives** — `md5`, `sha1`/`sha-1` (including in HMAC or "just for IDs"), `des`, `3des`, `rc4`, and RSA keys below 2048 bits.
- **Disabled TLS verification** — `rejectUnauthorized: false`, `verify: false`, or any disabling of certificate peer verification, on any connection.
- **Home-rolled crypto** — a hand-built cipher, AEAD, KDF, signature scheme, or any reimplementation of a primitive in userland instead of a vetted, approved one.
- **Unapproved primitive or library** — any algorithm, mode, key size, or crypto library not on the approved list in `security-controls.md`.

Dispatch the `auth-crypto-reviewer` agent (`${CLAUDE_PLUGIN_ROOT}/agents/auth-crypto-reviewer.md`) to confirm these findings against `security-controls.md`.

Gate: no banned or unapproved primitive, no disabled TLS verification, and no home-rolled crypto in the changed code.

**On pass — record the gate:** follow `${CLAUDE_PLUGIN_ROOT}/includes/security-gate-record.md` (the shared record mechanism). For this gate the relevant commit hook is **H-09b** (crypto/TLS). On any BLOCK, do NOT record the pass.

**Out-of-scope finding:** do not act on it and do not author an ADR (ADRs are user-attributed, via `/adr` only). Mark it inline with `[NEEDS-TRIAGE]`; never silently drop it.

## Hard rules

- MUST read `security-controls.md` before scanning — BLOCK if it cannot be read.
- MUST NOT use MD5, SHA1, DES, 3DES, RC4, or RSA below 2048 bits — even for non-security checksums or IDs.
- MUST NOT set `verify: false` or `rejectUnauthorized: false`, or otherwise disable certificate verification, on any TLS connection.
- MUST NOT use a home-rolled or userland-reimplemented cryptographic primitive.
- MUST NOT use any primitive, key size, or crypto library not on the approved list in `security-controls.md`.
- MUST record the `security-gate-passed` marker (via `hooks/security-pass.py`) ONLY when the gate genuinely passes — the marker is what unblocks the commit (hook H-09b), so a premature or unconditional recording defeats the gate.
