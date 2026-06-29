---
name: brief-generator
description: 'Use when the user asks to "create an influencer brief" or "write a campaign brief"; produces a structured creator brief with deliverables, key messages, creative direction, timeline, disclosure rules, and compensation terms. Not for choosing how to split spend across creators — use budget-optimizer.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Activate when the user needs to brief one or more influencers for a campaign, standardize brief formats across a team, onboard ambassador partners, build reusable templates for recurring campaigns, or tighten brief clarity after revision-heavy collaborations. Also fires for platform-specific briefs (TikTok review, Instagram Stories takeover, YouTube integration)."
argument-hint: "<campaign or product> [platform] [content type]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Plan
---

# Brief Generator

This skill helps you create clear, comprehensive influencer briefs that set creators up for success. Good briefs lead to better content, fewer revisions, and stronger partnerships.

## Quick Start

Shortest invocation:

```
Create an influencer brief for [campaign]
```

Common scenario:

```
Generate a TikTok brief for micro-influencers promoting [product], 1 review video, with disclosure and timeline
```

## Skill Contract

- **Reads**: campaign name, brand, product/service, target platforms, content types and quantities, key message, CTA, timeline, compensation terms. Pulls any prior campaign facts from `memory/hot-cache.md` when present.
- **Writes**: a complete creator-ready brief saved to `memory/influencer/brief-generator/YYYY-MM-DD-<topic>.md`.
- **Promotes**: durable campaign facts (brand handle, campaign hashtag, disclosure standard, posting window, usage-rights duration) to `memory/hot-cache.md`.
- **Done when**:
  - The brief covers all required sections (overview, key messages, deliverables, creative direction, timeline, compliance, compensation, contact).
  - Disclosure requirements and usage rights are stated explicitly, with no placeholder left unresolved that the user gave input for.
  - Deliverables and quantities match what the user requested per platform.
- **Primary next skill**: [budget-optimizer](../../plan/budget-optimizer/SKILL.md)

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family has no live integrations required (Tier 1). The skill works end to end by asking the user for inputs: campaign details, deliverables, key messages, timeline, and compensation. Provide those in the prompt and you get a complete brief with zero setup.

Optional connectors that can enrich a brief when available:

- `~~influencer database` — pull creator handles, audience size, and past collaboration notes to personalize the "Why You" section.
- `~~social platform analytics` — confirm current format specs and best-performing post lengths per platform.
- `~~CRM` — fetch the assigned point of contact and prior brief versions for an ambassador.

See [CONNECTORS.md](../../CONNECTORS.md) for the verified free/keyless recipe per category. None are required.

## Instructions

When a user requests a brief:

1. **Gather Brief Inputs**

   ```markdown
   ### Brief Requirements
   
   **Campaign Information**:
   - Campaign Name: [name]
   - Brand: [brand]
   - Product/Service: [description]
   
   **Deliverables**:
   - Platform(s): [platforms]
   - Content Type: [types]
   - Quantity: [number of posts]
   
   **Key Details**:
   - Key message: [main point to convey]
   - CTA: [what action should viewers take]
   - Timeline: [key dates]
   - Budget/Compensation: [terms]
   ```

