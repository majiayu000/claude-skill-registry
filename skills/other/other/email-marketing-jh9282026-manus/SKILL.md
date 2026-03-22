---
name: email-marketing
description: "Master email marketing strategy, campaign creation, deliverability optimization, and automation. Use for: building email campaigns, improving deliverability, list segmentation, A/B testing, email design, compliance (CAN-SPAM, GDPR), automation workflows, and measuring email performance across promotional, transactional, and lifecycle emails."
---

# Email Marketing

Create high-performing email campaigns with optimal deliverability and engagement.

## Overview

This skill provides comprehensive guidance on email marketing strategy, campaign creation, deliverability optimization, list management, automation, compliance, and performance measurement to maximize email ROI.

## Email Strategy Framework

### Campaign Types

| Type | Purpose | Frequency | Key Metrics |
|------|---------|-----------|-------------|
| **Promotional** | Drive sales, announce offers | Weekly/bi-weekly | Revenue, conversion rate, ROAS |
| **Newsletter** | Educate, engage, build authority | Weekly/monthly | Open rate, CTR, engagement |
| **Transactional** | Confirm actions, provide info | Triggered | Delivery rate, open rate |
| **Lifecycle** | Nurture through journey stages | Automated sequences | Conversion rate, engagement |
| **Re-engagement** | Win back inactive subscribers | Quarterly | Reactivation rate, list health |

### List Building Strategies

**Opt-In Methods**:
- Website signup forms (header, footer, sidebar)
- Content upgrades and lead magnets
- Exit-intent popups
- Landing pages
- Social media lead ads
- In-store signups
- Webinar registrations
- Gated content

**Double Opt-In Benefits**:
- Higher quality subscribers
- Better engagement rates
- Improved deliverability
- GDPR compliance
- Reduced spam complaints

## Deliverability Optimization

### Authentication Setup

**SPF (Sender Policy Framework)**:
- Specifies authorized sending servers
- Prevents email spoofing
- Required for deliverability

**DKIM (DomainKeys Identified Mail)**:
- Adds digital signature to emails
- Verifies email integrity
- Prevents tampering

**DMARC (Domain-based Message Authentication)**:
- Builds on SPF and DKIM
- Sets policy for failed authentication
- Provides reporting
- Mandatory for bulk senders

### Sender Reputation Management

**Factors Affecting Reputation**:
- Bounce rates (keep <2%)
- Spam complaint rates (keep <0.1%)
- Engagement rates (opens, clicks)
- Email volume consistency
- List quality and hygiene

**List Hygiene Practices**:
- Remove hard bounces immediately
- Suppress soft bounces after 3-5 attempts
- Remove inactive subscribers (90-180 days)
- Validate email addresses at signup
- Monitor engagement metrics
- Implement re-engagement campaigns

## Email Design and Content

### Design Best Practices

**Mobile Optimization** (60%+ opens on mobile):
- Single column layout
- Minimum 14px font size
- Large, tappable buttons (44x44px minimum)
- Compressed images
- Responsive design

**Visual Hierarchy**:
1. Logo/branding
2. Hero image or headline
3. Primary message
4. Call-to-action button
5. Supporting content
6. Footer

### Subject Line Optimization

**Best Practices**:
- 40-50 characters optimal
- Front-load important words
- Create curiosity or urgency
- Personalize when relevant
- Avoid spam triggers
- Test emoji usage

**Formulas That Work**:
- Question: "Ready to [achieve goal]?"
- Benefit: "Get [benefit] in [timeframe]"
- Urgency: "[Offer] ends [date/time]"
- Curiosity: "The secret to [desired outcome]"

### Email Copywriting

**Structure**:
1. **Preheader**: Complement subject line
2. **Opening**: Hook reader immediately
3. **Body**: Clear, scannable, benefit-focused
4. **CTA**: Single, clear action
5. **P.S.**: Reinforce offer

**Copywriting Principles**:
- Write conversationally
- Focus on benefits, not features
- Use "you" language
- Keep paragraphs short (2-3 lines)
- Use bullet points for scannability

## Segmentation and Personalization

### Segmentation Strategies

**Demographic Segmentation**:
- Age, gender, location
- Job title, industry (B2B)
- Income level

**Behavioral Segmentation**:
- Purchase history
- Browse behavior
- Email engagement
- Cart abandonment
- Lifecycle stage

**RFM Segmentation** (Ecommerce):
- **Recency**: When did they last purchase?
- **Frequency**: How often do they purchase?
- **Monetary**: How much do they spend?

### Personalization Tactics

**Basic Personalization**:
- First name in subject/body
- Location-based content
- Company name (B2B)
- Birthday/anniversary

**Advanced Personalization**:
- Dynamic content blocks
- Product recommendations
- Behavioral triggers
- Predictive content
- Send-time optimization

## Email Automation

### Essential Automated Workflows

**Welcome Series** (3-5 emails):
1. Immediate: Welcome + brand intro
2. Day 2: Value proposition
3. Day 5: Social proof
4. Day 8: Product overview
5. Day 12: Special offer

**Abandoned Cart** (3 emails):
1. 1 hour: Reminder
2. 24 hours: Add urgency
3. 3 days: Discount offer

**Post-Purchase**:
1. Order confirmation
2. Shipping notification
3. Delivery + usage tips
4. Review request
5. Cross-sell/upsell

**Win-Back** (inactive 90+ days):
1. "We miss you" message
2. Special offer
3. Preference center

## Compliance and Privacy

### CAN-SPAM Act (US)

**Requirements**:
- Accurate header information
- Non-deceptive subject lines
- Identify as advertisement
- Include physical address
- Provide opt-out mechanism
- Honor opt-outs within 10 days

### GDPR (EU)

**Key Requirements**:
- Explicit consent
- Clear purpose for data collection
- Right to access and delete data
- Data portability
- Breach notification (72 hours)

### Best Practices

- Double opt-in
- Clear privacy policy
- Easy unsubscribe
- Preference center
- Transparent data usage
- Regular list cleaning

## Email Analytics

### Key Metrics

**Deliverability**:
- Delivery rate: >95%
- Bounce rate: <2%
- Spam complaint rate: <0.1%

**Engagement**:
- Open rate: 15-25%
- Click-through rate: 2-5%
- Click-to-open rate: 10-20%
- Conversion rate: 1-5%

**Revenue**:
- Revenue per email
- Revenue per subscriber
- Email-attributed revenue
- ROI

### A/B Testing

**What to Test**:
- Subject lines
- From name
- Send time/day
- Email content
- CTA copy and design
- Personalization

**Testing Methodology**:
1. Form hypothesis
2. Minimum 1,000 per variant
3. Send simultaneously
4. Measure statistical significance
5. Implement winner
6. Document learnings

## Using the Reference Files

### When to Read Each Reference

**`/references/deliverability-deep-dive.md`** — Read when troubleshooting deliverability issues, setting up authentication, or improving sender reputation.

**`/references/campaign-templates.md`** — Read when creating specific campaign types with proven templates and examples.

**`/references/automation-workflows.md`** — Read when building advanced automation sequences or behavioral triggers.

**`/references/compliance-guide.md`** — Read when ensuring compliance with CAN-SPAM, GDPR, CASL, or other email regulations.
