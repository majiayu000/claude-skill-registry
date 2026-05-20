---
name: persona-generator
description: "Create research-backed buyer personas that drive real marketing and product decisions. Combine Buyer Personas methodology with Jobs-to-be-Done to build profiles based on actual behavior, not demographics fiction. Use when: **Starting customer discovery** to define who you're validating with; **Marketing campaign planning** to target the right messages to right people; **Content strategy** to create content that resonates with specific audiences; **Product roadmap prioritization** to build fea..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Persona Generator

> Create research-backed buyer personas that drive real marketing and product decisions. Combine Buyer Personas methodology with Jobs-to-be-Done to build profiles based on actual behavior, not demographics fiction.

## When to Use This Skill

- **Starting customer discovery** to define who you're validating with
- **Marketing campaign planning** to target the right messages to right people
- **Content strategy** to create content that resonates with specific audiences
- **Product roadmap prioritization** to build features for real users
- **Sales enablement** to help sales understand who they're talking to
- **Team alignment** to get everyone speaking the same customer language

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | Adele Revella - "Buyer Personas" (2015) + Clayton Christensen - Jobs-to-be-Done |
| **Core Principle** | "Buyer personas built on real research reveal the thinking behind buying decisions—not just demographics, but motivations, anxieties, and decision criteria." |
| **Why This Matters** | Most personas are demographic fiction ("Marketing Mary, 35, likes yoga"). Useful personas explain WHY someone buys—their anxieties, trigger events, and decision process. |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Generates research-based personas** - Built on behavior, not demographics
2. **Identifies buying triggers** - What events cause someone to seek a solution
3. **Maps decision criteria** - What factors drive the purchase decision
4. **Surfaces anxieties and barriers** - What stops them from buying
5. **Documents the buyer's journey** - How they research and decide
6. **Creates actionable segments** - Personas that drive real decisions

## How to Use

### Generate Personas from Customer Interviews
```
I've completed [X] customer interviews. Here are my notes: [summary]
Generate buyer personas using the Buyer Personas + JTBD methodology.
Focus on buying triggers, decision criteria, and anxieties.
```

### Create Hypothesis Personas (Pre-Research)
```
I'm building [product] for [market].
Generate hypothesis personas I should validate through customer discovery.
Include questions to ask to validate each persona.
```

### Analyze and Improve Existing Personas
```
Here are our current personas: [paste personas]
Analyze them against best practices.
What's missing? What questions should we research to make them useful?
```

## Instructions

When generating personas, follow this evidence-based methodology:

### Step 1: Understand What Makes Personas Useful

```
## The Persona Problem

### BAD Personas (Demographic Fiction)
"Marketing Mary"
- Age: 35
- Income: $80K
- Lives in suburbs
- Likes yoga and organic food
- Uses Instagram

**Why this fails:**
- Describes demographics, not motivations
- Doesn't explain why she would buy
- Can't drive marketing/product decisions
- Could describe millions of people

### GOOD Personas (Behavioral/JTBD-Based)
"The Overwhelmed First-Timer"
- **Trigger:** Just got promoted to manager, now responsible for [task]
- **Job-to-be-Done:** Make me look competent to my boss
- **Current Behavior:** Using spreadsheets, asking colleagues, stressed
- **Decision Criteria:** Easy to learn, makes me look good, won't fail publicly
- **Anxiety:** "What if I choose wrong and look incompetent?"

**Why this works:**
- Explains what triggered the search
- Reveals what they're really hiring the product to do
- Shows how they decide
- Surfaces what might stop them
- Drives specific marketing and product decisions
```

---

### Step 2: The Five Rings of Buying Insight

```
## Adele Revella's Five Rings

### Ring 1: PRIORITY INITIATIVE
**What event triggered their search?**

Questions to research:
- What was the trigger event?
- Why now vs. 6 months ago?
- What finally made this urgent?
- What was the breaking point?

Example insight:
"They start looking when they get a new boss who asks 'why don't we have...' or when a competitor does something that makes them look behind."

---

### Ring 2: SUCCESS FACTORS
**What outcome are they trying to achieve?**

Questions to research:
- What does success look like?
- How will they measure results?
- What would make them a hero internally?
- What would make them regret the decision?

Example insight:
"They don't actually want [product feature]. They want to be seen as innovative by their CEO while not risking a high-profile failure."

---

### Ring 3: PERCEIVED BARRIERS
**What could stop them from buying?**

Questions to research:
- What concerns came up during evaluation?
- What almost made them walk away?
- What would cause them to delay?
- What do they fear will go wrong?

Example insight:
"Their biggest fear isn't that it won't work—it's that their team won't use it and they'll have wasted budget on something that sits unused."

---

### Ring 4: DECISION CRITERIA
**How do they evaluate options?**

Questions to research:
- What features/capabilities are must-haves?
- How do they compare options?
- Who else influences the decision?
- What trade-offs are they willing to make?

Example insight:
"They create a spreadsheet comparing 3-5 options. Integration with existing stack is #1. If it doesn't connect to Salesforce, they won't consider it."

---

### Ring 5: BUYER'S JOURNEY
**How do they research and decide?**

Questions to research:
- How did they first learn about the category?
- What resources did they use to research?
- Who did they talk to?
- What was the decision timeline?

Example insight:
"They google '[category] vs [category]' then ask for recommendations in a Slack community. Reviews on G2 are the final checkpoint before talking to sales."
```

