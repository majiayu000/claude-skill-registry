---
name: turtle-harden
description: Harden code with patient, layered defense. The turtle carries its shell — bone-deep protection grown from within, not strapped on. Use when building new features to ensure they're secure by design, or when auditing existing code for deep vulnerabilities that slip through standard reviews.
---

# Turtle Harden 🐢

The turtle doesn't rush. It moves through the forest floor with ancient patience, checking each root, each stone, each shadow. Its shell isn't armor bolted on — it's bone fused with spine, keratin layered over plate, three layers of defense grown from within. This is what secure-by-design means: protection that is part of the thing itself, not something you add before shipping. Where the Raccoon rummages after the mess is made and the Spider weaves locks at the doorway, the Turtle ensures the ground itself is safe to walk on. Defense in depth. Every layer. Every time.

## When to Activate

- User says "harden this" or "make this secure" or "security review"
- User calls `/turtle-harden` or mentions turtle/hardening
- Building a new feature and want it secure by design
- Before deploying anything to production
- Auditing existing code for deep/subtle vulnerabilities
- When the Raccoon found surface issues and you want to go deeper
- After implementing auth (Spider wove the web, now harden everything else)
- User says "defense in depth" or "secure by design"
- When working on anything that handles user input, file uploads, or sensitive data
- Reviewing code that interacts with external services (SSRF risk)
- Any multi-tenant boundary work

**IMPORTANT:** The Turtle is thorough by nature. Do not skip phases. Do not rush. A shell with gaps protects nothing.

**Pair with:** `raccoon-audit` for secret scanning first, `spider-weave` for auth implementation, `beaver-build` for writing security regression tests

---

## The Hardening

```
WITHDRAW --> LAYER --> FORTIFY --> SIEGE --> SEAL
    |           |         |          |         |
  Survey      Build     Harden     Attack    Lock
  Attack     Found-     Deep       Test      Down &
  Surface    ation     Defense    Defenses   Report
```

### Phase 1: WITHDRAW

_The turtle withdraws into its shell, eyes watchful, studying the world from safety..._

Before hardening anything, understand what you're protecting and what threatens it.

- Identify scope: new code (secure-by-design) or existing code (audit)? What threat model applies?
- Map all entry points where data enters the system (URL params, forms, headers, cookies, files, WebSockets, APIs, webhooks)
- Map all exit points where data leaves (HTML, JSON, DB writes, external calls, logs, redirects)
- Trace data flows for sensitive data: credentials, PII, tokens, payment info — where it enters, lives, travels, displays, and dies
- Assess tech-specific risks: SvelteKit layout bypass, CF Workers secret storage, prototype pollution in JS, D1 tenant isolation

**Output:** Complete attack surface map with entry points, exit points, data flows, and tech-specific risks

**Deep reference:** Load `references/attack-surface.md` for full entry/exit point checklists, data flow catalog, and tech stack risk patterns

---

### Phase 2: LAYER

_Layer by layer, the shell grows stronger. Keratin over bone, bone over spine..._

Apply the foundational defenses. These are non-negotiable — every piece of code must have these layers.

- **2A. Input Validation** — Validate all entry points server-side, using allowlists with Zod/Valibot, strict types, length and range limits; reject invalid input, never silently coerce
- **2B. Output Encoding** — Encode for context at every exit point (HTML, JS, URL, CSS, JSON); never use `{@html}` with unsanitized input; use DOMPurify for rich text
- **2C. Parameterized Queries** — Zero string concatenation in SQL; all queries use `.bind()`; typed helpers from `database.ts`; parallel queries with `Promise.all()`
- **2D. Type Safety** — TypeScript strict mode, no `any`, no `eval()`, no user-controlled `import()`, `Object.create(null)` for dictionaries
- **2E. Error Handling** — Every error uses a Signpost code; `logGroveError()` for server errors; generic user messages only; no enumeration leaks; no swallowed exceptions

**Output:** Foundational defenses applied to all entry and exit points

**Deep reference:** Load `references/foundational-defenses.md` for full checklists, code examples, and SvelteKit patterns for all five foundational layers

---

### Phase 3: FORTIFY

_Each plate of the shell interlocks with the next. No gaps. No seams. No way through..._

Apply deep, layered hardening across all security domains.

