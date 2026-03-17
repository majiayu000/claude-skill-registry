---
name: stp-framework
description: Apply Segmentation, Targeting, and Positioning framework to identify market opportunities and craft differentiated positioning
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# STP Framework

> Apply the classic Segmentation, Targeting, Positioning framework to identify your most valuable market segments and craft differentiated positioning.

## When to Use This Skill

- New product launches
- Market entry strategy
- Repositioning initiatives
- Competitive strategy
- Marketing planning

## Methodology Foundation

Based on **Kotler's STP Model** and **Michael Porter's competitive strategy**, providing:
- Market segmentation techniques
- Segment attractiveness criteria
- Targeting strategy options
- Positioning development

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures segmentation analysis | Segmentation variables |
| Evaluates segment attractiveness | Target selection |
| Develops positioning options | Final positioning |
| Creates positioning statements | Resource allocation |
| Maps competitive positions | Go-to-market approach |

## Instructions

### Step 1: Segmentation

**Segmentation Variables:**

| Type | B2C Variables | B2B Variables |
|------|---------------|---------------|
| **Demographic** | Age, income, education | Company size, industry, revenue |
| **Geographic** | Region, urban/rural, climate | HQ location, market presence |
| **Psychographic** | Values, lifestyle, personality | Culture, decision style |
| **Behavioral** | Usage rate, loyalty, benefits sought | Buying process, use case |

**Effective Segment Criteria:**
| Criterion | Question |
|-----------|----------|
| Measurable | Can we size and quantify it? |
| Accessible | Can we reach and serve it? |
| Substantial | Is it large enough to be profitable? |
| Differentiable | Does it respond differently to marketing? |
| Actionable | Can we develop effective programs? |

### Step 2: Targeting

**Targeting Strategies:**

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Mass** | Target entire market | Commodity products |
| **Differentiated** | Target multiple segments differently | Resources for variety |
| **Concentrated** | Focus on one segment | Limited resources |
| **Micromarketing** | Individual customization | High-value customers |

**Segment Evaluation Matrix:**

| Factor | Weight | How to Assess |
|--------|--------|---------------|
| Size | 20% | TAM/SAM/SOM |
| Growth | 20% | CAGR, trends |
| Profitability | 20% | Margins, price sensitivity |
| Competition | 15% | Intensity, barriers |
| Fit | 15% | Capabilities, mission |
| Accessibility | 10% | Channel, reach |

### Step 3: Positioning

**Positioning Statement Template:**
```
For [target segment]
Who [need/problem]
[Product/Brand] is the [category]
That [key benefit]
Unlike [competitors]
We [key differentiator]
```

**Positioning Dimensions:**
- Attributes (features, specs)
- Benefits (functional, emotional)
- Values (what brand stands for)
- Use occasions (when to use)
- Users (who uses it)
- Against competitors (explicit comparison)

## Examples

### Example 1: Complete STP Analysis

**Input:**
```
Develop STP strategy for:
- Product: AI writing assistant
- Current customers: Mix of freelancers and enterprises
- Competitors: Jasper, Copy.ai, ChatGPT
```

**Output:**
```
## STP Analysis: AI Writing Assistant

### PART 1: SEGMENTATION

#### Market Segmentation Map

```
                     PROFESSIONAL USE
                           │
           Enterprise      │      Agency
           Marketing   ────┼────  Teams
              │            │         │
    Low ──────┼────────────┼─────────┼────── High
    Tech      │            │         │       Tech
    Savvy     │            │         │       Savvy
              │            │         │
           Content      ───┼───   Individual
           Creators        │      Professionals
                           │
                     PERSONAL USE
