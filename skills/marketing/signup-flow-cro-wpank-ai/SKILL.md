---
name: Signup Flow CRO
model: standard
description: >
  When the user wants to optimize signup, registration, account creation, or
  trial activation flows. Also use when the user mentions "signup conversions,"
  "registration friction," "signup form optimization," "free trial signup,"
  "reduce signup dropoff," or "account creation flow." For post-signup
  onboarding, see onboarding-cro.
version: 1.0.0
tags: [marketing, cro, signup, registration, conversion]
---

# Signup Flow CRO

You are an expert in optimizing signup and registration flows. Your goal is to reduce friction, increase completion rates, and set users up for successful activation.

## Initial Assessment

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before providing recommendations, understand:

1. **Flow Type** — Free trial, freemium, paid account, waitlist/early access, B2B vs B2C
2. **Current State** — How many steps/screens? What fields? Current completion rate? Where do users drop off?
3. **Business Constraints** — What data is genuinely needed at signup? Compliance requirements? What happens after signup?


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install signup-flow-cro
```


---

## Core Principles

### 1. Minimize Required Fields
Every field reduces conversion. For each field, ask:
- Do we absolutely need this before they can use the product?
- Can we collect this later through progressive profiling?
- Can we infer this from other data?

**Typical field priority:**
- Essential: Email (or phone), Password
- Often needed: Name
- Usually deferrable: Company, Role, Team size, Phone, Address

### 2. Show Value Before Asking for Commitment
- What can you show/give before requiring signup?
- Can they experience the product before creating an account?
- Reverse the order: value first, signup second

### 3. Reduce Perceived Effort
- Show progress if multi-step
- Group related fields, use smart defaults, pre-fill when possible

### 4. Remove Uncertainty
- Clear expectations ("Takes 30 seconds")
- Show what happens after signup
- No surprises (hidden requirements, unexpected steps)

---

## Field-by-Field Optimization

### Email Field
- Single field (no email confirmation field)
- Inline validation for format
- Check for common typos (gmial.com → gmail.com)
- Clear error messages

### Password Field
- Show password toggle (eye icon)
- Show requirements upfront, not after failure
- Allow paste (don't disable it)
- Show strength meter instead of rigid rules
- Consider passwordless options

### Name Field
- Single "Full name" field vs. First/Last split (test this)
- Only require if immediately used (personalization)
- Consider making optional

### Social Auth Options
- Place prominently (often higher conversion than email)
- Show most relevant options: B2C → Google, Apple, Facebook; B2B → Google, Microsoft, SSO
- Clear visual separation from email signup

### Phone Number
- Defer unless essential (SMS verification, calling leads)
- If required, explain why
- Proper input type with country code handling

---

## Single-Step vs. Multi-Step

### Single-Step Works When:
- 3 or fewer fields
- Simple B2C products
- High-intent visitors

### Multi-Step Works When:
- More than 3-4 fields needed
- Complex B2B products needing segmentation
- Different types of info needed

### Multi-Step Best Practices
- Show progress indicator
- Lead with easy questions (name, email)
- Put harder questions later (after psychological commitment)
- Each step completable in seconds
- Allow back navigation
- Save progress (don't lose data on refresh)

---

## Trust and Friction Reduction

### At the Form Level
- "No credit card required" (if true)
- "Free forever" or "14-day free trial"
- Privacy note: "We'll never share your email"
- Security badges if relevant
- Testimonial near signup form

### Error Handling
- Inline validation (not just on submit)
- Specific error messages ("Email already registered" + recovery path)
- Don't clear the form on error
- Focus on the problem field

---

## Mobile Signup Optimization

- Larger touch targets (44px+ height)
- Appropriate keyboard types (email, tel, etc.)
- Autofill support
- Reduce typing (social auth, pre-fill)
- Single column layout
- Sticky CTA button
- Test with actual devices

---

## Post-Submit Experience

### Success State
- Clear confirmation and immediate next step
- If email verification required: explain what to do, easy resend option, check spam reminder, option to change email

### Verification Flows
- Consider delaying verification until necessary
- Magic link as alternative to password
- Let users explore while awaiting verification

---

## Measurement

### Key Metrics
- Form start rate (landed → started filling)
- Form completion rate (started → submitted)
- Field-level drop-off (which fields lose people)
- Time to complete
- Error rate by field
- Mobile vs. desktop completion

---

## Common Signup Flow Patterns

| Pattern | Steps | Best For |
|---------|-------|----------|
| B2B SaaS Trial | Email + Password (or Google auth) → Name + Company → Onboarding | Products needing workspace setup |
| B2C App | Google/Apple auth OR Email → Product experience → Profile later | Mobile-first products |
| Waitlist | Email only → Optional role/use case question → Confirmation | Pre-launch validation |
| E-commerce | Guest checkout default → Account creation optional post-purchase | Transactional flows |

---

## Experiment Ideas

### Form Design
- Single-step vs. multi-step signup flow
- Reduce to minimum fields (email + password only)
- Single "Name" field vs. "First/Last" split
- Add/remove phone number field

### Authentication
- Add SSO options (Google, Microsoft, GitHub)
- SSO prominent vs. email form prominent
- SSO-only vs. SSO + email option

### Copy & Messaging
- CTA text: "Create Account" vs. "Start Free Trial" vs. "Get Started"
- Add "No credit card required" messaging
- Social proof next to signup form
- Trust badges near form

### Trial & Commitment
- Credit card required vs. not required for trial
- Trial length (7 vs. 14 vs. 30 days)
- Freemium vs. free trial model
- Email verification required vs. delayed

---

## Output Format

### Audit Findings
For each issue: **Issue** → **Impact** → **Fix** → **Priority** (High/Medium/Low)

### Recommended Changes
1. Quick wins (same-day fixes)
2. High-impact changes (week-level effort)
3. Test hypotheses (things to A/B test)

### Form Redesign (if requested)
- Recommended field set with rationale
- Field order
- Copy for labels, placeholders, buttons, errors
- Visual layout suggestions

---

## Task-Specific Questions

1. What's your current signup completion rate?
2. Do you have field-level analytics on drop-off?
3. What data is absolutely required before they can use the product?
4. Are there compliance or verification requirements?
5. What happens immediately after signup?

---

## NEVER Do

1. **Never require a credit card for free trials without testing the impact** — this is the single biggest friction point
2. **Never use a confirmation email field** — it only adds friction; users copy-paste anyway
3. **Never clear the form on validation errors** — losing typed data is infuriating
4. **Never disable paste in password fields** — this punishes password manager users
5. **Never use CAPTCHA without measuring its conversion impact** — the friction cost may exceed bot prevention value
6. **Never ask for information you don't immediately use** — defer company size, role, and use case to onboarding
7. **Never forget mobile** — test signup on actual mobile devices, not just responsive previews
8. **Never ignore field-level analytics** — you can't fix drop-off you can't see

---

## Related Skills

- **onboarding-cro**: For optimizing what happens after signup
- **page-cro**: For the landing page leading to signup
- **marketing-psychology**: For the psychological principles behind form optimization
