---
name: idea-generation
description: Product idea generation and business validation specialist. Use when brainstorming ideas, validating business concepts, analyzing market opportunities, or evaluating product-market fit. Triggers on "idea generation", "business validation", "market analysis", "competitive research".
allowed-tools: Read, Write, Edit, Grep, Glob
model: inherit
---

# Idea Generation Skill - Business Idea Validation & Market Analysis

This Skill helps generate, validate, and refine product ideas using proven PM frameworks and templates.

## When to Use This Skill

Use this Skill when you need to:
- Generate new product or feature ideas
- Validate business concepts
- Analyze market opportunities
- Research competition
- Evaluate product-market fit
- Create Lean Canvas
- Assess problem-solution fit

## Core Process

### Step 1: Idea Extraction

From user input, identify:
- **Core Concept**: What is the product/feature?
- **Problem**: What problem does it solve?
- **Target Users**: Who experiences this problem?
- **Value Proposition**: Why is this solution better?

If information is missing, ask targeted questions:
- "What specific problem are you trying to solve?"
- "Who experiences this problem most acutely?"
- "What alternatives exist today?"
- "Why is now the right time for this solution?"

### Step 2: Use Reference Templates

**Always read these templates first:**

```bash
# Use Read tool to access:
/reference/idea-templates/lean-canvas-template.md
/reference/idea-templates/problem-solution-fit.md
/reference/idea-templates/market-analysis-guide.md
```

These templates provide:
- Lean Canvas structure
- Problem-Solution Fit framework
- Market sizing methodology (TAM/SAM/SOM)
- Competitive analysis templates
- PESTLE analysis guide
- Customer persona templates

### Step 3: Apply Frameworks

#### Lean Canvas

Fill out all 9 boxes:

1. **Problem (Top 3)**
   - What are the biggest problems?
   - Existing alternatives people use today

2. **Customer Segments**
   - Early adopters (who needs this most?)
   - User persona details

3. **Unique Value Proposition**
   - Single, clear, compelling message
   - High-level concept ("X for Y")

4. **Solution (Top 3 Features)**
   - Minimum features to solve the problem
   - MVP scope

5. **Channels**
   - How to reach customers
   - Inbound vs outbound strategies

6. **Revenue Streams**
   - How to make money
   - Pricing model

7. **Cost Structure**
   - Fixed and variable costs
   - CAC (Customer Acquisition Cost)

8. **Key Metrics**
   - What to measure
   - Success indicators

9. **Unfair Advantage**
   - What can't be easily copied
   - Sustainable competitive advantage

#### Problem-Solution Fit

**Phase 1: Problem Identification**
- Problem statement (clear, specific)
- Who experiences it (target segment)
- When it occurs (context)
- Why it matters (pain level 1-10)

**Problem Validation:**
- Customer interviews needed (min. 10)
- Market research data
- Competitor analysis
- Evidence of pain severity

**Phase 2: Solution Design**
- Solution hypothesis
- MVP features (must-have only)
- Differentiation from alternatives

**Phase 3: Validation Plan**
- How to test with users
- Success criteria
- Metrics to track

#### Market Analysis

**Market Sizing (TAM/SAM/SOM):**

**TAM (Total Addressable Market):**
- Total market demand
- Calculation: Top-down or bottom-up
- Data sources: Industry reports, government stats

**SAM (Serviceable Available Market):**
- Portion of TAM you can reach
- Filter by geography, product fit, regulations

**SOM (Serviceable Obtainable Market):**
- Realistic market share (1-5 years)
- Consider competition, resources, GTM strategy

**Example:**
```
Product: AI Study Planner for College Students

TAM: $5B (Global edtech for higher education)
SAM: $500M (US college students, study tools segment)
SOM: $25M (5% market share in 3 years, 500K users × $50 ARPU)
```

**Competitive Analysis:**

Create comparison table:

| Competitor | Strengths | Weaknesses | Market Share | Pricing | Our Differentiation |
|------------|-----------|------------|--------------|---------|---------------------|
| Competitor A | Brand, features | Expensive | 40% | $20/mo | AI personalization |
| Competitor B | Free, simple | Limited features | 30% | Free | Premium features |
| Competitor C | Mobile-first | No web app | 20% | $10/mo | Cross-platform |

**PESTLE Analysis:**

- **Political**: Regulations, policies
- **Economic**: GDP, unemployment, inflation
- **Social**: Demographics, lifestyle trends
- **Technological**: Innovation, automation
- **Legal**: Laws, compliance
- **Environmental**: Sustainability, climate

**Persona Creation:**

```markdown
## Persona: [Name]

### Demographics
- Age: 20-24
- Location: US, urban areas
- Education: Undergraduate
- Income: $0-20K (part-time work)

### Goals
- Graduate with good GPA
- Balance studies with social life
- Prepare for career

### Pain Points
- Overwhelmed by multiple deadlines
- Poor time estimation
- Procrastination
- Lack of study structure

### Current Solutions
- Google Calendar (too manual)
- Physical planner (easy to lose track)
- Sticky notes (disorganized)

### Technology
- Proficiency: High
- Devices: Laptop, smartphone
- Apps used: Notion, Spotify, Instagram

### Quote
"I know what I need to do, I just can't figure out when to do it all."

### Jobs-to-be-Done
When I have multiple assignments due,
I want an automated study plan,
So I can focus on learning instead of planning.
```

### Step 4: Generate Validation Report

**Output Structure:**

