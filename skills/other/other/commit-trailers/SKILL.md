---
name: commit-trailers
description: Commit mesajlarina yapilandirilmis karar trailer'lari ekle. Constraint, Rejected, Confidence, Scope-risk, Not-tested trailer'lari ile karar baglamini koru.
---

# Commit Trailers -- Structured Decision Context

Supplement conventional commits with structured trailers that preserve the reasoning
behind a change. Future maintainers (and future agents) read commit history to
understand not just what changed, but why a specific approach was taken.

## Standard Trailers

Add these after the commit body, separated by a blank line, when they add value:

```
Constraint: <external limitation that shaped this approach>
Rejected: <alternative considered and the reason it was rejected>
Confidence: high | medium | low  <how certain we are this is correct>
Scope-risk: low | medium | high  <blast radius — how much can this break>
Not-tested: <what was not tested and why>
```

---

## When to Use Each Trailer

| Trailer | When to Include | When to Skip |
|---------|----------------|--------------|
| `Constraint` | External limitation forced a non-obvious decision | No external constraints applied |
| `Rejected` | A reasonable alternative was considered and discarded | Only one approach was viable |
| `Confidence` | Correctness is uncertain or untested in key areas | Straightforward well-tested change |
| `Scope-risk` | Change touches shared infrastructure, middleware, auth, or core data paths | Isolated, single-purpose change |
| `Not-tested` | A gap in test coverage is intentional and known | All paths are tested |

Not every commit needs trailers. A `fix: typo in error message` needs none.
A new auth middleware affecting every API call needs all five.

---

## Trailer Reference

### Constraint
An external limitation — browser API, hosting restriction, library limitation,
business rule, or environment constraint — that ruled out the obvious solution.

```
Constraint: Safari 15 does not support the CSS :has() selector
Constraint: Redis unavailable in staging — in-memory fallback only
Constraint: Must stay on Node 18, no upgrade path in scope
Constraint: Third-party payment API does not support idempotency keys
```

### Rejected
An alternative that was seriously considered. Helps future maintainers understand
why the current approach exists instead of the simpler-looking one they are thinking of.

```
Rejected: Redux — too much boilerplate for this feature's scope
Rejected: JWT stored in localStorage — XSS exposure, using httpOnly cookie instead
Rejected: Direct DB query — bypasses cache layer, use repository instead
Rejected: Polling every 5s — too much server load, went with SSE instead
```

### Confidence
Signal the quality of certainty around the correctness of the change.
`low` should trigger a code review comment or discussion before merge.

```
Confidence: high
Confidence: medium — edge case with concurrent writes not covered by tests
Confidence: low — reversing this migration is complex, needs review before merge
```

### Scope-risk
Signal how much of the system this change can affect if it is wrong.
Helps reviewers and the team calibrate how carefully to review and test.

```
Scope-risk: low
Scope-risk: medium — touches payment processing, needs manual smoke test
Scope-risk: high — auth middleware change, every authenticated endpoint affected
```

### Not-tested
Explicitly acknowledge a test gap. This is honest engineering, not an excuse.
A named gap is better than an invisible one.

```
Not-tested: email delivery — no SMTP server in test environment
Not-tested: concurrent request behavior — requires load testing setup
Not-tested: Safari-specific rendering — no CI browser suite yet
Not-tested: DB rollback on payment failure — requires Stripe test mode setup
```

---

## Full Example

```
feat: add rate limiting to API endpoints

Implement token bucket algorithm for /api/* routes.
Limits: 100 requests/min for free tier, 1000 for paid tier.
Exceeding the limit returns 429 with Retry-After header.

Constraint: Redis required for distributed rate limiting — in-memory does not work across multiple instances
Rejected: express-rate-limit — lacks per-user tier support without significant custom logic
Confidence: high
Scope-risk: medium — affects all /api/* routes, auth and webhook routes excluded
Not-tested: sustained 10K+ req/min behavior — requires dedicated load test environment
```

---

## Format Rules

- Trailers go AFTER the commit body, separated by a blank line
- One trailer per line, no line wrapping
- `Rejected` may appear multiple times (one per rejected alternative)
- Only include trailers that add genuine value — avoid mechanical inclusion
- `Confidence: low` is a signal for the team, not a reason to skip the commit
- This format supplements, not replaces, the conventional commit type prefix

## Integration with Other Rules

- `safety-and-quality.md` defines the base commit format (`<type>: <description>`)
- This rule adds optional trailers on top of that format
- `full-autonomy.md` requires commit approval — trailers give Batuhan the context to approve confidently
- Trailers are the commit-level equivalent of Priority Notes in the notepad system
