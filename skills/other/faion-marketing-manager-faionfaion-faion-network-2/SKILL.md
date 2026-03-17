---
name: faion-marketing-manager
description: "Marketing orchestrator: GTM, content, growth, conversion optimization."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Marketing Manager Orchestrator

Pure orchestrator that coordinates marketing activities by routing to specialized sub-skills.

## Purpose

Routes marketing tasks to appropriate sub-skill based on domain. No methodologies in this skill - all execution happens in sub-skills.

---

## Context Discovery

### Auto-Investigation

Check for existing marketing context:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `.aidocs/product_docs/gtm-manifest/` | `Glob("**/*gtm*")` | GTM strategy exists |
| `.aidocs/product_docs/seo/` | `Glob("**/seo/*.md")` | SEO strategy exists |
| `landing page files` | `Glob("**/pages/index.*")` | Landing page exists |
| `analytics config` | `Grep("GA4\|gtag\|analytics", "**/*")` | Analytics setup |
| `email templates` | `Glob("**/email*/**")` | Email marketing exists |

**Check existing assets:**
- Read landing page copy to understand current messaging
- Check meta tags for SEO status
- Look for pricing page to understand monetization

### Discovery Questions

Use `AskUserQuestion` to understand marketing goals and context.

#### Q1: Marketing Goal

```yaml
question: "What's your primary marketing goal right now?"
header: "Goal"
multiSelect: false
options:
  - label: "Launch a product"
    description: "Prepare and execute a product launch"
  - label: "Get more traffic"
    description: "Increase visitors to site/app"
  - label: "Convert more visitors"
    description: "Improve signup/purchase rates"
  - label: "Retain & grow users"
    description: "Reduce churn, increase engagement"
  - label: "Build brand awareness"
    description: "Establish presence and recognition"
```

**Routing:**
- "Launch" → `Skill(faion-gtm-strategist)` for full launch workflow
- "Traffic" → Ask Q2 (Budget) to decide organic vs paid
- "Convert" → `Skill(faion-conversion-optimizer)`
- "Retain & grow" → `Skill(faion-growth-marketer)`
- "Brand awareness" → `Skill(faion-content-marketer)` + `Skill(faion-smm-manager)`

#### Q2: Budget for Acquisition (if goal is traffic)

```yaml
question: "Do you have budget for paid acquisition?"
header: "Budget"
multiSelect: false
options:
  - label: "No budget (organic only)"
    description: "Focus on SEO, content, social"
  - label: "Small budget ($100-500/mo)"
    description: "Test paid channels carefully"
  - label: "Growth budget ($500+/mo)"
    description: "Scale what works with paid ads"
```

**Routing:**
- "No budget" → `Skill(faion-seo-manager)` + `Skill(faion-content-marketer)`
- "Small budget" → Test with `Skill(faion-ppc-manager)`, measure ROI
- "Growth budget" → `Skill(faion-ppc-manager)` + `Skill(faion-growth-marketer)`

#### Q3: Business Model

```yaml
question: "What's your business model?"
header: "Model"
multiSelect: false
options:
  - label: "B2C (consumers)"
    description: "Selling to individual consumers"
  - label: "B2B (businesses)"
    description: "Selling to companies/teams"
  - label: "B2B2C (platform)"
    description: "Businesses serve their customers through you"
  - label: "Marketplace"
    description: "Connecting buyers and sellers"
```

**Context impact:**
- "B2C" → Emotional messaging, social proof, viral loops
- "B2B" → ROI focus, case studies, LinkedIn, longer sales cycle
- "B2B2C" → Both B2B acquisition + B2C activation
- "Marketplace" → Chicken-egg problem, liquidity focus

#### Q4: Current Stage

```yaml
question: "What's your current traction?"
header: "Traction"
multiSelect: false
options:
  - label: "Pre-launch (no users yet)"
    description: "Building audience before launch"
  - label: "Early (< 100 users)"
    description: "Finding product-market fit"
  - label: "Growing (100-1000 users)"
    description: "Scaling what works"
  - label: "Scaling (1000+ users)"
    description: "Optimizing and expanding"
```

**Context impact:**
- "Pre-launch" → Audience building, waitlist, launch prep
- "Early" → Focus on learning, manual outreach, founder sales
- "Growing" → Test channels, find scalable acquisition
- "Scaling" → Optimize funnels, expand channels, retention

#### Q5: Existing Audience (multiSelect)

```yaml
question: "What audience/channels do you already have?"
header: "Channels"
multiSelect: true
options:
  - label: "Email list"
    description: "Newsletter or customer emails"
  - label: "Social following"
    description: "Twitter, LinkedIn, Instagram, etc."
  - label: "Existing customers"
    description: "People already paying/using"
  - label: "None yet"
    description: "Starting from zero"
```

**Context impact:**
- "Email list" → Leverage for launches, nurture sequences
- "Social following" → Distribution channel, engagement
- "Existing customers" → Referrals, case studies, upsell
- "None" → Focus on audience building first

---

## Architecture

