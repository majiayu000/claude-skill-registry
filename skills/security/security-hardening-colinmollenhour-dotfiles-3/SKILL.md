---
name: security-hardening
description: Review code for application-level security hardening issues beyond framework checklists. Focuses on abuse prevention, API protection, business logic exploitation, rate limiting, input validation, and early request rejection. Use when auditing code for security, reviewing endpoints for abuse potential, or checking application resilience to real-world attacks.
allowed-tools: Read, Grep, Glob, LS, WebFetch, WebSearch, Task
---

# Security Review

A read-only security review skill focused on **application-level security concerns** that emerge after deployment—issues that framework security guides don't cover.

## Philosophy

Framework security checklists help teams use tools correctly. They stop where application-specific behavior begins. This skill focuses on what breaks later:

- Abuse and misuse that looks like valid traffic
- Business logic that works for real users but fails at scale
- APIs called in ways you didn't expect
- Automated traffic exploiting assumptions about human behavior

## Review Checklist

When reviewing code, systematically evaluate these areas:

### 1. Automated Traffic & Bot Resilience

**Key questions:**
- Can we distinguish human traffic from automated traffic?
- Which endpoints are most attractive to bots?
- Would IP blocking alone be sufficient, or is behavioral analysis needed?

**Look for:**
- Endpoints with no bot detection or CAPTCHA
- Scraping-attractive routes (pricing, product data, user directories)
- Form submissions without behavioral signals
- Login/signup flows vulnerable to credential stuffing

**Red flags:**
```
- Public APIs without authentication
- No rate limiting on enumerable resources (/users/1, /users/2, ...)
- Predictable resource identifiers
- Missing bot detection on high-value flows
```

### 2. API Protection & Rate Limiting

**Key questions:**
- Are rate limits applied per user, per token, or per IP?
- Do authenticated and anonymous users have different limits?
- Can expensive operations be triggered repeatedly?
- Do limits reflect actual usage patterns?

**Look for:**
- Missing rate limiting on mutation endpoints
- Rate limits that don't account for authenticated vs anonymous
- Expensive operations (DB queries, external API calls, file processing) without throttling
- Generic rate limits that don't match business logic

**Red flags:**
```
- Global rate limits only (no per-user/per-endpoint granularity)
- Rate limits checked after expensive operations
- No rate limiting on password reset, signup, or verification flows
- Missing rate limits on search or export endpoints
```

**Good patterns:**
```typescript
// Rate limit with user context
rateLimit({
  keyGenerator: (req) => req.user?.id || req.ip,
  windowMs: 15 * 60 * 1000,
  max: (req) => req.user ? 1000 : 100, // Different limits for authed users
});

// Tiered limits for different operations
const limits = {
  read: { window: '1m', max: 100 },
  write: { window: '1m', max: 10 },
  export: { window: '1h', max: 5 },
};
```

### 3. Business Logic Abuse

**Key questions:**
- What actions would be expensive or harmful if automated?
- Which flows could be abused without triggering errors?
- Where do product rules need enforcement beyond validation?

**Look for:**
- Signup flows assuming humans move slowly
- Free trials assuming honest usage
- Checkout logic assuming single user at a time
- Referral/reward systems without abuse prevention
- Resource creation without ownership limits

**Red flags:**
```
- No limit on free trial signups per email domain
- Coupon/discount codes without usage tracking
- Referral bonuses without fraud detection
- Bulk operations without progress limits
- Vote/rating systems without velocity checks
```

**Abuse scenarios to consider:**
- Can a user create unlimited resources?
- Can timing attacks reveal sensitive information?
- Can parallel requests bypass sequential assumptions?
- Can free tiers be exploited for resource mining?

### 4. Input Validation & Early Rejection

**Key questions:**
- Do bad requests reach expensive code paths?
- Are invalid requests rejected as early as possible?
- Do failures behave predictably under load?

**Look for:**
- Validation after database queries or external API calls
- Large payload processing before authentication
- Missing size limits on uploads, JSON bodies, arrays
- Regex patterns vulnerable to ReDoS
- Deep object nesting without limits

**Red flags:**
```
- No Content-Length limits
- Unbounded array iteration from user input
- Database queries before input validation
- File processing before permission checks
- JSON parsing of arbitrary-depth objects
```

**Good patterns:**
```typescript
// Reject early - before any expensive work
app.use(express.json({ limit: '100kb' }));

// Validate structure before processing
const schema = z.object({
  items: z.array(z.string()).max(100),
  depth: z.number().max(10),
});

// Fail fast on invalid input
if (!isValidFormat(input)) {
  return res.status(400).send('Invalid format');
}
// Only then do expensive work
const result = await expensiveOperation(input);
```

### 5. Cost & Resource Protection

**Key questions:**
- What's the cost multiplier of a single request? (1 request = N database queries?)
- Can users trigger unbounded resource consumption?
- Are serverless/usage-based costs protected?

**Look for:**
- N+1 query patterns triggered by user input
- Unbounded pagination or export
- Large file uploads without quotas
- External API calls multiplied by user input
- Cache-busting through parameter manipulation

**Red flags:**
```
- No pagination limits (page_size=10000)
- Export endpoints without row limits
- Image processing without size limits
- GraphQL without query depth/complexity limits
- Recursive operations on user-provided data
```

### 6. Monitoring & Observability

**Key questions:**
- Can we detect when abuse starts?
- Do we know which endpoints are being targeted?
- Are security events logged and alertable?

**Look for:**
- Missing logging on authentication failures
- No metrics on rate limit triggers
- Unlogged admin/sensitive operations
- No anomaly detection signals

**Should be logged:**
```
- Failed authentication attempts (with IP, user agent)
- Rate limit triggers
- Permission denied events
- Unusual access patterns (bulk reads, rapid requests)
- Admin actions
```

## Review Process

1. **Map the attack surface**
   - List all public endpoints
   - Identify authenticated vs unauthenticated routes
   - Find endpoints that accept user input
   - Note endpoints that trigger expensive operations

2. **Trace request lifecycle**
   - Where does validation happen?
   - When is authentication checked?
   - What happens before rate limits apply?
   - Where do database/external calls occur?

3. **Think like an abuser**
   - What if this endpoint was called 10,000 times?
   - What if multiple requests came simultaneously?
   - What if the input was at maximum allowed size?
   - What if a bot was probing this systematically?

4. **Check deployment context**
   - Serverless? (cost implications of abuse)
   - Edge? (different security model)
   - Traditional server? (resource exhaustion risks)

## Output Format

When reporting findings, use this structure:

```markdown
## Security Review: [Component/Feature Name]

### Summary
[Brief overview of what was reviewed and key findings]

### Critical Issues
[Issues that need immediate attention]

### Warnings
[Issues that should be addressed but aren't immediately exploitable]

### Recommendations
[Suggested improvements and patterns to adopt]

### Questions for the Team
[Areas that need clarification or business context]
```

## What This Skill Does NOT Cover

This skill focuses on application-layer abuse. It does **not** replace:

- Framework-specific security guides (follow those first)
- OWASP Top 10 basics (XSS, SQLi, CSRF)
- Infrastructure security (TLS, secrets management)
- Authentication implementation details
- Dependency vulnerability scanning

For those concerns, use framework documentation and dedicated security tools.

## References

- OWASP API Security Top 10
- Rate limiting best practices
- Bot management strategies
- Serverless security considerations
