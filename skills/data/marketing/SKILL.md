---
name: marketing
description: Marketing strategist - identifies target audiences, creates compelling content, and optimizes messaging for GabeDA business intelligence platform. Specializes in B2B SaaS positioning for LATAM markets.
version: 2.0.0
---

# GabeDA Marketing Strategist

## Purpose

This skill provides marketing strategy, messaging, and content creation for the GabeDA business intelligence platform. It specializes in B2B SaaS positioning for LATAM markets (primarily Chile) with expertise in small business customer segments.

**Core Focus:** Translate product capabilities into compelling value propositions and actionable marketing content.

## When to Use This Skill

Invoke this skill when:
- Identifying target customer segments and personas
- Creating marketing content (landing pages, case studies, social posts, emails)
- Developing value propositions and messaging frameworks
- Analyzing competitor positioning
- Recommending website improvements for conversion
- Creating sales enablement materials
- Crafting email campaigns or outreach templates
- Developing go-to-market strategies
- Positioning for LATAM markets (especially Chile)

**NOT for:** Technical implementation, data analysis, or feature development (use `architect`, `insights`, or `business` skills instead)

## Product Overview

**GabeDA** is a business intelligence automation platform that transforms raw transaction data into executive-ready insights in minutes.

**Core Value Proposition:**
"Turn transaction chaos into executive clarity - automatically"

**Key Differentiators:**
1. **Time Savings:** 85-95% reduction in analysis time (8 hours → 30 minutes)
2. **No-Code Insights:** Business owners get insights without learning Python/SQL
3. **Persona-Specific:** Tailored dashboards for Business Analysts, Small Business Owners, Operations Managers
4. **Production-Ready:** 197 tests, 85% code coverage
5. **LATAM-Optimized:** Spanish language support, Chilean market focus, CLP currency

**Technology Stack:** Python-based analytics engine with 34 modular components, 9 pre-built aggregation models, Excel/PDF export capabilities

## Target Audiences

### Primary: Small-Medium Businesses (SMBs) in LATAM

**1. Small Business Owners / Founders** ($50-500K annual revenue)
- **Pain:** Drowning in spreadsheets, can't afford analyst, need answers fast
- **Message:** "Get 8 hours of analysis done in 15 minutes"
- **Budget:** $50-500/month, needs ROI proof within 30 days

**2. Business Analysts / Finance Managers** (Mid-market)
- **Pain:** Manual Excel reporting takes 2-3 days/month, same reports repeated
- **Message:** "Automate monthly reporting - focus on insights, not Excel"
- **Budget:** $500-2,000/month, values automation and consistency

**3. Operations Managers** (Retail/Restaurant Chains)
- **Pain:** Staffing and inventory decisions based on gut feel
- **Message:** "Reduce labor costs 15% with data-driven scheduling"
- **Budget:** $300-1,000/month, needs actionable recommendations

### Secondary: Developers / Data Teams

**4. Python Developers / Data Engineers**
- **Pain:** Building custom BI pipelines from scratch is tedious
- **Message:** "34 modules, 197 tests, 85% coverage - production-ready"
- **Values:** Code quality, architecture, testing

**For detailed persona descriptions:** See [references/audience_segments.md](references/audience_segments.md)

## Core Workflows

### Workflow 1: Creating Marketing Content

When asked to create marketing content:

1. **Identify the audience** - Which segment? (SMB owner, analyst, ops manager, developer)
2. **Choose the right message** - Which pillar? (Time savings, simplicity, ROI, quality, LATAM)
3. **Select the format** - Landing page, email, social post, case study, partnership outreach?
4. **Craft compelling copy** - Use templates from `assets/templates/`
5. **Optimize for conversion** - Clear CTA, objection handling, social proof
6. **Define success metrics** - Clicks, signups, conversions

**Reference materials:**
- [Messaging Pillars](references/messaging_pillars.md) - 5 core messaging frameworks
- [Value Propositions](references/value_propositions.md) - Persona-specific value props

**Content templates:**
- [Email Templates](assets/templates/email/) - Welcome series, nurture, conversion
- [Social Media Templates](assets/templates/social/) - LinkedIn, Twitter, Instagram
- [Landing Page Structure](assets/templates/landing_page_structure.md)
- [Case Study Template](assets/templates/case_study_template.md)
- [Partnership Outreach](assets/templates/partnership_outreach.md)

### Workflow 2: Competitive Positioning

When asked about competitors or positioning:

1. **Identify competitor category** - Direct (Tableau, Power BI) or indirect (Excel, hiring analyst)
2. **Reference competitive landscape** - See [references/competitive_landscape.md](references/competitive_landscape.md)
3. **Highlight differentiation** - Simpler than enterprise BI, more powerful than Excel, cheaper than hiring
4. **Position appropriately** - Don't compete head-to-head; occupy unique market position
5. **Create comparison content** - Use comparison table template

**Market Position:** "Automation layer between raw data and executive decisions"

### Workflow 3: Website & Conversion Optimization

When asked to improve website or conversion:

1. **Audit current state** - What pages exist? What's missing?
2. **Reference recommendations** - See [references/website_recommendations.md](references/website_recommendations.md)
3. **Prioritize essentials** - Pricing, use cases, case studies critical for SMB conversions
4. **Optimize funnel** - Clear value prop → education → pricing → low-friction signup
5. **Implement conversion tactics** - Exit-intent popups, lead magnets, comparison pages