---

### Step 3: Add Jobs-to-be-Done Layer

```
## JTBD Analysis Per Persona

### The Job Statement
"When I [situation], I want to [motivation], so I can [expected outcome]."

### Three Types of Jobs

**Functional Job:** What they need to accomplish
- "I need to get this report done faster"
- "I need to track our campaigns across channels"

**Emotional Job:** How they want to feel
- "I want to feel confident presenting to the board"
- "I don't want to worry about this anymore"

**Social Job:** How they want to be perceived
- "I want my team to see me as innovative"
- "I don't want to look like I made a bad decision"

### Forces That Drive Switching

**Push (away from current):**
- Pain points with current solution
- Frustrations with status quo
- External pressures (boss, market, competition)

**Pull (toward new):**
- Desired outcomes
- Attractive features
- Vision of better future

**Anxiety (about switching):**
- Fear of failure
- Implementation concerns
- Uncertainty about claims

**Habit (keeping current):**
- Familiarity with status quo
- Sunk costs
- "Good enough" mentality

For a persona to buy: Push + Pull > Anxiety + Habit
```

---

### Step 4: Persona Template

```
## PERSONA: [Name Based on Behavior, Not Demographics]

### Snapshot
| Aspect | Detail |
|--------|--------|
| **Role** | [Job title / responsibility] |
| **Environment** | [Company size, industry, team structure] |
| **Primary JTBD** | [Job statement] |
| **Current Solution** | [What they use today] |

---

### Ring 1: Priority Initiative (Trigger)

**What triggers the search:**
- [Specific event 1]
- [Specific event 2]
- [Specific event 3]

**Why now (urgency drivers):**
- [What makes them act now vs. later]

**Quotes:**
> "[Verbatim from research]"

---

### Ring 2: Success Factors

**Desired outcomes:**
1. [Functional outcome]
2. [Emotional outcome]
3. [Social outcome]

**How they'll measure success:**
- [Metric or indicator]

**What makes them a hero:**
- [Internal win they're seeking]

**Quotes:**
> "[Verbatim from research]"

---

### Ring 3: Perceived Barriers

**Concerns/anxieties:**
1. [Concern about product/vendor]
2. [Concern about implementation]
3. [Concern about results]

**What almost stops them:**
- [Top barrier]

**Risk they fear most:**
- [What failure looks like]

**Quotes:**
> "[Verbatim from research]"

---

### Ring 4: Decision Criteria

**Must-haves (non-negotiable):**
1. [Feature/capability]
2. [Feature/capability]
3. [Feature/capability]

**Nice-to-haves:**
- [Feature/capability]

**Deal-breakers:**
- [What would eliminate you]

**How they compare:**
- [Their evaluation process]

**Quotes:**
> "[Verbatim from research]"

---

### Ring 5: Buyer's Journey

**Stage 1 - Trigger:** [What happens]
**Stage 2 - Research:** [Where they look]
**Stage 3 - Evaluate:** [How they compare]
**Stage 4 - Decide:** [Who's involved]
**Stage 5 - Buy:** [Process/procurement]

**Information sources:**
- [Channel 1]
- [Channel 2]
- [Influencers]

**Timeline:** [Typical decision timeframe]

---

### Jobs-to-be-Done

**Primary Job:**
"When I [situation], I want to [motivation], so I can [outcome]."

**Functional Job:** [What to accomplish]
**Emotional Job:** [How to feel]
**Social Job:** [How to be seen]

**Forces Analysis:**
| Force | Strength | Specifics |
|-------|----------|-----------|
| Push | High/Med/Low | [Details] |
| Pull | High/Med/Low | [Details] |
| Anxiety | High/Med/Low | [Details] |
| Habit | High/Med/Low | [Details] |

---

### Marketing Implications

**Messaging that resonates:**
- [Message/hook]
- [Message/hook]

**Content they'd engage with:**
- [Content type]
- [Content type]

**Where to reach them:**
- [Channel]
- [Channel]

**What NOT to say:**
- [Anti-message]

---

### Sales Implications

**Objections to expect:**
- [Objection]
- [Objection]

**Questions they'll ask:**
- [Question]
- [Question]

**Proof points they need:**
- [Case study/demo]

**Decision process:**
- [How deals close with this persona]
```

