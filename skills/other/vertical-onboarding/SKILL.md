---
name: vertical-onboarding
description: Onboarding-and-switching playbook for SMB Product-Builder products. Defines the first-run experience that turns a prospect leaving an incumbent (ServiceTitan/Toast/Mindbody/Shopify/QuickBooks) into an activated user — import-first onboarding, the activation milestone, sample-data fallback, and the time-to-first-value target. Applied by migration-import-engineer and architect/pm so onboarding is designed as a funnel, not an afterthought. Our whole wedge is "low switching cost"; this skill makes that real on day one.
when_to_use: |
  Apply when:
  - migration-import-engineer designs the import that feeds first-run
  - architect/pm specs the first-run / activation flow for a new product
  - a product's adoption depends on leaving an incumbent (any of the 40 products)
  Do NOT apply for internal tools with no external onboarding.
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/migration/**"
  - "docs/architecture/**"
  - "docs/design/**"
---

# Vertical onboarding — switch them in, to first value, fast

The incumbent's moat is switching cost. Our wedge is dissolving it. Onboarding is where
that promise is kept or broken. **Design onboarding as a funnel with one activation
milestone, import-first.**

## 1. Import-first, not blank-slate

The default first-run path is **"bring your data from {incumbent}"**, powered by
`migration-import-engineer`'s import contract — not an empty dashboard the user must fill
by hand. A new user should see *their own* customers/jobs/menu/listings within minutes.

- Offer the import on screen one, with the named incumbent ("Import from ServiceTitan").
- Run it as a dry-run preview the user approves (the import contract's operator step).
- Provide a **sample-data fallback** ("Explore with example data") for users who can't
  export yet — never a dead empty state.

## 2. One activation milestone (define it per product)

Pick the single action that means "this user got value" — the north-star of onboarding.
Everything in first-run drives toward it. Examples:

| product | activation milestone |
|---|---|
| quoting (home services) | sent first priced quote |
| online-ordering (restaurants) | published menu + took first test order |
| class-booking (fitness) | imported members + first class booked |
| inventory (retail) | synced catalog + first reorder rule set |
| transaction-coordination (real estate) | first transaction checklist created |
| sponsorship-crm (creator) | first sponsor + deal stage |

Measure **time-to-first-value (TTFV)**; target minutes, not days. State the target in the
architecture doc.

## 3. The onboarding funnel (spec these steps)

```
1. Identify incumbent → 2. Import (dry-run → approve) → 3. Verify own data
→ 4. Complete the one setup the product needs → 5. Activation milestone → 6. Invite team
```

Each step: a clear single CTA, skippable where safe, resumable, and with progress shown.
Defer everything not on the path to the activation milestone.

## 4. Reduce setup to the minimum

- Pre-fill from imported data wherever possible (branding from the website, hours from the
  listing, tax rate from the address).
- Sensible defaults over required choices; advanced config lives in settings, not onboarding.
- One required integration max before activation (e.g. Stripe for quoting) — sequence the
  rest after first value.

## 5. Trust + reversibility

- Show what was imported and let the user undo a batch (ties to the import contract's
  rollback) — trust comes from "you can't break anything."
- Don't ask for payment details before the activation milestone unless the product is
  charge-to-use.

## Output

When applied, contribute an **Onboarding** section to the architecture or design doc:

```
## Onboarding
- incumbent(s): <names> → import via docs/migration/IMPORT-{slug}.md
- activation milestone: <the one action>
- TTFV target: <minutes>
- funnel: identify → import(dry-run→approve) → verify → setup → activate → invite
- empty-state fallback: sample data
- required-before-activation: <≤1 integration>
```