2. **Generate Professional Brief**

   ```markdown
   ---
   
   # Influencer Campaign Brief
   
   ## Campaign: [Campaign Name]
   
   ---
   
   ## 📋 Overview
   
   ### Brand
   **[Brand Name]** - [One-line brand description]
   
   [2-3 sentences about the brand, its values, and what makes it unique]
   
   ### Product/Service
   **[Product Name]**
   
   [Product description including:
   - What it is
   - Key features/benefits
   - Price point
   - Where to buy]
   
   ### Campaign Goal
   [Clear statement of what this campaign aims to achieve]
   
   ### Why You
   [Personalized note on why this influencer was selected - makes creators feel valued]
   
   ---
   
   ## 🎯 Key Messages
   
   ### Primary Message
   > "[The one thing viewers should take away]"
   
   ### Supporting Messages (choose 1-2 to incorporate naturally)
   - [Message 1]
   - [Message 2]
   - [Message 3]
   
   ### Talking Points
   - [Point 1]
   - [Point 2]
   - [Point 3]
   
   ### What NOT to Say
   - [Avoid 1]
   - [Avoid 2]
   
   ---
   
   ## 📱 Deliverables
   
   ### Content Requirements
   
   | Platform | Format | Quantity | Specs |
   |----------|--------|----------|-------|
   | [Platform 1] | [Format] | [#] | [Specs] |
   | [Platform 2] | [Format] | [#] | [Specs] |
   
   ### Platform-Specific Details
   
   #### [Platform 1] Requirements
   
   **Format**: [Format type]
   **Quantity**: [Number]
   **Duration**: [If video: length]
   
   **Technical Specs**:
   - Aspect ratio: [ratio]
   - Resolution: [minimum]
   - File format: [formats]
   
   **Caption Requirements**:
   - Include: [@brand mention, #hashtags, disclosure]
   - Character limit: [platform limit]
   - Link: [yes/no, where]
   
   **Additional Elements**:
   - [ ] [Element 1]
   - [ ] [Element 2]
   
   ---
   
   ## 🎨 Creative Direction
   
   ### Creative Concept
   [Describe the overall creative vision for this campaign]
   
   ### Tone & Style
   - Tone: [e.g., fun and energetic / authentic and relatable / premium and aspirational]
   - Style: [e.g., lifestyle integration / tutorial / review / day-in-the-life]
   - Visual: [e.g., bright and colorful / moody and cinematic / minimal and clean]
   
   ### Content Structure Suggestion
   
   **Hook** (first 1-3 seconds):
   [Suggestion for attention-grabbing opening]
   
   **Body**:
   [What the main content should cover]
   
   **CTA** (end):
   [What viewers should do next]
   
   ### Creative Freedom
   [Statement about how much creative freedom the influencer has]
   
   > 💡 **Note**: We love your creative voice! These are guidelines, not scripts. Feel free to make this your own while hitting the key messages.
   
   ### Inspiration
   
   **Reference Examples**:
   - [Link/description of example 1]
   - [Link/description of example 2]
   
   **What we love about these**:
   - [What makes them effective]
   
   ### Do's and Don'ts
   
   #### ✅ Do
   - [Do 1]
   - [Do 2]
   - [Do 3]
   - [Do 4]
   
   #### ❌ Don't
   - [Don't 1]
   - [Don't 2]
   - [Don't 3]
   - [Don't 4]
   
   ---
   
   ## 📦 Product Details
   
   ### What You'll Receive
   - [Product 1] - [description/variant]
   - [Product 2] - [description/variant]
   
   **Shipping Timeline**: [Expected delivery date]
   **Shipping Address**: [Confirm address with influencer]
   
   ### Product Key Features
   
   | Feature | Benefit | How to Show |
   |---------|---------|-------------|
   | [Feature 1] | [Benefit] | [Demo suggestion] |
   | [Feature 2] | [Benefit] | [Demo suggestion] |
   | [Feature 3] | [Benefit] | [Demo suggestion] |
   
   ### Product USPs to Highlight
   1. [USP 1]
   2. [USP 2]
   3. [USP 3]
   
   ---
   
   ## 🔗 Campaign Assets
   
   ### Required Elements
   
   | Element | Details |
   |---------|---------|
   | Brand Handle | @[handle] |
   | Campaign Hashtag | #[hashtag] |
   | Branded Hashtag | #[hashtag] |
   | Landing Page | [URL] |
   | Promo Code | [CODE] - [discount details] |
   | UTM Link | [full tracking URL] |
   
   ### Brand Assets (if needed)
   [Link to brand asset folder with logos, images, etc.]
   
   ---
   
   ## 📅 Timeline & Deadlines
   
   | Milestone | Date | Notes |
   |-----------|------|-------|
   | Brief Received | [date] | Today |
   | Product Delivery | [date] | |
   | Concept/Script Due | [date] | Optional - for approval |
   | Draft Content Due | [date] | For review before posting |
   | Feedback Provided | [date] | |
   | Revisions Due | [date] | If needed |
   | Final Approval | [date] | |
   | Content Goes Live | [date] | [time window if specific] |
   | Insights/Analytics Due | [date] | 48-72 hours post |
   
   **Posting Window**: [specific dates/times if applicable]
   
   ---
   
   ## ✅ Approval Process
   
   ### What to Submit for Review
   
   1. **Before filming/creating**:
      - [ ] Concept outline OR script (optional)
      - [ ] Any questions or concerns
   
   2. **For content approval**:
      - [ ] Draft content (unlisted/private)
      - [ ] Draft caption with all required elements
   
   3. **After posting**:
      - [ ] Live content link
      - [ ] Screenshots of insights (48-72 hours post)
   
   ### Submission Method
   [How to submit: email, platform, tool]
   
   ### Review Timeline
   - Initial review: [X] business days
   - Revision feedback: [X] business days
   
   ### Revision Policy
   [Number of revisions included, what constitutes a revision]
   
   ---
   
   ## ⚖️ Legal & Compliance
   
   ### Disclosure Requirements
   
   **Required disclosure**: All sponsored content MUST include clear disclosure.
   
   **Acceptable disclosures**:
   - #ad (required)
   - #sponsored
   - "Paid partnership with [Brand]" (platform feature)
   - Verbal disclosure in video: "This video is sponsored by [Brand]"
   
   **Placement**: Disclosure must be:
   - Visible without clicking "more"
   - At the beginning of caption
   - Clear and unambiguous
   
   ### Content Restrictions
   
   - [ ] No competitor mentions
   - [ ] No false claims about product
   - [ ] No before/after claims (unless approved)
   - [ ] No pricing comparisons
   - [ ] [Industry-specific restrictions]
   
   ### Usage Rights
   
   **[Brand] is granted the following rights**:
   - [ ] Repost on brand social channels
   - [ ] Use in paid advertising
   - [ ] Use on website
   - [ ] Use in email marketing
   - [ ] Use in presentations/sales materials
   
   **Duration**: [e.g., perpetual / 12 months / campaign duration]
   **Territories**: [e.g., worldwide / US only]
   
   ---
   
   ## 💰 Compensation
   
   ### Payment Terms
   
   | Item | Amount |
   |------|--------|
   | Base Fee | $[X] |
   | [Additional deliverable] | $[X] |
   | **Total** | **$[X]** |
   
   **Payment Method**: [method]
   **Payment Timeline**: [e.g., Net 30 after content goes live]
   **Invoice Requirements**: [what to include]
   
   ### Additional Compensation
   - Affiliate commission: [% on sales with code]
   - Product to keep: [Yes/No - value]
   - Performance bonus: [if applicable]
   
   ---
   
   ## 📞 Contact Information
   
   ### Your Point of Contact
   
   **Name**: [Contact name]
   **Role**: [Title]
   **Email**: [email]
   **Phone**: [phone - for urgent matters]
   **Response Time**: [expected response time]
   
   ### Escalation Contact
   [Secondary contact for urgent issues]
   
   ---
   
   ## ❓ FAQ
   
   **Q: Can I share the product with friends/family in the content?**
   A: [Answer]
   
   **Q: What if I need more time?**
   A: [Answer]
   
   **Q: Can I repurpose this content for other platforms?**
   A: [Answer]
   
   **Q: What happens if I'm not happy with the product?**
   A: [Answer]
   
   ---
   
   ## ✍️ Brief Acknowledgment
   
   By proceeding with this collaboration, you confirm:
   
   - [ ] I have read and understood this brief
   - [ ] I agree to the deliverables and timeline
   - [ ] I will comply with disclosure requirements
   - [ ] I understand the usage rights granted
   
   **Please confirm receipt and understanding by [date].**
   
   ---
   
   *Thank you for partnering with [Brand]! We're excited to work with you. Don't hesitate to reach out with any questions.*
   
   ---
   ```