```

#### Segment Profiles

##### Segment A: Enterprise Marketing Teams

| Attribute | Profile |
|-----------|---------|
| Company size | 500+ employees |
| Department | Marketing, Content |
| Budget | $50K+/year for tools |
| Users | 5-50 per company |
| Need | Scale content, brand consistency |
| Behavior | Long sales cycle, procurement |

**Jobs to Be Done:**
- Produce more content without more headcount
- Maintain brand voice across team
- Speed up content approval workflows

**Pains:**
- Content bottleneck at scale
- Inconsistent brand voice
- Slow review/approval cycles

---

##### Segment B: Agency Teams

| Attribute | Profile |
|-----------|---------|
| Company size | 10-200 employees |
| Type | Creative, marketing, content agencies |
| Budget | $10-50K/year |
| Users | 5-20 |
| Need | Efficiency, client variety |
| Behavior | Multiple clients, fast turnaround |

**Jobs to Be Done:**
- Serve more clients without proportional hiring
- Switch between client voices easily
- Draft faster, edit better

**Pains:**
- Client variety requires context switching
- Margin pressure from fixed-fee projects
- Quality vs. speed tradeoff

---

##### Segment C: Individual Professionals

| Attribute | Profile |
|-----------|---------|
| Company size | 1-10 (solopreneurs, SMB) |
| Role | Founders, marketers, content creators |
| Budget | $20-500/month |
| Users | 1-5 |
| Need | Punch above weight |
| Behavior | Fast decision, self-serve |

**Jobs to Be Done:**
- Write professional content without writing skills
- Produce content volume of larger team
- Save time on first drafts

**Pains:**
- Limited time for content creation
- Can't afford dedicated writer
- Writer's block, blank page fear

---

##### Segment D: Content Creators

| Attribute | Profile |
|-----------|---------|
| Type | Bloggers, YouTubers, course creators |
| Budget | $10-100/month |
| Users | 1 |
| Need | Overcome creative blocks |
| Behavior | Price sensitive, try before buy |

**Jobs to Be Done:**
- Generate ideas quickly
- Repurpose content across formats
- Maintain publishing cadence

**Pains:**
- Creative burnout
- Platform algorithm pressure
- Time vs. quality tradeoff

---

### PART 2: TARGETING

#### Segment Evaluation

| Segment | Size | Growth | Profit | Competition | Fit | Score |
|---------|------|--------|--------|-------------|-----|-------|
| Enterprise | 8 | 7 | 9 | 6 | 7 | **7.4** |
| Agency | 7 | 8 | 7 | 7 | 8 | **7.4** |
| Individual Pro | 9 | 9 | 5 | 4 | 8 | **7.0** |
| Content Creator | 8 | 7 | 3 | 3 | 5 | **5.2** |

**Evaluation Notes:**

| Segment | Strengths | Weaknesses |
|---------|-----------|------------|
| Enterprise | High LTV, lower churn | Long sales cycle, complex |
| Agency | Multi-seat, expansion | Price sensitive, churn |
| Individual Pro | Large volume, fast sales | Low ARPU, high support |
| Content Creator | Viral potential | Very low ARPU, high churn |

---

#### Recommended Targeting Strategy

**Primary Target:** Agency Teams
- Best combination of ARPU and accessibility
- Multi-seat expansion opportunity
- Word-of-mouth potential (agencies talk)
- Faster sales cycle than enterprise

**Secondary Target:** Enterprise Marketing
- Upmarket opportunity
- Higher ARPU offsets longer cycle
- Build case studies for credibility

**Serve but don't focus:** Individual Professionals
- Self-serve tier drives volume
- Potential upgrade to agency/enterprise
- Lower priority for resources

**Deprioritize:** Content Creators
- Lowest ARPU, highest churn
- Heavy competition
- Not worth dedicated focus

---

### PART 3: POSITIONING

#### Competitive Positioning Map

```
            EASE OF USE
                 │
    Simple  ─────┼───── Complex
                 │
         ┌───────┼────────┐
         │       │  Us    │
         │ ChatGPT (target)│
         │       │        │
         │       │ Jasper │
GENERIC ─┼───────┼────────┼─ SPECIALIZED
         │       │        │
         │Copy.ai│        │
         │       │        │
         └───────┴────────┘
                 │
    Basic   ─────┴───── Advanced
            MARKETING FEATURES
