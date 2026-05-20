---
name: skill-orchestrator
description: "Route to the optimal sequence of skills for any marketing, product, or business challenge. Stop using one skill at a time—orchestrate intelligent workflows that compound results. Use when: **Starting a new project** to determine the optimal skill sequence; **Complex multi-faceted challenges** that require multiple frameworks; **Team alignment** to agree on a structured approach; **When overwhelmed by options** to cut through skill paralysis; **Teaching structured thinking** to show how framew..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Skill Orchestrator

> Route to the optimal sequence of skills for any marketing, product, or business challenge. Stop using one skill at a time—orchestrate intelligent workflows that compound results.

## When to Use This Skill

- **Starting a new project** to determine the optimal skill sequence
- **Complex multi-faceted challenges** that require multiple frameworks
- **Team alignment** to agree on a structured approach
- **When overwhelmed by options** to cut through skill paralysis
- **Teaching structured thinking** to show how frameworks connect
- **Maximizing Claude's capabilities** to get more value from the skill library

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | MKTG Skills orchestration system |
| **Core Principle** | "The value isn't in individual skills—it's in intelligent sequencing. The right frameworks in the right order compound insights." |
| **Why This Matters** | Using one skill at a time is like using one tool for every job. Real problems require multiple perspectives and frameworks that build on each other. |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Analyzes your challenge** - Understands what you're really trying to accomplish
2. **Recommends skill sequences** - Identifies which skills, in what order
3. **Orchestrates workflows** - Guides you through multi-skill processes
4. **Captures handoffs** - Passes outputs from one skill as inputs to the next
5. **Suggests pre-built workflows** - Offers tested sequences for common scenarios
6. **Customizes sequences** - Adapts workflows to your specific context

## How to Use

### Get Skill Recommendations for a Challenge
```
I need help with: [describe your challenge]
My context: [industry, stage, constraints]
What skills should I use, and in what order?
```

### Use a Pre-Built Workflow
```
Run the [workflow-name] workflow for: [your specific case]
```

### Customize a Workflow
```
I want to run the [workflow-name] workflow but:
- Skip [step] because [reason]
- Add [skill] because [need]
- Adapt for [specific context]
```

---

## Pre-Built Workflows

### Workflow 1: Product Launch
**Use when:** Launching a new product, feature, or service
**Total skills:** 8
**Time estimate:** 4-6 hours of work

```yaml
workflow: product-launch
name: "Full Product Launch Sequence"
steps:
  1. first-principles:
     purpose: "Challenge assumptions about your market and offering"
     output: "List of validated truths vs. conventions to challenge"

  2. inversion:
     purpose: "Identify what could cause failure"
     output: "Anti-goals to avoid, risk mitigation strategies"

  3. buyer-personas (or persona-generator):
     purpose: "Define who you're launching to"
     input: "Use first-principles insights to challenge demographic assumptions"
     output: "2-3 behavior-based personas with JTBD"

  4. positioning:
     purpose: "Differentiate your offering"
     input: "Use personas to understand competitive alternatives"
     output: "Positioning statement and competitive frame"

  5. grand-slam-offers:
     purpose: "Create irresistible offer structure"
     input: "Use positioning to inform value stack"
     output: "Complete offer with bonuses, guarantees, urgency"

  6. pre-mortem:
     purpose: "Stress-test the launch plan"
     input: "Challenge the offer and positioning"
     output: "Updated plan with mitigations"

  7. launch-formula:
     purpose: "Sequence the launch mechanics"
     output: "Pre-launch, launch, post-launch timeline"

  8. six-thinking-hats:
     purpose: "Final validation from all perspectives"
     output: "Go/no-go decision with confidence"
```

---

### Workflow 2: Customer Validation (YC-Style)
**Use when:** Validating a business idea before building
**Total skills:** 5
**Time estimate:** 2-3 hours prep + interview time