---

### Step 5: Validate and Update

```
## Persona Validation Checklist

### Is this persona based on evidence?
- [ ] Minimum 5 interviews with this type
- [ ] Includes verbatim quotes
- [ ] Describes behavior, not just demographics
- [ ] Explains WHY they buy

### Does this persona enable decisions?
- [ ] Marketing team can use it to target campaigns
- [ ] Product team can use it to prioritize features
- [ ] Sales team can use it to tailor conversations
- [ ] Content team can use it to create relevant assets

### Is this persona distinct?
- [ ] Clearly different from other personas
- [ ] Different triggers
- [ ] Different decision criteria
- [ ] Different objections/anxieties

### Red Flags (Persona Needs Work)
- [ ] Based on assumptions, not research
- [ ] All demographics, no behaviors
- [ ] No quotes from real customers
- [ ] Too vague to drive decisions
- [ ] Overlaps significantly with another persona
```

---

## Examples

### Example 1: B2B SaaS Personas

**Input:**
> "Generate personas for our marketing analytics dashboard. Target: marketing managers at 100-500 employee B2B companies. Price: $500/month."

**Output:**

## PERSONA 1: The Proving-ROI Manager

### Snapshot
| Aspect | Detail |
|--------|--------|
| **Role** | Marketing Manager, reports to VP/CMO |
| **Environment** | B2B SaaS, 100-300 employees, small marketing team (3-5) |
| **Primary JTBD** | Prove marketing's ROI to justify budget and headcount |
| **Current Solution** | Spreadsheets + GA + Hubspot reports (manual) |

---

### Ring 1: Priority Initiative (Trigger)

**What triggers the search:**
- CFO/CEO asks "what's the ROI on marketing spend?"
- Budget review coming up, needs to defend numbers
- New CMO joins and wants visibility into performance
- Competitor's marketing seems more effective, board asking questions

**Why now:**
- Annual planning cycle approaching
- Just missed a target and needs to explain why
- Growing pressure to be "data-driven"

**Quotes:**
> "My CFO asked me last week what our CAC is by channel. I had to spend a full day in spreadsheets to give him a rough estimate."

---

### Ring 2: Success Factors

**Desired outcomes:**
1. One dashboard that shows marketing ROI (functional)
2. Confidence presenting to leadership (emotional)
3. Seen as data-driven and strategic (social)

**How they'll measure success:**
- Time saved on reporting
- Ability to answer CFO questions immediately
- Cleaner attribution to defend spend

**What makes them a hero:**
- "This dashboard proved we should 2x our Google Ads budget"

---

### Ring 3: Perceived Barriers

**Concerns:**
1. Will my team actually use this? (adoption)
2. Is the data accurate? (trust)
3. How long to implement? (time)

**What almost stops them:**
- Integration complexity with existing stack
- Fear of seeing data they don't want to see

**Risk they fear:**
- "I buy this, it's wrong, and now I've given the CFO bad data"

**Quotes:**
> "We tried a dashboard before and the numbers never matched Hubspot. That was a disaster."

---

### Ring 4: Decision Criteria

**Must-haves:**
1. Integrates with Hubspot (or their CRM)
2. Connects to Google Ads + LinkedIn
3. Attribution modeling (not just last-click)

**Nice-to-haves:**
- Automated reports
- Benchmarks vs. industry

**Deal-breakers:**
- Manual data entry required
- No Hubspot integration
- Takes >2 weeks to implement

**How they compare:**
- Create comparison spreadsheet
- Check G2 reviews
- Need social proof from similar companies

---

### Ring 5: Buyer's Journey

1. **Trigger:** CFO asks hard question → realizes need
2. **Research:** Google "marketing attribution software", asks peers in Slack
3. **Evaluate:** Shortlists 3 options, demos each, checks integrations
4. **Decide:** Brings to boss, creates business case, budget approval
5. **Buy:** IT security review, procurement, signed

**Timeline:** 4-8 weeks from trigger to purchase

---

### Marketing Implications

**Messaging that resonates:**
- "Answer CFO questions in real-time"
- "Prove marketing ROI without spreadsheets"
- "Attribution you can trust"

