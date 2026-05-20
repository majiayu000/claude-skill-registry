---
name: problem-interview
description: "Validate that the problem you want to solve is real, painful, and worth solving before building anything. Master Cindy Alvarez's structured approach to problem discovery interviews. Use when: **Before solution interviews** to confirm the problem exists; **Early customer discovery** to understand the problem space; **Pivoting** to find new problems worth solving; **Market expansion** to understand problems in new segments; **Feature prioritization** to validate which problems matter most"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Problem Interview

> Validate that the problem you want to solve is real, painful, and worth solving before building anything. Master Cindy Alvarez's structured approach to problem discovery interviews.

## When to Use This Skill

- **Before solution interviews** to confirm the problem exists
- **Early customer discovery** to understand the problem space
- **Pivoting** to find new problems worth solving
- **Market expansion** to understand problems in new segments
- **Feature prioritization** to validate which problems matter most
- **Hypothesis testing** to validate or invalidate problem assumptions

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | Cindy Alvarez - "Lean Customer Development" (2014) |
| **Core Principle** | "Problem interviews help you understand the problem space before committing to a solution. You're not pitching—you're learning." |
| **Why This Matters** | Most startups fail because they solve problems people don't care enough about. Problem interviews prevent building solutions to non-problems. |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Structures problem exploration** - Systematic approach to understanding pain points
2. **Identifies problem severity** - Distinguishes "nice to have" from "must solve"
3. **Discovers existing solutions** - Understands what people do today
4. **Validates problem frequency** - How often does this problem occur?
5. **Finds problem context** - When and where does the problem happen?
6. **Generates solution hints** - What would ideal look like?

## How to Use

### Prepare Problem Interview Script
```
I want to validate this problem hypothesis: [problem statement]
Target customer: [who]
Create a problem interview script with open-ended questions.
```

### Analyze Problem Interview Results
```
I conducted [X] problem interviews. Here's what I learned: [summary]
Analyze whether the problem is validated.
What should I do next?
```

### Design Problem Interview Experiment
```
Help me design a problem interview experiment to test:
Hypothesis: [problem hypothesis]
Target: [customer segment]
Sample size and success criteria needed.
```

## Instructions

### Step 1: Define Your Problem Hypothesis

```
## Problem Hypothesis Template

### The Problem Statement
"I believe [customer segment] has a problem with [problem area]
because [reason/observation]."

### Assumptions to Validate
| # | Assumption | Confidence | Evidence |
|---|------------|------------|----------|
| 1 | The problem exists | Low/Med/High | None yet |
| 2 | The problem is frequent (happens often) | Low/Med/High | None yet |
| 3 | The problem is severe (causes real pain) | Low/Med/High | None yet |
| 4 | People are actively seeking solutions | Low/Med/High | None yet |
| 5 | Current solutions are inadequate | Low/Med/High | None yet |

### What Would Invalidate This?
- If fewer than [X%] mention this problem unprompted
- If the problem happens less than [frequency]
- If severity rating is below [threshold]
- If people aren't spending time/money to solve it
```

---

### Step 2: Structure the Problem Interview

```
## Problem Interview Framework

### Interview Goals
1. Understand the CONTEXT where the problem occurs
2. Measure the SEVERITY of the problem
3. Discover EXISTING SOLUTIONS they use
4. Identify FREQUENCY of the problem
5. Find the COST (time, money, emotion) of the problem

### Interview Structure (30 minutes)

**Part 1: Context Setting (5 min)**
- "Tell me about your role and what you're responsible for..."
- "Walk me through a typical day/week..."
- Goal: Understand their world before diving into problems

**Part 2: Problem Exploration (15 min)**
- "What are the biggest challenges you face with [area]?"
- "Tell me about the last time [problem] happened..."
- "What was the hardest part about that?"
- "How often does this happen?"
- Goal: Deep dive into problem, frequency, severity

**Part 3: Current Solutions (7 min)**
- "How do you handle this today?"
- "What have you tried in the past?"
- "What works? What doesn't?"
- "What do you wish existed?"
- Goal: Understand competitive landscape from customer view

**Part 4: Impact & Close (3 min)**
- "How much time/money does this cost you?"
- "If this problem disappeared, what would change?"
- "Who else deals with this that I should talk to?"
- Goal: Quantify impact, get referrals
```

---

### Step 3: Ask Non-Leading Questions