```yaml
workflow: customer-validation
name: "YC-Style Customer Validation"
steps:
  1. jobs-to-be-done:
     purpose: "Understand what progress customers seek"
     output: "Job statements and forces diagram"

  2. persona-generator:
     purpose: "Create hypothesis personas to validate"
     input: "Use JTBD to define behavior-based segments"
     output: "2-3 personas with interview questions"

  3. mom-test:
     purpose: "Prepare non-leading customer questions"
     input: "Generate questions for each persona"
     output: "Interview script and commitment tests"

  4. objection-mapping:
     purpose: "Anticipate why they might not buy"
     input: "Based on JTBD anxieties"
     output: "Objection map with responses"

  5. lean-canvas:
     purpose: "Document and track hypotheses"
     output: "One-page model with riskiest assumptions flagged"
```

**After interviews, add:**
```yaml
  6. pricing-validation:
     purpose: "Test willingness to pay"
     input: "Insights from mom-test interviews"
     output: "Price range and pricing model recommendation"
```

---

### Workflow 3: Content Strategy
**Use when:** Planning a content marketing initiative
**Total skills:** 6
**Time estimate:** 3-4 hours

```yaml
workflow: content-creation
name: "Strategic Content Development"
steps:
  1. audience-research:
     purpose: "Understand who you're creating for"
     output: "Audience insights, pain points, questions"

  2. content-strategy:
     purpose: "Plan content pillars and calendar"
     input: "Match content to audience needs"
     output: "Content plan with pillar topics"

  3. copywriting-schwartz:
     purpose: "Match content to awareness level"
     input: "Segment content by awareness stage"
     output: "Content approach per awareness level"

  4. headline-formulas:
     purpose: "Create compelling entry points"
     output: "5-10 headlines per piece"

  5. copy-frameworks:
     purpose: "Structure the content"
     output: "Framework selection per content piece"

  6. cta-writing:
     purpose: "Convert readers to action"
     output: "CTAs matched to content goals"
```

---

### Workflow 4: Competitive Positioning
**Use when:** Entering a crowded market or repositioning
**Total skills:** 5
**Time estimate:** 2-3 hours

```yaml
workflow: competitive-positioning
name: "Competitive Differentiation"
steps:
  1. competitive-analysis:
     purpose: "Map the competitive landscape"
     output: "Competitor matrix, positioning map"

  2. first-principles:
     purpose: "Challenge category assumptions"
     output: "Conventions that can be challenged"

  3. category-design:
     purpose: "Consider creating a new category"
     output: "Category POV and naming options"

  4. positioning:
     purpose: "Define your unique position"
     input: "Use competitive gaps and category insights"
     output: "Positioning statement"

  5. value-proposition-canvas:
     purpose: "Align position with customer needs"
     output: "Value map matched to customer profile"
```

---

### Workflow 5: Sales Enablement
**Use when:** Preparing sales team for a new product/market
**Total skills:** 5
**Time estimate:** 3-4 hours

```yaml
workflow: sales-enablement
name: "Sales Playbook Development"
steps:
  1. persona-generator:
     purpose: "Understand who sales will talk to"
     output: "Buyer personas with decision criteria"

  2. objection-mapping:
     purpose: "Prepare for pushback"
     output: "Complete objection map with responses"

  3. sales-pitch-dunford:
     purpose: "Structure the sales conversation"
     output: "Sales pitch deck/talk track"

  4. positioning:
     purpose: "Nail the competitive differentiation"
     output: "Competitive positioning for sales"

  5. grand-slam-offers:
     purpose: "Structure the deal"
     output: "Offer structure with value stack"
```

---

### Workflow 6: Decision Making
**Use when:** Making a major strategic decision
**Total skills:** 5
**Time estimate:** 2 hours

```yaml
workflow: strategic-decision
name: "Structured Decision Making"
steps:
  1. first-principles:
     purpose: "Challenge assumptions about the decision"
     output: "True constraints vs. conventions"

  2. inversion:
     purpose: "Think about what could go wrong"
     output: "Ways to fail, what to avoid"

  3. pre-mortem:
     purpose: "Imagine failure and prevent it"
     output: "Risk register with mitigations"

  4. six-thinking-hats:
     purpose: "Examine from all perspectives"
     output: "Multi-perspective analysis"

  5. eisenhower-matrix:
     purpose: "Prioritize actions"
     output: "Prioritized action list"
```

---

### Workflow 7: AI Video Production
**Use when:** Creating video content using AI tools (ads, promos, social content)
**Total skills:** 5
**Time estimate:** 4-8 hours depending on complexity
**Source:** PJ Ace method (233M Views David Beckham workflow)

