---
name: proposalwriter
description: "Client brief in, polished proposal out. Takes project requirements and generates structured proposals with scope, timeline, pricing, and terms. Use when: responding to RFPs, quoting projects, or creating service agreements. NOT for: legal contracts (needs lawyer review), automated bidding, or mass proposal generation."
homepage: https://pawhub.ai/proposalwriter
metadata:
  {
    "openpaw":
      {
        "emoji": "📝",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/proposalwriter",
              "bins": ["proposalwriter"],
              "label": "Install ProposalWriter (npm)",
            },
          ],
      },
  }
---

# ProposalWriter 📝

Turn rough project notes into polished proposals. Scope, timeline, pricing, terms — all formatted professionally in minutes.

## When to Use

✅ **USE when:**

- Responding to RFPs
- Quoting freelance projects
- Creating service agreements
- Estimating project costs
- Drafting SOWs (statements of work)
- Proposal writing for agencies

## When NOT to Use

❌ **DON'T use when:**

- Legal contracts → needs lawyer review
- Binding agreements → require legal counsel
- Automated bidding → proposals should be thoughtful
- Mass generation → each proposal should be custom

## Example Interactions

**You:** Create proposal: client wants e-commerce site, Shopify, custom theme, 6 products, launch in 4 weeks, budget $8k

**Paw:** *analyzing requirements*

Got it. Building proposal for Shopify e-commerce site.

**Detected scope:**
- Platform: Shopify
- Custom theme development
- 6 products setup
- Timeline: 4 weeks
- Budget: $8,000

**Generating proposal...**

*30 seconds later*

✅ **Proposal ready**

**Preview:**

---

# E-commerce Website Development Proposal

## Project Overview

This proposal outlines the development of a custom Shopify e-commerce website for [Client Name]. The project includes custom theme development, product catalog setup, and full launch support.

## Scope of Work

### Phase 1: Discovery & Planning (Week 1)
- Client kickoff meeting
- Brand guidelines review
- Site architecture planning
- Design mockups (3 concepts)

### Phase 2: Development (Weeks 2-3)
- Custom Shopify theme development
- Responsive design (mobile, tablet, desktop)
- Product catalog setup (6 products)
- Payment gateway integration
- Shipping configuration

### Phase 3: Testing & Launch (Week 4)
- Quality assurance testing
- Client training session
- DNS configuration
- Launch support

## Deliverables

✅ Custom Shopify theme
✅ 6 products configured with images and descriptions
✅ Mobile-responsive design
✅ Payment processing setup
✅ Basic SEO optimization
✅ 2 rounds of revisions
✅ 30 days post-launch support

## Timeline

**Total Duration:** 4 weeks

- Week 1: Discovery & Design
- Weeks 2-3: Development
- Week 4: Testing & Launch
- Target Launch Date: [Date]

## Investment

**Total Project Cost:** $8,000

**Payment Schedule:**
- 50% deposit ($4,000) — upon proposal acceptance
- 25% milestone ($2,000) — design approval (Week 1)
- 25% final ($2,000) — upon launch

## Terms & Conditions

- All work covered under standard service agreement
- Client provides content (product descriptions, images)
- Additional features outside scope billed at $150/hour
- Domain and hosting fees not included

## Next Steps

1. Review and approve proposal
2. Sign service agreement
3. Submit 50% deposit
4. Schedule kickoff meeting

---

**Proposal stats:**
- Length: ~800 words
- Reading time: 3 minutes
- Professional tone: ✅
- Clear pricing: ✅
- Defined scope: ✅

**Want to:**
- Edit sections? (scope, pricing, timeline)
- Add client details? (name, logo)
- Export? (PDF, Word, Google Docs)
- Send? (email integration)

What do you want to do? 📝

---

**You:** Add payment terms: Net 15 on milestones

**Paw:** ✅ **Updated payment terms**

**Payment Schedule:**
- 50% deposit ($4,000) — upon proposal acceptance
- 25% milestone ($2,000) — design approval, Net 15
- 25% final ($2,000) — upon launch, Net 15

Terms section updated. Ready to export? 💼

---

**You:** Export to PDF and email to client@example.com

**Paw:** *generating PDF*

