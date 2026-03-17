---
name: choose-framework
description: Select the right strategic framework for your situation through exploratory dialogue. Use when user describes a problem, decision, or challenge; needs structured thinking approach; mentions "strategy", "decision", or "problem-solving"; or asks "how should I think about this?". Creates framework selection briefs in .frameworks-output/ folder.
---

# Choose Framework - Strategic Framework Selection

## Overview

This skill helps users select the right strategic framework for their situation through facilitated exploratory dialogue. The approach is **structured and evidence-based** - matching frameworks to problems using proven selection criteria.

**Core principles:**
- **Evidence-based selection** - Match frameworks to situations based on proven criteria
- **Exploratory dialogue** - Understand context deeply before recommending
- **Multiple options** - Present 2-3 frameworks with reasoning
- **Natural conversation** - Conversational flow, not rigid questionnaire
- **Clear reasoning** - Explain *why* each framework fits

**Output:** Framework selection brief saved to `.frameworks-output/[session-name]/framework-selection.md`

---

## Workflow

### Phase 1: Initial Understanding (5-10 minutes)

**Goal:** Understand user's situation, problem, and context.

Start with open questions:
- "Tell me about the situation or problem you're facing"
- "What are you trying to achieve or decide?"
- "What's the context?" (startup, corporation, personal, career)

**Listen for:**
- Problem type (strategic, operational, innovation, decision)
- Situation context (stable, changing, uncertain, complex)
- User's role and constraints
- Urgency and timeline
- Stakeholders involved

**Set expectations early:**
"I'll ask some questions to understand your situation, then recommend 2-3 frameworks that fit best. Sound good?"

### Phase 2: Deep Exploration (10-20 minutes)

**Goal:** Systematically explore 6 key dimensions to match framework to situation.

**Key Dimensions (explore all 6):**

1. **Problem Type**
   - Strategic decision (long-term direction)
   - Operational issue (process, execution)
   - Innovation challenge (new product, service, approach)
   - Decision-making need (choice between options)

2. **Situation Context**
   - Stable (clear cause-effect)
   - Changing (evolving, competitive)
   - Uncertain (multiple unknowns)
   - Complex (interconnected, emergent)

3. **Time Horizon**
   - Immediate (days/weeks)
   - Short-term (months)
   - Long-term (years)

4. **Stakeholders**
   - Who's involved?
   - Who's affected?
   - Who needs to buy in?

5. **Data Availability**
   - Rich data available
   - Some data, some assumptions
   - Mostly unknowns

6. **Implementation Complexity**
   - Simple (individual action)
   - Moderate (team effort)
   - Complex (organizational change)

**How to navigate:**

1. **Ask questions one at a time** - Don't bombard with a list
2. **Use discovery questions** from `references/discovery-questions.md`
3. **Follow interesting threads** - If user reveals something important, explore it
4. **Consult selection guide** - Use `references/framework-selection-guide.md` for category details
5. **Check warnings** - Use `references/framework-warnings.md` to identify mismatches
6. **Mark uncertainties** - Note what's unclear

**Reference files to consult:**
- `references/frameworks-index.md` - Complete framework catalog with keywords
- `references/framework-selection-guide.md` - Deep dive on selection dimensions
- `references/discovery-questions.md` - Question library for exploration
- `references/framework-warnings.md` - Warning signs and mismatches

**Dialogue style:**

**Good examples:**
- "What specifically are you trying to decide?" (clarify problem type)
- "How much is changing in your market/situation?" (assess context)
- "Who else is affected by this decision?" (identify stakeholders)
- "What data do you have vs what are assumptions?" (understand information)

**Bad examples:**
- Jumping to framework recommendation too quickly
- Not exploring context deeply enough
- Recommending frameworks user has heard of vs best fit
- Failing to explain *why* framework matches

**Key tactics:**

**1. Clarify problem type:**
- Is this about long-term strategy or immediate execution?
- Are you innovating or optimizing?
- Making a decision or solving a problem?

