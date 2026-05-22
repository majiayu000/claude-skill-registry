---
name: Solo Landing Page
description: This skill should be used for ANYTHING related to landing page development including "review my landing page", "create a landing page", "write landing page copy", "build a landing page", "improve conversion rate", "optimize landing page", "landing page CRO", "write headlines", "create CTAs", "landing page structure", "add tracking", or any landing page-related task for marketing sites, product pages, or sales pages.
version: 0.1.0
---

# Solo Landing Page

A comprehensive framework for solo founders to build, review, and optimize landing pages that convert visitors into customers.

## Purpose

Help solo founders create effective landing pages that drive signups, trials, and sales. Whether building from scratch, reviewing existing pages, or optimizing for conversions, this skill provides actionable guidance focused on what actually works.

## When to Use This Skill

Apply this skill for any landing page task:
- **Creating**: Building new landing pages from scratch
- **Reviewing**: Providing CRO feedback on existing pages
- **Optimizing**: Improving conversion rates
- **Writing**: Crafting compelling headlines, copy, and CTAs
- **Structuring**: Organizing page flow and sections
- **Tracking**: Setting up lean conversion measurement
- **Validating**: Checking if ready to ship

## Core Framework: The 6 Conversion Pillars

Every effective landing page needs these six elements:

### 1. First Impression (Above the Fold)
- **Value Proposition Clarity**: Visitors understand what this is in 5 seconds
- **Headline Impact**: Benefit-focused, not feature-focused
- **Hero Section**: Answers "What is this?" and "Why should I care?"
- **Visual Hierarchy**: Eye naturally flows to the most important elements

### 2. Messaging & Copy
- **Clarity over Cleverness**: Clear and direct beats clever but confusing
- **Benefit vs Feature Balance**: Benefits clearly stated, features support them
- **Customer Language**: Sounds like how customers talk, not marketing speak
- **Specificity**: Claims are specific and credible, not vague
- **Objection Handling**: Addresses common concerns and doubts

### 3. Social Proof & Trust
- **Testimonials**: Specific and credible with real names/results
- **Authority Markers**: Logos, metrics, case studies
- **Risk Reduction**: Free trial, money-back guarantee, no credit card
- **Proof Points**: Real numbers, real results, real customers

### 4. Call-to-Action (CTA)
- **CTA Clarity**: Primary action is obvious and singular
- **Button Copy**: States the value, not generic "Submit"
- **CTA Repetition**: Repeated at logical points
- **Friction Analysis**: Minimal form fields, no unnecessary barriers

### 5. Structure & Flow
- **Logical Progression**: Guides visitors through a clear journey
- **Scannability**: Value understood by skimming
- **Section Purpose**: Each section has a clear job
- **Length vs. Depth**: Right depth for product complexity and price

### 6. Solo Founder Specific
- **Launch Readiness**: Good enough to ship vs needs work
- **Quick Wins**: Highest-impact changes available now
- **De-prioritization**: What can be removed or simplified
- **Revenue Focus**: Guides toward paid conversion, not just signups

## Measurement Requirements (Stay Lean)

### Must Track (Non-Negotiable)
These are the minimum events needed to understand landing page performance:

1. **CTA Button Clicks** - Track every primary CTA click
   - Event: `cta_clicked`
   - Properties: `{button_text, button_location}` (e.g., hero, footer)

2. **Form Submissions** - Track when forms are submitted (if applicable)
   - Event: `form_submitted`
   - Properties: `{form_type}` (e.g., signup, demo_request)

3. **Page Views** - Basic traffic measurement
   - Event: `page_viewed`
   - Properties: `{referrer_source}` (where they came from)

**Implementation**: Use a simple analytics tool (Plausible, PostHog, Simple Analytics) or basic custom tracking.

### Should Track (High Value, Low Effort)
Add these for additional insight:

4. **Scroll Depth** - Did they read the whole page?
   - Track at 25%, 50%, 75%, 100%
   - Helps identify if people see your bottom CTA