```yaml
workflow: ai-video-production
name: "AI Video Ad Production (PJ Ace Method)"
steps:
  1. ai-video-concept:
     purpose: "Develop creative idea and structured script"
     output: "Script with 8-second scenes, voiceover + visual descriptions"

  2. ai-storyboard-2x2:
     purpose: "Create visual storyboard with 2x2 grid consistency"
     input: "Script scenes from step 1"
     output: "Figma board with sequenced frames, transition plan"

  3. ai-video-prompting:
     purpose: "Generate animation prompts for Veo/Runway/Kling/Pika"
     input: "Storyboard frames"
     output: "Optimized prompts per model, animated clips"

  4. ai-voice-design:
     purpose: "Design and generate voice for narration/dialogue"
     input: "Script dialogue"
     output: "TTS audio files (ElevenLabs or Qwen3-TTS)"

  5. ai-video-qa:
     purpose: "Quality assurance before publication"
     input: "Assembled video draft"
     output: "QA report, go/no-go decision, fixes list"
```

**When to use this workflow:**
- Creating AI-generated video ads
- Social media video content (TikTok, Reels, YouTube Shorts)
- Explainer videos with AI visuals
- Product demos with stylized visuals
- Any video where AI generation is appropriate for the brand

**When NOT to use:**
- Heritage/legacy brands with high expectations (risk too high)
- Content requiring perfect photorealism of real people
- Videos with complex hand/finger interactions
- Emotional content requiring subtle human expressions

---

## Instructions

When helping users orchestrate skills, follow this process:

### Step 1: Understand the Challenge

```
## Challenge Analysis

**What are you trying to accomplish?**
[ ] Launch something new
[ ] Validate an idea
[ ] Create content
[ ] Make a decision
[ ] Improve positioning
[ ] Enable sales
[ ] Solve a problem
[ ] Other: _______________

**What's your context?**
- Stage: [Idea / Early / Growth / Mature]
- Resources: [Solo / Small team / Large team]
- Timeline: [Urgent / Normal / Flexible]
- Constraints: [Budget / Time / People / Other]

**What do you already have?**
- [ ] Customer research/interviews
- [ ] Competitive analysis
- [ ] Existing positioning
- [ ] Content/copy
- [ ] Data/metrics
- [ ] Team alignment
```

---

### Step 2: Match to Workflow or Custom Sequence

```
## Workflow Selection

### If challenge matches a pre-built workflow:
1. Recommend the workflow
2. Explain why it fits
3. Offer to customize if needed
4. Proceed step by step

### If challenge is unique:
1. Identify the core components needed
2. Select skills that address each component
3. Sequence them logically (insights → decisions → execution)
4. Create custom workflow
```

**Sequencing Logic:**

| Phase | Skill Types | Purpose |
|-------|-------------|---------|
| **1. Foundation** | First-principles, JTBD, Audience research | Understand reality |
| **2. Analysis** | Competitive, Inversion, Pre-mortem | Identify challenges |
| **3. Strategy** | Positioning, Category design, Personas | Make strategic choices |
| **4. Creation** | Offers, Copy, Content | Build the thing |
| **5. Validation** | Six hats, Pricing validation, QA | Stress test |
| **6. Execution** | Launch formula, Sales pitch | Go to market |

---

### Step 3: Execute Step by Step

```
## Workflow Execution Template

### Current Workflow: [Name]
**Challenge:** [Description]

---

## Step [N]: [Skill Name]

**Purpose:** [Why this step matters]

**Inputs from previous steps:**
- [Output from Step N-1]
- [Any other inputs]

**Key questions to answer:**
1. [Question]
2. [Question]
3. [Question]

---

[Execute skill here - full skill content]

---

**Step [N] Outputs:**
- [Key output 1]
- [Key output 2]
- [Key output 3]

**Handoff to Step [N+1]:**
These outputs will inform [next step] by [how they connect].

---

## Progress Tracker

| Step | Skill | Status | Key Output |
|------|-------|--------|------------|
| 1 | [Skill] | ✅ Done | [Output] |
| 2 | [Skill] | 🔄 Current | |
| 3 | [Skill] | ⏳ Pending | |
```