```
## Problem Interview Questions

### Opening Questions (Broad to Specific)
"I'm researching how [people like you] handle [problem area].
I'm not selling anything—just trying to understand the reality."

### Problem Discovery Questions

**Existence:**
- "What's the most frustrating part of [area]?"
- "Walk me through the last time you dealt with [problem]..."
- "What keeps you up at night about [area]?"

**Frequency:**
- "How often does [problem] happen?"
- "When was the last time? The time before that?"
- "Is this daily? Weekly? Monthly?"

**Severity:**
- "On a scale of 1-10, how painful is this?"
- "What happens if you don't solve this?"
- "How does this affect your [work/life/business]?"

**Emotional Impact:**
- "How does it feel when this happens?"
- "What emotions come up when you deal with this?"
- "What would it mean to you to solve this?"

### Existing Solution Questions

**Current Behavior:**
- "How do you handle this today?"
- "What tools/processes do you use?"
- "Walk me through your current workflow..."

**Past Attempts:**
- "What have you tried before?"
- "What worked? What didn't?"
- "Why did you stop using [previous solution]?"

**Ideal State:**
- "If you had a magic wand, what would you change?"
- "What would the perfect solution look like?"
- "What would need to be true for this to be solved?"

### Impact Questions

**Quantification:**
- "How much time do you spend on this per week?"
- "How much does this cost you?" (direct and indirect)
- "What's the opportunity cost of not solving this?"

**Urgency:**
- "Is solving this a priority? Why/why not?"
- "What would make it urgent?"
- "Have you looked for solutions recently?"

### DON'T Ask These

❌ "Would you use a product that...?" (leading)
❌ "Don't you think [solution] would help?" (leading)
❌ "Is [feature] important to you?" (leading)
❌ "Would you pay for...?" (hypothetical, save for later)
```

---

### Step 4: Measure Problem Severity

```
## Problem Severity Assessment

### During Interview - Probe for:

**Time Cost:**
- "How much time do you spend on this?"
- Convert to $ (hourly rate × time)

**Money Cost:**
- Direct costs (tools, services, fixes)
- Indirect costs (opportunity cost, delays)

**Emotional Cost:**
- Frustration level
- Impact on job satisfaction
- Stress and worry

### Severity Scoring Framework

| Signal | Low (1-3) | Medium (4-6) | High (7-10) |
|--------|-----------|--------------|-------------|
| Frequency | Rarely | Monthly/weekly | Daily |
| Time spent | Minutes | Hours | Days |
| Money impact | <$100/mo | $100-1000/mo | >$1000/mo |
| Emotional | Annoyed | Frustrated | Distressed |
| Action taken | None | Some searching | Actively seeking |
| Budget allocated | None | Considering | Has budget |

### Severity Evidence

**Strong validation signals:**
- They brought up the problem before you asked
- They got emotional when describing it
- They've already spent money trying to solve it
- They can quantify the impact precisely
- They asked if you have a solution

**Weak validation signals:**
- Only mentioned when directly asked
- Vague about impact ("it's kind of annoying")
- Never tried to solve it
- Can't quantify the cost
- No urgency in their voice
```

---

### Step 5: Analyze and Decide

```
## Problem Interview Analysis

### Interview Summary Template

**Interview #[X]**
**Date:** _______________
**Participant:** [Role, Company type]

| Question Area | Response Summary | Severity (1-10) |
|---------------|------------------|-----------------|
| Problem existence | | |
| Frequency | | |
| Current solution | | |
| Impact/cost | | |
| Urgency | | |

**Key Quotes:**
- "[Verbatim quote about the problem]"
- "[Quote about severity/impact]"

**Observed Emotions:**
- [ ] Frustrated [ ] Stressed [ ] Resigned [ ] Energized when discussing
- [ ] No emotional reaction (weak signal)

---

### Aggregate Analysis (After 10+ Interviews)

| Metric | Target | Actual | Validated? |
|--------|--------|--------|------------|
| Mentioned problem unprompted | >50% | | |
| Average severity score | >7/10 | | |
| Currently spending to solve | >30% | | |
| Would prioritize solving | >50% | | |
| Can quantify impact | >60% | | |

### Decision Framework

**VALIDATED - Proceed to Solution Interviews if:**
- [ ] 7+ of 10 mentioned problem unprompted
- [ ] Average severity > 7/10
- [ ] Multiple people already spending on solutions
- [ ] Clear patterns in problem description
- [ ] Consistent emotional response

**NOT VALIDATED - Pivot if:**
- [ ] Fewer than 5 of 10 recognize the problem
- [ ] Severity consistently < 5/10
- [ ] No one is actively trying to solve it
- [ ] Wide variance in problem descriptions
- [ ] "Nice to have" language dominates

**NEEDS MORE RESEARCH if:**
- [ ] Mixed signals (some strong, some weak)
- [ ] Different sub-segments show different patterns
- [ ] Problem exists but may not be the ONE to solve
```