**Where to reach them:**
- LinkedIn (Marketing Manager targeting)
- RevOps/Marketing Slack communities
- G2/Capterra (bottom of funnel)

**What NOT to say:**
- "Vanity metrics" (they want revenue, not impressions)
- "AI-powered" (skeptical of hype)

---

## PERSONA 2: The Accidental Analyst

### Snapshot
| Aspect | Detail |
|--------|--------|
| **Role** | Marketing Coordinator or Specialist, early career |
| **Environment** | B2B, 150-400 employees, reports to Marketing Manager |
| **Primary JTBD** | Get data to my boss without spending all week in spreadsheets |
| **Current Solution** | Export from 5 tools, combine in Excel, format in Slides |

---

### Ring 1: Priority Initiative

**What triggers the search:**
- Weekly report takes 4+ hours to create
- Boss asks for new data cut they can't easily produce
- Made an error in last report, got called out

**Quotes:**
> "Every Monday I dread the reporting. I spend half my day in Excel just pulling numbers together."

---

### Ring 2: Success Factors

**Desired outcomes:**
1. Reporting takes 30 minutes not 4 hours (functional)
2. Stop dreading Mondays (emotional)
3. Look efficient and capable to manager (social)

---

### Ring 3: Perceived Barriers

**Concerns:**
- "I'm not technical—will I be able to set this up?"
- "Is this within my budget authority?" (need to get approval)
- "What if the numbers don't match what I've been reporting?"

---

### Ring 4: Decision Criteria

**Must-haves:**
1. No-code setup
2. Pre-built report templates
3. Easy to learn (not complex)

**How they compare:**
- Search YouTube for tutorials
- Look for "easy to use" in reviews
- Free trial required

---

### Marketing Implications

**Messaging:**
- "Your weekly report in 5 minutes"
- "No Excel required"
- "So easy, you'll set it up in an afternoon"

**Where to reach:**
- YouTube tutorials
- "Best [category] for beginners" content
- Marketing career newsletters

**Who they influence:**
- They don't buy, but they recommend to their manager (Persona 1)

---

### Example 2: Consumer Product Personas

**Input:**
> "We're launching a premium meal prep service ($150/week). Create personas based on these 8 customer interviews."

**Interview Summary:**
- 4 were working professionals who said "no time to cook"
- 2 were new parents who said "eating garbage since baby came"
- 2 were fitness-focused who said "need macro-specific meals"

**Output:**

## PERSONA 1: The Burned-Out Professional

