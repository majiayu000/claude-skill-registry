---
name: email-marketing
description: Activate for email campaigns, newsletters, drip sequences, automation flows, and email copywriting. Use when creating email content, designing automation workflows, or optimizing email performance.
license: MIT
---

# Email Marketing

Email campaign creation, automation workflows, and performance optimization.

## When to Use

- Email campaign creation
- Newsletter design
- Drip sequence building
- Automation flow design
- Email copywriting
- A/B testing strategy
- Deliverability optimization

## Core Capabilities

### Email Types & Templates
Load: `references/email-templates.md`

### Automation Workflows
Load: `references/automation-flows.md`

### Subject Line Formulas
Load: `references/subject-line-formulas.md`

### Deliverability Best Practices
Load: `references/deliverability-checklist.md`

## Quick Reference

**Key Metrics:**
- Open Rate: 15-25% average
- Click Rate: 2-5% average
- Unsubscribe: <0.5% target
- Bounce: <2% target

**Email Types:**
- Newsletter (weekly/monthly updates)
- Promotional (offers, sales)
- Transactional (receipts, confirmations)
- Drip/Nurture (automated sequences)
- Re-engagement (win-back)

## Workflow

### Campaign Creation
1. Define goal and audience segment
2. Choose email type/template
3. Write subject line (test 3-5 variants)
4. Create body copy with clear CTA
5. Design/add visuals
6. Set up tracking
7. Test across devices
8. Schedule optimal send time

### Automation Setup
1. Define trigger event
2. Map customer journey
3. Create email sequence
4. Set timing/delays
5. Add decision branches
6. Configure exit conditions
7. Test flow end-to-end

## Output Format

```markdown
## Email: [Campaign Name]

**Type:** [newsletter/promotional/drip/transactional]
**Segment:** [target audience]
**Goal:** [metric to improve]

### Subject Lines (A/B Test)
A: [subject]
B: [subject]

### Preview Text
[preheader]

### Body
[email copy with formatting]

### CTA
[button text + link]
```

## Report Output

**Activate:** `assets-organizing` skill for report file paths

Email reports go to `assets/reports/email/{date}-{campaign}-report.md`

## Agent Integration

**Primary Agents:** email-specialist, nurture-specialist, content-creator

**Skill Dependencies:** content-marketing, analytics, assets-organizing (report organization)

## Best Practices

1. Mobile-first design (60%+ open on mobile)
2. One primary CTA per email
3. Personalize beyond first name
4. Test send times for your audience
5. Clean list quarterly (remove inactive)
6. Respect unsubscribe immediately