3. **Create Brief Variations**

   For different content types, adjust:

   ```markdown
   ## Brief Variations
   
   ### TikTok Video Brief
   - Emphasize: Hook importance, trending sounds, native feel
   - Include: Sound/music options, trending formats to consider
   - Duration: 15-60 seconds optimal
   
   ### Instagram Reels Brief
   - Emphasize: Visual quality, cover image, carousel option
   - Include: Reel vs. Feed placement, Stories cross-posting
   - Duration: 15-30 seconds optimal
   
   ### Instagram Feed Post Brief
   - Emphasize: High-quality imagery, detailed caption
   - Include: Carousel considerations, aesthetic fit
   - Format: Square/Portrait/Landscape options
   
   ### Instagram Stories Brief
   - Emphasize: Authenticity, multiple frames, swipe-up/link
   - Include: Story frames breakdown, poll/questions use
   - Duration: 3-7 story frames typical
   
   ### YouTube Video Brief
   - Emphasize: Integration style (dedicated vs. mention), SEO
   - Include: Video description requirements, end screen
   - Duration: Varies by integration type
   
   ### YouTube Shorts Brief
   - Similar to TikTok with YouTube-specific features
   - Include: YouTube algorithm considerations
   ```

## How to Invoke

### Create a Campaign Brief

