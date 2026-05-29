---
name: risk-register
description: Document risks for changes touching auth, data, or migrations. Lists top risks, how to test/monitor them, and rollback strategy.
tools: Read, Grep, Glob
user-invocable: true
---

# Risk Register

For changes that touch sensitive areas (authentication, data, migrations, infrastructure), document the risks explicitly. This is what senior developers do naturally - making it explicit ensures nothing is overlooked.

## When to Use

Use this skill when your change involves:

- **Authentication/Authorization** - Login, sessions, permissions, tokens
- **User Data** - PII, passwords, payment info, user content
- **Data Migrations** - Schema changes, data transformations, backfills
- **External Integrations** - Third-party APIs, webhooks, OAuth
- **Infrastructure** - Deployment, scaling, configuration changes
- **Breaking Changes** - API changes, behavioral changes, deprecations

## Quick Start

```
/risk-register
```

Or specify the change:
```
/risk-register "Adding password reset functionality"
```

## The Risk Register Template

For each risky change, complete this register:

```markdown
# Risk Register: [Feature/Change Name]

## Summary
Brief description of what's changing and why it's sensitive.

## Top 3 Risks

### Risk 1: [Name]
**Likelihood:** Low / Medium / High
**Impact:** Low / Medium / High / Critical

**Description:**
What could go wrong?

**Mitigation:**
How are we preventing this?

**Detection:**
How would we know if this happened?

**Response:**
What do we do if it happens?

---

### Risk 2: [Name]
...

### Risk 3: [Name]
...

## Testing Strategy

### Pre-deployment
- [ ] Unit tests cover the change
- [ ] Integration tests for critical paths
- [ ] Manual testing of edge cases
- [ ] Security review completed

### Post-deployment
- [ ] Smoke test in production
- [ ] Monitor error rates
- [ ] Watch for anomalies in [specific metrics]
- [ ] Verify [specific functionality] works

## Monitoring & Alerting

What should we watch after deployment?

| Metric | Normal Range | Alert Threshold | Response |
|--------|--------------|-----------------|----------|
| Login failure rate | < 5% | > 10% | Check auth service |
| API error rate | < 1% | > 5% | Investigate errors |
| ... | ... | ... | ... |

## Rollback Strategy

### Can we rollback?
Yes / Partial / No (explain why)

### Rollback steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Rollback time estimate
[X minutes/hours]

### Data implications
What happens to data created after deployment if we rollback?

## Approval

- [ ] Engineer reviewed risks
- [ ] Security reviewed (if auth/data)
- [ ] Stakeholder aware of risks
```

## Risk Categories

### Authentication Risks

| Risk | Impact | Common Mitigations |
|------|--------|-------------------|
| Session hijacking | Critical | Secure cookies, HTTPS, token rotation |
| Credential stuffing | High | Rate limiting, MFA, breach detection |
| Token leakage | Critical | Short expiry, secure storage, no logging |
| Privilege escalation | Critical | Strict authz checks, principle of least privilege |
| Account takeover | Critical | Email verification, suspicious activity alerts |

### Data Risks

| Risk | Impact | Common Mitigations |
|------|--------|-------------------|
| Data loss | Critical | Backups, soft deletes, transaction safety |
| Data corruption | Critical | Validation, constraints, idempotency |
| Data leakage | Critical | Access controls, encryption, audit logs |
| Privacy violation | High | PII handling, consent, data minimization |
| Compliance breach | High | Audit trails, retention policies |

### Migration Risks

| Risk | Impact | Common Mitigations |
|------|--------|-------------------|
| Failed migration | High | Dry runs, backups, reversible migrations |
| Data inconsistency | High | Validation checks, reconciliation |
| Downtime | Medium | Rolling deploys, feature flags |
| Performance degradation | Medium | Index analysis, query optimization |

## Example Risk Register

```markdown
# Risk Register: Password Reset Feature

## Summary
Adding password reset via email. Touches auth system, sends emails with tokens,
allows password changes without current password.

## Top 3 Risks

### Risk 1: Token Theft/Replay
**Likelihood:** Medium
**Impact:** Critical

**Description:**
Reset tokens could be intercepted or reused to take over accounts.

**Mitigation:**
- Tokens expire in 1 hour
- Single use (invalidated after use)
- Tokens are cryptographically random (32 bytes)
- HTTPS only

**Detection:**
- Alert on multiple reset attempts for same user
- Log all password resets with IP

**Response:**
- Invalidate all tokens for affected user
- Force password change
- Notify user of suspicious activity

---

### Risk 2: Email Enumeration
**Likelihood:** High
**Impact:** Medium

**Description:**
Attackers could use the reset form to discover which emails have accounts.

**Mitigation:**
- Same response for valid/invalid emails
- Rate limiting on reset endpoint
- CAPTCHA after 3 attempts

**Detection:**
- Monitor for high volume of reset requests
- Alert on requests from same IP for many emails

**Response:**
- Block IP temporarily
- Enable additional rate limiting

---

### Risk 3: Token Logged/Exposed
**Likelihood:** Low
**Impact:** Critical

**Description:**
Reset token appears in logs, error messages, or URLs shared externally.

**Mitigation:**
- Token in POST body, not URL
- Logging excludes token field
- Error messages are generic

**Detection:**
- Grep logs for token patterns
- Review error handling

**Response:**
- Purge affected logs
- Rotate any exposed tokens
- Notify affected users

## Testing Strategy

### Pre-deployment
- [x] Unit tests for token generation, validation, expiry
- [x] Integration test for full reset flow
- [x] Test expired token rejection
- [x] Test reused token rejection
- [x] Security review of token handling

### Post-deployment
- [ ] Smoke test: Complete reset flow in production
- [ ] Monitor email delivery rate
- [ ] Watch for spike in reset requests

## Monitoring & Alerting

| Metric | Normal | Alert | Response |
|--------|--------|-------|----------|
| Reset requests/hour | < 100 | > 500 | Check for abuse |
| Reset completion rate | > 80% | < 50% | Check email delivery |
| Failed reset attempts | < 10% | > 30% | Check token generation |

## Rollback Strategy

### Can we rollback?
Yes - feature flag controls access to reset endpoint.

### Rollback steps
1. Disable `PASSWORD_RESET_ENABLED` feature flag
2. Invalidate all outstanding reset tokens
3. Communicate to support team

### Rollback time estimate
~5 minutes (feature flag toggle)

### Data implications
Outstanding reset tokens will be invalidated. Users mid-reset will need to retry.
```

## Integration with Wiggum

When wiggum detects changes to auth, data, or migrations, it should prompt:

```
This change touches [auth/data/migrations].
Should we create a risk register? (y/n)
```

If yes, use this skill to document risks before proceeding.

## Remember

- **Be specific** - "data loss" is too vague; "orphaned records if parent deleted" is actionable
- **Be honest** - If you can't roll back, say so
- **Think like an attacker** - What would you try if you wanted to break this?
- **Think like ops** - How would you know something is wrong at 3am?

The goal isn't to prevent all risks - it's to **know what the risks are** and have a plan.
