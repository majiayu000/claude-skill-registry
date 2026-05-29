---
name: stripe-webhook-code-generator
description: Generate production-ready Stripe webhook handlers that integrate with existing codebases. Analyzes project structure, matches code style, integrates with database/email/logging systems, and creates tests. Use for generating or updating webhook code, not for debugging webhooks (use stripe-webhook-debugger for that).
---

# Stripe Webhook Code Generator

Generates production-ready Stripe webhook handlers that seamlessly integrate with existing projects. Analyzes codebase to match patterns, conventions, and architecture.

## When to Use This Skill

Use this skill when you need to:
- ✅ Generate webhook handler code for your project
- ✅ Add new event handlers to existing webhooks
- ✅ Update/refactor webhook handling code
- ✅ Create tests for webhook handlers
- ✅ Integrate webhooks with database/email/logging

**For debugging webhooks:** Use "stripe-webhook-debugger" skill instead.

## Core Workflow

### Step 1: Analyze Codebase

**Before generating any code, analyze:**

1. **Framework and language**
   - Look for: package.json, requirements.txt, Gemfile
   - Identify: Next.js, Express, FastAPI, Django, Rails, etc.
   - Check: TypeScript vs JavaScript, Python version

2. **Project structure**
   - API routes location: /app/api, /pages/api, /routes, /controllers
   - Naming conventions: kebab-case, camelCase, snake_case
   - File organization patterns

3. **Existing Stripe integration**
   - Search for Stripe imports
   - Check if Stripe SDK installed
   - Find API key configuration
   - Look for existing webhook handlers
   - Check Stripe API version

4. **Project patterns**
   - Error handling: try/catch, error classes, middleware
   - Logging: console, Winston, Pino, Python logging
   - Database: Prisma, TypeORM, SQLAlchemy, ActiveRecord
   - Authentication: NextAuth, Passport, custom
   - Environment variable access

5. **Relevant models/schemas**
   - User/Customer model
   - Subscription model
   - Payment/Order model
   - Relationship to Stripe IDs

### Step 2: Ask Clarifying Questions

**Essential questions:**
1. Which events do you need to handle?
2. What should happen when events fire?
3. Do you have existing models for users/subscriptions/payments?
4. Email notifications needed?

### Step 3: Generate Integrated Code

**Code generation principles:**

1. **Match existing style** - Indentation, naming, imports, async patterns
2. **Integrate with infrastructure** - Error handling, logging, database
3. **Security by default** - Signature verification, env vars, validation
4. **Production ready** - Error handling, logging, idempotency, comments
5. **Maintainable** - Clear structure, reusable functions, well-named

### Step 4: Generate Supporting Files

**Always generate:**
1. Main webhook handler
2. Environment variables (.env.example)
3. Setup documentation

**Generate when applicable:**
4. Test files
5. Type definitions (TypeScript)
6. Database migrations
7. Email templates

## Framework Quick Reference

### Next.js App Router
**Location:** `/app/api/webhooks/stripe/route.ts`

**Key pattern:**
```typescript
import { headers } from 'next/headers';
export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  const body = await req.text();  // Raw
  const sig = headers().get('stripe-signature');
}
```

### Express
**Location:** `/src/routes/webhooks.ts`

**Key pattern:**
```typescript
router.post('/stripe',
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    // req.body is Buffer
  }
);
```

### FastAPI
**Location:** `/app/routers/webhooks.py`

**Key pattern:**
```python
@router.post("/stripe")
async def webhook(request: Request):
    payload = await request.body()  # bytes
```

Full framework examples in [references/frameworks/](references/frameworks/)

## Database Integration

### Prisma Example
```typescript
await prisma.subscription.create({
  data: {
    stripeSubscriptionId: sub.id,
    status: sub.status,
    currentPeriodEnd: new Date(sub.current_period_end * 1000),
    user: { connect: { stripeCustomerId: sub.customer } }
  }
});
```

### SQLAlchemy Example
```python
subscription = Subscription(
    stripe_id=sub['id'],
    status=sub['status'],
    current_period_end=datetime.fromtimestamp(sub['current_period_end'])
)
db.add(subscription)
db.commit()
```

## Code Quality Checklist

Before presenting code, verify:
- ✅ Signature verification implemented
- ✅ Raw body used (not parsed)
- ✅ Environment variables for secrets
- ✅ Idempotency check included
- ✅ Error handling comprehensive
- ✅ Logging for debugging
- ✅ Matches project patterns
- ✅ Integrates with database
- ✅ Comments explain critical sections
- ✅ Test file generated
- ✅ Setup documentation provided

## Communication Style

**Be context-aware:**
```
"Looking at your codebase:
- Next.js 14 App Router
- Prisma with Subscription model
- Resend for emails

I'll generate code matching these patterns."
```

**Explain integrations:**
```
"Key integration points:
- Line 45: Updates your Subscription model
- Line 62: Uses your Resend email config
- Line 78: Follows your error handling pattern"
```

**Provide complete setup:**
```
"Generated files:
1. /app/api/webhooks/stripe/route.ts
2. .env.example (updated)
3. route.test.ts (tests)
4. STRIPE_SETUP.md (guide)

Test with: stripe listen --forward-to localhost:3000/api/webhooks/stripe"
```

## Example Workflow

**User:** "I need to handle subscription payments"

**Claude:**
1. Analyzes codebase (Next.js, Prisma, TypeScript)
2. Asks: "Which events? (invoice.paid, subscription.created?)"
3. Asks: "Should I integrate with your Subscription model?"
4. Generates complete handler with:
   - Signature verification
   - Event routing
   - Database updates
   - Email notifications (if requested)
   - Tests
   - Documentation
5. Explains where files go and how to test

## References

Detailed framework examples and patterns:
- [references/code-templates.md](references/code-templates.md)
- [references/testing-patterns.md](references/testing-patterns.md)

## Success Criteria

User has successfully integrated webhooks when:
- ✅ Handler matches project structure
- ✅ Code integrates with database
- ✅ Signature verification implemented
- ✅ Error handling matches patterns
- ✅ Tests generated and pass
- ✅ Documentation is clear
- ✅ Environment variables documented
- ✅ Handler ready to deploy
