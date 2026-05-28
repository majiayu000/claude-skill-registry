---
name: factcheck-guard
description: Use this skill when making any factual claim about the codebase — existence, absence, or behavior. Converts the claim-verification rule into a systematic action protocol that prevents false assertions from grep-only results.
---

# FactCheck Guard — Runtime Claim Verification

Prevents false claims about the codebase. Grep results are hypotheses, not proof.
Every assertion about "what the code does" must be verified by reading the actual code.

## Why This Exists

An 80% false claim rate was observed when agents trusted grep results without reading files.
The pattern repeats: grep finds a string, agent asserts behavior, behavior is wrong.
This skill converts the claim-verification guidelines into an actionable protocol.

## Confidence Markers (MANDATORY)

Every factual claim about the codebase MUST carry one of these markers:

| Marker | Meaning | Requirements |
|--------|---------|-------------|
| [VERIFIED] | Read the file, traced the logic | Must cite file:line |
| [INFERRED] | Based on grep or file name | Must verify before asserting to others |
| [UNCERTAIN] | Not yet checked | Must investigate before making the claim |

Never promote an [INFERRED] claim to a statement of fact.
Never let [UNCERTAIN] appear in a response to the user — investigate first.

---

## Verification Protocol

### Level 1: Existence Claims

When asserting "X exists in the codebase":

**Step 1 — Search (produces [INFERRED])**
```
Grep/Glob for the pattern.
Result: "X appears at path/to/file.ts:42" [INFERRED]
```

**Step 2 — Read the file (required to reach [VERIFIED])**
```
Read path/to/file.ts, locate line 42.
Confirm the match is actual code, not a comment or string literal.
```

**Step 3 — Check context**
```
Is the code in a live code path, or inside a dead branch / disabled block?
Is it imported and actually used?
Does the function name match what you expected, or is it a different concept?
```

**Step 4 — State the claim with citation**
```
"Error handling exists at src/api/handler.ts:67 — try/catch wraps the database call" [VERIFIED]
```

---

### Level 2: Absence Claims

When asserting "X does NOT exist" — absence claims are the most dangerous.
A single missed search term invalidates the entire claim.

**Step 1 — Primary search**
```
Grep for the primary term. No results found.
Status: [INFERRED ABSENT] — not yet VERIFIED
```

**Step 2 — Alternative terms (minimum 3)**
```
Different naming conventions, abbreviations, synonyms.

Example: Searching for "rate limiting"
Try: "rateLimit", "rate_limit", "throttle", "throttling", "requestLimit", "limiter"
If any match: investigate that file before concluding
```

**Step 3 — Check likely locations manually**
```
Where would X logically live if it existed?
Read those files directly — grep may miss dynamically constructed patterns.

Example: Checking for auth middleware
Read: src/middleware/, app/middleware.ts, server.ts, app.ts
Even if grep found nothing, scan these files for auth-related logic.
```

**Step 4 — Only then claim VERIFIED ABSENT**
```
"Rate limiting does not exist. Searched: rateLimit, rate_limit, throttle, throttling,
requestLimit, limiter. Checked: src/middleware/index.ts, server.ts, app.ts. None found." [VERIFIED ABSENT]
```

---

### Level 3: Behavior Claims

When asserting "the system does X" — the most subtle failure mode.
Finding a function name does not tell you what the function actually does.

**Step 1 — Locate the function**
```
Grep/Glob finds the function name.
Status: [INFERRED] — you know it exists, not what it does
```

**Step 2 — Read the full function body**
```
Read the file. Read the entire function, not just the signature.
Look for: branches, early returns, side effects, what it actually returns.
```

**Step 3 — Trace the logic path**
```
Follow the execution path relevant to your claim.
If the function calls other functions, read those too (one level deep minimum).
Check: what happens in the error path? What are the edge cases?
```

**Step 4 — State behavior with evidence**
```
"processPayment() validates card number via Luhn check (payment.ts:34),
then calls Stripe API (payment.ts:41), and on failure rolls back the DB
transaction (payment.ts:58) — it does NOT charge the card on validation failure." [VERIFIED]
```

---

## Common False Claim Patterns