5. **Video Plays** - If you have a demo video
   - Event: `video_played`
   - Tells you if video is helping or ignored

### Could Track (Post-Launch Optimization)
Only add after you have initial traction:

6. **Section Visibility** - Which sections got viewed
7. **Link Clicks** - External links, testimonials, social proof
8. **A/B Test Variations** - When you're ready to test headlines/CTAs

### Don't Track (Analysis Paralysis)
Avoid these until you have real revenue:
- Heatmaps (nice-to-have, not essential)
- Session recordings (overkill for pre-launch)
- Micro-interactions (hover states, etc.)
- Complex funnels (keep it simple)

**The Goal**: Know the conversion rate (visitors → signups/trials). Avoid drowning in data before having customers.

## Task-Specific Guidance

### When Building a New Landing Page

**Required Information to Gather:**
1. What problem does the product solve?
2. Who is the target customer?
3. What's the primary conversion goal (trial, demo, purchase)?
4. What's the price point (free, low, medium, high)?
5. Any existing social proof or metrics?

**Structure to Follow:**
1. **Hero Section** - Value prop, headline, subheadline, primary CTA
2. **Problem/Agitation** - What pain are they experiencing?
3. **Solution** - How your product solves it (benefits, not features)
4. **Social Proof** - Testimonials, logos, metrics
5. **How It Works** - Simple 3-step explanation
6. **Features/Benefits** - Key capabilities tied to outcomes
7. **Pricing** (if applicable) - Clear, simple, objection-handling
8. **Final CTA** - Repeat the conversion ask

**Copy Formula:**
- **Headline**: [Desired outcome] without [common pain point]
- **Subheadline**: [How it works in one sentence]
- **CTA**: First-person, value-focused ("Start my free trial", not "Sign up")

**Tracking Setup:**
- Add `cta_clicked` event to all CTA buttons
- Add `form_submitted` event to signup/demo forms
- Add `page_viewed` event on load
- Use simple analytics (Plausible, PostHog, or custom)

### When Reviewing an Existing Landing Page

**Output Format:**

#### Quick Summary
**Overall Assessment**: [2-3 sentences on current state]
**Ship It?**: [Yes/No/Almost - with reasoning]
**Tracking Status**: [What's tracked, what's missing]

#### Critical Issues (Fix Before Launch)
List 2-4 issues that significantly hurt conversions:
- **[Issue]**: [Why it matters] → [Specific fix]

#### High-Impact Improvements
List 3-5 changes that would likely increase conversions:
- **[Current state]** → [Recommended change] → [Expected impact]

#### Copy Feedback
**Headline**: [Current] → [Suggested with reasoning]
**Subheadline**: [Current] → [Suggested with reasoning]
**CTA Copy**: [Current] → [Suggested alternatives with reasoning]

