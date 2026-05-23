---
name: nav-sop
description: Create Standard Operating Procedures after solving novel issues, establishing patterns, or documenting workflows. Use when user says "document this solution", "save this for next time", "create SOP".
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# Navigator SOP Creator Skill

Create Standard Operating Procedures (SOPs) - reusable documentation for processes, integrations, debugging solutions, and workflows.

## When to Invoke

Invoke this skill when the user:
- Says "document this solution", "save this for next time"
- Says "create SOP", "make this reusable"
- Solves a novel issue and mentions "don't want to hit this again"
- Sets up integration and says "document the setup"
- Establishes pattern and mentions "team should follow this"

**DO NOT invoke** if:
- Creating task documentation (use nav-task skill)
- Updating architecture docs (different purpose)
- Simple bug fix with no reusable pattern

## Execution Steps

### Step 1: Determine SOP Category

Ask user which category (or infer from context):

**Categories**:
1. **integrations** - Third-party service setups
2. **debugging** - Common issues & solutions
3. **development** - Dev workflows, patterns
4. **deployment** - Deploy procedures, CI/CD

**Examples**:
- "How to set up Stripe webhooks" → `integrations/`
- "Fixing CORS errors" → `debugging/`
- "Testing authenticated routes" → `development/`
- "Deploy to production" → `deployment/`

### Step 2: Determine SOP Name

**If user provided name**:
- Use their name (sanitize: lowercase, hyphens)
- Example: "Stripe Payment Setup" → "stripe-payment-setup"

**If no name provided**:
- Generate from context: `{service}-{action}`
- Example: "github-oauth-integration"
- Example: "cors-proxy-errors"

### Step 3: Check if SOP Already Exists

Check existing SOPs in category:

```bash
ls .agent/sops/{category}/*.md 2>/dev/null
```

**If similar SOP exists**:
```
⚠️  Similar SOP found:
   .agent/sops/{category}/{similar-name}.md

Options:
1. Read existing SOP (don't duplicate)
2. Update existing SOP (add to it)
3. Create new SOP (different enough)

Your choice [1-3]:
```

### Step 4: Generate SOP Content

Create SOP document from conversation:

```markdown
# {SOP Title}

**Category**: {integrations|debugging|development|deployment}
**Created**: {YYYY-MM-DD}
**Last Updated**: {YYYY-MM-DD}

---

## Context

**When to use this SOP**:
[Describe the scenario where this applies]

**Problem it solves**:
[What issue does this address?]

**Prerequisites**:
- [Requirement 1]
- [Requirement 2]

---

## The Problem

### Symptoms
[What does the issue look like?]
- Error message: `{specific error}`
- Behavior: [Unexpected behavior]
- Impact: [What breaks]

### Root Cause
[Why does this happen? Technical explanation]

---

## The Solution

### Step 1: {Action}

**Do this**:
```bash
# Command or code
npm install stripe
```

**Why**:
[Explanation of what this accomplishes]

**Expected output**:
```
+ stripe@12.0.0
added 1 package
```

### Step 2: {Next Action}

**Do this**:
```typescript
// Code example
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
```

**Why**:
[Explanation]

**Configuration**:
Add to `.env`:
```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Step 3: {Continue...}
...

---

## Complete Example

### Full Working Code

**File**: `src/services/stripe.ts`
```typescript
import Stripe from 'stripe';

export class StripeService {
  private stripe: Stripe;

  constructor() {
    this.stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
      apiVersion: '2023-10-16',
    });
  }

  async createPaymentIntent(amount: number) {
    return await this.stripe.paymentIntents.create({
      amount: amount * 100, // Convert to cents
      currency: 'usd',
    });
  }
}
```