✅ **PDF generated**
✅ **Email sent** to client@example.com

**Email:**
```
Subject: E-commerce Website Development Proposal

Hi [Client Name],

Attached is the proposal for your Shopify e-commerce project.

I've outlined the scope, timeline, and pricing based on our discussion. The total investment is $8,000 with a 4-week timeline.

Let me know if you have any questions. Happy to jump on a call to discuss further.

Best,
[Your name]
```

**Tracking:**
- Email sent ✅
- Opens: Will notify you
- Document views: Will track
- Response: Will alert you

Want me to set a follow-up reminder? (3-5 days is typical) 📅

## Commands

```bash
# Create proposal from brief
proposalwriter create "project brief here"

# Use template
proposalwriter create --template "web-development"

# Add sections
proposalwriter add-section "Custom Section" "content here"

# Update pricing
proposalwriter pricing --total 10000 --breakdown "deposit:50%,milestone:25%"

# Export
proposalwriter export proposal-123 --format pdf

# Email proposal
proposalwriter send proposal-123 --to "client@example.com"

# Track proposal
proposalwriter track proposal-123
```

## Templates

```bash
# List templates
proposalwriter templates list

# Create custom template
proposalwriter templates create "my-template" \
  --sections "overview,scope,deliverables,timeline,pricing"

# Use template
proposalwriter create --template "web-development"
```

## Available Templates

- **web-development**: Websites, web apps
- **mobile-app**: iOS/Android apps
- **design**: Brand, UI/UX projects
- **consulting**: Advisory, strategy work
- **marketing**: Campaigns, content creation
- **maintenance**: Ongoing support agreements

## Telegram Integration

**Quick proposal:**

**You:** *[forwards client email with project details]*

**Paw:** Want me to create a proposal from this?

Details extracted:
- Project: Website redesign
- Budget: $6,000
- Timeline: 3 weeks

React with 📝 to generate proposal.

---

**You:** 📝

**Paw:** *generates proposal*

Proposal ready. Preview:

**Project:** Website Redesign
**Scope:** [Summary]
**Investment:** $6,000
**Timeline:** 3 weeks

Reply with "export pdf" or "send email" when ready. ✅

## Proposal Tracking

```bash
# View proposal status
proposalwriter status proposal-123

# Example output:
# Status: Sent
# Sent: 2 days ago
# Opens: 3
# Last viewed: 5 hours ago
# Response: Pending
```

**Notifications:**

- 📧 Proposal opened (first time)
- 👀 Proposal viewed multiple times (hot lead)
- ⏰ No response after 3 days (follow-up reminder)
- ✅ Client replied (action needed)

## Pricing Calculator

```bash
# Calculate hourly rate pricing
proposalwriter calc-hourly --hours 40 --rate 150

# Calculate value-based pricing
proposalwriter calc-value --client-revenue 100000 --improvement 20

# Show pricing suggestions
proposalwriter suggest-pricing "web development project"
```

## Customization

```bash
# Set your branding
proposalwriter branding set \
  --company "Your Company" \
  --logo "logo.png" \
  --color "#FF6B35"

# Default payment terms
proposalwriter config payment-terms "Net 30"

# Default contract language
proposalwriter config contract-template "standard-terms.txt"

# Signature line
proposalwriter config signature "[Your Name], [Your Title]"
```

## Configuration

```bash
# Show config
proposalwriter config show

# Set default template
proposalwriter config set default-template "web-development"

# Set hourly rate
proposalwriter config set hourly-rate 150

# Payment terms
proposalwriter config set payment-terms "Net 30"

# Auto-follow-up delay
proposalwriter config set follow-up-days 3
```

## Pricing

- **Free tier:** 3 proposals/month, basic templates
- **Pro:** $19/month — unlimited proposals, custom templates, tracking, email integration

Install: [pawhub.ai/proposalwriter](https://pawhub.ai/proposalwriter)

## Notes

- Generated proposals are starting points (review before sending)
- Legal terms should be reviewed by attorney
- Pricing suggestions based on industry standards
- Proposal tracking respects privacy (only open/view metrics)
- All proposals stored locally (encrypted)
- Export to PDF, Word, Google Docs, Notion

---

Win more projects by responding faster with better proposals. 📝🐾