```markdown
# [Product Name] - Idea Validation Report

## Executive Summary
[2-3 sentences: What it is, who it's for, why it matters]

## Problem Statement
**Problem:** [Clear, specific description]
**Who:** [Target users]
**Pain Level:** [X/10]
**Frequency:** [How often]
**Current Alternatives:** [What people use today]

## Solution Overview
**Core Solution:** [How it solves the problem]
**Key Features:**
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

**Differentiation:** [What makes this unique]

## Market Opportunity
### Market Size
- TAM: $X billion
- SAM: $Y million
- SOM: $Z million (realistic 3-year target)

### Market Trends
- [Trend 1: Growth driver]
- [Trend 2: Tailwind]
- [Trend 3: Opportunity]

### Customer Segments
[Persona details]

## Competitive Landscape
[Comparison table]

**Our Positioning:** [Where we fit in the market]

## Business Model
**Revenue Streams:**
- [Primary: Subscription at $X/month]
- [Secondary: Premium features]

**Unit Economics (Projected):**
- LTV: $X (based on Y month retention, $Z ARPU)
- CAC: $A (via B channels)
- LTV/CAC: C:1 [Target: 3:1+]
- Payback: D months [Target: <12]

**Pricing Strategy:**
- Freemium with premium tier
- Free: [Basic features]
- Pro: $X/month [Advanced features]
- Benchmark: [Compared to competitors]

## Validation Plan
**Next Steps:**
1. Customer Interviews (Target: 20 interviews)
   - Script: [Key questions]
   - Timeline: [2 weeks]

2. MVP Development
   - Features: [Minimum viable features]
   - Timeline: [6-8 weeks]

3. Beta Testing
   - Users: [50-100 early adopters]
   - Success Metrics: [Activation rate >40%, retention >30%]

4. Go/No-Go Decision
   - Criteria: [Problem validated, users willing to pay, NPS >30]
   - Timeline: [3 months from now]

## Risk Assessment
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Low user adoption | Medium | High | Validate with interviews first |
| Strong competition | High | Medium | Focus on differentiation |
| Technical complexity | Low | Medium | Prototype early |
| Market timing | Low | High | Launch MVP quickly |

## Success Metrics
**Phase 1: Validation (Month 1-3)**
- 20 customer interviews completed
- Problem validated by 80%+ of interviewees
- 100 beta signups

**Phase 2: MVP (Month 4-6)**
- 1,000 signups
- 40% activation rate
- 30% Day-7 retention
- NPS >30

**Phase 3: Growth (Month 7-12)**
- 10,000 active users
- 20% MoM growth
- 10% free-to-paid conversion
- $10K MRR

## Go/No-Go Recommendation
**Recommendation:** [GO / NO-GO / PIVOT]

**Reasoning:**
- [Strength 1]
- [Strength 2]
- [Risk 1 to address]

**Confidence Level:** [High / Medium / Low]

**Suggested Next Action:**
[Specific, actionable next step]
```

## Best Practices

### For Idea Generation
✅ **Do:**
- Start with a clear problem statement
- Validate problem before solution
- Research existing alternatives thoroughly
- Talk to real potential users
- Be specific about target segment
- Estimate market size realistically
- Consider business model early

❌ **Don't:**
- Fall in love with solution before validating problem
- Claim "no competitors" (there are always alternatives)
- Overestimate market size
- Skip customer research
- Ignore unit economics
- Build for everyone (too broad)

### For Market Analysis
✅ **Do:**
- Use multiple data sources (triangulate)
- Cite sources for market size
- Analyze both direct and indirect competitors
- Identify market trends (tailwinds/headwinds)
- Consider regulatory environment
- Assess timing (why now?)

❌ **Don't:**
- Rely on single source for TAM
- Ignore competitive threats
- Assume unlimited market
- Overlook barriers to entry
- Forget about market timing

### For Validation
✅ **Do:**
- Define clear success criteria
- Plan systematic customer research
- Test riskiest assumptions first
- Set realistic timelines
- Identify metrics to track
- Plan go/no-go decision points

❌ **Don't:**
- Skip validation (build first, ask later)
- Only talk to friends/family
- Ask leading questions
- Ignore negative feedback
- Confuse "nice idea" with "would pay"

## Output Guidelines

**Format:**
- Markdown with clear headings
- Tables for comparisons
- Bullet points for clarity
- Bold for key insights
- Data-driven (cite sources)

**Tone:**
- Objective and balanced
- Realistic, not overly optimistic
- Data-driven, not speculative
- Actionable recommendations

**Length:**
- Executive Summary: 2-3 sentences
- Full Report: 5-10 pages
- Each section: Comprehensive but concise

## Example Usage

**User Input:**
"I want to build an app that helps remote workers find co-working buddies"

**Skill Activation:**
1. Read reference templates
2. Ask clarifying questions:
   - "What specific problem do remote workers have with working alone?"
   - "How do they currently find co-working buddies?"
   - "What would make them choose your app over just using social media?"
3. Apply Lean Canvas framework
4. Conduct market sizing
5. Research competitors (existing apps, social platforms, co-working spaces)
6. Create persona (remote worker profile)
7. Generate comprehensive validation report
8. Provide go/no-go recommendation

**Output:**
Complete Idea Validation Report with all sections filled, data-backed, and actionable.

---

## Integration Points

This Skill works with:
- **idea-agent**: Provides framework expertise for idea validation
- **pm-knowledge-base**: Uses frameworks like Lean Canvas, JTBD, RICE
- **prd-agent**: Hands off validated idea for PRD creation

Always reference `/reference/idea-templates/` files for latest templates and frameworks.
