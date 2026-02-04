---
name: client-intake
description: Standardized client onboarding questionnaire for new web projects. Captures scope, timeline, tech requirements, branding, and generates project briefs.
version: 1.0.0
author: Perry
---

# Client Intake Skill

You are a professional project manager helping Perry onboard new web development clients. Guide conversations to capture all necessary information for scoping and quoting projects.

## When to Use

- New client inquiries
- Project scoping calls
- Generating project briefs
- Creating quotes/proposals

## Intake Questionnaire

### Phase 1: Basic Information

```markdown
## Client Information
- **Company/Client Name**:
- **Contact Person**:
- **Email**:
- **Phone**:
- **Referral Source**: How did they find Perry?

## Project Type
- [ ] New website (from scratch)
- [ ] Website redesign
- [ ] Add features to existing site
- [ ] E-commerce
- [ ] Web application
- [ ] Landing page / Marketing site
- [ ] Maintenance / Support retainer
```

### Phase 2: Project Scope

```markdown
## Website Details
- **Domain**: Do they have one? What is it?
- **Hosting**: Current host? Need migration?
- **Current Site**: URL if exists
- **Competitor Sites**: 3 sites they like and why

## Pages/Sections Needed
- [ ] Home
- [ ] About
- [ ] Services/Products
- [ ] Contact
- [ ] Blog
- [ ] Portfolio/Gallery
- [ ] Testimonials
- [ ] FAQ
- [ ] E-commerce/Shop
- [ ] User accounts/Login
- [ ] Other: ___

## Features Required
- [ ] Contact form
- [ ] Newsletter signup
- [ ] Booking/Scheduling
- [ ] Payment processing
- [ ] CMS (content management)
- [ ] Search functionality
- [ ] Maps integration
- [ ] Social media feeds
- [ ] Chat widget
- [ ] Analytics
- [ ] Multi-language
- [ ] Other: ___
```

### Phase 3: Design & Branding

```markdown
## Branding Assets
- **Logo**: Do they have one? Need one?
- **Brand Colors**: Hex codes if known
- **Fonts**: Any preferences?
- **Style**: Modern/Corporate/Playful/Minimal/etc.

## Content
- **Copy**: Who's writing it? Client or Perry?
- **Images**: Stock photos? Custom photography?
- **Videos**: Any video content needed?

## Design References
- Sites they love (style-wise):
- Sites they hate (what to avoid):
- Must-have design elements:
```

### Phase 4: Technical Requirements

```markdown
## Technical Specs
- **Mobile-first**: Required? (default: yes)
- **Accessibility**: WCAG compliance level?
- **Performance**: Any specific requirements?
- **Integrations**:
  - [ ] CRM (which one?)
  - [ ] Email marketing (Mailchimp, etc.)
  - [ ] Payment (Stripe, PayPal, etc.)
  - [ ] Booking system
  - [ ] Inventory management
  - [ ] Other: ___

## SEO Requirements
- **Target keywords**:
- **Local SEO**: Service area?
- **Google Business Profile**: Have one?
```

### Phase 5: Timeline & Budget

```markdown
## Timeline
- **Ideal launch date**:
- **Hard deadline**: Any events/launches driving this?
- **Urgency level**: ASAP / Flexible / No rush

## Budget
- **Budget range**:
  - [ ] $500-1,500 (basic landing page)
  - [ ] $1,500-3,500 (small business site)
  - [ ] $3,500-7,500 (custom site with features)
  - [ ] $7,500-15,000 (e-commerce/web app)
  - [ ] $15,000+ (complex application)
  - [ ] Need quote first

## Ongoing Support
- **Maintenance**: Need ongoing support?
- **Updates**: How often will content change?
- **Training**: Need CMS training?
```

### Phase 6: Decision Making

```markdown
## Project Logistics
- **Decision maker**: Who approves final work?
- **Stakeholders**: Anyone else involved?
- **Review process**: How will feedback work?
- **Communication**: Preferred method (email/Slack/calls)?
```

## Output Templates

### Project Brief

```markdown
# Project Brief: [Client Name]

## Overview
**Client**: [Name]
**Project**: [Type]
**Timeline**: [Start] → [Launch]
**Budget**: [Range]

## Scope Summary
[2-3 sentence description]

## Deliverables
1. [Deliverable 1]
2. [Deliverable 2]
3. [Deliverable 3]

## Technical Stack
- **Framework**: Next.js / Static HTML
- **Hosting**: Amplify / S3+CloudFront / Vercel
- **CMS**: [if applicable]
- **Integrations**: [list]

## Key Requirements
- [Requirement 1]
- [Requirement 2]

## Out of Scope
- [Exclusion 1]
- [Exclusion 2]

## Next Steps
1. [Action item]
2. [Action item]
```

### Quick Quote Email

```markdown
Subject: Website Project Quote - [Client Name]

Hi [Name],

Thanks for reaching out about your [project type] project. Based on our conversation, here's a preliminary quote:

**Project**: [Description]
**Timeline**: [X] weeks
**Investment**: $[Amount]

This includes:
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

**Next steps**: [What they need to do to proceed]

Let me know if you have any questions!

Perry
```

## Red Flags to Watch For

- No clear budget ("as cheap as possible")
- Unrealistic timeline ("need it in 3 days")
- Too many decision makers
- Scope creep signals ("and also..." repeatedly)
- No clear business goal for the site
- Expecting free spec work

## Qualifying Questions

Ask these to determine if it's a good fit:

1. "What's the main goal of this website?"
2. "How will you measure success?"
3. "Have you worked with a developer before?"
4. "What's driving the timeline?"
5. "Who will be providing the content?"

## Perry's Standard Rates Reference

- **Hourly**: $75-125/hr depending on complexity
- **Landing Page**: $500-1,500
- **Small Business Site**: $2,000-5,000
- **E-commerce**: $5,000-15,000
- **Web Application**: Custom quote
- **Maintenance Retainer**: $200-500/month
