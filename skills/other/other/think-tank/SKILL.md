---
name: think-tank
agent: explore
context: fork
description: "Collaborative exploration and reasoning frameworks. Use when ideas need shaping, decisions need analysis, or requirements need clarification. Includes l'entonnoir questioning, incremental validation, YAGNI, and 12 reasoning techniques. Not for execution when path is clear or analysis is complete."
---

<mission_control>
<objective>Turn vague intent into validated direction through collaborative exploration and reasoning</objective>
<success_criteria>Intent clarified, framework applied if needed, actionable direction delivered</success_criteria>
</mission_control>

## Quick Start

**If user intent is vague:** Use l'entonnoir questions → Validate incrementally → Apply YAGNI

**If analysis is needed:** Route to reasoning framework → Execute technique → Deliver insight

**If unsure what to use:** Ask "What are you trying to do?" with options

## Navigation

| If you need... | Read this section... |
| :------------- | :------------------- |
| Collaborative exploration | ## PATTERN: L'Entonnoir Workflow |
| Reasoning frameworks | ## PATTERN: Intent Router |
| 12 technique details | ## PATTERN: Technique Reference |
| Common mistakes | ## ANTI-PATTERN: Common Mistakes |
| Quality check | ## Recognition Questions |

## PATTERN: L'Entonnoir Workflow

**Collaborative exploration for vague intent:**

1. **Clarify Intent** → Present 2-4 recognition-based options, each with tradeoffs
2. **Explore Context** → Quick project state check (existing patterns, stack)
3. **Validate Incrementally** → Present design in 200-300 word sections
4. **Apply YAGNI** → Strip speculative features

### Question Flow

Start broad, narrow progressively:

```
"What type of project?"
→ "What specific capability?"
→ "What integration needs?"
→ "What constraints matter?"
```

### Incremental Validation

Present sections one at a time:

```
**Architecture**

[200-300 words]

"Does this direction work, or adjust?"

[Wait for confirmation before proceeding]
```

### YAGNI Check

For each feature proposed:
- "Is this needed now, or speculative?"
- "What's the minimum to achieve the goal?"
- "What can we defer?"

## PATTERN: Intent Router

**Route to reasoning framework when analysis is the goal:**

| User Asks... | Use... |
| :----------- | :----- |
| "Why is this happening?" | 5 Whys |
| "What matters most?" | Pareto |
| "What could go wrong?" | Inversion |
| "Pros and cons?" | SWOT |
| "How will this feel long-term?" | 10/10/10 |
| "What's the one key thing?" | The One Thing |
| "What's really happening?" | Occam's Razor |
| "And then what?" | Second Order |
| "What should I do first?" | Eisenhower Matrix |
| "What am I giving up?" | Opportunity Cost |
| "What should I remove?" | Via Negativa |
| "What's the fundamental truth?" | First Principles |

### When Multiple Apply

Select the most appropriate technique based on analysis of the user's intent. Consider:

1. What is the core problem or question?
2. What outcome does the user need?
3. Which technique directly addresses this?

Trust your judgment—the AI agent can infer and select appropriately.

## PATTERN: Technique Reference

### 5 Whys

Drill to root cause.

**Output:** Problem → 5 levels of "why" → Root cause → Intervention

### Pareto

Find vital few (~20% driving ~80%).

**Output:** High-impact factors to focus on → Low-impact to deprioritize

### Inversion

What would guarantee failure?

**Output:** Failure modes → Avoidance strategies → "Never do" boundaries

### SWOT

Internal strengths/weaknesses, external opportunities/threats.

**Output:** 4-quadrant map → SO/WO/ST/WT strategic moves

### 10/10/10

Evaluate across time horizons.

**Output:** Each option at 10min / 10months / 10years → Time conflicts → Recommendation

### The One Thing

Single highest-leverage action.

**Output:** Goal → Candidate actions → Leverage point → Immediate next action

### Occam's Razor

Simplest explanation fitting all facts.

**Output:** Explanations with assumptions → Evidence check → Simplest valid

### Second Order

Consequences of consequences.

**Output:** First-order → Second-order → Third-order → Revised assessment

### Eisenhower Matrix

Urgent/important prioritization.

**Output:** Q1 (Do First) → Q2 (Schedule) → Q3 (Delegate) → Q4 (Eliminate)

### Opportunity Cost

What you give up.

**Output:** Resources required → Best alternative uses → True cost → Verdict

### Via Negativa

Improve by removing.

**Output:** Current state → Subtraction candidates → What to keep → After subtraction

### First Principles

Rebuild from fundamentals.

**Output:** Assumptions challenged → Fundamental truths → Rebuilt understanding → New possibilities

## ANTI-PATTERN: Common Mistakes

### Mistake 1: Questions Without Tradeoffs

❌ "What framework do you want?"

✅ "What type of project? (a) API, (b) Web app, (c) CLI - each has different stack implications"

### Mistake 2: Validating Too Much at Once

❌ "Here's the complete design"

✅ Present 200-300 words at a time, confirm each section

### Mistake 3: Accepting Speculative Features

❌ "We might need X later"

✅ "Build only what's needed now. Later = later."

### Mistake 4: Analysis Without Action

❌ "Here's a SWOT analysis"

✅ SWOT → Strategic moves → What to do next

### Mistake 5: Skipping Context

❌ "What database?" without checking existing stack

✅ Check existing patterns first, then propose options

## Recognition Questions

| Question | Check |
| :------- | :---- |
| Intent clarified? | L'entonnoir questions narrowed scope |
| Options had tradeoffs? | Each option explained implications |
| Design validated incrementally? | Sections confirmed one at a time |
| YAGNI applied? | Speculative features stripped |
| Framework matched intent? | Router used, technique appropriate |
| Output was actionable? | Specific next step identified |

---

<critical_constraint>
**Portability Invariant**: Zero external dependencies. Works standalone.

**Delta Standard**: Instructions assume basic reasoning competence. Don't explain what reasoning entails—apply it.
</critical_constraint>