---

## Examples

### Example 1: B2B Problem Interview

**Input:**
> "I want to validate that marketing managers struggle with tracking campaign ROI across channels. Create a problem interview script."

**Output:**

## Problem Interview Script: Marketing Campaign ROI

**Hypothesis:** Marketing managers at mid-size B2B companies struggle to track and report campaign ROI across multiple channels.

### Opening (2 min)
"Thanks for chatting. I'm researching how marketing teams handle performance measurement. I'm not selling anything—just trying to understand the reality. Mind if I ask some questions about how you track marketing results?"

### Context Setting (3 min)
1. "Tell me about your role. What are you responsible for?"
2. "How does your company measure marketing success?"
3. "What tools are in your marketing stack?"

### Problem Exploration (12 min)

**Existence:**
4. "What's the hardest part about measuring marketing performance?"
5. "Walk me through what happened the last time your CEO asked about marketing ROI..."
6. "How do you currently answer the question 'what's working and what's not?'"

**Frequency:**
7. "How often do you need to report on marketing performance?"
8. "How much time do you spend on this each week/month?"

**Severity (probe deeper):**
9. "What happens when you can't answer a ROI question?"
10. "Tell me about a time when lack of visibility caused a problem..."
11. "On a scale of 1-10, how frustrating is this part of your job?"

### Current Solutions (8 min)
12. "How do you handle this today? Walk me through your process..."
13. "What tools do you use for reporting?"
14. "What's good about your current approach?"
15. "What's frustrating about it?"
16. "Have you tried other solutions? What happened?"

### Impact & Close (5 min)
17. "If you had perfect visibility into ROI, what would change?"
18. "Is solving this a priority for you right now? Why or why not?"
19. "What would need to be true for this to become urgent?"
20. "Who else on your team deals with this that I should talk to?"

### Notes to Self
- Listen for: emotional language, specific examples, quantified impact
- Red flags: vague answers, "it's fine," no urgency
- Strong signals: they've tried to solve it, they can quantify the cost

---

### Example 2: Problem Interview Analysis

**Input:**
> "I did 12 problem interviews about freelancer financial planning. Here's my summary. Is the problem validated?"

**Summary provided:**
- 9/12 said they "should" be better at finances
- 6/12 mentioned tax season stress
- 4/12 currently use any tool
- Most said they use spreadsheets or nothing
- Average severity: 5.5/10
- Only 2 were actively looking for solutions

**Output:**

## Problem Interview Analysis

### Scorecard

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Problem recognition | >70% | 75% (9/12) | ✅ |
| Average severity | >7/10 | 5.5/10 | ❌ |
| Active solution seeking | >30% | 17% (2/12) | ❌ |
| Currently paying for solutions | >30% | 33% (4/12) | ⚠️ |

### Diagnosis: **PARTIALLY VALIDATED**

**What's validated:**
- People RECOGNIZE they have a problem (9/12)
- There's a specific pain point (tax season)
- Low tool adoption = opportunity exists

**What's NOT validated:**
- Severity is too low (5.5 vs. 7+ target)
- Very few actively seeking solutions (2/12)
- Language was "should" not "must" (obligation, not urgency)

### Key Insight
This is a **known problem but not a felt problem**. People know they "should" be better at finances, but it's not painful enough to drive action. This is typical of "vitamin" problems (nice to have) vs. "painkiller" problems (must have).

### Recommendations

**Option 1: Find the Acute Pain Point**
- The 6 who mentioned tax season stress: dig deeper
- Is there a specific trigger moment where it becomes urgent?
- "Walk me through what happened last April 14th..."
- Maybe the problem is "tax season panic" not "financial planning"

**Option 2: Find a Different Segment**
- The 2 actively seeking: who are they? What's different?
- High-earning freelancers (more at stake)?
- Freelancers who just got a tax surprise?
- Find the segment where severity IS 8+

**Option 3: Pivot Problem**
- What else did they say was painful?
- Maybe financial planning isn't the problem
- Maybe "irregular income stress" or "late invoices" is more acute

### Next Steps
1. Interview 5 more people who just went through tax season
2. Interview the 2 who were actively looking—understand why
3. Ask: "What's the MOST stressful financial moment you've had this year?"

Don't proceed to solution interviews until severity > 7/10 for a defined segment.

---

### Example 3: Problem Severity Deep Dive

**Input:**
> "In my problem interviews, people say 'yeah, that's annoying' but I'm not sure if it's severe enough. How do I probe deeper?"

**Output:**

## Severity Probing Techniques

### The "5 Whys" Approach
Keep asking "why" until you hit real pain:

**Surface:** "Yeah, tracking my expenses is annoying."

Probe 1: "Why is that annoying?"
→ "Because I have to collect receipts from everywhere."

Probe 2: "Why does that cause problems?"
→ "Because I miss deductions at tax time."

Probe 3: "Why does missing deductions matter?"
→ "I probably overpaid taxes by $3,000 last year."

Probe 4: "How does that affect you?"
→ "That's money I could have invested or taken as vacation."

Probe 5: "What would it mean to get that $3,000 back?"
→ "That's literally a trip to Europe. I think about it every time I do my taxes."

**Now we have:** Specific pain ($3,000), emotional weight (thinks about it), tangible impact (lost vacation).

### The "Worst Case" Technique
"What's the worst that happens if this isn't solved?"

**Surface:** "I don't get great reports from my tools."

Probe: "What's the worst case scenario if this continues?"
→ "I guess the CEO will keep asking questions I can't answer."

Probe: "What happens then?"
→ "Eventually they'll question if marketing is worth the investment."

Probe: "And then?"
→ "Budget cuts. Or I get blamed when sales dips and we can't prove marketing works."

**Now we have:** Job security fear, budget protection, accountability pressure.

### The "Money" Technique
Always try to quantify:

"You mentioned this takes time. Can you quantify it?"
→ "Maybe 5 hours a week."

"If your loaded cost is $80/hour, that's $20K/year just on this task. Does that sound right?"
→ "Oh wow, I never thought about it that way. Yeah, that's... a lot."

### The "Emotion" Technique
Listen for and probe emotions:

Them: "It's frustrating."

You: "Frustrating how? Walk me through what that feels like in the moment."
→ "I'm stressed. I'm rushing. My boss is waiting. I'm digging through spreadsheets at 10pm because I can't get the data I need during the day."

**Now we have:** Stress, time pressure, work-life impact.

### Severity Validation Signals

| Signal | What It Means |
|--------|---------------|
| They quantify without prompting | They've thought about this a lot |
| They get emotional | This really bothers them |
| They've tried multiple solutions | Active problem-solver |
| They ask if you have a solution | Ready to buy |
| They offer to pay for early access | Validated |
| They refer you to others | Community pain |

---

## Checklists & Templates

### Problem Interview Prep Checklist

```
## Before the Interview

□ Problem hypothesis written down
□ Assumptions to validate listed
□ Interview questions prepared
□ Note-taking system ready
□ Recording permission (if recording)
□ 30 minutes blocked

## During the Interview

□ Don't mention your solution
□ Ask open-ended questions
□ Let them do 70%+ of talking
□ Probe on severity (5 whys)
□ Get specific examples, not generalities
□ Listen for emotional language
□ Quantify impact (time, money)
□ Ask for referrals

## After the Interview

□ Write summary within 1 hour
□ Extract key quotes
□ Score severity (1-10)
□ Note signals (strong/weak)
□ Update hypothesis based on learnings
```

---

### Problem Interview Tracking Sheet

```
| # | Date | Participant | Problem Confirmed? | Severity | Active Seeking? | Key Quote |
|---|------|-------------|-------------------|----------|-----------------|-----------|
| 1 | | | Y/N | 1-10 | Y/N | |
| 2 | | | Y/N | 1-10 | Y/N | |

**Running Analysis:**
- Problem confirmation rate: ___%
- Average severity: __/10
- Active seeking rate: ___%
- Validation status: Validated / Not Yet / Needs Pivot
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

- Alvarez, Cindy. "Lean Customer Development" (2014) - Problem interview methodology
- Fitzpatrick, Rob. "The Mom Test" (2013) - Questioning techniques
- Blank, Steve. "The Four Steps to the Epiphany" (2005) - Customer development
- Torres, Teresa. "Continuous Discovery Habits" (2021) - Ongoing discovery

## Related Skills

- [mom-test](../mom-test/) - Questioning techniques for honest answers
- [solution-interview](../solution-interview/) - Next step after problem validation
- [customer-discovery](../customer-discovery/) - Broader validation framework
- [persona-generator](../persona-generator/) - Understanding who has the problem
- [jobs-to-be-done](../../strategy/jobs-to-be-done/) - Understanding the underlying need

---

## Skill Metadata


- **Mode**: cyborg
```yaml
name: problem-interview
category: validation
subcategory: customer-research
version: 1.0
author: MKTG Skills
source_expert: Cindy Alvarez
source_work: Lean Customer Development
difficulty: beginner
estimated_value: $1,500 customer research training
tags: [validation, interviews, customer-discovery, problems, startups, YC]
created: 2026-01-25
updated: 2026-01-25
```
