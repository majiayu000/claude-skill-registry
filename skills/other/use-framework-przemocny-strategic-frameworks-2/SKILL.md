---
name: use-framework
description: Apply strategic frameworks through facilitated workshop dialogue. Use when user selected framework via choose-framework; explicitly requests specific framework; knows which framework to apply; or needs structured guidance. Conducts 30-60 minute workshops guiding step-by-step through framework application. Creates workshop documents in .frameworks-output/ folder.
---

# Use Framework - Strategic Framework Application

## Overview

This skill guides users through applying strategic frameworks step-by-step via facilitated workshop dialogue. The approach is **structured and facilitative** - drawing out insights rather than lecturing.

**Core principles:**
- **Facilitative, not directive** - Draw out user's thinking, don't dictate answers
- **Structured application** - Follow framework phases rigorously
- **Natural dialogue** - Workshop-style conversation, not rigid template
- **Challenge assumptions** - Push for depth, not surface answers
- **Actionable outputs** - Every workshop ends with concrete recommendations

**Output:** Framework workshop document saved to `.frameworks-output/[session-name]/framework-workshop.md`

---

## Workflow

### Phase 1: Setup & Context (5-10 minutes)

**Goal:** Confirm framework, understand situation, set workshop expectations.

**Steps:**

1. **Identify framework:**
   - If provided as argument: Use that framework
   - If user mentioned in message: Extract and confirm
   - If unclear: "Which framework would you like to use?"

2. **Load framework definition:**
   - Read from `references/frameworks/[number]-[framework-name].md`
   - Understand structure, phases, and key questions
   - Examples: `14-design-thinking.md`, `07-jobs-to-be-done.md`, `21-regret-minimization-framework.md`

3. **Gather situation context:**
   - "Tell me about the situation you're applying this to"
   - "What are you trying to achieve?"
   - Listen for: Problem, goals, constraints, urgency

4. **Set workshop expectations:**

```markdown
# Workshop: [Framework Name]

## What is this framework?
[2-3 sentences from framework file]

## What we'll accomplish
[2-3 concrete outcomes]

## How this works
We'll work through [X] phases of this framework:
1. [Phase 1 name]
2. [Phase 2 name]
3. [Phase X name]

I'll ask questions for each phase, we'll explore together, and at the end you'll have clear insights and action items.

Ready? Let's start with [Phase 1].
```

### Phase 2: Framework Introduction (5-10 minutes)

**Goal:** Explain framework structure so user knows what to expect.

**What to cover:**

1. **Framework origin:**
   - Who created it (person/organization)
   - When and why
   - Famous applications

2. **Framework structure:**
   - Main phases/steps
   - What each phase accomplishes
   - How they connect

3. **Quick example:**
   - Brief real-world example relevant to user's context
   - "For instance, when Airbnb used Design Thinking to redesign their listing photos..."

4. **Answer questions:**
   - "Any questions about how this framework works?"
   - Clarify before diving into application

### Phase 3: Guided Application (20-40 minutes)

**Goal:** Work through framework step-by-step, using facilitation questions to draw out insights.

**General approach for all frameworks:**

**For each framework phase:**

1. **Introduce phase:**
   - "Let's move to [Phase Name]"
   - "The goal here is to [phase objective]"

2. **Ask facilitation questions:**
   - Use questions from framework file
   - Use supplementary questions from `references/facilitation-questions.md`
   - Ask ONE question or small group (2-3) at a time
   - Wait for user response before continuing

3. **Probe deeper:**
   - Challenge surface-level answers: "Can you be more specific?"
   - Explore examples: "Give me a concrete example"
   - Test assumptions: "How do you know that?"
   - Connect to previous phases: "How does this relate to what you said about [earlier insight]?"

4. **Capture insights:**
   - Acknowledge good insights: "That's important - [insight]"
   - Make connections: "This connects to [earlier point]"
   - Note patterns: "I'm seeing a pattern of [theme]"

5. **Flag pitfalls:**
   - Use `references/common-pitfalls.md` to warn proactively
   - "A common mistake here is [pitfall]. Let's make sure we avoid that by [action]"

6. **Transition between phases:**
   - Summarize: "So for [Phase], we identified [key points]"
   - Check understanding: "Does this resonate? Anything to add?"
   - Move forward: "Ready for [Next Phase]?"

**How to navigate:**

1. **Follow framework structure strictly** - Don't skip or reorder phases
2. **Adapt depth to engagement** - If user is deeply engaged, go deeper
3. **Use workshop guide** - Consult `references/workshop-guide.md` for facilitation patterns
4. **Check pitfalls** - Use `references/common-pitfalls.md` throughout
5. **Time management** - Balance depth with covering all phases
6. **Document as you go** - Note key insights for final summary

**Reference files to consult:**
- `references/frameworks/[framework-file].md` - Framework structure and questions
- `references/workshop-guide.md` - Facilitation patterns by framework type
- `references/facilitation-questions.md` - Question library for workshops
- `references/common-pitfalls.md` - Framework-specific pitfalls to avoid