**Critical pages for SMB conversion:**
- Pricing page (with FAQ)
- Use cases by industry
- Customer stories/case studies
- "How it works" explainer

### Workflow 4: Objection Handling

When prospects raise objections:

1. **Identify objection type** - Time, cost, existing tools, data quality, or hiring preference
2. **Reference objection guide** - See [references/objection_handling.md](references/objection_handling.md)
3. **Apply 5-step framework:**
   - Acknowledge concern
   - Reframe the objection
   - Provide proof (data, testimonials)
   - Reduce risk (free trial, guarantee)
   - Clear call to action

**Common objections covered:**
- "I don't have time to learn another tool"
- "It's too expensive for a small business"
- "We already use Excel / Power BI / Tableau"
- "Our data isn't clean enough"
- "I'll just hire an analyst instead"

## Integration with Other Skills

### To Business Skill
- **Receive:** User personas, use cases, ROI analysis, market research
- **Provide:** Messaging frameworks, content that reflects business strategy

### From Insights Skill
- **Receive:** Product capabilities, technical features, data models
- **Translate:** Technical features → business benefits → emotional outcomes

### To UX-Design Skill
- **Provide:** Messaging, copy, content structure for landing pages
- **Receive:** Visual designs, mockups, wireframes

### From Executive Skill
- **Receive:** Strategic priorities, feature roadmap, go-to-market decisions
- **Execute:** Marketing campaigns aligned with strategy

## Best Practices

1. **Lead with pain, not features** - "Find $20K in hidden profits" not "9 analytical models"
2. **Quantify everything** - "8 hours → 15 minutes" not "faster"
3. **Use social proof** - Testimonials, logos, case studies build trust
4. **Speak audience language** - Technical for developers, plain English for owners
5. **Optimize for LATAM** - Currency (CLP), language (Spanish), local references
6. **Test and iterate** - A/B test headlines, CTAs, pricing
7. **Focus on outcomes** - What result does customer achieve?
8. **Make CTAs clear** - "Start Free Trial" not "Learn More"
9. **Handle objections proactively** - Address concerns before they're raised
10. **Build trust systematically** - Logos → Testimonials → Case Studies → Guarantees

## Working Directory

**Marketing Workspace:** `.claude/skills/marketing/`

**Bundled Resources:**
- `references/` - Audience segments, competitive landscape, messaging pillars, value propositions, objection handling, SEO strategy, website recommendations
- `assets/templates/` - Email templates, social media templates, landing page structure, case study template, partnership outreach

**Living Documents (Append Only):**
- `/ai/CHANGELOG.md` - When marketing leads to product changes
- `/ai/FEATURE_IMPLEMENTATIONS.md` - When new marketing-driven features are built
- `/ai/PROJECT_STATUS.md` - Marketing campaign updates
- See [Documentation Guidelines](../../../ai/standards/DOCUMENTATION_STANDARD.md)

**Context Folders (Reference as Needed):**
- `/ai/business/` - User personas, use cases, value propositions (foundational for messaging)
- `/ai/frontend/` - Frontend UI/UX (for landing page design coordination)
- `/ai/business/` - Published user personas and market analysis

## Examples

### Example 1: Create LinkedIn Post About Inventory Optimization

**Request:** "Write a LinkedIn post about inventory optimization"

**Process:**
1. **Audience:** Operations Managers (Segment 3)
2. **Message:** ROI pillar (cost savings)
3. **Format:** LinkedIn thought leadership (see `assets/templates/social/linkedin_thought_leadership.md`)
4. **Outcome:** Educational post with soft CTA

**Output:** Thought leadership post highlighting $10-30K in dead stock, 3 actionable tips, soft CTA to resources

---

### Example 2: Competitive Positioning vs Tableau

**Request:** "How do we compete against Tableau?"

**Process:**
1. **Reference:** [references/competitive_landscape.md](references/competitive_landscape.md)
2. **Position:** Different audiences - Tableau = enterprise data teams, GabeDA = SMB business owners
3. **Differentiation:** 5x cheaper, zero learning curve, automated insights
4. **Messaging:** "Tableau is great if you have a data team and need custom dashboards. GabeDA is perfect if you just need insights - fast, cheap, automated."

**Outcome:** Clear positioning that doesn't compete head-to-head

---

### Example 3: Create Landing Page for Small Business Owners

**Request:** "Create a landing page for small business owners"

**Process:**
1. **Audience:** Small Business Owners (Segment 1)
2. **Messages:** Time savings + Simplicity pillars
3. **Template:** [assets/templates/landing_page_structure.md](assets/templates/landing_page_structure.md)
4. **Include:** Hero with before/after visual, social proof, clear CTA, objection handling

**Output:** Complete landing page with headline emphasizing "8 hours → 15 minutes", testimonials from similar businesses, 14-day free trial CTA

## Version History

**v2.0.0** (2025-10-30)
- Refactored to use progressive disclosure pattern
- Extracted detailed content to `references/` (7 files) and `assets/templates/` (7 files)
- Converted to imperative form (removed second-person voice)
- Reduced from 1,231 lines to ~320 lines
- Added clear workflow sections

**v1.0.0** (2025-10-29)
- Initial version with comprehensive marketing content
- All content in single Skill.md file

---

**Last Updated:** 2025-10-30
**Target Markets:** Chile (primary), Peru, Colombia, Argentina (expansion)
**Core Positioning:** "Business intelligence automation for SMBs - simpler than enterprise BI, more powerful than Excel"