**File**: `src/routes/webhook.ts`
```typescript
export async function handleStripeWebhook(req: Request, res: Response) {
  const sig = req.headers['stripe-signature'];

  try {
    const event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!
    );

    // Handle event
    switch (event.type) {
      case 'payment_intent.succeeded':
        // Process successful payment
        break;
    }

    res.json({ received: true });
  } catch (err) {
    res.status(400).send(`Webhook Error: ${err.message}`);
  }
}
```

---

## Testing

### Verify It Works

**Test 1: Create payment intent**
```bash
curl -X POST http://localhost:3000/api/create-payment \
  -H "Content-Type: application/json" \
  -d '{"amount": 10}'
```

**Expected result**:
```json
{
  "clientSecret": "pi_xxx_secret_yyy"
}
```

**Test 2: Webhook delivery**
```bash
stripe listen --forward-to localhost:3000/webhook
```

**Expected result**:
```
Ready! You are using Stripe API Version [2023-10-16]
```

---

## Prevention

**How to avoid this issue in future**:
- [Prevention strategy 1]
- [Prevention strategy 2]

**Red flags to watch for**:
- [Warning sign 1]
- [Warning sign 2]

---

## Troubleshooting

### Issue: Webhook signature verification fails

**Symptoms**:
```
Error: No signatures found matching the expected signature
```

**Cause**: Webhook secret mismatch or body already parsed

**Fix**:
```typescript
// Use raw body for webhook verification
app.post('/webhook', express.raw({type: 'application/json'}), handleStripeWebhook);
```

### Issue: Payment amount incorrect

**Symptoms**: Charged wrong amount

**Cause**: Forgot to convert to cents

**Fix**: Always multiply by 100 for Stripe amounts

---

## Related Documentation