### Snapshot
| Aspect | Detail |
|--------|--------|
| **Role** | Professional, 28-40, demanding job (consulting, finance, tech) |
| **Environment** | Urban, long hours, high income, limited personal time |
| **Primary JTBD** | Eat healthy without sacrificing career performance |
| **Current Solution** | Takeout, occasional HelloFresh (but doesn't cook it) |

---

### Ring 1: Priority Initiative

**Triggers:**
- Doctor says cholesterol is high
- Gained 10 lbs since starting new job
- Realized they've eaten takeout 5 days straight
- Friend looks great and asks what they're doing

**Why now:**
- Health scare or milestone birthday
- New Year's resolution
- Partner commented on their diet

**Quotes:**
> "I know I should eat better. I've tried cooking on Sunday but I'm so tired by the weekend I just don't."

---

### Ring 2: Success Factors

**Desired outcomes:**
1. Eat healthy meals without effort (functional)
2. Stop feeling guilty about my diet (emotional)
3. Look like I have my life together (social)

**What success looks like:**
- "I eat real food without thinking about it"
- "I have energy in the afternoon"

---

### Ring 3: Perceived Barriers

**Concerns:**
1. "$150/week feels expensive" (but they spend that on takeout)
2. "What if I don't like the food?"
3. "Will it actually fit my schedule?"

**Anxiety:**
- "Another subscription I'll cancel in a month"
- "Food delivery quality—will it be fresh?"

**Quotes:**
> "I've tried Blue Apron twice. Both times I ended up with a fridge full of rotting ingredients."

---

### Ring 4: Decision Criteria

**Must-haves:**
1. Zero cooking required (key!)
2. Healthy (real ingredients, balanced macros)
3. Variety (won't get bored)

**Nice-to-haves:**
- Customization for preferences
- Delivery flexibility

**Deal-breakers:**
- Any cooking/prep required
- Only healthy "rabbit food"
- Long subscription commitment

---

### Ring 5: Buyer's Journey

1. See friend on Instagram eating nice meal
2. Ask them about it or Google "meal delivery no cooking"
3. Compare 2-3 options on website, check reviews
4. Trial week to test
5. Subscribe if trial worked

**Timeline:** Same-week decision for trial

---

### Marketing Implications

**Messaging:**
- "Eat like you have a personal chef"
- "Zero prep. Zero cleanup. Real food."
- "For people too busy to cook but too smart to eat garbage"

**Where to reach:**
- Instagram (lifestyle/food content)
- Podcasts (business, productivity)
- LinkedIn (target by industry)

**What NOT to say:**
- "Meal kits" (sounds like cooking)
- "Diet food" (sounds restrictive)

---

## PERSONA 2: The Optimized Athlete

(Abbreviated for space)

### Key Differences from Persona 1

| Aspect | Burned-Out Professional | Optimized Athlete |
|--------|------------------------|-------------------|
| Primary JTBD | Eat healthy without effort | Hit my macros precisely |
| Trigger | Health concern, guilt | Competition coming, plateau |
| Success Factor | Convenience | Performance/results |
| Decision Criteria | No cooking | Macro transparency |
| Barrier | "Another subscription" | "Will macros be accurate?" |
| Messaging | "Zero effort" | "Fuel your performance" |

---

## Checklists & Templates

### Persona Interview Questions

```
## Customer Interview Guide for Persona Development

### Trigger (Priority Initiative)
- "What was happening when you first started looking for [solution]?"
- "Why now? Why not 6 months ago?"
- "What was the trigger event?"
- "What finally pushed you to do something?"

### Success Factors
- "What did you hope would change after buying?"
- "How would you know if this worked?"
- "If this was perfect, what would that look like?"
- "What would success mean for you personally?"

### Barriers (Perceived Risks)
- "What concerns did you have before buying?"
- "What almost made you NOT buy?"
- "What worries did you have about making a change?"
- "What would failure look like?"

### Decision Criteria
- "What was most important to you in evaluating options?"
- "What features were must-haves?"
- "What made you choose us over alternatives?"
- "What would have been a deal-breaker?"

### Buyer's Journey
- "How did you first hear about this category?"
- "What did you research? Where?"
- "Who else was involved in the decision?"
- "How long from first search to purchase?"
```

---

### Persona Validation Score

```
## Persona Quality Score

**Persona:** _______________

| Criteria | Score (1-5) | Notes |
|----------|-------------|-------|
| Based on real interviews (not assumptions) | | |
| Includes verbatim quotes | | |
| Explains triggers (why now) | | |
| Explains decision criteria | | |
| Surfaces real anxieties | | |
| Maps buyer's journey | | |
| Includes JTBD statement | | |
| Distinct from other personas | | |
| Marketing team can use it | | |
| Sales team can use it | | |

**Total:** __/50

- 40+: Ready to use
- 30-39: Needs more research
- <30: Start over with customer interviews
```

---

### Quick Persona Card

```
## [Persona Name]

**One-liner:** [Job title] who [key behavior] because [primary motivation].

**Trigger:** They start looking when ________________________________

**Job-to-be-Done:** "When I [situation], I want to [motivation], so I can [outcome]."

**Top 3 Decision Criteria:**
1.
2.
3.

**Biggest Anxiety:** ________________________________

**We win by:** ________________________________
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

- Revella, Adele. "Buyer Personas" (2015) - Five Rings methodology
- Christensen, Clayton. "Competing Against Luck" (2016) - Jobs-to-be-Done
- Ulwick, Tony. "What Customers Want" (2005) - Outcome-Driven Innovation
- Blank, Steve. "The Four Steps to the Epiphany" (2005) - Customer archetypes
- Klement, Alan. "When Coffee and Kale Compete" (2016) - JTBD for product

## Related Skills

- [jobs-to-be-done](../../strategy/jobs-to-be-done/) - Deep dive on JTBD theory
- [buyer-personas](../../strategy/buyer-personas/) - Original Adele Revella framework
- [mom-test](../mom-test/) - How to interview customers for persona research
- [customer-discovery](../customer-discovery/) - Systematic validation methodology
- [audience-research](../../strategy/audience-research/) - Broader audience understanding

---

## Skill Metadata (Internal Use)

```yaml
name: persona-generator
category: validation
subcategory: customer-research
version: 1.0
author: MKTG Skills
source_expert: Adele Revella, Clayton Christensen
source_work: Buyer Personas, Competing Against Luck
difficulty: intermediate
estimated_value: $3,000 persona research project
tags: [personas, customer-research, JTBD, buyer-personas, segmentation, YC]
created: 2026-01-25
updated: 2026-01-25
```