**2. Assess situation complexity:**
Use Cynefin-like thinking:
- Clear = Simple frameworks (Eisenhower Matrix, Pareto)
- Complicated = Analytical frameworks (Porter's Five Forces, SWOT)
- Complex = Sense-making frameworks (Cynefin, Systems Thinking)
- Chaotic = Fast-cycle frameworks (OODA Loop)

**3. Match to role and context:**
- **Founders/CEOs:** Mental Models, Regret Minimization, First Principles
- **Product Managers:** Jobs-to-be-Done, Design Thinking, RICE
- **Strategists:** Porter's Five Forces, Blue Ocean, Wardley Mapping
- **Operations:** Theory of Constraints, Pareto, Systems Thinking

**4. Consider time horizon:**
- **Immediate:** OODA Loop, Eisenhower Matrix, Pareto
- **Short-term:** Design Thinking, Lean Startup, Pre-Mortem
- **Long-term:** Regret Minimization, Scenario Planning, Wardley Mapping

**5. Identify warning signs:**
From `references/framework-warnings.md`:
- Framework too complex for situation (using McKinsey 7S for personal decision)
- Wrong framework type (using strategic framework for operational problem)
- Insufficient data (using quantitative framework without data)

### Phase 3: Framework Recommendation (5-10 minutes)

**Goal:** Present 2-3 best-fit frameworks with clear reasoning.

**Structure your recommendation:**

```markdown
# Recommended Frameworks for Your Situation

## Your Situation Summary
[2-3 sentences capturing key dimensions]

---

## 1. [Framework Name] - PRIMARY RECOMMENDATION

**Why it fits:**
- [Reason 1 based on problem type]
- [Reason 2 based on situation context]
- [Reason 3 based on constraints]

**What you'll gain:**
- [Concrete benefit 1]
- [Concrete benefit 2]
- [Concrete benefit 3]

**What it requires:**
- [Time commitment]
- [Data/information needed]
- [Who should be involved]

**Next step:**
Use `/use-framework [framework-name]` to apply it to your situation.

---

## 2. [Framework Name] - STRONG ALTERNATIVE

**Why it fits:**
- [Reason 1]
- [Reason 2]

**When to choose this over #1:**
[Specific conditions where this is better]

**Next step:**
Use `/use-framework [framework-name]` if this resonates more.

---

## 3. [Framework Name] - WORTH CONSIDERING

**Why it might be useful:**
- [Reason 1]
- [Reason 2]

**Best for:**
[Specific scenario or phase where this helps]

---

## ⚠️ Considerations

[Any warnings or important notes about framework application]

## What We Explored

- **Problem Type:** [Strategic/Operational/Innovation/Decision]
- **Context:** [Stable/Changing/Uncertain/Complex]
- **Timeline:** [Immediate/Short/Long-term]
- **Stakeholders:** [Who's involved]
- **Data:** [Rich/Moderate/Limited]
- **Complexity:** [Simple/Moderate/Complex]
```

**Follow-up:**
"Which framework resonates most with your situation? I can guide you through applying it with `/use-framework [name]`, or we can explore alternatives if none of these feel right."

### Phase 4: Wrap-up and Next Steps (2-5 minutes)

**Goal:** Create selection brief and offer next actions.

**Steps:**

1. **Propose session name** based on situation
   - Use kebab-case: `competitive-strategy-analysis`, `product-prioritization-decision`
   - Keep it descriptive

2. **Create framework selection brief:**
   ```
   .frameworks-output/[session-name]/
   └── framework-selection.md
   ```

3. **Document structure:**
   - Situation analysis (all 6 dimensions)
   - Recommended frameworks (with reasoning)
   - Alternative frameworks considered
   - Selection criteria applied
   - Warnings and considerations
   - Next steps

4. **Offer transition:**
   - "Ready to apply [Framework]? Let's use `/use-framework [name]`"
   - "Want to explore a different framework? I can explain the alternatives"
   - "Need to refine understanding first? Let's talk more about [dimension]"

---

## Framework Matching Logic

### By Problem Type

**Strategic (long-term direction):**
- Blue Ocean Strategy, Porter's Five Forces, Wardley Mapping, Scenario Planning, Ansoff Matrix, BCG Matrix

**Operational (execution, processes):**
- Theory of Constraints, Pareto Principle, OKR Framework, Systems Thinking, OODA Loop

**Innovation (new products/services):**
- Design Thinking, Lean Startup, Jobs-to-be-Done, First Principles, Blue Ocean Strategy

**Decision (choosing between options):**
- Mental Models, Regret Minimization, Pre-Mortem, Second-Order Thinking, Cynefin Framework

### By Situation Context

**Stable (clear environment):**
- SWOT Analysis, Porter's Five Forces, Eisenhower Matrix, Pareto Principle

**Changing (competitive, evolving):**
- OODA Loop, Wardley Mapping, Blue Ocean Strategy, Scenario Planning

**Uncertain (many unknowns):**
- Lean Startup, Pre-Mortem Analysis, Scenario Planning, Inversion Thinking

**Complex (interconnected):**
- Cynefin Framework, Systems Thinking, Mental Models, First Principles

### By Time Horizon

**Immediate (days/weeks):**
- OODA Loop, Eisenhower Matrix, Pareto Principle, Six Thinking Hats

**Short-term (months):**
- Design Thinking, Lean Startup, RICE Framework, OKR Framework

**Long-term (years):**
- Regret Minimization, Wardley Mapping, Scenario Planning, Business Model Canvas

### By Role

**CEO / Founder:**
- Regret Minimization, Mental Models, First Principles, Porter's Five Forces, Blue Ocean Strategy

**Product Manager:**
- Jobs-to-be-Done, Design Thinking, Lean Startup, RICE Framework, Kano Model

**Strategist:**
- Porter's Five Forces, Wardley Mapping, Scenario Planning, BCG Matrix, McKinsey 7S

**Operations Manager:**
- Theory of Constraints, Pareto Principle, OKR Framework, Systems Thinking

**Tech Leader / CTO:**
- Wardley Mapping, First Principles, Systems Thinking, Theory of Constraints

---

## Special Cases

### User Knows Framework They Want

If user asks for specific framework (e.g., "I want to use Design Thinking"):

1. **Validate fit:** "Let me understand your situation first to make sure Design Thinking is the best fit"
2. **Quick assessment:** Ask 2-3 key questions about context
3. **Confirm or suggest alternative:**
   - If good fit: "Yes, Design Thinking is perfect for this because [reasons]. Let's use it."
   - If poor fit: "Design Thinking could work, but [Framework X] might be better because [reasons]. Which do you prefer?"

### No Framework Fits Well

If none of the 48 frameworks seem right:

1. **Offer closest match:** "The closest fit is [Framework], though it's not perfect"
2. **Suggest combination:** "This might need combining [Framework A] for [aspect] and [Framework B] for [aspect]"
3. **Offer discover-framework:** "I don't have a perfect framework for this. Want to use `/discover-framework` to research and add one?"

### User Wants Multiple Frameworks

If user asks "Should I use multiple frameworks?":

**Answer:** "It depends on complexity. Generally:
- Start with ONE framework to avoid confusion
- Apply it fully first
- Then consider complementary framework for different aspect
- Example: Porter's Five Forces (competitive analysis) → Blue Ocean Strategy (positioning)"

---

## Output Quality Checklist

Before finalizing recommendation, verify:

- [ ] Explored all 6 dimensions (problem, context, time, stakeholders, data, complexity)
- [ ] Recommended 2-3 frameworks (not just 1)
- [ ] Explained WHY each framework fits (not just what it is)
- [ ] Considered alternatives and explained trade-offs
- [ ] Identified potential warnings or mismatches
- [ ] Created framework-selection.md with full reasoning
- [ ] Offered clear next step (use-framework)

---

## Key Reminders

1. **Don't rush to recommendation** - Explore situation deeply first
2. **Match evidence-based** - Use selection criteria, not popularity
3. **Explain reasoning** - Always say WHY framework fits
4. **Offer alternatives** - Give user choice, not just one answer
5. **Warn about mismatches** - If framework is imperfect fit, say so
6. **Natural dialogue** - Conversational exploration, not interrogation
7. **Document reasoning** - Save selection process to framework-selection.md
8. **Transition smoothly** - Offer to apply framework via use-framework

---

## References

- `references/frameworks-index.md` - All 48 frameworks with descriptions, categories, keywords
- `references/framework-selection-guide.md` - Deep dive on selection dimensions and criteria
- `references/discovery-questions.md` - Question library for exploring situation
- `references/framework-warnings.md` - Warning signs for mismatches and poor fits