| Pattern | Why It Fails | Correct Approach |
|---------|-------------|-----------------|
| grep found "try.*catch" | Could be in comment, string, or test mock | Read the file, confirm it wraps real code |
| grep found nothing | Wrong term, wrong directory, different naming | Try 3+ alternative terms |
| File named auth.ts exists | Doesn't mean auth is implemented | Read the file |
| Type definition has a field | Doesn't mean the field is set or used | Grep for field assignment and usage |
| Function is called somewhere | Doesn't mean it does what the name implies | Read the function body |
| Found in __tests__ directory | Test mocks are not real implementations | Confirm the actual source file |
| grep -L returned files | Those files lack the pattern — but pattern might exist under a different name | Try alternative terms before concluding |
| Found in commented-out block | Not active code | Check if block is enabled |

---

## Two-Pass Audit Protocol

For system audits, security reviews, and architecture reviews:

### Pass 1: Generate Hypotheses

Go through each area systematically. Produce hypothesis statements only:

```
"Input validation might be missing from the /api/upload route" [INFERRED]
"The auth token might not be refreshed on expiry" [INFERRED]
"Database queries might not use parameterized statements" [INFERRED]
```

Do not state these as facts. Do not include them in the user-facing summary.

### Pass 2: Verify Each Hypothesis

For every [INFERRED] hypothesis:

```
Hypothesis: "Input validation missing from /api/upload" [INFERRED]

Action: Read src/app/api/upload/route.ts
Found: Zod schema validation at line 18, applied before file processing.
Result: "Input validation exists at api/upload/route.ts:18" [VERIFIED]
Hypothesis was wrong.
```

```
Hypothesis: "Database queries might not be parameterized" [INFERRED]

Action: Search for raw SQL patterns (string interpolation in queries)
Grep: `db.query(\`.*\${`, `db.execute(\`.*\${`
Read: src/lib/db.ts, src/repositories/*.ts
Found: All queries use prepared statements. One raw query at analytics.ts:89.
Result: "Raw SQL injection risk at src/analytics.ts:89" [VERIFIED]
```

Only after Pass 2 are claims safe to report.

---

## Quick Checklist

Before making any codebase claim, confirm:

- [ ] Have I read the actual file, not just grep results?
- [ ] Is the code in a live path (not commented out, not test-only)?
- [ ] For absence claims: did I try 3+ alternative search terms?
- [ ] For absence claims: did I manually check the likely locations?
- [ ] For behavior claims: did I read the full function, not just the name?
- [ ] Does my claim include a file:line citation?
- [ ] Is my marker accurate: [VERIFIED] / [INFERRED] / [UNCERTAIN]?

---

## Integration Points

**claim-verification.md** — the rule file provides guidelines; this skill provides the action protocol.

**Agents that must use this skill:**
- code-reviewer: before asserting "the code lacks X"
- security-reviewer: before asserting "vulnerability exists/doesn't exist"
- architect: before asserting "pattern is/isn't used"
- sleuth: before asserting "root cause is X"
- coroner: before asserting "same bug exists elsewhere"

**Hook integration (optional):**
After every Grep tool result, the `epistemic-reminder` hook injects a warning.
That warning is this skill's Level 1 trigger — search results are [INFERRED], not [VERIFIED].

---

## Examples: Wrong vs Right

**Existence claim — WRONG**
```
Grep found "authMiddleware" in 3 files.
Claim: "Auth middleware is applied to all routes."
```

**Existence claim — RIGHT**
```
Grep found "authMiddleware" in 3 files.
Read server.ts: middleware applied only to /api/* routes, not /public/*.
Read admin/router.ts: authMiddleware missing from /admin/health endpoint.
Claim: "Auth middleware applied to /api/* (server.ts:23) but missing from
/admin/health (admin/router.ts:8)." [VERIFIED]
```

**Absence claim — WRONG**
```
Grep "rate limit" returned no results.
Claim: "No rate limiting implemented."
```

**Absence claim — RIGHT**
```
Grep "rate limit" → no results.
Grep "rateLimit", "throttle", "limiter", "requestLimit" → no results.
Read: src/middleware/index.ts, server.ts, next.config.js.
Confirmed none contain request throttling logic.
Claim: "No rate limiting found after searching 6 term variants and
reading 3 likely files." [VERIFIED ABSENT]
```