```
Create an influencer brief for [campaign] with [deliverables] for [product]
```

```
Generate a brief for [influencer type] promoting [product] on [platform]
```

### Specific Content Types

```
Create a TikTok brief for a product review video
```

```
Generate an Instagram Stories brief for a brand takeover
```

## When to Use This Skill

- Briefing influencers for a new campaign
- Standardizing brief formats across your team
- Onboarding new ambassador partners
- Creating templates for recurring campaigns
- Improving brief clarity after revision-heavy campaigns
- Preparing briefs for different content types

## What This Skill Does

1. **Brief Structure**: Creates organized, easy-to-follow briefs
2. **Clear Requirements**: Specifies all deliverables and guidelines
3. **Creative Direction**: Provides inspiration while allowing freedom
4. **Technical Specs**: Details platform-specific requirements
5. **Compliance**: Includes legal/disclosure requirements
6. **Timeline**: Establishes clear deadlines and milestones

## Example

**User**: "Create a brief for micro-influencers to promote our new organic protein powder on Instagram and TikTok"

**Output**: [Complete brief with product messaging around organic ingredients and clean label, deliverables of 1 Reel + 1 TikTok video, creative direction for "morning routine" or "workout fuel" angles, timeline, and disclosure requirements]

## Brief Templates by Campaign Type

### Product Launch Brief
- Focus: Introduction, key features, availability
- Content: Unboxing, first impressions, demo

### Review/Testimonial Brief
- Focus: Honest experience, specific benefits
- Content: In-depth review, before/after (if applicable)

### Event/Activation Brief
- Focus: Experience, atmosphere, brand interaction
- Content: Real-time posting, event highlights

### Always-On/Ambassador Brief
- Focus: Ongoing integration, long-term relationship
- Content: Regular organic mentions, lifestyle integration

### Giveaway Brief
- Focus: Entry mechanics, rules, excitement
- Content: Prize showcase, entry CTA

## Tips for Great Briefs

1. **Be clear, not controlling** - Guidelines, not scripts
2. **Show inspiration** - Visual examples help
3. **Respect their voice** - That's why you hired them
4. **Make it scannable** - Use formatting, headers, bullets
5. **Include everything** - Don't make them ask questions
6. **Be realistic** - Don't ask for too much in one post

## Reference Materials

- Shared contract: [skill-contract.md](../../references/skill-contract.md)
- Shared state model: [state-model.md](../../references/state-model.md)
- Connector recipes: [CONNECTORS.md](../../CONNECTORS.md)
- C3 scoring architecture (when scoring brief quality): [references/c3/scoring-architecture.md](../../references/c3/scoring-architecture.md)
- Sibling skills:
  - [campaign-planner](../campaign-planner/SKILL.md) - Create the campaign this brief supports
  - [budget-optimizer](../budget-optimizer/SKILL.md) - Allocate spend across the briefed creators
  - [content-reviewer](../../activate/content-reviewer/SKILL.md) - Review submitted content
  - [outreach-manager](../../activate/outreach-manager/SKILL.md) - Deliver briefs to influencers
  - [contract-helper](../../activate/contract-helper/SKILL.md) - Include legal terms

## Next Best Skill

- **Primary**: [budget-optimizer](../../plan/budget-optimizer/SKILL.md) - Once the brief defines deliverables, set how spend is split across creators and platforms.
- **Alternates (same Plan family)**:
  - [campaign-planner](../campaign-planner/SKILL.md) - Re-plan campaign scope if the brief surfaces new deliverable needs.
  - [outreach-manager](../../activate/outreach-manager/SKILL.md) - Send the finished brief to selected creators.

**Termination note**: Maintain a visited-set. If a recommended skill was already invoked this session, stop and report chain-complete instead of re-running it. Cap any handoff chain at max-depth 3.