#### Tracking Gaps
**Missing Events**: [What's not being tracked that should be]
**Quick Fix**: [Simplest way to add essential tracking]

#### Specific Rewrite Suggestions
```
BEFORE:
[Current copy]

AFTER:
[Improved version]

WHY: [What changed and why it converts better]
```

#### What's Working Well
List 2-3 things to NOT change:
- **[Element]**: [Why it's effective]

#### Quick Wins (Do These First)
Ranked by impact/effort:
1. **[Change]** - [Why this matters]
2. **[Change]** - [Why this matters]

#### For Later (Post-Launch)
- [Optimization idea]
- [Optimization idea]

### When Writing Copy

**Headlines That Convert:**
- Lead with outcome/benefit, not product
- Be specific: "Cut support tickets by 40%" beats "Better customer service"
- Avoid jargon and clever wordplay
- Test benefit-focused vs curiosity-driven

**Effective CTAs:**
- Use first-person: "Start my free trial" beats "Start your free trial"
- State the value: "Get my custom report" beats "Submit"
- Reduce friction: "No credit card required"
- Create urgency without false scarcity

**Social Proof That Works:**
- Specific testimonials: "Saved 10 hours/week" beats "Great product"
- Include name, photo, company for credibility
- Show real numbers: "2,453 solo founders" beats "Thousands of users"
- Use recognizable brand logos if available

### When Setting Up Tracking

**Minimum Viable Tracking Setup:**

```javascript
// Example: Simple tracking (adapt to your stack)

// Must have
trackEvent('cta_clicked', {
  button_text: 'Start Free Trial',
  button_location: 'hero' // or 'footer', 'pricing', etc.
})

trackEvent('form_submitted', {
  form_type: 'signup' // or 'demo_request', 'contact', etc.
})

trackEvent('page_viewed', {
  referrer_source: document.referrer
})

// Nice to have
trackScrollDepth([25, 50, 75, 100])
```

**Tool Recommendations (Pick One):**
- **Plausible**: Privacy-focused, simple, lightweight
- **PostHog**: Open-source, self-hostable, feature-rich
- **Simple Analytics**: Dead simple, privacy-friendly
- **Custom**: Log events to your database (perfectly fine)

**Don't Overcomplicate**: Logging CTA clicks and form submissions covers 80% of needs. Ship first, optimize later.

### When Optimizing for Conversion

**Common Friction Points:**
- Too many form fields (only ask what you need NOW)
- Unclear pricing (show it or explain why you don't)
- Generic copy that could apply to any product
- No clear next step
- Weak value proposition
- Missing objection handling
- No tracking (can't measure what you don't track)

**Quick Win Checklist:**
- [ ] Headline clearly states the benefit
- [ ] Primary CTA is obvious and above the fold
- [ ] CTA clicks are tracked
- [ ] Social proof is present and specific
- [ ] Copy uses "you" and customer language
- [ ] No technical jargon unless target audience uses it
- [ ] Form submissions are tracked
- [ ] Conversion rate is measurable

## Copywriting Formulas

### PAS (Problem-Agitate-Solution)
1. **Problem**: State the pain point
2. **Agitate**: Make them feel it
3. **Solution**: Present your product as the answer

### AIDA (Attention-Interest-Desire-Action)
1. **Attention**: Grab with bold headline
2. **Interest**: Show you understand their problem
3. **Desire**: Demonstrate the transformation
4. **Action**: Clear CTA to convert

### Before-After-Bridge
1. **Before**: Current painful state
2. **After**: Desired future state
3. **Bridge**: Your product is how they get there

## Principles for Solo Founders

- **Conversion over aesthetics**: Pretty doesn't pay the bills
- **Specific over vague**: "Save 5 hours/week" beats "Save time"
- **Quick wins first**: High-impact, low-effort changes
- **Ship when ready**: Good enough to test beats perfect paralysis
- **Measure what matters**: Track conversions, not vanity metrics
- **Test and iterate**: Launch, measure, improve
- **Revenue focus**: Guide toward paid conversion
- **Customer language**: Talk how they talk, not how you think

## Common Issues by Stage

### Pre-Launch (Must Fix)
- Unclear value proposition
- No obvious CTA
- Technical errors (broken links, typos)
- Trust issues (no social proof, looks unprofessional)
- Missing tracking (can't measure success)

### Launch-Ready (High Impact)
- Weak headlines
- Feature-focused instead of benefit-focused
- Generic testimonials
- Too much friction in signup flow
- Incomplete tracking setup

### Post-Launch (Optimize)
- A/B test copy variations
- Add more social proof as you get it
- Optimize based on scroll depth data
- Refine messaging based on customer feedback
- Test different CTA copy

## Tone & Approach

- **Direct and Actionable**: Specific changes, not vague advice
- **Encouraging but Honest**: Truth over sugar-coating
- **Revenue-Focused**: Everything ties to conversion
- **Pragmatic**: Balance perfect with shipped
- **Show, Don't Tell**: Provide actual copy examples
- **Data-Informed**: Track enough to know what works

Remember: The goal is landing pages that convert. Good enough to test and iterate beats endless optimization before launch. Ship it, track the essentials, measure conversion rate, improve based on data.