---

### Step 4: Capture Cross-Skill Insights

```
## Cross-Skill Synthesis

### Patterns Emerging
- [Pattern seen across multiple skills]
- [Recurring theme or insight]
- [Connection between frameworks]

### Conflicts to Resolve
- [Skill A says X, Skill B says Y]
- [Resolution approach]

### Strongest Insights
1. [Insight from Step X + Y combined]
2. [Insight that wouldn't emerge from one skill alone]

### Recommendations
Based on the full workflow:
1. [Recommendation]
2. [Recommendation]
3. [Recommendation]
```

---

## Examples

### Example 1: Orchestrating a Product Launch

**Input:**
> "I'm launching a new AI writing tool for marketers. Help me orchestrate the right skills."

**Output:**

**Challenge Analysis:**
- Type: Product Launch
- Stage: Early (pre-launch)
- Context: New product, competitive market (Jasper, Copy.ai)

**Recommended Workflow: Product Launch (Modified)**

Since you're in a competitive market, I'm adding competitive analysis early:

```
Modified Product Launch Workflow

1. competitive-analysis → Understand the landscape
2. first-principles → Challenge AI writing tool assumptions
3. persona-generator → Define who specifically (not "marketers")
4. category-design → Can you own a new category?
5. positioning → Differentiate in crowded market
6. grand-slam-offers → Create irresistible offer
7. pre-mortem → What could kill the launch?
8. launch-formula → Sequence the mechanics
```

**Let's start Step 1:**

[Would proceed to execute competitive-analysis skill, then carry insights forward]

---

### Example 2: Custom Workflow Creation

**Input:**
> "I need to write a sales page for my course on financial planning for freelancers. What skills should I use?"

**Output:**

**Challenge Analysis:**
- Type: Content creation (sales copy)
- Product: Course
- Audience: Freelancers
- Goal: Conversions

**Custom Workflow: Sales Page Copy**

```yaml
workflow: sales-page-copy
steps:
  1. persona-generator:
     purpose: "Understand the freelancer buying this"
     questions: "What triggers them to seek financial help? What's their anxiety?"

  2. copywriting-schwartz:
     purpose: "Determine awareness level"
     question: "Are they problem-aware? Solution-aware? Product-aware?"

  3. grand-slam-offers:
     purpose: "Structure the offer"
     output: "Value stack, bonuses, guarantees, urgency"

  4. storytelling-storybrand:
     purpose: "Structure the narrative"
     output: "Hero's journey framework for the page"

  5. headline-formulas:
     purpose: "Create the hook"
     output: "5-10 headline options"

  6. landing-page-copy:
     purpose: "Write the page"
     input: "Use all previous outputs"
     output: "Complete sales page copy"

  7. cta-writing:
     purpose: "Convert readers"
     output: "CTAs throughout the page"
```

**Sequencing rationale:**
- Start with WHO (persona) and WHERE THEY ARE (awareness)
- Then WHAT you're selling (offer structure)
- Then HOW to tell the story (StoryBrand)
- Then WRITE (landing page copy, headlines, CTAs)

Want me to start with Step 1?

---

### Example 3: Partial Workflow

**Input:**
> "I've already done customer research and have personas. I need to figure out positioning and then create my launch strategy."

**Output:**

**Starting point:** Personas complete

**Remaining workflow:**

```
Positioning + Launch (Starting Mid-Workflow)

Input: Your existing personas
↓
1. competitive-analysis (if not done)
   → Need to understand alternatives before positioning

2. positioning
   → Using personas + competitive insights

3. grand-slam-offers
   → Structure the offer based on positioning

4. pre-mortem
   → Stress test before launch

5. launch-formula
   → Plan the launch sequence
```

**Skip competitive-analysis if:**
- You already know competitors well
- You've mapped the landscape recently

Let's start with positioning. First, tell me:
1. What are the top 3 alternatives your personas currently use?
2. What do you do differently from them?

---

## Skill Library Reference

### Thinking Skills
| Skill | Use For |
|-------|---------|
| first-principles | Challenging assumptions |
| inversion | Identifying failure modes |
| pre-mortem | Risk anticipation |
| six-thinking-hats | Multi-perspective analysis |
| eisenhower-matrix | Prioritization |