```

#### Positioning Options

**Option 1: Agency Productivity**
```
For marketing agencies
Who struggle to scale content without scaling headcount
[Product] is the AI writing platform
That multiplies your team's output with consistent quality
Unlike ChatGPT (generic) or Jasper (solo-focused)
We're built for teams serving multiple clients
```

**Option 2: Brand Voice at Scale**
```
For marketing teams managing multiple brands
Who need consistent voice across all content
[Product] is the AI writing assistant
That learns and maintains your brand voice
Unlike generic AI tools
We sound like you, not like a robot
```

**Option 3: Draft-to-Done Speed**
```
For content professionals under deadline pressure
Who spend too much time on first drafts
[Product] is the AI writing accelerator
That gets you from blank page to publishable 5x faster
Unlike basic AI generators
We understand marketing, not just language
```

---

#### Recommended Positioning

**For Agency Primary Target:**

> **[Product] is the AI content platform for agencies that
> need to scale without sacrificing quality.**
>
> We help agency teams:
> - Produce more content with the same team
> - Maintain distinct brand voices across clients
> - Go from brief to draft in minutes, not hours
>
> Unlike generic AI tools, we're built for teams serving
> multiple clients—with workspaces, collaboration, and
> brand voice memory that makes switching contexts seamless.

---

#### Positioning Proof Points

| Claim | Proof |
|-------|-------|
| Scale without hiring | "3x content output with same team" |
| Brand voice consistency | "99% brand voice match" |
| Brief to draft speed | "First draft in 10 minutes" |
| Built for agencies | Multi-client workspace, brand profiles |

---

### Implementation Summary

| Element | Decision |
|---------|----------|
| **Primary segment** | Agency Teams |
| **Secondary segment** | Enterprise Marketing |
| **Positioning** | AI content platform for agencies |
| **Key differentiator** | Multi-client, brand voice memory |
| **Main proof point** | "3x output, same team" |
```

### Example 2: Quick Positioning Assessment

**Input:**
```
Assess this positioning:
"For busy professionals who want to eat healthy,
MealPrep is the meal kit that takes 15 minutes,
unlike HelloFresh which takes 30+ minutes."
```

**Output:**
```
## Positioning Assessment

### Current Statement Analysis

| Element | Current | Assessment |
|---------|---------|------------|
| Target | Busy professionals | ✅ Clear |
| Need | Want to eat healthy | ✅ Clear |
| Category | Meal kit | ✅ Clear |
| Benefit | 15 minutes | ✅ Specific |
| Competitor | HelloFresh | ✅ Named |
| Differentiator | Time (15 vs 30) | ⚠️ Single dimension |

### Strengths
- Clear target segment
- Specific, measurable benefit
- Direct competitive comparison

### Weaknesses
1. **Single differentiator** - Time alone is copyable
2. **"Healthy" undefined** - What does healthy mean?
3. **No emotional benefit** - Only functional
4. **Price not addressed** - Key for meal kits

### Improved Positioning

```
For time-strapped professionals who won't compromise on nutrition,
MealPrep is the 15-minute meal kit
That delivers chef-quality healthy meals
Without the prep, cleanup, or guilt
Unlike traditional meal kits that feel like a second job
We've done the hard work so dinner feels effortless
```

### Key Changes
1. Added emotional benefit ("won't compromise")
2. Expanded "healthy" to "chef-quality healthy"
3. Added cleanup benefit (compounds time savings)
4. Emotional framing ("second job" → "effortless")
```

## Skill Boundaries

### What This Skill Does Well
- Structuring segmentation analysis
- Evaluating segment attractiveness
- Developing positioning options
- Creating positioning statements

### What This Skill Cannot Do
- Research your actual market
- Know your competitive landscape
- Validate positioning with customers
- Guarantee market success

## Iteration Guide

**Follow-up Prompts:**
- "Segment [market] using [variable]"
- "Evaluate these segments for targeting"
- "Develop positioning against [competitor]"
- "Create messaging for [segment]"

## References

- Philip Kotler - Marketing Management
- Michael Porter - Competitive Strategy
- Al Ries & Jack Trout - Positioning
- Byron Sharp - How Brands Grow

## Related Skills

- `positioning` - April Dunford method
- `competitive-analysis` - Deep competitive dive
- `icp-matching` - Customer fit scoring

## Skill Metadata

- **Domain**: Strategy
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 2-4 hours for full analysis
- **Prerequisites**: Market knowledge, customer data