**Dialogue style:**

**Good examples:**
- "Walk me through exactly how that would work" (demand specificity)
- "What assumptions are you making there?" (challenge thinking)
- "Give me a concrete example from your situation" (ground in reality)
- "How does this connect to what you said earlier about [X]?" (create synthesis)

**Bad examples:**
- Lecturing about the framework instead of facilitating
- Accepting vague answers without probing
- Rushing through phases to "finish"
- Not connecting insights across phases

**Key facilitation tactics:**

**1. Draw out thinking (don't provide answers):**
- "What do you think about [X]?"
- "How would you approach [Y]?"
- "What's your intuition here?"

**2. Challenge surface-level answers:**
- "That sounds reasonable, but let's dig deeper. What specifically..."
- "Can you be more specific about [vague statement]?"
- "Give me a concrete example"

**3. Use silence strategically:**
- After asking good question, pause
- Let user think
- Don't rush to fill silence

**4. Make connections:**
- "This relates to what you said earlier about [X]"
- "I'm seeing a pattern: [theme]"
- "How does this [insight] affect [earlier decision]?"

**5. Celebrate insights:**
- "That's a key insight: [restate]"
- "This is important because [why it matters]"
- "I want to make sure we capture this: [insight]"

**6. Warn about pitfalls proactively:**
- "A common trap here is [pitfall]. Let's avoid that by [approach]"
- "Many people skip [step] but it's crucial because [reason]"

### Phase 4: Analysis & Insights (5-10 minutes)

**Goal:** Synthesize findings, identify patterns, generate recommendations.

**Steps:**

1. **Synthesize across framework:**
   - "Let's look at what emerged across all phases"
   - Identify themes and patterns
   - Connect insights

2. **Key insights:**
   - "The most important insights are..."
   - Explain why each matters
   - Prioritize by impact

3. **Generate recommendations:**
   - Based on framework application
   - Actionable and specific
   - Prioritized by importance/urgency

4. **Define next steps:**
   - Immediate actions (this week)
   - Short-term initiatives (this month/quarter)
   - Long-term considerations

5. **Create workshop document:**
   ```
   .frameworks-output/[session-name]/
   └── framework-workshop.md
   ```

**Document structure:**

```markdown
# Framework Workshop: [Framework Name]

## Framework Overview
- **Framework:** [Name]
- **Creator:** [Who]
- **Applied to:** [User's situation]
- **Date:** [Date]

## Your Situation
[2-3 paragraphs describing context, problem, goals]

## Framework Application

### Phase 1: [Phase Name]
**Goal:** [Phase objective]

**What we explored:**
- [Question/topic 1]
- [Question/topic 2]

**Key findings:**
- [Finding 1]
- [Finding 2]
- [Finding 3]

**Insights:**
[Important realizations or patterns from this phase]

---

### Phase 2: [Phase Name]
[Same structure for each phase]

---

[Continue for all framework phases]

## Key Insights

### 1. [Major Insight 1]
[Explanation of why this matters and what it means]

### 2. [Major Insight 2]
[Explanation]

### 3. [Major Insight 3]
[Explanation]

## Patterns & Themes

[Overarching patterns that emerged across multiple phases]

## Recommendations

### Immediate Actions (This Week)
1. [Action 1 with specifics]
2. [Action 2 with specifics]
3. [Action 3 with specifics]

### Short-term Initiatives (This Month/Quarter)
1. [Initiative 1]
2. [Initiative 2]
3. [Initiative 3]

### Long-term Considerations
1. [Consideration 1]
2. [Consideration 2]

## Success Metrics

How will you know this is working?
- [Metric 1]
- [Metric 2]
- [Metric 3]

## Warnings & Pitfalls to Avoid

- ⚠️ [Pitfall 1 specific to this framework]
- ⚠️ [Pitfall 2]
- ⚠️ [Pitfall 3]

## Next Steps

**Immediate:** [What to do right away]

**Follow-up:** [When to revisit this framework or apply complementary one]

---

*Framework applied: [Date]*
*Session: [session-name]*
```

6. **Review with user:**
   - "Here's what we accomplished..."
   - "Does this capture what emerged?"
   - "Anything to add or refine?"

### Phase 5: Wrap-up (2-5 minutes)

**Goal:** Ensure clarity and offer next actions.

**Steps:**

1. **Summarize key takeaways:**
   - "The most important things we discovered..."
   - "Your next actions are..."

2. **Offer follow-up options:**
   - "Want to apply a different framework to this situation for another perspective?"
   - "Need to explore one phase deeper?"
   - "Ready to document this in a different format?"

3. **Encourage action:**
   - "The framework is just the start - the value comes from acting on these insights"
   - "What's the first thing you'll do based on this?"

---

## Framework-Specific Adaptations

Different framework types require different facilitation styles:

### Strategic Frameworks
(Porter's Five Forces, Blue Ocean, Wardley Mapping, SWOT)

**Focus on:**
- Analysis and positioning
- Competitive dynamics
- Market forces
- Strategic options

**Facilitation style:**
- Analytical and thorough
- Challenge assumptions about competition
- Push for evidence and data
- Connect analysis to strategic choices

**Common pitfalls:**
- Analysis paralysis (too much thinking, no action)
- Ignoring execution challenges
- Assuming static environment

### Mental Models
(Munger's Mental Models, First Principles, Second-Order Thinking, Inversion)

**Focus on:**
- Thinking patterns
- Cognitive biases
- Perspective shifts
- Fundamental truths

**Facilitation style:**
- Philosophical and probing
- Challenge conventional wisdom
- Explore edge cases
- Connect to real decisions

**Common pitfalls:**
- Staying too abstract (not grounding in specifics)
- Overthinking simple decisions
- Paralysis by analysis

### Decision Frameworks
(OODA Loop, Cynefin, Pre-Mortem, Eisenhower Matrix, Pareto)

**Focus on:**
- Options and criteria
- Trade-offs and risks
- Decision process
- Action orientation

**Facilitation style:**
- Pragmatic and action-focused
- Force prioritization
- Explore consequences
- Push for commitment

**Common pitfalls:**
- Premature closure (deciding too fast)
- Confirmation bias
- Ignoring low-probability/high-impact risks

### Innovation Frameworks
(Design Thinking, Jobs-to-be-Done, Lean Startup, Six Thinking Hats)

**Focus on:**
- User needs and empathy
- Experimentation and iteration
- Rapid prototyping
- Learning from feedback

**Facilitation style:**
- Creative and exploratory
- Encourage wild ideas
- Push for prototypes over perfect plans
- Emphasize learning over being right

**Common pitfalls:**
- Skipping user research
- Falling in love with solution
- Overbuilding before testing
- Ignoring business viability

### Operational Frameworks
(Theory of Constraints, OKR, Pareto Principle, Systems Thinking)

**Focus on:**
- Execution and processes
- Metrics and measurement
- Resource allocation
- System optimization

**Facilitation style:**
- Practical and metric-driven
- Focus on bottlenecks
- Push for measurable outcomes
- Connect to business results

**Common pitfalls:**
- Metric gaming (optimizing wrong things)
- Losing sight of strategy
- Over-optimizing current state
- Ignoring people/culture factors

---

## Special Cases

### Framework Not in Library

If user requests framework not in `references/frameworks/`:

1. **Check if it exists:** Look in `references/frameworks/` folder
2. **Suggest discover-framework:** "I don't have [Framework] yet. Want to use `/discover-framework` to research and add it?"
3. **Offer alternative:** "The closest framework I have is [Alternative]. Would that work?"

### User Wants to Skip Phases

If user says "Let's skip to [later phase]":

**Response:** "Each phase builds on previous ones. Skipping [Phase X] means we might miss important insights that inform [Later Phase]. Let's at least do a quick pass through it. Should take [X] minutes."

**Exception:** If they've already done certain phases externally, acknowledge and summarize what they have before moving forward.

### User Stuck on One Phase

If user struggles with specific phase:

1. **Rephrase questions** - Try different angle
2. **Provide examples** - "For instance, when company X..."
3. **Break down further** - "Let's take that step by step"
4. **Acknowledge difficulty** - "This is often the hardest part"
5. **Offer to move on and return** - "Let's explore [Next Phase] and come back to this"

### Workshop Taking Too Long

If exceeding expected time:

**Options:**
1. **Increase pace:** "Let's move a bit faster through remaining phases"
2. **Focus on essentials:** "Let's focus on the most critical aspects"
3. **Pause and resume:** "Want to pause here and resume later?"
4. **Document progress:** "Let me capture what we have so far"

---

## Output Quality Checklist

Before finalizing workshop document, verify:

- [ ] Completed all framework phases (didn't skip steps)
- [ ] Asked facilitation questions (not just surface exploration)
- [ ] Captured specific insights from user (not generic statements)
- [ ] Identified patterns and themes across phases
- [ ] Generated actionable recommendations (not vague advice)
- [ ] Prioritized next steps (immediate, short-term, long-term)
- [ ] Flagged common pitfalls for this framework type
- [ ] Created framework-workshop.md with complete documentation
- [ ] Reviewed document with user for accuracy

---

## Key Reminders

1. **Facilitate, don't lecture** - Draw out user's thinking
2. **Follow framework structure** - Don't skip or reorder phases
3. **Ask, don't tell** - Questions are your primary tool
4. **Challenge surface answers** - Push for depth and specificity
5. **Connect insights** - Synthesize across phases
6. **Flag pitfalls proactively** - Warn before user falls into common traps
7. **Document thoroughly** - Create comprehensive workshop record
8. **End with action** - Concrete next steps, not just insights

---

## References

- `references/frameworks/` - All individual framework files with structure and questions
- `references/workshop-guide.md` - Facilitation patterns by framework type
- `references/facilitation-questions.md` - Question library for workshops
- `references/common-pitfalls.md` - Framework-specific pitfalls and how to avoid them