### Validation Skills
| Skill | Use For |
|-------|---------|
| mom-test | Customer interview prep |
| customer-discovery | Systematic validation |
| lean-canvas | Business model documentation |
| objection-mapping | Anticipating pushback |
| persona-generator | Creating research-based personas |

### Strategy Skills
| Skill | Use For |
|-------|---------|
| positioning | Differentiation |
| category-design | Creating new categories |
| jobs-to-be-done | Understanding customer needs |
| competitive-analysis | Landscape mapping |
| competitive-moats | Defensibility |
| pricing-strategy | Pricing decisions |
| buyer-personas | Audience definition |
| audience-research | Audience understanding |
| value-proposition-canvas | Value alignment |
| cognitive-biases | Understanding decisions |

### Content Skills
| Skill | Use For |
|-------|---------|
| copywriting-schwartz | Awareness-based copy |
| copywriting-ogilvy | Classic advertising principles |
| storytelling-storybrand | Narrative structure |
| headline-formulas | Creating headlines |
| copy-frameworks | AIDA, PAS, etc. |
| cta-writing | Call-to-action writing |
| landing-page-copy | Landing pages |
| email-writing | Email sequences |
| content-strategy | Content planning |
| content-writing | Long-form content |

### Sales/Offers Skills
| Skill | Use For |
|-------|---------|
| grand-slam-offers | Offer creation |
| sales-pitch-dunford | Sales conversations |
| launch-formula | Product launches |

### Branding Skills
| Skill | Use For |
|-------|---------|
| brand-strategy | Brand development |
| persuasion-cialdini | Influence principles |

### Video Skills (AI Production)
| Skill | Use For |
|-------|---------|
| ai-video-concept | Develop idea and structured script |
| ai-storyboard-2x2 | Create visual storyboard with 2x2 grid technique |
| ai-video-prompting | Generate prompts for Veo, Runway, Kling, Pika |
| ai-voice-design | Design and generate AI voices (ElevenLabs, Qwen3-TTS) |
| ai-video-qa | Quality assurance before publication |

---

## Checklists & Templates

### Workflow Planning Template

```
## Workflow: [Name]

**Challenge:** ________________________________

**Context:**
- Stage: [Idea / Early / Growth / Mature]
- Timeline: [Urgent / Weeks / Months]
- Resources: [Solo / Team]

**Skills Needed:**

| # | Skill | Purpose | Inputs | Outputs |
|---|-------|---------|--------|---------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

**Skip/Modify:**
- Skip [skill] because: _______________
- Modify [skill] for: _______________
```

---

### Workflow Progress Tracker

```
## [Workflow Name] Progress

**Started:** [Date]
**Challenge:** [Description]

| Step | Skill | Status | Key Output | Notes |
|------|-------|--------|------------|-------|
| 1 | | ⏳/🔄/✅ | | |
| 2 | | ⏳/🔄/✅ | | |
| 3 | | ⏳/🔄/✅ | | |

**Cross-Skill Insights:**
1.
2.
3.

**Final Recommendations:**
-
```

---

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- MKTG Skills library documentation
- Christensen, Clayton. "How Will You Measure Your Life?" - Job sequencing
- Rumelt, Richard. "Good Strategy Bad Strategy" - Strategic coherence
- Blank, Steve. "The Startup Owner's Manual" - Customer development sequence

## Related Skills

All skills in the library can be orchestrated. Key orchestration entry points:
- [first-principles](../../strategy/first-principles/) - Start here for foundation
- [lean-canvas](../lean-canvas/) - Start here for validation
- [positioning](../../strategy/positioning/) - Start here for differentiation
- [content-strategy](../../content/content-strategy/) - Start here for content
- [ai-video-concept](../../video/ai-video-concept/) - Start here for AI video production

---

## Skill Metadata (Internal Use)

```yaml
name: skill-orchestrator
category: meta
subcategory: orchestration
version: 1.1
author: MKTG Skills
source_expert: MKTG Skills System
source_work: Skills Library
difficulty: intermediate
estimated_value: $5,000 strategic consulting engagement
tags: [meta, orchestration, workflows, strategy, frameworks, sequencing]
created: 2026-01-25
updated: 2026-01-25
```
