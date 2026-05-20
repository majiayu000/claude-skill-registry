---
name: codesyncer
description: AI context persistence - tags in code = permanent memory across sessions
---

# CodeSyncer

> Claude forgets everything when the session ends. CodeSyncer makes it remember.

## When to use

Use this skill on ANY project where you want AI to:
- Remember decisions across sessions
- Track why code was written a certain way
- Auto-pause before touching payment/security/API code
- Never lose context again

## Core Rules

### 1. Always Add Tags

| Situation | Tag | Example |
|-----------|-----|---------|
| You inferred something | `@codesyncer-inference` | `// @codesyncer-inference: Page size 20 (standard UX)` |
| Decision after discussion | `@codesyncer-decision` | `// @codesyncer-decision: [2024-01-15] Using JWT` |
| Non-standard implementation | `@codesyncer-rule` | `// @codesyncer-rule: any type here (no types available)` |
| Needs user confirmation | `@codesyncer-todo` | `// @codesyncer-todo: Confirm API endpoint` |
| Business context | `@codesyncer-context` | `// @codesyncer-context: GDPR requires 30-day retention` |

### 2. Never Infer Critical Values

**ALWAYS ASK the user about:**
- 💰 Prices, fees, discounts, billing
- 🔐 Auth methods, token expiry, encryption
- 🔌 API endpoints, external service URLs
- 🗄️ Database schemas, migrations

```
❌ Bad: "I set the shipping fee to $5"
✅ Good: "What should the shipping fee be?"
```

### 3. Auto-Pause Keywords

When you detect these keywords, **STOP and discuss** before coding:
- payment, billing, subscription, charge, refund
- authentication, login, permission, encrypt, token
- delete, remove, drop, migrate, schema change
- personal data, GDPR, privacy

## Tag Examples

```typescript
// @codesyncer-decision: [2024-01-15] Using Stripe for payments (international support)
// @codesyncer-context: Supports USD, EUR, KRW currencies
const paymentProvider = 'stripe';

// @codesyncer-inference: 5 second timeout (typical API response time)
// @codesyncer-rule: Retry max 3 times (rate limit protection)
const apiConfig = {
  timeout: 5000,
  retries: 3,
};

// @codesyncer-todo: Confirm discount percentage with business team
const DISCOUNT_RATE = 0.1; // 10%
```

## Why This Matters

Next session, when AI reads your code:
1. Sees `@codesyncer-decision` → Knows WHY you chose Stripe
2. Sees `@codesyncer-inference` → Knows the reasoning behind values
3. Sees `@codesyncer-todo` → Knows what still needs confirmation

**Context survives across sessions. No more "why did we do this?"**

## Quick Reference

```
Inferred something?     → @codesyncer-inference: [reason]
Made a decision?        → @codesyncer-decision: [date] [what] [why]
Special rule?           → @codesyncer-rule: [explanation]
Need to confirm?        → @codesyncer-todo: [what to confirm]
Business context?       → @codesyncer-context: [domain knowledge]
```

## Learn More

- [Full Documentation](https://github.com/bitjaru/codesyncer)
- [Tag System Guide](https://github.com/bitjaru/codesyncer/blob/main/docs/TAGS.md)
- [Hooks Guide](https://github.com/bitjaru/codesyncer/blob/main/docs/HOOKS.md)