| Sub-Skill | Purpose | Methodologies |
|-----------|---------|---------------|
| **faion-gtm-strategist** | GTM strategy, product launches, positioning, pricing, partnerships, customer success | 26 |
| **faion-content-marketer** | Content strategy, copywriting, SEO, email campaigns, social media, video/podcast production | 16 + 30 refs |
| **faion-growth-marketer** | Analytics, experiments, A/B testing, AARRR metrics, retention, viral loops | 30 |
| **faion-conversion-optimizer** | Landing pages, CRO, funnels, PLG, onboarding flows | 13 |
| **faion-ppc-manager** | Paid advertising (Google Ads, Meta Ads, LinkedIn Ads) | External skill |
| **faion-seo-manager** | Technical SEO, AEO, Core Web Vitals optimization | External skill |
| **faion-smm-manager** | Social media management (Twitter, LinkedIn, Instagram growth) | External skill |

**Total:** 85+ methodologies across 7 specialized sub-skills

## Decision Tree

| If you need... | Route to | Example Tasks |
|---------------|----------|---------------|
| **GTM & Launch** | faion-gtm-strategist | Product Hunt launch, GTM strategy, positioning, pricing strategy, partnership programs, customer success playbooks |
| **Content Creation** | faion-content-marketer | Content strategy, blog posts, copywriting, email campaigns, social posts, video scripts, podcast production |
| **Growth & Analytics** | faion-growth-marketer | AARRR framework, A/B testing, retention analysis, viral loops, cohort analysis, growth experiments |
| **Conversion** | faion-conversion-optimizer | Landing page optimization, funnel analysis, CRO experiments, PLG strategies, onboarding flows |
| **Paid Ads** | faion-ppc-manager | Google Ads campaigns, Meta Ads optimization, LinkedIn Ads, PPC strategy |
| **SEO Technical** | faion-seo-manager | Technical SEO audits, AEO optimization, Core Web Vitals, search ranking |
| **Social Media Mgmt** | faion-smm-manager | Twitter growth, LinkedIn strategy, Instagram content, community building |

## Routing Examples

### Launch Scenario
```
Product Launch
├─→ faion-gtm-strategist (GTM strategy, positioning, launch timeline)
├─→ faion-content-marketer (launch content, press release, email campaign)
├─→ faion-conversion-optimizer (landing page, free trial flow)
├─→ faion-growth-marketer (metrics tracking, launch experiments)
└─→ faion-ppc-manager (paid launch campaigns)
```

### Content Marketing Scenario
```
Content Marketing Program
├─→ faion-content-marketer (content strategy, editorial calendar, creation)
├─→ faion-seo-manager (technical SEO, on-page optimization)
├─→ faion-growth-marketer (content metrics, A/B testing)
└─→ faion-smm-manager (social distribution)
```

### Growth Optimization Scenario
```
Growth Optimization
├─→ faion-growth-marketer (AARRR analysis, experiment design, analytics)
├─→ faion-conversion-optimizer (funnel optimization, PLG tactics)
├─→ faion-content-marketer (growth content, email nurture)
└─→ faion-ppc-manager (paid acquisition scaling)
```

### Brand Building Scenario
```
Brand Building
├─→ faion-gtm-strategist (brand positioning, messaging)
├─→ faion-content-marketer (brand content, thought leadership)
├─→ faion-smm-manager (social media presence)
└─→ faion-seo-manager (brand search optimization)
```

## Execution Pattern

1. **Analyze** task intent and marketing domain
2. **Route** to appropriate sub-skill(s) via Skill tool
3. **Invoke** one or more sub-skills as needed
4. **Coordinate** multi-skill workflows if needed
5. **Report** consolidated results to user

## Quick Reference

| Marketing Goal | Primary Sub-Skill | Secondary Sub-Skills |
|----------------|-------------------|---------------------|
| Launch product | gtm-strategist | content-marketer, conversion-optimizer, ppc-manager |
| Acquire users | content-marketer | growth-marketer, seo-manager, ppc-manager |
| Optimize conversion | conversion-optimizer | growth-marketer |
| Scale growth | growth-marketer | ppc-manager, content-marketer |
| Build brand | content-marketer | gtm-strategist, smm-manager, seo-manager |
| Retain users | growth-marketer | content-marketer |
| Partnerships | gtm-strategist | content-marketer |
| Improve SEO | seo-manager | content-marketer |
| Social presence | smm-manager | content-marketer |
| Paid campaigns | ppc-manager | conversion-optimizer, growth-marketer |

## Related Skills

**Upstream:**
- faion-net (parent orchestrator)

**Downstream (coordinated by this skill):**
- faion-gtm-strategist
- faion-content-marketer
- faion-growth-marketer
- faion-conversion-optimizer
- faion-ppc-manager
- faion-seo-manager
- faion-smm-manager

**Adjacent:**
- faion-researcher (market research, competitor analysis)
- faion-product-manager (product positioning, roadmap)
- faion-ux-ui-designer (design for marketing)

## Coordination Patterns

### Single Sub-Skill Tasks
Route directly to the appropriate sub-skill for focused execution.

### Multi-Sub-Skill Workflows
For complex marketing programs, coordinate multiple sub-skills:

1. **Sequential** - GTM strategy → content creation → distribution
2. **Parallel** - Content + paid ads + social media simultaneously
3. **Iterative** - Experiments → analysis → optimization → repeat

---

*Marketing Manager Orchestrator v2.1*
*Pure Orchestrator | 7 Sub-Skills | 85+ Methodologies*