**Stripe Docs**:
- [Payment Intents API](https://stripe.com/docs/api/payment_intents)
- [Webhooks Guide](https://stripe.com/docs/webhooks)

**Our Docs**:
- Task: `.agent/tasks/TASK-04-stripe-integration.md`
- System: `.agent/system/project-architecture.md` (payments section)

**External**:
- [Stripe Testing Cards](https://stripe.com/docs/testing)

---

## Maintenance Notes

**Update when**:
- Stripe API version changes
- Payment flow changes
- New webhook events added

**Owner**: [Team or person responsible]

---

**Last Updated**: {YYYY-MM-DD}
**Tested With**: Stripe API v2023-10-16, Node.js v18+
```

### Step 5: Save SOP File

Write to appropriate category:

```
Write(
  file_path: ".agent/sops/{category}/{name}.md",
  content: [generated SOP]
)
```

Filename: `.agent/sops/{category}/{name}.md`

### Step 6: Update Navigator Index

Edit `.agent/DEVELOPMENT-README.md` to add SOP to index:

```markdown
## Standard Operating Procedures

### Integrations
- **{Service}**: `.agent/sops/integrations/{name}.md` - {One-line description}

### Debugging
- **{Issue}**: `.agent/sops/debugging/{name}.md` - {Description}

### Development
...

### Deployment
...
```

### Step 7: Link to Related Task (If Applicable)

If SOP came from specific task, add reference:

**In task doc**:
```markdown
## Related SOPs

- `.agent/sops/integrations/stripe-payment-setup.md`
```

**In SOP**:
```markdown
## Related Documentation

- Task: `.agent/tasks/TASK-04-stripe-integration.md`
```

Cross-linking helps discoverability.

### Step 8: Confirm Success

Show completion message:

```
✅ SOP created successfully!

Title: {SOP Title}
Category: {category}
File: .agent/sops/{category}/{name}.md
Size: {X} KB (~{Y} tokens)

📚 SOP includes:
- Problem description & symptoms
- Step-by-step solution
- Complete code examples
- Testing instructions
- Troubleshooting guide

🔗 Navigator index updated
[If linked: Linked to TASK-{XX}]

To reference later:
Read .agent/sops/{category}/{name}.md
```

## SOP Categories Explained

### 1. integrations/
**Purpose**: How to set up third-party services

**Examples**:
- `stripe-payment-setup.md`
- `github-oauth-integration.md`
- `sendgrid-email-config.md`
- `redis-session-store.md`

**Structure**: Setup steps + Configuration + Testing

### 2. debugging/
**Purpose**: How to solve common issues

**Examples**:
- `cors-proxy-errors.md`
- `jwt-token-expiration.md`
- `database-connection-timeout.md`
- `build-errors-typescript.md`

**Structure**: Symptoms + Root cause + Fix + Prevention

### 3. development/
**Purpose**: Development workflows & patterns

**Examples**:
- `testing-authenticated-routes.md`
- `adding-new-api-endpoint.md`
- `database-migration-workflow.md`
- `component-testing-patterns.md`

**Structure**: When to use + Steps + Example + Best practices

### 4. deployment/
**Purpose**: Deploy, CI/CD, infrastructure

**Examples**:
- `deploy-to-production.md`
- `rollback-failed-deploy.md`
- `setup-github-actions.md`
- `environment-variables.md`

**Structure**: Prerequisites + Steps + Verification + Rollback

## Common Use Cases

### After Solving Tricky Bug
```
User: "Finally fixed CORS issue, save this so we don't hit it again"
→ Creates: .agent/sops/debugging/cors-proxy-errors.md
→ Captures: Error, root cause, fix, prevention
→ Team won't repeat mistake
```

### After Integration Setup
```
User: "Stripe webhooks working, document the setup"
→ Creates: .agent/sops/integrations/stripe-webhooks.md
→ Captures: All config steps, code, testing
→ Next integration is copy-paste
```

### Establishing Team Pattern
```
User: "Document how we test protected routes"
→ Creates: .agent/sops/development/testing-auth-routes.md
→ Captures: Pattern, examples, best practices
→ Team follows consistent approach
```

## Error Handling

**Category directory doesn't exist**:
```
Creating category: .agent/sops/{category}/
✅ Directory created
```

**SOPs directory missing entirely**:
```
❌ Navigator not initialized

Run /nav:init to create .agent/ structure.
```

**Duplicate SOP name**:
```
⚠️  SOP already exists: {name}.md

Options:
1. Read existing (don't duplicate)
2. Update existing (add new info)
3. Rename new SOP ({name}-v2.md)

Your choice [1-3]:
```

## Success Criteria

SOP creation is successful when:
- [ ] SOP file created in correct category
- [ ] Contains all required sections
- [ ] Includes working code examples
- [ ] Testing instructions provided
- [ ] Navigator index updated
- [ ] Linked to related task (if applicable)

## Scripts

**generate_sop.py**: Create SOP from conversation
- Input: Conversation, category, name
- Output: Formatted SOP markdown

## Best Practices

**Good SOP names**:
- `stripe-payment-integration` (specific, descriptive)
- `cors-proxy-configuration` (clear purpose)
- `jwt-token-refresh` (explains what)

**Bad SOP names**:
- `fix` (too vague)
- `integration` (not specific)
- `sop1` (meaningless)

**When to create SOPs**:
- ✅ Solved novel issue (will happen again)
- ✅ Set up integration (reusable process)
- ✅ Established pattern (team should follow)
- ✅ Complex workflow (needs documentation)
- ❌ One-off bug (not reusable)
- ❌ Obvious solution (don't over-document)

**SOP quality checklist**:
- [ ] Clear problem description
- [ ] Step-by-step solution
- [ ] Complete code examples (copy-paste ready)
- [ ] Testing instructions
- [ ] Troubleshooting common issues

## Notes

SOPs are **living documents**:
- Created when pattern established
- Updated when solution improves
- Referenced frequently by team
- Prevent repeated mistakes

They transform:
- Individual knowledge → Team knowledge
- One-time solution → Reusable process
- Tribal knowledge → Documented procedure

**Impact**: Zero repeated mistakes over time

This skill provides same functionality as `/nav:doc sop` command but with natural language invocation.