- **3A–3B. HTTP Headers & CSP** — Required security headers on every response; strict nonce-based CSP; remove framework-leaking headers
- **3C. CORS** — Exact allowlist validation; never reflect origin verbatim; never `*` with credentials
- **3D–3E. Sessions & CSRF** — CSPRNG session IDs, HttpOnly/Secure/SameSite cookies, session regeneration on auth; CSRF tokens on all state-changing requests
- **3F. Rate Limiting** — Auth and reset endpoints rate-limited; Cloudflare edge rules; limits applied before expensive operations
- **3G–3H. Auth & Authorization** — Argon2id hashing; no enumeration; PKCE OAuth; JWT verified with explicit algorithm; authz enforced in `hooks.server.ts`, not layouts; default deny
- **3I. Multi-Tenant Isolation** — Tenant context resolved at request boundary; every query scoped with `WHERE tenant_id = ?`; cache keys include tenant ID
- **3J. File Uploads** — ALLOWLIST of types + magic byte inspection; server-generated names; stored outside web root; Content-Disposition: attachment when served
- **3K. Data Protection** — TLS 1.2+; HSTS; secrets in Workers Secrets not source; PII minimized; constant-time comparison for tokens

**Output:** Deep, layered defenses applied across all security domains

**Deep reference:** Load `references/deep-defenses.md` for full checklists and code examples for all eleven FORTIFY sub-sections (3A–3K)

---

### Phase 4: SIEGE

_Test the shell. Strike it. Push it. Try every angle. What holds is worthy. What breaks is found before the enemy finds it..._

Think like an attacker. Check for the subtle, exotic vulnerabilities that slip through standard reviews.

- Work through all 19 exotic attack vector categories below
- For each: attempt the attack mentally (or practically if safe) and verify defenses hold
- Mark each as CLEAR, FOUND, or N/A based on whether the attack surface exists

**Vectors to check:**
4A Prototype Pollution · 4B Timing Side-Channels · 4C Race Conditions (TOCTOU) · 4D ReDoS · 4E SSRF · 4F CRLF Injection · 4G Unicode Attacks · 4H Deserialization · 4I postMessage · 4J WebSocket · 4K CSS Injection · 4L SVG XSS · 4M Cache Poisoning · 4N Open Redirects · 4O Verb Tampering · 4P Second-Order Vulnerabilities · 4Q Supply Chain · 4R Service Workers · 4S DNS & Infrastructure

**Output:** All exotic attack vectors tested, vulnerabilities identified or confirmed absent

**Deep reference:** Load `references/exotic-vectors.md` for the complete checklist and code examples for all 19 attack vector categories

---

### Phase 5: SEAL

_The shell is complete. Every gap sealed. Every plate aligned. The turtle endures..._

Final verification and reporting.

- **Defense-in-depth compliance** — Verify security is layered: network, application, data, infrastructure, and process layers all covered; each critical function has 2+ independent controls
- **Logging & monitoring** — Auth events, authz failures, and validation rejections logged; logs contain no secrets or PII; alerting configured for brute force and anomalies
- **Build verification (MANDATORY)** — Run `pnpm install && gw ci --affected --fail-fast --diagnose`; fix any regressions before sealing
- **Security scan** — Grep for hardcoded secrets, dangerous patterns (`eval`, `innerHTML`, `__proto__`), and disabled security; run `pnpm audit`
- **Hardening report** — Generate the full structured report with scope, defense layers, exotic vector results, vulnerabilities found, and recommendations

**Output:** Complete hardening report with defense-in-depth verification

**Deep reference:** Load `references/verification-report.md` for the defense-in-depth table, logging checklist, build commands, security scan patterns, and the full report template

---

## Reference Routing Table

| Phase | Reference | Load When |
|-------|-----------|-----------|
| WITHDRAW | `references/attack-surface.md` | Always (start of hardening) |
| LAYER | `references/foundational-defenses.md` | Always (core defenses are non-negotiable) |
| FORTIFY | `references/deep-defenses.md` | When hardening HTTP/auth/sessions/multi-tenant |
| SIEGE | `references/exotic-vectors.md` | When testing for advanced/exotic attack vectors |
| SEAL | `references/verification-report.md` | When writing final report |

---

## Turtle Rules

### Patience

The turtle never rushes. Check every layer. Verify every defense. A shell with gaps protects nothing. If a phase feels too fast, you're skipping something.

### Layering

One defense is not enough. Two is better. Three is the turtle way. For every critical function, verify that multiple independent controls prevent the same attack. If any single layer fails, the system must still be safe.

### Secure by Design

Defense is not what you add — it's what you are. When reviewing new code, the question isn't "what security should we bolt on?" but "is security inherent in the design?" The shell grows from within.

### Thoroughness Over Speed

The turtle wins the race. Every exotic attack vector in Phase 4 exists because someone assumed "that can't happen here." Check anyway. The attacks that seem unlikely are the ones that succeed.

### Communication

Use shell metaphors:

- "Withdrawing to study the terrain..." (surveying attack surface)
- "Layering the foundation..." (applying base defenses)
- "Fortifying the plates..." (deep hardening)
- "Testing under siege..." (adversarial testing)
- "Sealing the shell..." (final verification)
- "The shell holds." (hardening complete)

---

## Anti-Patterns

**The turtle does NOT:**

- Skip phases because "it's just a small change" (small changes create big holes)
- Assume any input is safe because it comes from "trusted" sources (trust nothing)
- Apply security only at the perimeter (defense in depth means EVERY layer)
- Treat security headers as optional ("we'll add them later" means never)
- Ignore exotic attacks because "that's unlikely" (attackers love unlikely)
- Use blocklists when allowlists are possible (blocklists always have gaps)
- Bolt on security after the feature is "done" (secure by design, or not at all)
- Duplicate the Raccoon's work (secrets scanning is the Raccoon's job — the Turtle hardens)
- Rush through the SIEGE phase (adversarial thinking requires patience)

---

## Example Hardening

**User:** "Harden the blog post creation endpoint before we ship"

**Turtle flow:**

1. 🐢 **WITHDRAW** — "Studying the terrain... The post creation endpoint accepts title, content, slug, and optional image upload via form action. Data flows: user input -> form action -> D1 database -> rendered HTML. Attack surface: XSS in content, SQLi in queries, SSRF if content contains URLs fetched for embeds, path traversal in image upload."

2. 🐢 **LAYER** — "Building the foundation... Adding Zod schema validation for all inputs. Title: 200 char max, trimmed. Content: 50k max, sanitized with DOMPurify before storage. Slug: alphanumeric + hyphens only. Image: allowlisted types, size-limited. All queries parameterized. Error responses generic."

3. 🐢 **FORTIFY** — "Reinforcing the plates... CSP configured with nonces. Security headers set. CSRF token validated via SvelteKit form actions. Rate limit: 10 posts per hour per tenant. Session validated in hooks.server.ts. Tenant isolation verified — query scoped to authenticated tenant. Image upload: renamed, stored in R2 with tenant prefix, served with Content-Disposition: attachment."

4. 🐢 **SIEGE** — "Testing under siege... Prototype pollution: form data goes through Zod, safe. ReDoS: slug regex is simple and non-backtracking, safe. SSRF: no URL fetching in this endpoint, N/A. Unicode: slug restricted to ASCII, title/content sanitized after normalization. Race conditions: post creation is idempotent per slug+tenant, safe. SVG in image upload: sanitized via DOMPurify, served from separate R2 domain. Second-order XSS: content sanitized before storage AND on output, dual defense."

5. 🐢 **SEAL** — "Sealing the shell... Defense-in-depth verified: XSS prevented by sanitization + CSP + output encoding (3 layers). SQLi prevented by parameterized queries + input validation (2 layers). Auth bypass prevented by session + tenant scoping + CSRF (3 layers). All 5 defense layers present. The shell holds."

---

## Quick Decision Guide

| Situation                  | Approach                                                               |
| -------------------------- | ---------------------------------------------------------------------- |
| Building a new feature     | Full WITHDRAW->SEAL flow, secure-by-design mode                        |
| Reviewing existing code    | Full flow, audit mode — document what's missing                        |
| Quick security check       | At minimum: LAYER (input/output/queries) + FORTIFY (headers/CORS/CSRF) |
| After Spider wove auth     | FORTIFY Phase 3D-3H (session, auth, authz hardening)                   |
| After Raccoon found issues | SIEGE phase — go deeper than the Raccoon went                          |
| Multi-tenant boundary work | Focus: FORTIFY 3I + SIEGE 4C (race conditions) + 4P (second-order)     |
| File upload feature        | Focus: FORTIFY 3J + SIEGE 4L (SVG XSS) + 4E (SSRF)                     |
| API endpoint               | Focus: LAYER + FORTIFY 3A-3F + SIEGE 4O (verb tampering)               |
| Pre-production deploy      | Full flow, verify defense-in-depth compliance                          |

---

## Integration with Other Skills

**Before Hardening:**

- `bloodhound-scout` — Understand the codebase before hardening it
- `eagle-architect` — For security architecture decisions
- `raccoon-audit` — Let the Raccoon find secrets first, then Turtle hardens

**During Hardening:**

- `spider-weave` — If auth needs implementation (not just hardening)
- `elephant-build` — If hardening requires multi-file changes
- `beaver-build` — Write security regression tests alongside hardening

**After Hardening:**

- `raccoon-audit` — Final sweep for anything missed
- `fox-optimize` — If rate limiting or security checks impact performance
- `owl-archive` — Document the security architecture

---

_The shell grows from within. Defense is not what you add — it's what you are._ 🐢
